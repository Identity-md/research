# Audit: `0xbB0c1F82A2ea0253ea3D91c2f05cADed82133415` (SIMD, "Super Intelligent Identity")

**Snapshot time:** 2026-10-04, ~17:15–17:20 UTC (Ethereum mainnet block ≈ 26,120,444)
**Token age at snapshot:** ~30 minutes (created block 26,120,280, 16:46:59 UTC)
**Primary source:** Etherscan pages for each address and transaction linked below. On-chain state was cross-checked with read-only `eth_call` / `eth_getLogs` via public RPC (Foundry `cast`).

---

## Verdict (short answer)

**The contract itself looks legitimate. It is not a honeypot, and the code has no rug-pull mechanism. The investment is still a very high-risk micro-cap memecoin.**

- **Token contract:** a stock OpenZeppelin ERC-20 with a fixed 1,000,000,000 supply. It has no owner, no mint, no blacklist, no pause, no transfer tax, and it isn't upgradeable. Its one custom hook (`distributor`) is set to `address(0)` and is immutable, so that hook can never run.
- **Liquidity:** the full supply was placed into a Uniswap V4 pool by the launchpad's hook contract. The verified hook code has no way to remove that liquidity, and only the hook can add liquidity. A classic LP rug isn't possible.
- **Selling works:** 98 sell swaps had succeeded by the snapshot.
- **The creator burned their dev buy:** they sent 12,883,228 of their 12,883,229 SIMD to `0x…dEaD`.
- **Real risks that remain:**
  - 3% fee on every buy and sell.
  - 99% anti-snipe fee during the first 20 seconds.
  - Extremely young token with a tiny opening FDV ($4,000).
  - The pool is priced in **IMD**, a bridged token that its owner can rename. On Etherscan it is labeled "Fren Pet (FP)".
  - Price can collapse simply because holders sell. That's normal memecoin risk, not a code exploit.

"Legit" here means **the code doesn't cheat you**. It does **not** mean the token will hold value.

---

## 1. Facts (directly observed, with sources)

### 1.1 Token contract

