# Stablecoin v4 research R4: fractional reserves and protocol-controlled liquidity

**As of:** 2026-09-16T00:00:00Z (retrieval day; exact completion time is in the dataset)  
**Window for eligibility:** 2020-01-01 through 2021-12-31; later events are traced as outcomes, not projected backward into launch mechanics.  
**Bottom line:** fractional redemption can turn a falling endogenous share token into the run’s accelerant, while protocol ownership of liquidity prevents LP withdrawal but does not create a holder’s redemption claim. FRAX v1, Polygon IRON, and FEI v1 allocated superficially similar “backing” in legally and economically different ways. Their stress outcomes therefore cannot be compared using one collateral-ratio number.

## Coverage and method

I searched Ethereum, BNB Smart Chain (BSC), Polygon PoS, and Fantom Opera sources for the three assigned families, then bounded the contrast set to Olympus and Tomb. The deep set is FRAX, IRON, and FEI; Olympus and Tomb are shorter adjacent records because neither launch asset was a dollar-redeemable fractional stablecoin. Discovery routes included project documentation, repositories/releases, explorer-published code and addresses, audits, project postmortems, governance/shutdown code, and an event study based on Polygon transactions. Search-result snippets were not treated as retrieved primary evidence. Stable claim IDs below resolve to `artifacts/r4-data.json`.

The search stopped after the three required families had versioned mechanism and outcome evidence and the two mandated adjacent comparisons had primary descriptions. This is not a completeness claim. I did not enumerate every 2020–21 Basis fork, obtain a complete historical state reconstruction, or independently replay transactions. The unresolved queue is: archived IRON source/parameter snapshots and BSC wind-down; FEI’s inaccessible forum votes and exact activation blocks; FRAX v1 pool-by-pool reserve snapshots and exact v1→AMO transition; Tomb’s September exploit transaction/code; and Olympus v1 deployment dates/roles from contemporaneous rather than current legacy docs. No sibling reports were requested or read, and I have no known exposure to them.

## Census and taxonomy

| Family | Eligibility | Target | Reserve/control model | Holder exit at launch |
|---|---|---|---|---|
| FRAX v1 | Included, deep | USD 1 | External collateral plus endogenous FXS; dynamic target CR | Protocol mint/redeem, with collateral and newly minted FXS at fractional CR |
| IRON BSC / Polygon | Included, deep | USD 1 | BUSD+STEEL on BSC; USDC+TITAN on Polygon; separate deployments | Fractional protocol redemption; Polygon’s endogenous leg collapsed |
| FEI | Included, deep | USD 1 | Protocol-owned ETH/FEI liquidity (PCV), later diversified reserves and PSM | Launch: secondary market, not a general par claim on PCV; later versions added direct stabilization/redemption facilities |
| Olympus v1 | Adjacent | Floating reserve currency, not USD peg | Treasury-owned reserves and LP tokens acquired through bonds | Market sale; no promise that one OHM redeems for one dollar |
| Tomb | Adjacent | 1 TOMB per 1 FTM, not USD | Seigniorage/share/bond loop plus developer-controlled DAO fund | Market sale or voluntary TOMB→TBOND below peg; not external-collateral redemption |

Basis-style multi-token seigniorage is ancestry, not an extra deep family: Tomb itself identifies Basis, bDollar, and soup as inspiration [R4-C020]. No unlaunched proposal was promoted to deployed status. FEI’s prelaunch mechanism claims are kept separate from what happened after genesis, and current FRAX documentation is used only where it expressly marks the v1 mechanism “retired” [R4-C001].

## Deep case 1 — FRAX v1: a fractional claim with a reflexive remainder

FRAX launched on Ethereum on 20 December 2020. Its own historical page calls v1’s sole mint/redeem AMO the “base stability mechanism” and explicitly says it was retired in later versions [R4-C001]. At v1, FRAX targeted $1; FXS was the governance/value-accrual and endogenous absorption token. When the market price of FRAX exceeded $1, the target collateral ratio (CR) stepped down; below $1, it stepped up [R4-C002]. This was a policy target, not proof that immediately liquid collateral equaled liabilities.

