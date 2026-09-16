# Stablecoin v4 research — R5: collateralized controls and cross-chain comparators

**As of:** 2026-09-16T03:48:11Z  
**Historical window:** 2020-01-01 through 2021-12-31  
**Conclusion:** collateralization was not a single control. The cases differed in collateral title, redemption, liquidation throughput, oracle and governance authority, and who absorbed a shortfall. DAI’s March 2020 loss arose despite overcollateralized vaults because auctions and keepers failed under congestion; LUSD shifted first-loss capacity to voluntary Stability Pool depositors and then surviving borrowers; sUSD mutualized market and oracle risk across SNX stakers; Kava USDX combined CDPs with cross-chain custody and auction dependencies; VAI showed that nominal excess collateral without a credible holder redemption can coexist with a persistent discount. These controls neither establish that a new asset is necessary nor that collateral alone assures stability.

## 1. Coverage and method

I searched Ethereum/Maker, Liquity and Synthetix repositories and governance materials; BNB Smart Chain/Venus; Kava’s Cosmos SDK chain and its Binance Chain gateway; dForce’s Ethereum USDx; and ancestry leads for BitUSD and NuBits. Deep cases are **DAI, LUSD, sUSD and Kava USDX**. VAI is a shorter, evidence-rich stress comparator; dForce USDx is an adjacent namesake. Searches stopped after the four priority mechanisms, one additional failure comparator, the principal USDX collision, and ancestry were documented. This is not a completeness claim. Unresolved queue: exact historical Kava genesis parameters by upgrade height; archival VAI deployment bytecode/addresses and the final accounting of its 2021 shortfall; historical supplies and peg time series; exact bridge contract/custodian inventories for every secondary deployment; and contemporaneous BitUSD/NuBits 2020–2021 activity.

Methodologically, a current documentation page is evidence of the described mechanism, not automatically evidence that every parameter applied in 2020. Deployment manifests, dated SIPs/MIPs, release tags and dated governance posts carry more temporal weight. “Verified” in the dataset means a first-party deployment/code manifest identifies the address; it does not mean this report independently matched explorer bytecode. Claims use stable IDs that resolve in the JSON source register.

No sibling campaign reports were requested or read; I have no known exposure to them.

## 2. Census and taxonomy

| Case | Window status | Target and backing | Holder exit / peg path | First material loss bearer |
|---|---|---|---|---|
| DAI (MCD) | Included; active throughout | USD soft peg; heterogeneous vault collateral, later material centralized-stablecoin exposure | Market arbitrage; vault repayment; PSM from Dec. 2020; direct collateral claim only after Emergency Shutdown | Liquidated vault owners, then surplus, ultimately MKR dilution; DAI holders can be haircut in shutdown [R5-C001–R5-C005] |
| LUSD v1 | Included; launched 2021-04-05 | USD peg; borrower-owned ETH locked in immutable contracts | Permissionless $1-of-ETH redemption plus borrowing/redemption fee feedback | Trove owner; Stability Pool depositors; residual debt/collateral redistributed to active Troves [R5-C006–R5-C010] |
| sUSD / Synthetix v2 | Included; active | USD unit; pooled SNX collateral and system-wide synthetic debt | Burn for issuer debt; synth exchange/AMM arbitrage; no unconditional $1 collateral redemption | Flagged SNX stakers and, economically, all debt-pool stakers [R5-C011–R5-C014] |
| Kava USDX | Included; cross-chain case | USD reference; CDPs holding imported and native assets | Repay/burn; secondary-market arbitrage; no general par redemption documented | CDP owner, then auction outcome, then KAVA dilution/governors [R5-C015–R5-C019] |
| VAI | Included, triaged | USD target; Venus money-market collateral capacity | Repayment and market demand; no evidenced unconditional par redemption in reviewed period | Borrowers/liquidators and ultimately protocol/risk-fund/governance stakeholders [R5-C020–R5-C022] |
| dForce USDx | Adjacent namesake | Basket/meta-stablecoin, not Kava CDP USDX | Constituent-stablecoin conversion design | Constituent/custody/governance exposure; not reconstructed deeply [R5-C023] |

