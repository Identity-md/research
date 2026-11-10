# Remaining ETHW in legacy contracts: a bounded, read-only finding

**Answer:** Yes. A publicly documented Parity-incident multisig still holds **114,939.000010007777777777 native ETHW** in the checked EthereumPoW snapshot. This establishes that at least one old, previously compromised contract retains a substantial native balance. **No currently recoverable balance or profitable MEV opportunity was established.** The observed missing library and historical operator account support a frozen-funds interpretation. The research covers one documented wallet and its library, not a chain-wide inventory. [Saved RPC evidence](../evidence/ethw-snapshot.json), [operator's historical account](https://medium.com/iconominet/proof-of-solvency-technical-overview-d1d0e8a8a0b8).

**Network and date.** These amounts are ETHW on EthereumPoW, not ETH on Ethereum mainnet or ETC on Ethereum Classic. EthereumPoW's launch announcement identifies the public RPC, currency symbol ETHW and post-fork chain ID 10001. The responding RPC returned `0x2711` (10001), the Ethereum genesis hash, and a recent block with positive mining difficulty, consistent with the project's client configuration. These checks identify the expected network through one provider; they are not independent consensus verification. [Official announcement](https://medium.com/@ETHW/ethw-mainnet-info-released-d775865a05e6), [client configuration](https://github.com/ethereumpow/go-ethereum/blob/master/params/config.go), [saved responses](../evidence/ethw-snapshot.json).

| Snapshot field | Observed value |
| --- | --- |
| Public RPC source | `https://mainnet.ethereumpow.org` |
| Collection completed, UTC | `2026-11-10T20:18:53.159534+00:00` |
| State block number | `25435687` (25,435,687) |
| State block timestamp, UTC | `2026-11-10T20:05:12+00:00` |
| State block hash | `0xbc1f243589a10824ee9dafe23156ec7291fe774f7a6de8bce56cb538b0b4b58c` |
| State root | `0x1fcfbb41bfb2f220fcbbc4d537db6be03426e425100a5dea6507692588c0c0ff` |
| Initial reported head | 25,435,751; 2026-11-10 20:18:27 UTC |
| Confirmation buffer | 64 blocks behind that reported head |

All account reads used the same explicit block number. A second read of that block returned the same header. The state root is recorded for identification; account proofs against it were not obtained. Complete requests, raw JSON responses and response hashes are preserved in the [evidence file](../evidence/ethw-snapshot.json).

**Verified balances and code.** The following are direct RPC observations at that block, rather than copied Ethereum-mainnet explorer balances:

| Historical account | Address | Native ETHW | Runtime code |
| --- | --- | --- | --- |
| ICONOMI Parity-incident multisig | `0x376c3e5547c68bc26240d8dcc6729fff665a4448` | `114939.000010007777777777` | 925 bytes; includes the library address as a literal |
| Destroyed Parity WalletLibrary account | `0x863df6bfa4469f3ead0be8f9f2aae51c91a907b4` | `0.003624159265358979` | 0 bytes (`0x`) |

The exact integer balances are respectively `114939000010007777777777` wei and `3624159265358979` wei. Conversion uses 10^18 wei per native unit without floating-point arithmetic. The library row is a historical contract **account with no remaining code**, not a second functioning contract or an additional withdrawal opportunity. [RPC evidence](../evidence/ethw-snapshot.json), [JSON-RPC method definitions](https://ethereum.org/en/developers/docs/apis/json-rpc/).

**Attribution and interpretation.** In its April 20, 2018 technical account, ICONOMI explicitly identified this wallet as affected by the Parity incident and said that proving ownership through key signatures did not give it access to the assets. That is an operator statement about the historical wallet, not evidence of current ETHW ownership or authorization to recover anything. [ICONOMI, Proof of Reserves section](https://medium.com/iconominet/proof-of-solvency-technical-overview-d1d0e8a8a0b8).

EIP-999 explains that dependent Parity multisigs lost access after their shared library was destroyed, and proposed restoring that library through a protocol state change. The proposal page is marked Withdrawn. Separately, the current ETHW snapshot reports empty code at precisely that library address. **Inference:** the sampled wallet is consistent with the inherited Parity freeze and should be treated as apparently inaccessible through its historical wallet mechanism. An embedded address alone is not a formal proof of every execution path; this study did not perform a full bytecode audit or recovery simulation. [EIP-999](https://eips.ethereum.org/EIPS/eip-999), [observed ETHW code](../evidence/ethw-snapshot.json).

**The replay history is real, but historical.** BlockSec's September 18, 2022 first-party analysis reports attacks observed from September 16 and describes an example involving 200 ETHW. Its finding concerned OmniBridge message validation using a stored chain identity, rather than replaying an identical signed Ethereum transaction. This supports the premise that fork-inherited applications experienced message-replay failures. It does not establish that the same failure remains usable today, that another contract is affected, or that any remaining funds can be taken. This study did not test that bridge's present state. [BlockSec incident analysis](https://blocksecteam.medium.com/reveal-the-message-replay-attacks-on-ethereumpow-64e4feee991c).

**MEV and profitability remain unanswered.** MEV concerns value from transaction inclusion or ordering; a contract balance by itself establishes neither such a trade nor a net return. This study collected no executable market quotes, liquidity measurements, liquidation eligibility, gas estimate, or transaction-ordering evidence. It therefore makes no profit estimate or recommendation to extract funds. The observed legacy balance is evidence of retained assets, not demonstrated MEV. [MEV definition](https://ethereum.org/en/developers/docs/mev/).

**Limits and unresolved questions.**

- **Coverage:** one operator-attributed frozen wallet and its missing library were checked. No exhaustive address discovery, other incident-family survey, or population estimate was performed. This finding cannot establish that other contracts are empty or that other opportunities do not exist.
- **Freshness and trust:** balances are valid only as reported for the stated block. One public RPC supplied the data; no independent provider, synced node, or cryptographic account-proof verification corroborated it. Local hashes detect changes to saved bytes, not false provider responses.
- **Ownership and access:** present ownership, recovery rights and owner authorization are unverified. A historically frozen or deprecated contract does not imply that its assets were abandoned.
- **Economics:** native ETHW is distinguished from wrapped tokens and copied ERC-20 balances. No token backing, exchange redemption, sale proceeds, or USD valuation was established.
- **Chain activity:** the RPC reported a head timestamp close to collection time. The brief's description of the chain as effectively dead was not established as a technical halt; ecosystem activity and economic viability were not measured.

**Reproduction and checks.** The dependency-free [capture script](../scripts/capture_snapshot.py) preserves nine successful read-only requests: chain ID, genesis and snapshot headers, two balances, two code reads, and a header reread. It performs no signing, broadcasting or contract execution. The [offline verifier](../scripts/verify_evidence.py) recomputes raw-response hashes, checks summary arithmetic, verifies that account reads share a block, and compares the report's metadata and amounts with the saved responses. These checks assess local consistency only and provide no independent authority for the research conclusions. See the [README](../README.md) for commands and [source notes](../evidence/sources.md) for provenance and access limitations.

The offline verifier passed. Five author-run checks also passed: verification with network access disabled, plus rejection of corrupted raw responses, an altered balance summary, an unpinned account read and an incorrect report balance. The [check record](../evidence/checks.json) records those local results; the temporary mutation-test harness is not part of the deliverable.