The pool interface exposed distinct 100%, fractional, and 0%-collateral mint/redeem functions. In the fractional phase a minter supplied external collateral and FXS; a redeemer burned FRAX and received collateral plus newly minted FXS. Collection was a second transaction, documented as a flash-loan defense [R4-C003]. At an 85% CR the project’s historical explanation gives $0.85 USDC and $0.15 newly minted FXS for one FRAX [R4-C004]. Thus the dollar claim was partly a fixed external asset claim and partly a contemporaneously priced claim on dilution capacity. Early redeemers could sell the endogenous leg while liquidity remained; late holders bore worsening slippage and FXS dilution if demand fell.

The control loop depended on market-price oracles: v1 documentation identifies Uniswap TWAP inputs and Chainlink USD pricing [R4-C005]. Oracle delay can be protective against a one-block manipulation yet dangerous in a fast endogenous-asset fall: redemption quantities are computed from a lagged value while executable exit is at spot. Recollateralization paid FXS plus a documented 0.75% incentive for external collateral, while excess collateral could buy back FXS [R4-C006]. Those actions assigned gains to arbitrageurs and dilution to FXS holders; they did not guarantee that collateral could be acquired during a confidence shock.

The essential run condition is reflexive: if FRAX trades below peg, the CR is supposed to rise, but each fractional redemption mints FXS. Selling that FXS depresses the very asset funding the remaining redemption promise. The mechanism can survive only if external collateral plus credible future FXS demand and market depth absorb redemptions faster than the endogenous leg deteriorates. This is an inference from the documented mechanics, not a claim that FRAX v1 suffered an IRON-scale collapse [R4-C007].

Later Frax should not be silently folded into this result. Current historical docs distinguish v1 from v2’s broader AMOs; later protocol-owned market operations, lending, swaps, and eventual fully collateralized policy are redesign evidence, not launch properties [R4-C008]. The relevant survival fact is narrower: FRAX continued and changed its machinery; that does not validate every v1 counterfactual under an unobserved maximal run.

## Deep case 2 — IRON: same template, separate chains, asymmetric run

IRON is the cleanest natural experiment here. The project announced Polygon launch for 18 May 2021 at 16:00 UTC and explicitly said it was not bridging the BSC tokens: Polygon IRON used USDC and TITAN, whereas BSC IRON remained backed by BUSD and STEEL [R4-C009]. Explorer pages identify separate token contracts: Polygon IRON `0xD86b…ae9a`, Polygon TITAN `0xaAa5…285A`, BSC IRON `0x7b65…ddd8`, and BSC STEEL `0x9001…87eb`; the dataset records exact addresses and verification status [R4-C010]. “IRON” therefore cannot be treated as one fungible cross-chain liability.

The Polygon version maintained a target collateral ratio and effective collateral ratio. At the approximately 75% external-collateral level seen during the run, redemption returned USDC for the external portion and minted TITAN for the balance. TITAN pricing used a ten-minute weighted average while TITAN’s executable spot price fell much faster [R4-C011]. On 16 June 2021 large TITAN sales followed a rapid run-up; the lag made newly created or redeemed IRON packages overvalue TITAN. The target CR could increase only 0.25 percentage points per hour, too slowly to close the gap [R4-C012]. This was not a Solidity theft: it was an oracle/timing and economic insolvency spiral expressed through authorized mint/redemption paths.

Ordering determined outcomes. Large Polygon accounts exited first [R4-C013]. Early arbitrageurs could use stale TITAN valuation; redeemers obtained scarce USDC and dumped minted TITAN. TITAN holders absorbed extreme dilution and price collapse, later IRON holders faced depleted or congested redemption capacity, and LPs suffered reserve composition changes and impermanent loss. The project reportedly spent excess reserves buying TITAN, briefly lifting its price, but the intervention did not stop the run [R4-C014]. IRON traded below the 75% external-collateral ratio transiently, then near $0.75 after TITAN became effectively worthless; panic/liquidity discounts and final external backing were distinct phases.

