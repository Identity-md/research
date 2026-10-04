# SIMD ("Super Intelligent Identity" / @SuperIMD_eth): what it is, what it does, and an honest opinion

**Snapshot:** 2026-10-04, about 16:47–17:56 UTC (Ethereum blocks 26,120,280 → ~26,120,631). The token was **about 70 minutes old** when this was written. Anything about price, holders or volume will be out of date within hours.

**Subject:** Ethereum token `0xbb0c1f82a2ea0253ea3d91c2f05caded82133415`, website https://www.si-md.xyz/, X account https://x.com/SuperIMD_eth.

**Labels used below**
- **[FACT-chain]**: I read this directly from Ethereum mainnet with `cast` against a public RPC (`ethereum-rpc.publicnode.com`). You can reproduce it.
- **[FACT-src]**: Stated by a named web page. I read it through a fetch or summarisation tool, not line by line, so a summarisation error is possible.
- **[INFERENCE]**: My interpretation of the facts.
- **[UNKNOWN]**: Not established.

---

## 1. Short answer

SIMD is a **one-hour-old memecoin-style ERC-20**, launched through the Identity.md (IMD) launchpad. The creator wallet has also deployed a small helper contract, **`IMDJobsPayer`**. That contract takes the creator's share of SIMD trading fees, paid in IMD tokens, and uses it to **refund part of what users pay for Identity.md jobs**. That is the whole "utility": SIMD trading volume produces fees, and the fees subsidise IMD job costs.

The token contract has no functions beyond a plain ERC-20. It grants holders no rights, no revenue share, no governance and no access. The subsidy mechanism is real and visible on-chain, but it is small: 1.75 IMD had been refunded at snapshot time. It is controlled by a single wallet that can pause it, change it or sweep it. It currently refunds **50%, not the "100%" the X bio claims**.

**My opinion:** the mechanism is a genuine, transparent idea and better than a token with no story at all. But the token itself is a speculative, very early, low-liquidity asset (≈$14k FDV, ≈$11k liquidity), and its value depends entirely on one anonymous operator continuing to act in good faith. Treat it as a high-risk memecoin with a narrative, not as an investment in infrastructure.

---

## 2. Evidence

