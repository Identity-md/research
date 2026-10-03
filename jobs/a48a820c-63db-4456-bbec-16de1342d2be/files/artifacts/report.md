# Swarm Pepes fee-sharing token: feasibility and design

Research date: 3 October 2026. Scope: Ethereum mainnet; research only, no deployment or contract implementation.

**Verdict: YES to a prototype with changes; NO to production exactly as described.** ETH-denominated hook fees and NFT-specific accrual are feasible. A standard transferable ERC-20 cannot enforce “one pool only,” zero-price auctions do not guarantee a buyer, and ongoing NFT minting needs an explicit eligibility rule. The swarm can implement and test this, but its ability to provide an adequate independent audit has not been established.

Evidence labels: **Fact** means supported by a linked primary source; **Inference** means analysis of those facts or the proposed mechanism; **Recommendation** means a design choice, not a proven optimum. **Unknown** identifies evidence still needed. Collection address, 5,000 maximum supply, no transfer hooks and standard ERC-721 behavior are **client-provided assumptions**. The collection's verified source and live state were not independently retrieved: the Etherscan code-page request failed. No current minted count, mint finality, burn behavior or runtime bytecode verification is claimed. Primary sources below were accessed on the research date; GitHub `main` links are mutable and must be pinned before implementation.

## 1. Can the swarm build, test and audit it?

**Inference: technically buildable, organizational audit capacity unknown.** Use a fixed-supply ERC-20 with actual supply-reducing burn; an immutable native-ETH/token v4 hook; and one distributor/custody/auction state machine. Combining custody and auction accounting avoids cross-contract transitions leaving an NFT simultaneously active and auctioned. Separate creator withdrawal accounting from NFT liabilities.

