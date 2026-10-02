# IMDRIP (`0x885ea754bdD1dF1c363249321142e24bef99D2aC`) risk review

**Verdict (snapshot: 2026-10-02 12:57 UTC):** The **token contract** has a strong, narrow set of immutable properties: it is verified, not a proxy, has no owner/administrator interface, and exposes no post-deployment mint, tax, blacklist, pause, or transfer-restriction function. The **liquidity position** is credibly locked in the sense relevant to this Uniswap v4 design: its launcher reports `lpBurned = true` and `owner = 0x0`, while still reporting non-zero position liquidity. The irreversible lock was performed in a confirmed transaction.

That is **not a blanket “safe” verdict**. Trading is governed by a distinct, still-owned hook which levies a fixed 2% ETH-side fee. Its owner can redirect the 0.5% marketing share. The contract that receives the other 1.5% is also controlled by that same owner/keeper and does not enforce the advertised “top 100 holders” allocation on-chain. The token is also extremely new, thinly held, and concentrated. I would characterize it as **technically simple at the ERC-20 and LP-lock layers, but economically and reward-distribution centralized; high risk for a buyer**.

This is an on-chain code/state review, not financial advice or a security audit.

## Scope and evidence method

All state below was read from Ethereum mainnet at the snapshot time using `eth_call` against `https://ethereum-rpc.publicnode.com`; code, source, events, transactions, and holder data were cross-checked in Blockscout. Links identify the actual contracts/transactions, rather than relying on a token-list label. “Verified source” means the explorer reports source verification; it does not independently prove that the code has no bug.

Primary evidence:

- [IMDRIP token—verified contract and holder view](https://eth.blockscout.com/address/0x885ea754bdD1dF1c363249321142e24bef99D2aC)
- [IMDRIP launcher—verified contract](https://eth.blockscout.com/address/0xcb39c4058f43fb758df6725c4213d1e588d7285e)
- [Confirmed `burnLp()` transaction](https://eth.blockscout.com/tx/0x83fd0698a9e342eab732ee68c8d936a7528b2e0e23c5afc963bd190e43ad6de3)
- [IMDRIP Hook—verified contract](https://eth.blockscout.com/address/0x7C9EE7476D131FFe0655Ca1E24587a921BC3e0cc)
- [DripDistributor—verified contract](https://eth.blockscout.com/address/0xAe4BBa5839194d81327F46a45966887de2F72e6f)
- [Token deployment / initial mint](https://eth.blockscout.com/tx/0x8d9c7112a1b429080369000d57253ce3bbc0a8eb2c1753e497bea1c4fa524c0c)

## Facts — token contract

| Observation | Evidence / result |
|---|---|
| Chain and identity | Ethereum mainnet ERC-20; name/symbol `IMDRIP`, 18 decimals. |
| Source and upgradeability | The explorer marks it verified and no proxy/implementation. The verified ABI/runtime dispatcher has only `name`, `symbol`, `decimals`, `TOTAL_SUPPLY`, `totalSupply`, `balanceOf`, `allowance`, `approve`, `transfer`, and `transferFrom`. |
| Supply | `totalSupply()` and `TOTAL_SUPPLY()` each returned `1,000,000,000 × 10^18`. The deployment minted that amount once to the launcher `0xcb39…285e`. |
| Owner / renouncement | There is **no `owner()`, `renounceOwnership()`, or admin role** in the token ABI or verified source. `owner()` reverts. Thus it was not “renounced” in the usual Ownable-event sense; it was deployed without token ownership to renounce. |
| Mint, tax, blacklist, pause | The verified source has a private `_mint` used only by the constructor, and no externally callable mint/burn, fee-setting, blacklist/allowlist, pause, rescue, or arbitrary-transfer function. Transfers use the ordinary ERC-20 balance/allowance logic. |

## Facts — liquidity lock and renouncement

This is a Uniswap v4 position, not a conventional ERC-20 LP token. The verified launcher is the position owner and is the relevant control point.

| Snapshot read from launcher `0xcb39…285e` | Value |
|---|---:|
| `launched()` | `true` |
| `lpBurned()` | `true` |
| `owner()` | `0x0000000000000000000000000000000000000000` |
| `positionLiquidity()` | `31,627,551,493,412,811,474,352` (non-zero) |
| pool | native ETH / IMDRIP, fee `0`, tick spacing `60`, hook `0x7C9E…e0cc` |

The verified `burnLp()` code sets `lpBurned = true` and then transfers launcher ownership to `address(0)`. The launcher’s only removal route, `removeLiquidity(address)`, requires both `onlyOwner` and `!lpBurned`; therefore, on the observed state it cannot be called by anyone. The successful `burnLp()` call was made by `0xd1E9…5745` at block `26,100,128` on 2026-10-01 21:22:35 UTC. These are direct, attributable facts from the linked transaction and launcher source.

## Facts — trading hook and rewards controls

The fixed-supply token is not the whole trading system. The pool key points to the verified [IMDRIPHook](https://eth.blockscout.com/address/0x7C9EE7476D131FFe0655Ca1E24587a921BC3e0cc), whose current reads were:

| Hook control / setting | Snapshot value |
|---|---|
| `FEE_BPS()` / `MARKETING_BPS()` | `200` / `50` (2% total ETH-side swap fee; 0.5% of trade to marketing and 1.5% to drip) |
| hook `owner()` | `0xd1E9d964f272C7E252fB5967A20810DCAa9b5745` |
| `marketingWallet()` | the same `0xd1E9…5745` address |
| `distributor()` | `0xAe4BBa5839194d81327F46a45966887de2F72e6f` (immutable) |
| `initialized()` | `true` |

The hook source makes the fee constants and distributor immutable and has no blacklist, per-user tax, trading switch, or fee-rate setter. It does expose `setMarketingWallet(address)` to its owner, so that owner can redirect the marketing portion at any time. `flush()` is permissionless, but it sends the two already-accrued portions to the fixed distributor and the mutable marketing wallet.

The hook’s immutable distributor is also a verified, non-proxy contract. Its current `owner()` **and** `keeper()` are `0xd1E9…5745`. It holds the IMD reward token and lets the keeper buy IMD and publish a Merkle root. The source does prevent the owner from rescuing IMD, but `publishRoot` only checks that total allocations do not exceed available IMD; it does **not** verify “top 100,” average balances, or an independent holder snapshot. A keeper can publish a root allocating the available IMD to arbitrary addresses, including itself. This is a material control retained by the same address.

## Facts — market structure and concentration

At the snapshot, the explorer reported 49 holders. The Uniswap v4 PoolManager held `398,734,176.878` IMDRIP, about **39.87%** of the 1 billion supply. The next ten non-pool holder entries together held about **28.56%**; the largest individual non-pool holder held about **4.53%**. These figures are a point-in-time holder ledger, not proof that addresses are independent people or that all holdings are freely sellable. See the token’s linked holder view.

## Inferences and risk interpretation

- **LP lock: supported.** The combination of the source’s irreversible guard, `lpBurned=true`, zero launcher owner, a confirmed burn transaction, and non-zero position liquidity is strong evidence that this launcher’s initial v4 position cannot be withdrawn through its published code. It is better evidence than merely seeing tokens sent to a burn address.
- **Token renouncement: wording needs care.** It is accurate to say the token has no owner and no privileged token functions. It is inaccurate to imply a conventional `renounceOwnership()` event occurred on the token, because the token does not implement Ownable.
- **No token-level honeypot mechanism found.** The verified token implementation is standard fixed-supply ERC-20 logic and its dispatcher has no hidden fallback routes. The verified hook applies a fixed 2% ETH-side fee to swaps and does not contain address-specific sell blocking. This reduces a common contract-level rug vector, but is not a guarantee that a trade will execute or be profitable.
- **The “safe functions” conclusion applies only narrowly.** The hook and distributor add meaningful non-token trust assumptions: the hook owner controls the marketing recipient, and the distributor owner/keeper controls which Merkle root receives the IMD rewards. The issuer address presently occupies all of those roles.
- **Economic risk remains high.** A ~40% pool share, only 49 listed holders, substantial wallet concentration, a very recent deployment, price impact, and a 2% fee mean the asset can still lose value rapidly even if no token mint or LP withdrawal is available.

## Unanswered questions / limits

- I did not identify the human or organization behind `0xd1E9…5745`, nor establish whether it controls any holder wallets. On-chain addresses alone cannot answer that.
- This review does not audit Uniswap v4 PoolManager, the external IMD token/pool used by the distributor, router integrations, MEV behavior, or the project website/social claims.
- No independent audit, formal verification, or live buy-and-sell simulation was performed. A future code change is impossible for these non-proxy contracts, but external infrastructure and market conditions can change.
- “LP locked” addresses only the observed launcher-owned initial position. It cannot prevent third parties from adding/removing their own liquidity positions, and it does not guarantee depth, price stability, or the safety of every integration.

## Reproducibility checks performed

1. Read token, launcher, hook, and distributor state directly with `eth_call` at the snapshot time.
2. Compared the token runtime selector list to its verified ABI; no privileged token selector was present.
3. Read the verified launcher, hook, and distributor source and inspected the access control around liquidity removal, fee routing, and reward allocation.
4. Cross-checked token deployment, `burnLp()` execution, verification/proxy flags, and holder balances in the linked explorer records.