The central taxonomy is therefore: (1) **redeemable single-collateral debt money** (LUSD); (2) **governed multi-collateral debt money with a balance-sheet backstop and PSM** (DAI); (3) **pooled synthetic liability** (sUSD); (4) **application-chain CDP money with imported collateral and validator/governance backstop** (Kava USDX); and (5) **overcollateralized credit without a strong holder-side par conversion** (VAI). “Crypto-backed” obscures these balance-sheet differences.

## 3. Deep cases

### 3.1 DAI: collateral auctions, governance and the PSM

Multi-Collateral Dai was already deployed in November 2019, so it qualifies as an earlier system materially active in the window. Vault users retained beneficial ownership of excess collateral but transferred enforceable control to the protocol until debt repayment. Governance selected collateral types and risk parameters, trusted oracle sets, the one-hour Oracle Security Module delay, and emergency actors. DAI was a $1 **soft peg**, not an ordinary on-demand claim on a specific reserve asset. Before shutdown, normal holder exit was a market sale; vault owners bought/burned DAI to free their own collateral. Emergency Shutdown froze feeds and later let DAI holders claim a proportional collateral basket, potentially with a haircut [R5-C001, R5-C002].

Liquidations 1.x moved unsafe vault collateral into English auctions requiring keepers to source DAI and bid. On 2020-03-12, severe ETH decline, gas congestion and thin keeper participation permitted zero/near-zero bids, leaving protocol bad debt and extraordinary losses for affected vault owners. The later MIP45 Liquidations 2.0 design replaced this with Dutch auctions: `Dog.bark` confiscates the vault, records bad debt in `Vow`, starts a `Clipper`, and pays keeper incentives. This is causal evidence against equating nominal collateral ratio with realizable collateral value: liquidation market access and operational diversity were part of backing quality [R5-C003, R5-C004].

Bad debt first consumes system surplus; debt auctions mint MKR for DAI, diluting MKR holders. Conversely surplus auctions can burn MKR. Thus MKR is a contingent recapitalization claim, not segregated reserve collateral. Governance itself is powerful: it can add risky or centrally controlled collateral, modify ceilings and fees, select oracles, and execute shutdown after the governance delay [R5-C002].

The USDC Peg Stability Module, activated in December 2020, materially changed the peg. It allowed fixed-price, low-slippage exchange between DAI and USDC subject to governance-set fees and limits, strengthening downward/upward arbitrage but importing Circle freeze, custody, banking and USDC depeg risk. Inference: PSM inventory is economically closer to reserve backing than borrower overcollateralization, even though it sits inside Maker’s governed accounting [R5-C005]. DAI on other chains during the period generally depended on canonical or third-party lock/mint bridges rather than independent MCD balance sheets; those representations inherit bridge administration and message-finality risk. Exact historical bridge inventories remain a gap.

### 3.2 LUSD v1: direct redemption and explicit loss waterfall

Liquity’s first-party deployment manifest dates mainnet to 2021-04-05 and identifies LUSD at `0x5f98805A4E8be255a32880FDeC7F6728C6568bA0`; it also records the deployed core addresses and code version. The core was designed as immutable and governance-free, accepting only ETH. Borrowers owned the economic residual of a Trove, but its ETH was controlled by protocol contracts until repayment or liquidation [R5-C006, R5-C007].

The hard peg path was unusually direct: anyone could redeem LUSD for $1 worth of ETH (less a dynamic fee), starting with the lowest-collateralized Troves. A 110% minimum collateral ratio created the complementary upper-side borrowing arbitrage. Redemptions increase `baseRate`; the rate decays with a 12-hour half-life, affecting future borrowing and redemption fees. This was real collateral conversion, not merely a promise that market makers would return the price to par [R5-C008].

