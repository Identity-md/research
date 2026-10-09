# Top 10 most controversial Polymarket resolutions (in the vein of "Suitgate")

*Research date: 2026-10-09. Covers markets resolved from June 2024 to June 2026.*

## How to read this report

Each entry is labeled by the kind of claim it makes:

- **FACT (primary):** taken directly from Polymarket's own public Gamma API (`gamma-api.polymarket.com/markets?slug=…&closed=true`), fetched 2026-10-09. This covers the exact question, the rules text (the `description` field), dates, volume, the final outcome (`outcomePrices`, where `["1","0"]` means Yes won and `["0","1"]` means No won) and the UMA proposal/dispute history (`umaResolutionStatuses`). Raw JSON snapshots are in `evidence/gamma-api/`.
- **REPORTED:** facts stated in press coverage, with a link to the source. I did not verify these independently.
- **INFERENCE:** my own reasoning about why a resolution was contested.
- **UNCERTAIN / OPEN:** places where sources conflict or I could not check the claim.

**About "exact criteria".** The quoted rules below are the `description` text Polymarket serves today, copied verbatim with typos kept (for example "is is" and "arial"). Two limits apply:

1. Polymarket sometimes adds "Additional context" or clarification notes to the market page. These notes are **not** in the API description field and only render in the page's JavaScript, so I could not retrieve them. Where press coverage quotes one, I mark it as REPORTED.
2. The API returns the current text. If Polymarket edited a description after launch, the original wording may differ.

**How I ranked them (INFERENCE / judgment).** No official "controversy" metric exists. I combined four things: (a) money at stake, (b) how many UMA dispute rounds the market went through, (c) how much mainstream or crypto-press coverage there was, and (d) consequences such as a lawsuit, a Polymarket override, or oracle reform. Someone weighing these differently could reasonably order the list differently.

---

## Summary table

| # | Market (exact question) | Resolved | Volume (API) | UMA history (API) | Core controversy |
|---|---|---|---|---|---|
| 1 | Will Zelenskyy wear a suit before July? | **No** | $242.2M | 5× proposed→disputed | Widely reported "suit" at NATO; oracle said No |
| 2 | MicroStrategy sells any Bitcoin by May 31, 2026? | **No** | $375.8M | 2× disputed | 8-K showed 32 BTC sold May 26–31; lawsuit filed |
| 3 | US x Iran ceasefire extended by April 22, 2026? | **No** | $203.6M | 3× disputed | Trump announced an extension; Iran's confirmation contested |
| 4 | US x Iran permanent peace deal by June 15, 2026? | **Yes** | $177.4M | 2× disputed | Was a 60-day interim MOU a "permanent" deal? |
| 5 | Ukraine agrees to Trump mineral deal before April? | **Yes** | $7.1M | (not recorded) | UMA whale; no deal existed; Polymarket called it "unprecedented" |
| 6 | Will the U.S. invade Venezuela by January 31, 2026? | **No** | $8.4M | proposed (no dispute) | Maduro captured in a U.S. raid, but ruled "not an invasion" |
| 7 | Will Nicolas Maduro Win the 2024 Venezuela presidential election? (and Edmundo González market) | Maduro **No** / González **Yes** | $2.6M / $1.7M (event $6.15M) | (not recorded) | Official primary source said Maduro won |
| 8 | Was Barron involved in $DJT? | **No** | $1.14M | (not recorded) | Polymarket publicly said UMA was wrong and refunded |
| 9 | Trump declassifies UFO files in 2025? | **Yes** | $16.7M | 2× disputed | No formal declassification; AARO video deemed enough |
| 10 | Gold missing from Fort Knox? | **No** | $3.5M | (not recorded) | Closed months early as No; manipulation alleged |

Honorable mention: **"Israel x Hezbollah Ceasefire extended by April 26, 2026?"** resolved **Yes** ($20.9M, 2× disputed), even though its rules require confirmation from "Hezbollah". It is covered at the end.