### 2.1 Token contract
| Item | Value | Source |
|---|---|---|
| Name / symbol | "Super Intelligent Identity" / SIMD | [FACT-chain] `name()`, `symbol()` |
| Supply | 1,000,000,000 (1e27 wei, 18 decimals), fixed | [FACT-chain] `totalSupply()`; [FACT-src] [Etherscan token page](https://etherscan.io/token/0xbb0c1f82a2ea0253ea3d91c2f05caded82133415) |
| Contract type | `LaunchToken`, Solidity 0.8.26, source verified | [FACT-src] [Etherscan code tab](https://etherscan.io/address/0xbb0c1f82a2ea0253ea3d91c2f05caded82133415#code) |
| Functions | Standard ERC-20 only. Etherscan's ABI shows no mint, burn, pause, blacklist or tax functions | [FACT-src] same page |
| `factory()` | `0xc6B080DEd03C3382476A76345e79f82BD480977B` (verified as `LaunchFactory`) | [FACT-chain]; [FACT-src] [Etherscan](https://etherscan.io/address/0xc6B080DEd03C3382476A76345e79f82BD480977B) |
| `creator()` | `0xE132be23CE6255930556a45406075E62fb6340C0` (EOA) | [FACT-chain] |
| `distributor()` | `0x000…000` (none) | [FACT-chain] |
| `metadataUri()` | `{"description":"Autonomous intelligence operating across the Identity.md network.","web":"https://www.si-md.xyz/","x":"https://x.com/SuperIMD_eth","tg":"", ...}` | [FACT-chain] |
| Created | Tx `0xf6f58c7a…5cead`, block 26,120,280, 2026-10-04 16:46:59 UTC, sent by the creator to the factory with 0.021 ETH | [FACT-chain] |
| Etherscan reputation | "Reputation UNKNOWN", no audit submitted | [FACT-src] Etherscan token page |

**Address attribution.** The on-chain `metadataUri` points to both si-md.xyz and @SuperIMD_eth, and the website shows this contract address. All three items you gave me therefore belong to the same project. [FACT-chain + FACT-src: [si-md.xyz](https://www.si-md.xyz/)]

### 2.2 Launch mechanics and liquidity
- In the creation transaction, 100% of supply was minted to the `LaunchHook` contract (`0x322dcec4958c14e021a9f1cd49df11b9457968cc`). The hook placed it into a Uniswap v4 pool as liquidity; the `ModifyLiquidity` event's sender is the hook itself. The creator's 0.021 ETH bought 1.288% of supply. [FACT-chain, from the creation receipt logs]
- The creator **sent that entire 12,883,228 SIMD to `0x…dEaD`** 25 blocks later (block 26,120,305), and now holds ≈1.03 SIMD. [FACT-chain] **[INFERENCE]** No large dev bag is left to dump. That is a positive sign, although the creator earns from fees rather than from holding (see 2.3).
- `LaunchHook` and `LaunchFactory` are verified contracts deployed by `0xec4529D8…9A17`. They are shared IMD launchpad infrastructure, not code written for SIMD. Per the summarised source, the hook has no owner function to pull liquidity, charges a per-launch fee capped at 3% plus a platform fee, and sends fees to a `FeeEscrow` (`0xacefe251…24ba`). [FACT-src: [hook code](https://etherscan.io/address/0x322dcec4958c14e021a9f1cd49df11b9457968cc#code)] **[INFERENCE, medium confidence]** Liquidity looks effectively locked, because the hook owns the position. I did not audit the hook line by line.
- Pools ([DexScreener API](https://api.dexscreener.com/latest/dex/tokens/0xbb0c1f82a2ea0253ea3d91c2f05caded82133415)) [FACT-src]:
  - **SIMD/IMD** (Uniswap v4): ≈$11.1k liquidity, ≈$14.3k FDV, ≈$59.9k 24h volume, 185 buys / 113 sells.
  - **SIMD/USDC**: ≈$74 liquidity, effectively unused.

### 2.3 The "utility": `IMDJobsPayer`
The X bio reads: *"A protocol tracking IMD agents in real time, using protocol fees to cover 100% of Identity.md job costs @ethereum"*. [FACT-src: [fxtwitter mirror of the profile](https://api.fxtwitter.com/SuperIMD_eth); x.com itself returned HTTP 402]

What the chain shows:
- The creator wallet repeatedly calls **Claim** on `FeeEscrow`. Between blocks 26,120,284 and 26,120,596 it received ≈141.6 IMD from the escrow in 12 claims. [FACT-chain, IMD `Transfer` logs]
- After almost every claim it forwards IMD to `0xd60483eb8004e3de3e283b3eff0e67fbb57f9b21`: ≈104.2 IMD in 12 transfers, about 74% of what it claimed. It kept the rest (≈37.4 IMD balance at snapshot). [FACT-chain]
- `0xd604…9B21` is a verified contract named **`IMDJobsPayer`**, deployed by the same creator wallet. [FACT-src: [Etherscan](https://etherscan.io/address/0xd60483eb8004e3de3e283b3eff0e67fbb57f9b21)]
- Live configuration [FACT-chain]:
  - `paymentToken` = IMD (`0xD34a99Bc…63B7`, `name()` = "Identity.md")
  - `refundBps` = **5000 (50%)**
  - `boostBps` = 0
  - `maxPaidPerPayment` = 5 IMD
  - `maxRefundPerDay` = 250 IMD
  - `maxEthBuyPerDay` = 3 ETH
  - `dev()` = the creator wallet
  - not paused
- Per the summarised source, `refund()` takes a list of past payments (payer, token, amount) and pays `refundBps` (plus any boost) back to each payer. `buyToken()` can swap ETH for IMD through Uniswap v4. The `dev` can pause, change rates, change the pool or token, and **sweep ETH and tokens out**. The dev role is transferable. [FACT-src: [IMDJobsPayer code](https://etherscan.io/address/0xd60483eb8004e3de3e283b3eff0e67fbb57f9b21#code)]
- Refunds actually paid so far: **4 transfers, 1.75 IMD in total, to 3 wallets**. One of them (`0x5b95a971…0d06`) is also a top-3 SIMD holder at ≈2.9%. The contract held ≈105.4 IMD. [FACT-chain]
- The refund transactions were sent by the creator wallet. [FACT-src, Etherscan tx list] **[UNKNOWN]** I did not verify whether anyone else can trigger refunds, or how the operator decides which payments qualify. The payment list is supplied by the caller, so in practice this looks operator-curated.

**Context: what Identity.md is.** Per its docs, Identity.md is a network where a "swarm" of AI agent "seats" (ERC-8004 agent registrations) does work for requesters. Creating launches, oracle questions or schedules costs **0.5 IMD per action**, paid with the x402 payment protocol. Launches mint 1B tokens. [FACT-src: [imd.fun/docs](https://imd.fun/docs)] **[INFERENCE]** SIMD therefore offers a partial rebate on those IMD fees, paid out of SIMD trading fees. The docs also describe a "swarm launch", where 10% goes to the swarm through a distributor. SIMD's `distributor` is zero, so it was **not** a swarm-reward launch. **[UNKNOWN]** The docs I read say launches are "currently Sepolia testnet", which does not match the mainnet factory. The docs may simply be out of date.

### 2.4 Distribution and trading
Reconstructed from all 331 SIMD `Transfer` logs up to block 26,120,597 [FACT-chain]:
- **53 holders**, which matches Etherscan.
- Uniswap v4 PoolManager: 53.1% (pool liquidity).
- Dead address: 1.29% (the creator's burn).
- The other 51 wallets hold 45.6%. The top 10 of them hold 22.3%, and the largest holds 3.13%.
- **Within the first ~10 blocks (about 2 minutes), roughly 69% of supply was bought out of the pool.** In block 26,120,282 alone, 13 wallets bought 32.9%. Much of that has since been sold back into the pool.
- **[INFERENCE]** This is a classic bot or sniper opening. The ≈$60k of volume on a ≈$14k cap reflects churn, not organic adoption.

### 2.5 Website and X account
- **si-md.xyz:** the fetched content contains only the name "SIMD", the @SuperIMD_eth link, the contract address with an Etherscan link, a logo, and a `#network` anchor. No whitepaper, team, docs or roadmap were visible. [FACT-src: [si-md.xyz](https://www.si-md.xyz/)] **[UNKNOWN]** The "network" view is probably rendered client-side, perhaps as a live display of IMD agents to match "tracking IMD agents in real time". I could not retrieve its content.
- **X:** "Superintelligent Identity.md", joined 2026-09-27, 46 followers, 10 posts. [FACT-src: fxtwitter] I could not read the posts.
- **Creator wallet:** Etherscan shows it was funded from a Binance hot wallet about 5 hours before the snapshot, with 36 transactions in total. [FACT-src: [Etherscan](https://etherscan.io/address/0xE132be23CE6255930556a45406075E62fb6340C0)] There is no public identity, no team and no audit.

---

## 3. Full utility, stated plainly
1. **For SIMD holders:** nothing on-chain. The token is a plain ERC-20 with no staking, fee share or governance. Any value comes from trading demand and from the story.
2. **For Identity.md users:** possibly a partial refund (currently 50%, at most 5 IMD per payment, at most 250 IMD per day) on IMD job payments. The operator decides when to pay.
3. **For the creator:** the creator's share of SIMD trading fees, received in IMD. About 74% of it was observed going into the refund contract and about 26% stayed in the creator's wallet. Nothing on-chain requires the creator to keep forwarding fees.
4. **"Tracking IMD agents in real time":** claimed but **not verified**. I could not see the network page.

## 4. Honest opinion

**Positives**
- Everything is verified and readable on-chain. The token has no hidden mint or tax.
- Liquidity sits in a launchpad hook that has no owner withdrawal path (medium confidence).
- The dev burned their launch buy.
- There is a real, observable flow of fees into a subsidy contract, which is more than most launches do.

**Negatives**
- The value proposition is *rebates for a different token's users*. SIMD holders capture none of it directly. Only indirect "narrative" demand supports the price.
- The "100%" claim is false today. The contract is set to 50%, and 1.75 IMD has been refunded in total.
- One anonymous key controls the refund contract, and that key can sweep it. The roughly 26% of claimed fees kept in the creator's wallet is not explained.
- The launch is about one hour old, has ≈$11k liquidity, sniper-dominated early trading and a minimal website. Most tokens with this profile lose most of their value quickly. That is a base rate, not a prediction about this specific token.
- SIMD depends on the IMD ecosystem: if IMD job demand or the IMD price falls, the story falls with it.

**Verdict:** an interesting, honestly built-looking micro-experiment in "trading fees subsidise agent jobs", with no protective rights for token holders. If you buy, size it as money you can lose entirely. Watch whether `IMDJobsPayer` keeps receiving fees and paying refunds, and whether the operator explains the 50% vs 100% gap and the fees they keep.

## 5. Open questions (unanswered)
- Who runs the project, and do they have any relationship with the Identity.md team? There is no evidence either way.
- How are refund-eligible payments chosen? Can users claim refunds themselves?
- What does the website's `#network` view actually show, and does real-time agent tracking exist?
- What are the exact creator-fee and platform-fee percentages on this specific launch? (`feePpm` was not read.)
- Did the 10 posts on X make claims beyond the bio?
- Will the subsidy continue once the launch-day volume fades?

## 6. How to reproduce the on-chain checks
```
R=https://ethereum-rpc.publicnode.com
cast call --rpc-url $R 0xbb0c1f82a2ea0253ea3d91c2f05caded82133415 'metadataUri()(string)'
cast call --rpc-url $R 0xd60483eb8004e3de3e283b3eff0e67fbb57f9b21 'refundBps()(uint256)'
cast call --rpc-url $R 0xd60483eb8004e3de3e283b3eff0e67fbb57f9b21 'dev()(address)'
cast logs --rpc-url $R --from-block 26120280 --address 0xbb0c1f82a2ea0253ea3d91c2f05caded82133415 'Transfer(address indexed,address indexed,uint256)'
```
