# IMD hackathon: consensus top five

## Scope and conclusion

This is a consensus ranking calculated from the four supplied “top 5” ballots. It is **not** an official hackathon result: the ballots are the only voting evidence supplied here, and the public IMD Radar account said that 78 entries were still under review when it described the event. The research cutoff for this report is 28 October 2026 UTC.

The five projects, in order, are:

1. **imdUSD — `@imdusd`**
2. **intelligent dance markets — `@theidmfun`**
3. **robobet — `robobet_fun`, now `@paperclash_xyz`**
4. **IMD Radar — `@imdradar`**
5. **NIGHTSHIFT — `@nightshiftimd`**

## How the ranking was calculated

I treated each supplied list as a ranked ballot. “Most votes” means appearances across the four ballots; placement breaks equal-appearance ties. As a transparent secondary check, I assigned 5 points for first place, 4 for second, 3 for third, 2 for fourth, and 1 for fifth.

| Project | Ballot places | Appearances | Points | Result |
|---|---:|---:|---:|---|
| imdUSD | 1, 1, 1, 1 | 4 | 20 | 1 |
| intelligent dance markets | 5, 2, 2 | 3 | 13 | 2 |
| robobet / Paperclash | 2, 3, 4 | 3 | 9 | 3 |
| IMD Radar | 3, 3 | 2 | 6 | 4 |
| NIGHTSHIFT | 4, 4 | 2 | 4 | 5 |

This also resolves the only meaningful tie: the three-appearance projects rank by total points (and average placement), not by an invented popularity measure. `imdLend`, `@seeronimd`, `@moneycanbuy_fun`, `@theidmfun`’s other aliases, `@ConditionalsImd`, `@Imdirectorb`, and `@swornbyswarm` do not make the top five because they appear on fewer ballots or score below the selected projects.

## Project information and IMD use

### 1. imdUSD — `@imdusd`

