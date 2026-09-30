# What categories is Vitalik most bullish on? — evidence from *Snowmoon*

**Source:** Vitalik Buterin, *Snowmoon*, https://vitalik.eth.limo/snowmoon/ (32 chapters, about 100k words, all read in full).
Chapter links below use the form `https://vitalik.eth.limo/snowmoon/html/chapter-N.html`, written as **[chN]**.
**Retrieved:** 2026-09-30. The page gives no publication date, and *Snowmoon* is not listed on the blog index at https://vitalik.eth.limo/, so I can't date it.

---

## 0. Read this first: what kind of source this is

- **Fact:** *Snowmoon* is a **novel**, not an essay or an investment post. It follows characters in the fictional countries of Veridia, Dzego, Freetown/the United Cities and the "Arctic Empire". The author's declaration on the index page says: "All words were written directly by me." Spelling, style, rule-consistency checking, HTML/CSS and SVGs were done with help from AI models. It is released under GPL v3.
- **Fact:** The text names **no real cryptocurrency, token, chain or company**. A full-text search of all 32 chapters finds 0 hits for "Ethereum", "blockchain", "Bitcoin", "ETH", "stablecoin" and "DeFi". The in-world money is "zipcoins", running on an unnamed "cryptographic network".
- **Fact:** Where the book touches speculation, it is **negative**. The tax rubric in the story puts content that promotes "gambling or risky investment" in its higher-tax tiers [ch1]. A hedge fund uses a derivative bet to give itself "a free option on our backs", pushes a firm into bankruptcy to dodge severance, and loses in court [ch11], [ch21], [ch23].
- **So:** "Bullish" can't mean "price view" here. This report reads it as **the technology and institution categories the book presents as working, winning or worth adopting**. That reading is an **inference**. Views voiced by fictional characters are not automatically the author's views. Section 3 says how much weight each signal can bear.

---

## 1. Short answer

Ranked by how strongly and how consistently the novel backs them:

| # | Category | Strength of signal in the text |
|---|---|---|
| 1 | **Privacy tech and applied cryptography**: ZK proofs, hardware attestation, mixnets, anti-coercion voting, obfuscation/MPC, steganography, social recovery | Very strong. Everywhere in the book, and it decides the plot |
| 2 | **Defensive, open-source technology ("d/acc")**: open hardware, verifiable security cameras, distributed manufacturing, defensive drones | Very strong. The book's main policy fight, and the winning side |
| 3 | **Biodefense and public health**: clean indoor air, far-UVC, CO₂/PM2.5 monitoring, open anti-pandemic tech; longevity with open access | Strong |
| 4 | **Privacy-protected governance and funding mechanisms**: sortition, anonymous committees, "Graph Funding", quadratic voting, land-tax-based "Steering" | Strong, but QF and transparent bodies are shown failing |
| 5 | **Open, interoperable, verifiable social platforms** (Silverchat vs Bluewhale) | Strong |
| 6 | **Forecasting and "info finance"**: prediction markets, competing AI forecasters, privacy-preserving queries | Moderate. Endorsed, with explicit caveats |
| 7 | **Local or personal AI and AI-assisted verification**, with strong caution about AI | Moderate and mixed |
| — | Financial speculation, derivatives, closed or proprietary tech, centralized surveillance | **Bearish** |

---

## 2. Evidence by category

### 2.1 Privacy tech and applied cryptography (strongest signal)