**Fact:** v4 supports native ETH, custom accounting and pool lifecycle hooks ([v4 whitepaper](https://app.uniswap.org/whitepaper-v4.pdf)). Hook permissions are encoded in the deployed address, including return-delta flags ([Hooks.sol](https://github.com/Uniswap/v4-core/blob/main/src/libraries/Hooks.sol)). **Recommendation:** authenticate PoolManager and the exact PoolKey; authorize initialization; initialize, seed liquidity and set launch time atomically. Restrict any hook-owned swap entry point: core skips swap callbacks when the hook itself is the caller, so a publicly exposed untaxed hook swap would be dangerous.

Hard parts: delta signs and settlement, partial fills, exact-output semantics, malicious receivers, custody consistency, eligibility without mint callbacks, and economic manipulation. Test all supported directions and amounts, price-limit partial fills, callback reentrancy, last-NFT exits, same-block exit/buy/swap ordering, direct PoolManager calls, fake NFT callbacks and repeated auction cycles. Fuzz conservation: received ETH must cover paid ETH, creator credits, NFT liabilities and rounding residue; escrow count must match custody; auction reactivation must start with zero pending. Fork-test the actual NFT and pinned v4 deployment. Require an independent Solidity/v4 review plus economic review and remediation before production; swarm self-review is useful but is not independent assurance. No such tests or audits were performed for this research report.

## 2. Is 2.5% in ETH on both sides implementable? Can routing bypass it?

**Fact:** return deltas adjust swapper obligations; PoolManager requires all currency deltas settled before unlock completes ([PoolManager.sol](https://github.com/Uniswap/v4-core/blob/main/src/PoolManager.sol)). Uniswap's test fee hook takes the unspecified currency through `manager.take` and returns a matching delta ([FeeTakingHook.sol](https://github.com/Uniswap/v4-core/blob/main/src/test/FeeTakingHook.sol)); it is an example, not audited production code.

**Recommendation:** first support exact-input swaps only. For an ETH buy budget `B`, charge `fB` ETH and swap `(1-f)B`; for a sell yielding gross ETH `G`, charge `fG` and deliver `(1-f)G`. Buy ETH is the specified currency, suited to `beforeSwap` specified deltas; sell ETH is unspecified, suited to `afterSwap`. For the pilot, revert price-limit partial fills and require full consumption of the post-fee input. Later partial-fill support must reconcile/refund unused fee reservations; taxing a requested amount when only part fills overcharges users. Reject unsupported exact-output modes explicitly in both quotes and execution. Full exact-output support requires gross-up: desired net sell output `Y` needs gross `Y/(1-f)`, and buy pool input `X` needs total `X/(1-f)`. A naive afterSwap-only hook cannot implement all four direction/mode combinations. Sign, integer rounding and partial-fill handling require implementation tests.

This is a **hook surcharge**, separate from LP/protocol fees; changing only the dynamic LP fee would not route all fees to the distributor or charge sells in ETH. Use native ETH, not WETH, as the pool currency; routers can wrap/unwrap at the edges.

**Fact:** PoolKey includes currencies, LP fee, tick spacing and hook address; pool initialization is public ([PoolKey.sol](https://github.com/Uniswap/v4-core/blob/main/src/types/PoolKey.sol), [initialize](https://raw.githubusercontent.com/Uniswap/v4-core/main/src/PoolManager.sol)). **Inference:** every ordinary swap in this designated pool invokes its configured hook regardless of router, but anyone holding an unrestricted token can fund another v4 pool without it, another AMM, or an OTC trade. Launching one pool does not prevent those markets. Liquidity addition/removal can also create alternative economic exchange paths and deserves adversarial testing. Transfer restrictions could constrain venues but sacrifice unrestricted ERC-20 composability and still do not tax offchain claims. Prefer accepting and disclosing pool-local coverage.

**Unknown:** actual aggregator/UI support for this specific hook. Require fee-aware quoting, net-output slippage, maximum fee and deadlines; test the chosen Universal Router/quoter and aggregator versions. Do not require router-specific identity or trust `hookData` to supply the fee. Unsupported hooks may be omitted from routing entirely.

## 3. Anti-sniper start and decay

**Recommendation:** start at 20%, decay linearly over 30 minutes to 2.5%, continuously by elapsed seconds:

`feeBps(t) = 250 + ceil(1750 * (1800 - min(t,1800)) / 1800)`

Here `t = block.timestamp - launchTime`, with a prelaunch guard. Use full-precision arithmetic and an immutable launch time. This is a moderate, provisional choice: simulate demand and price impact before adopting it. At -1 percentage point/minute, 20% reaches the floor in 17.5 minutes with continuous decay, or 18 minutes with clamped minute steps. “1%” must mean 100 basis points, not a relative 1% decrease. A near-100% start creates extreme execution costs and exact-output problems.

**Fact:** Ethereum PoS has 12-second slots, and execution timestamps must equal the consensus slot time ([Ethereum PoS](https://ethereum.org/developers/docs/consensus-mechanisms/pos/), [consensus validation](https://raw.githubusercontent.com/ethereum/consensus-specs/master/specs/bellatrix/beacon-chain.md)). **Inference:** proposers cannot choose arbitrary timestamps; they can still reorder, delay or omit transactions. Minute steps create predictable cliffs; continuous decay reduces those cliffs but does not stop bundles, sandwiches, private ordering or bots waiting for cheaper fees. In the suggested curve one normal slot changes the fee by about 11.7 bps. A fee is a deterrent, not sniper prevention. If fair allocation is essential, evaluate a batch launch separately; do not market this as fair distribution.

## 4. Accumulator, precision and changing counts

**Recommendation:** let `Q=10^27`, `A` be a scaled accumulator, and `D[id]` scaled debt. For NFT-share incoming wei `W` and active count `N>0`:

`increment = floor(W*Q/N); A += increment; pending(id) = floor((A-D[id])/Q)`.

Use full-precision multiplication/division, checked bounds and explicit residue accounting. Never use raw integer `newEth / activeCount`: deposits below `N` wei would disappear. Global division residue is less than `N/Q` wei per update; per-ID payout truncation can discard less than one wei per exit. Leave that dust backed and disclosed, never permit an admin sweep of liabilities. Do not recompute entitlements from the contract's ETH balance: forced ETH and unsolicited transfers need separate accounting.

On exit, compute pending at the old count; mark the ID inactive, reset its debt and decrease `N` before external interactions, then complete NFT custody and ETH payout atomically. A reverting ETH recipient should revert only its own exit; offer an owner-selected payout recipient. On purchase, mark auction consumed, burn payment, set `D[id]=A`, and increase `N` before delivering the NFT, with rollback on failure. Inactive IDs have zero pending regardless of `A`. Normal transfers change neither `A` nor debt, so accrual follows the ID. Explicit owner authorization prevents an approved NFT operator from stealing its ETH payout. Reject unsolicited safe transfers; define recovery for direct unsafe NFT transfers without manufacturing an exit entitlement.

**Critical unknown:** is minting finished, and can IDs be burned? ERC-721 enumeration/`totalSupply` is optional ([ERC-721](https://eips.ethereum.org/EIPS/eip-721)). With no mint callback, reading an increasing supply does not set new IDs' initial debt. Default-zero debt would award them historical fees and can make liabilities exceed assets. **Recommendation:** launch after minting is irrevocably finished, or use an immutable snapshot of eligible IDs and count, with lazy membership proofs. The latter changes the promise to snapshot NFTs, not all future minted NFTs. Do not treat unminted IDs as active or silently include future mints; supporting them prospectively requires a different enrollment/mint integration.

Small `N` amplifies concentration: at `N=1` all new NFT-share fees go to one ID. At `N=0`, division is undefined. Suggested policy: block designated-pool swaps until an auction buy reactivates an NFT; keep auction buys available. This is a disclosed liveness tradeoff, not a universal trading halt. Never queue zero-count fees for the first reactivating buyer to capture. Reentrancy protection must cover swaps/funding, exits and buys together, not merely each external function in isolation.

## 5. Dutch auction soundness, first sale and wash sales

**Inference: reject the last-sale multiplier as proposed.** The first auction has no reference. A zero-price sale makes the next start zero, and the entire sequence can remain free. A cheap wash purchase lowers subsequent starts; an expensive purchase can inflate them and delay turnover. Burning payment makes manipulation costly, but does not make the sale an independent valuation, especially in an illiquid self-issued token. A global last-sale reference also lets one auction distort others and ignores trait differences.

**Recommendation:** use a disclosed fixed token-denominated bootstrap price `P0` for every auction in the pilot, rather than an adaptive reference. Use `price(t)=ceil(P0*(1-min(t,T)/T)^2)` with `T=36h`, computed as an integer rational expression; allow zero-cost claim after expiry. Store each auction's start time and price once; add buyer `maxPrice`, deadline and a unique auction nonce. `P0` remains a launch decision requiring token denomination and demand simulations; no defensible numerical token price follows from the supplied information. Later calibration could use a bounded, slow-moving reference with minimum/maximum starts and exclude zero sales, but cannot prove wash resistance from addresses alone.

Zero price means *claimable*, not “always sells”: transactions, gas and an interested recipient are still needed; bots may win the expiry race. Burn via the token's supply-reducing function atomically with acquisition, rather than merely sending to a dead address. Burning does not guarantee token appreciation or ETH backing. All auction proceeds can be burned, but token purchases to fund bids also incur hook fees only if they use the designated pool.

## 6. Can the exit/rebuy loop be farmed?

**Inference:** correct debt resets prevent claiming the same accrual twice. Buying a cheap NFT with accumulated ETH and exiting it is ordinary arbitrage; the buyer must obtain the NFT and loses it into auction. Immediate rebuy has zero historical pending. Repeating the loop without new funding earns zero ETH and costs gas/payment.

Economic farming remains: acquire low-price auction NFTs, collect future fees, then exit; keep some NFTs active while others are excluded; bundle NFT acquisition before a large swap and exit after it. If an attacker owns `k` of `N` active NFTs, it can recover approximately `k/N` of NFT-share fees it creates. For one fee `F` and creator fraction `c`, its unrecovered fee is approximately `F*[1-(1-c)*k/N]`, before LP fees, price impact and gas. At `k=N` and `c=0`, it recovers all hook fees eventually: fee-funded wash volume can be cheap. This is an incentive consequence, not necessarily an accounting exploit. No address blacklist solves multi-wallet self-dealing.

**Recommendation:** enforce one escrow/auction state per ID, zero-debt reentry and atomic payments; permit exits only after 24h from auction reactivation (ID-specific, survives transfer). A one-block minimum only prevents some atomic cycles. The 24h delay limits rapid churn but does not prevent future-fee capture or ordinary transfers bundling accrual. Initial snapshot holders retain immediate exit rights. Disclose the cooldown and model low-count scenarios; neither cooldowns nor burn establish economic sustainability.

## 7. Gas and mainnet viability

**Estimate, unmeasured:** for a straightforward implementation, budget **30,000–90,000 extra gas per swap** over the same route without the hook, roughly **150,000–300,000 total** for a simple routed single-pool swap, and **140,000–260,000 gas per exit** excluding any prior NFT approval. Auction buys might be **110,000–220,000 gas**. These are engineering allowances based on additional calls, storage updates, custody and settlement, not fork benchmarks or guaranteed bounds; tick crossings, cold/first writes, receiver contracts and router composition can exceed them.

At hypothetical effective gas prices of 10/30 gwei:

| Operation | At 10 gwei | At 30 gwei |
|---|---:|---:|
| Total swap, 150k–300k gas | 0.0015–0.003 ETH | 0.0045–0.009 ETH |
| Exit, 140k–260k gas | 0.0014–0.0026 ETH | 0.0042–0.0078 ETH |

**Fact:** cost is gas used times effective gas price; base fee varies with demand ([Ethereum gas](https://ethereum.org/developers/docs/gas/)). The table is not today's quote; no USD price assumption is needed. Mainnet is plausible for meaningful trades and infrequent accrued exits, unattractive for dust harvesting. Keep O(1) funding, avoid per-holder writes on swaps, and accrue creator credits instead of sending ETH to a creator on every swap. Funding must be a minimal deterministic path so a creator receiver cannot freeze trading. PoolManager claim-based batching may save transfers but requires flushing before every count change to preserve attribution; do not add it before profiling. An L2 would need NFT bridging/wrapping and cross-chain entitlement rules, materially changing this same-chain proposal.

**Launch correction:** token-only concentrated liquidity is feasible, but “above current price” must specify units. Native ETH is currency0; at core price `token/ETH`, token1-only liquidity is below current price (above in reciprocal `ETH/token`). Verify ordering, decimals and directional range traversal in fork tests. Out-of-range liquidity is one-sided ([concentrated liquidity](https://developers.uniswap.org/docs/get-started/concepts/liquidity-providers/concentrated-liquidity)). Specify supply allocation, range width, LP custody/withdrawal powers and inventory exhaustion. “Launched from zero” can mean zero ETH raised, not zero initialized price: v4 requires a valid nonzero square-root price. First buyers provide ETH inventory; future ETH exit liquidity is not guaranteed.

## 8. Would I build it? Top three changes and creator disclosures

**Recommendation:** build a limited prototype after settling these three changes:

1. Promise fee sharing from the designated pool, accepting external-market bypass; support exact-input first, fix launch price/range and disclose LP control.
2. Freeze eligibility and implement scaled, solvent ID accounting with atomic custody, debt reset and explicit zero-active behavior.
3. Replace last-sale pricing with fixed-start auctions for the pilot; disclose free expiry claims, add a 24h reexit delay, and test fee-recovery/concentration economics.

Creator share: suggest **500 bps of collected hook ETH**, immutable, with an absolute **1,000-bps cap** in code (5% chosen; 10% maximum of fees, not trade volume). At the 2.5% base surcharge, 5% of fees is 0.125% of the defined ETH fee base for the creator and 2.375% for NFTs, subject to rounding. Credit the share before the NFT accumulator; withdraw separately. Say “all fees reach the distributor, then 95% goes to NFTs,” not “100% goes to NFTs.” Prefer an immutable recipient, or clearly disclose any recipient-change authority; upgrades could defeat nominal hard caps unless excluded.

**Legal fact:** SEC guidance distinguishes an asset's category from transactions sold as investment contracts; representations of managerial efforts and expected profits matter ([SEC transaction guidance](https://www.sec.gov/resources-small-businesses/capital-raising-building-blocks/transactions-involving-crypto-assets), [March 2026 interpretation](https://www.sec.gov/rules-regulations/2026/03/s7-2026-09)). **Inference, not a legal classification:** explicit passive ETH sharing and creator promotion merit jurisdiction-specific securities, tax and consumer-disclosure advice for both the new token and NFT entitlement. An NFT label, automation or a capped creator fee is not an exemption. Issuer/operator identity, marketing, purchaser jurisdictions and powers are unresolved. Disclose recipient, fee basis, launch schedule, creator cap, change powers, pool-local coverage, custody/exit risks, auction burn/free claims and absence of guaranteed yield or liquidity. This research does not determine registration or licensing obligations.

## Suggested parameters and risk register

| Parameter | Pilot recommendation |
|---|---|
| Token | Fixed supply; 18 decimals; real burn; no transfer tax or venue restrictions |
| Venue | One designated native-ETH v4 pool; external markets allowed |
| Supported swaps | Exact-input buys/sells first; reject partial fills in pilot |
| Hook surcharge | 250 bps base; 2,000 bps launch; linear 1,800-second decay |
| LP fee | Provisional 30 bps, separate from hook fee; simulate depth/LP economics |
| Creator | Immutable 500 bps of hook revenue; absolute 1,000-bps cap |
| Eligibility | Finalized mint set, else immutable snapshot with membership proofs |
| Accumulator | `Q=10^27`; full-precision math; explicit dust backing |
| Active count zero | Designated swaps revert; auction buys remain available |
| Auction | Fixed `P0`; squared decay; 36h; zero-price expiry claim; 100% payment burn |
| Reactivation | Debt reset to current accumulator; 24h ID-based reexit delay |
| Admin | Prefer immutable fee/eligibility/custody logic; no liability withdrawal |

`P0`, total token supply, initialization price, liquidity ticks/amounts and LP custody are **unanswered launch inputs**, not hidden defaults. All suggested values are provisional economic choices, not audited parameters.

| Risk | Priority / consequence |
|---|---|
| Alternative pools and OTC bypass | Critical to revenue promise; no universal fee guarantee |
| Incorrect mint eligibility/debt | Critical solvency failure or historical-fee theft |
| Hook settlement or custody/reentrancy bugs | Critical loss of funds/NFTs or frozen swaps |
| Small/zero active count | High concentration and designated-pool liveness risk |
| Auction reference manipulation/free claims | High economic distortion; burn may be negligible |
| MEV, wash volume and fee recapture | High; anti-sniper fee/cooldown only mitigate parts |
| Shallow/exhausted range or LP withdrawal | High price impact and liquidity loss |
| Unsupported routing or mainnet cost | Medium/high adoption and execution risk |
| Creator powers and legal characterization | High; disclosures and jurisdictional review required |

Validation performed: local document structure and arithmetic model checks only (see README). They support report integrity and examples, not contract behavior, security, economic profitability or an independent audit.
