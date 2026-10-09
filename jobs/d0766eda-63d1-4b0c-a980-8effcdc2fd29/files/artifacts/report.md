# Research report: the most viral token the IMD swarm could launch itself

*Prepared 2026-10-09 (UTC). Research only: nothing was deployed and nothing was paid. The deliverable spec, with 5 concepts, the pick, the launch prompt, the tweet and the TL;DR, is in [`swarm-token.md`](swarm-token.md).*

**Labels used throughout:** **[F]** is a fact with a source, **[I]** is my inference or a design choice, **[U]** is uncertain, and **[Q]** is an open question. For each source, *Access* says how I read it: `fetched` means I opened the page or API myself; `snippet` means I saw only the search-engine summary, so treat it as secondary.

## 1. Question and answer in brief

**Question:** what original token, launchable by the IMD swarm on IMD, has the best chance of going viral? And what is its complete `univ4_hook` launch spec?

**Answer:** **MEATBAG ($MEAT)**, a reverse Turing test. Humans each write up to 200 characters a day, and a 7-agent IMD oracle panel signs on chain which entry is most clearly human. That entry wins an ETH pot fed by a 2% hook fee on every trade. The choice comes from three findings:

1. Viral 2025–26 launches turned personal expression or status into an asset (§2).
2. IMD's distinctive capability is a multi-agent judging panel that delivers on chain and can be paid for by a contract in one transaction (§3).
3. Of the five concepts, MEATBAG is the only high-frequency one that runs fully on chain with no admin, using only IMD actions that are live today (§4).

## 2. What went viral onchain in 2025–2026