**Facts (what the text says):**
- Everyday life runs on zero-knowledge (ZK) protocols. A watch runs "a zero-knowledge authentication protocol" to confirm a passing drone is harmless, "and nothing else" [ch1]. A venue gate "learned that someone holding a valid and unused credential had arrived - and nothing else" [ch1].
- A loan is backed by reputation through a ZK proof with a **nullifier**: "The only information that would be publicly visible was the nullifier and the amount borrowed." Sales-tax payments are zero-knowledge too. Savings sit behind **social recovery** ("four of six keys held by pre-selected family members and friends") [ch6]. The recovery flow is tested later in the book [ch16].
- Chip supply chains: physical unclonable functions, manufacturer keys published to "the cryptographic network", random destructive inspection, and a **mixnet for physical goods** so inspectors and consumers draw from the same pool [ch9]. People-mixing "black cars" swap cabins, "Like a mixnet, but for people" [ch18].
- Post-quantum direction: factoring-based crypto is "popular science cryptography"; "even elliptic curves are falling out of fashion because everyone's worried ... a quantum computer". The hero studies "stateless tree-of-tree-based" **hash-based signatures** [ch9], [ch10].
- **Coercion-resistant voting**: keys are registered in person with 3 of 5 members of a "Key Allocation Group", and validity is decryptable only by an obfuscated circuit, so a would-be briber "can't tell which votes I submit are real or fake" [ch15], [ch17].
- Obfuscation, steganography and MPC recur as plot tools. LLM-guided steganography gets messages out of occupied territory [ch15], [ch22]. A message is delivered as an "obfuscated language model" [ch19]. Private information is fed to forecasting bots through "verifiable two-party computation" or garbled circuits, backed by an end-to-end machine-checked proof [ch27].
- **Thesis lines:** "Privacy isn't a luxury, it's why we're still here" [ch21]; "Privacy for the weak, transparency for the powerful" [ch32]. The only Veridian institutions that resisted the infiltration are the private ones: "the Order, the Courts, the graph funding" [ch21], and in [ch32], "The Order of Steering worked, the Courts worked, Graph Funding has been fine. But everything more transparent has been broken."

**Inference:** This is the book's central category. Almost every turning point is won by cryptography or privacy. The concrete primitives (nullifiers, social recovery, anti-coercion voting, hash-based signatures, attestation, MPC) match what the Ethereum ecosystem calls ZK/privacy, account abstraction or social recovery, MACI-style voting, and post-quantum signatures. That mapping is mine; the book never names these real-world projects.

### 2.2 Defensive, open-source technology (d/acc)

**Facts:**
- The longest policy thread is a vote on the "Openness in hardware" tax rubric [ch6]. A faction pushes to exempt military, surveillance and counter-surveillance products from the open-source tax breaks [ch10], [ch13]. That faction turns out to be led by a foreign agent [ch20], [ch21]. The protagonist votes **No** on the exemption and **Yes** on *raising* the incentive to open hardware [ch17].
- The pro-openness argument: open-sourcing defensive tech gives weaker actors a "lifeline". It cites how open formal verification let Dzego harden its devices against sabotage [ch10]. Also: "Put the whole world on a more level playing field, so no one is in a position to light a fire and be the only ones with fireproof suits" [ch17].
- Distributed rather than centralized capacity: "grow roots, no head", "Use distributed manufacturing to build all our tools" [ch2]; "we have lots of smaller, distributed underground fabs" after a central fab is bombed [ch7].
- **Verifiable surveillance**: cameras that reveal data only when triggered, post a hash for each reveal, are hardware-attested, and can be unscrewed and inspected by any citizen [ch5], [ch9], [ch20]. The book shows the other side too. After Veridia "watered down" its cryptographic limits, both the Arctics and the Dzegojan could backdoor its cameras [ch24], [ch25]. The ending replaces them with cameras "with built-in hard guarantees of what information they can and can't transmit" [ch32].
- Ending line on captured Arctic technology: "Open source - it's not just a good idea, it's the law" [ch31].