BSC is crucial contradictory evidence. The Federal Reserve transaction study reports that BSC IRON did not break peg during the same episode even though STEEL declined, and notes that the systems were not mutually arbitrageable [R4-C015]. That weakens a story of universal loss of trust in the brand or code alone. It supports a chain-specific trigger: Polygon TITAN’s prior bubble, abrupt selling, oracle lag, and local liquidity. It does not prove BSC was structurally safe; the same reflexive template remained exposed to a sufficiently fast STEEL run.

LP “value” also needs care. An IRON/USDC LP token was a pro-rata claim on AMM inventory, not a fixed quantity of USDC; arbitrage transferred USDC out as IRON flowed in. Counting both gross LP notional and the reserve assets underlying it would double-count backing. Protocol farming emissions amplified liquidity while demand lasted but did not establish senior redemption rights. The post-run outcome was effectively residual recovery through the external-collateral component, with endogenous holders and late claimants bearing losses; no evidence supports retroactively calling the launch fully collateralized.

## Deep case 3 — FEI: owned liquidity is not user-owned collateral

FEI launched on Ethereum on 3 April 2021. Genesis contributors committed ETH and received FEI/TRIBE; the launch seeded FEI–ETH and FEI–TRIBE Uniswap markets [R4-C016]. The defining balance-sheet distinction was Protocol Controlled Value (PCV): the protocol owned contributed ETH and deployed it as liquidity. Users did not hold a withdrawal receipt for that ETH. Consequently, “PCV approximately equals circulating FEI value” did not mean each FEI had an enforceable par redemption at launch.

V1 expansion sold FEI through an ETH bonding curve. Below peg, direct incentives minted rewards to buyers and burned an increasing amount from sellers on the incentivized FEI–ETH pool. Governance-controlled PCV could withdraw liquidity, buy FEI to move the pool price, redeposit remaining assets, and burn acquired FEI—a reweight [R4-C017]. Protocol ownership prevented a private LP whale from withdrawing the core liquidity, but holders still exited into an AMM whose ETH reserve and curve set marginal recovery. Control over liquidity is therefore operational power, not identical to a senior collateral claim.

At genesis, excess FEI supply and selling pressure pushed FEI below peg. The burn penalty made an already-lossy exit still worse and was not correctly surfaced by generic Uniswap routing; the project warned users to use its interface to see the burn [R4-C018]. A separately discovered April 6 vulnerability could have repeatedly drained about 1,410 ETH by earning buy rewards then bypassing sell penalties through transfers; it was reported before exploitation and rewards were paused [R4-C019]. That incident is a code/economic incentive bug, distinct from the observed launch liquidity crisis.

FEI’s later history changes the comparison. FIP-2-era changes and later stabilizers moved toward explicit redeemability and diversified PCV. The repository’s v2.0 release (`76739f5`) includes collateralization oracles, rate-limited minting, a Tribe reserve stabilizer, Curve deposits, and removal of the original Uniswap PCV controller [R4-C021]. FEI v2 went live in December 2021; its balance-sheet framework treated TRIBE as a recapitalization/backstop asset rather than merely applying launch direct incentives [R4-C022]. These later facilities cannot be cited as rights genesis holders already possessed.

After the 2021 Rari merger, an April 2022 Fuse exploit created losses outside FEI’s original peg machinery. The DAO subsequently dissolved. Shutdown code created an immutable FEI–DAI 1:1 wrapper intended to be seeded with enough DAI for circulating (not protocol-owned) FEI, a separate capped Fuse claimant process, and pro-rata TRIBE redemption in remaining assets [R4-C023]. Ordering was explicit: burn protocol-owned FEI, fund FEI redemption, handle eligible exploit claims, and distribute residual assets to TRIBE. FEI holders therefore received a senior par path in shutdown; TRIBE holders were residual; capped hack victims depended on the separate Merkle allocation. This was governance-directed wind-down after later losses, not evidence of a launch PCV redemption promise.

## Adjacent monetary experiments

