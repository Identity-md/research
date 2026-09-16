# Stablecoin v4 research R2 — debt, coupon and seigniorage lineages

**As of:** 2026-09-16T03:23:08Z  
**Historical window:** 2020-01-01 through 2021-12-31; later outcomes followed where evidence was found.  
**Bottom line:** ESD coupons and Basis-family bonds were not debt in the ordinary enforceable sense. A holder had a contract-defined, condition-dependent route to newly minted endogenous tokens, normally only after the market price recovered. There was no external debtor, maturity payment, collateral foreclosure, or bankruptcy estate. Burning circulating cash could reduce the immediately transferable cash supply, but replaced it with a contingent claim and could not create the demand or reserve asset needed to make that claim valuable. In the zero-new-demand state, the redemption gate never opens or the treasury remains unfunded; coupon/bond holders lose, while early expansion recipients and sellers have already extracted the liquid side of the trade [R2-C003, R2-C008, R2-C013, R2-C020].

## Coverage and method

I searched Ethereum, BNB Smart Chain and Fantom lineages using official GitHub repositories and commit history, verified explorer source, contemporary project documentation/blogs, the original Basis paper, and contemporary postmortem/analysis. I inspected contract paths controlling issuance, coupon purchase/expiry, bond caps/redemption, oracle capture, epoch advancement, boardroom allocation, and governance. Claims are tied to stable claim IDs below and in the JSON. Project-authored promises are labeled `project_claim`; causal conclusions are `inference` unless directly demonstrated. Current token pages establish present contract/code status, not historical success.

The deep cases are ESD, DSD, Basis Cash, and Basis Gold. Basis Dollar, Mith Cash, bDollar and Tomb remain census records because their lineage/deployment was evidenced but full bytecode-to-repository and lifecycle reconstruction did not fit the bounded search. The original Basis proposal is ancestry, not a live protocol. This is deliberately not a completeness claim: the stopping point was an evidence-rich reconstruction of four families plus the named forks; the unresolved queue includes Mith Cash’s later MIC2/MIS3 migration, bDollar governance history, Tomb’s version transitions, and other short-lived cross-chain clones.

No sibling campaign reports were requested or read. Known exposure is the assignment text and the public sources in the register.

## Census and taxonomy

| ID | System | Window status | Target / mechanism | Evidence posture |
|---|---|---|---|---|
| R2-P001 | Empty Set Dollar (ESD) | launched 2020; regulation paused 2021; v1 migration enabled | USD; single-token DAO plus expiring coupons | deep, repository and verified token |
| R2-P002 | Dynamic Set Dollar (DSD) | launched 2020; severe Dec. 2020 depeg; token still transferable | USD; ESD fork with 2-hour epochs and 30-day coupons | deep, verified token and contemporary docs; repo provenance missing |
| R2-P003 | Basis Cash (BAC/BAB/BAS) | launched Nov. 2020; v2 activated Apr. 2021; terminal date unknown | USD; three-token seigniorage shares | deep, code/deployments/blog |
| R2-P004 | Basis Gold (BSG/BSGB/BSGS) | launched Jan. 2021 | floating gold/XAU target; Basis Cash fork plus XAU oracle | deep, code and launch record |
| R2-P005 | Original Basis/Basecoin | cancelled in 2018, never launched | CPI/USD proposal with bond queue and shares | ancestry only |
| R2-P006 | Basis Dollar | deployed 2020 | USD; explicit GitHub fork of Basis Cash | triaged verified lineage |
| R2-P007 | Mith Cash / Mithril Cash | deployed Jan. 2021 | USD; MIC/MIB/MIS Basis-family fork | triaged, verified token and official address list |
| R2-P008 | bDollar | 2020–2021 candidate on BSC | USD; Basis Cash-style boardroom | triaged; eligibility retained, exact fork proof incomplete |
| R2-P009 | Tomb Finance | active 2021 on Fantom | FTM-denominated target, bonds and shares | adjacent/triaged; materially non-dollar and later redesigns not reconstructed |

