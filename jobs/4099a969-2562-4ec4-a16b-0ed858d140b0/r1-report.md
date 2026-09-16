# Stablecoin v4 research — R1: rebasing and monetary controllers

**As of:** 2026-09-16T03:07:15Z  
**Historical eligibility window:** 2020-01-01 through 2021-12-31; major later outcomes traced where evidence was found  
**Research character:** bounded historical evidence report, not protocol design, endorsement, audit, or stability promise

## Executive finding

“Rebasing stablecoin” hides mechanisms with very different balance sheets and failure modes. AMPL changes every holder’s displayed units proportionally but supplies neither collateral nor a contractual target-price redemption. YAM initially combined that accounting with reserve seigniorage and governance, allowing one scaling bug to overmint, inflate voting supply, freeze governance and endanger a DEX pool. DIGG changed the target from purchasing power to BTC and layered vault/DAO incentives on top; Badger governance later acknowledged that rebasing had not maintained the target and moved toward free float. RAI is the deliberate control case: it is collateralized debt with unchanged wallet balances, a floating target, and a feedback controller that changes the accounting price of debt rather than token quantity [R1-C001–C002](https://github.com/fragmentsorg/ampleforth-contracts/blob/master/contracts/UFragments.sol), [R1-C006](https://medium.com/yam-finance/yam-post-rescue-attempt-update-c9c90c05953f), [R1-C016](https://forum.badger.finance/t/bip-92-digg-restructuring-v3-revised/5653), [R1-C018–C021](https://docs.reflexer.finance/faq).

The central historical constraint is therefore not “choose a better rebase.” A proportional rebase is an accounting transform: absent transfers, each holder owns the same percentage before and after. It cannot mechanically create aggregate real wealth, guarantee a buyer, or create a redeemable reserve. Feedback still depends on agents being willing and able to trade, borrow, repay, or provide liquidity after oracle observation and before the next control action. Delays, thin liquidity, leverage constraints and changing demand can produce overshoot or persistent error. Collateral and liquidation can make a claim solvent without fixing its exchange rate; conversely, a target-price controller can influence exchange behavior without making the token collateralized.

## Coverage and method

I searched Ethereum and BNB Smart Chain leads for all seven named seeds: AMPL, YAM, BASE, DEBASE, DIGG, Ditto and RAI. I added one explicit claimed relative, reBΔSE, and recorded RMPL and AmpleGold only in the unresolved discovery queue. Four deep cases were selected: AMPL as the canonical proportional rebase; YAM as the best versioned code/governance incident; DIGG as the best-evidenced contrasting target fork; and RAI as a non-rebasing, collateralized feedback controller. BASE and DEBASE are triaged. Ditto is unresolved because current searches are confounded by an unrelated later project and did not yield a dependable canonical 2020–2021 primary artifact.

Sources were prioritized in this order: deployed/verified code, project repositories, contemporaneous postmortems and migration notices, governance records, then current official documentation with explicit temporal caveats. A third-party mirror of the BASE paper was used only to support its stated target, not contract verification. Current branches and living docs were not silently treated as proof of historical parameters. Search routes and dead ends are in `searchLog`; claim/source records preserve publication, event and retrieval dates separately.

This is not a comprehensive rebase-token census. The stopping point was reached after all seeds were dispositioned and the four deep families could support causal comparison. Exact AMPL oracle evolution, YAM migration transactions, RAI’s full 2021 parameter chronology, Ditto identity, and long-tail forks remain queued. No sibling campaign report was requested or read, and I have no known exposure to one.

## Census and taxonomy

| ID | Protocol | Disposition | Monetary object | Target/backing | Depth |
|---|---|---|---|---|---|
| R1-P001 | AMPL | Included | proportional wallet-balance rebase | CPI-adjusted dollar purchasing-power target; unbacked/no par redemption | Deep |
| R1-P002 | YAM v1/v2/v3 | Included | rebase plus treasury seigniorage, then fixed-balance governance token | 1 USDC while active; treasury not redemption backing | Deep |
| R1-P003 | BASE | Included | proportional rebase | crypto-market-cap index; no evidenced basket redemption | Triaged |
| R1-P004 | DEBASE | Included | elastic supply plus stabilizer pools | DAI/USD-oriented target; no evidenced par redemption | Triaged |
| R1-P005 | DIGG | Included | proportional daily rebase | 1 BTC target; explicitly no BTC under management | Deep |
| R1-P006 | Ditto | Unresolved | unknown | unknown | Unresolved |
| R1-P007 | RAI | Adjacent | collateralized mint/repay plus floating-price controller; **not rebasing** | ETH collateral and floating redemption price | Deep |
| R1-P008 | reBΔSE | Unresolved relative | claimed AMPL fork | policy/oracle deployments not established | Unresolved |

These categories prevent four common category errors:

1. **Supply rebase versus redeemability.** Changing `balanceOf` pro rata is not a right to exchange one token for one dollar, BTC, or a collateral basket.
2. **Nominal balance versus wealth.** A 10% positive rebase makes everyone’s displayed balance about 10% larger; it does not guarantee market capitalization rises. A negative rebase reduces units but preserves network share, before trading and rounding.
3. **Fixed versus floating target.** YAM’s 1-USDC and DIGG’s 1-BTC reference are fixed to external units. AMPL’s target moves with CPI. RAI’s redemption price deliberately floats and may never return to its launch value [R1-C019](https://docs.reflexer.finance/faq).
4. **Controller policy versus collateral accounting.** RAI’s PID changes the redemption rate/price; SAFEs, liquidation, surplus and bad-debt machinery account for ETH backing. One must not be credited for the other’s job.

BASE illustrates why ancestry must be proved rather than guessed. Its source visibly uses AMPL-like hidden shares and proportional supply changes, but its index target and owner-maintained ban list materially differ [R1-C011](https://github.com/Base-Protocol/contracts/blob/master/contracts/BaseToken.sol). DEBASE has an Etherscan “Source Code Verified Exact Match” token at `0x9248…0907`; initialization names DEBASE/DAI and LP pool allocations and a `debasePolicy`, supporting inclusion but not a complete controller history [R1-C012](https://etherscan.io/token/0x9248c485b0b80f76da451f167a8db30f33c70907). reBΔSE’s repository explicitly calls itself an AMPL fork, but its README leaves policy and oracle addresses “TBD”; it remains unresolved rather than upgraded to a live monetary system by assertion [R1-C023](https://github.com/reBASEcapital/REBASE).

## Deep case 1 — AMPL: supply accounting is not a reserve

The retrieved AMPL token code holds balances in a fixed hidden denomination, “gons.” A rebase changes total fragments and the gons-per-fragment conversion rate; `balanceOf` divides fixed gon balances by the new rate. The result is proportional: a passive address’s displayed AMPL changes, but its share of supply does not [R1-C001](https://github.com/fragmentsorg/ampleforth-contracts/blob/master/contracts/UFragments.sol). This is the cleanest separation between nominal quantity and real wealth. If price falls at the same time as quantity expands, a larger token count can still be worth less. Conversely, contraction is not confiscation in relative-supply terms, though integrations, taxes, rounding, leverage and market timing can make outcomes non-neutral.

The repository lists token `0xD46b…A161`, supply policy, orchestrator, market oracle and CPI oracle as distinct contracts [R1-C003](https://github.com/fragmentsorg/ampleforth-contracts/blob/master/README.md). That modularity matters: token accounting executes an authorized delta; it does not decide the target or certify the price. The policy/oracle layer observes market and CPI data, applies threshold/lag logic, and asks the token to rebase. This report does not assert one immutable oracle window across 2020–2021 because current code and docs were not commit-diffed across the whole period.

AMPL provides no target-price redemption and holds no collateral pool in the rebase token contract. Convergence depends on market participants anticipating future supply and trading accordingly. That arbitrage is constrained: a trader cannot atomically buy below target and redeem at target; the trade is exposed to price movement, timing, gas, liquidity and the behavior of every other trader. A delayed controller may act on an average that no longer describes spot demand, while aggressive feedback can overshoot. The proportional design limits direct redistribution through the rebase itself, but it does not prevent transfer through trading against informed actors or through liquidity pools.

DEX integration is especially subtle. Pool token balances rebase even when reserves recorded by an AMM have not been synchronized, so execution and surplus handling depend on AMM design and maintenance calls. Contracts that cache a nominal amount may become wrong after rebase. WAMPL addresses one interface problem: a fixed wAMPL balance represents a fixed percentage of AMPL market capitalization and can be unwrapped into a variable amount of AMPL [R1-C004](https://github.com/fragmentsorg/ampleforth-contracts/blob/master/contracts/WAMPL.sol). It does not add collateral or eliminate AMPL price risk.

## Deep case 2 — YAM: three versions, one coupled code/governance failure

### Contemporary sequence

YAM launched farming on 2020-08-11 (some project prose says August 12) as a 1-USDC-target elastic token with a distinctive reserve feature: part of positive expansion would be minted and sold into a pool to acquire treasury assets [R1-C005](https://docs.yam.finance/yam). This meant expansion was not purely pro rata. Treasury capture diluted the otherwise constant holder share and imposed programmatic sale flow on the chosen pool.

On 2020-08-12, the team discovered that rebase arithmetic would mint far more reserve YAM than intended. Because YAM voting power used the same inflated token supply, the erroneous mint drove the governance quorum threshold beyond reach. A rescue proposal could not repair the system; treasury governance became inaccessible [R1-C006](https://medium.com/yam-finance/yam-post-rescue-attempt-update-c9c90c05953f). The project warned that residual YAM/yCRV Uniswap V2 liquidity would remain unsafe because a positive rebase would continue the bad mint-and-sale route [R1-C007](https://medium.com/yam-finance/yam-migration-faq-57c705688fe6).

This classification matters. The immediate failure was a **code arithmetic defect amplified by governance coupling**, not proof that rebase feedback first lost the peg. There is no need to posit an attacker; beneficiaries are not established. LPs who exited early avoided later exposure, while residual LPs and holders bore inventory risk, loss of functionality and migration burden. Calling it merely a “monetary failure” would hide the causal evidence.

YAMv2 was a deliberately non-rebasing ERC-20 placeholder. During a short window, v1 could be burned for v2 according to `balanceOfUnderlying`, a quantity designed not to vary with rebases. The plan was then to migrate v2 1:1 into an audited v3 [R1-C008](https://medium.com/yam-finance/yam-migration-faq-57c705688fe6). Migration was a recovery conversion, not redemption for a dollar or reserve asset.

V3 restored an elastic policy with a SushiSwap YAM/ETH TWAP. Official archived docs specify no rebase between 0.95 and 1.05 USDC, expansion above, contraction below, and an additional treasury mint equal to 5% of the rebase amount on positive cycles, sold for ETH through SushiSwap [R1-C009](https://docs.yam.finance/yam). Thus oracle observation, controller action and DEX execution were linked but separate: the TWAP estimated price; scaling altered holders; the extra mint transferred value toward treasury; the pool absorbed execution and slippage.

On 2020-12-29 governance disabled rebasing and fixed the scaling factor at 2.50. The project’s 2021 retrospective says rebasing created unanticipated friction unnecessary for a governance token [R1-C010](https://yamfinance.medium.com/yam-2020-recap-2021-roadmap-65cb5cad76d4). That is a role redesign, not an insolvency event. YAM persisted as governance for a treasury/ecosystem. The version history shows why token role must be dated: “YAM is a rebasing stablecoin” became false within the same year.

## Deep case 3 — DIGG: a BTC target plus demand subsidies

DIGG is the strongest evidenced contrast because it retained AMPL-like accounting but changed the external reference and surrounded it with BadgerDAO products. Official materials describe an uncollateralized elastic asset targeting 1 BTC, rebasing daily: expansion above 1.05 BTC, contraction below 0.95, and no change inside the band. They explicitly state there was no Bitcoin under management and that a rebase changed wallet units without changing percentage ownership [R1-C013](https://oldlandingpage.badger.com/products/digg). Source code independently shows fixed-gon accounting and an `onlyMonetaryPolicy` rebase path [R1-C015](https://github.com/Badger-Finance/digg-core/blob/master/contracts/UFragments.sol).

DIGG therefore offered neither WBTC redemption nor a collateral arbitrage. It depended on traders believing supply changes and future demand would pull price toward BTC. A BTC target also imports BTC volatility: even perfect ratio tracking would not be dollar stability. Daily discrete action plus a ±5% deadband reduces constant adjustment but permits error to accumulate; delayed observations and speculative positioning can then amplify a step response. Negative rebases cannot force marginal demand to appear.

Badger supplied auxiliary incentives. DIGG could be deposited into a Sett for bDIGG, an interest-bearing vault receipt whose DIGG exchange rate was explicitly not 1:1, or paired with WBTC in SushiSwap and deposited into an LP vault. Holding DIGG/bDIGG also affected Badger Boost rewards [R1-C014](https://oldlandingpage.badger.com/products/digg). These flows can deepen liquidity or subsidize demand, but rewards are not backing. They expose additional loss bearers: a DIGG/WBTC LP can bear relative-price divergence and rebase/integration effects; a vault depositor adds strategy and receipt-accounting risk; BADGER stakeholders fund emissions or confront dilution trade-offs.

Hindsight is unusually clear. An April 2022 BIP stated that original and modified rebasing had not maintained 1:1, described DIGG at roughly a 50% BTC discount, and proposed a free-floating rate, stopping all rebases, external LP support and DIGG emissions [R1-C016](https://forum.badger.finance/t/bip-92-digg-restructuring-v3-revised/5653). The price observation and causal language are a DAO claim, not an independently reproduced measurement, and the execution transaction was not checked. Still, the governance record is direct evidence that policy participants no longer considered the feedback regime successful. Unlike YAM v1, this is appropriately categorized as a **monetary/demand failure**, followed by redesign, rather than an arithmetic exploit.

## Deep case 4 — RAI: collateralized managed float, explicitly not rebasing

RAI belongs only as an adjacent controller case. Official documentation answers “Is RAI a rebase token?” with “No”: the quantity in a wallet does not change [R1-C018](https://docs.reflexer.finance/faq). Users lock ETH in SAFEs and generate RAI debt; repaying or liquidation contracts supply. This is balance-sheet issuance, unlike AMPL’s proportional rescaling.

RAI also rejects a fixed dollar peg. Its redemption price is the price the protocol seeks on secondary markets, used when generating debt and during Global Settlement. The redemption rate continuously devalues or revalues that redemption price. If market price remains below redemption price, a positive rate raises the future debt-accounting price: SAFE users face costlier repayment and reduced borrowing power, while holders gain a stronger settlement claim. If market price remains above target, a negative rate reverses those incentives. Official docs say the floating price may never return to its initial value [R1-C019–C020](https://docs.reflexer.finance/faq).

Three separations are essential. First, the ordinary borrow/stability fee is not the redemption rate. Second, ETH oracle and liquidation machinery protect collateral solvency; the RAI-market TWAP informs monetary error. Third, Global Settlement redemption is not an everyday promise to redeem one RAI for a fixed dollar [R1-C021](https://docs.reflexer.finance/faq). A system can be overcollateralized yet trade away from its controller target, especially if liquidation is healthy but market participants do not want additional debt or exposure.

Controller timing creates familiar feedback risks. The current production automation repository documents a 30-minute pinger schedule and a 720-minute minimum TWAP update interval [R1-C022](https://github.com/reflexer-labs/geb-pinger-bots), but these are not asserted as immutable 2021 settings. Any PID-like loop with oracle averaging, transaction cadence and slow borrower response has delay. High gains can overshoot or oscillate; integral accumulation can continue while users are constrained; weak gains tolerate prolonged deviation. Arbitrage is not atomic because no always-open fixed-price redemption exists. SAFE users must accept ETH collateral/liquidation risk, capital costs and a debt whose redemption price changes; holders must accept market and settlement uncertainty.

Loss allocation differs from rebases. With AMPL/DIGG, passive holders keep relative supply share but bear market-cap decline. With RAI, a positive redemption rate shifts expected value toward holders and raises debtor burden; a negative rate favors debtors and discourages holders. Liquidation shortfall and bad debt are collateral-accounting losses handled by auctions/backstop machinery, not by changing every RAI wallet balance. This makes RAI valuable evidence without mislabeling it.

## Dated outcomes and cross-case stress properties

- **2020-08-12/13 — YAMv1:** reserve overmint plus token-vote coupling made governance quorum unattainable; rescue failed, unsafe LP exposure was warned, and migration followed. Category: code/governance failure.
- **2020-08 to 2020-09 — YAMv2:** non-rebasing recovery placeholder with a deadline. Category: migration/operational risk, not stabilization.
- **2020-09 to 2020-12-29 — YAMv3 rebase:** audited relaunch, then governance disabled rebase because it hindered the token’s governance role. Category: deliberate redesign.
- **2021-01 onward — DIGG:** proportional BTC-target rebase plus vault/Boost incentives. By 2022 the DAO recorded severe persistent target deviation and proposed stopping policy support. Category: monetary/demand failure and shutdown of the feedback regime.
- **2021-02 onward — RAI:** collateralized floating target remained conceptually distinct from a fixed peg. No major incident claim is made here because this search did not reconstruct a verified insolvency, exploit or shutdown event.

Some properties did survive stress. AMPL/DIGG’s fixed-share accounting preserved relative ownership through the rebase itself. YAM’s `balanceOfUnderlying` gave migration a non-rebasing reference even after visible balances became unreliable. RAI’s separate collateral ledger means controller error does not directly rewrite wallets. None of these properties alone establishes price stability or economic safety.

## Historical constraints for later designers

These are evidence-derived constraints, not a proposed v4 design:

1. **State the enforceable claim.** A displayed target without redemption is a policy objective, not a floor. Treasury assets without a holder claim are not backing.
2. **Model wealth, shares and units separately.** Tests and interfaces must follow invariant ownership shares as well as nominal balances; integrations that cache balances can misaccount.
3. **Keep policy failure from disabling governance.** YAM shows a monetary arithmetic error can become unrecoverable when it also inflates voting supply/quorum.
4. **Treat oracle window plus action delay as one control loop.** An average reduces spot manipulation but adds lag. Rebase timing is public and invites positioning; feedback gain, deadband, cadence and market response determine oscillation together.
5. **Do not assume arbitrage is atomic.** Without redeemability, arbitrageurs warehouse price, timing and liquidity risk. With collateralized debt, they additionally face capital, liquidation and changing-debt risk.
6. **Specify DEX loss allocation.** Rebases touch pool balances; treasury sales consume depth; LPs bear relative-price and stale-accounting risks. Wrappers improve composability but add conversion and custody surfaces.
7. **Separate subsidy from stabilization.** Farming, Boost and stabilizer pools can rent liquidity or demand. When rewards end, the price response may disappear; this is not equivalent to collateral.
8. **Version every claim.** YAMv1, v2 and v3 had different balance behavior and recovery rights. Current documentation cannot establish old settings without commits or transactions.
9. **Name the loss bearer under contraction and bad debt.** A proportional contraction changes everyone’s units; collateral liquidation charges a leveraged borrower; bad debt may reach backstop stakeholders. These are not economically interchangeable.
10. **Provide a safe cessation path.** Both YAM and DIGG eventually stopped rebasing. The historical evidence supports treating controller shutdown, wrappers, migrations and residual pools as first-class operational states.

Counterfactual mitigations—such as isolating voting weight from rebase supply, adding redemption, shortening or lengthening oracle windows, or retuning feedback—are only inferences unless tested against historical states. This report does not claim any one would have prevented the observed outcomes.

## Disputes, gaps and unresolved queue

The YAM launch date is inconsistently narrated as August 11 versus August 12; the dataset records August 11 for farming launch and treats the following rebase phase separately. “Exploit” is also used loosely in public discussion: the retrieved postmortem establishes a bug, but not a malicious attacker, so the incident summary explicitly says none was required.

Current AMPL code establishes accounting and current addresses but not every 2020–2021 oracle source/window. DIGG’s 2022 “~50% discount” is retained as a project governance claim rather than a reproduced market measurement. RAI’s current pinger configuration cannot silently establish all 2021 cadence and gains. BASE lacks a reconstructed production oracle/deployment. DEBASE lacks controller history. Ditto remains unresolved. The next evidence should be explorer creation transactions and events, archived governance parameter changes, commit-pinned deployments, and canonical archived Ditto pages. RMPL, AmpleGold and other possible forks remain leads, not researched inclusions.

## Source register

The machine-readable register contains 20 sources with limitations. Principal sources are:

- **AMPL:** [official contract addresses](https://github.com/fragmentsorg/ampleforth-contracts/blob/master/README.md), [UFragments token code](https://github.com/fragmentsorg/ampleforth-contracts/blob/master/contracts/UFragments.sol), [protocol explanation](https://docs.ampleforth.org/learn/about-the-ampleforth-protocol), [WAMPL wrapper code](https://github.com/fragmentsorg/ampleforth-contracts/blob/master/contracts/WAMPL.sol).
- **YAM:** [official archived mechanics](https://docs.yam.finance/yam), [migration FAQ](https://medium.com/yam-finance/yam-migration-faq-57c705688fe6), [post-rescue postmortem](https://medium.com/yam-finance/yam-post-rescue-attempt-update-c9c90c05953f), [token code](https://github.com/yam-finance/yam-protocol/blob/master/contracts/token/YAM.sol), [2020 retrospective](https://yamfinance.medium.com/yam-2020-recap-2021-roadmap-65cb5cad76d4).
- **BASE/DEBASE:** [BASE token code](https://github.com/Base-Protocol/contracts/blob/master/contracts/BaseToken.sol), [mirrored BASE paper](https://www.allcryptowhitepapers.com/wp-content/uploads/2020/12/Base-protocol.pdf), [DEBASE verified explorer source](https://etherscan.io/token/0x9248c485b0b80f76da451f167a8db30f33c70907).
- **DIGG:** [official archived product page](https://oldlandingpage.badger.com/products/digg), [token code](https://github.com/Badger-Finance/digg-core/blob/master/contracts/UFragments.sol), [launch parameters](https://forum.badger.finance/t/digg-launch-parameters/209), [BIP-92 restructuring](https://forum.badger.finance/t/bip-92-digg-restructuring-v3-revised/5653).
- **RAI:** [official FAQ](https://docs.reflexer.finance/faq), [controller modeling repository](https://github.com/BlockScience/reflexer), [production automation repository](https://github.com/reflexer-labs/geb-pinger-bots).
- **Relative:** [reBΔSE repository](https://github.com/reBASEcapital/REBASE).

## Validation notes

`r1-data.json` was parsed as a single UTF-8 JSON object. Local validation checked required top-level keys, all required protocol/version/incident/source/claim/search/exclusion/uncertainty fields, unique IDs, and resolution of claim/source/version/protocol references. The report was checked for the required sections and word-range target. These checks establish artifact structure and internal linkage only; they do not independently certify historical truth, source authenticity, contract behavior, market measurements or completeness.