| Item | Value | Source |
|---|---|---|
| Name / symbol / decimals | Super Intelligent Identity / SIMD / 18 | [Etherscan token page](https://etherscan.io/token/0xbB0c1F82A2ea0253ea3D91c2f05cADed82133415); `name()`, `symbol()` eth_call |
| Source verified | Yes, "Similar Match" to `0x834E1D9c…18bED9568`. Contract name `LaunchToken`, solc v0.8.26, optimizer 200 runs, EVM cancun | [Etherscan code tab](https://etherscan.io/address/0xbB0c1F82A2ea0253ea3D91c2f05cADed82133415#code) |
| Total supply | 1,000,000,000 SIMD (`TOTAL_SUPPLY` constant, minted once in the constructor) | Verified source; `totalSupply()` = `0x033b2e3c9fd0803ce8000000` |
| Creator | `0xE132be23CE6255930556a45406075E62fb6340C0` | [Etherscan](https://etherscan.io/address/0xe132be23ce6255930556a45406075e62fb6340c0); `creator()` |
| Factory | `0xc6B080DEd03C3382476A76345e79f82BD480977B` (`LaunchFactory`, verified) | `factory()`; [Etherscan](https://etherscan.io/address/0xc6b080ded03c3382476a76345e79f82bd480977b#code) |
| `distributor` | `0x0000000000000000000000000000000000000000` | `distributor()` eth_call |
| Creation tx | [`0xf6f58c7a…5255cead`](https://etherscan.io/tx/0xf6f58c7a775e8587f73add13247329befa4c6bbcb55aa09f029dba6d5255cead), `createLaunchAndBuy`, block 26,120,280 | Etherscan tx page |
| Embedded description | "Launched on Stockereum.fun - #1 Meme/Stocks Launchpad on Ethereum" | `DESCRIPTION` constant |
| `metadataUri` | `{"description":"Autonomous intelligence operating across the Identity.md network.","web":"https://www.si-md.xyz/","x":"https://x.com/SuperIMD_eth","tg":"",...}` | `metadataUri()` eth_call, decoded |

**What the verified source contains** (from `src/LaunchToken.sol`):
- It inherits OpenZeppelin `ERC20` and nothing else (no `Ownable`, no proxy).
- It has three immutables: `creator`, `factory`, `distributor`.
- It overrides only `_update`, and only to call `IHolderDistributor(distributor).onTransfer(...)` **if `distributor != address(0)`**. Because `distributor` is `0x0` and immutable, the override does nothing for this token.
- The ABI exposes only standard ERC-20 functions plus the view getters `DESCRIPTION`, `TOTAL_SUPPLY`, `creator`, `factory`, `distributor`, `metadataUri`. It has no state-changing admin functions.

### 1.2 Launch, liquidity and pool configuration

From the creation transaction (Etherscan token-transfer section and receipt logs):

1. 1,000,000,000 SIMD were minted to the hook `0x322dcEc4958C14e021A9F1cD49DF11b9457968cC`. The hook then transferred all of them to the **Uniswap V4 PoolManager** `0x000000000004444c5dc75cB358380D2e3dE08A90`.
2. In the same transaction, the creator paid 0.021 ETH:
   - 0.001 ETH creation fee went to treasury `0x7D32E6c4…206CF4ad2`.
   - 0.02 ETH dev buy went through router `0xcdf832D2…DD7233767` and returned **12,883,229.0289 SIMD** (≈1.29% of supply) to the creator.

Pool state, read from the hook with `getLaunch(poolId)` (poolId `0x99de115f6fcf3a505e94a16175fbb34a304425f9a72a2e091c60fb723dc39a4e`, taken from the factory's `Launched` event):

| Field | Value |
|---|---|
| quote asset | `0xD34a99Bc0f67aE1bbd63C660e6d0b0dd03E263B7` (see §1.5) |
| feePpm | 30,000 = **3%** |
| feeRecipient | the creator `0xE132…40C0` |
| feesToHolders | false |
| tick range | [-145,800, 887,200]: single-sided SIMD liquidity from the opening price upward |
| opening FDV | $4,000 (`openingFdvUsd()` = 4000e18) |
| `currentFee(poolId)` | 30,000 (the anti-snipe window has ended) |

What the verified `LaunchHook` source ([Etherscan](https://etherscan.io/address/0x322dcec4958c14e021a9f1cd49df11b9457968cc#code)) does:
- **Liquidity is locked by construction.**
  - `beforeAddLiquidity` reverts unless the sender is the hook itself.
  - The hook's only liquidity code path (`ACTION_SEED` in `unlockCallback`) adds a positive liquidity delta.
  - No function anywhere calls `modifyLiquidity` with a negative delta, so nobody can withdraw the position.
- **The hook has no owner or admin functions.** `factory`, `escrow` and `poolManager` are immutable. `openLaunch` can only be called by the factory, and only when a launch is created.
- **Fees:**
  - Buys pay `feePpm` on the IMD input and sells pay it on the IMD output.
  - During the first 20 seconds the fee decays linearly from 99% down to `feePpm` (`ANTI_SNIPE_DURATION = 20`, `LAUNCH_FEE = 990_000`).
  - Because `feePpm` is ≥ 20,000, 1% goes to the platform (`PLATFORM_FEE_HIGH`) and the remaining 2% is credited to the creator in `FeeEscrow` `0xAcefe251…A060824BA`.
- **Only exact-input swaps are allowed.** `beforeSwap` reverts on exact-output swaps. Some aggregators may fail to route because of this, but it isn't a sell block.
- The hook's address bits enable exactly beforeInitialize, beforeAddLiquidity, beforeSwap, afterSwap, beforeSwapReturnDelta and afterSwapReturnDelta (`0x…68cc` & `0x3fff` = `0b10100011001100`). That matches the verified code. The "not implemented" callbacks (remove liquidity, donate) are never invoked.

On-chain wiring, read by eth_call: `factory.hook()` = the hook, `hook.factory()` = the factory, `hook.escrow()` = FeeEscrow, `escrow.hook()` = the hook. The factory and hook pointers are both one-time-set.

### 1.3 Trading activity (blocks 26,120,280–26,120,444)

These figures come from the hook's `Trade` events filtered by this poolId:
- 265 swaps: **167 buys and 98 sells, all successful.**
- About 3,523.9 IMD went in (gross), about 2,883.2 IMD came out (net), and about 194.9 IMD was taken in fees.
- Largest sell: 32,376,608 SIMD → 162.8 IMD, [tx `0x1650a270…`](https://etherscan.io/tx/0x1650a2707197a3489d54ed65e303340ec3dd8232b7706da32672595802f13366).

### 1.4 Holders and creator behaviour

- **Holders:** Etherscan reports 60–61. The top holders ([holders tab](https://etherscan.io/token/0xbB0c1F82A2ea0253ea3D91c2f05cADed82133415#balances)) are:
  - Uniswap V4 PoolManager: 43.82%.
  - The largest non-pool wallet `0xda804D6B…080ef742B`: 3.13%.
  - The next ~20 wallets: about 1.1–2.9% each.
  - `0x…dEaD`: 1.29%.
- **Dev-buy burn:** the creator sent 12,883,228 SIMD to `0x…dEaD` ([tx `0xf28efe50…`](https://etherscan.io/tx/0xf28efe50d0998ec025647fe407f70996a32a99d7335130cf0a9d7426b020765b), 16:51:59 UTC). The creator now holds ≈1.03 SIMD.
- **Creator wallet:** funded by "Binance 17" about 5 hours before launch, and its first transaction was about 1 hour before (Etherscan labels). It repeatedly calls `claim` on FeeEscrow (collecting its 2% trading fees, in IMD) and sends IMD to `IMDJobsPayer` `0xd60483Eb…Bb57f9B21` (verified, methods `Refund` and `Set Refund Boost`).

### 1.5 Quote asset (what SIMD is priced in)

- **Address:** `0xD34a99Bc0f67aE1bbd63C660e6d0b0dd03E263B7`. On Etherscan its contract name is `BridgedFP` and its token tracker is **"Fren Pet (FP)"** ([Etherscan](https://etherscan.io/address/0xd34a99bc0f67ae1bbd63c660e6d0b0dd03e263b7#code)).
- **On-chain `name()`/`symbol()`** currently return **"Identity.md" / "IMD"**.
- **Why they differ:** the verified source is a LayerZero OFT with owner-only `updateName`, `updateSymbol` and `updateNameAndSymbol`, plus the usual OFT owner powers (`setPeer`, `setDelegate`, etc.).
- **USD price used at launch:** $8.554 per IMD (the `quoteUsdPrice` signed into the creation calldata).

### 1.6 Launchpad admin

- **Owner:** `LaunchFactory` and `FeeEscrow` are both owned by `0xec4529D816f2A1F4604B241755d01a15c2cE9A17`, which has no contract code, so it is an EOA rather than a multisig. `pendingOwner` is 0x0.
- **What the owner can change:** treasury, router, price signer, creation fee, opening FDV, pause new launches, register quotes, and the escrow's platform-fee recipient.
- **What the owner can't change:** none of these powers reach an existing pool's liquidity, fee rate or fee recipient, or the SIMD token.
- **Scale:** the factory has 1,636 launches (`launchCount()`).

### 1.7 Off-chain links

https://www.si-md.xyz/ returns HTTP 200 with the title "SIMD", and the page contains this contract address. https://x.com/SuperIMD_eth returned HTTP 200. I didn't review the content of either.

---

## 2. Inferences (my reasoning, not direct observations)

1. **Not a honeypot.** The token has no transfer restrictions, the hook's sell path only takes a fee, and 98 real sells succeeded. *Confidence: high.*
2. **No LP rug possible through this pool.** The position is owned by an ownerless hook that has no withdrawal path. *Confidence: high, based on reading the verified source.* I didn't independently compile it and byte-compare it against the deployed code; I relied on Etherscan's verification.
3. **The creator's incentive is fees, not dumping.** With the dev buy burned, the creator's visible income is the 2% trading fee. About 194.9 IMD in total fees had been taken by the snapshot; roughly two-thirds is the creator's share. At the $8.55 launch quote price that is on the order of $1,100. That figure is an estimate.
4. **Fair-launch-ish, but the creator had an edge.** The dev buy in the creation block paid the base 3% fee, while other buyers in the first 20 seconds paid up to 99%. The creator burned those tokens, so that edge wasn't monetized.
5. **IMD is a second layer of risk.** SIMD's dollar value depends on IMD, a renameable bridged token whose owner holds LayerZero bridge-configuration powers. A problem with IMD would hit the SIMD pool directly.
6. **Volume is concentrated.** The hook records `trader` as the swap sender, which is often a router, so "16 unique traders / 10 unique sellers" undercounts real wallets. Activity is still small and concentrated.

## 3. Uncertainty

- Everything is a **~30-minute-old snapshot**. Holders, prices and creator behaviour can change at any time.
- **Price and market cap:** Etherscan showed no market data, and I didn't compute a live SIMD price.
- **Unread code:** I didn't audit the router (`0xcdf832D2…`), `IMDJobsPayer`, or the full LayerZero OFT for IMD. They don't control SIMD's transfer or liquidity logic, but they matter for anyone routing through them.
- **Sybil wallets:** whether the creator controls other holder wallets wasn't investigated. The flat ~1–3% distribution among the top wallets is consistent with either organic snipers or sybils.
- **Peer review:** this report hasn't been independently reviewed.

## 4. Unanswered questions

- Who controls the factory and escrow owner EOA `0xec4529D8…`, and who controls the IMD/BridgedFP owner? Is Stockereum.fun / "Stockpad" (the EIP-712 domain name) a known team?
- Why is the IMD token still labeled "Fren Pet (FP)" on Etherscan? Was the rename sanctioned, and what is IMD's own liquidity and backing?
- Is there any official link between SIMD and the Identity.md project, beyond the metadata text and the IMD quote pairing?
- What is `IMDJobsPayer`, and why is the creator routing fee income to it?

## 5. Practical guidance

- Safe to interact with at the contract level. Only approve the router you actually swap through, and only use exact-input swaps.
- Expect to lose 3% on entry and 3% on exit, and don't buy within 20 seconds of any new launch from this factory.
- Treat SIMD as a speculative micro-cap whose value is denominated in another speculative token (IMD). Size any position accordingly.
