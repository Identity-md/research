# Chainlink ETH/USD latest answer

**Answer: $2,654 USD, rounded down to whole dollars.**

At the latest Ethereum mainnet block returned by the public dRPC endpoint during this observation, the specified proxy returned **265407000000**, with **8 decimals**, equivalent to **$2654.07000000 USD per ETH**. Observation completed at **2026-10-02T18:57:13.169539+00:00**. This is a timestamped answer, not a continuously updated quote.

## Observed facts and evidence

| Field | Observed value |
|---|---|
| Feed proxy | `0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419` |
| RPC chain ID | `1` (Ethereum mainnet) |
| Latest block selected | [26106573](https://etherscan.io/block/26106573) (`0x18e5acd`) |
| Block hash | `0x069a68e4623a117b0d24ded03469b15790550904ab370f844eeebdb641bd36c2` |
| Block timestamp (UTC) | 2026-10-02T18:56:59+00:00 |
| `latestRoundData()` round ID | `129127208515966895578` |
| Signed answer | `265407000000` |
| `decimals()` | `8` |
| `startedAt` | `1790966380` |
| `updatedAt` | `1790966435` (2026-10-02T18:40:35+00:00) |
| `answeredInRound` | `129127208515966895578` |
| Feed update age at selected block | 984 seconds |

These values come from direct JSON-RPC reads against [dRPC's public Ethereum endpoint](https://eth.drpc.org). Exact requests, responses, and local request/response timestamps are preserved in [evidence.json](evidence.json). `latestAnswer()` independently returned the same integer through the same endpoint. A second read of the selected block returned the same block hash.

[Chainlink's official feed listing](https://data.chain.link/feeds/ethereum/mainnet/eth-usd) identifies the Ethereum ETH/USD standard proxy. [Chainlink's API reference](https://docs.chain.link/data-feeds/api-reference#latestrounddata) documents the round fields; its [decimals documentation](https://docs.chain.link/data-feeds/api-reference#decimals) defines the answer precision. The numeric price above comes from the RPC capture, not a search snippet or cached web quote.

## Calculation

Integer arithmetic gives:

```text
USD = 265407000000 / 100000000 = 2654.07000000
floor(USD) = 2654
```

This whole-dollar result is a deterministic calculation from the observed answer and decimals, rather than an estimate of a market trading price.

## Reproduction

Run from the repository root with Python 3 and curl:

```sh
python3 artifacts/read_feed.py 0x18e5acd
```

The script first verifies `eth_chainId`, retrieves the pinned block, then calls the proxy with these exact `eth_call` selectors and block tag `0x18e5acd`:

- `0xfeaf968c`: `latestRoundData()`; decode five 32-byte ABI words as `(uint80,int256,uint256,uint256,uint80)`.
- `0x313ce567`: `decimals()`.
- `0x50d25bcd`: `latestAnswer()`.

The complete JSON-RPC payloads are in `evidence.json`. Omit the block argument to select `eth_getBlockByNumber("latest", false)` at a new observation time. Running the script overwrites `evidence.json` and `answer.json`; copy the original evidence first if retaining this snapshot. Historical replay requires the endpoint to retain the selected block state.

## Limits and unanswered questions

“Latest” means the endpoint's head at the recorded block-selection request, pinned for all subsequent price calls. New blocks and feed updates can arrive before this report is read. The feed's update timestamp precedes the selected block; this answer represents its latest stored answer at that block, not a new observation produced in that block.

The result relies on one public RPC provider. Agreement between two contract methods and the repeated block hash is a consistency check, not independent provider verification or a consensus proof. The selected head was not required to be finalized and could be reorganized. No independent reviewer certified the observation. The price at later blocks remains unanswered by this snapshot.

## Local checks

The capture script passed assertions for mainnet chain ID, the five-word round response, 8 decimals, positive answer, matching `latestAnswer()`, a nonzero update timestamp no later than the block timestamp, and stable block hash. Offline artifact checks confirmed the integer calculation and required report content. These are author checks only.
