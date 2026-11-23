# Fren Pet and IMD bridge verification

Fren Pet on Base and IMD on Ethereum are the same asset linked by a LayerZero bridge. Ethereum IMD at `0xd34a99bc0f67ae1bbd63c660e6d0b0dd03e263b7` returned `0xab152db8aac047b6757ffcf495ffe88d7712690a` from `peers(30184)`. On Base, that adapter returned Fren Pet at `0xff0c532fdb8cd566ae169c1cb157ff2bdc83e105` from `token()` and pointed back to Ethereum IMD via `peers(30101)`. The adapter’s `peers(30416)` named Robinhood Chain IMD at `0x5f7bb59365ce557c26dbcaa4ee9d39a4b95b7127`, whose `peers(30184)` pointed back to the adapter. The contracts’ `endpoint()` and the endpoints’ `eid()` reads confirmed the endpoint IDs. [Ethereum token reference](https://etherscan.io/token/0xd34a99bc0f67ae1bbd63c660e6d0b0dd03e263b7), [LayerZero OFT documentation](https://docs.layerzero.network/v2/developers/evm/oft/quickstart).

## Supply at the sampled blocks

| Chain | Block and timestamp | Contract read | Tokens |
| --- | --- | --- | ---: |
| Base | 61420084 · 2026-11-23 22:53:12 UTC | Fren Pet `totalSupply()` | 7,079,679.939616311457236507 |
| Base | 61420084 · 2026-11-23 22:53:12 UTC | Fren Pet `balanceOf(Base adapter)` | 4,295,815.922283 |
| Ethereum | 26480946 · 2026-11-23 22:52:59 UTC | IMD `totalSupply()` | 4,229,910.957698 |
| Robinhood Chain | 121771467 · 2026-11-23 22:53:11 UTC | IMD `totalSupply()` | 65,781.001515 |
| Ethereum and Robinhood Chain | | Combined IMD supply | 4,295,691.959213 |

The Base adapter held **123.96307 more Fren Pet** than the combined Ethereum and Robinhood Chain IMD supply. The sampled blocks have different timestamps. The reads establish the difference at those blocks. Its cause and circulating supply remain open. The Base adapter balance is included in Base’s total supply.

Etherscan returned HTTP 403. The proof uses read-only calls to [Ethereum RPC](https://ethereum-rpc.publicnode.com), [Base RPC](https://mainnet.base.org) and [Robinhood Chain RPC](https://rpc.mainnet.chain.robinhood.com). The `LayerZeroTokenBridge` line in `artifacts/page.json` records the block hashes, calldata and expected results. All three tokens returned 18 decimals.

## Notes

The assignment provided .imd/reads/project.md as a pinned project-history input. It supplied the earlier page and logo as local artifact files at artifacts/page.json and artifacts/logo.png, with pinned copies at .imd/reads/artifacts/page and .imd/reads/artifacts/logo. Both copies matched the supplied SHA-256 digests. The supply comparison uses three separately sampled blocks. The reason for the difference and the circulating supply remain unverified.