**Olympus v1.** Olympus sold discounted OHM in exchange for reserve assets or LP tokens (“bonds”), causing the treasury—not mercenary LPs—to own reserves and liquidity. Stakers received rebasing sOHM emissions [R4-C024]. OHM was marketed as a reserve currency with a floating market price, not a $1 stablecoin. Treasury backing constrained policy and provided optional intervention capacity, but an OHM holder did not have a routine right to redeem one OHM for one dollar. LP-token valuation remained contingent on both pool legs and AMM state. Its relevance is protocol-owned liquidity and treasury acquisition, not dollar-peg evidence.

**Tomb.** Tomb launched on Fantom on 2 June 2021 and targeted one TOMB per one FTM, so its USD value floated with FTM [R4-C020]. Above target, the Masonry minted TOMB to TSHARE stakers (with DAO/developer allocations); below target, users could voluntarily burn TOMB for TBOND and later redeem bonds when price recovered. During debt phase, 65% of expansion was reserved for bonds [R4-C025]. A developer-controlled DAO fund could buy below peg or sell above it [R4-C026]. This is seigniorage debt plus discretionary reserves, not fractional external collateral. A September 2021 exploit/social panic and bank run were described in the project postmortem; the exact exploit transaction remains unresolved [R4-C027]. TOMB’s presence here must not imply a dollar peg.

## Cross-case loss ordering and stress properties

| Mechanism | First practical exit | What fails under a run | Primary loss bearer |
|---|---|---|---|
| FRAX v1 fractional | Redeem for collateral + minted FXS, then sell FXS | FXS liquidity/demand and oracle execution can deteriorate faster than CR rises | FXS holders, then late FRAX holders through slippage/capacity |
| Polygon IRON | Redeem/mint using USDC + TWAP-valued TITAN | Stale endogenous price overstates value; redemptions hyperinflate TITAN and drain external reserve | TITAN holders, LPs, late IRON holders |
| FEI v1 | Sell into protocol-owned AMM | Penalty and curve impede exit; PCV value/liquidity is not a par claim | Sellers and remaining FEI holders through market discount; PCV absorbs interventions |
| Olympus | Sell OHM | Treasury backing is not routine redemption; emissions/demand can diverge | OHM/LP holders through price and dilution |
| Tomb | Sell or burn into TBOND | Contraction requires voluntary demand for junior debt and eventual future expansion | TOMB/TSHARE/TBOND holders according to timing |

Two properties survived stress more often than slogans did. External stablecoin inventory retained residual value after endogenous shares failed (Polygon IRON), and protocol ownership kept liquidity from simply being withdrawn (FEI/Olympus). Neither property alone ensured par. Early-exit advantage remained whenever redemption was sequential, reserve-limited, oracle-lagged, or routed through finite AMM depth.

## Historical constraints for later designers (not a protocol design)

1. **Separate asset ownership from claimant rights.** “Backing,” PCV, treasury assets, and AMM liquidity are not interchangeable. State who owns each asset and whether a token holder has a callable claim.
2. **Value LP positions net, under stress.** LP notional is endogenous to pool prices; never count the LP token and its underlying reserves twice. Model reserve composition after adverse arbitrage.
3. **Endogenous recapitalization is executable only with demand.** Minting a share token can balance accounting at an oracle price while destroying realizable recovery at spot.
4. **Oracle smoothing trades manipulation resistance for run latency.** IRON shows a ten-minute average can be catastrophically stale during a minutes-long collapse; CR adjustment cadence must be compared with market speed.
5. **Specify queue and seniority before stress.** Who redeems first, pool ceilings, pauses, two-step collection, and reserve exhaustion determine distribution even if aggregate assets appear sufficient.
6. **Liquidity control is power and risk.** POL prevents third-party withdrawal but concentrates price intervention, valuation, and governance authority. Governance keys and emergency controls belong in solvency analysis.
7. **Contraction needs a willing balance sheet.** Recollateralization rewards, bond buyers, endogenous share purchasers, or treasury spending all require someone to accept risk precisely when confidence is scarce.
8. **Do not infer safety from survival or failure from depeg alone.** BSC IRON’s contemporaneous non-run is evidence about triggers, not proof of robustness; FEI’s launch depeg and later shutdown had different causes.

