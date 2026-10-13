# How Uniswap v4 hooks changed liquidity pools

*One-page summary · Sources checked 13 October 2026*

**Established facts.** A liquidity pool lets people swap tokens using funds supplied by liquidity providers. Uniswap v3 let providers choose price ranges and pools with fixed swap fees. V4 added hooks: separate programs on the blockchain that a pool can call before or after actions such as a swap or adding or removing funds. Developers can now build custom behavior into those moments. The v4 whitepaper describes features that previously required a separate implementation of the core protocol. [Source: Uniswap v4 Core, August 2024, introduction and §2](https://app.uniswap.org/whitepaper-v4.pdf).

Hooks are optional; a pool without one retains v3-style concentrated liquidity. Each pool has at most one hook address, chosen when it is created, which cannot later be replaced for that pool. The hook implements the actions it needs, rather than every possible action. [Source: Uniswap developer documentation, Hooks](https://developers.uniswap.org/docs/protocols/v4/concepts/hooks).

**Three concrete examples**

1. **Change the trading fee as conditions change — documented capability.** A hook could raise the fee when prices become more volatile and lower it when conditions settle. V4 supports updating the liquidity-provider fee over time or setting it separately for each swap in a pool configured for dynamic fees. This changes what traders pay without making them move to another fixed-fee pool. Better provider returns are a possible benefit, not an established result for every strategy. [Source: Uniswap developer documentation, Dynamic Fees](https://developers.uniswap.org/docs/protocols/v4/concepts/dynamic-fees).

2. **Spread a large trade over time — published sample design.** Uniswap Labs described a time-weighted average market maker (TWAMM) hook: a user deposits an order and chooses its duration, allowing a treasury sale, for example, to be divided into smaller trades. In that design, subsequent swaps or liquidity actions trigger settlement of outstanding timed orders; the hook does not run itself on a clock. Spreading execution aims to reduce how much the order moves the price. The August 2023 article explicitly says the design was still being developed, so it does not establish current deployment or guaranteed savings. [Source: Uniswap Labs, Uniswap v4 TWAMM Hook](https://blog.uniswap.org/v4-twamm-hook).

3. **Convert an asset through the pool interface — published implementation.** Uniswap Labs’ WETHHook wraps ETH into WETH, its token representation, and unwraps it at a one-to-one rate with zero swap fees; network transaction costs still apply. This illustrates a pool doing asset conversion. The whitepaper explains how hooks can supply their own token accounting and bypass the usual trading-price model. [Sources: Uniswap Labs hook repository](https://github.com/Uniswap/v4-hooks-public#hooks), [v4 Core, §5](https://app.uniswap.org/whitepaper-v4.pdf).

**Inference.** Hooks make a pool a place to program trading and asset-handling rules while using v4’s shared infrastructure. These examples are choices developers implement, not features every v4 pool automatically receives.

**Uncertainty and unanswered questions.** This research establishes capabilities and published designs, not safety or performance of a particular deployed hook. Which code and upgrade controls does a chosen pool use? Does its strategy improve execution or provider returns after fees and transaction costs? Answering those requires deployment-specific review and measured results, neither performed here.