Excluded from the live count are Ampleforth/Yam (wallet-wide rebasing rather than voluntary debt claims), Fei (PCV/direct incentives), Frax (fractional collateral and algorithmic share rather than coupon seniority), and TerraUSD (two-token burn/mint convertibility rather than expiring coupon or boardroom debt). They are useful adjacent comparisons, not members of this assignment’s narrow mechanism lineage.

## Deep case 1 — Empty Set Dollar

### Mechanics by version

ESD’s deployed Ethereum addresses are recorded in its repository: token `0x36F3…d723`, DAO `0x443D…13D3`, USDC/ESD Uniswap V2 pair, oracle, and incentivization pool. Etherscan labels the token source an exact verified match [R2-C001]. In the late-2020/January-2021 implementation, an externally called `advance()` minted an advance incentive, stepped bonding, captured the oracle, stepped the coupon market, and paid a stability reward. Epochs shifted from daily to eight-hour periods; a bootstrapping override returned $1.10 for 90 epochs, accelerated by a factor of three [R2-C002].

When captured TWAP was below $1, the regulator did **not** seize balances. It increased an internal debt allowance by a price-gap formula, capped each epoch’s change and capped aggregate debt ratio. A user voluntarily called `purchaseCoupons(amount)`: the DAO burned that ESD, recorded coupon principal and premium for the purchase epoch, and thereby removed transferable ESD. When price exceeded $1, `growSupply` reset debt and minted a bounded expansion. The controller allocated supply first to redeemability and then to bonded stakeholders; coupons required at least two epochs before redemption. Coupons expired after 90 epochs. Later code prorated premium by time spent in contraction, while expired coupons could recover only recorded underlying in specified circumstances [R2-C003, R2-C004].

The oracle was endogenous: a Uniswap V2 USDC/ESD TWAP with minimum reserve checks. Governance and reward weight came from bonded ESD/LP positions with exit lockups. This means the system’s measurement, exit liquidity, and stabilization demand all depended on the same ESD market. Bootstrap issuance and `advance()` rewards were explicit inflationary incentives, not backing [R2-C002].

### Stress and outcome

Contemporary prices fell durably below peg after late December 2020; later analysis reports both ESD and DSD near $0.23–$0.24 after their large peak supplies. This is secondary evidence and should not be read as a precise on-chain measurement [R2-C005]. Repository history supplies harder lifecycle evidence: proposal code paused regulation on 2021-04-04; later changes removed bonding and enabled migration to a v2 DAO by 2021-08-08 [R2-C006].

In a zero-new-demand state, coupon purchase can burn cash only if someone voluntarily gives up liquid ESD for a still-more-junior contingent claim. The coupon has no claim on USDC in the AMM and no party obligated to buy ESD. Redemption is funded solely by protocol minting after a qualifying expansion. Thus contraction does remove current ERC-20 units, but does not retire economic claims: it creates coupons, and premiums increase the quantity potentially minted later. If recovery never occurs before expiry, coupon buyers absorb the loss; if it occurs, later holders suffer dilution while bonded users and advance callers may also receive issuance. This is an inference from the code’s cash flows, not a claim that every holder behaved identically [R2-C003, R2-C007].

## Deep case 2 — Dynamic Set Dollar

DSD publicly described itself as an ESD-derived, non-collateralized USD token. Etherscan currently marks the DSD token at `0xBD2F…66e3` “Source Code Verified Exact Match” [R2-C009]. Its contemporary FAQ says epochs were two hours (12/day), coupons expired after 360 epochs/30 days, TWAP covered one epoch, and expansion flowed first to coupon redemption, then 60% to bonded DAO holders and 40% to LP/oracle participants. A successful caller manually advanced epochs for a minted incentive [R2-C010]. The project’s comparison page claimed a maximum 10% supply move and a price-gap formula divided across the higher epoch frequency; that is a project claim because the canonical historical repository was not recovered [R2-C011].

The debt semantics mirror ESD: under peg, the protocol *creates debt capacity*; users then voluntarily burn DSD for discounted coupons. Above peg, endogenous DSD is minted to coupons before stakeholder rewards. A coupon is enforceable only as contract state conditional on eligibility, non-expiry and future mint allocation. It is not redeemable for USDC. The faster oracle/epoch cadence shortened reaction time but also shortened expiry to 30 days and did not add an external asset or obligated buyer.

