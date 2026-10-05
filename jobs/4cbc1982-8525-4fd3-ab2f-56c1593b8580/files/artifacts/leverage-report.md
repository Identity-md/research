# CLAUS: interest-free spot-backed leverage assessment

**Recommendation: no-go for live lending now; retain spot-only trading.** Separate ETH and CLAUS lending could support real main-pool longs and shorts without a second pool or new coin, but no executable depth, independent proxy-state read, exact fee-aware quote or adversarial fork result was obtained. A finite term removes indefinite occupation; it does not remove gap losses or make providers profitable. Recommended live capacity is **zero**. No production design is selected and no funds are allocated.

The useful research candidate is one isolated position at no more than **1.5x**, a **24-hour maximum lifetime**, no automatic renewal, an upfront charge tested at 0/0.5/1/1.5% of gross position notional, and independently funded lending, loss and gas reserves. These are next-test parameters, not safe production parameters. At unchanged price, the illustrative 1% impact per leg plus 2.3% pool fees already creates approximately 6.4% friction on long notional before gas or opening charges. A small mainnet position has a substantial additional gas burden. A 2x short requires twice collateral value in actual borrowed CLAUS; a 2x long requires once collateral value in borrowed ETH.

## Evidence, refreshed baseline and continuity

Inputs were read: project history, both protected Solidity suites, DeFi background and license. This is research, so launch-contract tests do not apply and were not run. The checkout contained the supplied reads but no prior working artifacts. Earlier published evidence was retrieved and retained by reference, hashes and baseline source records in the JSON. Prior job `032c95fc-86f0-4c53-a28a-939b61faa7bd`, commit `21676ace3b947b3a73a02430e3d3adad3ff99377`, artifact set `48e7e019aa3aa121fae7e0682c47f9fec81078193965e3688f41c4563130fabe` remains the predecessor. [Published provenance and artifact links](https://github.com/Identity-md/research/blob/21676ace3b947b3a73a02430e3d3adad3ff99377/jobs/032c95fc-86f0-4c53-a28a-939b61faa7bd/_identitymd/README.md).

Earlier idea IDs remain research: `claus-market-loom-v1`, `claus-commons-crossing-v1`, `claus-liquidity-creature-v1`, `claus-trade-archaeology-v1`, `claus-counterfactual-reserve-v1`, `claus-gap-commons-v1`, `claus-market-metronome-v1`. Counterfactual Reserve is useful for replay evidence and Gap Commons for gap-risk framing; neither selects leverage or authorizes a subsidy.

Evidence levels: **A** independently read chain/code; **B** primary published API/docs or deployment manifest; **C** supplied baseline/announcement; **D** analytical assumptions/inferences. No A-level mainnet pool result was obtained here. HTTP reads succeeded through Python after the browser tool failed. Exact retrieval times and SHA-256 hashes are in JSON.

| Observation | Evidence and pin | Meaning/limit |
|---|---|---|
| Official claus/CLAUS, Ethereum chain 1 | [about.json](https://claus.si/about.json), updated 2026-10-05 19:16:05.362 UTC; B | Token remains `0x1b54E762aa34CF6E28E9C082F2848e28E45DA6b8` |
| Main proxy | `0x37Bfb8AC7C960E558657871D41Ca70E07e7DbfFf`; B/C | Upgradeable execution is a material dependency |
| Fee API implementation | [fee-state.json](https://claus.si/fee-state.json), observed 19:16:30.961 UTC; block **26128200**, hash `0x591fe5460028dc4f66cc95459d7c83a24dc35a2b6046916780c5856e71c83300`, block time 19:16:23 UTC; B | Reports `0x03a87b410cfb7c4a74737319161c7f6d6613dc92`, superseding supplied 18:46 observation |
| Total swap charge | Fee API: 23000 ppm of gross ETH, project 20000 + platform 3000; B | Dry weather: burn 1500, LP 3500, wallet 13500, Fomo 1500 ppm; weather reallocates, does not reduce total |
| LP accumulation | [hook-stats.json](https://claus.si/hook-stats.json), observed 19:16:31.087 UTC; block **26128198**, hash `0xdd353b7fb4580b7dbd2398539472363a6a68de3609b86f4a4df22ada8756d5f9`, block time 19:15:59 UTC; B | 27 cumulative deposits, 2.446903698943701538 ETH added; explicitly **not current pool balance or lending inventory** |
| Upgrade announcement | [Hooks](https://claus.si/Hooks) and [journal](https://claus.si/journal/journal%3Ahook-efficiency-20261005.json); B/C | Reports combined buybacks, separate LP batches and optional-failure isolation; reported gas improvements are not a benchmark for leverage |
| Proxy state/code verification | EIP-1967 storage at block 26128200 attempted on publicnode and llamarpс; HTTP 403 | Actual implementation remains independently unverified. Etherscan original, candidate and companion code: HTTP 403; Sourcify candidate metadata 404 |

Pool ID is `0xfaa42866f7667e3a1a10d783f3b629171febd45f056336b8df766d74afc0f0f7`. Supplied PoolKey: native ETH zero address / official CLAUS, fee `8388608` dynamic flag, tickSpacing `1`, main proxy; manager `0x000000000004444c5dc75cB358380D2e3dE08A90`; LP fee zero. These exact key/LP-fee facts are C until directly read. Original implementation [0xFBF8…97d](https://etherscan.io/address/0xFBF8A66314e1B67c9131ab320584Fe31EB34D97d#code), candidate [0x03a8…C92](https://etherscan.io/address/0x03a87b410CFB7C4a74737319161C7f6D6613dC92#code), companion [0x83dd…832](https://etherscan.io/address/0x83ddbAf00118d8920B98B31CbaCD4E178921C832#code) are source references, not code verified by this run. Neither old nor new implementation is assumed executable in our model.

### Helix, critically

[Helix docs, listing and fees](https://helixlev.fun/docs.html#listing) are B, not compatibility proof. Listing creates a separate pool/pot, costs 0.01 ETH, and pays the funder fees and running interest. Docs quote 1% opening at 1.5x, 1.5% at 2x; listed interest caps at 40% APR. Slow floor/ceiling prices, position/book caps and liquidations constrain lending. Ethereum keeper deposit is 0.003 ETH. Listed-funder withdrawals keep utilization at most 80%; the generic table says 90%, so these contexts must not be conflated. A listed pause blocks trades, closes and liquidation; an exit/restart or reported 48-hour escape restores access. This is unsuitable for CLAUS repayment liveness.

[Published Ethereum deployment manifest](https://helixlev.fun/deployments/1.json) names long `0x39C574bCAde4243E1e16Cf05b178DD265D893b9D`, short `0xFa1610E4BecDD59c60a828F731A614b740F00A7E`, vault `0xD8cD3fd94410f0Aa875C00F9e33c2558803D9ed7`. [ABI](https://helixlev.fun/abi.js) and [config](https://helixlev.fun/config.js) were read; ABI signatures do not prove behavior. Etherscan long/short code was blocked and Sourcify long metadata absent. Important claims remain source-unverified. [Announcement](https://x.com/Helixlevdotfun/status/2107174659011608599) was reachable but yielded no authenticated contract evidence; community proposals establish no compatibility. No listing or dependency is selected.

## Smallest coherent architecture and actual v4 role

This is a **separate vault/position periphery**, not a new hook. A website or escrow is not a v4 hook. Keep the main proxy, ordinary public-router spot trading, fee recipients and existing LP principal/claims intact. No router allowlist or main-pool permission change is proposed. No token issuance, share coin or synthetic CLAUS. Provider claims could initially be internal, nontransferable asset-denominated accounting entries with a withdrawal queue.

Two independently funded vault sleeves lend ETH to longs and CLAUS to shorts. Each has cash, loans receivable and explicit loss accounting in its loan asset. A position ledger locks balances and identifies ownership; a narrowly scoped adapter/router calls the fixed main PoolKey. A keeper computes executable liquidation health and executes closes. An observation contract would require authenticated pool state, bounded freshness and manipulation-resistant observations; no deployed CLAUS oracle with those properties was verified. IMD can help research/replay and monitoring; neither an LLM per swap nor an asynchronous web response is a fast liquidation oracle.

| Event | Actual assets and debt movement |
|---|---|
| Open long | Trader deposits net ETH collateral C plus separately disclosed charges; ETH sleeve lends D=(L−1)C; main-pool buy spends gross N=LC, pays existing fees; real CLAUS Q stays locked; ETH debt remains D |
| Open short | Trader deposits C ETH; CLAUS sleeve lends Q=N/p0 with N=LC; main-pool sale pays existing fees; all ETH sale proceeds S and C stay locked; debt is Q CLAUS |
| Partial close α | Long sells αQ and repays αD ETH; short buys αQ CLAUS and returns it. Record actual fills and costs. Release only surplus consistent with remaining debt and stressed full-exit health, never automatically α collateral if it leaves insolvency. No fee refund on swaps already executed |
| Full healthy close | Long sells remaining CLAUS, repays ETH debt, returns surplus; short spends locked ETH on actual CLAUS buyback, repays token debt, returns surplus. Trader-paid gas, refundable unused keeper deposit and reserve reconciled separately |
| Expiry | Permissionless close through same pool, same repayment waterfall, no penalty purely for expiry; unused keeper reserve refunded after execution. Admission stops before synchronized maturities overload depth/gas. Debt never disappears at expiry |
| Liquidation | Keeper executes same actual swap using bounded quote and receives disclosed gas/reward. No discretionary seize-at-mark substitute. Default reward $2 plus illustrative gas is reserved up front, not promised from insolvent equity |
| Insolvency | All locked position assets used first; optionally trader adds funds. Residual bad ETH/token debt hits dedicated reserve in that asset, then sleeve providers pro rata. No recourse to LP principal, existing fees/claims or other sleeve. Partial token repayment measures missing CLAUS units, not just marked dollars |
| Unexecutable close | Fail atomically rather than pretend debt repaid; permissionless retries and direct debt top-up/repayment remain available. Do not pause healthy closes or repayments when new opens stop. Liquidity failure can still strand exposure |

Core unlock/settlement mechanics follow [Uniswap flash accounting](https://developers.uniswap.org/docs/protocols/v4/concepts/flash-accounting): adapter initiates unlock, authenticates callback, swaps, settles native ETH with value and ERC-20 via sync/transfer/settle, and takes received assets. All manager deltas must resolve before return. This does not establish actual CLAUS compatibility; fork verification is required.

The proxy address low permission bits (`0x…bfFf & 0x3fff = 0x3fff`) advertise all fourteen callback/delta flags; that address-level inference is not implementation behavior. In particular beforeSwap/afterSwap and beforeSwapReturnDelta/afterSwapReturnDelta must be reviewed against current source. Initialization and liquidity callbacks already exist by address encoding; leverage needs no new callback. Returned deltas can shift specified/unspecified quantities and fee timing; quotes must use final router cash movements, not raw AMM output. Match caller identity correctly: hook sender is router, not trader. Position ownership is authenticated in the periphery, never inferred from arbitrary hookData.

Prevent external reentrancy across ledger, vault, callback and payouts; mark position execution before swap and reconcile after settlement, with only expected manager callback allowed during execution. No nested unlock when optional buyback executes inside an already unlocked manager. Buybacks change reserves/ticks and may use claims; separate LP processing can change depth between quote and inclusion. Include both branches of optional buyback success/failure and pending batches in fork tests. Exact-input buys bound total ETH and minimum received CLAUS; exact-output short repayment bounds total gross ETH, verifies full debt amount obtained, handles price-limit partial fills, and reverts without debt credit on underfill. Prove exact-output support rather than assume it. Long sells bound output and price limit. Bounds must include all return-delta fees; public-router quotes and calldata paths require matched state/size tests. Opening leverage cannot skip the main pool or net long/short opens off-pool to evade charges. Voluntary debt top-ups do not refund or bypass earlier executed swap fees.

## Capital convention and inventory needs

All dollar amounts below are **D assumptions**, not available funds. ETH/USD is held at **$2,700**, no live dollar feed; CLAUS is hypothetically **$0.001** at entry. Risks and collateral are ultimately CLAUS/ETH risks. ETH/USD changes create additional dollar exposure. C is net usable collateral; N=LC is gross buy cash for a long and pre-impact spot value of tokens borrowed for a short. Long exposure after buy fees/impact is less than N. Short debt N differs from long debt (L−1)C; short leveraged exposure is N/C. User gross cash is C + aN + opening gas + refundable keeper deposit. It is not C, debt or notional.

At utilization u=0.8: ETH inventory ≥ nLong(L−1)C/u; token inventory ≥ nShort LC/(p0u). Posted collateral and proceeds belong to positions, never reusable lending inventory. Add a separately funded loss reserve of 10% of loan entry value in the loan asset and separately held gas/reward reserve per position of $10.10 (two $4.05 gas assumptions plus $2 incentive). The 10% reserve is an illustrative buffer, not a derived safety guarantee. Unlent 20% inventory is liquidity cash, not counted again as the loss reserve.

The following inventories include the 80% utilization cash buffer, **exclude** collateral, locked proceeds, separate first-loss and gas reserves, and show all-long / all-short books. Mixed books sum each sleeve for its actual count; no cross-netting.

| C/user | L | 1 long: ETH inventory | 5 longs | 10 longs | 1 short: CLAUS inventory | 5 shorts | 10 shorts |
|---:|---:|---:|---:|---:|---:|---:|---:|
| $50 | 1.5x | 0.01157 | 0.05787 | 0.11574 | 93,750 | 468,750 | 937,500 |
| $50 | 2x | 0.02315 | 0.11574 | 0.23148 | 125,000 | 625,000 | 1,250,000 |
| $100 | 1.5x | 0.02315 | 0.11574 | 0.23148 | 187,500 | 937,500 | 1,875,000 |
| $100 | 2x | 0.04630 | 0.23148 | 0.46296 | 250,000 | 1,250,000 | 2,500,000 |
| $250 | 1.5x | 0.05787 | 0.28935 | 0.57870 | 468,750 | 2,343,750 | 4,687,500 |
| $250 | 2x | 0.11574 | 0.57870 | 1.15741 | 625,000 | 3,125,000 | 6,250,000 |
| $500 | 1.5x | 0.11574 | 0.57870 | 1.15741 | 937,500 | 4,687,500 | 9,375,000 |
| $500 | 2x | 0.23148 | 1.15741 | 2.31481 | 1,250,000 | 6,250,000 | 12,500,000 |

For every size/leverage above, a mixed 5-book is 2 longs + 3 shorts; a mixed 10-book is 5 + 5; a 1-book is necessarily one-sided. Multiply the 1-long inventory by nLong and 1-short by nShort. JSON contains the complete 1/5/10 × collateral × leverage × one-sided/mixed matrix (a five-book uses two longs). At $100 and 2x, ten mixed positions need 0.23148 ETH lending inventory and 1,250,000 CLAUS inventory; $1,000 posted collateral is separate, five longs lock 967,326.73 CLAUS and five shorts lock $967.33 proceeds. Add $150 entry-value first-loss reserve (ETH/CLAUS segregated) and $101 gas/reward reserve. No dollar lending source is inferred from these examples.

### Capacity derived from exits and manipulation

Inventory alone cannot set safe OI. For long debt cap: `ΣD ≤ u * ETH sleeve`, but also stressed liquidation proceeds must cover debt and expenses. For shorts: `ΣQ ≤ u * token sleeve`, and stressed executable ETH buyback must fit locked cash and reserves. For a common C: `nLong ≤ floor(u*ETHinventory*ETHUSD/((L−1)C))`; `nShort ≤ floor(u*CLAUSinventory*p0/(LC))`. Apply simultaneous-close rather than only single-position limits.

For a **hypothetical** constant-product virtual quote reserve R=$100,000, a gross buy G has average fee-stripped impact `(1−f)G/R`. This CP average-impact bound is for the buy direction; sell average impact is x/(R+x) in quote-value terms and exact-output repayment can be substantially worse near exhausted depth. A 0.5% average-impact budget implies G≤$511.77; net C≤$341.18 at 1.5x or $255.89 at 2x. Aggregate same-side close size also needs a stressed depth budget: five $100 2x closes are $1,000 nominal and already exceed that illustrative cap. This is an analytical sensitivity, not evidence of actual depth. Concentrated v4 liquidity crosses ticks, can be out of range, and may not have those virtual reserves. Actual current reserves/ticks/limits remain unknown; cumulative added ETH is unusable as R.

For self-funded manipulation, a CP price push r needs net ETH `R(√r−1)` and gross cash `/ (1−f)`. Recoverable inventory/cash is not attack cost. Fee-only round-trip lower bound is `f R(√r−1)[1/(1−f)+1]`: about $227.16 for a 10% push at hypothetical R=$100k. At one tenth that depth it is only $22.72. Do not copy Helix caps: cap aggregate extractable loan loss well below independently replayed minimum attacker cost, with haircut for attacker LP/fee-recipient ownership, slow-price manipulation, arbitrage and buyback flows. A claimant receiving project fees may have lower net cost than this formula. Without that test no positive manipulation-based cap is defensible. Mixed books do not cancel loan-asset risks or eliminate independent closes.

## User costs and provider receipts

Model: f=0.023, each leg has adverse factor i=0.01, gas g=$4.05 per transaction (500,000 gas × 3 gwei × $2700/ETH), keeper reward k=$2 on forced exits, service cost $1/position. Gas is a candidate budget, **not a measured quote**; at 30 gwei the same operation is $40.50 and opening+closing gas is $81. Separate actual gas measurements for old/new hook branches and proposed contracts are required.

Long entry Q=N(1−f)/(p0(1+i)); gross sale=Qp0r/(1+i); net exit V=N(1−f)²r/(1+i)². Long debt D=N−C. Exit equity=max(0,V−D−g−k). Short borrows Q=N/p0, sells for net S=N(1−f)/(1+i); exact-output buyback cash B=Nr(1+i)/(1−f); equity=max(0,C+S−B−g−k). User P&L deducts C, aN and opening g, and includes closing g in equity. Keeper deposit is refunded when unused; forced-exit reward is a further cost. Successful early close gets no refund of fixed opening service charge in this candidate; a rejected atomic open incurs no charge, only failed transaction gas. Pro-rata time refunds are a separately modeled design choice, not included here.

If a real onchain quote already includes f, **do not subtract another 2.3%**. Our formulas include f explicitly because they are not onchain quotes. Project revenue here is 2% of each actual gross ETH leg and platform 0.3%; no lender entitlement. The short buy's gross ETH is B, not Nr, which matters for full-size fees.

Unchanged-price round trip, including both gas transactions; zero opening charge versus 1% of N. Negative values are user loss. No liquidation reward on voluntary close.

| C | L | Long P&L a=0 | Long a=1% | Short a=0 | Short a=1% | Long break-even rise a=1% | Short break-even fall a=1% |
|---:|---:|---:|---:|---:|---:|---:|---:|
| $50 | 1.5x | $-12.92 | $-13.67 | $-13.08 | $-13.83 | 19.48% | 17.84% |
| $50 | 2x | $-14.53 | $-15.53 | $-14.75 | $-15.75 | 16.59% | 15.23% |
| $100 | 1.5x | $-17.74 | $-19.24 | $-18.07 | $-19.57 | 13.71% | 12.62% |
| $100 | 2x | $-20.96 | $-22.96 | $-21.39 | $-23.39 | 12.27% | 11.31% |
| $250 | 1.5x | $-32.20 | $-35.95 | $-33.02 | $-36.77 | 10.25% | 9.48% |
| $250 | 2x | $-40.24 | $-45.24 | $-41.33 | $-46.33 | 9.67% | 8.96% |
| $500 | 1.5x | $-56.31 | $-63.81 | $-57.94 | $-65.44 | 9.09% | 8.44% |
| $500 | 2x | $-72.38 | $-82.38 | $-74.55 | $-84.55 | 8.80% | 8.18% |

Worked $100/2x long: user gross cash $108.05 = $100 collateral + $2 opening charge + $4.05 open gas + $2 keeper deposit. Vault lends $100 ETH-value; gross buy $200, fee $4.60, Q=193,465.35 CLAUS. Unchanged-price gross exit $191.55, net exit $187.14; close gas $4.05; debt repaid $100, trader equity $83.09 plus unused $2 keeper deposit refunded. Total P&L **$-22.96**. Both pool fees total **$9.01**, adverse impact loss $3.76, already reflected in equity. At +25%, long equity is $129.88 and net user P&L $23.83.

Worked $100/2x short: vault lends **200,000 real CLAUS**. Gross pre-fee sale ETH-value $198.02, fee $4.55, locked proceeds $193.47 plus C=$100. At unchanged price, gross exact-output buyback is $206.76 (including $4.76 fee); close gas $4.05; 200,000 CLAUS repaid, trader equity $82.66, unused keeper deposit refunded. Total P&L **$-23.39**; both pool fees **$9.31**. At −25%, buyback is $155.07, equity $134.35 and net user P&L $28.30. These examples keep ETH/USD fixed; none is an exact CLAUS execution.

Provider revenue is upfront receipts only, distinct from pool revenue. Assuming user-funded gas and $1 service per position, the $100/2x unchanged-price examples give:

| Upfront rate on N | Receipt | Healthy provider net after $1 service | User long P&L | User short P&L |
|---:|---:|---:|---:|---:|
| 0.0% | $0.00 | $-1.00 | $-20.96 | $-21.39 |
| 0.5% | $1.00 | $0.00 | $-21.96 | $-22.39 |
| 1.0% | $2.00 | $1.00 | $-22.96 | $-23.39 |
| 1.5% | $3.00 | $2.00 | $-23.96 | $-24.39 |

Actual provider profit = opening receipts − loan-asset bad debt − provider-paid gas − service/keeper overhead. The table is **not** expected profit: loss frequency and overhead are unknown. A $1 healthy net at 1% is overwhelmed by one crash loss; mark short losses in CLAUS first. If gas reserves fail or keeper needs a larger incentive, provider net deteriorates. Loss reserves shift who absorbs loss, not whether the system lost money. Existing operating wallet payments for LP processing remain existing obligations, not a lending subsidy.

## Stress, insolvency and adversaries

Below: immediate liquidation at stressed endpoint, $100 C, 2x, 1% entry/exit impact, $4.05 closing gas and $2 reward; no assumption of earlier successful liquidation. The stress model conservatively deducts close gas/reward from position resources before repayment; it does not credit the separately reserved escrow toward debt recovery. Thus it overstates loan shortfall relative to expenses paid entirely from separate escrow, which consumes that reserve instead. Keeper escrow is an earmarked expense balance, never reusable loan inventory. Provider loss is principal shortfall **before** separately funded reserve absorption, valued at entry (short current-value loss additionally shown). Upfront revenue is excluded from principal loss; zero residual user equity does not cancel debt.

| CLAUS/ETH move | Long equity | Long ETH-debt loss ($ entry) | Short equity | Short debt loss ($ entry) | Short debt loss ($ current) |
|---:|---:|---:|---:|---:|---:|
| -10% | $62.38 | $0.00 | $101.34 | $0.00 | $0.00 |
| +10% | $99.81 | $0.00 | $59.98 | $0.00 | $0.00 |
| -25% | $34.31 | $0.00 | $132.35 | $0.00 | $0.00 |
| +25% | $127.88 | $0.00 | $28.97 | $0.00 | $0.00 |
| -50% | $0.00 | $12.48 | $184.04 | $0.00 | $0.00 |
| +50% | $174.67 | $0.00 | $0.00 | $14.65 | $21.98 |
| -90% | $0.00 | $87.34 | $266.74 | $0.00 | $0.00 |
| +200% | $455.38 | $0.00 | $0.00 | $107.33 | $321.98 |
| +1000% | $1,952.54 | $0.00 | $0.00 | $174.73 | $1,921.98 |

The JSON also contains all these stresses at 1.5x. Long loss at −90% is $42.01 at 1.5x versus $87.33 at 2x; short +1000% still loses most token principal at either leverage. At 2x the $100/short +1000% loss is approximately 174,725 CLAUS ($174.73 at entry; $1,922 at current price). Ten same-side positions scale principal losses roughly tenfold only under the fixed-impact assumption; correlated execution can be worse. The separate 10% loss reserve does not cover these gaps.

Solvency-only thresholds with forced-exit expenses: long `r=(D+g+k)(1+i)²/[N(1−f)²]` (2x about 0.567); short `r=(C+S−g−k)(1−f)/[N(1+i)]` (2x about 1.390). Liquidate well before these, using full-exit quotes. Candidate exit-health trigger 1.25 is a research buffer: long health=net executable sale/D; short health=locked ETH/executable buyback. It needs gas/reward subtraction and stressed quote uncertainty. Even a larger health threshold cannot protect a one-block gap.

| Failure/adversary | Loss mechanism and next-test requirement |
|---|---|
| ±10/25/50%; rapid −90%, +200/+1000% | Table separates trader equity and loan shortfall. Shorts owe tokens after a squeeze; higher ETH value does not mean new tokens can be created. Replay actual exits, not marks |
| One-block gap | No keeper/oracle update necessarily runs before price jumps. Crash can consume nearly all long ETH loans; unlimited squeeze makes repurchasable token fraction approach zero |
| 1/5/30 minute keeper outage | JSON uses illustrative ±1%/minute compounded paths. Under 30-min decline r=.7397 or rise r=1.3478, both 2x sleeves remain solvent under our fixed-depth endpoint assumption, but are close enough to require liquidation. Time alone implies no loss: any outage can contain a −90%/+1000% gap |
| Thin/out-of-range liquidity | Missing ticks or liquidity removal can make bounded swaps unfillable. Reserves do not create pool depth; widen slippage only within explicit position risk. Actual exits may fail indefinitely |
| Simultaneous closes/expiry crowding | Subsequent prices and gas deteriorate. Reserve aggregate stressed close depth, cap same-side OI, stagger deadlines and auction permissionless keeper execution. No promise that expiry equals immediate cash settlement |
| Stale/manipulated mark; slow-oracle lag | Spot manipulation can change admission and liquidation; TWAP/slow price can lag a genuine crash or squeeze. Freshness failure stops opens, not repayment. Compare delayed reference against executable full-exit quote; no oracle arrangement proved safe here |
| Front-running/sandwich | Adverse executions eat health. Bound deadlines, gross cash, min outputs and exact-output debt fills; replay worst allowed fills. Private execution may help but is not assumed available |
| Self-funded pump/dump | Open at manipulated price, exit or abandon to extract pot. Our fee-only attack estimates are insufficient if attacker owns LP/fee claims; measure net unrecoverable cost versus aggregate provider exposure. Do not rely on market cap |
| Vault withdrawal with open loans | Withdraw only sleeve cash above utilization/liquidation buffers; lock receivables, queue remainder until repayment/expiry; no instant withdrawal of lent assets. Stop new lending on exit notice; never stop existing close |
| Hook upgrade/optional processors | Changed permissions/quotes, pause behavior or reentrancy can invalidate adapter assumptions; stop opens on unreviewed implementation change. A permission change is outside this task; test compatibility without restricting ordinary spot users |

**True worst case:** all allocated lending inventory and separately allocated reserves can be lost through price gaps, absent exit liquidity, manipulation or contract failures. Under pure price scenarios loss is bounded by assets actually lent; a short's ETH mark-to-market replacement liability can be unbounded, while finite missing token units approach the entire token loan. Unlent inventory is not normally price-gap loan loss but can suffer token-price losses or contract compromise. The stress table is not the true maximum, a probability forecast or audited guarantee.

## Interest-free alternatives and recommendation

1. **Fixed term + upfront charge:** clearest bounded capital occupation. Charge pays origination/risk/capacity service, not hourly accrual; debt does not grow with time. Utilization caps and permissionless expiry repayment reclaim inventory only if closes remain executable. Never roll automatically or levy disguised hourly renewals. Stagger expiries and hold withdrawal requests against actual cash.
2. **Fixed term + zero provider charge:** technically possible, economically unattractive absent separately authorized voluntary funding of service and bad-debt risk. No project allocations assumed available. Use zero as a research control, not a promise of free unlimited lending.
3. **Fully collateralized in loan asset / prepaid maximum-loss escrow:** can remove unsecured provider price exposure at much higher user capital and custody cost; may defeat useful leverage. Finite-term, capped in-kind credit with demonstrably sufficient independent collateral is more defensible than indefinite zero-cost occupation, but requires a complete separate payoff analysis.
4. **Bounded matched payoff:** escrow both counterparties' maximum losses and settle finite claims at expiry, without unlimited loans. Explicitly a different derivative, not a silently substituted spot-backed short. Its pool-fee relationship, oracle and settlement require separate work; no new coin or off-pool fee bypass is approved.

Staying spot-only preserves existing fees and LP economics, needs no external pot or liquidation oracle, avoids token-loan bad debt and borrower withdrawal mismatch, and leaves users bearing their own spot-price/gas/slippage risk. Leveraged positions offer amplified exposure but use scarce inventory and roughly two full-notional pool swaps; for $50/$100 positions fixed mainnet gas often dominates provider revenue. The smallest coherent spot-backed candidate still needs ledger, two asset sleeves, adapter, observations, keeper and loss accounting. It is materially more complex than spot-only.

Recommended now: **zero live OI; no deployment or allocation**. For the next local test only: ≤1.5x, one $50–$100 collateral position at a time, 24-hour maximum lifetime, 80% utilization ceiling, candidate 1.25 exit-health threshold and segregated 10% loan-value reserve plus measured gas/reward escrow. These provisional buffers are not certified safe; choose no upfront fee until cost/loss evidence supports one. $250/$500 and five/ten concurrency remain scenarios to test, not promised capacity. A positive eventual cap must be the minimum of actual inventory, stressed simultaneous exit depth and manipulation-loss economics; an arbitrary pool TVL percentage is insufficient.

Unresolved: independently pinned implementation and runtime source; callback deltas/fee rounding for exact input/output; active ticks/current LP state; actual quote sizes and buyback branches; proposed router support; independent oracle feasibility in a single thin market; keeper profitability and outage recovery; provider loss appetite and new funding source; term/withdrawal UX and fee refund policy. Do not report any of those as solved.

Narrow next test: obtain a pinned mainnet block and actual proxy implementation, verified current source and complete relevant tick state; rehearse a single position's open/partial/full/expiry/liquidation path on an offline fork with identical public-router comparisons, recording gross cash, deltas, fee destinations and gas. Then replay one-block crash/squeeze and self-funded manipulation before admitting any concurrency. Nothing in this assignment signs, sends or deploys a transaction.

## Reproduce and local checks

From repository root:

```sh
python3 artifacts/leverage-model.py --self-test
mkdir -p test/scratch
python3 artifacts/leverage-model.py > test/scratch/recomputed.json
python3 -m json.tool artifacts/leverage-analysis.json > /dev/null
```

Default model output reproduces `analytical_results` in the JSON, including every capital/cost/stress row. It uses only Python standard library, no network, secrets or payments. Calculations are floating-point analytical amounts, not Solidity/fork rounding; self-tests additionally check directed 18-decimal rounding using Decimal, cash conservation, actual debt-asset repayment, nonnegative fees, insolvency and break-even. Precision shown in tables is for reproducibility, not market precision. Conservation tests cover simplified healthy/insolvent exits; they do not prove deployed settlement, reentrancy safety or liquidation liveness. The model uses fixed adverse execution factors; capacity/attack examples use a hypothetical constant-product approximation, **never an exact concentrated-liquidity v4 simulation**.

All three artifact paths were checked, JSON parsed, model self-tests run and analytical output compared with the saved JSON. These are local checks without independent authority. No production-readiness, audit or profitability claim is made.