| # | Pattern | Evidence | Access |
|---|---|---|---|
| 2.1 | **One-click launches at mass scale.** Pump.fun reportedly passed $100M revenue in 217 days. Jan 24 2025 had $15.38M in daily fees, driven by Vine Coin. About 600k tokens launched in Jan 2025, and 12.8M by Oct 2025 (about 50% of Solana tokens). | [F] [CoinDesk](https://www.coindesk.com/markets/2025/02/15/pump-fun-doubles-down-on-memecoin-craze-by-starting-new-mobile-app-as-new-token-launch-hits-record), [Netcoins](https://www.netcoins.com/blog/pump-fun-the-memecoin-launchpad-revolutionizing-solana), [Solflare](https://www.solflare.com/ecosystem/pump-fun-where-memes-meet-markets-on-solana/) | snippet |
| 2.2 | **Celebrity/identity coins.** $TRUMP launched 17 Jan 2025 and was reported at about $11.7B to $15B market cap by 19–20 Jan. In April a "dinner with top holders" promise moved it +50%. | [F] [Forbes](https://www.forbes.com/sites/tylerroush/2025/01/19/donald-trump-launches-trump-meme-coin-token-exceeds-12-billion-market-cap/), [Al Jazeera](https://www.aljazeera.com/economy/2025/1/20/trumps-new-meme-coin-and-crypto-token-soar-on-his-first-day-in-office), [CNBC](https://www.cnbc.com/2025/04/23/trump-coin-surges-50percent-after-president-promises-dinner-with-top-holders.html) | snippet |
| 2.3 | **Social posts as coins, built on Uniswap v4 hooks.** Every Zora post is a 1B-supply coin with an instant Uniswap pool, and the creator earns 1% of trades. After the Base App launched (17 Jul 2025), daily Zora coin creation reportedly went from about 6k to about 50k. | [F] [Blockworks](https://blockworks.com/news/zora-latest-content-coin-fad), [crypto.news](https://crypto.news/zoras-creator-coins-push-base-past-solana-in-daily-token-launches-but-will-it-last/), [CoinGecko](https://www.coingecko.com/learn/what-is-zora-crypto); Zora's v4 hook is listed in [Uniswap/hooklist #1728](https://github.com/Uniswap/hooklist/issues/1728) | snippet |
| 2.4 | **Launch by social reply.** Believe (Apr 2025) launches a coin when you reply to an X post. $LAUNCHCOIN rose more than 20× between 12 and 15 May 2025, to about $354M. | [F] [CoinGecko](https://www.coingecko.com/learn/what-is-believe-token-launchpad), [Incrypted](https://incrypted.com/en/internet-capital-markets-and-believe-app-when-an-explosive-trend-finds-its-launchpad/) | snippet |
| 2.5 | **AI-judged games (the closest analogue).** Freysa (22 Nov 2024, just before the window) let anyone pay a rising fee, from about $10 up to about $450, to persuade an AI to release its pot. 481 attempts failed before one message won 13.19 ETH (about $47k). 70% of each fee went to the pot. | [F] [TradingView/U.Today](https://www.tradingview.com/news/u_today:38a5a3bb7094b:0-someone-just-tricked-ai-agent-into-sending-them-eth/), [Coinspeaker](https://www.coinspeaker.com/freysa-ai-surrenders-47000-prize-clever-user-exploits-language-loophole/), [Jarrod Watts on X](https://x.com/jarrodWattsDev/status/1862299845710757980) | snippet |
| 2.6 | **AI-agent tokens and "fair" launch by activity.** Virtuals Genesis (Apr 2025) allocates by points pledged rather than by speed. VIRTUAL reportedly peaked near $4.5–5B market cap in Jan 2025. | [F] [Messari](https://messari.io/report/understanding-virtuals-protocol-a-comprehensive-overview), [The Defiant](https://thedefiant.io/news/nfts-and-web3/ai-agent-token-virtual-up-on-genesis-updates) | snippet |
| 2.7 | **Status NFTs.** Hypurr was 4,600 free NFTs airdropped in Sep 2025. Its floor was reportedly about $69k at launch with $45M traded on day one. | [F] [Datawallet](https://www.datawallet.com/crypto/hypurr-nfts-explained), [Blocmates](https://www.blocmates.com/news-posts/is-this-the-nft-comeback-hyperliquid-launches-hypurr-collection-on-hyperevm) | snippet |
| 2.8 | **Attention/InfoFi.** Kaito pays for "mindshare". It changed its algorithm after backlash over gaming. | [F] [CoinGecko](https://www.coingecko.com/learn/what-is-kaito-earn-yap-points), [BeInCrypto](https://beincrypto.com/kaito-updates-crypto-mindshare-algorithm/) | snippet |
| 2.9 | **v4 hooks as products.** Uniswap v4 went live on mainnet on 30 Jan 2025. Launchpads (Zora, Clanker, Flaunch) built on hooks. The hooklist reportedly reached about 180 hook projects by late Apr 2026. | [F] [Invezz](https://invezz.com/news/2025/01/31/uniswap-v4-launches-across-multiple-blockchains-including-zora-network/), [Bankless on Clanker v4](https://www.bankless.com/read/clanker-v4-token-creator); hook count from [Bitget Wallet on X](https://x.com/BitgetWallet/article/2054168094604759402) (secondary) | snippet |
| 2.10 | **Burn hooks.** IMD's own POOL4 hook burns 85% of the tokens it trims above a cap, and $IMD supply fell about 29% (10M to about 7.1M) by 25 Sep 2026. | [F] [Bankless](https://www.bankless.com/read/inside-imd-ethereum-s-new-ai-swarm-experiment), [TokenPost](https://www.tokenpost.com/news/technology/24260) | fetched |
| 2.11 | **The cool-down.** Commentators describe a 2025 memecoin "heat death" after the early-year peak. | [F] [BestBrokers](https://www.bestbrokers.com/crypto-brokers/the-heat-death-of-memecoins/) | snippet |

**What I infer from these patterns:**

- [I] The repeatable viral drivers were (a) a near-zero-effort action, (b) an output that is about *you* (your post, your coin, your status), (c) a visible number that goes up, and (d) a story that sounds new in one sentence.
- [I] Pure launch volume (2.1) declined in 2025 (2.11). Mechanics with a recurring reason to come back (Zora posting, Kaito yapping) held attention longer than one-off memes.
- [I] Freysa (2.5) is the strongest proof that people will pay escalating fees to argue with AI judges. Its weakness was a single model with a single loophole.

## 3. What IMD uniquely enables (primary sources)

| # | Capability | Evidence | Access |
|---|---|---|---|
| 3.1 | **The swarm.** There are 2,000 NFT seats, each running an agent with the operator's own Claude or Codex subscription. 372 agents were online on 25 Sep 2026, with an 86% acceptance rate on about 50.7k attempts. On 2026-10-09 the API reported **878 online**. | [F] [Bankless](https://www.bankless.com/read/inside-imd-ethereum-s-new-ai-swarm-experiment); `online` field in `evidence/imd-oracle-check-meatbag-sample-2026-10-09.json` | fetched |
| 3.2 | **The oracle.** Answer types are bool, address, bytes32, uint256, address[] and bytes32[]. `evidence: "panel"` uses off-chain sources. Panel size is 5–100 (minimum 5). Quorum means "every one must match", not a simple majority. `allowAmbiguous` skips the wording and not-answerable screens. Answers are EIP-712 attestations (domain "IdentityMD Oracle" v2), and a callback gets 200k gas. | [F] [imd.fun/docs](https://imd.fun/docs/) (Oracle body, Attestation sections); `evidence/imd-capabilities-2026-10-09.json` (`limits.oracle.request`) | fetched |
| 3.3 | **Paying for the oracle on chain, from a contract.** `Intake.request(action, body, (target, selector), asset, amount)` at `0x1397434cd35e8a9c8ac312a61d3a285eb31dea56` on mainnet costs 0.5 IMD (`0xd34a…63b7`). Action id: `oracle.request@oracle-1`. The body is 1 byte to 16 KiB of JSON. "Jobs, launches and workflows are not sold on chain yet." | [F] [imd.fun/docs](https://imd.fun/docs/) "Pay on chain"; `onchain` block in `evidence/imd-capabilities-2026-10-09.json` | fetched |
| 3.4 | **Oracle track record.** 7,531 requests: 7,321 attested (97.2%), 187 disagreed (2.5%), 20 blocked. The current attester/signer is `0x5598aa9146215bc13eb26f2c692ad1461fd32982`. | [F] `GET https://api.imd.fun/oracle/counts`, `/oracle/requests` → `evidence/imd-oracle-counts-2026-10-09.json` | fetched |
| 3.5 | **Launch policy (mainnet `univ4_hook`).** Policy 34 (2026-10-07): fee tier [12500] = 1.25%, supply 1e9, `initialMarketCaps[ETH] = 10 ETH`, paired currencies ETH, IMD or FWA. The ETH customCap range is 1–1,000 ETH. | [F] `GET https://api.imd.fun/launch/policies` → `evidence/imd-launch-policies-2026-10-09.json`; `evidence/imd-capabilities-2026-10-09.json` | fetched |
| 3.6 | **Precedent launches in the same style.** KING #814/#832 (25% fee decaying to 2.5%, 10 ETH open, LP fee 12500), OG #1040 (policy 34, ETH, tick spacing 60, 10 ETH), HACK #1032 (oracle-judged weekly prize, signer `0x5598…`, a documented re-roll trust assumption), PLEA #1148 (sells gated by oracle panel). Self-referential swarm memes already exist: STRIKE #763, Frogs #618, SWARM #1091. | [F] [launch-814](https://github.com/identity-md-launches/launch-814-custom-token-king-hill), [launch-832](https://github.com/identity-md-launches/launch-832-redeploy-already-built-reviewed), [launch-1040](https://github.com/identity-md-launches/launch-1040-og-symbol-og-the-launch-s-standard-token), [launch-1032](https://github.com/identity-md-launches/launch-1032-tonofhackathons-hack-univ4-hook-launch), [launch-1148](https://github.com/identity-md-launches/launch-1148-build-plea-sepolia-test), [launch-763](https://github.com/identity-md-launches/launch-763-swarm-local-2000) | fetched |
| 3.7 | **Swarm-built sites** are hosted at `<label>.sites.imd.fun` or on IPFS/ENS. | [F] [imd.fun/docs](https://imd.fun/docs/) | fetched |

**Dry run.** I submitted a sample MEATBAG judging question (5 entries, including an injection attempt) to the free `POST /requests/check` endpoint. It returned **no blockers and no suggestions**, and filled in quorum 5, window 24h and validForSeconds 86400 [F, `evidence/imd-oracle-check-meatbag-sample-2026-10-09.json`].

This check is narrower than it sounds. It used the short input form, which has no `definitions` or `allowAmbiguous`, and it returned `judged:false`. So it shows the question shape passes the static checks. It does **not** show that the panel will agree [U].

## 4. Concepts and selection

The five concepts are summarised here; full details are in `swarm-token.md`.

| Concept | Share frequency | Fully on chain, no admin, today? | "Only the swarm" | Main risk |
|---|---|---|---|---|
| **MEATBAG ($MEAT)**: reverse Turing test | Daily, per entrant | **Yes**: oracle.request is sold on chain (3.3) | AI panel judges humanity | Hung juries on a subjective question |
| LAST WORDS ($EPITAPH): oracle-judged FOMO clock | When the clock ends | Yes | Removes last-block sniping | The clock may never end; text routed via hookData |
| DELPHI ($PROPHET): oracle-checked prophecies | When predictions mature | Yes | Turns free text into typed resolutions | Prediction-market regulation; ambiguity |
| THUNDERDOME ($DRAFT): a coin that births coins | Weekly | **No**: launches are not sold on chain (3.3) | Judges *and* launches | Needs an off-chain operator |
| WORK ORDER ($ORDER): holders commission jobs | Weekly | **No**: jobs are not sold on chain (3.3) | Commissions the swarm | Operator, ETH→IMD swap, output quality |

**Why MEATBAG wins:**

1. **Most frequent shareable moment.** Each entry is a self-portrait, and each daily verdict is a status claim [I, following 2.3, 2.4, 2.7].
2. **Freysa's proven pull, without Freysa's single point of failure.** The judge is a panel with a quorum [I, following 2.5 and 3.2].
3. **Buildable with live on-chain IMD actions only** [F, 3.3].
4. **IMD already has the pattern.** It reuses the architecture of #1032 and #1148 [F, 3.6], with one judge request per round so that #1032's re-roll weakness is avoided [I].
5. **The swarm-origin story is literal.** AIs built a game in which AIs decide who is human. `ORIGIN` sits on chain, and the site's "Built by the swarm" page links the launch job, the repo and every oracle request [I].

## 5. Design rationale for the spec

- **Fee and opening price.** 2% ETH hook fee, plus an anti-snipe decay from 25% to 2% over 30 minutes on buys only. This copies the reviewed shape of KING and OG [F, 3.6]. The opening cap of 10 ETH is 1e8 MEAT per ETH, as in policy 34 [F, 3.5].
- **Fee split.** The team takes 25% of the hook fee, so 0.5% of volume. The rest (1.5% of volume) goes to the pot. That is a higher prize share than Freysa's 70% [F, 2.5] [I].
- **Illustration only [I].** At 50 ETH of daily volume, the hook fee is 1 ETH: 0.25 ETH to the team and 0.75 ETH to the pot. Add entry fees of up to 0.82 ETH (Σk·0.001 for k=1..40). The winner gets about 80% of the pot, roughly 1.2 ETH on that day.
- **Entry cap.** At most 40 entries of at most 200 bytes, each placed in `definitions` (up to 64 keys of up to 512 characters). The keeper submits the texts, which are checked against stored hashes. A 40-entry body is about 9 KB, within the 16 KiB limit (measured in scratch) [F/I]. ASCII-only text avoids JSON escaping bugs [I].
- **Slot pricing.** Slot k costs k·0.001 ETH. This rewards early writing, prices out spam, and makes the 40 seats feel scarce [I].
- **Judging.** One judge request per round, panel 7, quorum 4 (a majority; docs allow 2..7) [F, 3.2]. A disagreeing panel causes a carry-over, presented as a "hung jury". That is itself shareable content [I].
- **No admin.** The Intake, IMD and signer addresses are constants. This trades upgradeability for "nobody can change anything", which runs against the docs' advice to keep them as owner settings [F, 3.2 docs "Settings"]. The **sunset rule** handles a dead or rotated signer: after 7 consecutive unsettled rounds, entrants of those rounds get equal pull claims, so ETH is never stranded and no admin is needed [I].
- **Callback limit.** Payouts are pull-based, so the oracle callback stays under its 200k-gas budget [F, 3.2].

## 6. Uncertainty and unanswered questions

- [U] **Panel agreement on taste.** IMD's 2.5% disagreement rate (3.4) is measured mostly on factual questions. Agreement on "most human" could be far lower. Hung juries are handled by carry-over, but frequent ones would hurt engagement.
- [U] **Wording screen.** The real body has `definitions` and `allowAmbiguous: true`, and it was not run through `/requests/check`, because that check accepts only the short input form. It might still be refused at quote time, and the 0.5 IMD would then be lost by the keeper.
- [U] **`definitions` limit.** The docs say "keys 1–64", which could mean 1–64 keys or key length 1–64. Both readings allow 41 keys.
- [U] **Signer rotation.** If IMD rotates the attester or ships `oracle-2`, MEATBAG stops settling and eventually sunsets. That is the deliberate cost of having no admin.
- [U] **Keeper economics.** Judging costs 0.5 IMD (about $5 at the Sept 2026 price of about $9.73 [F, Bankless]) plus gas. The reward is 3% of the pot. On small pots no one may judge, and the pot then carries over.
- [U] **Virality itself** cannot be verified in advance. Every "why people share it" claim is inference from analogues.
- [U] **Ticker collision.** Other tokens named MEAT or MEATBAG may exist on other chains. Not checked.
- [Q] **`<TEAM_WALLET>`** must be supplied by the requester before submission. It is a placeholder by design.
- [Q] Does IMD want a sarcastic "meatbag" brand? An alternative name is in §7.
- [Q] **Legal.** Is a skill contest paying ETH prizes acceptable in the team's jurisdictions? Not assessed.

## 7. Method and limits

- **Method.** Web search for 2025–26 viral mechanics. Fetched IMD primary sources: the docs, `/requests/capabilities`, `/launch/policies`, `/oracle/counts`, `/oracle/requests`, the GitHub API for the launch repos, and one free `/requests/check`. Snapshots are saved in `evidence/` in the repo.
- **What was not done.** No paid requests, no deploys, no contract code. I did not independently review the market figures in §2: rows marked *snippet* come from search summaries.
- **Possible rename** if "meatbag" is judged too edgy: **MOST HUMAN ($HUMAN)**. Same mechanic.
- **Integrity.** A structural check of this file proves its path and bytes, not that the research is true. An independent reviewer should re-verify policy 34 and the signer before launch.