Liquidation avoided auctions. Below 110%, Stability Pool LUSD was burned against debt and depositors received the Trove’s ETH; any uncovered remainder was redistributed, debt and collateral together, to active Troves. Anybody could trigger liquidation for gas compensation. When system TCR fell below 150%, Recovery Mode blocked worsening actions and expanded liquidatability. Consequently loss absorption was legible: borrower equity first; then Stability Pool depositors bear LUSD burn in exchange for volatile ETH; then surviving borrowers inherit redistributed debt and collateral. If ETH falls faster than execution and pool depth can absorb, “overcollateralized” can still become economically insufficient [R5-C009, R5-C010].

Oracle dependence did not disappear. The deployed PriceFeed was fixed at launch and mediated ETH/USD inputs/fallback behavior; immutability removed parameter capture but also removed ordinary emergency repair. Keepers were permissionless transaction submitters rather than capital-bidding auctioneers, reducing but not eliminating dependence on timely Ethereum inclusion and economically motivated bots.

Later outcome: LUSD v1 remained distinct when Liquity v2/BOLD launched; current v2 materials explicitly describe removal of v1 Recovery Mode and different multi-collateral branch/shutdown logic. That redesign is hindsight, not evidence that v1 had those controls. It does show which v1 trade-offs the project later revisited [R5-C024]. Non-Ethereum LUSD encountered in the period or later should be presumed bridged/wrapped unless an independently deployed Liquity core is proven; the reviewed first-party manifest establishes only Ethereum.

### 3.3 sUSD: pooled debt, reflexive SNX and administrative controls

sUSD was not a vault claim. SNX stakers minted sUSD while assuming a proportional share of a **pooled debt** whose value changed as users traded among synths. Locked SNX was volatile and reflexive: system stress could depress the backstop itself. A staker burned sUSD to reduce their debt and unlock SNX, but an unrelated holder lacked an unconditional $1 claim on collateral. Peg support therefore leaned on exchange utility, AMM/market arbitrage, staking incentives and governance-set fees rather than hard redemption.

SIP-15’s implemented liquidation mechanism allowed an undercollateralized SNX account to be flagged, gave it a delay to repair, then let a liquidator burn sUSD and receive SNX plus a penalty until the target ratio was restored. The SIP explicitly notes that below collateral plus penalty, liquidation can leave debt and anticipated an insurance fund. This makes ultimate loss mutualization materially different from LUSD’s ordered Troves: debt-pool participants remain exposed to aggregate synthetic positions and oracle pricing [R5-C011, R5-C012].

Oracle and admin powers were extensive. Chainlink prices, exchange waiting periods/reclaims, circuit breakers, issuance ratios, liquidation ratios/penalties and system suspension were configurable through the protocol’s governance/owner machinery. SIP-120 (created 2021-02-24) proposed atomic exchanges using Chainlink plus Uniswap v3 prices, per-block caps and volatility circuit breakers; it candidly described profitable oracle-latency trading as an expense to the debt pool [R5-C013]. The May 2021 deprecation notice for EtherCollateral loan contracts further shows active administrative migration: new loans were paused and remaining loans became liquidatable after a stated deadline [R5-C025].

Cross-chain architecture became balance-sheet architecture. SIP-165, created 2021-12-16 for Ethereum and Optimism, said each chain then had an isolated debt pool and proposed synthesis using Chainlink-reported cross-chain debt/debt-share ratios and Optimism messaging for fee-period closure. The proposal therefore documents additional oracle, relayer/message and chain-liveness dependencies rather than a trust-free duplicate deployment [R5-C014]. Later versions and sUSD peg stress must not be projected backward; a complete post-2021 incident chronology was not established in this bounded pass.

### 3.4 Kava USDX: application-chain CDPs and imported collateral

