# Where Identity MD fits in the agentic finance thesis

**Research date:** 2026-09-30

## Answer

Identity MD appears to fit as **agent-work infrastructure and an application-building / research layer around agentic finance**, rather than as one of the consumer financial providers or payment rails described in Joe Chalom's thesis. Its published materials describe a network where people commission work from distributed agents, including building financial applications and smart-contract-related work; the network also exposes paid job and oracle request interfaces. That could help people build or evaluate agentic-finance applications. This is a fit by function, not evidence that Identity MD is already automating consumer finance or capturing the fee savings in Chalom's forecast.

## Evidence and reasoning

**What the article says (attributed reporting):** COINOTAG's article, which links to Chalom's X post, describes “agentic finance” as software that researches products, negotiates terms, and executes payments. It reports Chalom's estimate of $1.4 trillion in annual savings by 2035 and frames the competition as control of agent wallets, with payment networks, fintechs, exchanges, and settlement rails as contenders. The article also explicitly calls the forecast conditional on agents gaining access to consumer decisions. [COINOTAG article, “A $1.4 Trillion Fee Forecast” and “The Race for the Agent Wallet”](https://en.coinotag.com/sharplink-ceo-ai-agents-1-4-trillion-fees-ethereum)

**What Identity MD says about itself (primary source):** Its API documentation calls IMD “a network to create net new 0 to 1 billion financial applications” and describes it as a consensus layer managed by distributed agents that pairs with smart contracts and blockchains. The docs specify paid requests, job and workflow APIs, oracle requests, and a contributor fleet. [Identity MD API docs](https://imd.fun/docs/)

**Inference:** Taken together, the closest role is upstream infrastructure: coordinating agents and supplying a way to commission financial-application work, research, and on-chain related tasks. The article's center of gravity is downstream autonomous consumer finance—choosing products, moving money, and settlement. Identity MD's published description is adjacent to that stack, but does not establish that it currently provides an agent wallet, connects to users' deposit accounts, negotiates financial terms for consumers, executes consumer payments, or settles those payments on Ethereum. So it is better characterized as a potential builder/enabler of agentic-finance systems than as a demonstrated agentic bank, broker, wallet, or payment rail.

## Facts, inference, and uncertainty

- **Fact:** The article attributes the fee and savings estimates to Chalom and describes his thesis as autonomous financial research, negotiation, and payment execution. These are reported projections, not measured savings.
- **Fact:** Identity MD's own documentation describes an agent-managed network aimed at creating financial applications and documents paid requests, jobs, workflows, and oracle functions.
- **Inference:** Those functions could support creation, operation, or evaluation of applications in the emerging agentic-finance stack. That is a capability-level mapping, not confirmation of adoption or production integration.
- **Uncertainty:** The source material reviewed does not show Identity MD handling live consumer financial accounts, agent-wallet custody, regulated advice, payment execution, or an integration with the firms named in the article. It also does not show what share, if any, of the forecast market Identity MD could address.
- **Source limitation:** X denied direct access to the referenced post in this research session. The article links to the post and summarizes it, but it is secondary and marked as AI-assisted. I therefore attribute the thesis and numbers to the article's account of Chalom, rather than treating the inaccessible post as independently verified. The Identity MD description is sourced directly to its own API docs.

## Sources

1. [COINOTAG, “Sharplink CEO Says AI Agents Could Cut $1.4 Trillion in Fees, With Ethereum (ETH) at the Center”](https://en.coinotag.com/sharplink-ceo-ai-agents-1-4-trillion-fees-ethereum) — secondary coverage linking the target X post.
2. [Identity MD API documentation](https://imd.fun/docs/) — first-party description and API surface.
3. [Joe Chalom's referenced X post](https://x.com/joechalom/status/2102729939543863754) — target source; direct fetch returned HTTP 403, so its text was not independently inspected.