On 2020-12-28 DSD reportedly traded as low as $0.27 before a partial rebound; the project strategist’s January 2021 essay acknowledged MIC, BAC, ESD and DSD under-peg and argued that bond burning often does not itself cause spot buying [R2-C012, R2-C013]. That distinction is crucial: burning inventory held off-market reduces nominal float, but if the burner already owned DSD it need not cross the AMM or improve the marginal price. When expected future DSD is worth less than the forgone DSD, coupon demand disappears. Outstanding coupon holders and residual DSD holders bear the failure; there is no senior reserve claimant.

Uncertainty is higher here than for ESD. Verified token code establishes identity and transfer/mint roles, while mechanics come from the project FAQ/site rather than a recovered canonical commit. Exact DAO addresses, proposal sequence, and shutdown date remain unresolved [R2-U001].

## Deep case 3 — Basis Cash

### v1 monetary core

Basis Cash explicitly called itself a simplified implementation of the unlaunched Basis design. It separated BAC cash, BAB bonds and BAS shares. The repository deployment manifest records BAC `0x3449…A69a`, BAB `0xC368…Abc5`, BAS `0xa7ED…3696`, two oracles, treasury and boardroom [R2-C014].

Below $1, `buyBonds` read the bond oracle, imposed a price/slippage guard and bond cap, burned `amount` BAC, and minted `amount / price` BAB. BAB therefore bought at a larger discount as BAC fell. It had no expiry in this implementation. Above the curve-defined ceiling (described as $1.05 in code comments/README), `redeemBonds` burned BAB and transferred 1 BAC per BAB—but only if the treasury already held enough BAC. This is a hard redemption **gate plus budget constraint**, not unconditional convertibility [R2-C015].

On expansion, the seigniorage oracle was updated, supply growth equaled circulating supply times the excess over $1, and BAC was minted to the treasury. The code allocated 2% to a community fund, reserved enough for outstanding BAB less already accumulated seigniorage (but only 80% of an epoch if the whole expansion would be consumed), and sent the remainder through a seigniorage proxy to boardroom/reward recipients. Fixed-window Uniswap V2 cumulative-price oracles required explicit periodic updates; bond purchase/redeem used an update modifier and one-block guard [R2-C016].

Bootstrap distribution was separate: the November 2020 launch promised 50,000 BAC over five days to deposits of existing stablecoins, followed by BAS liquidity mining. Deposited assets incentivized participation; they did not become a redemption reserve for BAC [R2-C017]. Admin power was material: token operators, treasury ownership, fund allocation and migration routes were controlled through owner/timelock paths in code.

### v2 and outcome

After BAC lost its target, the January 2021 BIP-X roadmap proposed Curve/stableswap liquidity, a new BAS, an arbitrage vault and BAC borrowing demand. The April 2021 v2 activation added migration, vault/farm and bondroom components; these were demand/liquidity programs, not retroactive collateralization of BAB [R2-C018]. A definitive shutdown transaction or final mint date was not found, so the record says “failed to sustain peg; terminal date unknown,” not “contract ended.”

In a debt rollover state, every redeemed BAB is funded by newly minted BAC from demand-driven expansion or pre-funded treasury balance. Reserving seigniorage gives BAB temporal priority over boardroom distributions, but not priority over any external asset. If the market stays below the gate, redemption stops. New BAB purchases can burn BAC, but increase the eventual endogenous BAC obligation by the discount. BAB holders lose if no expansion arrives; BAC holders bear dilution if it does; BAS/boardroom recipients lose future seigniorage when BAB absorbs expansions. This is debt seniority within an issuance waterfall, not solvency seniority [R2-C019, R2-C020].

## Deep case 4 — Basis Gold, a materially different fork

Basis Gold reused the three-token architecture but targeted one unit of gold rather than one dollar. Its January 9, 2021 announcement names BSG cash, BSGB bonds, BSGS shares and BUILD governance; records distribution beginning January 14 and stabilization January 21; and publishes all token addresses [R2-C021]. The GitHub repository states its derivation from Basis Cash through near-identical Treasury/Boardroom structure, but the price path combines a BSG market TWAP with Chainlink XAU/USD. That makes it a non-dollar monetary experiment, not a USD stablecoin.

