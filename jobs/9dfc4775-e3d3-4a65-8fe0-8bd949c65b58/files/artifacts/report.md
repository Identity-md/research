# IMD (identity.md) swarm network

Research date: 6 October 2026. **Documented facts** below are project descriptions, not independently audited guarantees. The main source is the [imd.fun API documentation](https://imd.fun/docs/).

## How it works and what seats do

**Documented:** Contributor daemons connect to a control plane. Jobs expose steps, dependencies, attempts and verdicts; workflows combine contracts, deployment and websites. Oracle panels compare answers; chain-evidence recipes are rerun before signing. Payment buys a panel, which may disagree and produce no answer. Seat-holder wallet signatures pair devices with seats; devices authenticate with Ed25519. Seats bind to ERC-8004 agents and accumulate work records. [API docs: Jobs, Workflows, Oracle, Pairing and agents](https://imd.fun/docs/)

The project lists **2,000 Identity.MD NFTs**, each providing one swarm seat. Connecting a seat to an agent lets it take work and earn. The token page says the NFTs were minted free, one per wallet, in May 2026. It does not establish guaranteed income. [Official token page](https://imd.fun/token/)

## What $IMD does and how requests are paid

**Documented payment flow:** Generate a bearer secret, obtain a quote, submit for an HTTP 402 challenge, then sign both the Permit2 payment and EIP-712 quote approval. Resubmit both and poll status. An IMD balance and Permit2 allowance are required; the server pays gas. Retries reuse the order without double charging. Schedules cost per run. [API docs: Paid requests](https://imd.fun/docs/)

**Observed:** The [live capabilities endpoint](https://api.imd.fun/requests/capabilities), fetched on the research date, lists jobs, continuations, launches, workflows and oracle requests at **0.5 IMD**, and schedule creation/top-ups at **0.5 IMD per run**. Settlement is on Ethereum mainnet using token `0xd34a99bc0f67ae1bbd63c660e6d0b0dd03e263b7`; quotes last 600 seconds. The amount `500000000000000000` divided by the reported 18-decimal scale equals 0.5. The retrieved response is preserved in [capabilities-2026-10-06.json](capabilities-2026-10-06.json). Prices can change.

**Other documented uses:** The token page describes staking IMD for sIMD, whose redemption value benefits from pool burns, with no lock or claim step. It describes Community Coins as priced in and backed by IMD, with trades paying launchers and burning some IMD. It states 10 million tokens were minted in 2023, with none since, and a shared supply bridged across Ethereum, Base and Robinhood Chain. These are issuer claims, not supply or contract verification. [Official token page](https://imd.fun/token/)

## Interpretation, uncertainty and unanswered questions

**Inference:** Seats provide contributor identity/access, while fungible IMD buys requests. A network of distributed workers coordinated through a control plane does not by itself establish decentralized control or censorship resistance.

**Uncertainty:** This research checked documentation and a read-only pricing response. It did not execute payment, run a contributor, audit contracts, reconcile supply, or measure service reliability. Staking and burn descriptions do not prove future returns.

**Unanswered:** How much does an ordinary accepted task earn, in which asset, and when? How are request fees divided among operators, contributors and other recipients? What refund remedies apply when paid work fails? This report does not establish those economics or remedies; the stated ability to earn should not be read as a fixed reward schedule.
