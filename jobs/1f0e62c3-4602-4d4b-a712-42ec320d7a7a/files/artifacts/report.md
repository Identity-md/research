# Who covers Identity.md ($IMD) on X — evidence report (May 1 – Nov 1, 2026)

## Bottom line
**I could not produce a verified "main list."** X timelines, advanced search and most individual post pages were not readable from this environment (post fetches returned HTTP 402; only web-search snippets and third-party pages were available). The main-list criteria (substantive posts in ≥3 months, ≥5 contributions, one since Sep 1) need per-account post histories that I did not obtain. Rather than invent counts, this report lists **candidate accounts with the evidence actually seen**, and marks every threshold as **unverified**. "No qualifying posts found" below means "not observable with my tools", never "none exist".

## Project identification (fact, from sources read)
- IMD / identity.md: Ethereum AI-agent swarm project; 2,000 identity.md NFTs = swarm seats (ERC-8004 agent identities); token $IMD at `0xD34a99Bc0f67aE1bbd63C660e6d0b0dd03E263B7` (per [Bankless](https://www.bankless.com/read/inside-imd-ethereum-s-new-ai-swarm-experiment), published Sep 25, 2026); predecessor Fren Pet ($FP → $VIBE → $IMD, May 2026). Docs: [imd.fun/docs](https://imd.fun/docs/).
- Disambiguation: "IMD" also means India Meteorological Dept., Azure IMDS, etc.; one analytics page ([ANALYST](https://www.analystrh.com/token/0x5f7bb59365ce557c26dbcaa4ee9d39a4b95b7127)) places "$IMD Identity.md" on Robinhood Chain, which conflicts with the Ethereum mainnet contracts in the official docs — unresolved; treat that page with caution.
- Caution: [@SuperIMD_eth](https://x.com/superimd_eth) ("Superintelligent Identity.md") appears to be a *separate* token ($SIMD) and launchpad built around IMD per a search snippet; not confirmed as official or team. Do not treat it as the official account.

## Official / team accounts (separate section)
| Account | Role | Evidence |
|---|---|---|
| [@surfcoderepeat](https://x.com/surfcoderepeat) (Adam) | Founder / lead developer (Bankless names him lead dev; KuCoin calls him the Fren Pet dev) | Bankless links his posts [2103110920709034175](https://x.com/surfcoderepeat/status/2103110920709034175) (mainnet deployments) and [2102134245086941640](https://twitter.com/surfcoderepeat/status/2102134245086941640). Dates not visible to me. Primary source for roadmap and protocol claims; his "90% of new Ethereum agents" claim is self-reported. |
| [@IdentityUnits](https://x.com/IdentityUnits) | Spin-off NFT collection (787 pieces made by the swarm) | Reported via a search snippet of @SuperIMD_eth; relationship to the team not confirmed. |
An official project handle other than the founder's was **not** confirmed.

## Candidate accounts (all thresholds unverified)
Ranked by apparent usefulness/original contribution. Post counts = **not determined**; months active = not determined.

1. **Bankless / William M. Peaster — [@Bankless](https://x.com/Bankless) (publisher; the article's page lists [@BanklessHQ](https://x.com/BanklessHQ) and author [@wmpeaster](https://x.com/wmpeaster))**
   - Relationship: independent media (disclosed as an outlet; no IMD affiliation seen). 
   - Focus: tokenomics, swarm mechanics, risk. 
   - Evidence: article ["Inside IMD"](https://www.bankless.com/read/inside-imd-ethereum-s-new-ai-swarm-experiment) (Sep 25, 2026) with primary-source data (supply 10M→~7.1M, ~2.3M staked, 380/2,000 seats enrolled, ~86% of ~50.7k attempts accepted, top-10 seats ≈8.5% of accepted work), explicit "unaudited experiment" framing and the POOL4 CappedBurnHook split (85% burn / 6% compute / 4.5% / 4.5%). X thread: [status 2104546260195713113](https://x.com/Bankless/status/2104546260195713113) (a search snippet dates it Sep 28). 
   - Why follow: balanced, sourced overview beyond the founder's posts. Limits: media coverage may be sparse over time; one or two items seen.
2. **Eli5DeFi — [@Eli5defi](https://x.com/Eli5defi)** — KuCoin republished a post of theirs (page timestamp 2026/10/07) summarizing IMD ("wants an idea to become a working financial app"), including a risk list: shared AI mistakes, deployer-dependent signing, unaudited POOL4 contracts with owner powers to withdraw liquidity/sweep staked IMD, Sepolia-only swarm deployment as of Oct 5. Relationship: independent commentator (inferred). Source: [KuCoin](https://www.kucoin.com/news/insight/ETH/6ac64ca138a2640007930118). The original X post URL was not seen.
3. **Ansem — [@blknoiz06](https://x.com/blknoiz06)** — Trader/influencer. Posted "my bet is $IMD" ([status 2106770699637440750](https://x.com/blknoiz06/status/2106770699637440750); a search snippet dates it Oct 4) and is embedded in Bankless ([2103262569263759457](https://twitter.com/blknoiz06/status/2103262569263759457)). Value: attention/sentiment signal, not analysis. Likely fails the "substantive" bar for a main list; undisclosed positions unknown.
4. **notwashed — [@notwashed](https://x.com/notwashed/status/2106085777407164654)** and **nftimm — [@nftimm](https://x.com/nftimm/status/2102344092659134834)** — surfaced only because a GitHub project ([launch-625](https://github.com/identity-md-launches/launch-625-website-showcasing-top-twitter)) lists those posts as top IMD tweets. I did not read the posts; content, dates and relationships unknown.
5. **Dess — [@Despite_zmw](https://x.com/Despite_zmw/status/2104844142777909271)** — snippet: "As more and more media starts talking about $imd. Are you holding or selling?" Sentiment/engagement style; likely non-qualifying.

## Occasional but valuable (non-X, tied to builders — handles unknown)
These are valuable contributions, but I found **no X handles** for the authors, so they cannot be follow recommendations on X:
- **mtezy** (GitHub) — [imd-writeup](https://github.com/mtezy/imd-writeup), snapshot Sep 24, 2026: reverse-engineered due diligence. Findings: pay-per-job swarm not an API marketplace; 0.5 IMD per action via x402/Permit2; 30 fixed skills; of 38 paid orders 7 failed `payment_permission_expired`; work concentration (tokenId 1299: 215 attempts/166 accepted); "early and experimental". Well-supported, critical-but-fair.
- **imtrippin** (GitHub) — [imd-monitor](https://github.com/imtrippin/imd-monitor): unofficial read-only dashboard for worker seats; listed as a community guide in official docs.
- **RobertKodes** (GitHub) — [imd-kit](https://glama.ai/mcp/servers/RobertKodes/imd-kit) SDK/CLI/MCP server (listing seen; not verified further).
If these authors have X accounts, they are worth finding; I did not find them.

## Suggested starter list (provisional; verify before relying)
1. @surfcoderepeat — primary source for protocol changes (official).
2. @Bankless / @wmpeaster — independent, sourced analysis with risk framing.
3. @Eli5defi — concise explainer plus explicit risk list (verify posting history).
4. @blknoiz06 — sentiment gauge only; expect no analysis and possible undisclosed positions.
(Fewer than 5 because I could not substantiate more; padding would be invention.)

## Method and limitations
- Done: 5 web searches (keywords: Identity.md, $IMD, identitymd, swarm/NFT, risks/dashboard) and fetches of Bankless, KuCoin, two GitHub pages. Dates marked "snippet" come from search-result summaries, not from the posts.
- Not done: month-by-month keyword search on X, reply/quote-post discovery, mention-graph crawling, follower/metric collection, contract-address search on X. No follower counts are given because none were verified.
- Unanswered: which accounts meet the 3-month/5-post/post-since-Sep-1 thresholds; the official handle set beyond @surfcoderepeat; whether critics exist on X (the only critical material I found is off-X: Eli5DeFi's risk list via KuCoin and mtezy's writeup).
- Recommended next step: rerun with X advanced search access (e.g. `$IMD since:2026-05-01 until:2026-06-01` per month, plus `0xD34a…63B7`, `imd.fun`, `explorer.imd.fun`), then apply the thresholds.
