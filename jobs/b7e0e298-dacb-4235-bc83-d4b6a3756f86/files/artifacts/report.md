# Ethereum ERC-20 Bag gacha: evidence, mechanism and launch design

Research date: **13 October 2026 (UTC)**. Scope: read-only research and design; no deployment, signatures, approvals, paid oracle requests or transactions were sent. This report includes an offline economic model, not production Solidity or an audit.

**Recommendation.** Build a small, ownerless pilot with a separately funded ETH reserve, request-time TWAP commitments, one outstanding draw, and fee-funded depositor rewards. Start at **0.10 ETH per spin**, with **92% token-value EV / 90.16% cashout EV before wallet gas**, and **50 ETH of irrevocable reserve capital**. Make low liquidity, insufficient reserve and unsuitable inventory reject new spins mechanically. Do not launch until the capital, oracle integration, gas benchmarks and independent security review exist.

The concept is economically possible, but its ETH payouts do not come from the ERC-20 collateral itself. FWA depositors supply ETH backing; Bag depositors do not. A token launch or a positive expected house margin does not substitute for cash reserves. Also, paying both the depositor and the spinner on a cashout would make this design lose money. The exclusive settlement rules below are essential.

**Evidence labels.** **Observed** means a read made for this report, with block or saved data. **Documented** means the project/provider states it, not that every implementation detail was audited. **Reported** means an incident account with incomplete independent verification. **Design** means a recommendation. **Model** means a result conditional on explicit assumptions. **Unresolved** identifies a remaining uncertainty. Parameters in the proposed design are not FWA parameters.

## 1. What Fake World Assets actually does

### Deployments and version boundaries

