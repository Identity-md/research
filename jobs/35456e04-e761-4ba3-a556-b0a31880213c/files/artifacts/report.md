# who holds identity.md?

## answer

At Ethereum block **26,060,938** (2026-09-26 10:09:59 UTC), the eligible top-500 holder base looks like a mixed but active collector/trader cohort with a strong minter-retention core. The evidence for “collector” is that 88 of 102 sampled original recipients still held every identity.md token they received from the zero address, or 86.3%. The evidence for “active” is that only 30 of 500 wallets, or 6.0%, had no successful outgoing Ethereum transaction in the preceding 90 days. The cohort is not uniformly old: the median first normal transaction was 216.4 days ago, while the upper quartile was at least 1,281.0 days old.

That is an inference about wallet behavior, not demographics or identity. The chain does not establish the holders’ occupations, locations, motives, or whether multiple wallets belong to one person.

## measured results

All rows below use the same observation block, **26,060,938**. Ages are elapsed time from that block’s timestamp. “Median” is the ordinary 50th percentile; quartiles use linear interpolation.

| measure | result | distribution / denominator | block |
|---|---:|---|---:|
| current identity.md token holding age | 39.2 days median | p25 10.7; p75 59.4; range 0.01–135.4 days; 1,342 reconstructed current tokens | 26,060,938 |
| wallet-level identity.md holding age | 28.6 days median | age of the oldest currently held identity.md token per wallet; p25 6.7; p75 128.9; range 0.01–135.4 days; 498 wallets reconstructed | 26,060,938 |
| original-recipient full retention | 86.3% | 88 of 102 cohort wallets that received at least one token from the zero address still held every such token | 26,060,938 |
| other ERC-20/NFT position age | 151.5 days median | p25 96.5; p75 479.1; range 0.1–3,374.0 days; 23,863 reconstructed non-identity positions | 26,060,938 |
| typical wallet’s other-position age | 132.8 days median | median of each wallet’s position ages; p25 47.4; p75 336.7; 403 wallets with at least one reconstructed other position | 26,060,938 |
| NFT rapid-turnover proxy | 54.2% | 271 of 500 wallets received and later sent the same ERC-721/ERC-1155 asset within 30 days, with both legs in the trailing year | 26,060,938 |
| wallet age | 216.4 days median | p25 119.5; p75 1,281.0; range 0.01–3,392.9 days; 495 wallets with an indexed normal transaction | 26,060,938 |
| dormant | 6.0% | 30 of 500 had no successful outgoing normal transaction in the trailing 90 days; 12 of those had no indexed outgoing normal transaction at all | 26,060,938 |

The identity.md transfer reconstruction covers 1,342 of the 1,346 tokens represented by the cohort balances at block 26,060,938 (99.7%) and 498 of 500 wallets (99.6%). The four-token difference is an index/pagination reconciliation gap, so the holding-age distribution is not claimed as exact for those four tokens. Other-position histories were requested with a 10,000-record limit per token standard; no wallet hit that limit at block 26,060,938.

## definitions and attribution

The cohort starts with the collection’s holders ordered by reported balance. I screened candidates in that order until 500 eligible wallets remained. This required inspecting ranks through 629 at block 26,060,938. Of those candidates, 129 were excluded as code-bearing accounts; 127 were identified by the explorer as EIP-7702 delegated accounts and 2 as ERC-7760 accounts. No burn address and no publicly tagged centralized-exchange wallet appeared among those screened candidates at block 26,060,938.

Contract status and public labels came from [Blockscout’s indexed holder records](https://eth.blockscout.com/api/v2/tokens/0x0000ec93127baa929e58e97dd0095a2bfb38ec1d/holders). Burn screening used the zero and conventional dead destinations. Exchange screening searched Blockscout public tags for major centralized-exchange labels. This can miss an unlabelled exchange address. EIP-7702 delegation deliberately makes an EOA code-bearing; excluding it follows the requested “exclude contracts” rule but may remove real end-user smart wallets. [EIP-7702](https://eips.ethereum.org/EIPS/eip-7702) explains that distinction.

Collection identity, supply, type, transfers, and holder balances came from [Blockscout’s collection record](https://eth.blockscout.com/api/v2/tokens/0x0000ec93127baa929e58e97dd0095a2bfb38ec1d), its holder and transfer endpoints, bounded to block 26,060,938. The snapshot timestamp and hash came from [Blockscout’s block record](https://eth.blockscout.com/api/v2/blocks/26060938). Normal transactions and ERC-20, ERC-721, and ERC-1155 histories came from Routescan’s Ethereum [Etherscan-compatible account API](https://docs.routescan.io/api-endpoints/etherscan-compatible-api), with `endblock=26060938`.

An identity.md token’s holding age is time since its latest inbound transfer to its snapshot owner. Wallet-level holding age uses the oldest identity.md token currently in that wallet. “Still holds every token received at mint” means every token transferred from the zero address to that wallet was still owned by it at the snapshot; it does not include later purchases.

For other positions, transfers were netted by token contract through the snapshot. A positive reconstructed balance counted as a position, and its age is time since that contract’s latest inbound transfer. This is a reproducible last-receipt age, not tax-lot age or time since the first-ever acquisition. Rebasing assets, non-transfer balance changes, and spam can make transfer-derived balances differ from contract state.

Wallet age is time since the first indexed normal Ethereum transaction involving the address. Five of 500 wallets had no indexed normal transaction at block 26,060,938 and are excluded from that distribution. Dormancy uses the most recent successful outgoing normal transaction, not token-transfer events, signatures, or activity on other chains.

## facts, inference, uncertainty, unanswered

**Facts measured from the stated sources:** the table values, cohort construction, exclusions, reconstruction coverage, and observation block.

**Inference:** high original-recipient retention plus low normal-transaction dormancy is consistent with active collectors who tend to keep identity.md. The broad wallet-age and other-position-age distributions indicate a blend of relatively new wallets and multi-year Ethereum users. The rapid-turnover proxy shows that many wallets also move NFTs quickly, so “collector” does not mean “never trades.”

**Uncertainty:** indexers can omit, lag, or classify records differently. Public exchange labels are incomplete. Strictly excluding delegated code-bearing accounts changes the population. One person can control several wallets, and a wallet can represent several people. Position ages use latest receipt, which biases recurring-balance positions younger than first-acquisition age.

**Unanswered:** the literal share that *bought and sold* an NFT within 30 days is not proven by transfer logs. The measured 54.2% is an upper-bound behavior proxy because gifts, migrations, staking, wrapping, and self-transfers can produce the same in/out sequence. Proving trades would require decoded, venue-aware consideration data and a self-transfer/entity-resolution policy. Nothing in this analysis supports identifying individuals or inferring demographics.

## three x post options

### option a

the median identity.md token has sat in its wallet for 39 days

does that look like a trade or a keep?

number used: **39 days**. source: median age of 1,342 reconstructed current identity.md tokens at Ethereum block 26,060,938.

### option b

86% of sampled original recipients still hold every identity.md they minted

what makes you keep an onchain identity?

number used: **86%**. source: 88 full retainers among 102 cohort wallets that received identity.md from the zero address, at Ethereum block 26,060,938.

### option c

6% of the top holder cohort had no outgoing transaction in the last quarter

what does activity say about conviction?

number used: **6%**. source: 30 dormant wallets among the eligible top-500 cohort using the trailing 90-day definition, at Ethereum block 26,060,938.