The deployed logic burned BSG below the gold target and minted `amount / priceRatio` BSGB. Above target, BSGB redeemed 1:1 subject to treasury budget. Expansion minted BSG; 2% initially went to the BUILD-controlled fund, enough was reserved against bonds, and the remainder went to BSGS boardroom stakers. The launch distributed only 50 BSG during a seven-day bootstrap and one million BSGS over a year. Its tiny initial float was intended to seed oracle liquidity, but also made the market/reference ratio sensitive to shallow AMM conditions [R2-C022].

This fork exposes a second oracle dependency absent from dollar-only clones: even a correct BSG/DAI TWAP is insufficient without a live, correctly scaled XAU/USD reference. Yet its balance sheet remained endogenous. There was no vaulted gold and no right to receive gold, dollars, or BUILD treasury assets. Thus “synthetic gold” described the target unit, not backing. Zero new BSG demand produces the same blocked redemption loop, with additional basis risk between market liquidity and the off-chain gold feed. A definitive shutdown and full explorer verification of treasury/boardroom were not established; only token addresses and repository/launch evidence are claimed [R2-U003].

## Genealogy, disputes, and rename risk

The original Basis paper (formerly Basecoin, v0.99.7) proposed basecoins, bonds and shares, a FIFO bond queue, and automatic expiry/default of old bonds. The company cancelled before launch in 2018. It therefore belongs in ancestry, not the 2020 live count [R2-C023]. Basis Cash’s own README says it simplified bond issuance and seigniorage; GitHub marks Basis Dollar as forked from Basis Cash. Basis Gold names Basis Cash as its direct work base. Mith Cash’s verified token and official address list reproduce cash/bond/share/boardroom/treasury roles, but no surviving canonical GitHub core repository was found, so “fork” is a strong structural inference rather than a verified GitHub fork relationship [R2-C024].

Names are collision-prone: later unrelated projects use “Base Dollar” and “Basis Gold,” and Heco also hosted a Basis Gold-branded project. This report binds the deep fork to BUILD Finance’s Ethereum addresses and `build-finance/basis-gold-protocol`, and binds “Basis Dollar” to `basisdollar/basisdollar-protocol`. The JSON keeps aliases and chains explicit.

## Historical failure conditions and constraints (not a protocol design)

1. **A burn is not a bid.** Voluntary coupon/bond conversion reduces transferable units but may involve no spot purchase. Price impact requires demand at the market, not only accounting contraction [R2-C013].
2. **Conditional endogenous redemption is not backing.** Coupon/BAB/BSGB claims are paid by later minting after oracle gates. No claimant can seize USDC, gold or protocol-independent collateral [R2-C007, R2-C020].
3. **Discounts worsen rollover arithmetic.** Lower spot prices mint more face-value claims per burned cash. If recovery occurs, future dilution grows; if not, the discount merely compensates for a claim likely to expire or remain gated.
4. **Seniority reallocates seigniorage, not solvency.** Paying bonds before boardroom shares protects bondholders only when expansion exists. In a permanent contraction there is no waterfall asset.
5. **Expiry clears liabilities by creditor loss.** ESD/DSD expiry limits overhang, but it does so by deleting claim value; it does not demonstrate successful contraction or repay anyone.
6. **Oracle timing is economic policy.** Manual epoch advancement, stale fixed-window observations, minimum liquidity and two-oracle composition determine when issuance and redemption become callable. Faster epochs did not solve DSD’s demand failure.
7. **Bootstrap yield can simulate demand.** Farming emissions attract deposits and liquidity but are liabilities/incentives, not durable use. The state after rewards end must be evaluated separately.
8. **External target complexity does not create reserves.** Basis Gold’s XAU reference changed the numeraire and oracle risks while leaving claim funding endogenous.

These are historical constraints. Any claim that a parameter change alone would have prevented failure is counterfactual and untested.

## Disputes, gaps, and stopping point