**Documented:** current FWA documentation distinguishes its V1 main pool from V2, which starts at block **25,944,480**. Both use the same FWA token and hook. Do not conflate the exploited early launch, the July relaunch now documented as V1, and the present V2. V1 positions and claims remain with their original contracts; this is not an in-place proxy migration. [V1 guide](https://www.fwa.fun/docs/v1), [V2 deployments](https://www.fwa.fun/docs/v2-deployments).

| Component | Ethereum address |
|---|---|
| V1 main pool | [0xB276F62DB0ce8CA2Ca5bc522695bE604521eAc1c](https://etherscan.io/address/0xB276F62DB0ce8CA2Ca5bc522695bE604521eAc1c) |
| V1 rewards | [0x6a1a1C0CfB3D3C538e13D36d608a5bcaa992fc78](https://etherscan.io/address/0x6a1a1C0CfB3D3C538e13D36d608a5bcaa992fc78) |
| V1 VRF service | [0xa084c33Fb7a467307452898b8D58165ebd2E5D9f](https://etherscan.io/address/0xa084c33Fb7a467307452898b8D58165ebd2E5D9f) |
| Shared FWA ERC-20 | [0xa0Df17B5aC76ABaBA36E1450E2cbCd18A620C845](https://etherscan.io/address/0xa0Df17B5aC76ABaBA36E1450E2cbCd18A620C845) |
| Shared Uniswap v4 hook | [0x2C67ebA8A50AF0dB5Fba55F725247a75CbDA6444](https://etherscan.io/address/0x2C67ebA8A50AF0dB5Fba55F725247a75CbDA6444) |
| Existing V1 ERC-20 pack wrapper | [0x727C739F07A89f11E883FE0F34937c55e4c3d74A](https://etherscan.io/address/0x727C739F07A89f11E883FE0F34937c55e4c3d74A) |
| V1 FWAIR launch manager | [0x900252d9A8F9AcC3DD1014C594c91fC33e5A6AAf](https://etherscan.io/address/0x900252d9A8F9AcC3DD1014C594c91fC33e5A6AAf) |
| V2 main pool | [0x958C41181182e76F221331b2755b77D9e1426A98](https://etherscan.io/address/0x958C41181182e76F221331b2755b77D9e1426A98) |
| V2 rewards | [0xA54b44C7a894AA19C49734A753D01f9B8C5f6516](https://etherscan.io/address/0xA54b44C7a894AA19C49734A753D01f9B8C5f6516) |
| V2 buyback | [0xaba91665cdf921F0f6B33A099337336B324c9793](https://etherscan.io/address/0xaba91665cdf921F0f6B33A099337336B324c9793) |
| V2 VRF service | [0xCACBd874e24B533935176154E990Bf710F56693A](https://etherscan.io/address/0xCACBd874e24B533935176154E990Bf710F56693A) |
| V2 floor oracle | [0xaA4D9009a4664604b57644bF13e447E9036727DC](https://etherscan.io/address/0xaA4D9009a4664604b57644bF13e447E9036727DC) |
| V2 whitelist authority | [0x0ad3128429242007D58952c65546BA99b9b70146](https://etherscan.io/address/0x0ad3128429242007D58952c65546BA99b9b70146) |
| V2 FWAIR launch manager | [0x716486a7bD6B4d7409fC4F8B52f0B23D2BcFac72](https://etherscan.io/address/0x716486a7bD6B4d7409fC4F8B52f0B23D2BcFac72) |

Address attribution: [official V1 deployment catalogue](https://www.fwa.fun/docs/deployments) and [official V2 catalogue](https://www.fwa.fun/docs/v2-deployments). Campaign children must be discovered through their version's manager. The existing wrapper is explicitly described as owner-curated ERC-20 denominations; merely wrapping fungible assets is therefore not a novel distinction. The proposed differences are TWAP valuation, no depositor ETH backing, fixed spin price and constrained IMD curation.

**Observed:** at finalized block **26,181,994**, hash `0x7f749dfd50c5427c690e957623b22f7edf56fd0e45760e101861e722ad1b1c55`, timestamp **2026-10-13 07:12:23 UTC**, V1 had **685** active listings and V2 **3,553**. Both returned owner `0x019817ad02a31b990433542097be29d97613e8cb`. Their runtime lengths were 21,425 and 24,390 bytes. These are code-presence/getter observations, not source-to-bytecode verification or proof of safety. See [block](https://etherscan.io/block/26181994), respective contract links above, and saved `research/onchain-snapshot.json`.

### Deposit, price, selection and settlement

**Documented:** a depositor supplies an NFT **and ETH backing B**. Selection weight is approximately `1e36/B`; it measures backing, not NFT appraisal. Active listings receive equal shares of distributable acquisition ETH, while token rewards use square-root backing. An allocated listing is reserved until settlement. [Positions and weighting](https://www.fwa.fun/docs/prizes-odds).

**Documented:** the acquisition price floats with weighted expected backing, approximately the harmonic mean, plus a surcharge. VRF service charges are separate. Requests process in sequence; new deposits stage while requests are unresolved, and cannot reshape an earlier request. The current docs specify VRF v2.5 with native subscription payment. Refunded/expired acquisitions earn no purchaser reward. [Pricing and allocation](https://www.fwa.fun/docs/pricing-draw).

**Documented settlement:** keeping the NFT returns the depositor's own backing less a settlement fee; accepting its standing bid pays the purchaser from that backing and returns the NFT to the depositor. Keeping and relisting requires fresh backing. There are separate ETH and FWA cashout rates. The purchaser has an exclusive choice interval, followed by depositor/public resolution paths. This is not a promise that an NFT sells for its backing. [Settlement](https://www.fwa.fun/docs/winning).

V2 adds floor-based backing ceilings, initially ask plus 10%, a challenge-based floor oracle that also admits owner-set manual quotes, collection exemptions, scheduled purchase blackouts and a 12-hour crown commitment. These are mutable/privileged features, not the ownerless model requested here. [V2 overview](https://www.fwa.fun/docs/v2).

### Fees, reward token and destinations

**Documented V1 reference, not immutable terms:** 2.5% acquisition surcharge; 1% protocol acquisition cut; 1% NFT-outcome settlement cut; 90% standing bid; 1% crown tithe; 3 request confirmations; purchaser choice for one hour and public finalization after 24 hours. Published V1 routing sends 100% of protocol cuts to token buying, then 60%/20%/20% to purchaser rewards/depositor rewards/burn. These settings should not be retroactively applied to July or to V2. [V1 guide and settings](https://www.fwa.fun/docs/v1).

**Observed live distinction:** both pool getters returned 100 bps acquisition and NFT settlement cuts and 9,000 bps ETH bid rates at the pinned block. V2's token bid getter returned **9,150 bps**, whereas documentation describes **9,250 bps as a default**. The FWA cashout example below independently uses 91.5%. A default is not a live quote. The current quoted pool acquisition fees were approximately **0.029633 ETH V1** and **0.064545 ETH V2**, excluding VRF. [V2 contract](https://etherscan.io/address/0x958C41181182e76F221331b2755b77D9e1426A98#readContract), [settlement defaults](https://www.fwa.fun/docs/winning).

**Documented V2 fee destinations:** acquisition fees first cover the protocol cut and crown allocation; the remaining distributable ETH goes equally to active listings. NFT-outcome fees and retained cashout spreads are distinct; cashout does not additionally charge the NFT-outcome fee. Early voluntary crown exit costs 1% of backing. [Fee accounting](https://www.fwa.fun/docs/fees).

**Documented V2 buybacks:** permissionless fee payout funds a separate executor; executing a buyback is another action. Its stated source defaults are 40% depositor rewards, 40% purchaser rewards and 20% burn, with up to 1 ETH per execution and a 0.5% caller incentive. These are explicitly configurable defaults. Shared token-market trading fees are a separate stream; documentation describes a planned 64/8/8/20 recipient split, not evidence that the wiring was executed. Live recipient balances/splitter configuration were not audited here. [Buybacks and fee routing](https://www.fwa.fun/docs/fwa-buybacks).

**Documented original FWA allocation:** 50% market liquidity, 30% fifteen-day incentives split equally between depositors and purchasers, 20% snapshot claim for block 25,452,023. Market trading fees are 1%. Original emissions ended; subsequent rewards can be financed by existing tokens and buybacks. [FWA token overview](https://www.fwa.fun/docs/fwa).

**Documented rewards:** square-root backing determines depositor token weight; each successful acquisition earns a purchaser epoch share. Purchaser epochs must close and resolve pending requests before claims. Repricing/removal checkpoints accrued rewards. The docs also describe funded fifteen-day rewards for the current pool, but this report did not verify a V2 emission funding/start transaction; do not infer V2 rewards from V1's emission dates. [Earning and claiming](https://www.fwa.fun/docs/fwa-rewards).

### Transaction examples, checked against receipts

**Observed:** all examples below have successful receipts. ABI event layouts came from FWA's published frontend bundle; matching request/listing IDs establishes the linked flow, not a full execution-trace audit. Hashes, calldata, log data and receipt gas are in `research/onchain-snapshot.json`.

| Action | Evidence and interpretation |
|---|---|
| Deposit/list | [0x8be6…a6af](https://etherscan.io/tx/0x8be6e151e351b03ee03fcb64802c1a9e34cad7daf57762eacb1cb4c80d65a6af), block 26,181,982: listing 83,849, NFT #695 of `0x6e6b13a7ff06b53dcc3589d35b1b0ffd58c5bdeb`, backing **0.034 ETH**. Receipt gas 710,587. |
| Request | [0xb627…92c9](https://etherscan.io/tx/0xb62702034ca3e5e6cc4c5458e36430117b9c8e5db42f2eb36109ccd521b092c9), block 26,181,965: pool acquisition fee **0.064551875216807254 ETH**, transaction value **0.06792358196047961 ETH**. Difference alone is not a trace-level fee allocation. Gas 485,778. |
| VRF result and allocation | [0xec94…e580](https://etherscan.io/tx/0xec949e2a59123494e63432c7cf14653d6be0d8a22ee1b31b781e7605f14be580), block 26,181,970: same request ID as above, sequence 76,354; cached random word and allocated listing **83,715**, backing **0.0429 ETH**. Gas 589,854. |
| ETH cashout of that listing | [0xa407…97d5](https://etherscan.io/tx/0xa40729b79ca4fb49c74026d1b0746051bad4a268342f5027cae57b9aeb6197d5), block 26,181,975: **0.03861 ETH payout + 0.00429 ETH retained**, exactly 90/10. Gas 137,836. |
| Token cashout | [0x4d99…bd79](https://etherscan.io/tx/0x4d99dd84baa44e596be5474164dc1b76e6fb32e06177e63ee76bb4ccdb09bd79): listing 78,995; 0.02745 ETH token-buy budget, 0.00255 ETH retained; about **5,535.6123 FWA** output. Budget is 91.5% of 0.03 ETH, not a guaranteed FWA resale value. |
| Keep | [0x5035…0c13](https://etherscan.io/tx/0x5035b707cdb614fe3c376627542610e05707d24180e8d474c779c084a0e0ca13): listing 80,213; event reports **0.07425 ETH** backing returned. Purchaser and depositor addresses coincide. This proves a self-acquisition example, not profitable wash farming. |
| Fee routing | [0xb5a5…e1c6](https://etherscan.io/tx/0xb5a520679b9ac9b58706ad7a09f1be57af5b38a7c26e309e8bdd8bc6a8ece1c6): `ProtocolFeesToBuyback` directs **0.003948415001734457 ETH** to V2's executor. Funding it is not proof a swap occurred in this transaction. |

**Observed VRF wiring:** both main pools returned coordinator `0xD7f86b4b8Cae7D942340FF628F82735b7a20893a`, the 200-gwei key hash and a 900,000 callback gas limit. Subscription IDs are saved as full returned words in the snapshot, avoiding truncation. Chainlink lists this coordinator for Ethereum v2.5. [Supported networks](https://docs.chain.link/vrf/v2-5/supported-networks).

### FWAir is funding and distribution, not free inventory

**Documented:** artists escrow a collection and supporters supply ETH backing. A randomized fraction becomes direct supporter NFT awards; remaining positions enter FWA. Direct awards give the artist the backing. When a pool buyer keeps a recognized launch NFT, backing returns to its supporter; when the buyer cashes out, the supporter gets the NFT. Campaign failures have refund/recovery paths. Launch recognition is listing-specific. [FWAIR overview](https://www.fwa.fun/docs/fwair-launch).

FWAIR adds no separate campaign fee in the current guide. Artists earn listing ETH fees; supporters share harvested FWA rewards with one share per originally supported position, not one share per ETH. Recognized launch NFT-keep outcomes waive the pool's owner settlement fee; early crown exits can still charge. Supporter backing does not finance campaign randomness. [Fund flows](https://www.fwa.fun/docs/fwair-fund-flows). The Bag design should not import this funding arrangement unless supporters expressly accept inventory and capital risk.

### Exploit, farming and what happened after emissions

**Reported incident, not replayed:** founder Adam's July 3 post describes front-running a Chainlink callback to shift the selected NFT and unfairly acquire CryptoPunk #5450. The original post is linked but direct retrieval was denied; the founder's statement was inspected as embedded in contemporary reporting. It is evidence of an application-state selection failure, not evidence Chainlink's random-number proof was broken. Full exploit transaction reconstruction and remediation audit are unresolved. [Founder statement](https://x.com/Rhynotic/status/2073038964299092048), [retrieval context](https://www.banklesstimes.com/articles/2026/07/03/chainlink-callback-exploit-hits-tokenworks-cryptopunk-lost/).

**Inference from documented incentives:** paying purchasers per successful pull and depositors per square-root backing can subsidize repeated play; splitting capital into more equally backed listings increases aggregate square-root weight. Over-backing an unattractive NFT can reduce selection frequency while collecting listing income. V2's ceiling and crown commitment address related incentives, but that does not prove an individual farmer exploited them. No verified list of profitable farming wallets or comprehensive exploit catalogue was established. The self-acquisition receipt above is deliberately not labelled proof of an exploit.

**Observed emission endpoint:** V1 rewards `emissionStart()` returned **2026-07-20 19:01:23 UTC**; `EMISSION_DAYS()` returned 15. Their sum is **2026-08-04 19:01:23 UTC**. Reads are pinned to the snapshot block. [V1 rewards contract](https://etherscan.io/address/0x6a1a1C0CfB3D3C538e13D36d608a5bcaa992fc78#readContract).

**Observed activity after that endpoint:** archival logs were counted over complete UTC windows; dates below are inclusive. The metric is `AcquisitionRequested` and its `acquisitionFee`, **before refunds**, not settled sales, total transaction count, net fees, or profit. `research/collect_activity.py` reproduces it with read-only RPC; `research/activity-windows.json` preserves exact boundary blocks/hashes and sample logs.

| UTC window | Pool | Requests | Gross request acquisition ETH |
|---|---|---:|---:|
| July 28–August 3 | V1 | 38,532 | 4,130.4463 |
| August 5–11 | V1 | 17,808 | 1,439.4670 |
| August 12–18 | V1 | 9,272 | 742.9815 |
| October 6–12 | V1 | 115 | 4.9679 |
| October 6–12 | V2 | 10,722 | 798.3974 |

Evidence is attributable to the [V1 event-emitting contract](https://etherscan.io/address/0xB276F62DB0ce8CA2Ca5bc522695bE604521eAc1c#events) and [V2 contract](https://etherscan.io/address/0x958C41181182e76F221331b2755b77D9e1426A98#events). The first post-emission week shows **53.8% fewer requests and 65.1% less gross request ETH** than the preceding full week. These comparisons establish contraction, not causation: fee changes, token prices, user mix and later version changes are confounders.

**Independent measurement source, not independently reproduced accounting:** DefiLlama's downloaded parent-protocol daily-fee series averaged **$404,685/day** July 28–August 3, **$109,161/day** August 5–11, **$37,351/day** August 12–18 and **$83,146/day** October 6–12. Its peak in the retrieved series was **$1,631,833 on July 25**. October includes V2; October 13 is incomplete and excluded. Saved numeric series: `research/fee-series.json`. [Series endpoint](https://api.llama.fi/summary/fees/fake-world-assets?dataType=dailyFees), [dashboard](https://defillama.com/protocol/fake-world-assets).

The adapter nets cashouts against acquisition income and includes settlement categories. Its historical comments still mention 85% bids, illustrating why labels and current settings cannot replace log-level accounting. This report inspected the methodology but did not recalculate every USD fee. [V1 measurement code](https://github.com/DefiLlama/dimension-adapters/blob/master/fees/fwa/index.ts), [V2 measurement code](https://github.com/DefiLlama/dimension-adapters/blob/master/fees/fwa-v2/index.ts).

**Conclusion from evidence:** original emissions ending coincided with a substantial activity decline, but FWA did not cease operating. Continued V2 activity is not proof of sustainable unsubsidized demand: the reward streams and product changed. The Bag recommendation therefore assumes no launch emissions and no token-price appreciation.

## 2. Proposed Bag mechanism

Everything in this section is **Design**, unless explicitly sourced. The objective is honest displayed odds and funded commitments, not uninterrupted spinning through every market condition.

### Assets, rights and lifecycle

A Bag is an ERC-721 containing **one to four distinct ERC-20s**, immutable quantities after sealing. Sort addresses and reject duplicates, zero quantities and unsupported decimals. The depositor transfers actual tokens from their wallet; mint only after all balance deltas equal the requested amounts. No leverage, borrowing, shared depositor collateral or rehypothecation. The independent BagNFT vault owns the ERC-20s; the BagPool owns listed NFTs. Token balances backing Bags never count as reserve ETH.

`seal → unlisted Bag → list/staged → eligible → draw-locked → allocated → keep OR cashout`.

An unlisted Bag may trade freely. Its holder can burn it to create per-component withdrawal entitlements and claim the tokens separately. A failed or later-blacklisted component must not lock unrelated components; claim rights persist after burning. A listed Bag cannot trade because the pool holds it. Listing rights and accrued dividends belong to the recorded depositor, not whoever later receives the NFT.

Listing requires current whitelist approval, exact custody, safe oracle inputs, maximum Bag value and a **24-hour maturation** after its latest seal/list operation. During maturation it earns nothing and cannot be selected. Rewards begin only on activation. Maximum active inventory is **64 Bags / 8 distinct underlying tokens**; excess inventory waits outside the active set. Reject further listings at a bounded staging cap instead of maintaining an unbounded queue. No dilution by unactivated listings.

A depositor commits to at least **24 hours after activation**, then may signal an exit with **one hour's notice**. The intent immediately excludes it from *future* snapshots; an already committed draw retains its original rights. On expiry, return the NFT without an ETH penalty if it was not selected. Pause/delist waives the minimum residence and notice for uncommitted positions. An assigned winner or an unresolved randomness request remains committed. Depositor withdrawal never creates a right to reserve ETH at a historical price.

**Liveness tradeoff:** an unresolved VRF request locks the eligible inventory snapshot until it resolves. There is deliberately no timeout reroll or selective refund. A permanent coordinator failure can strand those listed Bags. Outside-pool Bags and existing ETH/token credits remain withdrawable. This is a material limit of the proposed immutable pilot, not a solved recovery mechanism. If unconditional timed exits are a product requirement, redesign and review the randomness/commitment mechanism before launch.

### Valuation: define the time before revealing randomness

“Draw time” means **the accepted request transaction's commitment time**, not the later fulfillment or keeper processing time. Evaluate all Bag contents then, store the resulting values/weights and immutable inventory version, and issue VRF in the same transaction. The spinner accepts that price timestamp. Never reprice or change eligibility after the random word becomes visible. Fulfillment-time pricing would give validators, keepers or curators control over the mapping from randomness to prizes.

Use canonical **Uniswap v3 token/WETH pools**, with an explicit exception `WETH = 1 ETH`. Native v4 pools do not provide the built-in v3 observation history; a v4 launch market is not automatically a suitable TWAP source. V3 exposes cumulative tick and seconds-per-liquidity observations. [Uniswap oracle specification](https://developers.uniswap.org/docs/protocols/v3/concepts/price-oracles).

| Proposed valuation rule | Concrete requirement |
|---|---|
| Venues | Two curator-approved canonical v3 pools for the same token/WETH pair, normally different fee tiers; verify factory membership, token ordering, decimals and code. Two pools of the same token are not independent credit risks. |
| Mark | Conservative minimum of both pools' **30-minute and 60-minute geometric TWAPs**, denominated in ETH. WETH bypasses pricing calls. |
| History | At least 7 days of operating history for admission; actual initialized observations spanning 60 minutes at use. Increasing cardinality alone is insufficient. `observe` failure means no new draw. |
| Staleness | Last initialized observation no older than **5 minutes**; a successful extrapolated `observe(0)` is not proof of recent trading. Cached preparatory quotes expire after **60 seconds** and cannot replace request-transaction reads. |
| Divergence | Reject if the two 30-minute quotes differ by more than **3%**, or either pool's 5-minute TWAP or spot differs from its 30-minute TWAP by more than **5%**. These are shutdown guards, not fallback prices. |
| Minimum liquidity | Each pool: 30-minute harmonic liquidity converted to at least **1,000 ETH of virtual WETH-side reserves**, and current actual WETH balance at least **500 ETH**. These tests alone do not prove broad executable depth. |
| Depth admission | IMD verifies at least **200 ETH executable depth in each direction within a 10% price move**, and persistence in at least 99% of five-minute samples over the prior 24 hours. Admission/review attestation expires after 24 hours. Concentrated-liquidity depth must be simulated across ticks, not inferred from headline TVL. |
| Exposure | Each non-WETH token at most **25% of eligible marked inventory**, at most **20 ETH** outstanding marked inventory, and no Bag above **2.1 ETH**. WETH may constitute 100% during a technical pilot. |
| Unknown data | Fail closed for new deposits/activations/spins; preserve custody and already fixed claims. |

The virtual reserve conversion must respect whether WETH is token0 or token1. Quote raw token quantities with full-precision multiplication/division and round down; correctly floor negative average ticks. For amount `a_j` in a token with `d_j` decimals and ETH-per-whole-token quote `Q_j`, `V = Σ floor(a_j Q_j / 10^d_j)`. Bounds on decimals (0–18), amounts and aggregate value must precede casts. Token amounts are not necessarily 18 decimals. [Uniswap OracleLibrary implementation](https://github.com/Uniswap/v3-periphery/blob/main/contracts/libraries/OracleLibrary.sol).

These thresholds are deliberately restrictive **proposals**, not measurements establishing that a particular token qualifies today. Admission begins with WETH; additional tokens require real checks. A 60-minute TWAP is not manipulation-proof: concentrated liquidity and consecutive proposer control remain concerns. Two correlated pools and a daily depth attestation can both fail under rapid LP withdrawal. Exposure caps and hard reserve reservation limit consequences; they do not prove an attack uneconomic. [Uniswap's PoS oracle research](https://blog.uniswap.org/uniswap-v3-oracles).

### Tiers, weights and admission

Fixed spin price `P = 0.10 ETH`; accept exactly P in native ETH. Wallet transaction gas is additional. No platform-token payment or spinner emission bonus.

| Tier | Admission value band | Reference size | Reference ETH | Probability |
|---|---:|---:|---:|---:|
| Small | 0.38–0.42 P | 0.40 P | 0.040 | 70% |
| Medium | 0.95–1.05 P | 1.00 P | 0.100 | 24% |
| Large | 3.8–4.2 P | 4.00 P | 0.400 | 5% |
| Jackpot | 19–21 P | 20.00 P | 2.000 | 1% |

Bands deliberately leave gaps. A Bag outside all bands remains withdrawable/staged, not quietly put in a different prize distribution. Depositors can withdraw, open and reseal; do not mutate their sealed quantities automatically. Prices changing may make a pool temporarily unavailable.

Draw a tier with probability `p_t`, then a Bag within that tier with normalized weight `w_i/Σ_t w`. Initial weights are equal. IMD may supply a bounded multiplier for each admitted token; a multi-token Bag's multiplier is its value-weighted average, so adding dust cannot obtain a preferred category. No private per-wallet favoring. The effective probability is `π_i = p_t × w_i/Σ_t w`.

The request transaction must verify:

- All four tiers are populated, all committed Bag prices valid, and the exact snapshot satisfies **0.919 P ≤ Σ π_i V_i ≤ 0.930 P**. Thus modeled cashout EV is at least 90.062% and keep-mark EV at most 93%.
- Per-token exposure caps, safety attestations, bound checks and the reserve invariant hold.
- No randomness request is outstanding, staged/exit changes have been applied deterministically, and the user's expected inventory/configuration version matches.
- Any expired curation validity, missing tier or out-of-band aggregate EV rejects the *new request*. Never redistribute empty-tier odds or reroll an unavailable prize after seeing the word.

There is only **one unresolved random draw globally** in the pilot. After its allocation is fixed, unselected Bags unlock and another draw may be requested; previously allocated choice entitlements can coexist and remain fully reserved. Use rejection sampling for unbiased integer intervals and domain-separated hashes for tier/Bag selection. An indexer may propose a candidate view but cannot supply authoritative membership or prices.

IMD's numerical powers are restricted to tier probabilities and pool multipliers. Hard ranges: small 65–75%, medium 20–28%, large 3.5–6.5%, jackpot 0.5–1.5%; probabilities sum to 10,000 bps. Multipliers stay in [0.5, 2.0]. For every coordinate `x`, enforce `abs(new-old) × 10,000 ≤ old × 1,000`, and allow numerical updates only at least **86,400 seconds after the previous applied update**. This prevents splitting a daily change across transactions. Apply vector changes atomically, with a 24-hour announced delay; the EV guard remains independently binding. Tier boundaries, price, fee rates, reserve floor and valuation safety limits are immutable.

A binary single-token safety pause/delist is a separate explicit power, not a covert numerical update to zero weight. It immediately blocks *future* eligibility for every Bag containing that token. It cannot alter an in-flight snapshot, confiscate tokens, change fee recipients or move reserve ETH. Unpausing needs a fresh passing attestation and 24-hour delay.

### Keep, cashout and the depositor's payout

Freeze value `V` and both settlement rates with the request. After allocation the spinner has **five minutes** to choose; anyone may finalize **KEEP** afterward. Nothing happens merely because a clock expires: a transaction must finalize. The short cashout option still has market value; report both the fixed quote and live estimated token value.

| Choice | Spinner | Original depositor | Bag state | Reserve cash obligation |
|---|---|---|---|---:|
| KEEP | NFT entitlement; may claim NFT, trade it, or open components | Pull-credit **0.98 V ETH**; future dividends stop | Leaves pool permanently for this listing | 0.98 V |
| CASHOUT | Pull-credit **0.98 V ETH** | Retains beneficial ownership; **no sale payout**; resumes dividends when reactivated | Same sealed Bag returns to eligible/staged pool after fresh checks | 0.98 V |

No NFT and ETH together; no double depositor payment on repeated cashouts. “Taken” in this design means KEEP. Cashout is the protocol paying to cancel the spinner's allocation, not buying a Bag from a depositor already paid. A returned Bag that fails current safety/price rules is held for depositor withdrawal and earns no new rewards.

Use pull credits for ETH; allocation and settlement perform no arbitrary recipient callbacks. KEEP finalization records NFT entitlement even if its recipient cannot accept `safeTransferFrom`. The beneficiary can later choose a capable recipient. Underlying token problems cannot prevent an already-reserved ETH payment. Once the spinner claims/transfers/opens a kept NFT, the original cashout option no longer exists.

### ETH reserve and fee accounting

The reserve is supplied by **voluntary, explicitly non-redeemable capital contributions**, initially **50 ETH = 500 P**. There is no reserve LP token or promised principal withdrawal in this pilot. The contributor bears reserve loss and illiquidity. The team fee is not a claim on that capital. If the intended sponsor requires returnable capital, this design needs a separate reviewed reserve-share mechanism and different simulations.

Do not treat a launch valuation, platform-token holdings, ERC-20 Bag TVL, anticipated fees or future deposits as usable ETH. All fixed obligations are recorded separately from free ETH.

For each accepted spin allocate:

| Use | Per spin | Purpose |
|---|---:|---|
| Depositor platform-token purchase budget | 2% P = 0.002 ETH | Actual tokens bought, then distributed to earned units |
| Team pull-credit | 1% P = 0.001 ETH | Immutable beneficiary fixed before deployment |
| Operations budget | 1% P = 0.001 ETH | VRF funding and capped successful processing/buyback bounties |
| Free reserve increment before prize cost | 96% P = 0.096 ETH | Pays whichever one settlement beneficiary wins |

The depositor's **2% sale discount** is embedded in the prize cost `0.98V`, not another transfer on top of this table. Cashout's 2% discount is likewise embedded. With reference odds, expected prize liability is `0.98 × 0.92 P = 0.9016 P`; expected retained cash is **0.0584 P**. This is an expectation, not an amount paid to a treasury per spin.

Define `R` as ETH free of fee budgets, ETH credits and known allocated liabilities; `L` as unknown-draw worst-case reservations. New admission requires:

`R + 0.96P − L − 0.98 × 21P ≥ 100P`.

Here `L` is zero before the sole new random request; show it separately to make double counting impossible. On request, earmark **20.58 P = 2.058 ETH**. On allocation, replace the maximum reservation by exactly `0.98V`, releasing only the excess. On choice/finalization, convert that same liability to the correct user's credit; this must not deduct it a second time. On claim, actual balance and credit liability decrease together. Known allocations can remain outstanding; none are available for another request.

For economic simulation, subtracting `0.98V` immediately is equivalent to removing that amount from free reserve, even if users delay claiming. The wallet's raw ETH balance is never the solvency test. Reserve donation events distinguish contributed capital from retained revenue. There is no admin sweep, lending, token-market rescue purchase or reserve withdrawal.

### Dividend accounting and token purchases

A reward is a share of **fees actually spent buying tokens**, not fixed token emissions or an APY promise. Before the random result, give each eligible depositor ETH-denominated units from that spin's 0.02P budget:

`u_i = floor(0.02P × π_i V_i / Σ_j π_j V_j)`.

This uses expected prize value supplied, rather than square-root weight or wallet count. Checkpoint the chosen snapshot before changing membership. Include the subsequently selected Bag for that accepted spin; it supplied inventory at commitment. At most 64 entries are updated, so cost is bounded. Units are credited to `(depositor, hourlyEpoch)` and cannot be transferred with the NFT. Rounding dust stays earmarked for dividends and carries into a later epoch, never team/reserve revenue.

Close an epoch before swapping its budget. Permissionless execution purchases through a fixed canonical **platform-token/WETH v3 route** and credits only that epoch. If execution uses multiple capped chunks, accumulate output and claimable ratios; claims cannot include unexecuted units. Final accounting uses `tokensPurchased × userUnits / epochTotalUnits`, with claimed amounts tracked and token dust retained. Units created afterward cannot capture a prior buyback. A departed depositor retains all earned units.

The platform launch's v4 market is separate. Require a sufficiently funded v3 reward route before allowing token purchases: at least **10 ETH actual WETH**, 60 minutes of history, a 30-minute TWAP, at most 0.5% execution slippage from a fee-adjusted TWAP quote, and per-swap input at most **min(0.01 ETH, 0.1% of WETH depth)**. Split large epoch budgets across transactions; pay bounty only after successful output, from operations. No arbitrary router or calldata. No required immediate purchase at an attacker-set price. If the route fails, ETH and units remain escrowed for that epoch; rewards are delayed, not diverted or newly minted. Token payout amounts and resale value are not guaranteed. This second market needs separately provided liquidity; the IMD token launch does not create it automatically.

The five-minute choice window, staged inventory and fixed denomination bands intentionally constrain throughput. The interface must show unavailable states rather than advertise a continuously redeemable slot machine.

## 3. Economics and stress tests

**Model, not forecast.** `simulation/model.py` uses Python's standard library, seed **20261013**, **10,000 paths × 5,000 spins**. Draws are independent with the reference probabilities and values; inventory is stationary and immediately replenished/reactivated. No token appreciation, price noise, wallet gas, swap execution loss, depositor arrival model or oracle failure probability is assumed. Reserve halts are modeled, but inventory/depth halts are not; actual throughput can be lower. A 5,000-spin horizon is not a calendar-time forecast.

The model calculates cash conservation, exclusive settlement recipients, expected rewards, a deterministic bad streak and an analytical 50% crash. It is an economic reference implementation, not a test of yet-unwritten Solidity or proof that oracle manipulation is costly enough.

### Reference unit economics

`E[V]/P = 0.70×0.40 + 0.24×1 + 0.05×4 + 0.01×20 = 0.92`.

| Per spin | P units | ETH at P = 0.10 |
|---|---:|---:|
| Spinner keeps: expected marked token value | 0.9200 | 0.09200 |
| Spinner cashes out: expected ETH | 0.9016 | 0.09016 |
| Cash paid to one settlement beneficiary | 0.9016 | 0.09016 |
| Platform-token dividend purchase budget | 0.0200 | 0.00200 |
| Team budget | 0.0100 | 0.00100 |
| Operations budget | 0.0100 | 0.00100 |
| Expected reserve increase | **0.0584** | **0.00584** |

A value-independent keep fraction `k` gives spinner marked RTP `90.16% + 1.84%×k`. Rational users instead exercise a price-dependent option: `max(actual recoverable token value, 0.98V)` during the choice window. **92% is therefore not a guaranteed realized upper bound under subsequent price increases**, nor is TWAP value the same as net liquidation proceeds. Keep sales incur gas, venue fees and slippage. Cashout has gas but no token liquidation slippage.

At an illustrative 0.001 ETH of wallet gas per completed spin, cashout RTP on total spending is `0.09016 / 0.101 = 89.27%`. At 0.0001 ETH gas it is 90.07%. Gas is not hidden inside the advertised 90–93% **pre-gas** target. Mainnet gas can make this product unattractive; the website must show all-in expected value and refuse misleading fee estimates.

### Depositor economics

Let `q` be the probability a selected Bag is cashed out and returned. Under the stationary model, a Bag with probability `π_i` survives on average `1/((1−q)π_i)` spins before sale. With reward units proportional to `π_iV_i`, expected dividend purchase value before sale is:

`D_i = 0.02P × V_i / (E[V] × (1−q))`.

Relative to the tokens' unchanged entry value, expected net return before gas and reward-market costs is `0.02/(0.92(1−q)) − 0.02`:

| Cashout fraction q | Expected dividend buying budget / Bag value | Sale discount | Expected net return |
|---|---:|---:|---:|
| 0% | 2.1739% | 2% | **0.1739%** |
| 50% | 4.3478% | 2% | **2.3478%** |
| 80% | 10.8696% | 2% | **8.8696%** |

These are lifetime returns until a sale, not annual yields. At q→1, the finite-time sale assumption breaks: quoting infinite yield would be wrong. At zero spin demand there are zero new fee-funded dividends. Rewards distributed as tokens may be worth less when claimed or sold.

For a concrete inventory of **40 small, 16 medium, 6 large and 2 jackpot Bags** (64 total, **9.6 ETH marked contents**), at q=50% the expected spins until sale are approximately **114, 133, 240 and 400** respectively. A medium 0.10 ETH Bag gets 0.098 ETH sale proceeds plus about 0.004348 ETH of reward purchasing budget, before costs. A small Bag's expected net budget gain is only **0.000939 ETH**; seal/list/claim gas can consume it. A 50% decline before sale overwhelms these returns.

### Reserve results

The guard is evaluated before accepting a request. With reference maximal Bag band 21P, its threshold is **119.62P of free reserve before adding the new spin payment**. The separate minimum retained buffer is 100P. A 100P reserve cannot open the pilot at all.

| Starting free ETH | Starting P | Halted within 5,000 spins | Terminal free ETH, 5th / median / 95th percentile |
|---|---:|---:|---|
| 10 | 100 | 100%: admission initially fails | 10 / 10 / 10 |
| 25 | 250 | **367 / 10,000 = 3.67%** | **25.446 / 54.298 / 77.093** |
| 50 | 500 | **0 / 10,000 observed** | **54.856 / 79.376 / 102.093** |

For the 25 ETH run, sampling standard error of the halt fraction is approximately **0.188 percentage points**. Zero halts at 50 ETH means an approximate one-sided 95% binomial upper bound of **0.030%** *under this model*, not zero real risk. Without the admission guard, the same hypothetical random walks crossed negative cash in 0.17% of 25 ETH runs. The guard changes a would-be inability to pay into refusal of future business.

**Bad streak:** 21 consecutive reference jackpots cost `(19.6−0.96)P = 18.64P` each. A 50 ETH reserve pays all 21 and ends at **10.856 ETH**, then refuses the next draw. Repeated jackpot cashouts can reuse inventory; the streak is not limited to the initial two jackpot Bags. The raw probability of 21 consecutive independent 1% jackpots starting at a specified spin is `10^-42`, but adversarial selection is not modeled by that probability. The hard invariant, not this improbability, protects already accepted commitments.

**50% crash:** fresh marks would lower reference keep EV to **46%** and cashout EV to **45.08%**. The EV/divergence gates stop new requests. ETH reserve principal has **zero direct token mark-to-market loss** because it holds ETH; unsold depositors bear a 50% loss in their token inventory. The model therefore does not pretend a crash merely halves payouts while the product keeps advertising 92% RTP.

An already committed draw still pays its frozen quote. Maximum liability remains **2.058 ETH**. If a 2.1 ETH marked Bag falls to 1.05 ETH, that frozen cashout exceeds current token value by **1.008 ETH**. This is bounded option exposure already reserved, not a second liability. Known allocations whose choices remain open are also fully reserved. A process-time repricing bug that doubled values would instead change expected reserve drift to **−0.8432P per spin**; the snapshot is a solvency control as well as a fairness control.

### Adverse selection, whales and bots

**Adverse selection:** a depositor cannot sell arbitrary falling inventory to the reserve on demand. Only a KEEP outcome pays them; a rational spinner may choose ETH instead, leaving the depositor with the falling tokens. Nonetheless, stale marks can turn the experience into cashout-only gambling and pay dividends to bad inventory. The 24-hour maturation, short-window divergence guards, narrow tier bands, expiring safety checks and no entry-price payout promise are intended to reduce that problem. Maturation does not stop informed holders anticipating tomorrow's crash; do not present it as insurance.

An attacker who owns all inventory and spins against themselves cannot count their own returned Bag as new wealth. Their expected net ETH loss after capturing all dividend purchasing value is **`1−0.9016−0.02 = 7.84%` per spin**, before gas. Capturing the team fee too still leaves **6.84%**. Removing external emissions makes simple wash spinning negative in this stationary model. It does not prove absence of attacks involving oracle manipulation, MEV, reward-token markets or compromised attestations.

**Whales:** rewards are linear in probability-weighted value supplied, so splitting one reward entitlement across addresses does not manufacture value. There is no enforceable Sybil-resistant per-wallet cap. A whale can still dominate scarce inventory, withdraw it to halt a tier, or buy transaction priority. Whitelist and token exposure caps constrain asset risk, not beneficial-owner concentration. Show concentration metrics without promising identity-level fairness.

**Bots:** publish deterministic quotes, exact odds, inventory versions and outstanding claims; bots receive the same VRF distribution. Prevent stale-quote submission with version and deadline checks. Fund finite successful-processing bounties rather than pay for arbitrary retries. Do not reward raw spin counts, wallet counts, oracle submissions or unsuccessful buybacks.

**Parameter recommendation:** retain the reference set, 50 ETH free reserve, 2 ETH separately budgeted for initial operations/VRF, 64 active Bags, one unknown draw at a time, 24-hour maturation and 5-minute choice. Increase throughput only after measuring real gas and inventory turnover. Do not raise jackpot odds to cure a lack of users or token-price decline.

## 4. Attack analysis and residual risk

| Attack | Mitigation in the design | Residual / required validation |
|---|---|---|
| Flash-loan or multi-block TWAP manipulation | Two canonical deep pools; 30/60-minute marks; short-window divergence checks; liquidity history; 2.1 ETH prize cap; request-time commitment | TWAP is manipulation-resistant, not unmanipulable. Simulate tick-range liquidity, proposer sequences and adversary capital for each admitted token; actual liquidity can disappear within the attestation interval. |
| Fee-on-transfer, sender-side tax, rebase, blacklist, pause, max-wallet or upgradeable tokens | Reject these capabilities at admission, inspect implementation/admin paths and runtime identity, exact incoming balance deltas; disable new eligibility on fresh failure | A transfer simulation is not proof of future behavior. WETH-first admission is safer than a broad meme-token list. If a token later breaks, component claims isolate other assets; promised ETH credits still pay. |
| Fake pool / attacker-chosen oracle | Fixed factory; verify pool token pair and fee tier; store reviewed pool identities; do not accept a depositor's router or oracle | Two legitimate pools may still be attacker dominated. Attested historical depth and exposure caps matter. |
| Callback front-running to shift winning Bag | Commit the complete ordered eligible set, prices, tier sums and weights before requesting VRF; freeze changes affecting that request | Tests must reproduce insert/remove/reorder/delist attempts around fulfillment. A snapshot hash without retained verifiable data is insufficient. |
| Front-running a draw with a new deposit | 24-hour staged maturation, deterministic activation, snapshot/version check | Mature inventory can still be added just before another request, so show the exact accepted distribution and reject stale client bounds. |
| VRF result timing / reroll | 12 confirmations proposed; bind coordinator and request ID; no cancel/re-request; fixed selection data; duplicate/late messages cannot create a second claim | Fulfillment has no guaranteed latency. Coordinator/key retirement is a liveness failure for immutable deployment. Pending claims need permanently available service. |
| Underfunded VRF / request griefing | Fund subscription before enabling; reserve worst-case service cost separately; one unknown draw; every accepted draw pays P; callback only stores word | Paid requests can still occupy the slot; a service outage can freeze inventory. No owner-funded rescue assumption. |
| Callback out-of-gas | Minimal authenticated word-storage callback, proposed 150k limit; settlement in permissionless separate transaction | Chainlink does not automatically retry a reverting consumer callback. Must benchmark maximum callback state and prove it cannot revert for a valid request. |
| Oracle attestation replay / wrong question / weak panel | Pin schema/question derivation, chain and consumer, exact token/pools/action, validity, observation window, monotonic nonce and prior-state hash; verify agreed/quorum thresholds; single use | An attester signature is still a trusted signing-key dependency. IMD availability and key rotation cannot be repaired by an admin in this design. |
| Oracle front-running / updates timed after seeing random word | Numerical updates delayed and rate-limited; snapshot version fixed; pauses affect only future requests | A malicious valid curator can censor future token admission. Hard bounds reduce financial authority but do not eliminate oracle trust. |
| Reentrancy through ERC-20 callbacks, ERC-721 receivers or ETH recipients | Checks-effects-interactions; global nonreentrant state-changing pool paths; separate component claims; pull ETH; no token transfers in VRF callback | Test adversarial tokens despite whitelist policy, including `balanceOf`/metadata reverts and unusual return data. |
| Wash spinning / emissions farming | No purchaser rewards or emissions; dividends funded only by 2% of accepted spin price; freeze earned units before execution | Off-platform subsidies or token-price effects can change profitability; negative model EV is not a security proof. |
| Sandwiching reward purchases | Bounded chunks, historical quote, fixed route, min output, deadline, permissionless execution; retry rather than relax limits | Private transaction delivery is optional convenience, not the security boundary. Rewards can remain illiquid or unexecuted. |
| Reward capture just before buyback | Units attach to the earning epoch before swap; closed-epoch budget and total units immutable | Property tests must cover joining/leaving, partial execution, dust, repeated claims and token transfer failures. |
| Reserve run / double payment | Contributions are nonredeemable; account for unknown draws, allocated choices and pull credits; exactly one recipient per draw | Nonredeemable capital is hard to attract. No withdrawal promise to contributors; immutability makes design errors permanent. |
| Missing jackpot / withdrawal starvation | All tiers checked before admission; withdrawal intents excluded from future snapshots; never reroll after fulfillment | An outstanding unknown draw can still delay exits indefinitely. Lack of inventory halts sales instead of lowering RTP. |

Provider guidance supports binding request IDs, preventing input changes after requests, avoiding rerolls, and keeping callbacks non-reverting; those principles are applied here, with the ownerless adapter differences discussed below. [Chainlink security considerations](https://docs.chain.link/vrf/v2-5/security).

## 5. Contract architecture within IMD limits

**Design:** five application contracts, deployed in dependency order; the platform token is a separate earlier launch. No proxy, delegatecall-based upgrade, owner role, arbitrary external-call executor, constructor child deployment or external constructor call. Constructors validate static values and store constants only. No constructor calls ERC-20 metadata, a factory, coordinator, registry or another application. Runtime validation occurs before first use.

| Order / contract | Static constructor arguments (words) | Responsibilities and principal storage | Principal events |
|---|---|---|---|
| 1. `BagCurator` | attester address, canonical policy hash (**2**) | Exact IMD verifier; token/pool safety records, expiries, pauses, proposed configurations, consumed request IDs, prior-state hashes, numerical update time and config version | `CurationProposed`, `AttestationAccepted`, `TokenAdmitted`, `TokenPaused`, `TokenDelisted`, `OddsScheduled`, `OddsApplied` |
| 2. `BagValuator` | curator, canonical v3 factory, WETH (**3**) | View-only valuation and liquidity/observation checks; fixed thresholds; no arbitrary token price overrides | No state-changing price-setting event; pool emits the consumed quote commitment |
| 3. `BagNFT` | curator (**1**) | ERC-721, sealed arrays/amounts, total per-token custody obligations, burned-Bag component claims; ordinary NFT ownership authorizes opening | standard `Transfer`/`Approval`, `BagSealed`, `BagOpened`, `ComponentClaimed` |
| 4. `RewardSwapAdapter` | platform token, WETH, v3 factory, router, fee tier (**5**) | Fixed route; authenticated router interactions, TWAP/min-output and trade-size limits; permissionless paid swaps to specified recipient; no inventory/reserve authority | `RewardSwap` |
| 5. `BagPool` | curator, valuator, BagNFT, adapter, platform token, team beneficiary, VRF coordinator, key hash, P (**9**) | Inventory lifecycle, full draw snapshot, request/word status, allocations, free ETH/reservations/pull credits, operations balance, dividend epoch units/budgets/output, nonreentrancy guard, internally created subscription ID | `BagListed`, `ExitSignalled`, `BagWithdrawn`, `DrawCommitted`, `WordStored`, `BagAllocated`, `Kept`, `CashedOut`, `ETHClaimed`, `ReserveFunded`, `DividendUnitsEarned`, `EpochPurchased`, `DividendClaimed`, `VRFInitialized` |

All counts are below **8 contracts and 16 static constructor words**, the assignment's limits. Addresses refer only to earlier artifacts or already deployed infrastructure. The NFT needs no privileged pool binding: a user authorizes listing, the pool receives ordinary ownership, and ordinary ownership gives it transfer/open rights. The swap adapter is a permissionless fixed-route utility, so it also needs no later admin binding. Avoid circular initialization and “first caller becomes owner” patterns.

`BagPool` must fit EIP-170 runtime size and the launch transaction gas cap. This is a design partition, not a measured compiled size. If it exceeds the limit, use the remaining three slots to split immutable custody/accounting with a deterministic, verified binding; do not solve size by adding a proxy or an unauthenticated initializer. Exact compiled limits and dependency wiring are release gates.

### IMD attestation contract and curator questions

**Documented interface:** IMD supplies version-2 EIP-712 attestations bound to a consumer. Answers include the question hash, block window, validity and panel agreement. A valid signature alone does not prove the consumer asked the intended question. Numeric answers, booleans and fixed/list hashes are supported. [IMD oracle documentation](https://imd.fun/docs/#oracle).

**Observed:** the public oracle listing returned attester **`0x5598aa9146215bc13eb26f2c692ad1461fd32982`** on October 13. This differs from the quote signer in capabilities. Save and independently confirm the oracle attester before deployment; never use `onchain.quoteSigner` as a substitute. [Oracle listing](https://api.imd.fun/oracle/requests?limit=1), saved `research/imd-attester.json`.

**Proposed question definitions** use a fixed, versioned policy document and canonical question generator. A public proposal can name a token or candidate bounded numerical vector, but cannot choose its own safety definition. Store the proposal and its prior-state/configuration hash before buying an answer. Compute `expectedQuestionHash` from the entire canonical IMD question body, including definitions, action, addresses, window and consumer; use the official `oracleQuestionHash` format with cross-language test vectors. Do not accept a caller-supplied arbitrary question hash as policy authorization.

| Question | Exact proposed meaning / answer | Evidence and application |
|---|---|---|
| `BAG_ADMIT_V1` | “Under policy hash H, does token T with runtime hash C and canonical pools A/B pass every safety, liquidity, history and exposure-admission condition as of the committed closing block?” **bool**; missing evidence means no approval, never guessed true | Panel inspects verified source and implementation/admin dependencies, transfer semantics, holder/admin powers and historical depth. A true answer schedules admission after 24 hours; runtime pool identity/balance/history checks still apply. |
| `BAG_REVIEW_V1` | Same predicate for an existing token, with new observation window and monotonic token nonce. **bool** | True renews its 24-hour safety validity; false delists future participation. Silence lets validity expire and blocks new eligibility; it does not confiscate inventory. |
| `BAG_PAUSE_V1` | “Is there evidence at the committed block of a specified transfer restriction, unsafe code/implementation change, exploit, or breach of policy H for token T?” **bool** | True pauses that token immediately for future requests. False is not an unpause. No free-text answer directly changes storage. |
| `BAG_UNPAUSE_V1` | Full passing admission/review predicate for paused T, referencing pause nonce. **bool** | Fresh true answer plus 24-hour delay; no numerical bound waiver or reopening on stale approval. |
| `BAG_PARAMS_V1` | “Does candidate vector hash X, replacing state hash Y, satisfy policy H's diversification objective, prescribed ranking criteria and every on-chain bound for the next configuration epoch?” **bool** | Candidate vector is already on-chain. Approval authorizes that vector only; 24-hour notice, 24-hour rate interval, hard coordinate ranges, normalization and EV guard remain mandatory. |

Use **panelSize ≥25, quorum ≥20, agreed ≥20 and agreed ≥quorum** as proposed minimums, tolerance zero for authorization. This is an assumption about acceptable curation trust, not a measured resistance to swarm collusion. The system may be unable to assemble that quorum; missing answers never relax it. Safety review needs `evidence: panel` because arbitrary semantic code analysis is not simply a supported log-count recipe. Submit objective chain metrics separately where reproducible recipes exist.

Verify the EIP-712 domain `IdentityMD Oracle`, version `2`, chain 1, exact `BagCurator` address; attestation chain 1; expected answer type/length; exact question/proposal binding; recorded block range/hash; no future issuance; maximum issuance age (one hour for pause, six hours for routine review); signed expiry; and consumed nonce/request ID. Pin the observation window in the request record according to the policy's current scheduled interval, so a proposer cannot choose a favorable old market window. Require passing quotes to refer to a closing block no older than six hours. Proposal IDs and prior-state hashes prevent applying an approval to a different configuration.

Anyone may pay for or relay an answer; payment gives no curation authority. Verification and applicability determine authority. Prefer permissionless `submitAttestation` plus `apply` over doing expensive activation inside a callback. If using Intake callbacks, store only a small authenticated result; never move value on an unsigned failure callback. The canonical hashing, typed encoding, actual signature verification and proposal-window logic require integration tests against real IMD response fixtures before deployment.

**No-owner limit:** the attester and schema are fixed. No owner can rotate them, replace the oracle, change beneficiaries or widen bounds. If IMD retires the signer/schema, admissions expire and uncommitted inventory exits; a new immutable deployment is needed. Ownerlessness removes an application admin key, **not** the IMD signing-key trust dependency. The requested curation model cannot honestly be described as trustless.

### VRF subscription with no administrative key

**Documented:** the coordinator supports runtime subscription creation, consumer registration by the subscription owner, and native funding. The stock `VRFConsumerBaseV2Plus` inherits `ConfirmedOwner` and exposes coordinator migration; copying it unchanged would violate this brief. [Subscription API source](https://github.com/smartcontractkit/chainlink-evm/blob/develop/contracts/src/v0.8/vrf/SubscriptionAPI.sol), [consumer source](https://github.com/smartcontractkit/chainlink-evm/blob/develop/contracts/src/v0.8/vrf/VRFConsumerBaseV2Plus.sol).

**Design:** implement a reviewed minimal immutable coordinator-authenticated consumer in `BagPool`. Permissionless `initializeVRF()` executes **after deployment**, takes no configuration from the caller, creates exactly one subscription and adds only `address(this)` as consumer. The pool contract itself is the subscription owner. Set the initialization/reentrancy state before external calls; atomic revert restores it on failure. There is no exposed cancel, owner-transfer, consumer-addition or migration function. A caller cannot capture ownership by racing initialization.

Use the Ethereum coordinator observed above and proposed key hash `0x8077df514608a09f83e4e8d300645594e5d7234665448ba83f51a50f842bd3d9`, **12 confirmations**, one random word, native payment and a **150,000-gas callback target**. Pin actual coordinator configuration and test this limit before launch. The documented Ethereum native-payment premium is 24%, with a minimum of three confirmations; the proposed twelve is a policy choice, not a latency guarantee. [Chainlink network parameters](https://docs.chain.link/vrf/v2-5/supported-networks).

Anyone can donate through `fundOperations()` or fund the exact subscription. Permissionless `topUpVRF()` sends only earmarked operations ETH to that subscription. New spins require sufficient service funds and no outstanding random request; proposed operating gate is base fee ≤1 gwei. Start with **2 ETH of service/operations funding**, maintain a **1 ETH service buffer**, and provision a conservative **0.30 ETH coverage allowance for the sole pending request** at the selected 200-gwei lane until exact billing limits are measured. This is a funding assumption, not a provider quote. If actual configuration needs more, adjust the design before deployment; do not raid payout reserves after launch.

The callback only authenticates, stores the word and marks its request ready. No token transfers, swaps, oracle updates or Bag selection loops. Anyone then calls processing for the unique ready request. Only successful bounded work earns an operations bounty. Payment P remains fixed even if service expenses change; insufficient operations funding halts new requests and donations may restore service. This explicitly exposes the economic risk of a fixed retail price with variable infrastructure costs.

### Gas budget, not measured Bag gas

| Action | Engineering estimate | What must be measured |
|---|---:|---|
| Seal one-token Bag | 160k–260k | ERC-20 behavior, new custody slots, NFT mint |
| Seal four-token Bag | 350k–600k | Four transfers, quantities and component accounting |
| List existing Bag | 90k–180k | Custody, lifecycle and staging state; oracle validation may add cost |
| Request spin | **0.8m–3.5m** | Bounded 64-Bag/8-token valuation, snapshot writes, dividend unit allocation, VRF request |
| VRF callback | target ≤150k | Worst-case authenticated storage path only; coordinator proof/billing gas is additional |
| Process allocation / settle choice | 150k–350k / 80k–160k | Selection and liability conversion; settlement must not loop through all deposits |
| ETH claim / NFT claim | 35k–65k / 60k–110k | Pull withdrawals and recipient behavior |
| Epoch reward purchase | 180k–350k | Fixed-route swap and chunk accounting |

At 1 gwei, 0.8m–3.5m request gas alone costs **0.0008–0.0035 ETH**, or 0.8–3.5% of P; settlement adds more. At 10 gwei the proposed gate refuses new spins. These ranges are deliberately not FWA's measured gas extrapolated as if this implementation existed. The actual FWA receipt examples above are the only measured execution gas in this report. Mainnet viability requires benchmarking realistic maximum inventory and publishing the result before setting immutable parameters.

## 6. IMD launch plan, costs and decisions still needed

### Separate platform-token launch

**Design recommendation:** use a separate **`custom_token`** launch for a plain, fixed-supply, nonupgradeable ERC-20: **1 billion tokens, 18 decimals, no mint-after-deployment, taxes, blacklist, pause or governance privileges**. Allocate **90% to the launch pool and 10% to the swarm**, with no unallocated founder remainder and no spin/deposit emissions. Use ETH pairing and an illustrative **100 ETH opening fully diluted valuation**, subject to current policy admission. That opening price is not capital raised, a redemption promise or proof of deep liquidity.

The team receives only the separately disclosed game fee and whatever trading-fee rights the token launch policy actually assigns. Token holders get no vote over Bags, reserve redemption or guaranteed distribution. Depositors receive purchased tokens because they supply eligible inventory, not because they merely hold the platform token. Exclude the platform token from eligible Bag contents to avoid circular valuation and self-backed jackpot inventory.

**Observed platform terms:** public capabilities list Ethereum `custom_token` and `evm_contracts`, a current ETH custom-cap range of 1–1,000 ETH, and **0.5 IMD** for each listed `launch.open`, `job.open`, `workflow.open` and `oracle.request` action. These are service prices, not the reserve, gas, market liquidity or an audit budget. [Live capabilities](https://api.imd.fun/requests/capabilities), saved `research/imd-capabilities.json`.

**Documented constraints:** `evm_contracts` deploys 1–8 contracts without a token or pool; static arguments may reference earlier contracts, and the manifest makes no post-deployment calls. The documented token policy retains a 10% swarm allocation and quotes a 1.25% trading fee split between payer and network. Confirm the actual quoted policy and fixed token economics at launch. [IMD launch documentation](https://imd.fun/docs/).

### Ordered jobs and activation

1. **Specification/review job:** resolve the economic and legal release gates, canonical oracle questions and state machine. Have an independent reviewer challenge price-manipulation cost, reserve accounting, liveness and reward incentives. This report's local model is not that independent review.
2. **Platform-token implementation, tests and launch:** pin the exact fixed-supply source and separate token launch parameters; independently inspect its market hook and fee recipients. Record deployed token, pool and hook identities. No Bag contract should use an invented future token address.
3. **Application build job:** implement the five contracts in order; vendor all Solidity dependencies as ordinary files; static constructors only. Use the recorded token address, actual team beneficiary and validated oracle/coordinator infrastructure. No `$token` placeholder in a contracts-only launch. Compile and enforce runtime size and constructor-word limits.
4. **Independent tests and audit jobs:** fuzz accounting and state transitions; run malicious ERC-20/ERC-721 recipients; exercise snapshot mutation attempts, every oracle rejection condition, expired/weak/wrong-domain attestations, duplicate VRF callbacks, withheld words, missing tiers and repeated cashouts. Test at least maximum inventory, gas bounds and a historical crash/manipulation fork. Require all high/critical findings closed with reproductions and a second review of fixes.
5. **Sepolia rehearsal, then explicitly authorized mainnet `evm_contracts` launch:** same code and constructor schemas, chain-specific official infrastructure. Verify source/bytecode, static manifest arguments and all five recorded addresses. Confirm no hidden owner/proxy or external constructor calls. These are proposed future jobs, not actions taken in this assignment.
6. **Post-deployment permissionless setup transactions:** call the no-argument VRF initializer; donate **50 ETH reserve + 2 ETH operations**, fund the subscription, obtain genuine IMD admission attestations and activate matured inventory. Establish the additional v3 platform-token/WETH reward route with at least **10 ETH WETH liquidity** and actual tokens. This step cannot be pretended to happen inside IMD's deployment manifest.
7. **Website job after deployment:** build against verified addresses/ABI hashes; publish a static export through the chosen IMD hosting workflow. Validate hosted bytes, network, token approvals, exact inventory and current claimability. Do not ship a connect-wallet interface against rehearsal addresses.
8. **Operational launch:** permissionless external keepers submit only deterministic allowed actions. Publish reserve/obligation/operations balances, halted reasons, actual reward purchases, oracle attestations and request-to-result links. Fund repeat curation questions; do not schedule this report to wait in real time.

The website needs seal/list/open/trade flows, independent ETH and reward claims, request progress, exact accepted odds, price timestamp and TWAP age, net gas estimates, cashout expiry, withdrawal intent, and a clear distinction between the underlying asset value and guaranteed fixed ETH claim. Show all-in RTP, inventory concentration and a warning when a non-recoverable randomness commitment remains pending. Avoid simulated “near misses” or animations suggesting different odds from the contract.

### Capital, operating costs and legal review

**Proposed capital requirement:** at least **62 ETH plus tokens for the separate reward-market LP**, before implementation/review costs and transaction gas: 50 ETH nonredeemable reserve, 2 ETH operations and 10 ETH reward-route WETH. The 10 ETH LP is separate risk capital; its token half has a real acquisition cost. It must not be counted as the payout reserve. The IMD launch pool allocation is mostly token inventory, not 50 ETH available to pay winners.

At 1,000 spins/day, the model collects 100 ETH/day gross spin payments, spends an expected 90.16 ETH on exclusive payouts, earmarks 2 ETH for depositor token buying, 1 ETH for team and 1 ETH for operations, retaining an expected 5.84 ETH. This is **a volume scenario, not a demand forecast**. Deployment gas budget might be 10m–25m gas across jobs, or 0.01–0.25 ETH at 1–10 gwei, but must be replaced with compiled estimates and per-transaction cap checks. Paid security work and legal costs are unquoted.

For four non-WETH token reviews plus one numerical-policy question per day, five oracle requests at the observed service price imply **2.5 IMD/day or 75 IMD/30 days**, excluding emergency questions, request/relay gas and service-price changes. Anyone may sponsor questions. No system can guarantee affordable curation forever with immutable fees and no admin; expiry intentionally stops new exposure if it cannot be funded.

**High-level legal consideration:** ETH consideration, chance-based allocation and freely cashable/tradable prizes warrant jurisdiction-specific gambling analysis before launch. The UK Gambling Commission identifies cash-convertible game items as money or money's worth in its guidance; this is one jurisdiction's view, not a global classification of this design. Counsel should address licensing, age/access restrictions, consumer disclosures, financial-promotion/securities issues around the token/dividends, AML/sanctions and tax. Immutability and a frontend geofence do not themselves answer those questions. [UKGC guidance](https://www.gamblingcommission.gov.uk/authorities/codes-of-practice/guide/page/digital-and-virtual-currencies), [loot-box statement](https://www.gamblingcommission.gov.uk/news/article/loot-boxes-within-video-games).

### Unresolved matters and release gates

- **Real-world commitments:** no reserve sponsor, team fee beneficiary, token name/symbol, market LP provider or permitted target jurisdictions have been supplied. This research does not need to invent them; a deployment request must provide them before constructing executable arguments or authorizing transactions.
- **Infrastructure permanence:** exact deployed IMD attestation fixtures and canonical question hashing must be integration-tested. The specified quorum's availability and economics are unmeasured. A fixed signer/schema and coordinator create permanent external liveness dependencies.
- **Token eligibility:** no non-WETH token is certified by this report. Each candidate needs current code, pool-depth and manipulation-cost analysis. The reward-route pool does not yet exist for the proposed platform token.
- **Gas and bytecode:** all Bag gas and deployment-cost numbers are estimates. The five-contract architecture satisfies the stated structural counts, but implementation size and a full launch gas payload have not been compiled or tested.
- **FWA research limits:** verified Solidity retrieval through Etherscan was unavailable, so this is not a source audit. Published ABI layouts, project docs and pinned chain reads underpin the analysis. The July exploit was not replayed; current fee-recipient splits and V2 emission funding were not fully reconstructed. Reported farming profitability and organic-versus-incentivized demand remain unproven.
- **Economic limits:** the model lacks endogenous inventory exits, correlated price paths, option exercise under volatility, manipulation optimization and realistic keeper congestion. A reserve stop protects payment commitments but can close the business. Zero simulated insolvencies cannot certify solvency of unimplemented contracts.

## 7. Reproducibility and local checks

The required deliverable is this report. Companion source files are ordinary repository files, not additional named artifacts:

- `README.md`: task scope, commands and evidence limits.
- `simulation/model.py` and `simulation/results.json`: offline model, exact parameters/seed and results.
- `research/onchain-snapshot.json`: pinned getter results, runtime hashes and successful transaction/log examples, including explicitly recorded unsuccessful getter probes.
- `research/collect_activity.py` and `research/activity-windows.json`: read-only archival event aggregation with block hashes and sample events.
- `research/fee-series.json`, `research/imd-capabilities.json`, `research/imd-attester.json`: dated public data used in the report.
- `research/evidence-manifest.json`: source provenance and SHA-256 hashes of delivered data.
- `research/check_report.py` and `research/check-results.json`: local consistency checks, with no independent review authority.

Run the model offline with `python3 simulation/model.py`. Reproducing historical activity needs an archival Ethereum endpoint passed explicitly to `python3 research/collect_activity.py --rpc URL` and Foundry's `cast` for event hashing. Only `eth_call`, code/block/log/receipt and transaction reads were used in this research. Public contract, block and transaction links identify the evidence; machine-local provider addresses are not cited as sources. The brief supplied no public Ethereum RPC URL to attribute, so no substitute provider is invented.

Checks validate numerical consistency, file integrity and the saved evidence relationships. They do not certify FWA's claims, deployed contract behavior, legal suitability or the security of the proposed design.