**Supporting non-fiction source (a separate Vitalik essay, not Snowmoon):** "My techno-optimism" (https://vitalik.eth.limo/general/2023/11/27/techno_optimism.html) sets out "d/acc: Defensive (or decentralization, or differential) acceleration". It has sections on macro physical defense, "Micro physical defense (aka bio)", "Cyber defense, blockchains and cryptography" and "Info defense". Its framing lines up closely with categories 2.1–2.3 and 2.5.

**Inference:** The novel dramatizes the d/acc thesis. Open, verifiable, defense-leaning technology is the winning bet, and closed or centralized capability is the danger.

### 2.3 Biodefense and public health

**Facts:**
- Watches show CO₂ and PM2.5 as standard [ch3], [ch11], [ch19]. Rooms automatically ramp up fans and far-UVC when a flu virus is detected [ch6]. There is an explicit tax rubric for "Clean indoor air" [ch6], [ch11].
- Motive: "Super-pandemics. Like, deliberately released by the Arctics" [ch11]. Funding is steered to "open source tech for air filtering, cleaning, wastewater scanning". The book flags that wastewater data raises a privacy question needing a cryptographic answer [ch11].
- Filters are made "twice as cheap every two years for the past decade" [ch11]. In Dzego, "average indoor CO2 levels dropped by over a hundred points within a month" [ch22], and filters and UV lamps "increased more than tenfold" [ch24].
- **Longevity is treated positively, but only with openness.** "A longer life is a healthier life by default" [ch27]. The problem with Arctic clinics is that "you don't get to learn what we are doing to your body, and ... you have to keep coming back" [ch31].

**Inference:** Pro air-quality, pandemic-defense and longevity technology, on the condition that it is open and not a source of dependence.

### 2.4 Privacy-protected governance and public-goods funding

**Facts:**
- Mechanisms in play: **quadratic voting** on building aesthetics, where votes are normalized so it is "mathematically provably best" to vote your true strength [ch1]. **Sortition** with split, isolated sub-groups for Keepers, Sentinels and Courts [ch6], [ch23]. Acolytes are **scored on predicting** Sentinel audits [ch1]. Randomly re-drawn court panels with bad-faith-appeal penalties [ch21], [ch23]. Parts of the city from ch22 also run on congestion and acceleration **road pricing**.
- **Graph Funding**: funding flows through a DAG of randomly selected node committees, and the top decile is **randomized above a cutoff** to protect intrinsic motivation [ch17]. It is credited as one of the institutions that held up [ch21], [ch32].
- **Quadratic Funding is shown as vulnerable.** A bribery app lets people "donate ten zipcoins and get back twenty". It is later revealed as a competitor's attack [ch11], and "the Arctics just did the same attack on Quadratic Funding that Bluewhale did but at ten times the scale" [ch17]. A character calls QF "even worse" than the transparent Parliament at resisting exploitation [ch7].
- Land-tax-centred public finance: aesthetics, air quality, emergency preparedness and similar rubrics are components of a "composite land tax" [ch1], [ch11]. Freetown's government is "constitutionally banned from collecting more than the basic land tax" plus resource rent [ch10].

**Inference:** The book favors mechanism design built on **privacy, randomness and collusion resistance** over plain transparency or plain quadratic funding. That is a qualified view: bullish on the category of "coordination tech" and "funding public goods", openly skeptical about naive QF.

### 2.5 Open, interoperable, verifiable social platforms

**Facts:**
- The protagonist learned to code by writing "an alternative client for Silverchat". This was possible because its API was open, which he credits to the openness tax rubric. Bluewhale is the closed foil [ch3], [ch8].
- Silverchat's feed is verifiable: it publishes "proofs onto a cryptographic network every time the set of readable messages is updated". Changing the algorithm needs "a new algorithm hash ... with a twenty-day delay". Its taxes fall to zero because of "algorithmic transparency ... interoperability, respecting users' privacy" [ch27].
- Graph Funding sends "eighty percent" of open-source social-media analysis funding to Silverchat [ch17]. A privacy-preserving, large-sample Silverchat poll becomes the legitimacy lever in the climax [ch27], [ch28].

**Inference:** Bullish on open, interoperable social and information infrastructure with verifiable ranking, and bearish on closed attention platforms. This lines up with "info defense" in the d/acc essay.

### 2.6 Forecasting, prediction markets and competing AIs (info finance)

**Facts:**
- "Prediction markets are cool", followed straight away by two weaknesses: manipulation (with a stated result that non-risk-neutral, finite-capital arbitrageurs can't fully offset a manipulator) and leakage of private information [ch27]. The workaround is to query the top leaderboard bots from "Silverchat Predict" privately through 2PC [ch27].
- The epilogue's diagnosis: Veridian institutions "don't really have a built-in concept of predicting the future... You've [sic] aligning people to each other, but you're not aligning people to reality". The proposal is "some kind of open competition" of AIs: "AI should be a player, not the game" [ch32].

**Inference:** Positive on forecasting and prediction-market mechanisms as a category, but framed as young ("right now prediction markets are new") and in need of privacy and anti-manipulation work.

### 2.7 Local and personal AI, AI-assisted verification, and AI caution

**Facts:**
- Everyone uses a local assistant ("Emerald, the local AI running from Gladias's hand device") [ch1]. The book describes an emerging "internet minimalism... you can have your whole world on your own device" [ch23]. AIs cross-check formal proofs and re-implement crypto code from papers [ch27].
- Caution is voiced strongly: AI models are "grown, not forged. They don't have walls, they have immune systems" [ch29]. Adversarial-example attacks decide the final battle [ch29], [ch30]. "Language models will always be attackable in ways that regular software is not" [ch32]. There is also worry about "nine trillion" bots and humans no longer being a constraint [ch32].

**Inference:** Pro local, user-controlled AI and AI as a verification aid. It stays wary of AI as a centralized decision-maker and of AI security.

---

## 3. Facts vs inferences vs uncertainty

**Established facts (checkable in the text):** everything quoted and cited with [chN] above; the absence of any named real-world coin, chain or protocol; the negative portrayal of speculative finance; how the plot resolves (the open-hardware incentive is raised, private institutions survive while transparent ones fail, and QF is attacked).

**Inferences (mine):**
- Treating "bullish" as "portrayed as winning or worth adopting" is my reading, since the source contains no price or investment views.
- Mapping in-world tech to real-world categories (ZK and privacy, social recovery, MACI-style voting, post-quantum signatures, d/acc, info finance) is my interpretation, backed by the separate "My techno-optimism" essay. *Snowmoon* doesn't make that mapping itself.
- The ranking reflects how often and how decisively each category appears. It is a judgement call, not a count taken from the author.

**Uncertainty:**
- **Author's views vs characters' views.** Several lines are debate positions: Ephelion's growth argument, the Seila/Verdow/Zei exchanges in ch32 ("What if sometimes different parts of the lake have to be water and ice at the same time?" "That may be."). The ending leaves some questions open on purpose. Plot success is a signal, not a statement.
- **Dating:** the page has no date and doesn't appear on the blog index, so I can't say whether it reflects his current views.
- Fiction can put forward ideas the author is exploring rather than endorsing. Example: the book shows surveillance helping to find Lily, then argues against unrestricted cameras [ch26], [ch28].

## 4. Unanswered questions

1. Does Vitalik have **investment** preferences among these categories (tokens, protocols, companies)? This source doesn't answer that and shouldn't be used as evidence for it.
2. Which **real projects** (if any) does he think best implement the in-world tech? Not stated.
3. How does *Snowmoon* relate in time to his other writing (d/acc follow-ups, posts on prediction markets or info finance, privacy)? Not checked beyond one essay. The date is unknown.
4. Is the skepticism about quadratic funding in the story his current position, or a plot device? Can't tell from this source.

## 5. Method and limits

- Fetched the index and all 32 chapter HTML pages from `vitalik.eth.limo` (all HTTP 200), stripped them to text and read every chapter in full. Keyword searches were only used to confirm absences (e.g. "Ethereum": 0 hits).
- Also fetched one non-fiction essay, "My techno-optimism", solely to check the d/acc framing used as supporting context. No other sources were consulted.
- This is one reviewer's reading. It has not been independently reviewed. Quotes were copied from the retrieved text. Chapter numbers refer to the site's chapter files.
