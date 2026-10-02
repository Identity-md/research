# Chainlink ETH/USD answer on Ethereum mainnet

**Answer: $2,728 per ETH, rounded down to whole dollars.** At the latest common Ethereum mainnet block reported by two RPC nodes during the read, block **26,103,003** (`0x18e4cdb`), the feed's answer was **$2,728.04000000** (raw signed integer `272804000000`). The feed reported **8 decimal places**, so the calculation is `floor(272804000000 / 100,000,000) = 2728`.

## Facts and evidence

- Chainlink identifies the [Ethereum mainnet ETH/USD standard feed](https://data.chain.link/feeds/ethereum/mainnet/eth-usd) with [proxy address `0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419`](https://etherscan.io/address/0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419). Its [Data Feeds API reference](https://docs.chain.link/data-feeds/api-reference) defines `latestRoundData()` as returning `(roundId, answer, startedAt, updatedAt, answeredInRound)` and `decimals()` as the answer's scale. [Ethereum's JSON-RPC documentation](https://ethereum.org/developers/docs/apis/json-rpc/) describes block-number state reads with `eth_call`.
- Both [PublicNode](https://ethereum-rpc.publicnode.com) and [Blast](https://eth-mainnet.public.blastapi.io) returned chain ID `0x1`, block hash `0x96cee2a267b763c5aaebd036d42faa7d7828cbce7794252f8aadfc5d893867e8` for [block 26,103,003](https://etherscan.io/block/26103003), and the same `latestRoundData()` result when called at `0x18e4cdb`. The block timestamp was **2026-10-02 06:59:23 UTC**. The read ran from **2026-10-02 06:59:25 UTC** to **2026-10-02 06:59:26 UTC**. Their reported heads were 26,103,003 and 26,103,003, respectively; the shared block was used for both calls.
- At that block, `decimals()` (`0x313ce567`) returned `8`. `latestRoundData()` (`0xfeaf968c`) returned round ID `129127208515966895560`, answer `272804000000`, startedAt **2026-10-02 06:21:24 UTC**, updatedAt **2026-10-02 06:21:59 UTC**, and answeredInRound `129127208515966895560`. The separate `latestAnswer()` read at the same block also returned `272804000000`.

The exact `latestRoundData()` return data from each node was:

```text
0x00000000000000000000000000000000000000000000000700000000000085c80000000000000000000000000000000000000000000000000000003f8462b100000000000000000000000000000000000000000000000000000000006abf4d64000000000000000000000000000000000000000000000000000000006abf4d8700000000000000000000000000000000000000000000000700000000000085c8
```

Reproduce the block-pinned read with either RPC endpoint above, using this JSON-RPC request body:

```json
{"jsonrpc":"2.0","method":"eth_call","params":[{"to":"0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419","data":"0xfeaf968c"},"0x18e4cdb"],"id":1}
```

## Inference

The USD amount and whole-dollar answer are arithmetic inferences from the on-chain integer and the on-chain `decimals()` response. At the sampled block, the feed's `updatedAt` time was **37 minutes 24 seconds** before the block timestamp.

## Uncertainty and unanswered questions

**Uncertainty:** This is a snapshot of the feed's latest *reported answer* at that block; later blocks may carry another answer. The two RPC services agreed on the block hash and contract return data, but this check does not independently verify Ethereum consensus.

**Unanswered questions:** None needed to compute the requested block-specific answer. This report does not establish the price in blocks after 26,103,003.
