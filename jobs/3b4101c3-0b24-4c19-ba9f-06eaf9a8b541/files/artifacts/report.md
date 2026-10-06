# SPEPE / Swarm Pepe: design and economic review

**Scope.** This is a design review, not an implementation or deployment recommendation. Dollar examples are scenario arithmetic, not forecasts. “Fact” means directly observed or linked; “inference” means an assumption or calculation; “unknown” means I could not establish it from the cited material.

## Executive verdict

The proposed system is technically possible, but not realistic as specified for Ethereum mainnet. The largest issue is not gas: it is that the original ERC-721 has no transfer hook, while the design wants a transferable, stateful economic position. A distributor can track state by `tokenId` and read `ownerOf()` lazily, but it cannot enforce that every transfer, marketplace sale, wrapper, or custody change is reflected in the protocol. That is survivable only if the rules are explicitly token-id based and all value is claimed through the distributor; it is incompatible with promises about holder-time accounting or automatic transfer settlement.

The “single-sided liquidity from first buyers” launch is also a poor mainnet launch mechanism. A pool with no initial ETH has no meaningful initial price; the first buyers provide price discovery while the token side can be bought out or manipulated. A 2.5% buy plus 2.5% sell hook fee makes a 5% round trip before LP fee, price impact, gas and NFT-marketplace fees. It can generate revenue, but it strongly invites wash trading and makes honest liquidity formation expensive.

**Recommendation:** do not launch the full auction/exit/three-level loop. If proceeding, use one audited v4 pool, a 1.0% fee on each direction, zero team cut until a public reserve threshold is met, fixed immutable activation prices, three weights of 1/2/4, a capped activation set, a timelocked emergency pause, and a separate permissionless distributor claim. Use a wrapper/escrow only if transfer-time semantics are essential. Otherwise, treat the NFT as a bearer certificate whose level and accrual stay with the token ID.

## What is verified about the existing collection

As checked on 6 October 2026:

* The live contract is `0x999ce0CE8C5f7661e0c74a568FfE27CEB9177bDB` on Ethereum mainnet. Its read-only RPC calls returned `MAX_SUPPLY() = 5,000`, `totalMinted() = 1,239`, `MAX_PER_WALLET() = 3`, and `mintOpen() = true`. The contract’s standard `totalSupply()` selector reverts, so it should not be used as a minted-count source.
* The project frontend exposes the same ABI/state and says that slots are allowlisted, minting is gas-only, and there is “no mint price”; it also says the owner cannot mint and that each wallet can mint up to three. [Swarm Pepe’s live mint UI](https://swarmpepe.xyz/) is attributable evidence for the stated user-facing rules; the RPC values above are the stronger on-chain evidence.
* OpenSea currently reports 1,239 items, 459 unique owners, 118 listed (9.5%), a roughly $72 floor, and 6.9% creator fee on its collection page. Its API stats separately reported 458 owners, 349 sales and 6.916 ETH all-time volume at the time checked; this small discrepancy is expected from indexing timing, so these are marketplace observations, not consensus state. [OpenSea collection page](https://opensea.io/collection/swarm-pepe), [OpenSea collection stats API](https://api.opensea.io/api/v2/collections/swarm-pepe/stats).
* The holder page showed concentration at the top: the largest displayed holder had 11 (0.89%), the next 10 (0.81%), and several had 6–9. This is only the displayed leaderboard, not a complete concentration calculation. [OpenSea holders](https://opensea.io/collection/swarm-pepe/holders).
* Recent activity included mints and secondary sales, confirming that minting is still active in the indexer view. [OpenSea activity](https://opensea.io/collection/swarm-pepe/activity).

The contract’s on-chain mint price is therefore **0 ETH** for the current allowlisted claim path, with gas payable. A wallet still needs an allocation; “free” does not mean permissionless. Historical stages, allocations, and any future owner change remain an uncertainty to monitor.

## Feasibility and complexity

Uniswap v4 can call a hook around swaps, supports custom accounting/deltas, and supports native ETH through the singleton architecture. Those are real primitives, not a guarantee that every router will present the amounts or call pattern the design expects. [Uniswap v4 hooks](https://developers.uniswap.org/docs/get-started/concepts/hooks), [custom accounting and hook fees](https://developers.uniswap.org/docs/protocols/v4/guides/custom-accounting), and the [v4 whitepaper](https://app.uniswap.org/whitepaper-v4.pdf) are the primary technical references.

The hook must be permissioned to one exact `PoolKey`, reject unexpected currencies and callers, calculate actual deltas rather than trusting user-supplied calldata, and handle native ETH/WETH and exact-input/exact-output paths. “Only one pool” is a social rule unless the token itself or all liquidity venues are controlled. A second v2/v3/v4 pool, aggregator route, OTC trade, bridge or wrapper bypasses the fee.

Indicative mainnet gas ranges (inference, not a benchmark; calldata, cold/warm slots, ETH price and base fee dominate):

| Action | Plausible gas range | Main cost/risk |
|---|---:|---|
| Simple SPEPE swap plus hook | 120k–220k | Hook accounting, ETH settlement, router path |
| Activation (approve/permit + burn + several storage writes) | 120k–220k | ERC-20 approval can be a separate transaction |
| Exit, NFT escrow, payout, auction creation | 180k–320k | ERC-721 safe transfer callback and reentrancy |
| Auction purchase and NFT transfer | 150k–280k | Token burn, auction state, ERC-721 transfer |
| Claim only | 60k–120k | Storage update and ETH transfer |
| Initial pool/configuration | 300k–1m+ | Deployment, initialization, liquidity position |

These are material costs for a collection whose observed floor is only tens of dollars. Every ETH payout also needs a reentrancy-safe pull pattern, failed-send handling, and a policy for dust/rounding. Auditing the hook, distributor, auction, and an ERC-721 escrow/wrapper is a multi-contract audit, not a small add-on.

## Recommended accounting model

Let level weights be `w1=1`, `w2=2`, `w3=4`. Let `W` be the sum of weights of activated token IDs. Keep a global fixed-point accumulator `accPerWeight`, and for each active token store `weight` and `debt`:

`accPerWeight += distributableEth * SCALE / W`

`pending(id) = weight[id] * accPerWeight / SCALE - debt[id]`.

On activation, first account the new token at the current accumulator, set its weight, and set `debt[id] = weight * accPerWeight / SCALE`; it earns nothing from prior fees. On claim/exit, pay pending, then set debt to the current weighted share. On an NFT transfer, no hook is required if level and accrual are deliberately properties of `tokenId`; only the current `ownerOf(id)` may claim or exit. This makes the prize travel with the NFT, but it means a buyer receives any unclaimed pending amount. A marketplace sale cannot atomically force the seller to settle.

There is a crucial zero-active-set rule. If fees arrive while `W=0`, do **not** divide by zero and do not assign the balance to the first activator. Keep `backlogEth` and a `backlogRate`/release schedule. For example, release at most 1/30 of backlog per day into `accPerWeight`, with a maximum per block, until exhausted. New activation sets debt against the current accumulator and receives none of the already-held backlog. A simpler equivalent is to keep `undistributed` and stream it over a fixed 30-day epoch; the invariant is that no first-activator windfall exists.

Do not maintain a holder array or loop over NFTs. Never rely on the collection’s broken/reverting `totalSupply()`; active count and total weight are protocol-owned state and must be updated only on activation, exit, and auction settlement.

## Levels, costs and parity

Recommended launch parameters:

| Level | Weight | Immutable SPEPE burn | Rationale |
|---|---:|---:|---|
| 1 | 1 | `B` | Entry utility |
| 2 | 2 | `3B` cumulative | Meaningfully higher commitment |
| 3 | 4 | `8B` cumulative | Scarce high-weight position |

Set `B` once from a published launch parameter and do not derive it from a spot price. If the project wants price-sensitive costs, use a long-window, capped TWAP only as a quote displayed off-chain; do not make activation safety depend on a manipulable single-block price. Since minting is currently zero ETH, the minimum parity condition is:

`free mint + B + gas + risk premium >= price of an already-active level-1 NFT with comparable pending ETH`.

That inequality cannot be guaranteed by a contract because secondary NFT prices are external. At launch, `B` should be near the expected market premium for activation, and there should be a public dashboard showing activation cost, pending ETH, and the observed secondary floor. If a free mint plus cheap activation creates a much cheaper active position than secondary purchase, rational users mint (if allowlisted), divert demand from secondary holders, and inflate active count. If activation is too expensive, no one activates and fees backlog.

Levels should travel with the token ID while it is held externally. Exit must permanently clear the level before auction. An auction buyer receives a zero-level, zero-accrual NFT and must activate it afresh. The auction should not use “10x previous sale price” as an oracle: the previous price is trivially manipulable and a zero floor is a free-NFT giveaway. Use a fixed token-denominated reserve schedule or a commit/reveal auction with a nonzero reserve and a timeout; if no sale occurs, keep the NFT escrowed rather than promising “always sells.”

## Fee-income scenarios

Assume daily volume is total SPEPE swap notional, the proposed 2.5% is charged on each direction’s notional, 100% of that fee goes to the distributor, and volume is evenly split buys/sells. The gross distributor inflow is therefore `2.5% × daily volume`. At a 10% team cut, shown only as a sensitivity, distributable ETH is 90% of gross. ETH/USD is held at $2,700 solely to make the table readable.

| Daily volume | Gross fee/day | Gross USD/day | After 10% team cut | After-cut USD/day |
|---:|---:|---:|---:|---:|
| $10,000 | $250 | $250 | $225 | $225 |
| $50,000 | $1,250 | $1,250 | $1,125 | $1,125 |
| $200,000 | $5,000 | $5,000 | $4,500 | $4,500 |

For `N1`, `N2`, `N3` active NFTs at weights 1/2/4, a level-1 NFT’s daily share is `D/(N1+2N2+4N3)`, level 2 is twice that, and level 3 four times that. Example with 100/100/50 NFTs gives total weight 500:

| Daily volume | D after 10% cut | L1/day | L2/day | L3/day |
|---:|---:|---:|---:|---:|
| $10k | $225 | $0.45 | $0.90 | $1.80 |
| $50k | $1,125 | $2.25 | $4.50 | $9.00 |
| $200k | $4,500 | $9.00 | $18.00 | $36.00 |

At 300/300/150 active NFTs (1,500 total weight), divide those yields by three. At full collection activation with equal levels (roughly 1,667 each), total weight is about 11,669; at $50k/day and zero team cut, a level-1 position receives about $1.07/day, level 2 $2.14, level 3 $4.29. These are fee yields, not returns: SPEPE price, volume, gas, activation burn and NFT price can all move against the holder.

**Pressure loop.** Each activation buys and burns `B`, `3B` or the incremental amount needed for that level. Each auction purchase buys and burns the auction’s token price. Neither creates ETH; both are demand sinks funded by new or existing holders. If a holder exits and the auction buyer uses new token, there is temporary buy/burn pressure, but the NFT’s old economic position is reset. If fees are larger than the NFT’s market value, exit/re-buy can extract value and the loop becomes a transfer of ETH from later fee payers to arbitrageurs. Sustainable operation therefore requires recurring real swap volume and willing buyers; it is not self-sustaining merely because tokens burn.

## Main exploit and failure analysis

* **Exit/re-buy arbitrage:** If pending ETH plus level value exceeds the NFT’s market price, a holder can exit, receive ETH, and later acquire the reset NFT cheaply. Use a claim/exit cooldown, settle at a bounded epoch, and make auction reserve reflect only a published fixed schedule. Do not pretend this removes the economic arbitrage.
* **Floor sniping:** A nonlinear Dutch curve ending at zero is guaranteed to be sniped by bots. A 10x self-referential start is manipulable by one artificial prior sale. Use a reserve, commit/reveal, random close, or accept that the auction is a giveaway and model it as one.
* **Wash trading:** A 2.5% fee each way can be farmed if a trader’s expected distributor share exceeds 5% round-trip cost plus price impact and gas. Require a minimum volume/time lock only as a weak deterrent; the robust defense is lower fees, per-block/per-address caps, and treating volume as untrusted. Caps also reduce genuine liquidity.
* **Extra pools and routes:** The hook only sees its attached pool. A second pool, direct transfer, OTC trade, bridge, or aggregator route bypasses it. The token cannot force all ERC-20 transfers through the hook. Publish the canonical pool, monitor others, and never market the fee as universal.
* **Cheap new mints:** Because mint is currently gas-only and allowlisted, a newly minted NFT has zero weight until activation, but it can still be activated cheaply if `B` is too low. Enforce activation only by current owner, initialize debt at the current accumulator, and impose no retroactive share.
* **MEV around activation:** A user can buy SPEPE, activate, and sell around the same block; if activation changes weight before a fee accrual, ordering matters. Define accrual at the start/end of each call, use a minimum activation holding period, and avoid a public “activate then claim” bundle that can be copied. Private orderflow is not a protocol guarantee.
* **Reentrancy and accounting:** ETH sends, ERC-721 safe transfers, ERC-20 callbacks/nonstandard tokens, auction settlement, and hook callbacks create reentrancy surfaces. Use checks-effects-interactions, a reentrancy guard, pull payments, exact balance-delta checks, and invariant tests for conservation of ETH and weight.
* **Upgrade/admin risk:** An immutable fee cap is good, but the owner of the collection, the hook, and any distributor must be separately documented. Use immutable addresses where possible, a timelock for parameters, a pause that cannot confiscate pending ETH, and a recovery path for stuck NFTs.

## Is 2.5% each way appropriate?

No for launch. A 5% round trip is unusually punitive before LP fee, gas and price impact, and it makes wash trading profitable whenever the expected share exceeds that hurdle. It also encourages users to route around the canonical pool. I recommend 1.0% each way initially, with the ability to reduce (not increase) under an immutable maximum; test 0.5–1.0% against actual volume. A team cut should be zero at launch. If a team share is necessary, cap it at 5% of collected hook fees, stream it to a publicly identified multisig, and activate it only after a stated ETH reserve/audit threshold. A hard cap protects holders only if the recipient and withdrawal rules are also immutable and observable.

## Simpler and stronger variants

1. **Simplest:** a canonical v4 pool with 1% fee, ETH distributed pro rata to explicitly staked token IDs, one activation level, no auctions, and no team cut. Users can claim; they do not surrender NFTs. This removes the most dangerous state transitions.
2. **Bearer certificate:** keep three levels and weighted accounting by token ID, but remove exit and auction. The NFT is a transferable certificate; a buyer knowingly inherits its level and pending balance. This is compatible with the existing ERC-721 and ordinary marketplaces, subject to the claim-before-sale caveat.
3. **Escrowed position:** if exit/reset is core, require a protocol wrapper that holds the original NFT and issues a position token. All transfers of the position then go through a controlled ERC-721/ERC-1155 wrapper. This is more honest and enforceable, but changes UX and adds custody/approval risk.
4. **Use auctions only for voluntary exits:** let the exiting holder choose a reserve and sell through an audited marketplace-compatible escrow. Do not burn all proceeds automatically; burning creates a reflexive bid for SPEPE and makes valuation harder to reason about.

## Unanswered questions before any build

The exact v4 deployment, fee accounting convention for exact-output swaps, canonical token decimals/supply, intended SPEPE allocation and initial price, desired active-set size, team recipient governance, and legal/tax treatment of ETH distributions are not specified. These are decision inputs, not details an implementer should guess. The live collection’s allowlist/owner policy can also change while minting remains open.

## Final recommended parameter set

* One canonical Uniswap v4 pool; no claim that other venues are covered.
* 1.0% hook fee on each buy/sell, calculated on actual settled deltas; immutable maximum 1.0% and zero team cut at launch.
* Weights 1/2/4; immutable token-denominated cumulative activation burns `B/3B/8B`; no oracle-dependent activation requirement.
* Token-id accounting with `accPerWeight`, per-token debt, current-owner authorization, and a 30-day capped backlog stream when total weight is zero.
* Levels persist on ordinary transfers, but exit clears them; auction/reset is removed from v1. If retained later, use a nonzero reserve and commit/reveal, never a zero-floor “always sells” promise.
* Activation cooldown of at least one epoch (or 24 hours), no same-transaction activation/exit, and explicit per-call ordering rules.
* Audits plus invariant/fuzz tests for fee conservation, no retroactive activation rewards, no double claim, weight conservation, ETH solvency, and arbitrary ERC-721 transfers.

**Verdict:** realistic as a carefully constrained token-id dividend/staking experiment; unrealistic as a frictionless, universal-fee, self-calibrating, always-selling economic loop. It depends on continuing real trading and new capital, and the proposed 2.5%/2.5%, zero-floor auctions, and automatic exit/reset mechanics should be rejected for mainnet v1.