Kava USDX is the relevant cross-chain USDX comparator—not dForce USDx and not newer same-ticker products. It was a native coin on Kava’s Cosmos SDK application chain, minted from CDPs. In the documented BNB path, Binance Chain BNB was frozen/unfrozen while a representation was minted/burned on Kava. Backing quality therefore combined collateral market risk with gateway custody/operations, Binance Chain availability, Kava validator consensus, and pricefeed governance [R5-C015, R5-C016].

The CDP module locked user collateral, minted USDX up to parameterized limits, accrued fees each block, and burned repayment. Governance parameters included collateral-specific liquidation ratios, ceilings, stability fees, market IDs, global debt limits, savings allocation and auction thresholds. A missing price suspended liquidations, fees, collateral changes, new CDPs and further draws—safer than acting on a stale value, but capable of freezing risk reduction during stress [R5-C017].

Unsafe collateral moved to two-stage auctions: bidders first increased USDX for the full lot, then decreased collateral demanded once the maximum debt bid was reached; surplus returned to the original CDP owner. This required independently funded USDX auction bots and timely Kava access. If collateral auctions failed to cover debt and a threshold was reached, debt auctions minted KAVA for USDX. Thus borrowers lost collateral first, competitive bidders determined execution, and KAVA holders absorbed residual insolvency through dilution; governors/validators were explicitly the lender of last resort [R5-C018, R5-C019].

USDX documentation calls the peg “loose” and says market forces determine price. No unconditional holder-side $1 redemption was found. Repayment demand and auctions burn USDX, while governance adjusts parameters and incentives. This is weaker price-floor machinery than LUSD’s face-value ETH redemption. A later exact shutdown/depeg accounting was not recovered; it remains an explicit high-priority gap, not a claim of no incident.

## 4. Additional comparator: VAI

VAI was minted on BNB Smart Chain against Venus money-market collateral capacity. It qualifies as active in 2020–2021, but this pass did not recover a version-pinned launch deployment manifest, so its addresses are recorded as unknown rather than “verified.” A Venus team post dated 2021-09-08 acknowledged serious oversupply, said USD:VAI exceeded 1.3:1, and proposed pausing minting. That is direct project evidence that excess collateral did not itself create holder demand or a par exit [R5-C020].

The 2021 design debate added a stability fee to discourage supply, while liquidation depended on Venus account solvency and liquidator participation. The May 2021 XVS price-manipulation/liquidation episode left a protocol shortfall; later Venus governance proposed risk-fund income, XVS-vault slashing, unissued XVS and ultimately a bond as a loss waterfall. Because the reviewed proposal is partly prospective, those mechanisms are project claims, not proof that they were live during the incident [R5-C021, R5-C022]. VAI illustrates three distinct failures: peg/demand imbalance, oracle/market manipulation, and bad-debt socialization. They should not be collapsed into “insolvency.”

## 5. USDX disambiguation and non-Ethereum dependencies

**Kava USDX** (uppercase) was native to Kava and debt-created; collateral such as BNB crossed via a freeze/mint gateway. **dForce USDx** (often styled lowercase x) was an Ethereum meta/index stablecoin launched from late 2019 and described in dForce’s 2020 whitepaper as a basket-based synthetic stablecoin. These are different issuers, chains, balance sheets and redemption stories [R5-C023]. Present-day `usdx.money` (delta-neutral) and `usdxstable.com` (fiat-reserve, multi-EVM) appeared in discovery but are later same-ticker products and excluded from the historical protocol census.

Non-Ethereum risk is not captured by writing “multichain”:

- Kava imported assets depended on the source chain plus freeze/mint gateway operators and Kava consensus.
- Synthetix’s Ethereum/Optimism plan depended on common debt oracles and cross-chain messaging; the debt itself was intended to become cross-domain.
- DAI and LUSD representations outside their canonical Ethereum accounting inherit bridge lockboxes, upgrade keys/custodians and destination-chain liveness unless independently native issuance is proven.
- VAI was native to BNB Smart Chain, inheriting its validator/governance and oracle environment rather than an Ethereum bridge.

