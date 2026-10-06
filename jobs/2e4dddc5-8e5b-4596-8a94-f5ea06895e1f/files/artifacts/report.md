# Ten contested Polymarket resolutions, as yes/no questions for the IdentityMD oracle

Prepared 2026-10-06. Reviewed by no one but the author.

## What this answers

You asked for the ten most controversial Polymarket resolutions decided through UMA, like "suitgate", turned into plain yes/no questions you can ask the IdentityMD oracle. For each market below you get:

- **Ask the oracle**: a short question.
- **Ask with the rules**: the same question with the market's own resolution text. Use this one if you want to test how the oracle reads the rules, not just whether it remembers the news.
- **What happened**: the actual outcome, with sources.
- **Labelled notes** on facts, inferences, and what's still uncertain.

### How to read the labels

- **FACT**: stated in a primary source (Polymarket's own market data) or in at least one named news outlet, which is linked.
- **INFERENCE**: my reading of the rules against the facts. It is not a source claim, and it does not say how the market *should* have resolved.
- **UNCERTAIN**: the sources conflict, or I couldn't verify the point.

### Primary source

Market titles, rule text, outcomes, volumes, close times and the UMA status history all come from Polymarket's public Gamma API (`https://gamma-api.polymarket.com/events?slug=<slug>`), pulled on 2026-10-06. A trimmed copy is saved in [`evidence/polymarket-gamma-snapshot.json`](evidence/polymarket-gamma-snapshot.json). In that API, an outcome price of `1` means the outcome won. Volumes are in USD and rounded.

### How the ten were chosen

There is no official "most controversial" list, so the ranking is my judgment. A market made the list if it had all three of the following:

1. Named news coverage of a fight over how it resolved, not just over the event itself.
2. A UMA dispute or vote on record, or Polymarket publicly overriding or clarifying the result.
3. Meaningful volume.

They are ordered roughly by volume times how much coverage the dispute got. Two cases that nearly made it are listed at the end.

---

## Quick list (copy and paste)

| # | Ask the oracle (answer Yes or No) | Polymarket's actual result |
|---|---|---|
| 1 | Did Volodymyr Zelenskyy wear a suit, as photographed or videotaped, between May 22 and June 30, 2025? | **No** |
| 2 | Was the April 7, 2026 US–Iran ceasefire officially extended by April 22, 2026? | **No** |
| 3 | Did the US and Iran agree to a permanent peace deal by June 15, 2026? | **Yes** |
| 4 | Was TikTok banned for download and/or use by most Americans, under US law, before May 2025? | **Yes** |
| 5 | Did the Trump administration declassify previously classified UFO/UAP files in 2025? | **Yes** |
| 6 | Did the US invade Venezuela (start a military offensive meant to control Venezuelan territory) by January 31, 2026? | **No** |
| 7 | Did the US and Ukraine agree to a deal involving Ukrainian rare earths between Feb 2 and Mar 31, 2025? | **Yes** |
| 8 | Did Edmundo González win the July 2024 Venezuelan presidential election? | **Yes** (González Yes, Maduro No) |
| 9 | Was the missing OceanGate Titan submersible, meaning its passenger cabin and not just debris, found by June 23, 2023? | **Yes** |
| 10 | Is there a preponderance of evidence that Barron Trump was involved in creating the Solana token $DJT (as of June 23, 2024)? | **No** (UMA), but Polymarket said UMA got it wrong |

---

## 1. "Suitgate": Zelenskyy's suit

- **Ask the oracle:** Did Zelenskyy wear a suit between May 22 and June 30, 2025? Yes or No.
- **Ask with the rules:** "This market will resolve to 'Yes' if Volodymyr Zelenskyy is photographed or videotaped wearing a suit between May 22 and June 30, 2025 ET… The resolution source will be a consensus of credible reporting." On June 24, 2025, at the NATO summit, he wore a black jacket, matching trousers and a collared shirt with no tie. Yes or No?
- **What happened:** Resolved **No** on 2025-07-09. Volume was about **$242M**.

**FACT**
- Polymarket's data shows the rule text above and a **No** result.
- The UMA status history records five rounds of proposal and dispute: `proposed, disputed` ×5 ([API snapshot](evidence/polymarket-gamma-snapshot.json); [event page](https://polymarket.com/event/will-zelenskyy-wear-a-suit-before-july)).
- Decrypt reports that UMA first ruled "No" on July 1, the final "No" came on July 9, and more than 40 outlets, including Reuters and the BBC, described the outfit as a suit ([Decrypt](https://decrypt.co/329210/polymarket-rules-no-237m-bet-zelenskyy-suit?amp=1)).
- The Defiant reports that the result was first "Yes" and was flipped after disputes. It also reports that what appeared to be the designer's comms agency said the outfit "can indeed be referred to as a suit" ([The Defiant](https://thedefiant.io/news/nfts-and-web3/polymarket-controversy-heats-up-after-the-zelenskyy-suit-market-resolves)).

**INFERENCE**
- The fight is over a definition: does "suit" require a traditional matched suit, or is it whatever a consensus of reporting calls a suit? The rule names "consensus of credible reporting" as the source, and that reading favors Yes.

**UNCERTAIN**
- Decrypt gives the window start as March 22, but the API rule text says May 22. I used the API.
- Sources disagree on whether an early "Yes" proposal was ever final.

## 2. US–Iran ceasefire extended by April 22, 2026

- **Ask the oracle:** Was the April 7, 2026 US–Iran ceasefire officially extended by April 22, 2026? Yes or No.
- **Ask with the rules:** The rules ask for "clear public confirmation from both the United States government and the government of Iran… **or** for an official extension… to be otherwise confirmed by an overwhelming consensus of media reporting." Unilateral pauses and informal understandings do not count. Trump announced an extension before the deadline. Yes or No?
- **What happened:** Resolved **No**. That sub-market had about **$204M** volume; the whole event had about $210M.

**FACT**
- The API shows **No** with three rounds of proposal and dispute, and a close time of 2026-05-01 ([snapshot](evidence/polymarket-gamma-snapshot.json); [event](https://polymarket.com/event/us-x-iran-ceasefire-extended-by)).
- Secondary sources say Trump extended the ceasefire on Truth Social on April 21 and Pakistan welcomed it, but Iran's government did not confirm it in its own voice ([polymarkets.co.il explainer](https://polymarkets.co.il/en/news/polymarket-uma-scandal-explained/); [The Next Web](https://thenextweb.com/news/polymarket-345-million-iran-peace-deal-dispute-uma-whale-voting)).

**INFERENCE**
- The "overwhelming consensus of media reporting" clause is a second path to Yes. That makes the No result arguable, and it is the main source of the dispute.

**UNCERTAIN**
- Whether Iran ever gave any official confirmation. I did not check Iranian government sources.

## 3. US–Iran "permanent peace deal" by June 15, 2026

- **Ask the oracle:** Did the US and Iran agree to a permanent peace deal by June 15, 2026? Yes or No.
- **Ask with the rules:** The deal must "explicitly indicate that military hostilities… have ended or will permanently cease". Explicitly temporary agreements do not qualify. It must be signed or formally adopted by both sides, or clearly confirmed by both governments. Reports from around June 14–16 described a 60-day interim framework that also contained "permanent termination" language. Yes or No?
- **What happened:** Resolved **Yes** on 2026-06-18. The June 15 sub-market had about **$177M** volume; the whole event had about **$479M**.

**FACT**
- The API shows **Yes**, with two rounds of proposal and dispute ([snapshot](evidence/polymarket-gamma-snapshot.json); [event](https://polymarket.com/event/us-x-iran-permanent-peace-deal-by)).
- Ynet reports a memorandum on June 14 calling for a final agreement "within 60 days", a signing on June 17, and losing bettors threatening to sue. It also reports that seven whale voters held 50.3% of the vote and all voted Yes ([Ynet](https://ynetnews.com/business/article/b1ajjg97gx)).

**INFERENCE**
- A 60-day path toward a final agreement looks like the kind of "explicitly temporary" deal the rules exclude. The "permanent termination" wording points the other way. Both readings are defensible.

**UNCERTAIN**
- The sources disagree on dates and on whether Iran publicly confirmed the deal.
- I could not confirm the whale-vote figures from on-chain data.

## 4. TikTok banned before May 2025

- **Ask the oracle:** Was TikTok banned for download and/or use by most Americans, by a ban mandated by US law, before May 2025? Yes or No.
- **Ask with the rules:** The rules require a ban "mandated by US federal law, policy, or the court system" that has "gone into effect". TikTok went dark on January 18–19, 2025, as the law took effect. It returned within about a day after Trump said he would delay enforcement. Yes or No?
- **What happened:** Resolved **Yes** on 2025-01-22. Volume was about **$120M**.

**FACT**
- The API shows the rule text and a **Yes** result ([snapshot](evidence/polymarket-gamma-snapshot.json)).
- DL News reports that UMA voters argued the law took effect and enforcement was "moot". It also reports a petition from No bettors who said TikTok shut itself down preemptively ([DL News](https://www.dlnews.com/articles/markets/tiktok-disappearance-sparks-polymarket-petition)).

**INFERENCE**
- The rules define "banned" by its effect on users ("banned for download and/or use"). The app really was unavailable for a short time, and it was still unavailable for download for some time afterward.
- The weaker point for Yes is whether a self-imposed shutdown counts as a ban "mandated by" law.

## 5. UFO files declassified in 2025

- **Ask the oracle:** Did the Trump administration declassify any previously classified UFO/UAP files in 2025? Yes or No.
- **Ask with the rules:** The market needs "any previously classified files pertaining to extraterrestrial life and/or unexplained aerial phenomena" to be declassified by December 31, 2025. The primary source is official US information. The evidence offered was AARO adding items to its public "Official UAP Imagery" page. Yes or No?
- **What happened:** Resolved **Yes** on 2025-12-10, three weeks before the deadline. Volume was about **$16.7M**.

**FACT**
- The API shows **Yes** with `proposed, disputed, proposed, disputed` ([snapshot](evidence/polymarket-gamma-snapshot.json)).
- CryptoSlate reports that the cited evidence was AARO imagery items from 2022, that there was no White House declassification order, and that community backlash followed ([CryptoSlate](https://cryptoslate.com/polymarket-faces-major-credibility-crisis-after-whales-forced-a-yes-ufo-vote-without-evidence/)).

**INFERENCE**
- The rules don't require a White House order; "any previously classified files" is broad. So the real question is whether the AARO items had ever been classified. CryptoSlate says that wasn't shown.

**UNCERTAIN**
- I could not verify whether the AARO items were previously classified.

## 6. US "invasion" of Venezuela by January 31, 2026

- **Ask the oracle:** Did the US invade Venezuela, meaning start a military offensive intended to establish control over any part of Venezuela, by January 31, 2026? Yes or No.
- **Ask with the rules:** The rule is "commences a military offensive intended to establish control over any portion of Venezuela". On January 3, 2026, US forces captured Nicolás Maduro in Caracas and left; Trump said the US would "run" Venezuela. Yes or No?
- **What happened:** Resolved **No**. The January 31 sub-market had about **$8.4M** volume; the event had about $14.2M.

**FACT**
- The API shows **No** with a single `proposed` status, which means the UMA proposal was not disputed ([snapshot](evidence/polymarket-gamma-snapshot.json)).
- SAN quotes Polymarket's clarification that Trump's "run Venezuela" statement "does not alone qualify the snatch-and-extract mission… as an invasion" ([SAN](https://san.com/cc/whats-an-invasion-gambling-sites-definition-costs-gamblers-millions/)).

**INFERENCE**
- This one was contested through Polymarket's clarification and public backlash, not a UMA vote. It is on the list for the size of the backlash, not for whale voting.

## 7. Ukraine–US minerals deal before April 2025

- **Ask the oracle:** Did the US and Ukraine agree to a deal explicitly involving Ukrainian rare earths between February 2 and March 31, 2025? Yes or No.
- **Ask with the rules:** "An announcement of a deal will qualify regardless of if/when the deal is enacted… The resolution source… will be official information from the governments of the US and Ukraine." Yes or No?
- **What happened:** Resolved **Yes**, closing on 2025-03-25. Volume was about **$7.1M**.

**FACT**
- The API shows **Yes** ([snapshot](evidence/polymarket-gamma-snapshot.json)).
- The Block and CoinDesk report that no official agreement existed when the market resolved ([The Block](https://www.theblock.co/post/348171/polymarket-says-governance-attack-by-uma-whale-to-hijack-a-bets-resolution-is-unprecedented); [CoinDesk](https://www.coindesk.com/markets/2025/03/27/polymarket-uma-communities-lock-horns-after-usd7m-ukraine-bet-resolves)).
- Polymarket called it "an unprecedented situation" and said it would not refund bettors.
- Cointelegraph, citing an X researcher, reports that one whale with about 5M UMA across three accounts cast about 25% of the votes ([Cointelegraph](https://cointelegraph.com/news/polymarket-trump-ukraine-bet-whale-governance-attack)).

**INFERENCE**
- On the rules as written and the facts as reported, this is the clearest case of a resolution that doesn't match the evidence.

**UNCERTAIN**
- The whale's identity and positions come from a third-party analysis. I did not check them on-chain.

## 8. Venezuela 2024 presidential election winner

- **Ask the oracle:** Did Edmundo González win the July 28, 2024 Venezuelan presidential election? Yes or No. (You can also ask: did Nicolás Maduro win it?)
- **Ask with the rules:** Venezuela's electoral council (CNE) declared Maduro the winner. Opposition tally sheets showed González winning. Per news reports, the rules named official Venezuelan information as the primary source and said "a consensus of credible reporting will also suffice". Who won?
- **What happened:** González resolved **Yes** and Maduro **No**, on 2024-08-06. The event had about **$6.2M** volume.

**FACT**
- The API shows González Yes and Maduro No ([snapshot](evidence/polymarket-gamma-snapshot.json)).
- Criptonoticias and Bitcoin.com covered the backlash ([Criptonoticias](https://www.criptonoticias.com/comunidad/polymarket-cierra-capitulo-elecciones-venezuela-ganador); [Bitcoin.com](https://news.bitcoin.com/polymarkets-integrity-questioned-over-venezuelan-presidential-election-bet-outcome/)).

**UNCERTAIN**
- The API's event description no longer contains the per-market rule text, so the source clause quoted above comes from news reporting, not Polymarket.

**INFERENCE**
- The answer depends on whether "official information" (CNE) beats "credible reporting". It is a test of how the oracle ranks sources.

## 9. OceanGate Titan submersible "found" by June 23, 2023

- **Ask the oracle:** Was the Titan submersible found by June 23, 2023, counting only if the passenger cabin was located and not just debris? Yes or No.
- **Ask with the rules:** "If pieces are located, but not the cabin which contains the vessel's passengers, that will not suffice for this market to resolve to 'Yes.'" On June 22, the US Coast Guard announced a debris field consistent with a catastrophic implosion. Yes or No?
- **What happened:** Resolved **Yes** after a UMA dispute. Volume was about **$2.25M**.

**FACT**
- The API shows the quoted rule and a **Yes** result ([snapshot](evidence/polymarket-gamma-snapshot.json)).
- DL News reports that No bettors objected because only pieces were found, not the cabin ([DL News](https://www.dlnews.com/articles/markets/crypto-bets-on-titan-sub-cause-uproar-at-uma-polymarket)).

**INFERENCE**
- Read literally, the cabin clause favors No. The Yes vote suggests voters treated "imploded and located" as meeting the spirit of the rule.

## 10. Barron Trump and the $DJT token

- **Ask the oracle:** Is there a preponderance of evidence, as of June 23, 2024, that Barron Trump was involved in creating the Solana token $DJT? Yes or No.
- **Ask with the rules:** "Yes if a preponderance of evidence suggests that Barron Trump was involved in the creation of the Solana token $DJT." Martin Shkreli publicly claimed he co-created the token with Barron, and ZachXBT linked Shkreli to it. Barron made no public statement. Yes or No?
- **What happened:** UMA resolved **No** on 2024-06-26. Volume was about **$1.1M**.

**FACT**
- The API shows **No** ([snapshot](evidence/polymarket-gamma-snapshot.json)).
- Polymarket publicly said: "We firmly believe that UMA got this resolution wrong" ([The Block](https://www.theblock.co/post/302171/polymarket-contradicts-umas-resolution-on-barron-trumps-involvement-with-djt-token)).
- A related market with a stricter "definitive evidence" rule (`did-barron-trump-launch-djt`, about $2.1M) also resolved No.

**UNCERTAIN**
- Reports say Polymarket later refunded Yes holders in USDC. This comes only from a Manifold market's notes ([Manifold](https://manifold.markets/Joshua/what-will-happen-with-the-controver)), not a primary Polymarket source.

**INFERENCE**
- This is the reverse of most cases here: the platform thought the oracle was too strict.

---

## Near misses (not in the ten)

- **"Gold missing from Fort Knox?"** (about $3.5M): resolved **No** on 2025-03-11, though its window ran to June 30, 2025.
  - It was flagged in an X thread for possible whale voting (reported by [Decrypt](https://decrypt.co/311634/polymarket-allegations-oracle-manipulation)).
  - It was left out because coverage was thin.
  - One secondary claim, that Polymarket overrode the oracle here, could not be verified.
- **"Israel x Hezbollah ceasefire extended by April 26, 2026?"** (about $21M): resolved Yes after two disputes. Per a [secondary explainer](https://polymarkets.co.il/en/news/polymarket-uma-scandal-explained/), the "both governments confirm" path couldn't work because Hezbollah is not a government.

## Open questions

1. **Ranking.** "Top 10 most controversial" is a judgment. A different ranking, for example by dollars on the losing side or by number of UMA disputes, would give a different list.
2. **Whale votes.** Per-vote UMA voter data was not pulled from chain, so every whale-concentration figure above is a press claim.
3. **What the oracle needs.** I don't know whether the IdentityMD oracle has web access or a knowledge cutoff. If it doesn't know the facts, the "Ask with the rules" versions give it enough context to answer from the rules alone.
4. **No "correct" answers.** The report does not say what the right answer was for any market. The "Actual result" column is only what Polymarket did, for comparison.

## Sources

- Polymarket Gamma API, all ten events (snapshot in `evidence/`).
- [Decrypt: suit ruling](https://decrypt.co/329210/polymarket-rules-no-237m-bet-zelenskyy-suit?amp=1)
- [The Defiant: suit](https://thedefiant.io/news/nfts-and-web3/polymarket-controversy-heats-up-after-the-zelenskyy-suit-market-resolves)
- [Ynet: Iran deal](https://ynetnews.com/business/article/b1ajjg97gx)
- [The Next Web: Iran](https://thenextweb.com/news/polymarket-345-million-iran-peace-deal-dispute-uma-whale-voting)
- [polymarkets.co.il: ceasefire explainer](https://polymarkets.co.il/en/news/polymarket-uma-scandal-explained/)
- [DL News: TikTok](https://www.dlnews.com/articles/markets/tiktok-disappearance-sparks-polymarket-petition)
- [CryptoSlate: UFO](https://cryptoslate.com/polymarket-faces-major-credibility-crisis-after-whales-forced-a-yes-ufo-vote-without-evidence/)
- [SAN: Venezuela invasion](https://san.com/cc/whats-an-invasion-gambling-sites-definition-costs-gamblers-millions/)
- [The Block: Ukraine](https://www.theblock.co/post/348171/polymarket-says-governance-attack-by-uma-whale-to-hijack-a-bets-resolution-is-unprecedented)
- [CoinDesk: Ukraine](https://www.coindesk.com/markets/2025/03/27/polymarket-uma-communities-lock-horns-after-usd7m-ukraine-bet-resolves)
- [Cointelegraph: Ukraine whale](https://cointelegraph.com/news/polymarket-trump-ukraine-bet-whale-governance-attack)
- [Criptonoticias: Venezuela election](https://www.criptonoticias.com/comunidad/polymarket-cierra-capitulo-elecciones-venezuela-ganador)
- [Bitcoin.com: Venezuela election](https://news.bitcoin.com/polymarkets-integrity-questioned-over-venezuelan-presidential-election-bet-outcome/)
- [DL News: Titan](https://www.dlnews.com/articles/markets/crypto-bets-on-titan-sub-cause-uproar-at-uma-polymarket)
- [The Block: Barron](https://www.theblock.co/post/302171/polymarket-contradicts-umas-resolution-on-barron-trumps-involvement-with-djt-token)
- [Manifold: Barron aftermath](https://manifold.markets/Joshua/what-will-happen-with-the-controver)
- [Decrypt: Fort Knox / manipulation allegations](https://decrypt.co/311634/polymarket-allegations-oracle-manipulation)
