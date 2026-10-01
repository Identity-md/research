# Tokens bought by `vitalik.eth` on Ethereum mainnet

**Checked 1 October 2026.** The name `vitalik.eth` resolves to [0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045](https://eth.blockscout.com/address/0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045). This report concerns that address, not every wallet associated with Vitalik Buterin.

## Verified paid acquisitions

The following six ERC-20 tokens each have at least one successful Ethereum mainnet transaction initiated by the address in which it provided ETH or another token and received the listed token. The transaction links show the call value and token transfer events. Contract addresses identify the assets more reliably than symbols.

| Token | Ethereum contract | Direct payment and receipt evidence |
| --- | --- | --- |
| OMG (OMG Network) | [0xd26114cd6ee289accf82350c8d8487fedb8a0c07](https://eth.blockscout.com/token/0xd26114cd6ee289accf82350c8d8487fedb8a0c07) | [13 Sep 2018 Kyber trade](https://eth.blockscout.com/tx/0x06d3839b4dde3fee9208b360306fa1c0b33a9f67b0f9cb2145f68a6f65a77480): the address sent 0.01 ETH and received 0.5743490932817 OMG. |
| USDC | [0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48](https://eth.blockscout.com/token/0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48) | [17 Nov 2022 Uniswap swap](https://eth.blockscout.com/tx/0x9847acfee40a9aafab839e9f89c6c12606f3e4f451d0298327f79bc370e7dae6): the address sent about 400 ETH to the router and received 480,000 USDC. A [31 Mar 2025 swap](https://eth.blockscout.com/tx/0x929c667e756b8007801680b2376bf1ccf375c5548cec45e6930fe81437a83288) also shows DOG tokens leaving it and USDC arriving. |
| RAI (Rai Reflex Index) | [0x03ab458634910AaD20eF5f1C8ee96F1D6ac54919](https://eth.blockscout.com/token/0x03ab458634910AaD20eF5f1C8ee96F1D6ac54919) | [21 Jan 2023 Universal Router swap](https://eth.blockscout.com/tx/0xf82bd3d38b4c17821ed0c6d895a1a3951fec3b7f74c7089239e4e55c27f24238): the address sent ETH to the router and received RAI in two transfer events, totaling about 277,392 RAI. |
| DAI | [0x6B175474E89094C44Da98b954EedeAC495271d0F](https://eth.blockscout.com/token/0x6B175474E89094C44Da98b954EedeAC495271d0F) | [11 Mar 2023 Uniswap swap](https://eth.blockscout.com/tx/0x872ef1fca3aacd6ef892511edbc72d79917a59026dfb792d64f4f7c3f1bcdc5c): 10,000 RAI left the address and about 27,178.596 DAI arrived. A [30 Sep 2026 swap](https://eth.blockscout.com/tx/0x9923356a458f1407ebc867eacc0552c45e49a034031ff76f35c69701a4f0b26c) also exchanged ETH for 15 DAI. |
| sUSDS | [0xa3931d71877C0E7a3148CB7Eb4463524FEc27fbD](https://eth.blockscout.com/token/0xa3931d71877C0E7a3148CB7Eb4463524FEc27fbD) | [29 Nov 2025 routed swap](https://eth.blockscout.com/tx/0x89c11f1b56df1f4f729e6dc629b8c5dd578dd03070b5cefadd55c159a3bd1a68): the address supplied 0.002 ETH; the route exchanged WETH through USDT and delivered about 5.556503 sUSDS to it. |
| AZTEC | [0xA27EC0006e59f245217Ff08CD52A7E8b169E62D2](https://eth.blockscout.com/token/0xA27EC0006e59f245217Ff08CD52A7E8b169E62D2) | [12 Jul 2026 Uniswap swap](https://eth.blockscout.com/tx/0x5eee8b6e11e9aca63f45c3703a8294b5993930d65f47aaa9669777c28d969f1b): the call supplied 0.01 ETH, wrapped it to WETH in the route, and delivered about 1,276.306186 AZTEC to the address. |

## How to read this list

**Facts:** Each cited transaction is marked successful by the mainnet explorer and shows the address as initiator. Its call value or token transfer events show consideration, and its token transfer events show the listed ERC-20 arriving at the address. The table gives examples of purchases, not totals bought or current balances.

**Inference:** Calling these *bought* is an inference from consideration leaving and an asset arriving in the same transaction. This is especially clear for the direct Kyber and Uniswap swaps. The ETH amounts sent to routers are gross call values; a router may refund some ETH, so they are not asserted as exact net prices. A wallet transaction does not establish who made the decision or why.

**Excluded as free or non-purchase acquisitions:** An incoming transfer alone is insufficient: token issuers and others can send assets to this public address without its consent. For example, its [ENS claim](https://eth.blockscout.com/tx/0x20189ce02ecf1acd2cb6878245539104ac9dfdc8341297a5a13e00cdd48b0b55) is a claim rather than a purchase. [Wrapping ETH into WETH](https://eth.blockscout.com/tx/0x8ee79b7a033dfee60a21d765857328747f64b2cab2fccf285cceb6e18b1b950d) is a one-to-one conversion, so WETH is not counted as a market purchase here. Native ETH, NFTs, ENS names, gas fees, gifts, and tokens that only passed through a router without reaching this address are outside this ERC-20 list.

**Uncertainty:** This is a list of purchases with direct transaction evidence, not a certified exhaustive history. An off-chain purchase later transferred into the wallet, a swap settled in a separate transaction, a purchase through another wallet or contract, or older non-standard token contracts could add assets that this same-transaction test cannot establish. New transactions or a changed ENS resolution after the check date would also affect an updated report.

**Unanswered questions:** Did any paid acquisitions occur through those other routes? Does the address still own any listed token? The cited transactions do not answer either question.