## 6. Dated outcomes and stress attribution

| Date | Event | Classification and loss allocation |
|---|---|---|
| 2020-03-12 | Maker Black Thursday auctions cleared at zero/near-zero bids amid congestion | Liquidation-market/keeper failure during price crash; affected vault owners lost collateral, protocol booked bad debt, MKR backstop was invoked [R5-C003] |
| 2020-12 | Maker USDC PSM activated | Redesign/peg support; reduced price friction while importing centralized collateral and freeze risk [R5-C005] |
| 2021-04-05 | Liquity v1 deployed | Launch; immutable ETH-only system with direct redemption and Stability Pool [R5-C006] |
| 2021-05 | Venus XVS episode and shortfall | Oracle/market manipulation plus liquidation shortfall; subsequent proposals socialize recovery through protocol revenue/XVS mechanisms [R5-C021, R5-C022] |
| 2021-06-25 | Synthetix legacy EtherCollateral loans became liquidatable after sunset notice | Controlled migration; remaining borrowers risked all collateral to third-party repayment [R5-C025] |
| 2021-09 | Venus acknowledged material VAI oversupply/off-peg | Demand/peg failure, not by itself proof of collateral insolvency [R5-C020] |
| 2021-12-16 onward | Synthetix proposed synthesized Ethereum/Optimism debt pools | Cross-chain redesign introducing common-oracle and messaging dependencies [R5-C014] |
| 2025-era v2 documentation | Liquity BOLD architecture removed v1 Recovery Mode and uses branch shutdown logic | Later redesign; not silently attributed to LUSD v1 [R5-C024] |

## 7. Constraints for later designers (not a protocol design)

1. **Specify the creditor and the claim.** “Backed” must state who owns collateral, whether holders can redeem it, in what asset, at what time, with what priority and fee.
2. **Model liquidation as market infrastructure.** Collateral ratio is only a mark; congestion, oracle delay, bidding capital, chain inclusion and keeper concentration determine realization.
3. **Make the loss waterfall executable.** Name borrower equity, reserve/surplus, stability depositors, surviving borrowers, governance-token dilution and holder haircut in order. Avoid prospective “insurance” being reported as funded coverage.
4. **Separate peg liquidity from solvency.** VAI’s discount and DAI’s PSM show that demand/convertibility can dominate the market peg even when accounting collateral exists. Conversely a liquid peg can mask concentrated custodian exposure.
5. **Treat oracle/admin authority as liabilities.** Pause, upgrade, parameter, feed-selection, freeze and shutdown powers need dated ownership; immutability trades capture risk for recovery rigidity.
6. **Bound keeper assumptions.** Permissionless entry does not prove participation. Required inventory, profitability during gas spikes, transaction ordering and fallback paths are system constraints.
7. **Account for correlation and reflexivity.** SNX or governance-token backstops can fall when liabilities rise; stablecoin PSM collateral can depeg together; bridged collateral adds common custodians.
8. **Represent cross-chain debt explicitly.** A wrapped token, native duplicate and synthesized debt pool are different. Message delay, replay/finality, lockbox control and chain halt determine whether supplies reconcile.
9. **Do not infer necessity or stability from controls.** These comparators identify failure surfaces. They do not prove a new asset improves welfare, nor that collateral eliminates monetary, governance or operational risk.

## 8. Disputes, gaps and unresolved queue

