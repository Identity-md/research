# Swarm Pepe: minting, reveal, and related job status

*Research checked 8 October 2026. Labels distinguish what the sources state from interpretation and gaps.*

## What the collection is

- **Sourced fact:** Swarm Pepe is a collection of 5,000 fully on-chain pixel Pepes on Ethereum. Its site says collection data and artwork are read from the contracts rather than hosted as images, and describes each Pepe as generated from a seed and rendered by contract. ([Swarm Pepe collection site](https://swarmpepe.xyz/), [How it works](https://swarmpepe.xyz/#about))
- **Sourced fact:** The collection contract is `0x999ce0CE8C5f7661e0c74a568FfE27CEB9177bDB`; the site links its mint interaction to the contract’s Etherscan Write Contract page. ([Contract on Etherscan](https://etherscan.io/address/0x999ce0CE8C5f7661e0c74a568FfE27CEB9177bDB#writeContract))

## How mint slots are earned

- **Sourced fact:** The site says wallets earn slots for requests they send the swarm; slots are not sold. It states that wallets can mint up to three Pepes, the owner cannot mint, and there is no mint price (Ethereum gas still applies). ([Mint instructions](https://swarmpepe.xyz/#mint), [Collection details](https://swarmpepe.xyz/#about))
- **Inference:** Eligibility is an allowlist allocation, not a public paid mint: the site directs users to check their wallet’s allocation before minting, and the contract exposes per-wallet allowance/remaining-slot reads. ([Mint instructions](https://swarmpepe.xyz/#mint))

## How `claim()` works

- **Sourced fact:** An eligible wallet can call `claim()` with no arguments on Etherscan to mint its full remaining allocation. The site also describes a `claim(amount)` form for selecting a smaller amount. A successful mint commits the token; it does not reveal the art in that same transaction. ([Mint instructions](https://swarmpepe.xyz/#mint), [Contract on Etherscan](https://etherscan.io/address/0x999ce0CE8C5f7661e0c74a568FfE27CEB9177bDB#writeContract))
- **Sourced fact:** The site reports that minting must be open and the wallet must have slots remaining; a wallet may mint at most three, and the contract owner is excluded. ([Mint instructions](https://swarmpepe.xyz/#mint))

## Reveal window

- **Sourced fact:** Each mint commits to the block immediately after the mint transaction. The site says reveal can be called after that block and within Ethereum’s 8,191-block block-hash history, approximately 27 hours. Anyone can reveal any pending token; tokens not ready or already revealed are skipped. ([How it works](https://swarmpepe.xyz/#about), [Collection site](https://swarmpepe.xyz/))
- **Sourced fact:** After the block-hash history window passes, a still-pending token can remain unrevealed; the contract does not switch to a later random block. ([How it works](https://swarmpepe.xyz/#about))
- **Inference:** The reveal window is a deadline for preserving the committed randomness, not a period during which only the original minter can reveal.

## $OG Uniswap v4 hook and NFT reward distributor

- **Open question:** I could not identify a matching $OG Uniswap v4 hook job or NFT reward distributor job in the accessible IMD Explorer records, so their current statuses cannot be established from the cited evidence. The Explorer does show a completed, paid “Pepe Panels” job for a Swarm Pepe companion site, but that is a different deliverable and says nothing about either requested job. ([Explorer job record](https://explorer.imd.fun/jobs/0f544d5f-567e-40af-806b-70b516d5d37d), [Explorer](https://explorer.imd.fun/))
- **Open question:** The job IDs or exact Explorer links for the $OG hook and NFT distributor are needed to determine whether they are queued, running, complete, failed, or deployed. ([Explorer](https://explorer.imd.fun/))