**Verified facts.** The project describes imdUSD as a dollar-denominated stablecoin borrowed against staked IMD. Its documentation says users lock sIMD (or deposit IMD that is staked in the same transaction) and borrow imdUSD; price feeds are produced by IdentityMD agents and submitted on chain. The documentation identifies the vault and token contracts on Ethereum mainnet. [imdUSD overview](https://imdusd.com/docs/overview/what-is-imdusd/) [official contracts reference](https://imdusd.com/docs/reference/contracts-and-addresses/)

**How it uses IMD.** IMD is the collateral/economic base: IMD can become sIMD, sIMD backs the debt, and the IdentityMD swarm supplies the price-attestation mechanism. The project’s own site currently describes the core flow as borrow, redeem, price, and liquidation. [imdUSD](https://imdusd.com/)

**Inference and limits.** This is the clearest direct IMD integration among the five because both the collateral and oracle dependency are specified in project documentation. “Stablecoin” describes the intended design, not a guarantee that the market price will always equal one dollar; the documentation itself lists peg, oracle, and liquidation risks. The site also says some live figures/deployment views may be unavailable, so current operational health is not established by this report.

### 2. intelligent dance markets — `@theidmfun`

**Verified facts.** The IMD Explorer’s hackathon review identifies a submitted contract and says the project is a Uniswap v4 hook whose on-chain state is a 16-step sequencer: swaps change the sequencer, with trade size affecting the drum and the market able to rewrite tracks/key. The same record says the submission’s pool is IDM/ETH and that a swarm launch record matched the token and hook review/deployment. [IMD Explorer review record](https://explorer.imd.fun/jobs/0b7a08e0-8b6b-4aaa-9699-781e6d055a4c)

**How it uses IMD.** The project turns IMD ecosystem market activity into music: public project updates describe a radio in which token buys and sells create music, with the IMD swarm setting up the synthesizers; a later account description says the Ethereum IMD pool is one of the radio’s stations. [IMD Radar project post](https://teapawt.org/imdradar) [builder/account description](https://teapawt.org/badfriend)

**Inference and limits.** The evidence supports “IMD ecosystem data/swarm + an on-chain market hook drives creative output.” It does not, by itself, prove continuous volume, listener numbers, or that every advertised station was live throughout the event. “IDM” (the project’s token/name) and “IMD” (the IdentityMD ecosystem) are related in the evidence but should not be treated as interchangeable assets.

### 3. robobet — `robobet_fun`, now `@paperclash_xyz`

**Verified facts.** The IMD Explorer review describes Robobet as an AI-powered crypto trading experience: users deposit USDC, while paid IMD research jobs analyze market data and choose trade direction, leverage, and take-profit target. Its launch record specifies IMD as the paired currency for the token launch. [IMD Explorer review record](https://explorer.imd.fun/jobs/0b7a08e0-8b6b-4aaa-9699-781e6d055a4c) [Robobet token record](https://explorer.imd.fun/jobs/f6bc6667-08db-4622-b3de-f14c7c2dde84)

**How it uses IMD.** IMD is the paid research/oracle-like work layer used to inform the trade, rather than merely a logo or paired token. The builder’s later account description says Paperclash is the next iteration of Robobet, built on Papertrade and IMD, with IMD letting the swarm make trades in one click. [Paperclash/Robobet transition description](https://teapawt.org/noahwbragg)

**Inference and limits.** “Now Paperclash” is supported by the builder’s public description, but the available records do not establish that every Robobet feature carried over unchanged. The Explorer record supports the described IMD research flow; it does not independently prove trading profitability, user funds, or that an agent always makes a correct trade.

### 4. IMD Radar — `@imdradar`

**Verified facts.** The account describes IMD Radar as scanning blockchain and X for new tokens, agents, and signals in the IMD ecosystem, and links `imdradar.site`. It also publicly announced the IMD hackathon and described reviewing 78 entries. [IMD Radar profile and project description](https://teapawt.org/imdradar) [hackathon announcement](https://teapawt.org/imdradar)

**How it uses IMD.** IMD Radar is an ecosystem intelligence and safety/discovery layer: it monitors IMD launches and projects, reports signals, and has described an “IMD Vault” whose rules would lock team tokens and constrain withdrawals. The account says projects passing its review and locking supply can receive an IMD RADAR seal. [IMD Vault announcement](https://teapawt.org/imdradar)

**Inference and limits.** It is reasonable to call Radar IMD-native because its stated subject, review process, and proposed vault are all tied to IMD. However, the accessible evidence does not prove that every Radar feature is a deployed, permissionless contract or that a seal guarantees safety. Its role in hosting/reviewing the hackathon is also a potential source of selection bias, so the ballot consensus should not be read as independent judging.

### 5. NIGHTSHIFT — `@nightshiftimd`

**Verified facts.** NIGHTSHIFT describes itself as a platform where one sentence becomes an AI company, built by the IMD swarm for people and AI agents. Its public changelog/account describes agent companies, games, an IMD-token launchpad, an on-chain token scanner, and a “Night Watch” connected to imdUSD. [NIGHTSHIFT account/changelog](https://teapawt.org/nightshiftimd)

The IMD Explorer’s launch record confirms a NIGHTSHIFT/SHIFT token, 1 billion supply with 18 decimals, an IMD-paired Uniswap v4 pool, and a launch that distributed shares to accepted contributors and paired seats. [NIGHTSHIFT launch record](https://explorer.imd.fun/jobs/dcb84320-d973-47bc-9f1a-dffc2ffd137f)

**How it uses IMD.** IMD is used as ecosystem currency and infrastructure: the launch pairs SHIFT with IMD; the platform says its games and services use IMD; and the Night Watch uses holder-run bots to monitor/liquidate unsafe imdUSD loans, with the stated aim of supporting imdUSD liquidity and safety. [NIGHTSHIFT account/changelog](https://teapawt.org/nightshiftimd)

**Inference and limits.** The launch record verifies deployment and allocation data, while the operational claims about the Night Watch and revenue are project statements. The sources do not establish uptime, profitability, or that all listed services were fully mature at the time of the hackathon.

## Unanswered questions

- The organizer’s final official winner list, if different from this ballot-derived ranking, is not supplied here.
- The ballots do not identify voter counts, voter eligibility, or whether the four names represent equal voting weight; this report therefore treats each ballot as one equal vote.
- For every project, a current chain-by-chain transaction sample would be needed to prove ongoing use rather than a deployed contract, launch record, or project description.
- Ownership of several handles and the relationship between builders and project accounts are not independently verified by the cited records.