- Kava’s current docs expose module concepts and example parameters but not a fully reconstructed 2020/2021 parameter timeline by height. Historical genesis and governance transactions are needed.
- VAI’s exact launch addresses, source commit, liquidation formula by deployed version, and audited 2021 bad-debt ledger remain unresolved. Team/community posts are not substitutes.
- Maker’s exact bridge deployments and PSM parameter changes by executive spell were not exhaustively enumerated.
- Synthetix SIP status proves proposal lifecycle metadata, but implementation dates/releases should be matched to deployment transactions for a full chronology.
- No complete price/supply dataset was gathered; qualitative “depeg” statements are limited to attributable project admissions.
- Current LUSD/Kava documentation may have changed wording. Versioned repository manifests or release tags are preferred where available.
- BitUSD and NuBits were not shown, in this search, to satisfy independent material activity in 2020–2021; they remain ancestry rather than controls.

## 9. Ancestry appendix (not 2020–2021 controls)

**BitUSD** is an earlier BitShares market-issued asset lineage: collateralized debt positions, feed prices, margin calls and settlement mechanisms influenced later on-chain stable assets. **NuBits** is a separate seigniorage/liquidity-support lineage and need not be collateralized. Neither is used here as evidence that collateralized controls succeeded in the study window. Their 2020–2021 activity was not independently verified in this bounded pass, so the JSON marks them ancestry and records the gap rather than backfilling current descriptions.

## 10. Source register

Full metadata, retrieval dates, limitations and locators are in `r5-data.json`. Key sources:

- **R5-S001:** Maker MCD whitepaper (Feb. 2020), governance, oracles, shutdown and loss backstop: https://makerdao.com/whitepaper/White%20Paper%20-The%20Maker%20Protocol_%20MakerDAO%E2%80%99s%20Multi-Collateral%20Dai%20%28MCD%29%20System-FINAL-%20021720.pdf
- **R5-S002:** Maker MIP45 Liquidations 2.0: https://mips.makerdao.com/mips/details/MIP45
- **R5-S003:** Maker first-party MCD deployment addresses: https://github.com/sky-ecosystem/dss-deploy-scripts
- **R5-S004:** Liquity v1 deployment manifest: https://github.com/liquity/liquity/blob/master/packages/lib-ethers/deployments/default/mainnet.json
- **R5-S005–S008:** Liquity v1 general, redemption, Stability Pool and Recovery Mode docs: https://docs.liquity.org/liquity-v1
- **R5-S009:** Liquity v1 repository/architecture: https://github.com/liquity/dev
- **R5-S010:** Liquity v2 borrowing/liquidation comparison: https://docs.liquity.org/v2-faq/borrowing-and-liquidations
- **R5-S011:** Synthetix SIP-15 liquidation: https://github.com/Synthetixio/SIPs/blob/master/content/sips/sip-15.md
- **R5-S012:** Synthetix SIP-120 atomic exchange/oracle controls: https://github.com/Synthetixio/SIPs/blob/master/content/sips/sip-120.md
- **R5-S013:** Synthetix SIP-165 cross-chain debt synthesis: https://github.com/Synthetixio/SIPs/blob/master/content/sips/sip-165.md
- **R5-S014:** Synthetix EtherCollateral deprecation notice: https://blog.synthetix.io/deprecating-ethercollateral-loan-contracts/
- **R5-S015–S019:** Kava basics, CDP concepts/parameters, auctions and bot documentation: https://docs.kava.io/docs/cosmos/modules/cdp/concepts/
- **R5-S020–S022:** Venus VAI peg admission, code, and shortfall proposal: https://community.venus.io/t/the-solution-to-re-peg-vai-is-coming/1760
- **R5-S023:** dForce 2020 whitepaper: https://raw.githubusercontent.com/dforce-network/documents/master/white_papers/en/dForce_Whitepaper_V1.pdf

## 11. Validation notes

The dataset was parsed as a single UTF-8 JSON object. A local validator checked every required top-level key, required uniform protocol/version/incident/source/claim/search/exclusion/uncertainty fields, ID uniqueness, protocol/version/source/claim references, and report claim/source identifiers. It does not independently certify historical truth, completeness, archive persistence, contract bytecode, or economic causation. URLs were retrieved during this research turn; inaccessible/dead-end routes are retained in the search log. Word-count target was checked excluding the source register.
