# Can IMD turn an AI swarm into a network people pay for?

Research snapshot: November 13, 2026. Market figures below use a live quote captured around 14:45 UTC.

Paradigm’s public leaderboards had an IMD-named entry in first place on its prediction-market challenge and fifth on its AMM fee challenge. That is the clearest reason I’m paying attention: this is a live network trying to coordinate people’s AI agents, and it has produced competitive results on public, measurable problems.

The details matter. The leaderboard entries were `imd.fun swarm (seat #662)` and `imd.fun swarm (seat #29)`, both submitted as `@builtbyimd`. Their scores came from simulations, not from live trading or paying customers. The results show the swarm can organize experimentation. They do not yet show that IMD has a durable business or that $IMD captures much of the value.

**What is IMD?**

Identity.md is a service that takes a job in plain English, sends pieces of it to AI agents running on other people’s machines, and publishes the work and its reviews. Today, a user can ask it to build a website or contract, research a question, run an audit, create a token launch, or return an oracle answer. The [API docs](https://imd.fun/docs/api/) price most requests at 0.5 IMD.

Say I want a small Uniswap hook built. I submit the brief and pay 0.5 IMD. IMD’s orchestrator turns it into steps and assigns them to workers whose setup fits the task. A worker runs the task using its operator’s Claude Code or Codex login and quota. For research and audits, the system can send the work to a panel. Another agent reviews results, while a verifier checks the submitted files and, for contract work, rebuilds and tests them. The result and agent reviews get a public job record, with accepted work attached to the agent’s onchain identity.

There are 2,000 identity.md NFT seats. A holder can register one with the network and run its worker on a Mac, PC, or VPS. One seat authorizes one active device. Most tasks go to a single machine; research and audits can go to multiple agents. Agents pass information through the orchestrator and the shared job artifacts. This is coordinated, distributed execution, not agents freely chatting peer to peer. The [official docs](https://imd.fun/docs/) and [worker repository](https://github.com/Identity-md/worker) describe the setup.

The work review is useful, but it is not a universal proof of truth. Code can be rebuilt and tested. The API docs say text outputs are checked for structure, while the content still needs a human or agent to assess its accuracy. An accepted research report can still be wrong.

**Why am I paying attention?**

The interesting distinction from one developer opening several Claude or Codex windows is the source of the extra capacity. Each seat is operated by someone else, on their own hardware and AI account. The network can route a job across those machines, use different tools, and leave a public record of who did and reviewed the work. A solo developer can reproduce parts of this with a good harness. IMD’s bet is that independent operators, persistent identities, reputation, and shared work products add capacity and accountability that one person’s setup cannot easily supply.

That advantage is still conditional. IMD runs the scheduler and verifier. If the service goes down or routes work badly, the workers cannot coordinate through the product. And lots of agents using the same model can still make the same mistake. The network creates more parallel attempts; it does not make their judgments independent by default.

There is a working product behind the pitch. The [docs](https://imd.fun/docs/) and worker client support job intake, agent registration, model setup, the explorer, deployments, and reviews. On November 13, [IMD’s own API](https://api.imd.fun/swarm) reported 1,084 enrolled seats, 1,042 agents online, and 16,132 completed jobs. Those are the project’s counters, not an independent count of unique operators, paying customers, or successful outcomes. I did not find a public breakdown of repeat customers, outside revenue, or job payments by customer.

There is some outside building. The community-run [Identity MD hackathon](https://www.imdradar.site/hackathon) closed on October 21 and listed projects using the protocol. Its $10,000 prize pool was community funded, and the rules assigned some judging to IMD agents. That is evidence of builders experimenting with the product, not proof they stayed or became paying customers.

**What the competition results actually show**

On November 13, Paradigm’s [prediction-market leaderboard](https://www.paradigm.xyz/puzzles/prediction-market-challenge) ranked `@builtbyimd`, named `imd.fun swarm (seat #662)`, first with a mean-edge score of 111.402. That entry was created November 10 and had 27 attempts. The [AMM fee leaderboard](https://www.paradigm.xyz/puzzles/amm) ranked `@builtbyimd`, named `imd.fun swarm (seat #29)`, fifth at 528.333, less than 0.2 points behind the leader. It had been run through 1,000 simulations and submitted 15 times.

These are strong placements, but they are not two wins in the same sense. The prediction entry was first on the board at this snapshot. The AMM entry was fifth. Ranks and scores move as contestants submit, so the date matters.

The prediction puzzle asks for a Python strategy that quotes passive orders in a simulated binary YES market. The market has a latent fair value, retail orders, an informed arbitrageur, and a competing market maker. Each strategy is scored by its average edge across 200 simulations. In plain terms, the puzzle asks whether the bot can make money from retail trades without giving too much back to better-informed traders. There is no real customer order flow or capital at risk. The [public simulator and rules](https://github.com/danrobinson/prediction-market-challenge) make the task reproducible.

The AMM challenge asks a Solidity strategy to set buy and sell fees for a constant-product pool. It competes against a fixed 30-basis-point pool. Arbitrageurs trade against stale prices; retail flow goes to the cheaper pool. The score is average trading edge over randomized simulations. It tests whether a fee policy can attract retail volume while limiting arbitrage losses, not whether IMD’s own pool earns those returns in the market. The [challenge code](https://github.com/benedictbrady/amm-challenge) publishes the mechanics and scoring.

What did the swarm contribute? Taylor, a contributor to IMD, said in a [November 6 post](https://x.com/taylor_/status/2118787746579742768) that 202 agents had worked on the prediction task, trying ideas in sequence and feeding the best strategy into the next round. Taylor reported 21 attempts and $14.52 in cost, and said no human wrote the strategy. Those are team-reported figures. Adam’s [November 6 post](https://x.com/surfcoderepeat/status/2118779774403231801) said he was actively testing and improving the new `/goal` feature, so the fair description is a human-directed experiment in which agents generated and compared strategies. The current leaderboard row later showed 27 attempts. The team has not published a model-by-model breakdown, a full compute-cost accounting, or an account of human hours for the result.

This is still a good demonstration. The system appears to turn a high-level goal into parallel experiments, compare results, and promote promising work quickly. It also surfaced a small network effect: Adam said other contestants were reading IMD’s public submissions and building on them. That is a report from the founder, not a measured adoption metric, but it is a concrete example of open work feeding work outside the network.

The limits are just as concrete. A single benchmark can reward tuning to its simulator. Paradigm’s score says little about code quality in production, independent customer demand, or whether the swarm can solve a less measurable task. The results also do not prove that 202 independent agents each contributed a distinct useful insight. They show a competitive strategy carrying an IMD seat’s name, with the team’s account of how it was produced.

**Why the swarm thesis could matter**

Matt Huang’s [November 10 post](https://x.com/matthuang/status/2120209025099043286) describes “swarm riders”: people who can set objectives, design evaluations, and direct large groups of agents toward useful work. He argues this is a new management skill and says the best practitioners he knows spend far more on models than typical developers. That spending estimate is his claim, not an independently audited statistic.

The connection to IMD is conceptual. Huang’s post mentions teams at Tempo and Paradigm, but does not mention Identity.md. I found no endorsement, investment, or partnership with IMD in that post. Paradigm hosting the competitions is not evidence that Paradigm backs the entrant.

The category could matter if more capable models make parallel experimentation cheap, while the hard part shifts to breaking a goal into useful tasks, checking the results, and deciding what to keep. IMD’s strongest angle is that it is building those pieces as a public network: outside operators bring compute and model access, work is assigned and reviewed, and accepted contributions can build onchain reputation. If different owners and skills make the network broader than one company’s agent fleet, that could be valuable.

IMD also seems unusually good at shipping and iterating. The worker, public explorer, job records, token launches, and the Paradigm experiments are visible today. The public [worker repository](https://github.com/Identity-md/worker) describes an installable client that runs the operator’s own Claude Code or Codex runtime. This is more tangible than a roadmap alone. The counterweight is that the core orchestration remains a service operated by the project, and the network’s reported scale does not yet tell us how much useful work outside customers are buying.

**What does this mean for the token?**

The official Ethereum contract is [`0xd34a…63b7`](https://etherscan.io/token/0xd34a99bc0f67ae1bbd63c660e6d0b0dd03e263b7). The same token lineage is on Base at [`0xff0c…e105`](https://basescan.org/token/0xff0c532fdb8cd566ae169c1cb157ff2bdc83e105) and Robinhood Chain at [`0x5f7b…7127`](https://robin.etherscan.io/token/0x5f7bb59365ce557c26dbcaa4ee9d39a4b95b7127). The project says there is one supply across the three chains, with bridged tokens backed by tokens locked on Base.

The history is real and somewhat unusual. Fren Pet launched on Base in August 2023 as $FP. The project opened a LayerZero bridge to Ethereum in October 2025; in 2026 the name changed from FP to VIBE to IMD. The [current token page](https://imd.fun/token/) calls it the same coin, and I found no holder swap or conversion event. The 2,000 identity.md NFTs were a separate free mint in May 2026. Fren Pet’s [original token docs](https://fren-pet-docs.vercel.app/fp) say all FP was distributed through a BaseSwap pool and the team received no pre-allocation. [Bankless](https://www.bankless.com/read/inside-imd-ethereums-new-ai-swarm-experiment) identifies Adam, @surfcoderepeat, as Fren Pet’s lead developer. So $IMD is legacy FP exposure with a new product and use case attached, not a fresh token launch.

At about 14:45 UTC on November 13, [DEX Screener’s Uniswap v4 pool](https://dexscreener.com/ethereum/0xb07d640fd9e2eb9dc81b953c8e4fd006bdfeaf276010fb5418eb763ca15abfb3) quoted IMD around $2.88. The [Base origin contract](https://basescan.org/token/0xff0c532fdb8cd566ae169c1cb157ff2bdc83e105) had about 7.081 million tokens outstanding. Ethereum and Robinhood balances are bridged representations backed by Base tokens in the bridge, so adding all three chains’ contract supplies would double count. At that price, the project-wide value against currently outstanding supply was about $20.4 million.

There is a market-data wrinkle. DEX Screener’s [Ethereum-only contract view](https://dexscreener.com/ethereum/0xd34a99bc0f67ae1bbd63c660e6d0b0dd03e263b7) showed about $12.2 million because it reads roughly 4.24 million tokens on that contract. The [official docs](https://imd.fun/token/) describe one global supply. For a project-wide figure I use the Base supply as the anchor and do not add the bridged copies. The team says 10 million were minted at launch and there has been no net new issuance. Roughly 2.92 million are already burned. Against currently outstanding supply, both circulating market cap and a current-supply FDV are about $20.4 million. If a vendor calculates FDV against the original 10 million issuance, it gets about $28.8 million. That counts tokens the project says are gone, rather than an upcoming unlock. There is no scheduled unlock or future emissions schedule in the docs.

The token has live utility. Jobs, launches, and oracle questions cost 0.5 IMD, paid to the network treasury. Users therefore need IMD to use the service, and the [API docs](https://imd.fun/docs/api/) say payments fund network operations. Operators, however, run their own model plans and quotas. The docs promise reputation and a share of tokens launched by the swarm: 8% goes to seats online when a launch is admitted, and another 2% to wallets with accepted work on it. They do not promise a fixed wage for each ordinary job. I found no public accounting of fee revenue or how much the treasury retains versus spends.

There is also a live Uniswap v4 hook called POOL4. Its [docs](https://pool4.imd.fun/docs) say the pool charges a 1% swap fee, which is protocol revenue. That fee is separate from the burn and is not automatically paid to holders. When the hook trims IMD inventory above its pool cap, its stated split is 85% burned, 4.5% to sIMD stakers, 6% reserved for a future bond program, and 4.5% reserved for future NFT inference nodes. Staking is live; bonding and node payouts are still planned. The docs also say the pool owner can close the market and withdraw its liquidity, and the vault owner can pause or sweep funds. The contracts are unaudited.

The bull case is that real jobs create recurring demand for IMD, while launches and pool trading deepen the token’s role and drive burns or staking rewards. The weakness is the gap between product usage and token value. A customer buying 0.5 IMD to open work creates demand at the point of use, but that fee goes to a project treasury and may be spent. There is no automatic claim on business profits, and the 1% pool fee is not a holder distribution. A useful agent network would not automatically make this token a good investment.

**What I’d still want to understand**

I would want to see recurring outside customers, meaningful payment volume, and evidence that users return because the work is good. I would also want an independently reproducible record of the competition strategy, including the models, human input, compute costs, and frozen code for the top entries. For the token, I would want onchain reporting that ties task payments, pool fees, treasury spending, burns, and staking to one clear set of value flows.

My view would strengthen if IMD publishes repeat-customer and revenue data, shows that genuinely distinct operators keep winning useful work, and makes its fee and treasury flows easy to audit. It would weaken if the public job counts mostly reflect internal experiments, the agent fleet depends on a small number of operators, or usage grows without creating sustained demand or value capture for $IMD.

**Questions I’d send the team**

- Of completed jobs and 0.5 IMD payments, what share came from unaffiliated customers, and how many paying wallets returned for a second job?
- How many distinct people or organizations operate the 1,084 enrolled seats, and what do workers earn per accepted job after their model and hosting costs?
- Can you publish the frozen code, model mix, human contribution, and full cost breakdown for Paradigm seats #662 and #29, with a reproducible rerun?
- Where do task payments and the 1% POOL4 fee go in practice, and which multisig or owner currently controls the pool, vault, and reward destinations?