## Disputes, gaps, and hindsight discipline

The IRON team called the event a bank run; the transaction evidence supports a run amplified by a stale valuation rule, but “ran out of reserves” is qualified by the Fed authors as presumed rather than contract-state proof. FEI’s launch shortfall, unexploited incentive vulnerability, later Fuse loss, and dissolution are separate events. Tomb’s postmortem combines a technical exploit narrative with social-panic attribution and lacks transaction-level corroboration here. Olympus and current FRAX legacy docs are retrospective; they are used only for expressly historical mechanics and cross-checked with repositories/releases where possible.

Unknown deployment dates are null rather than guessed. Explorer `verified: true` means the cited explorer displays exact-match source code; Polygon TITAN and BSC STEEL are not upgraded to exact verification where the retrieved page showed proxy/similar-match ambiguity. No price series was reconstructed, and no source establishes exhaustive coverage.

## Source register

The machine-readable register in `r4-data.json` records publication/event/retrieval dates, access limitations, and locators. Principal sources are:

- [Frax historical v1 design](https://docs.frax.finance/frax-v1-original/original-design) and [v1 pool functions](https://docs.frax.finance/frax-v1-original/frax-pools) (project documentation, explicitly historical).
- [Frax Solidity repository and v1 whitepaper](https://github.com/FraxFinance/frax-solidity) and [verified FXS contract](https://etherscan.io/address/0x3432b6a60d23ca0dfca7761b7ab56459d9c964d0).
- [IRON Polygon launch announcement](https://ironfinance.medium.com/iron-finance-expansion-to-polygon-8a714ba5635e) and [Federal Reserve transaction study](https://www.federalreserve.gov/econres/notes/feds-notes/runs-on-algorithmic-stablecoins-evidence-from-iron-titan-and-steel-20220602.html).
- Explorer records for [Polygon IRON](https://polygonscan.com/address/0xD86b5923F3AD7b585eD81B448170ae026c65ae9a), [Polygon TITAN](https://polygonscan.com/address/0xaaa5b9e6c589642f98a1cda99b9d024b8407285a), [BSC IRON](https://bscscan.com/token/0x7b65b489fe53fce1f6548db886c08ad73111ddd8), and [BSC STEEL](https://bscscan.com/token/0x9001ee054f1692fef3a48330cb543b6fec6287eb).
- [FEI post-genesis notice](https://medium.com/fei-protocol/fei-post-genesis-35284a57a659), [core releases](https://github.com/fei-protocol/fei-protocol-core/releases), [mainnet address registry](https://github.com/fei-protocol/fei-protocol-core/blob/develop/protocol-configuration/mainnetAddresses.ts), [Immunefi postmortem](https://medium.com/immunefi/fei-protocol-vulnerability-postmortem-483f9a7e6ad1), and [shutdown audit scope](https://github.com/code-423n4/2022-09-tribe).
- [Olympus legacy bonds](https://github.com/OlympusDAO/olympus-docs/blob/main/docs/legacy/02_bonding.md) and [legacy staking](https://github.com/OlympusDAO/olympus-docs/blob/main/docs/legacy/01_staking.md).
- [Tomb overview](https://docs.tomb.com/), [platform mechanics](https://docs.tomb.com/protocol/platform), [DAO fund](https://docs.tomb.com/protocol/dao-fund), and [September postmortem](https://tombfinance.medium.com/tomb-finance-post-mortem-480fa68375b2).

## Validation notes

The JSON was parsed locally; required top-level keys, uniform nested keys, ID uniqueness, and claim/source/version/deployment references were checked by a purpose-built script. The report’s `[R4-C…]` references were also checked against dataset claim IDs, URLs were extracted, and word count was measured. These are structural checks only: they do not independently certify historical truth, contract behavior, completeness, or source permanence.