Material gaps are explicit in `uncertainties`: DSD’s canonical DAO commit/deployments; exact ESD v1-to-v2 user outcomes; Basis Cash’s terminal on-chain action; Basis Gold’s treasury verification and terminal date; Mith Cash’s MIC2/MIS3 transition; and the eligibility/version histories of bDollar and Tomb. Price histories are especially fragile: contemporary articles and current explorer displays are supporting lifecycle evidence, not authoritative OHLC datasets. “Verified” is asserted only for token/explorer entries or repository fork metadata that explicitly supports it; repository-published addresses alone use `verified: null`.

The search stopped after the named families and four deep cases were adequately evidenced, leaving an unresolved discovery queue rather than making a universal census claim.

## Source register

Full metadata is in `r2-data.json`. Principal sources:

- R2-S001 — [ESD repository and deployment README](https://github.com/emptysetsquad/dollar)
- R2-S002 — [ESD January 2021 constants at commit cec1c22](https://github.com/emptysetsquad/dollar/blob/cec1c22/protocol/contracts/Constants.sol)
- R2-S003 — [ESD coupon market at commit cec1c22](https://github.com/emptysetsquad/dollar/blob/cec1c22/protocol/contracts/dao/Market.sol)
- R2-S004 — [ESD regulator at commit cec1c22](https://github.com/emptysetsquad/dollar/blob/cec1c22/protocol/contracts/dao/Regulator.sol)
- R2-S005 — [ESD proposal/commit history](https://github.com/emptysetsquad/dollar/commits/master/)
- R2-S006 — [DSD verified token](https://etherscan.io/token/0xBD2F0Cd039E0BFcf88901C98c0bFAc5ab27566e3)
- R2-S007 — [DSD contemporary FAQ](https://dynamicsetdollar.medium.com/dynamic-set-dollar-faq-b8a36c4fcab)
- R2-S008 — [DSD project mechanism page](https://dsd.finance/)
- R2-S009 — [Basis Cash repository/README](https://github.com/Basis-Cash/basiscash-protocol)
- R2-S010 — [Basis Cash Treasury](https://github.com/Basis-Cash/basiscash-protocol/blob/78ce115f03850a6d21d68056fc115088b4cce981/contracts/treasury/Treasury.sol)
- R2-S011 — [Basis Cash oracle](https://github.com/Basis-Cash/basiscash-protocol/blob/78ce115f03850a6d21d68056fc115088b4cce981/contracts/oracle/Oracle.sol)
- R2-S012 — [Basis Cash deployment manifest](https://github.com/Basis-Cash/basiscash-protocol/blob/78ce115f03850a6d21d68056fc115088b4cce981/deployments/7.json)
- R2-S013 — [Basis Cash BIP-X roadmap](https://medium.com/basis-cash/bip-x-a275b2e9b51f)
- R2-S014 — [Basis Gold launch](https://medium.com/basis-gold/introducing-basis-gold-7ae25750903e)
- R2-S015 — [Basis Gold protocol repository](https://github.com/build-finance/basis-gold-protocol)
- R2-S016 — [Original Basis whitepaper v0.99.7](https://www.basis.io/basis_whitepaper_en.pdf)
- R2-S017 — [Basis Dollar GitHub fork](https://github.com/basisdollar/basisdollar-protocol)
- R2-S018 — [Mith Cash official addresses](https://mithcash.medium.com/official-contract-addresses-and-details-bbe4311adc28)
- R2-S019 — [Mith Cash verified MIC token](https://etherscan.io/token/0x368b3a58b5f49392e5c9e4c998cb0bb966752e51)
- R2-S020 — [Contemporary critique by Mith Cash strategist](https://algostable.medium.com/why-algo-stable-bonds-dont-work-cb218eb2e59e)
- R2-S021 — [Secondary ESD/DSD failure synthesis](https://www.quadrigainitiative.com/casestudy/emptysetdollarstablecoincollapse.php)

## Validation notes

The JSON was parsed with `jq`; a local validator checked all required top-level and nested keys, uniform narrative fields, ID uniqueness, and resolution of every claim/source/version/lineage reference. The report’s material claim IDs occur in the dataset and URLs were compared with the source register. These checks establish structural integrity only, not independent truth, archival completeness, bytecode equivalence, or economic causation.
