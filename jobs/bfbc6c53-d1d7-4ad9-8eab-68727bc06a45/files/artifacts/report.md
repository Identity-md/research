# Why Uniswap v4 matters: what its architecture enables that v3 could not

*Technical research report. Research date: 2026-09-25. Code citations are pinned to specific commits (listed in [References](#references)).*

---

## How to read this report

Each substantive claim carries a tag:

| Tag | Meaning |
|---|---|
| **[F]** | **Fact.** Directly supported by the cited primary source: source code, specification, whitepaper, official docs, or a first-party post-mortem. |
| **[R]** | **Reported.** A claim made by a third party (auditor, competitor, news outlet) that this report did not independently verify. Where the source has a commercial interest, that is noted. |
| **[I]** | **Inference.** The author's reasoning from the facts. It may be wrong. |
| **[U]** | **Uncertain / open.** The evidence is missing, disputed, or still changing. |

Bracketed numbers such as [1] refer to the numbered [References](#references).

---

## Executive summary

**Question.** What does Uniswap v4's architecture make possible that Uniswap v3's architecture could not?

**Short answer.** v4 makes three structural changes. Taken together, they turn Uniswap from a fixed AMM product into a settlement layer that third parties can program.

1. **One contract holds every pool, and balances are settled once per transaction ("flash accounting").** In v4 every pool is a storage entry inside one `PoolManager` contract [F][2][5]. Inside a single `unlock` callback, a caller can run any sequence of swaps, liquidity changes, donations, `take`s and `settle`s across any pools. Only the *net* per-token balance ("delta") has to reach zero before the callback returns [F][2][3]. Those deltas live in EIP-1153 transient storage, which costs 100 gas per access and is wiped at the end of the transaction [F][9]. The whitepaper says this design became affordable only after the Cancun fork [F][1]. The result is that an N-hop swap needs only two real token transfers, one for the input token and one for the output [F][6]. Integrators, not pools, now decide when to pay. In v3, each pool was its own contract, and every pool call had to be paid for in that pool's callback [F][4][14].
2. **Hooks.** A pool creator can attach an external contract that the `PoolManager` calls at up to 10 lifecycle points. Four further permissions let the hook return its own balance deltas ("custom accounting") [F][1][5]. Which callbacks run is decided by 14 low-order bits of the hook's *address*, and it is fixed for the life of the pool [F][5][7]. This lets outside developers build things that v3 could only get by forking the protocol: dynamic fees, on-chain limit orders, TWAMM, custom or non-concentrated-liquidity curves, custom oracles, and MEV-mitigation schemes [F][1]. Each now has public reference or production code (§3.4).
3. **Rules that v3 fixed are now per-pool choices.** Fee tiers and tick spacings are no longer set by governance [F][1]. Fees can be any static value or fully dynamic [F][8][12]. Native ETH is supported [F][1]. The v3 built-in oracle has been removed from the base pool, which the whitepaper says saves about 15k gas on the first swap in each block [F][1].

**The cost.** Hooks move a lot of trust and security work away from Uniswap's audited core and onto each hook developer, and then onto the routers and users who touch those hooks.
- Two hook-based protocols, Cork (May 2025) and Bunni (September 2025), lost a combined ~$20M. Neither loss came from a bug in v4-core [F][17][18][R][16][20].
- In September 2026, DEX aggregator 0x said that 54.2% of 84,163 deployed hooks it analysed were malicious ("quote spoofing"). Uniswap's founder disputed what this means [R][21][22].
- Liquidity can split across unlimited pools per token pair, and it is unclear who should curate which hooks get routed to (§4.6, §5) [I][U].

**Verdict [I].** v4's core advance is architectural and real. It makes AMM customisation cheap, composable and permissionless, where v3 made it impossible without a fork. But v4 does not make custom pools *safe*. It gives safety to the core and hands the risk of each hook to the market. Whether that trade pays off depends on hook-review and routing infrastructure, which is still being built and argued over (§5).

---

## 1. Baseline: what v3's architecture fixed in place

These properties of v3 are the constraints v4 removes:

- **One contract per pool.** `UniswapV3Factory.createPool` deploys a new `UniswapV3Pool` contract with `CREATE2` for each (token0, token1, fee) combination [F][14]. Each pool holds its own token balances. Because contract creation is gas-heavy, creating a pool is expensive [F][6].
- **Payment is checked per pool.** `UniswapV3Pool.swap` sends the output token, calls `uniswapV3SwapCallback`, and then checks that its own balance went up by the amount owed (`require(balance0Before.add(...) <= balance0(), 'IIA')`) [F][14]. A multi-hop route therefore moves the intermediate token out of one pool contract and into the next. In the ETH→USDC→DAI example in Uniswap's docs, the USDC is transferred between pool contracts [F][6].
- **Flash loans existed, but one pool at a time and for a fee.** v3 already had per-pool flash swaps and `flash()` with a fee equal to the pool's swap fee [F][14]. v4's advance is *not* "flash loans exist". It is that one ledger covers every pool and token at once (§2.3).
- **Features and parameters were fixed by the protocol.** v3 allowed only fee tiers that the factory owner (governance) had enabled through `enableFeeAmount`. The defaults were 0.05%, 0.30% and 1.00% [F][14][8]. The v3 whitepaper put a TWAP oracle into every pool, and swappers paid for it whether or not anyone used it [F][1][15]. The v4 whitepaper says that TWAMM, volatility oracles, limit orders and dynamic fees "require reimplementations of the core protocol, and can not be added to Uniswap v3 by third-party developers" [F][1].
- **No native ETH.** v2 and v3 pools required ETH to be wrapped into WETH [F][1].

---

## 2. Singleton `PoolManager` and flash accounting

### 2.1 Mechanism (from the code)

- **Pools are storage entries, not contracts.** The v4-core README says: "v4-core uses a singleton-style architecture, where all pool state is managed in the `PoolManager.sol` contract" [F][2]. A pool is identified by its `PoolKey`: `currency0, currency1, fee, tickSpacing, hooks` [F][5]. Creating one is a call to `PoolManager.initialize(key, sqrtPriceX96)`, which writes storage and deploys no bytecode [F][5].
- **Unlock and callback.** State-changing pool operations carry the `onlyWhenUnlocked` modifier. `unlock` works as follows [F][5]:

  ```solidity
  // v4-core src/PoolManager.sol (pinned commit 46c6834), lines ~104-113
  function unlock(bytes calldata data) external override returns (bytes memory result) {
      if (Lock.isUnlocked()) AlreadyUnlocked.selector.revertWith();
      Lock.unlock();
      // the caller does everything in this callback, including paying what they owe via calls to settle
      result = IUnlockCallback(msg.sender).unlockCallback(data);
      if (NonzeroDeltaCount.read() != 0) CurrencyNotSettled.selector.revertWith();
      Lock.lock();
  }
  ```

  Inside `unlockCallback`, the caller can call `swap`, `modifyLiquidity`, `donate`, `take`, `settle`, `sync`, `clear`, `mint` and `burn` in any order and as many times as it likes. Each call adjusts a per-(caller, currency) delta. The transaction reverts unless the count of non-zero deltas is back to zero when the callback returns [F][2][5].
- **The deltas live in transient storage.** `NonzeroDeltaCount` and the per-currency deltas are read and written with `tload`/`tstore` [F][5]. EIP-1153 prices `TSTORE` and `TLOAD` at 100 gas each, and "all values in transient storage are discarded at the end of the transaction" [F][9].
- **Why it needed Cancun.** The whitepaper explains that before the Cancun hard fork, "the flash accounting architecture was expensive because it required storage updates at every balance change." Even storage that was set and then cleared within the transaction hit the EIP-3529 refund cap [F][1][9].
- **Borrowing inside an unlock is free at the core level.** `take()` records a negative delta and transfers tokens. It charges no fee [F][5]. The caller only has to settle the delta before the unlock ends. [I] v3 charged a flash fee per pool; v4-core does not, although a hook or periphery contract could add one.

### 2.2 Gas: what is sourced and what is not

| Claim | Source | Status |
|---|---|---|
| Pool deployment is "99% cheaper" than under the factory model | v4 whitepaper §3 [1] | **[R]** First-party claim. This report did not benchmark it. |
| An N-hop swap needs only 2 token transfers (input and output) | Uniswap docs, flash accounting [6] | **[F]** Follows from the code in [5]. |
| `TSTORE` and `TLOAD` cost 100 gas | EIP-1153 [9] | **[F]** |
| A native ETH transfer costs about 21k gas, versus about 40k for an ERC-20 transfer | v4 whitepaper §4 [1] | **[R]** Rough, first-party figures |
| Removing the built-in oracle saves about 15k gas on the first swap in a pool per block | v4 whitepaper §6.3 [1] | **[R]** First-party |

**[U]** This report did not find or run an independent, like-for-like benchmark of v3 and v4 end-to-end swap gas. Actual savings depend on route length, token implementations, and the hooks involved. A hook can *add* arbitrary gas.

### 2.3 What this enables that v3 could not

1. **Atomic multi-pool composition with one net settlement [F][1][6].** Consider "swap ETH→USDC→DAI, then add ETH/DAI liquidity, then take the leftover". In v4 this is one unlock with one payment per token. In v3 the same flow needs a transfer and a balance check at every pool.
2. **Flash-style borrowing of any token held anywhere in the singleton [F][1][5].** The whitepaper says a caller "can … access any of its tokens, as long as no tokens are owed to or from the caller by the end of the lock." In v3, one pool could lend only its own two tokens.
3. **Balances held inside the protocol (ERC-6909) [F][1].** Users and hooks can `mint` a claim token instead of withdrawing an ERC-20. This skips repeated transfers for frequent traders and market makers.
4. **A cheaper cost of fragmentation [F][1].** The whitepaper argues that singleton plus flash accounting reduce "the cost of liquidity fragmentation", which matters because hooks "will greatly increase the number of pools". See §4.6 for the counter-argument.

### 2.4 What changes for integrators

- **[F]** Routers and position managers must implement `IUnlockCallback`, track deltas, and settle correctly: `sync` then transfer then `settle` to pay, `take` to receive, or `mint`/`burn` for 6909 claims [F][2][5][6]. The code notes that "if settling native, integrators should still call `sync` first to avoid DoS attack vectors" [F][5].
- **[F]** Only one unlock can be active at a time (`AlreadyUnlocked`). All composition therefore happens inside a single callback frame, or through hooks called from within it [F][5].
- **[F]** Positions can carry a `salt`, so two positions on the same range stay separate. v4 `PositionManager` also supports *subscribers*, which receive notifications for staking without transferring the NFT [F][6].
- **[I]** A wider range of mistakes is now possible. The Uniswap Foundation's framework lists "flash accounting and transient state risks" as "a hook-specific risk vector not present in previous Uniswap versions" [F][12].

---

## 3. Hooks

### 3.1 Lifecycle callbacks

The v4-core README lists these callbacks: `{before,after}Initialize`, `{before,after}AddLiquidity`, `{before,after}RemoveLiquidity`, `{before,after}Swap`, `{before,after}Donate` [F][2]. The whitepaper calls them "ten such hook callbacks" [F][1].

| Callback | When it runs | Typical use |
|---|---|---|
| `beforeInitialize` / `afterInitialize` | Once, when the pool is created | Check the PoolKey (for example, require a dynamic fee), set up state |
| `beforeAddLiquidity` / `afterAddLiquidity` | On each liquidity increase | Access control, anti-JIT bookkeeping, liquidity mining |
| `beforeRemoveLiquidity` / `afterRemoveLiquidity` | On each liquidity decrease | Withdrawal fees and JIT penalties. Also a liveness risk (§4.4) |
| `beforeSwap` / `afterSwap` | Around each swap | Dynamic fees, order execution, gating, oracle updates, custom curves |
| `beforeDonate` / `afterDonate` | Around `donate()` | Custom tipping or fee-distribution logic |

There are also **four return-delta permissions**: `beforeSwapReturnDelta`, `afterSwapReturnDelta`, `afterAddLiquidityReturnDelta` and `afterRemoveLiquidityReturnDelta`. They let a hook return balance deltas that are debited from or credited to the user and credited to or debited from the hook [F][1][7]. The whitepaper calls this **custom accounting**. It lets a hook "forgo the concentrated liquidity model entirely, creating custom curves" [F][1]. If a `BeforeSwapDelta` uses up the whole specified amount, the core concentrated-liquidity math is skipped. The docs call this a **NoOp swap** [F][12]. The code caps this: a hook delta may not flip an exact-input swap into exact-output or the reverse (`HookDeltaExceedsSwapAmount`) [F][7].

### 3.2 How the hook address encodes its permissions

From `Hooks.sol` [F][7]:

| Bit | Flag | Bit | Flag |
|---|---|---|---|
| 13 | `BEFORE_INITIALIZE` | 6 | `AFTER_SWAP` |
| 12 | `AFTER_INITIALIZE` | 5 | `BEFORE_DONATE` |
| 11 | `BEFORE_ADD_LIQUIDITY` | 4 | `AFTER_DONATE` |
| 10 | `AFTER_ADD_LIQUIDITY` | 3 | `BEFORE_SWAP_RETURNS_DELTA` |
| 9 | `BEFORE_REMOVE_LIQUIDITY` | 2 | `AFTER_SWAP_RETURNS_DELTA` |
| 8 | `AFTER_REMOVE_LIQUIDITY` | 1 | `AFTER_ADD_LIQUIDITY_RETURNS_DELTA` |
| 7 | `BEFORE_SWAP` | 0 | `AFTER_REMOVE_LIQUIDITY_RETURNS_DELTA` |

- `ALL_HOOK_MASK = (1 << 14) - 1`. The source comment gives an example: a hook deployed at `0x…2400` has bits 13 and 10 set, so it runs `beforeInitialize` and `afterAddLiquidity` [F][7].
- `isValidHookAddress` rejects any address where a return-delta flag is set without its matching action flag. It also requires a non-zero hook to have at least one flag or a dynamic fee [F][7].
- Developers therefore **mine a `CREATE2` salt** (for example with `HookMiner`) until the deployed address carries the right bits. If the address lacks a flag, "the `PoolManager` never calls that hook function, so the logic silently does nothing" [F][10].
- **Why it was designed this way [F][1].** Reading permissions from the address is gas-efficient because no external call is needed. It also "ensures that even upgradeable hooks obey certain invariants". The *set* of callbacks is fixed by the address, even if the code behind the address changes. Separate add and remove permissions exist because "hooks that can affect minting but not burning of liquidity are safer for liquidity providers, since they are guaranteed to be able to withdraw their liquidity" [F][1].
- **Immutable binding [F][10].** The hook is part of the `PoolKey`. It "cannot be added, removed, or swapped afterward". To change it you create a new pool.
- **Self-calls are skipped [F][7][13].** Callbacks are skipped when the hook itself is the caller (`noSelfCall`, `msg.sender == address(self)` checks). OpenZeppelin warns that this can cause subtle bugs in hooks that swap internally [F][13].

### 3.3 Dynamic fees: the mechanism

- **[F]** A pool opts in at creation by setting `fee = DYNAMIC_FEE_FLAG (0x800000)`. The choice cannot be changed later [F][7][8].
- **[F]** There are two ways to update the fee [F][5][8]:
  1. The hook calls `PoolManager.updateDynamicLPFee(key, fee)`. The call reverts unless `msg.sender == key.hooks` and the pool is dynamic.
  2. `beforeSwap` returns a per-swap fee with `OVERRIDE_FEE_FLAG (0x400000)` set.
- **[F]** The maximum LP fee is 100% (`MAX_LP_FEE = 1_000_000` pips) [F][7]. The protocol-fee cap is 0.1% (`MAX_PROTOCOL_FEE = 1000` pips) [F][5]. v3 allowed only the tiers governance had enabled [F][14].

### 3.4 New pool behaviours, each with a concrete example

"Reference" means example code published by Uniswap Labs or OpenZeppelin. "Production" means a deployed third-party protocol. The existence of the code is a **[F]**. How well a design works economically is **[U]** unless stated.

| Behaviour | Why v3 could not do it | Concrete example | Hook points used |
|---|---|---|---|
| **Dynamic fees** | Fees were fixed per pool, from a governance-set menu [14] | *Reference:* Uniswap's early `VolatilityOracle.sol`. It requires a dynamic-fee pool in `beforeInitialize` and calls `updateDynamicLPFee`. Its fee formula ("100 bps a minute") is a placeholder, not a real volatility model [F][11]. OpenZeppelin ships `BaseDynamicFee`, `BaseOverrideFee` and `BaseDynamicAfterFee` [F][13]. *Production:* Angstrom's `beforeSwap` returns a fee with `OVERRIDE_FEE_FLAG` set [F][19]. | `beforeInitialize`, `afterInitialize`/`beforeSwap` |
| **On-chain limit orders** | No execution hook when the price crosses a tick | *Reference:* Uniswap's `LimitOrder.sol` (uses `afterSwap`) [F][11]. OpenZeppelin `LimitOrderHook` places one-sided liquidity at a tick not yet crossed and fills it "if the pool's price crosses the order's tick" [F][13]. | `afterInitialize`, `afterSwap` |
| **TWAMM** (large orders spread over time) | Needed a fork of the core [1] | *Reference:* Uniswap's `TWAMM.sol` runs outstanding long-term orders in `beforeSwap` (`_executeTWAMMOrders`) [F][11]. It is based on Paradigm's TWAMM design [1]. | `beforeInitialize`, `beforeSwap`, liquidity hooks |
| **Custom AMM curves / non-CL liquidity** | v3 was concentrated liquidity only [1] | *Reference:* OpenZeppelin `BaseCustomCurve` performs NoOp swaps through `BeforeSwapDelta` [F][12][13]. The whitepaper cites "Uniswap v2 on Uniswap v4" as an example [F][1]. *Production:* Bunni v2, a hook with custom liquidity-distribution functions [F][18]. It was also exploited (§4.2). | `beforeSwap` + `beforeSwapReturnDelta`, liquidity return-deltas |
| **Custom oracles** | v3 had one enshrined TWAP oracle that every swapper paid for [1][15] | *Reference:* Uniswap's `GeomeanOracle.sol`, a full-range, zero-fee oracle pool with locked liquidity [F][11]. The whitepaper also mentions "median, truncated, or other custom oracle implementations" [F][1]. | `beforeInitialize`, `beforeSwap`, liquidity hooks |
| **MEV mitigation / MEV internalisation** | No per-swap control over ordering, pricing or fees | *Production:* Sorella's **Angstrom**. `UnlockHook.beforeSwap` reverts with `CannotSwapWhileLocked` unless the pool has been unlocked for the block by an attested Angstrom node's signed payload, and sets the fee [F][19]. *Reference:* OpenZeppelin `AntiSandwichHook` ensures no swap in a block fills better than the price at the start of the block (in one direction only) [F][13]. `LiquidityPenaltyHook` penalises just-in-time LPs [F][13]. The whitepaper's citation for MEV internalisation is the am-AMM paper [1][23]. | `beforeSwap`, `afterSwap`, `afterAdd/RemoveLiquidity` |

The oracle, TWAMM, limit-order and volatility examples are from Uniswap Labs' early `v4-periphery`. They were removed from the repository in July 2024 ("Clean up repo (#159)") [F][11]. They should be read as design demonstrations, not audited production code [I].

---

## 4. Trade-offs and risks

### 4.1 The trust boundary moves outward

- **[F]** Uniswap describes the core as "non-custodial, non-upgradeable, and permissionless" [1]. The core was reviewed by several firms. The v4-core repository holds reports from ABDK, Certora, Spearbit (the latter two marked draft), OpenZeppelin and Trail of Bits [F][2]. Uniswap Labs says there were nine audits, a $2.35M security competition and a $15.5M bug bounty, with no critical bugs found [R][24]. This is a first-party announcement.
- **[F]** None of that assurance covers hooks. The Uniswap Foundation's security framework says it "does not review, audit, or certify any submissions" [12]. Trail of Bits: "hook developers secure the application-specific logic they add" [F][16]. The Uniswap docs: "just because you made a hook, that does not mean you will get liquidity routed to your hook from the Uniswap frontend" [F][10].
- **[I]** A v4 pool is therefore only as safe as its hook, the hook's upgrade keys, and any external contracts the hook calls. LPs and swappers now have to evaluate those as well as the Uniswap brand. In v3, every pool ran the same audited bytecode.

### 4.2 Buggy hooks: documented losses

| Incident | Date | Loss | Root cause (per sources) | Was v4-core at fault? |
|---|---|---|---|---|
| **Cork Protocol** | 2025-05-28 | ≈ $11–12M | `CorkHook.beforeSwap` had no `onlyPoolManager` check, so "anyone can call it directly with arbitrary parameters". There was also no validation of pool ID or hook address, and a separate pricing flaw [F/R][17] | No. The hook was missing access control |
| **Bunni v2** | 2025-09-02 | ≈ $8.4M (USDC/USDT on Ethereum, weETH/ETH on Unichain) | A rounding direction in `BunniHubLogic::withdraw()` that was safe for a single call became exploitable across many tiny withdrawals. Team: "A rounding direction that's safe in the context of a single operation may not be safe in the context of multiple operations" [F][18] | No. The bug was in the hook protocol's accounting |

- **[F]** Trail of Bits (July 2026) lists seven recurring classes of hook bugs: unauthorised callers, untrusted pool selection, accounting errors, callback-timing errors, address/permission mismatches, callback reverts that block exits, and state changes across callbacks. It notes that Cork and Bunni "account for more than $20M in losses" [16].
- **[R]** An early BlockSec study (November 2023, before launch) found that 8 of 22 (36%) hook projects in the "awesome-uniswap-hooks" list were vulnerable, mostly because of flawed access control [20]. The sample is small and pre-launch, so treat it as indicative only.

### 4.3 Malicious hooks and "quote spoofing"

- **[R]** 0x, a competing DEX aggregator, published "Uniswap v4 hooks were a mistake" on 2026-09-14. It says that of 84,163 hooks across six chains (snapshot 2026-09-11), 54.2% were classified malicious, 26.4% likely malicious and 19.4% safe. The mechanism it describes is a hook that returns an attractive quote during the router's simulation and then delivers up to 50% less at execution [21].
- **[R]** Uniswap founder Hayden Adams pushed back, according to secondary reporting. He argued that malicious contracts exist in every permissionless system and are "not a design flaw", and noted that the Uniswap API only integrates reviewed hooks [22]. This report could not retrieve his primary statement.
- **[F]** The mechanism is technically possible. Hooks with `beforeSwap` and return-delta or fee-override permissions can change pricing at execution time [7][8]. The Uniswap Foundation framework itself warns: "Fees can be raised selectively after seeing a user's trade" [12].
- **[U]** The *percentages* are hard to interpret. Most of the 84k "hooks" may be spam or deployments with no liquidity, not places where users actually trade. 0x's classification method and false-positive rate are not independently audited, and 0x competes with Uniswap on routing. The volume-weighted share of harm is not established by these sources.

### 4.4 Liveness: hooks can lock LPs in

- **[F]** The whitepaper itself says that splitting add and remove permissions exists so that LPs can be "guaranteed to be able to withdraw" when a hook lacks `beforeRemoveLiquidity` [1]. The inverse follows: a hook *with* remove-liquidity callbacks (or return-deltas) can revert, charge fees on, or otherwise block withdrawals. Trail of Bits lists "callback failures blocking exits" as a bug class [16].
- **[I]** LPs should check the address flags before depositing. Bits 8, 9 and 0 are the ones that matter for exit safety.

### 4.5 Immutability versus upgradeability

- **[F]** The hook address bound to a pool and its permission bits are fixed [1][10]. The core is not upgradeable [1].
- **[F]** The *code* behind a hook address can still be upgradeable through a proxy. The Uniswap Foundation calls upgradeability a "major" risk: "many real-world exploits stem not from logic bugs, but from unsafe upgrade paths, compromised keys, or storage layout mistakes". It advises teams to "prefer immutability" or "deploy new hook contracts (v1 -> v2)" [12]. BlockSec pointed to upgradeable proxies and `selfdestruct` plus `CREATE2` redeployment as malicious-hook patterns [R][20].
- **[I] The tension.** An immutable hook cannot be patched: Cork and Bunni both needed migrations. An upgradeable hook asks LPs to trust an admin key. Because the hook is part of the `PoolKey`, fixing an immutable hook means moving liquidity to a new pool, which splits liquidity further (§4.6).

### 4.6 Liquidity fragmentation

- **[F]** v3 allowed one pool per (pair, enabled fee tier) [14]. In v4 the `PoolKey` includes `hooks`, `fee` and `tickSpacing` [5], so any pair can have an unlimited number of pools.
- **[F]** The whitepaper argues that singleton plus flash accounting *reduce the cost* of this fragmentation by making multi-pool routes cheaper [1].
- **[I] The counter-argument.** Cheaper routing across pools does not create depth. Liquidity split across many hook pools still gives each pool less depth. And routers must now judge hook safety as well as price, as 0x's report and Uniswap's reviewed-hooks policy both show [21][22]. Trail of Bits and the Uniswap Foundation also flag multi-hop routes that call the same hook several times as a source of value leakage [12][16].
- **[U]** This report found no rigorous, independent measurement of how v4 liquidity is actually spread across hook and non-hook pools compared with v3.

### 4.7 Audit burden and who bears it

- **[F]** The Uniswap Foundation's framework scores hooks from 0 to 33 on complexity, custom math, external dependencies, TVL potential, upgradeability and other factors. For high-risk hooks it recommends multiple audits, math-specialist review, monitoring and formal verification [12].
- **[I]** This cost falls on every hook team separately. Many small teams will ship lightly reviewed code. The docs even present hooks as a way to "drive down your audit costs" by building on a shared codebase [10]. That holds for the core but not for the hook's own logic, which is where both documented losses happened.

### 4.8 Trade-offs inside the "good" use cases

- **[F]** OpenZeppelin's `AntiSandwichHook` warns that it protects only one swap direction. It also warns that because it makes MEV unprofitable, "prices at beginning of the block [are] not necessarily close to market price", and that its tick loop can run out of memory [13].
- **[F]** `LiquidityPenaltyHook` warns that in low-liquidity pools, attackers using several accounts can get around it [13].
- **[I]** Angstrom-style gating moves MEV protection into an off-chain node network. Swaps revert unless an attested node unlocks the pool [19]. This swaps miner or builder trust for trust in that network. Whether that is a better trust model is a judgement call.
- **[F]** Dynamic fees add their own manipulation risks, such as fee changes after a trade is seen, non-linear fees, and new MEV routes. The framework calls for adversarial modelling [12].

---

## 5. Open questions

1. **[U] Who curates hooks, and how?** If routers such as the Uniswap API and 0x each keep private allowlists, permissionless hooks become permissioned in practice at the routing layer. It is unclear whether a shared, credible reputation or attestation system will emerge.
2. **[U] How much economic harm do malicious hooks do, weighted by volume?** The 84k-hook headline and the "reviewed hooks only" rebuttal are both unaudited, and they measure different things.
3. **[U] Do dynamic-fee and MEV-internalising hooks improve LP returns net of costs?** The docs list motivations such as volatility pricing and order-flow discrimination [8], and am-AMM gives theory [23]. This report found no independent, large-sample empirical result.
4. **[U] What are the real end-to-end gas savings over v3,** once typical routes and hook gas are counted? First-party numbers exist [1]. Independent benchmarks were not found.
5. **[U] Do upgradeable hooks with timelocks or immutable versioned hooks win in practice,** and how often will immutable hooks force liquidity migrations?
6. **[U] Does fragmentation across hook pools reduce effective depth** compared with v3's few pools per pair, or does routing across pools make up for it?

---

## 6. Summary: v3 versus v4

| Capability | v3 | v4 |
|---|---|---|
| Pool creation | New contract per pool [14] | Storage entry in singleton; first-party claim of 99% cheaper [1] |
| Multi-hop settlement | Transfer at every hop, checked per pool [14] | Net deltas and 2 transfers total [5][6] |
| Flash borrowing | Per-pool, fee = pool fee [14] | Any token in the singleton, no core fee, settled by end of unlock [5] |
| Fee structure | Governance-enabled tiers [14] | Any static fee or hook-controlled dynamic fee [7][8] |
| Custom logic | Only by forking [1] | Hooks with 14 permission bits, including custom accounting [7] |
| Oracle | Enshrined, paid by all swappers [15] | Optional, hook-implemented [1] |
| Native ETH | No (WETH) [1] | Yes [1] |
| Security surface | Uniform audited pool bytecode | Audited core plus arbitrary per-pool hook code [12][16] |

---

## Methodology and limitations

- **Sources read directly.** v4-core source (`PoolManager.sol`, `Hooks.sol`, `LPFeeLibrary.sol`, `NonzeroDeltaCount.sol`, `ProtocolFeeLibrary.sol`, README), v3-core source, the v4 whitepaper PDF (text extracted locally), EIP-1153, Uniswap developer docs pages, the Uniswap Foundation security framework, OpenZeppelin `uniswap-hooks` source, Sorella's Angstrom source, the historical `v4-periphery` example hooks, and the Bunni post-mortem.
- **Sources read through summarisation.** Several third-party pages (Dedaub, Trail of Bits, BlockSec, 0x, Crypto Briefing) were read through an automated fetch-and-summarise tool. Quotations from them are as the tool returned them. Figures from them are marked **[R]** unless a primary source confirms them.
- **Not retrieved.** Cork's own post-mortem returned HTTP 403, so its details rely on Dedaub [17]. The v4-core `Known_Effects_of_Hook_Permissions.pdf` could not be text-extracted, so it is not relied on. Hayden Adams's primary statement was not found.
- **No independent measurements.** No gas benchmarks, on-chain liquidity measurements, or hook-classification checks were performed.
- **Moving target.** Hook ecosystems, incidents and router policies change fast. Figures are as of the dates stated.

---

## References

Code links are pinned to the commits retrieved on 2026-09-25.

1. Adams, H., Salem, M., Zinsmeister, N., Reynolds, S., Adams, A., Pote, W., Toda, M., Henshaw, A., Williams, E., Robinson, D. *Uniswap v4 Core* (whitepaper), August 2024. https://github.com/Uniswap/v4-core/blob/46c6834698c48bc4a463a86d8420f4eb1d7f3b75/docs/whitepaper/whitepaper-v4.pdf
2. Uniswap, `v4-core` README (Architecture) and `docs/security/audits/` directory. https://github.com/Uniswap/v4-core/blob/46c6834698c48bc4a463a86d8420f4eb1d7f3b75/README.md ; https://github.com/Uniswap/v4-core/tree/46c6834698c48bc4a463a86d8420f4eb1d7f3b75/docs/security/audits
3. Uniswap developer docs, *v4 vs v3*. https://developers.uniswap.org/docs/protocols/v4/concepts/v4-vs-v3
4. Uniswap v3 Core whitepaper (Adams, Zinsmeister, Salem, Keefer, Robinson, 2021). https://uniswap.org/whitepaper-v3.pdf
5. Uniswap, `v4-core/src/PoolManager.sol` (`unlock` L104, `take` L291, `settle` L300, `updateDynamicLPFee` L339), `libraries/NonzeroDeltaCount.sol`, `libraries/ProtocolFeeLibrary.sol`. https://github.com/Uniswap/v4-core/blob/46c6834698c48bc4a463a86d8420f4eb1d7f3b75/src/PoolManager.sol
6. Uniswap developer docs, *Flash Accounting*. https://developers.uniswap.org/docs/protocols/v4/concepts/flash-accounting
7. Uniswap, `v4-core/src/libraries/Hooks.sol` (flags L29–47, `isValidHookAddress` L109, `noSelfCall` L171) and `LPFeeLibrary.sol` (`DYNAMIC_FEE_FLAG`, `OVERRIDE_FEE_FLAG`, `MAX_LP_FEE`). https://github.com/Uniswap/v4-core/blob/46c6834698c48bc4a463a86d8420f4eb1d7f3b75/src/libraries/Hooks.sol ; https://github.com/Uniswap/v4-core/blob/46c6834698c48bc4a463a86d8420f4eb1d7f3b75/src/libraries/LPFeeLibrary.sol
8. Uniswap developer docs, *Dynamic Fees*. https://developers.uniswap.org/docs/protocols/v4/concepts/dynamic-fees
9. Akhunov, A., Salem, M. *EIP-1153: Transient storage opcodes*. https://eips.ethereum.org/EIPS/eip-1153
10. Uniswap developer docs, *Hooks* (concepts and FAQ). https://developers.uniswap.org/docs/protocols/v4/concepts/hooks
11. Uniswap, `v4-periphery` example hooks (`TWAMM.sol`, `LimitOrder.sol`, `GeomeanOracle.sol`, `VolatilityOracle.sol`, `FullRange.sol`) at commit 087a262 (the parent of removal commit f242024, 2024-07-18). https://github.com/Uniswap/v4-periphery/tree/087a262e3cfdc0989cdb0b2a4194c340ec0ac063/contracts/hooks/examples
12. Uniswap Foundation / Uniswap developer docs, *Security Framework* (hook risk classes and scoring). https://developers.uniswap.org/docs/protocols/v4/security ; https://github.com/uniswapfoundation/security-framework
13. OpenZeppelin, `uniswap-hooks` library (`src/general/LimitOrderHook.sol`, `AntiSandwichHook.sol`, `LiquidityPenaltyHook.sol`, `src/base/BaseCustomCurve.sol`, `src/fee/*`). https://github.com/OpenZeppelin/uniswap-hooks/tree/80bd72492bb373c67d1e37d179f42a19b89e2440/src
14. Uniswap, `v3-core` contracts: `UniswapV3Factory.sol` (fee tiers, `enableFeeAmount`), `UniswapV3PoolDeployer.sol` (CREATE2 per pool), `UniswapV3Pool.sol` (`swap` L596, `flash` L791). https://github.com/Uniswap/v3-core/tree/d0831dc6b8a318df3872b6d68f6de135c9f3ec29/contracts
15. Uniswap v3 Core whitepaper §5 (oracle). See [4].
16. Trail of Bits, *Building secure Uniswap v4 hooks*, 2026-07-30. https://blog.trailofbits.com/2026/07/30/building-secure-uniswap-v4-hooks/
17. Dedaub, *The $11M Cork Protocol Hack: A Critical Lesson in Uniswap V4 Hook Security*. https://dedaub.com/blog/the-11m-cork-protocol-hack-a-critical-lesson-in-uniswap-v4-hook-security/ (Cork's own post-mortem, https://www.cork.tech/blog/post-mortem, was not retrievable.)
18. Bunni, *Exploit Post Mortem* (Bunni Diaries). https://blog.bunni.xyz/posts/exploit-post-mortem/ ; source: https://github.com/Bunniapp/bunni-v2
19. Sorella Labs, Angstrom source, `contracts/src/modules/UnlockHook.sol`. https://github.com/SorellaLabs/angstrom/blob/3690f9198321983f3700c5e417827335461e3651/contracts/src/modules/UnlockHook.sol
20. BlockSec, *Thorns in the Rose: Exploring Security Risks in Uniswap v4's Novel Hook Mechanism*, 2023-11-06. https://blocksec.com/blog/thorns-in-the-rose-exploring-security-risks-in-uniswap-v4-s-novel-hook-mechanism
21. 0x, *Uniswap v4 hooks were a mistake*, 2026-09-14. https://0x.org/post/uniswap-v4-hooks-were-a-mistake (the author is a competing aggregator)
22. Crypto Briefing, *0x calls Uniswap v4 hooks a mistake after finding 54% are malicious, Hayden Adams pushes back*, 2026-09-15. https://cryptobriefing.com/0x-criticizes-uniswap-v4-hooks-malicious/ (secondary source)
23. Adams, A., Moallemi, C., Reynolds, S., Robinson, D. *am-AMM: An Auction-Managed Automated Market Maker*, arXiv:2403.03367, 2024. https://arxiv.org/abs/2403.03367
24. Uniswap Labs, *Uniswap v4 is here*, launch announcement, 2025-01-31. https://blog.uniswap.org/uniswap-v4-is-here (first-party; used only for the launch date and vendor-stated audit and bounty figures)