---

## 1. "Suitgate": Will Zelenskyy wear a suit before July?

**FACT (primary, API):**
- Slug `will-zelenskyy-wear-a-suit-before-july`.
- Opened 2025-05-22; end date 2025-06-30; closed 2025-07-09.
- Volume **$242,231,180**. Final outcome **No**.
- `umaResolutionStatuses`: proposed, disputed, proposed, disputed, proposed, disputed, proposed, disputed, proposed, disputed.

**Exact rules:**
> This market will resolve to "Yes" if Volodymyr Zelenskyy is is photographed or videotaped wearing a suit between May 22 and June 30, 2025 ET. Otherwise, this market will resolve to "No".
>
> For this market to resolve to "Yes" the images or video must be taken and released within this market's timeframe. The images or video must be authentic, not the result of artificial intelligence or video editing.
>
> The resolution source will be a consensus of credible reporting.

**REPORTED:**
- Zelenskyy appeared at the NATO summit on June 24, 2025, in a black jacket and trousers that many outlets described as a suit.
- UMA finalized "No", citing insufficient "credible reporting consensus" ([Decrypt, 2025-07-09](https://decrypt.co/329210/polymarket-rules-no-237m-bet-zelenskyys); [CoinDesk, 2025-07-07](https://www.coindesk.com/markets/2025/07/07/polymarket-embroiled-in-usd160m-controversy-over-whether-zelensky-wore-a-suit-at-nato)).
- Traders alleged that UMA whales with "No" positions decided the vote. UMA said it saw no evidence of foul play.
- Defenders pointed to a May precedent, where a similar outfit was judged not to be a suit.
- Menswear writer "Derek Guy" weighed in on whether it was a suit ([The Defiant](https://thedefiant.io/news/nfts-and-web3/polymarket-controversy-heats-up-after-the-zelenskyy-suit-market-resolves); [CryptoRank](https://cryptorank.io/news/feed/a2359-polymarket-faces-backlash-over-disputed-200m-zelensky-suit-market)).

**INFERENCE:** The rules never define "suit" and rely only on "a consensus of credible reporting". That left the question of what counts as a suit to UMA token holders.

**UNCERTAIN:**
- Decrypt gives the window as "March 22" to June 30. The API says **May 22**, and I treat the API as authoritative.
- Press reports give different dates for when UMA's "No" became final (July 1 vs. July 8). The API's `closedTime` is 2025-07-09 00:30 UTC.

## 2. MicroStrategy sells any Bitcoin by May 31, 2026?

**FACT (primary, API):**
- Slug `microstrategy-sells-any-bitcoin-by-may-31-2026`, in event "MicroStrategy sells any Bitcoin by ___ ?" (event volume $407.2M).
- Market volume **$375,813,105**. Final outcome **No**.
- UMA history: proposed, disputed, proposed, disputed. Closed 2026-06-04.
- The sibling market "…by June 30, 2026?" resolved **Yes**.

**Exact rules (API description):**
> This market will resolve to "Yes" if MicroStrategy sells any of its Bitcoin by 11:59 PM ET on the date specified in the title. Otherwise, this market will resolve to "No".
>
> The primary resolution source for this market will be information from MSTR and on-chain data, however a consensus of credible reporting will also be used.

**REPORTED:**
- Strategy's Form 8-K (disclosed June 1) reported selling 32 BTC between May 26 and May 31.
- Polymarket's review ended June 3 with "No", after a UMA vote.
- Two Yes holders, William Wood and Thomas Bush, sued Polymarket, CEO Shayne Coplan and CMO Matthew Modabber in New York Supreme Court on July 3, 2026. Their claims include breach of contract, bad faith, unjust enrichment and NY GBL deceptive practices.
- The plaintiffs allege that Polymarket added "clarifying language" that "effectively required public confirmation by the May 31 deadline rather than merely a sale by that date" ([The Block, 2026-07-07](https://www.theblock.co/news/regulation/2026-07-07-two-traders-sue-polymarket-strategy-bitcoin-sale-407368)).
- Polymarket's reported position was that "Confirmation achieved outside of the market's time frame does not qualify" ([Yahoo Finance](https://finance.yahoo.com/markets/crypto/articles/polymarket-faces-backlash-over-microstrategy-215046170.html)).

**INFERENCE:** The description served by the API contains **no** requirement that confirmation happen within the window. The dispute is about the gap between that base text and a clarification that sits outside it.

**OPEN:**
- I could not retrieve the clarification text or its timestamp.
- I found no public outcome for the lawsuit as of the research date.

## 3. US x Iran ceasefire extended by April 22, 2026?

**FACT (primary, API):**
- Slug `us-x-iran-ceasefire-extended-by-april-22-2026`.
- Volume **$203,621,392**. Final outcome **No**.
- UMA history: 3× proposed→disputed. Closed 2026-05-01.

**Exact rules:**
> This market will resolve to "Yes" if there is an official extension of the two-week ceasefire agreement between the United States and Iran announced on April 7, 2026, defined as a publicly announced and mutually agreed extension to the halt in direct military engagement between the United States and Iran, by the specified date, 11:59 PM ET. Otherwise, this market will resolve to "No".
>
> Both extensions of the April 7 ceasefire and new agreements for an extended ceasefire will qualify, even if a brief period occurs during which there is no formal ceasefire in effect after the expiration of the April 7 ceasefire.
>
> If a qualifying agreement is officially reached before the resolution date, this market will resolve to "Yes," regardless of whether the ceasefire extension ultimately takes effect.
>
> An extension of the ceasefire agreement requires clear public confirmation from both the United States government and the government of Iran that they have agreed to halt military hostilities against one another for longer than the initially agreed two-week period, or for an official extension of the ceasefire agreement in place to be otherwise confirmed by an overwhelming consensus of media reporting.
>
> Any form of informal understanding, backchannel communication, de-escalation, or unilateral pause in hostilities without a confirmed agreement on a qualifying extension will not qualify. Similarly, newly agreed-upon humanitarian pauses, limited operational pauses, or temporary tactical stand-downs will not qualify.
>
> A newly agreed-upon broader peace deal will qualify if it includes a qualifying extension of the ceasefire agreement/halt in military hostilities. Agreements that outline future negotiations or de-escalation measures, but do not explicitly commit to extending the ceasefire, will not qualify.
>
> This market's resolution will be based on official statements from the United States government and the government of Iran. However, an overwhelming consensus of credible media reporting confirming that an official ceasefire extension agreement has been reached will suffice.

**REPORTED:**
- On April 21, Trump announced on Truth Social an "indefinite extension at Pakistan's request".
- Pakistan's PM Shehbaz Sharif confirmed the extension on X, and the UN Secretary-General welcomed it.
- The CoinCentral article (2026-04-28) reports that Reuters, AP, BBC and WSJ covered the extension, but it cites no direct Iranian confirmation ([CoinCentral](https://coincentral.com/a-77m-dispute-why-polymarkets-resolution-on-the-us-iran-ceasefire-is-becoming-a-scandal/)).

**INFERENCE:**
- The likely basis for "No" is the clause that *Iran* must also confirm ("mutually agreed", "clear public confirmation from both").
- Yes holders relied on the "overwhelming consensus of media reporting" fallback.
- Iran's unilateral silence versus the U.S. announcement is the crux.

**UNCERTAIN:** I did not find a primary statement from Polymarket or UMA explaining the final "No".

## 4. US x Iran permanent peace deal by June 15, 2026?

**FACT (primary, API):**
- Slug `us-x-iran-permanent-peace-deal-by-june-15-2026-734-856-129`.
- Volume **$177,370,818**. Final outcome **Yes**.
- UMA history: proposed, disputed, proposed, disputed. Closed 2026-06-18. Event total $478.9M.

**Exact rules:**
> This market will resolve to "Yes" if Iran and the United states agree to a permanent peace deal by the specified date, 11:59 PM ET. Otherwise, this market will resolve to "No".
>
> A permanent peace deal refers to any agreement which explicitly indicates that military hostilities between the United States and Iran have ended or will permanently cease, or uses equivalent language clearly signaling a lasting end to military hostilities between the United States and Iran. Agreements that are explicitly temporary or which do not include a definitive agreement to end military hostilities between the US and Iran on a lasting basis (e.g. a temporary extension of the two-week ceasefire agreement announced on April 7, 2026), will not qualify.
>
> A qualifying agreement will be considered to have been established if either of the following conditions are met:
>
> - The United States and Iran each sign or formally adopt a written agreement (e.g. a treaty or multi-point agreement) which meets the above criteria.
>
> - Both the governments of the United States and Iran provide clear public confirmation that a qualifying agreement has been definitively established. Negotiations, statements of progress, or other statements which do not constitute a definitive announcement that a qualifying agreement has been reached will not count.
>
> The primary resolution source for this market will be official information from the governments of the United States and Iran; however, a consensus of credible reporting may also be used.

**REPORTED:**
- Pakistan announced a deal including "immediate and permanent termination of military operations on all fronts".
- Its details showed an interim 60-day framework, with a memorandum of understanding to follow ([The Next Web, 2026-06-15](https://thenextweb.com/news/polymarket-345-million-iran-peace-deal-dispute-uma-whale-voting)).
- Citing Bloomberg, TNW says nine wallets hold more than half the UMA tokens used in dispute votes, and more than 60% of active UMA voters have Polymarket accounts.
- Calcalist describes traders contesting whether the MOU met the "permanent" definition, given continued attacks ([Calcalist/CTech](https://www.calcalistech.com/ctechnews/article/wgc50wv09)).

**INFERENCE:** The text says "permanent end", but the substance was transitional. The rules key on explicit language ("explicitly indicates … will permanently cease"), which favors Yes on the letter and No on the spirit.

**UNCERTAIN:** Sources disagree on when the MOU was signed (June 14 vs. June 17), which matters for a June 15 deadline. I could not resolve this.

## 5. Ukraine agrees to Trump mineral deal before April?

**FACT (primary, API):**
- Slug `ukraine-agrees-to-give-trump-rare-earth-metals-before-april`.
- Opened 2025-02-03; end date 2025-03-31; closed **2025-03-25**.
- Volume **$7,079,947**. Final outcome **Yes**.
- The API has no recorded UMA history for this older market.

**Exact rules:**
> This market will resolve to "Yes" if the United States and Ukraine agree to any deal between February 2 and March 31, 2025, 11:59 PM ET, that explicitly involves Ukrainian rare earth elements. Otherwise this market will resolve to "No".
>
> This includes, but is not limited to, agreements related to the exchange of Ukrainian rare earths for U.S. aid (military or civilian), partnerships involving rare earth metals, future rights to rare earth resources, mining rights, or any other form of cooperation related to rare earth elements.
>
> An announcement of a deal will qualify regardless of if/when the deal is enacted.
>
> The resolution source for this market will be official information from the governments of the US and Ukraine.

**REPORTED:**
- The price went from about 9% to 100% between March 24 and 25. One holder with about 5M UMA across three accounts cast roughly 25% of the votes.
- Polymarket called it "unprecedented", said it was not a "market failure", and issued no refunds ([The Block](https://www.theblock.co/post/348171/polymarket-says-governance-attack-by-uma-whale-to-hijack-a-bets-resolution-is-unprecedented); [CoinDesk, 2025-03-27](https://www.coindesk.com/markets/2025/03/27/polymarket-uma-communities-lock-horns-after-usd7m-ukraine-bet-resolves)).
- The actual US–Ukraine minerals agreement was signed at the end of April 2025, after the window closed.
- The episode is cited as a driver of UMIP-189 / MOOV2, which introduced whitelisted proposers in August 2025 ([web3isgoinggreat](https://www.web3isgoinggreat.com/single/polymarket-governance-attack)).

**INFERENCE:** The broad "any deal … any other form of cooperation" language gave some cover for Yes. But no official US or Ukraine agreement existed by March 25, and the rules name those governments as the resolution source.

## 6. Will the U.S. invade Venezuela by January 31, 2026?

**FACT (primary, API):**
- Slug `will-the-us-invade-venezuela-by-january-31-2026`, in event "Will the U.S. invade Venezuela by...?".
- Volume **$8,368,551**. Final outcome **No**.
- UMA history: proposed only, with no formal dispute recorded. Closed 2026-02-01.

**Exact rules:**
> This market will resolve to "Yes" if the United States commences a military offensive intended to establish control over any portion of Venezuela between November 3, 2025, and January 31, 2026, 11:59 PM ET. Otherwise, this market will resolve to "No".
>
> For the purposes of this market, land de facto controlled by Venezuela or the United States as of September 6, 2025, 12:00 PM ET, will be considered the sovereign territory of that country.
>
> The resolution source for this market will be a consensus of credible sources.

**REPORTED:**
- U.S. forces captured Nicolás Maduro in Caracas on Jan 3, 2026.
- Polymarket's added "Additional Context" said that Trump's statement that the U.S. will "run" Venezuela "does not alone qualify the snatch-and-extract mission to capture Maduro as an invasion" ([DeFi Rate, 2026-01-07](https://defirate.com/news/polymarket-sparks-outrage-settling-10-5m-venezuela-invasion-market-as-no/); [Forbes, 2026-01-07](https://www.forbes.com/sites/siladityaray/2026/01/07/why-polymarket-is-not-paying-bets-on-the-us-invading-venezuela/)).
- Traders called the ruling "Polyscam" ([Futurism](https://futurism.com/future-society/polymarket-venezuela-invasion-bets)).
- Separately, insider-trading allegations surfaced around the "Maduro out" markets.

**INFERENCE:** This is controversial for the opposite reason to the others: Polymarket's own context note, rather than a whale vote, steered the outcome. The fight was over "intended to establish control".

## 7. Venezuela 2024 presidential election

**FACT (primary, API):**
- Event `venezuela-election-winner`, $6,152,241 total.
- "Will Nicolas Maduro Win the 2024 Venezuela presidential election?" resolved **No** ($2.59M).
- "Will Edmundo González win the 2024 Venezuela presidential election?" resolved **Yes** ($1.73M).
- Both closed on 2024-08-06.

**Exact rules (Maduro market; González is identical except for the name):**
> The 2024 Venezuela presidential election is scheduled to take place on July 28, 2024.
>
> This market will resolve to "Yes" if Nicolás Maduro wins. Otherwise, this market will resolve to "No."
>
> This market includes any potential second round. If the result of this election isn't known by December 31, 2024, 11:59 PM ET, the market will resolve to "No."
>
> In the case of a two-round election, if this candidate is eliminated before the second round this market may immediately resolve to "No".
>
> The primary resolution source for this market will be official information from Venezuela, however a consensus of credible reporting will also suffice.

**REPORTED:**
- The CNE declared Maduro the winner with 51.2%.
- The U.S. Secretary of State said González "won the most votes" ([CRS](https://www.congress.gov/crs_external_products/IN/HTML/IN12354.web.html)).
- Critics argued UMA voters ignored the *primary* source ([Bitcoin.com, 2024-08-09](https://news.bitcoin.com/polymarkets-integrity-questioned-over-venezuelan-presidential-election-bet-outcome/); [LessWrong](https://www.lesswrong.com/posts/d4YjM6RWEoT3rBEHe/ambiguity-in-prediction-market-resolution-is-still-harmful)).

**INFERENCE:** On a literal reading, "primary … official information from Venezuela" favors Maduro. The resolution relied on the secondary "credible reporting" clause, which turned a factual question into a legitimacy judgment.

## 8. Was Barron involved in $DJT?

**FACT (primary, API):**
- Slug `was-barron-involved-in-djt`.
- Opened 2024-06-21; end date 2024-06-23; closed 2024-06-26.
- Volume **$1,143,639**. Final on-chain outcome **No**.
- A sibling market, "Did Barron Trump launch $DJT?" ($2.08M), with a stricter "definitive evidence" standard, also resolved No.

**Exact rules:**
> This market will resolve to "Yes" if a preponderance of evidence suggests that Barron Trump was involved in the creation of the Solana token $DJT. Otherwise this market will resolve to "No".
>
> Determination as to whether Barron was involved in the creation of $DJT will be made by this market's decentralized resolver, UMA, and will take into account all available evidence as of 12 PM ET, June 23.

**REPORTED:**
- After UMA voted No, Polymarket posted "We firmly believe that UMA got this resolution wrong" ([The Block, 2024-06-27](https://www.theblock.co/post/302171/polymarket-contradicts-umas-resolution-on-barron-trumps-involvement-with-djt-token)).
- Polymarket then said it was "conclusive" Barron was involved "in some way" and refunded Yes holders without changing the on-chain outcome ([crypto.news](https://crypto.news/polymarket-reverses-oracle-decision-on-barron-trumps-involvement-in-djt-meme-coin/)).

**INFERENCE:** This is the clearest documented case of Polymarket publicly overriding its own oracle. That makes it controversial in both directions: some objected to the oracle's ruling, others to the override.

## 9. Trump declassifies UFO files in 2025?

**FACT (primary, API):**
- Slug `trump-declassifies-ufo-files-in-2025`.
- Opened 2025-04-17; closed 2025-12-10.
- Volume **$16,680,241**. Final outcome **Yes**.
- UMA history: proposed, disputed, proposed, disputed.

**Exact rules:**
> This market will resolve to "Yes" if the Trump administration declassifies any previously classified files pertaining to extraterrestrial life and/or unexplained arial phenomena by December 31, 2025, 11:59 PM ET. Otherwise, this market will resolve to "No".
>
> Announcements of declassifications that are not implemented within this market's timeframe will not count.
>
> The primary resolution source for declassification will be official information from the government of the United States, however a consensus of credible reporting will also be used.

**REPORTED:**
- The trigger was a Pentagon AARO release of a military sensor video. AARO itself called the object "unremarkable".
- Critics said no formal declassification had happened and called the mechanism "proof-of-whales" ([Yahoo Finance](https://finance.yahoo.com/markets/crypto/articles/pentagon-drops-first-ever-alien-160618372.html); [Bitget/CryptoSlate syndication](https://www.bitget.com/news/detail/12560605105613)).
- Polymarket's own newsletter argued the release "quite possibly" counted ([The Oracle by Polymarket](https://news.polymarket.com/p/is-that-a-ufo)).

**INFERENCE:** "Any previously classified files" is a low bar if any released video counts. The dispute was whether that AARO clip was previously classified and whether "the Trump administration declassifies" happened at all.

## 10. Gold missing from Fort Knox?

**FACT (primary, API):**
- Slug `gold-missing-from-fort-knox`.
- Opened 2025-02-17; end date 2025-06-30; but closed **2025-03-11**.
- Volume **$3,518,425**. Final outcome **No**.

**Exact rules:**
> According to the U.S. Government, Fort Knox holds 147,341,858.38 Troy Ounces of Gold (see: https://www.fiscal.treasury.gov/reports-statements/gold-report/21-02.html)
>
> This market will resolve to "Yes" if it is confirmed that Fort Knox holds less than 147,300,000 troy ounces of gold between February 17, 2025, and June 30, 2025, 11:59 PM ET. Otherwise this market will resolve to "No".
>
> If gold is removed from Fort Knox after February 17, 2025, this will not qualify for a "Yes" resolution. If an audit confirms that there is no gold missing from Fort Knox, or that it otherwise contains 147,300,000 troy ounces of gold or more, this market will resolve to "No".
>
> The resolution source for this market will be official information from the U.S. Government, including the Department of Government Efficiency.

**REPORTED:**
- During the Ukraine-minerals fallout, a critic alleged that manipulators resolved this market "No" early in March, "stealing $3.5 million" ([Mitrade, 2025-03-26](https://www.mitrade.com/insights/news/live-news/article-3-720742-20250326)).
- A trader on X complained it was resolved on a "super dumb technicality" ([X post](https://x.com/gigageek0/status/1902537487916175637)).

**INFERENCE:** The early "No" (3.5 months before the deadline) presumably relied on some official statement that the gold was all there, treated as "an audit confirms". Whether that statement was really an audit is the likely crux.

**UNCERTAIN, and the weakest entry:**
- A 2026 explainer ([PolyScope](https://polyscope.pro/8-polymarket-resolution-disputes-that-rocked-trader-trust-in-2026/)) says the dispute hinged on the word "allow". That word does **not** appear in this market's rules, so the explainer may be describing a different Fort Knox market or be wrong.
- I could not confirm the dispute count or the official statement used.

---

## Honorable mention: Israel x Hezbollah Ceasefire extended by April 26, 2026?

**FACT (primary, API):**
- Resolved **Yes**. Volume $20,894,918. UMA history: 2× disputed.
- The rules require "clear public confirmation from both the Israeli government and Hezbollah … or … an overwhelming consensus of media reporting".

**REPORTED:** Critics contrasted it with #3: Hezbollah, which is not a government, did not confirm, yet the market resolved Yes, while #3 resolved No ([polymarkets.co.il commentary](https://polymarkets.co.il/en/news/polymarket-uma-scandal-explained/), a lower-reliability secondary site).

**INFERENCE:** The pairing suggests the "consensus of media reporting" fallback is applied inconsistently.

## Cross-cutting patterns (INFERENCE, supported by the cases above)

1. **Fallback clauses.** Most of these markets have a primary source plus "a consensus of credible reporting" as a fallback (#1, #3, #4, #7, #9, Hezbollah). Disputes cluster on which of the two governs.
2. **Undefined key terms.** Contested words include "suit", "invade", "permanent", "declassifies" and "involved".
3. **Event time vs. confirmation time** (#2): did the event happen in the window, or did it have to be confirmed in the window?
4. **Oracle concentration.**
   - REPORTED: nine wallets hold more than half the voting UMA, and over 60% of active voters have Polymarket accounts (Bloomberg via TNW).
   - REPORTED: the WSJ found the top-10 wallets cast more than half the votes in the average dispute (via [Yahoo Finance](https://finance.yahoo.com/markets/crypto/articles/polymarket-faces-backlash-over-microstrategy-215046170.html)). I did not read these underlying analyses directly.
5. **Off-API clarifications** (#2, #6): Polymarket's "Additional context" notes materially changed outcomes but are not part of the base rules text.

## Unanswered questions

- What exact clarification text was added to the MicroStrategy May 31 market, and when? This is the central fact in the lawsuit; I could not retrieve it.
- What is the status of *Wood & Bush v. Polymarket* after July 2026?
- What official source did UMA rely on for the early Fort Knox "No"?
- When was the US–Iran MOU signed relative to June 15, 2026?
- What were the full UMA vote tallies for each dispute? These could be reconstructed from UMA's Data Verification Mechanism records on-chain; I did not do so.
- Were the Ukraine-minerals, Barron and Venezuela-2024 markets formally disputed? The API's `umaResolutionStatuses` is empty for pre-2025 markets, so the absence of a recorded dispute there is **not** evidence of no dispute.
- Completeness: according to one secondary site, 2026 alone had more than 1,150 contested markets. Lower-coverage disputes may have been more egregious than some entries here, so this list reflects disputes that received **press attention**.
