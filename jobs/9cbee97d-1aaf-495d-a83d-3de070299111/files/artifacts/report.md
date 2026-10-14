# PROJECT RICKY — Phase 1 preparation

**Decision memo and handoff specification • 14 October 2026 • version 1.0 • NOT APPROVED FOR LAUNCH**

Commissioned for the requester. This report contains research, original creative proposals and specifications only. No token, production contract, live website, account, funded transaction or published campaign has been created. The reference token belongs to an existing project; this commission supplies no authority over it.

## 1. Final recommendation

**Do not launch a token on the evidence available. Approve a distinct fictional brand for validation first.** The recommended working brand is **CUFFLINKS**, starring **Ricky Cufflinks**, with provisional ticker **$RCUFF**. Its central joke: a gangster spends a fortune on his cuffs, then gets a second pair for free. The recurring line is **“Expensive suit. Free cuffs.”** Recognition comes from the image and the reversal of status, rather than a real person's identity or criminal allegations.

If later validation and approvals justify a token, recommend **one PulseChain-native CUFFLINKS/WPLS constant-product pool**, a fixed 1 billion supply, immutable zero transfer tax, 90% supply seeded in liquidity, 5% creator vesting and 5% community vesting. Use IMD for commissioned creative work and transparent community participation. Do not launch an IMD pair on PulseChain without authentic bridge and market evidence. Do not use the reference address as this project's address.

ETH and IMD pairings are evaluated in §5. Neither currently supplies an evidenced turnkey PulseChain route through IMD. A launch on Ethereum would be a substantive scope change requiring the requester’s approval. The recommended burn is voluntary and decreases actual total supply; the phrase “Tax Fraud Burn” is fictional comedy, never a claim of tax relief, reduced liability, automatic appreciation or concealed accounting.

**Commercial judgment:** the joke is repeatable; a sustainable token business is unproven. The existing RICKY already occupies the closest identity, its ownership is extremely concentrated, and indexed trading is thin. The strongest opportunity is original character entertainment and commissioned meme production. A token should follow demonstrated participation, not substitute for it.

### Evidence labels used throughout

- **Verified observation (V):** directly retrieved chain state or a source's published content. Verification of a publication does not establish that all of its assertions are true.
- **Reported (R):** attributed claim from an identified party or aggregator; not independently proven here.
- **Inference (I):** our interpretation or calculation, with its basis stated.
- **Proposal (P):** original recommended design, target, cost assumption or copy; not an existing feature.
- **Unresolved (U):** missing evidence, clearance or requester decision. A later agent must not silently fill it.

## 2. Research: reference token, market and news

### 2.1 Identity and contract observations

**V:** Public PulseChain RPC returned chain ID 369. At block **27,796,195**, direct calls to `0x79FC0E1d3EC00d81E5423DcC01A617b0e1245c2B` returned **MOST WANTED**, **RICKY**, **18 decimals**, and **5,555,555,555 tokens**. The explorer reported 719 holder addresses when retrieved; those are addresses, not necessarily people. Direct balance verification found **87.3942%** of supply at `0xe01D620618754eA1855Cc9f8Dd9058f9AaA83403`. Saved evidence is in `research/reference_rpc_pinned.json`, `pulse_explorer_token.txt` and `reference_holders.json`. Public sources: [RPC](https://rpc.pulsechain.com), [explorer token data](https://api.scan.pulsechain.com/api/v2/tokens/0x79FC0E1d3EC00d81E5423DcC01A617b0e1245c2B), [holder data](https://api.scan.pulsechain.com/api/v2/tokens/0x79FC0E1d3EC00d81E5423DcC01A617b0e1245c2B/holders).

**V/I:** The first ten explorer holder entries sum to approximately **95.8764% of issued supply**, including the main AMM pool. This is a raw concentration measure, not ten independent beneficial owners. The largest address is classified by the explorer as not a contract. Its identity, key control and any off-chain restrictions are unknown. **Do not call it a founder wallet, burn wallet, scammer or attacker without additional proof.** Its balance nevertheless makes public float and possible sell pressure central risks.

**V:** The explorer flags source verification as true, but full verification as false. The retrieved flattened `GoPulseToken` source mints constructor supply once and its published ABI has no external mint, burn, owner, pause, blacklist or tax setter. Its transfer path is the standard balance transfer in the retrieved source. **I:** that source is consistent with zero token transfer tax and no public supply-changing entry point. This is a limited source inspection, not an audit, bytecode reproduction or buy/sell simulation. Independent review must reconcile the explorer’s incomplete verification before stronger claims. [Contract metadata and source](https://api.scan.pulsechain.com/api/v2/smart-contracts/0x79FC0E1d3EC00d81E5423DcC01A617b0e1245c2B).

**V:** The indexed main pool is PulseX V2 RICKY/WPLS at `0xBfE5AE40BBcA74878419ad7d7E115a30CCFC62F1`. Its LP holder list places about **99.8499%** of listed LP balances at `0x0000000000000000000000000000000000000369`. This unusual address is an observed existing destination, not a recommended owner or an assumed irreversible burn. A holder list alone does not prove a legal lock, inaccessible key, non-withdrawable liquidity or protection from whale selling. No lock term was established. [LP holders](https://api.scan.pulsechain.com/api/v2/tokens/0xBfE5AE40BBcA74878419ad7d7E115a30CCFC62F1/holders).

### 2.2 Liquidity and current trading snapshot

**R:** DEX Screener token-pairs API, retrieved 14 October 2026 around 14:50–14:54 UTC, returned four pools. Values are aggregator estimates, not audited reserves, and were not all fetched at a single block. The site title can show valuation where a reader expects a per-token price; use explicit API fields. [Token-pairs API](https://api.dexscreener.com/token-pairs/v1/pulsechain/0x79FC0E1d3EC00d81E5423DcC01A617b0e1245c2B).

| Indexed pair | Pool address | Liquidity USD | 24h volume USD | 24h buys / sells | 24h price change |
|---|---|---:|---:|---:|---:|
| RICKY/WPLS | `0xBfE5AE40BBcA74878419ad7d7E115a30CCFC62F1` | 2,474.85 | 99.12 | 7 / 18 | −43.70% |
| RICKY/HEX | `0x8a1e6e81795B4CcF61dAAF443ab865381862871d` | 219.31 | 50.40 | 15 / 4 | −45.72% |
| RICKY/eHEX | `0x11969149dA330853C2a851464A0782857C7D1A36` | 205.94 | 20.39 | 7 / 2 | −40.80% |
| RICKY/PLSX | `0x606146cf3d18A527ecDcfe68bc998B7eA776835E` | 279.95 | 17.45 | 3 / 2 | −39.40% |

The main pool’s reported token price was **$0.00001720**, FDV **$95,594**. Four-pool totals: liquidity **$3,180.05**, volume **$187.36**. These sums cover returned pools only, may contain arbitrage or wash activity, and cannot be treated as unique demand. Thin secondary pools are poor independent price evidence. [Main pool](https://dexscreener.com/pulsechain/0xbfe5ae40bbca74878419ad7d7e115a30ccfc62f1).

**I:** the main quote reserve represents roughly $1,237, not $95,594 of cash available to sellers. In a balanced constant-product illustration, a $100 buy against $1,237 quote reserve has approximately 7.5% average execution deterioration before fees; the spot price moves more. That is a model using indexed liquidity, not a current executable quote. FDV is supply multiplied by marginal price, not a realizable exit value.

### 2.3 Historical performance

**R/I:** GeckoTerminal supplied 180 daily USD candles from 17 April through 14 October 2026 for the main pool. Exclude the incomplete 14 October candle from close-to-close calculations. No claim is made that this covers the token’s lifetime. [OHLCV source](https://api.geckoterminal.com/api/v2/networks/pulsechain/pools/0xbfe5ae40bbca74878419ad7d7e115a30ccfc62f1/ohlcv/day?aggregate=1&limit=180&currency=usd).

| Comparison, ending at 13 October close | Starting close USD | Ending close USD | Calculated return |
|---|---:|---:|---:|
| 17 April → 13 October | 0.000018670064 | 0.000030493999 | +63.33% |
| 15 July → 13 October, 90 days | 0.000008713580 | 0.000030493999 | +249.96% |
| 13 September → 13 October, 30 days | 0.000056006849 | 0.000030493999 | −45.55% |
| 6 October → 13 October, 7 days | 0.000037330851 | 0.000030493999 | −18.31% |

Sample intraday high: $0.000139453681 on 20 August; 13 October close was **78.13% below that sample high**. Median daily volume over the last 30 completed candles was approximately **$15.42**; total **$1,259.62**. These are USD aggregator candles, affected by quote-token price and thin trades. They are not holder P&L or guaranteed fills. The large 90-day rise and subsequent drawdown can coexist.

**R/U:** Blockspot reports an all-time high of $0.00110745 on 15 January 2025, and a different rounded supply. This was not corroborated with lifetime OHLCV. It is excluded from the verified historical calculations. Its “inactive website” flag also conflicts with the newer links indexed by DEX Screener; it cannot establish that the whole project is abandoned. [Blockspot listing](https://blockspot.io/coin/most-wanted-4/).

### 2.4 Community attention and competitors

**V/R:** Reference pool metadata links to `x.com/MOSTWANTEDRICKY`, `t.me/RickyMostWanted`, a YouTube channel and a GoPulseChain ecosystem listing. The listing identifies Ricky Most Wanted; directory/profile links do not prove official control or active membership. No authenticated X analytics, reliable follower count, Telegram member audit or independently measured organic engagement was obtained. 719 holder addresses and 25 main-pool trades per 24 hours are limited attention proxies. [Existing project listing](https://www.gopulsechain.com/ecosystem/defi/ricky-most-wanted), [indexed social links](https://dexscreener.com/pulsechain/0xbfe5ae40bbca74878419ad7d7e115a30ccfc62f1).

Competitor searches were exploratory DEX Screener queries, capped by its returned results. These are **individual returned pools**, not total token liquidity or official endorsements. Contract identity, rather than ticker alone, is essential.

| Competitor and observed identity | Example returned pool | Liquidity / 24h volume USD | Creative lesson and caution |
|---|---|---:|---|
| MOST WANTED / RICKY, reference address | Main WPLS pool above | 2,474.85 / 99.12 | Already owns the nearest concept. A new RICKY would be confusing. |
| Hex Orange Address / HOA, `0x7901a3569679AEc3501dbeC59399F327854a70fe` | `0x714D3e632Bdd5E840A37eddaE6399B4Cca859E26` | 2,108.65 / 227.18 | Insider wordplay creates belonging, but liquidity remains a constraint in this pool. |
| BEAR / TEDDY BEAR ㉾, `0xd6c31bA0754C4383A41c0e9DF042C62b5e918f6d` | `0x24c4D0532cDDAE3b0B8935196F2B91e68d6b85ED` | 98,692.87 / 6,029.66 | Simple recurring mascot supports recognition. Larger returned pool does not establish fair ownership or organic trades. |
| PulseChain Mog Coin / MOG, `0x495d9b70480A22a82D0FB81981480764BA55550e` | `0x8A41dCd8cfd5F34F9ba9731Fbdbf34b45B1B41aa` | 3,342.81 / 1,191.72 | Strong meme shorthand; do not assume affiliation with other chains' MOG. |

Sources: [HOA search](https://api.dexscreener.com/latest/dex/search?q=Hex%20Orange%20Address), [Teddy search](https://api.dexscreener.com/latest/dex/search?q=Teddy%20Bear), [MOG search](https://api.dexscreener.com/latest/dex/search?q=Mog%20Coin). Teddy’s own community site publishes the same contract and warns about unrelated projects: [brand notice](https://teddybearpulse.com/brand-notice/). We have not audited competitors or verified their tax, LP ownership or holder distributions.

**I:** “gangster arrested” by itself is occupied and event-dependent. “Cufflinks become handcuffs” offers a reusable visual joke, wearable merchandise and stories about due diligence that work without a headline. PulseChain users supply an initial cultural audience; IMD makers can supply creative participation. The size and spending power of their overlap remain unknown.

### 2.5 PulseChain context and legal news: separate events from conclusions

**R:** DeFiLlama’s retrieved chain series estimates PulseChain TVL at **$53,500,085 on 14 October 2026**, versus a sample peak **$976,505,568 on 8 December 2024**, a calculated decline of about **94.52%**. This is provider methodology, not total network wealth or available meme liquidity. Its DEX endpoint reports header `total24h` of **$1,697,792**, while its dated chart contains **$9,052,951 for 14 October** and the protocol subtotals also differ. The header corresponds to the prior dated row. Treat this as a freshness/aggregation discrepancy; do not advertise a single “live daily volume” number from it. [TVL series](https://api.llama.fi/v2/historicalChainTvl/PulseChain), [DEX series](https://api.llama.fi/overview/dexs/PulseChain). This supports caution, not a prediction of network failure.

**V:** The official bridge landing page provides bridge distribution links. Its existence establishes an onboarding route, not an audited safety guarantee, current asset mapping or redemption liquidity. [PulseChain Bridge](https://bridge.pulsechain.com/). This review did not verify recent protocol upgrade claims or comprehensively establish every October 2026 news development; rumors about treasury balances and “guaranteed pumps” are excluded.

**V/R:** The SEC announced its July 2023 civil complaint against Richard Schueler, known as Richard Heart, and associated projects. Its fraud and unregistered-offering assertions were **allegations**, not findings of guilt. [SEC announcement](https://www.sec.gov/newsroom/press-releases/2023-143). A February 2025 dismissal is reported on jurisdictional grounds; Reuters coverage is an independent secondary account. [Reuters report syndicated by Yahoo](https://finance.yahoo.com/news/us-judge-dismisses-sec-fraud-011525434.html). Heart’s counsel reports that the SEC declined to amend on 21 April 2025 and links the court documents. This is an interested-party account; copies were retrieved for the evidence archive, but not independently authenticated against the court docket. [Counsel’s dated account and document links](https://www.csvllp.com/latest-news/sec-declines-to-file-amended-complaint-against-csv-client-richard-heart-cementing-a-complete-victory-for-mr-heart-in-the-secs-case-against-him).

**R/U:** Finnish public broadcaster Yle reported police suspicions of aggravated tax evasion and assault in September 2024 and luxury-watch seizures in January 2025. Those articles do not establish conviction, arrest, or current whereabouts in October 2026. A direct current police case update was not obtained. [Yle, 17 September 2024](https://yle.fi/a/74-20112197), [Yle, 7 January 2025](https://yle.fi/a/74-20135322). Do not depict a real person's alleged crimes as proven. A Red Notice is not an international arrest warrant; INTERPOL states this expressly. [INTERPOL explanation](https://www.interpol.int/en/How-we-work/Notices/Red-Notices).

**P:** Ricky is a separate invented character. No likeness of Heart, real cartel figure, victim, government agency insignia or real arrest photograph. His international escorts are cartoon officers of an invented “International Meme Police.” A disclaimer alone would not fix a recognizable defamatory portrayal. Legal clearance must assess the combined character, copy and context.

## 3. Brand recommendation and availability screen

### 3.1 Provisional selection

| Element | Proposed source-of-truth value |
|---|---|
| Short project/token name | **CUFFLINKS** |
| Character name | **Ricky Cufflinks** |
| Ticker | **RCUFF**, five letters, provisional |
| Main line | **Expensive suit. Free cuffs.** |
| Secondary line | **He confused private keys with a private jet.** |
| Community | **The Paper Trail**; makers are “case contributors,” not investors promised riches |
| Format | Luxury editorial meets an absurd booking desk |
| Premise | A fictional gangster discovers that public ledgers are terrible places to hide anything |
| Tone | Dry, self-incriminating, crypto-native; joke targets Ricky’s vanity and bad reasoning |

**P — canonical narrative:** Ricky Cufflinks has a tailored suit, an untailored alibi, and two international officers who keep asking for the transaction hash. He insists he is “going cross-chain.” They explain that this is a transfer to another precinct. He hires a swarm of creative agents to manufacture excuses. The community turns those excuses into memes, then the swarm organizes the receipts. Ricky remains vain and incompetent; the project remains transparent.

Recurring original slogans: “Proof of Suit.” “Public ledger. Private panic.” “Self-custody met custody.” “Every excuse needs a transaction hash.” “The receipts have receipts.” “Booked, not bullish.” “Luxury on the outside. Audit trail on the inside.” “His only successful bridge was to the booking desk.” Use one punchline per asset, not all at once.

**I — why this wins:** suit and cuffs read at avatar size; status collapse creates surprise; “custody,” “chain,” “burn,” “keys” and “receipts” support repeatable crypto wordplay. The audience can replace the excuse without needing to redraw Ricky. The concept can attract people who never buy the token. That remains a hypothesis until measured.

### 3.2 Availability checked, not guaranteed

Screen date: 14 October 2026. Web searches included exact `"Ricky Cufflinks"`, `"RCUFF" cryptocurrency`, `"RCUFF" token PulseChain`, `"Cufflinks" meme token`, and CUFF/CUFFED alternatives. DEX Screener queries for `RCUFF` and `Ricky Cufflinks` were saved. **No exact Ricky Cufflinks / RCUFF token identity was found in these returned results.** RCUFF query returned an unrelated Solana FELY entry; the longer query returned existing Ricky projects, not an exact combined name. Fuzzy search results are not a registry or proof of absence. [RCUFF query](https://api.dexscreener.com/latest/dex/search?q=RCUFF), [character-name query](https://api.dexscreener.com/latest/dex/search?q=Ricky%20Cufflinks).

| Candidate | Screen result | Recommendation |
|---|---|---|
| Ricky / RICKY | Exact same-chain reference collision; other Ricky tokens also returned | Reject as new token identity |
| Most Wanted / MOST | Reference name occupied; other MostWanted listing surfaced | Reject |
| CUFF | Jail Cat uses CUFF on Solana | Reject despite strong shorthand |
| CUFFED | Golden Handcuffs uses CUFFED on Base; another CUFFED listing on Solana | Reject |
| CUFFLINKS / RCUFF, Ricky Cufflinks | No exact token match found in limited screening; ordinary “cufflinks” commerce is extensive | Recommend conditionally |

Collision sources: [Jail Cat / CUFF listing](https://coinmarketcap.com/currencies/jail-cat-cuff/), [Golden Handcuffs / CUFFED](https://www.coinbase.com/en-pt/price/base-golden-handcuffs), [Solana CUFFED listing](https://www.solanatracker.io/tokens/2PiSyDJSRkkvUULkfJyqftkAKXPcGLRkMYEr3LAupump).

**U:** No trademark-register legal clearance, domain registrar availability, X handle ownership or account reservation was completed. CUFFLINKS is descriptive in apparel and may be weak alone as a trademark. Use the distinctive combined character/mark and obtain target-jurisdiction clearance. Token names/tickers have no globally exclusive allocation. Recheck all screens immediately before approval. Proposed handle stem `RickyCufflinks` and domain stem `rickycufflinks` are preferences, **not available or controlled addresses**. Do not hyperlink them as project channels until requester control is verified. No availability claim is stronger than “no exact match found in this bounded screen.”

### 3.3 Character and identity specification

Ricky: angular pear-shaped face, warm olive skin, swept black hair with one silver streak, narrow pencil moustache, exaggerated single raised eyebrow; no resemblance reference. Plum double-breasted suit, ivory shirt, crooked electric-cyan tie, oversized square gold cufflinks shaped like the original RC monogram. Front wrists in polished steel cartoon cuffs; a thin chain creates the visual transition from luxury accessories to custody. He looks annoyed about the tailoring, not terrified of violence.

Two escorts: different heights and silhouettes, plain navy coats, small invented globe-with-a-paperclip badge, one carries a transparent evidence envelope, the other a receipt printer. Caption can call them international police within the fictional story. No actual INTERPOL/Europol badges, flags implying jurisdiction, weapons, blood, victim jokes, racial caricatures or recognizable celebrity clothing.

Palette: ink `#101116`; ivory `#F5F0E5`; suit plum `#542A49`; brass `#C8A55A`; flash cyan `#69E5ED`; muted red `#A4424D`. Ivory-on-ink for body text; brass only for large headings/decorations after contrast testing. Headline direction: condensed editorial capitals; body: legible system sans; transaction fields: system monospace. Final custom lettering preferred for the wordmark. Avoid borrowing competitor logos, recognizable film frames or luxury brand marks.

## 4. Tokenomics specification — proposed baseline T1

This is a complete recommended economic baseline awaiting approval, **not finalized by consent**. Any changed allocation, lock, pairing, burn behavior or privileged role invalidates downstream claims. No address, owner, recipient or deployment parameter is guessed.

### 4.1 Supply and allocation

**P:** Fixed initial supply **1,000,000,000 RCUFF**, 18 decimals; initial atomic supply `1000000000000000000000000000`. Mint once at creation with deterministic distribution; no later mint. Zero token transfer tax on buys, sells and ordinary transfers, with no setter. DEX fees, gas and slippage remain separate costs. No rebasing, reflection, hidden transfer restriction, blacklist, proxy, owner trading override or automatic swapback. No yield, revenue share, redemption claim or promise of financial return.

| Bucket | Share | Tokens | Proposed custody and release |
|---|---:|---:|---|
| Initial primary liquidity | 90% | 900,000,000 | All seeded in one approved pool; no private sale of this bucket |
| Creator | 5% | 50,000,000 | Non-upgradeable vesting; 12-month cliff, then linear release over the next 24 months, fully vested at month 36 |
| Community creative treasury | 5% | 50,000,000 | 6-month cliff, then linear release over the next 24 months, fully vested at month 30; beneficiary is disclosed 3-of-5 multisig |
| Initial burn, presale, undisclosed wallets | 0% | 0 | None |
| **Total** | **100%** | **1,000,000,000** | No allocation counted twice |

Vesting starts at the approved canonical launch timestamp. Zero accrual before each cliff; accrual begins at the cliff, with no immediate catch-up payout. Claims may be less frequent than continuous accrual. Changing recipient must not accelerate vesting; recommend fixed beneficiaries after deployment, accepting lost-key risk. Final contract design and recovery policy need independent review and approval.

The community bucket funds judged creative work, not holder dividends. Publish every grant, amount, beneficiary, conflict disclosure and remaining balance. Before spend: 72-hour public proposal notice plus multisig execution; emergency administrative changes do not override the token. Creator allocation is compensation at risk, not operating cash. No undisclosed creator purchases or side-wallet awards. A multisig does not establish five independent humans unless signer relationships are disclosed.

### 4.2 Fairness, liquidity ownership and concentration

**P:** No presale, paid whitelist, preferential insider price or promised airdrop. Publish the supply distribution, intended liquidity and launch policy before trading; withhold signing secrets. No “fair launch” claim implying bots cannot participate. Open AMMs cannot prevent snipers or Sybil concentration without adding restrictions we do not recommend. Publish actual launch outcomes and connected-wallet exposure, not merely policy.

Lock **100% of project-created LP tokens for 24 months** in an independently reviewed, non-upgradeable time-lock, with no early unlock or admin escape. The beneficiary at maturity is the disclosed treasury multisig. Give an explicit UTC unlock date and contract proof. External LPs remain free to withdraw their own liquidity. At 21 months, publish a continuity plan; extending a lock requires its own approval. Do not say “locked forever.” LP fees, if accrued in the chosen pool, remain part of locked LP value and are not dependable project revenue during the lock.

**P:** Creator/community control is 10% economic supply in total even when locked. Report these linked buckets together. Dashboard concentration must show raw address rankings and an adjusted view that labels pools and vesting contracts; do not exclude them silently. Proposed gates: no additional undisclosed team allocation; no non-pool, non-vesting beneficial-owner cluster above 5% without prominent disclosure and renewed launch review. Post-launch a breach prompts factual disclosure and a pause of promotion, not censorship or confiscation. Wallet clustering is imperfect and must carry confidence labels.

Ownership/admin promise: the proposed token itself needs no owner role. Vesting, LP custody, website and community spending have separate control arrangements. “Ownerless token” is not “ownerless project,” and a liquidity lock does not stop price collapse. Verify allowance behavior, burns, full distribution and absence of proxy/admin paths independently in Phase 2.

### 4.3 Tax Fraud Burn — receipt-first satire

**P:** Public-facing heading **“Tax Fraud Burn — fictional paperwork, real supply reduction.”** Subline: “Ricky tried to delete the receipts. The ledger kept them.” Every explanation includes: **“This is satire. Burning tokens does not erase records, avoid taxes or guarantee price gains.”** If user testing reads it as tax advice or concealment, rename the feature **“Receipt Burn”** while retaining the joke in character dialogue.

Mechanism: an optional holder-initiated native `burn(amount)` reduces the caller's balance and `totalSupply` by exactly the amount, emitting the standard burn transfer event. No treasury can burn somebody else’s funds. Baseline exposes no delegated `burnFrom` flow, avoiding extra approval risk. Use established ERC-20 semantics with a narrowly scoped self-burn entry point, independently reviewed later. [OpenZeppelin ERC-20 burn behavior](https://docs.openzeppelin.com/contracts/5.x/api/token/erc20).

No transfer tax supplies the burn. No scheduled buyback, compulsory fee, fundraising promise, volume target or burn-linked token reward. A “case closed” episode can invite voluntary participation after legal review, but a person earns the same creative eligibility without buying or burning. No automatic treasury burn commitment is included. Any later treasury-funded burn must state the source, authorization and effect on promised budgets first.

Accounting: `cumulativeBurned = initialSupply − totalSupplyAtFinalizedBlock`. Independently sum successful burn events since deployment, excluding the initial mint and reverted calls; reconcile the two values at the same block. A zero destination in the event is the standard burn sentinel, not a stand-in owner address. Token transfers to a “dead” account that leave `totalSupply` unchanged do **not** count. Do not count LP burns, PLS gas burns, another token’s burns or the reference token’s transfers.

Dashboard shows initial supply, current issued supply, cumulative true burns, burn percentage of initial supply, block number/hash, timestamp, transaction link, amount and initiating address. Show “No verified burns yet” before the first successful burn; no animated fabricated number. If RPCs disagree or reorg evidence appears, show last verified data with a stale label. Proposed confirmation depth: 64 PulseChain blocks for displayed confirmed burns, pending a chain-specific security review; this is a design choice, not guaranteed finality. Keep pending events separate, roll back orphaned events and reconcile totals after restart. Store integer atomic units and format only for display.

Burning decreases supply; it does not create demand, increase the quote reserve, grant a tax deduction or make FDV realizable. Tax and recordkeeping obligations remain subject to the holder's jurisdiction.

## 5. Pairing decision and IMD feasibility

**V:** IMD’s retrieved public capabilities list launch chains **Ethereum (1), Robinhood Chain (4663) and Sepolia (11155111)**; **PulseChain (369) is absent**. ETH and IMD pairing options appear on the listed production chains. This is a dated capability observation, not a guarantee of execution or PulseChain incompatibility for all future software. The docs identify mainnet IMD as `0xd34a99bc0f67ae1bbd63c660e6d0b0dd03e263b7` and paid actions through its request system. [Live capabilities](https://api.imd.fun/requests/capabilities), [official docs](https://imd.fun/docs/).

**V/R:** IMD’s token page describes Community Coin trade cuts for creators, referrals and IMD burning. These project statements establish the described model, not audited end-to-end fee behavior. A zero transfer-tax token can still trade in a fee-charging venue; saying “zero total trading fees” would be misleading. A hook or launchpad policy must not quietly replace this report’s zero-tax, fixed-supply and LP-lock commitments. [Official token page](https://imd.fun/token/).

| Option | Benefit | Cost / dependency | Decision |
|---|---|---|---|
| PulseChain CUFFLINKS/WPLS | Native audience and quote asset; no bridge dependency for the primary quote; simple pool mechanics | PLS price volatility; source/review actual factory/router; verify custody and route depth | **Recommended primary**, conditional on funding and review |
| PulseChain CUFFLINKS/bridged WETH | ETH reference and possible broader recognition | Ethereum ETH is not native PulseChain ETH; authentic mapping, bridge custody/redemption and routing need verification | Conditional alternative only if measured routes beat WPLS; no address assumed |
| PulseChain CUFFLINKS/IMD | Thematically close to IMD | No authentic PulseChain IMD mapping or deep market established; unsupported by current IMD launch capabilities; two speculative assets | Reject for launch under present evidence |
| Ethereum CUFFLINKS/ETH | Native ETH, broader infrastructure; available IMD capability category | Different chain scope; gas and audience friction; launchpad economics need review | Best ETH route **if requester explicitly switches chain** |
| Ethereum CUFFLINKS/IMD | Genuine mainnet IMD and community fit; capability category exists | IMD volatility, quote depth, hooks/trade cuts and user onboarding; no assumed sustainable fees | Optional later market only with chain switch and quantitative depth review |

**P — strongest combined setup:** keep one canonical token on PulseChain, one funded WPLS pool and an off-chain creative relationship to IMD. Pay future authorized IMD jobs through the authentic supported-chain workflow with a capped separate operating budget; never bridge Ricky just to manufacture an “integration.” No new bridge, hook or multi-chain token in the baseline. If platform launch support is mandatory, stop the token track until the requester chooses a supported chain or an independently built PulseChain deployment route.

### Liquidity sizing, derived planning model

**P/I:** For a balanced constant-product pool with quote reserve `Q` and buy input `q`, ignoring fees, average execution-price premium to starting spot is `q/Q`; output shortfall against a spot quote is `q/(Q+q)`. These are different metrics. Requiring no more than 5% average premium on a $500 buy implies **Q ≥ $10,000**, total pool value approximately **$20,000**. Require measured round-trip routing costs too; this model is not a live quote or a universal AMM formula.

| Total balanced liquidity USD | Quote side USD | Approximate average premium: $100 buy | $500 buy | $1,000 buy |
|---:|---:|---:|---:|---:|
| 10,000 | 5,000 | 2% | 10% | 20% |
| 20,000 | 10,000 | 1% | 5% | 10% |
| 50,000 | 25,000 | 0.4% | 2% | 4% |

At the baseline $20,000 pool illustration, 900M tokens against $10,000 of WPLS sets token price approximately **$0.0000111111**, initial FDV **$11,111.11**. The quoted token-side $10,000 is a marking of freshly issued inventory, not another $10,000 cash expenditure. External quote capital is $10,000, plus gas/fees and operational costs. This opening valuation is intentionally modest and arbitrary; it does not forecast price or establish intrinsic value. The approved funding amount and contemporaneous WPLS valuation must set the actual ratio later. Supply denomination does not create wealth.

## 6. IMD integration and participation plan

Everything below is **P**. No partnership, endorsement, live bot, existing Ricky integration or paid workflow is claimed.

**Narrative role:** Ricky hires “the Paper Trail” to write excuses; a creative swarm keeps finding receipts instead. In factual copy call it “a proposed creative workflow using IdentityMD tools,” not “official IMD coin.” Use plain text naming and links; IMD logos require permission. Autonomous output is a draft, not legal clearance or proof.

Workflow: approved brand brief and verified fact IDs → bounded meme-writing job → image/layout concept drafts → human originality/likeness/license check → separate factual and risk review → requester approval → authorized publication later. A creator can work manually with the same prompt and scoring; no paid AI service or token balance required to join. Agents receive no private keys, signing requests or authority to post. Operator credentials stay server-side in Phase 2.

Three repeatable programs:

1. **Alibi Lab:** participants submit a two-line original excuse and its contradictory receipt. Weekly judging: 40% joke clarity, 30% originality, 20% character consistency, 10% accessibility. Entries credited with opt-in attribution. Human shortlist prevents agent spam dominating. No purchase, burn, repost or friend-tag requirement.
2. **Receipts vs Excuses:** an IMD maker and a community illustrator transform the same approved brief in different ways. Publish the prompt, approved asset provenance and actual corrections after permission. Let audiences discuss craft rather than vote on token price. Label any paid contributor and sponsor.
3. **International Meme Police case files:** rotating fictional charges such as “possession of an unverified roadmap.” One editable caption template, one agent-assisted variation, one human winner. No real-person accusations. Run a judged creative contest, not a random prize lottery.

**P:** Pilot without monetary prizes; use credit and featured artwork under explicit permission. After budget approval, offer fixed commissions (illustrative $50–$150 per accepted work) from operating cash, not tokens contingent on trading or burn size. Final eligibility, countries, age rules, rights, judging, conflicts and tax reporting must be approved before any competition opens. Keep optional attribution separate from payment identity. Do not collect unnecessary personal data or publish private entrant information.

Cross-community value: Ricky gains repeatable story material and production provenance; IMD makers gain credited demonstrations and optional paid work; both gain discussion around transparent creative methods. Measure distinct returning makers, helpful revisions, opt-in collaboration and attributable completed work. Do not use bought engagement, coordinated trading, engagement farms, fake testimonials or invented “swarm-approved” claims.

Dependencies: check current IMD pricing/capabilities and terms before each paid batch; cap spend, limit attempts, record actual outputs and obtain publication permission. If network access or rights are unsuitable, use an equivalent manual creative workflow and remove the IMD integration claim. No essential token function should depend on a creative service uptime.

## 7. Premium mobile-first website blueprint

**P:** Editorial “booking dossier,” not a wall of price widgets. A compact navigation and a portrait hero present Ricky being escorted away; ink background, ivory typography, gold cuffs, cyan camera flash. Mobile first at 360 CSS px, with tablet and wide layouts. No live site is built in Phase 1. The SVG concept sheet in `preparation/visual-direction.svg` is a non-production composition study only.

### Page structure and copy hierarchy

| Section / route | Purpose and required content | Dependencies |
|---|---|---|
| `/` hero | CUFFLINKS; “Expensive suit. Free cuffs.”; one-sentence fictional premise; development status; primary “Meet Ricky” and secondary “Read the receipts” | Approved B1 brand; legal review |
| Story / case file | Character, recurring scene, original episode gallery; explicit fictional status | Brand bible; licensed assets |
| Token dossier | Approved T1 supply/allocation/taxes; vesting charts and role explanations; fees separately disclosed | Approved economics; verified contract facts |
| `/verify` | Chain ID 369; full canonical token address; copy button; explorer; source/compiler details; independent review report; pool, router, treasury, vesting and LP-lock addresses | Deployed and independently reconciled manifest, later approval |
| `/burns` | True supply reduction metrics, transaction history, confirmation/stale states and satirical explanation | Reviewed burn semantics; indexed logs; RPC reads |
| `/memes` | Original templates, plain-language participation rules, credit and licensing; no sign-in needed to view | Rights register; competition rules |
| IMD creative desk | Precisely describe actual tools used and link authentic IMD docs; provenance, no endorsement badge | Confirmed jobs/terms and permission |
| Risks / FAQ | Total-loss warning, liquidity/quote/bridge/admin risks, no profit/revenue entitlement, fiction, lock expiry, contacts | Legal review; verified implementation |
| Footer | Controlled social links only, official-contract verification path, privacy/terms, rights and revision date | Requester-controlled channels; signed-off disclosures |

Before deployment: “Phase 1 concept. No project token deployed.” Address, burn data and social slots are **null/unset**, not plausible-looking fake values. There is no buy link until canonical details are verified and publication approved. Never populate project fields with the reference token.

At launch: full address visible without wallet connection. Any “Trade” button goes through chain/address verification and fee/risk context. Prefer an external approved DEX link over a custom router or opaque embed. A read-only burn tracker does not require connecting a wallet. Optional self-burn interface is a separately reviewed feature with amount, irreversible effect and transaction preview; it requires express feature approval and must be accessible independently of marketing animation.

### Functional and security requirements

- Fast static reading surface; budget hero imagery under 250KB mobile, total initial payload target under 1MB; no autoplay video. Performance targets: LCP ≤2.5s, CLS ≤0.1, INP ≤200ms on representative mobile tests. Targets, not observed metrics.
- Meet WCAG 2.2 AA direction: real headings, descriptive alt text, keyboard operation, focus visibility, reduced motion and adequate contrast. Meme text remains readable as text/alt text, not only pixels. [W3C recommendation](https://www.w3.org/TR/WCAG22/).
- Touch targets at least 44px design goal; no horizontal scrolling for addresses/tables at 360px; address copy feedback does not obscure chain labels. Body 16–18px, short lines, no tiny risk footnotes.
- Data records include chain, contract, block hash/number, source, retrieved UTC and status. Decimal-safe formatting; pagination of burns; empty/error/loading states; no falling back to fabricated zero for network failure.
- Approved RPC read sources with health monitoring and independent reconciliation; no signing secrets in client code. Chain mismatch disables transaction actions. Content Security Policy, restricted third-party scripts, dependency pinning, rate limits and sanitized submissions.
- Minimal analytics with documented retention/consent and bot filtering; no “online now,” holder-growth ticker or visitor counter unless evidence supports it. No contact or prize data on public IPFS. Account permissions and DNS changes reviewed by two people.
- Corrections panel and immutable versions of economic disclosures; an emergency banner can announce uncertainty but cannot change token rules. Maintain a controlled recovery publication channel before launch.

**Website disclosure draft:** “CUFFLINKS is a proposed fictional meme project. It is not affiliated with any police agency, real gangster or existing RICKY token. Cryptoassets can lose all value. Zero token tax does not remove network fees, DEX fees, slippage or tax obligations. Liquidity locks and burns do not guarantee a market or price. IdentityMD involvement, if implemented, is a creative tooling relationship unless a separate agreement says otherwise.” Replace “proposed” only after approved verified launch state exists; do not claim affiliation by implication.

## 8. Visual concepts and production brief

**P:** These are original direction specifications and an original vector study, not final approved assets. Phase 2 produces layered masters, final raster exports and independent rights review. No AI raster generation or external stock image is included in this phase.

| Asset | Concept | Phase 2 specifications |
|---|---|---|
| Logo | Original RC monogram connecting a square cufflink to an open steel cuff; wordmark CUFFLINKS in custom compressed capitals | Master SVG/PDF plus transparent PNG; monochrome and dark/light variants; clear space one cuff radius; test at 24/32px; no resemblance to luxury labels |
| Avatar | Ricky’s asymmetric eyebrow, silver hair streak, plum collar, and raised cuffed wrists at lower edge | 1024² master; 400² / 128² exports; face inside central circular crop; no small slogan or ticker |
| X banner | Ricky centered-right escorted by two invented international officers; left headline “Expensive suit. Free cuffs.”; receipt trail below | 1500×500 export and layered master; keep important text clear of lower-left avatar overlap and mobile cropping; no address until verified |
| Website hero | Editorial arrest walk under exaggerated camera flash, velvet-rope luxury exit becoming a booking queue | Desktop landscape and separately composed portrait, not just cropped; decorative police tape uses invented words |
| Meme template family | Ivory case-file frames; stable character silhouettes; detachable caption, receipt and transaction-proof panels | 1080² and 1080×1350 versions, 16:9 variants; editable captions; alt text and source manifest |

### Twelve original meme concepts

| ID | Visual / scene | Exact original caption | Repeatable community variation / guardrail |
|---|---|---|---|
| M01 | Tailor shows gold cufflinks; officers add steel cuffs | “Expensive suit. Free cuffs.” | Substitute the luxury item; never imply a real arrest |
| M02 | Ricky presents a seed phrase card; desk officer points to a holding-room key | “Self-custody met custody.” | Describe a custody misunderstanding without revealing actual phrases |
| M03 | Airport lounge door becomes a precinct door; receipt printer rolls out itinerary | “He asked for a cross-chain transfer. They transferred him.” | Fictional destinations and chain puns; no genuine travel claims |
| M04 | Ricky holds a blank glossy roadmap; officer stamps it “NEEDS DETAILS” | “The roadmap had an exit. Just not his.” | Replace a roadmap cliché; no allegation about a named project |
| M05 | “Anonymous” name tag; an enormous transparent receipt hangs from the suit | “Private panic. Public ledger.” | Caption the bad anonymity assumption, never dox holders |
| M06 | Two interview desks: Ricky’s alibi versus matching timestamped receipts | “The receipts have receipts.” | Original excuse/contradiction pair; no fabricated chain screenshots |
| M07 | Ricky photographs cufflinks for “Proof of Suit”; officer requests a block hash | “Proof of Suit failed verification.” | Replace vanity credentials with another fictional status symbol |
| M08 | Prison bars form a candlestick chart while Ricky studies the tailoring | “Support found at the booking desk.” | Clearly illustrative chart; no price prediction or genuine prison imagery |
| M09 | Ricky points at a red candle; printer produces a liquidity receipt | “Market cap wore a suit. Liquidity showed up in slippers.” | Educational comparison; any real data requires date and source |
| M10 | Paper labelled “ALIBI” goes through a cartoon furnace; immutable receipt survives | “Tax Fraud Burn: the tokens left. The records didn't.” | Pair with the explicit satire/tax disclaimer; do not burn actual paperwork |
| M11 | Creative agents hand Ricky twelve excuses; human editor marks all with “SOURCE?” | “He hired a swarm. It organized the evidence.” | Credit actual makers; no agent endorsement or invented job claims |
| M12 | Ricky mistakes an LP time-lock calendar for his fictional custody calendar | “The liquidity has a release date. So does the joke.” | Display illustrative dates as illustrative; never fake a lock certificate |

Optional episode extensions: “cold wallet, warm interrogation room”; “slippage in Italian leather shoes”; “burn receipt too long for an evidence bag.” Test for comprehension before making them primary slogans. Every meme receives an originality check, a real-person likeness check, alt text and a simple asset provenance record. Social satire never turns a suspicion into a conviction.

## 9. Seven-day X campaign: 21 English posts

**P — ready copy for the approved concept-reveal stage.** These posts intentionally describe a concept and proposed mechanics, without claiming a launch, actual integration, users, volume or profits. They contain no missing URLs or fabricated placeholders. Suggested editorial slots: 09:00, 15:00 and 21:00 UTC, starting only on a requester-approved date. They are not scheduled or published here. Final media, brand clearance, jurisdictional review and explicit publication approval remain dependencies. Legal review may require jurisdiction-specific additions; “no token sale” language alone does not settle promotion law.

All challenges are informal creative invitations with no promised award, purchase condition, mandatory repost, friend tagging or trading action. A future prize competition needs separately approved rules. Each post text is also provided in `preparation/campaign.csv` for handoff, with concept and alt-text direction. Only the text column is publication copy.

| ID / day / slot | Ready-to-publish text | Meme and accessibility direction |
|---|---|---|
| X01 / 1 / 09:00 | Meet Ricky Cufflinks. Expensive suit. Free cuffs. A fictional gangster comedy concept for PulseChain. No token launched. His first mistake was assuming “public ledger” meant a publicist. | M01; alt: cartoon Ricky with gold cufflinks and steel cuffs between invented officers |
| X02 / 1 / 15:00 | Ricky asked for self-custody. The international meme police heard the second word. Fictional character. Real lesson: know who controls the keys. | M02; alt: Ricky offers a blank key card at a fictional booking desk |
| X03 / 1 / 21:00 | Write Ricky's alibi in six words. Make it original. Our opening statement: “The suit was never in scope.” No buying, tagging friends or reposting required. | M06 blank alibi form; alt includes the six-word prompt |
| X04 / 2 / 09:00 | Ricky requested a cross-chain transfer. They transferred him to another precinct. CUFFLINKS is a concept, not a live token. The itinerary is fiction. | M03; alt: lounge exit leads to cartoon precinct |
| X05 / 2 / 15:00 | Proposed CUFFLINKS rule: 0% token buy/sell tax. Ricky looked relieved until someone explained gas, DEX fees and slippage. Zero token tax does not mean zero costs. | M09 receipt; alt distinguishes token tax from other costs |
| X06 / 2 / 21:00 | Give Ricky's fictional gang a compliance department name. “The Paper Trail” is on the door already. Bonus points for a joke that survives without a price chart. No token purchase needed. | M05; alt: cartoon office with an oversized receipt |
| X07 / 3 / 09:00 | Ricky brought Proof of Suit. The reviewer asked for a block hash. Excellent tailoring remains a terrible substitute for verification. | M07; alt: cufflink photo beside a request for evidence |
| X08 / 3 / 15:00 | Market cap is not a suitcase full of cash. Liquidity is what a trade actually meets. Ricky learned this while trying to expense the suitcase. Fictional comedy, useful distinction. | M09; alt: decorative suitcase versus a labelled liquidity receipt, no real market numbers |
| X09 / 3 / 21:00 | Caption challenge: Ricky says, “The roadmap has an exit.” The officer replies, “For whom?” Write the next line. Original jokes only. Nobody needs to buy anything. | M04; alt: blank roadmap and a fictional officer’s speech bubble |
| X10 / 4 / 09:00 | Proposed feature: “Tax Fraud Burn.” Fictional paperwork, real supply reduction if built. Burning tokens would not erase records, avoid taxes or guarantee price gains. Ricky hates the receipts part. | M10; alt includes the tax and price disclaimer |
| X11 / 4 / 15:00 | A burn claim needs a receipt: chain, contract, amount, transaction and a lower total supply. “Trust me, bro” is not an accounting method. Ricky has requested a second opinion from his tailor. | M06 / M10; alt: evidence checklist, no fabricated transaction hash |
| X12 / 4 / 21:00 | Write a two-panel meme: Ricky's excuse on the left, the receipt on the right. Keep both fictional. No real-person accusations. The funniest contradiction wins our attention, not a promised token reward. | M06 template; alt: two labelled empty panels |
| X13 / 5 / 09:00 | Ricky's proposed next hire: an AI creative swarm to write alibis. Plot twist: it organizes the evidence. We're exploring IdentityMD tools, not claiming a partnership or live integration. | M11; alt: invented creative agents hand Ricky source requests |
| X14 / 5 / 15:00 | Human joke. Agent draft. Human edit. Receipt for the process. That's the creative workflow we want to test for CUFFLINKS. Buying a token is not an entry requirement. | M11 process panels; alt: four labelled creative steps |
| X15 / 5 / 21:00 | Makers: turn “Expensive suit. Free cuffs.” into one original scene. Sketches and words both count. Credit stays attached. We'll ask permission before featuring your work. | M01 template; alt: original scene prompt with a blank caption area |
| X16 / 6 / 09:00 | A locked liquidity position can still sit beside a falling price. Ricky would prefer the shorter slogan. We prefer the complete sentence. CUFFLINKS remains a proposed project. | M12; alt: illustrative lock calendar beside an explicitly fictional chart |
| X17 / 6 / 15:00 | Creator allocation should come with a public vesting schedule, not a private wink. Our proposal: 5% creator, 5% community, 90% initial liquidity. Not deployed. Ricky's wink has been declined. | Allocation dossier; alt repeats percentages and “proposal, not deployed” |
| X18 / 6 / 21:00 | Rewrite this fictional excuse: “I thought the wallet was anonymous.” Keep it under ten words. No doxxing, real names or actual wallet addresses. Ricky's tailor is already busy enough. | M05; alt: blank fictional identity card, no address |
| X19 / 7 / 09:00 | Seven days of Ricky. Still a concept. The test is whether people make better jokes together, not whether we can manufacture a price chart. Expensive suit. Free cuffs. | M01 episode collage, no claimed user count |
| X20 / 7 / 15:00 | If CUFFLINKS can't earn original contributions without promising returns, it shouldn't become a token. Ricky calls that pessimism. The accountant calls it a launch criterion. | M08 / M09; alt: cartoon accountant marks a “participation first” checklist |
| X21 / 7 / 21:00 | Final scene: Ricky is escorted out. His alibi stays on the public ledger. Which original scene deserves another episode? Reply if you want. No purchase required. Fictional character, real creative choice. | Banner / M06; alt: invented officers escort Ricky while a receipt remains |

Keep responses human-reviewed. Do not manufacture replies or quote tweets. Never report entry numbers until deduplicated records support them. If a later campaign introduces a real contract, burn, partnership, prize or purchase CTA, rewrite it from the new approved truth record and review it again; do not simply replace “proposed” with “live.”

## 10. Business case, costs and risk

### 10.1 Demand and growth model

**I:** audience demand is plausible but unmeasured. Existing RICKY proves an idea has been listed, not that a second version is wanted. PulseChain competitors demonstrate recognizable mascots and insider humor; the reference’s low daily median trading volume suggests little dependable monetization. IMD communities might enjoy showing their creative process, but no conversion rate or overlap count was verified.

**P:** run a later, expressly approved 14-day content-only validation, with no token sale and no prize subsidy initially. The current assignment does not wait 14 days or publish anything. Track unique participating humans (with uncertainty, no intrusive identity checks), returning creators, original submissions, opt-in repeat participation and helpful corrections. Do not use follower totals, raw impressions or bots as the primary gate.

Organic loop: recognizable scene → original caption contribution → credited human-edited asset → voluntary sharing → another reusable prompt. Publish craft and corrections, not trading rankings. Neither bots generating endless variants nor price spikes establish retention. A useful character can remain a non-token project if economics fail.

### 10.2 Proposed planning budget — estimates, not quotes

| Item | Low USD | High USD | Budget treatment |
|---|---:|---:|---|
| Brand clearance and jurisdictional legal review | 2,000 | 8,000 | Obtain scope-specific quotes; complex obligations can exceed this |
| Original layered art / typography / template masters | 1,000 | 3,500 | Assignment and license paperwork included |
| Phase 2 site, read-only tracker and accessible layouts | 2,000 | 6,000 | No live build in current assignment |
| Token, vesting, LP custody implementation and independent review | 3,000 | 10,000 | Includes reproducible build/testing; unusual contracts increase cost |
| 90-day editorial/community operations | 1,500 | 4,500 | No market-making or paid engagement |
| Hosting, monitoring and authorized creative-tool usage | 200 | 800 | IMD fee USD value unquoted; pay only from an approved cap |
| **Operating subtotal** | **9,700** | **32,800** | Before contingency |
| 20% contingency | 1,940 | 6,560 | Planning reserve |
| **Operating capital** | **11,640** | **39,360** | May be lost; not funded by assumed token sales |
| Primary pool quote capital | **10,000** | **25,000** | $20k–$50k marked pool target; separate at-risk capital |
| **Total proposed capital at risk** | **21,640** | **64,360** | Fees/FX/tax reserve may add cost |

No funds spent in this phase. These internal estimates are intentionally explicit to permit a commercial decision; no vendor quote or available requester budget is implied. Maintain operating reserves in an approved denomination independent of RCUFF price. Token inventory is not operating cash.

### 10.3 Sustainable revenue options

**P:** revenue should pay for entertainment or work, not require turnover in the token. Baseline token-tax revenue is **zero**. Primary candidates: original merchandise with a vendor and rights agreement; commissioned illustration/caption packages; disclosed sponsored creative episodes reviewed for accuracy. Reject guaranteed buybacks, paid shilling, holder profit distributions and transaction taxes reintroduced under another name. Licensing requires rights that actually exist.

Illustrative contribution model: a $30 shirt nets $8 after assumed production, fulfillment and fees, before fixed expenses and tax. With $1,500 monthly cash overhead, **188 shirts/month** are needed to cover it. A $250 custom meme package contributing $150 before overhead needs **10 packages/month** for that same overhead. A mix of 100 shirts and five packages contributes $1,550. These are scenarios, not margins, orders or demand verified from vendors. Break-even arithmetic alone does not establish sustainability.

Ordinary income belongs to the operating business; holding RCUFF grants no revenue entitlement. Any relationship between business income and community spending requires disclosed accounts and separately approved policy. Treasury token sales create sell pressure and conflicts; they are not the baseline revenue source. If the project works only through continually selling allocations into newcomers, abandon the token business.

### 10.4 Security and operational risk register

| Risk | Severity / likelihood judgment | Required control and residual risk |
|---|---|---|
| Thin liquidity, quote volatility, inability to exit | High / high | Fund minimum quote reserve; disclose route impact; no assurance of resale; locked liquidity still loses value |
| Reference-name confusion and impersonation | High / high | Distinct mark/ticker; explicit unaffiliated notice; full chain/address checks; monitor copycats |
| Founder/team or whale concentration | High / high | Hard allocation ceiling, vesting, linked-wallet disclosures; bot buyers can still concentrate holdings |
| Contract/vesting/LP-lock vulnerability | High / medium | Minimal immutable token, reviewed custody contracts, independent reviewer, invariant and integration tests; audit does not guarantee safety |
| Malicious approvals / fake interfaces | High / medium | Read-only default, narrow approved actions, transaction preview, authentic links, no broad Permit2 prompts for reading |
| Bridge failure if bridged ETH used | High / medium | Baseline avoids bridged quote; authenticate mapping/redeemability if changed; no new Ricky bridge |
| Key compromise / signer collusion | High / medium | Independent multisig signers, hardware-backed procedures, public grants; recovery must not break token promises |
| Burn tracker reorg / decimal bug / stale source | Medium / medium | Pinned blocks, integer arithmetic, log/supply reconciliation, confirmations, stale labels; fail visibly |
| Defamation / likeness / governmental affiliation | High / medium | Invented faces/officers, legal review; combined context can still be misleading |
| AI licensing and copyright uncertainty | High / medium | Human authorship, assignments, provenance, terms review; cannot guarantee exclusive rights in machine-only output |
| Content spam / contest manipulation | Medium / high | Human judging, no trading incentives, transparent conflicts and deduplication; subjective selection remains |
| Unsustainable workload and revenue | High / high | Content-only gate, cash runway, paid-work demand tests; stop token track if failed |
| Jurisdictional promotion/consumer obligations | High / unresolved | Identify entity/markets and obtain counsel’s written route before publication; disclaimer alone insufficient |

### 10.5 Legal obligations to resolve, not assumed exemptions

**V:** The SEC Division of Corporation Finance’s 27 February 2025 meme-coin statement describes typical entertainment-oriented coins and a limited staff view. It is not a binding exemption; facts and circumstances matter, and fraud may trigger other laws. The creator’s compensation, managerial promises, sale method and revenue rights need counsel’s classification. [SEC staff statement](https://www.sec.gov/newsroom/speeches-statements/staff-statement-meme-coins). No “SEC-approved” copy.

**V:** EU MiCA Title II can require an offeror legal person, white paper, notification and compliant marketing; exemptions and admission-to-trading treatment require specific analysis. Marketing must be identifiable, fair, clear and consistent with required disclosures. A meme label alone is not an exemption. [MiCA Articles 4–9](https://eur-lex.europa.eu/eli/reg/2023/1114/oj/eng).

**V:** The UK FCA says the financial-promotion regime applies to firms marketing cryptoassets to UK consumers, including overseas firms and social posts. Determine a lawful communication route and territorial controls before publishing. “Not financial advice” and a broad public X account do not settle that question. [FCA guidance, updated 6 February 2026](https://www.fca.org.uk/firms/cryptoassets/marketing-uk-consumers).

**U:** Requester entity, residence, operational jurisdiction and target markets are unspecified; this report cannot certify legality. Counsel must also scope consumer protection, tax/accounting for allocations and burns, paid-endorsement disclosure, privacy/retention, sanctions and AML duties if the business activity triggers them, competition rules, merchandise returns/product obligations and trademark/likeness risk. Do not collect keys or act as custodian as an informal shortcut. No legal clearance, country eligibility list or compliance certification has been obtained.

## 11. Ownership, IMD terms and third-party restrictions

**P — intended rights position:** all original project-specific copy, compositions, character specifications and concepts in this package are supplied for the requester’s use and intended ownership to the fullest legally possible extent. No voluntary open-source or Creative Commons license is applied to the original deliverables. This intent is not an executed assignment from IMD, an art vendor, a model provider or a community contributor, nor a guarantee that every idea is protectable.

**V/U — IMD review:** official home, docs, token page, public capabilities and OpenAPI were inspected. No output-IP assignment or comprehensive legal terms were found in those reviewed pages. Candidate `/terms`, `/terms/`, `/terms-of-service`, `/privacy` and API `/terms` routes returned 404. Docs' quote “terms” fields concern action admission and result guarantees, not intellectual-property assignment. We did not access private account or commission terms. **Applicable IMD output ownership remains unverified.** Public availability of artifacts and publication features also creates a confidentiality concern; do not submit private or unreleased assets to a publishing workflow without understanding it. [Official docs](https://imd.fun/docs/), [OpenAPI](https://api.imd.fun/openapi.json). Saved fetch failures establish what was tried, not that no legal terms exist anywhere.

**U — required later evidence:** obtain the applicable requester/IMD commissioning terms and versions, a written statement about output rights/publication/retention, and vendor rights before final assets or commercialization. Preparation can proceed with this limitation disclosed; final exclusivity claims cannot. Do not create an implied official IMD partnership because the job used its contributor network.

**V:** The U.S. Copyright Office’s January 2025 report says generative-AI output requires sufficient human expressive authorship for copyright protection; prompts alone do not supply it. Copyrightability, contract ownership and permission to use are different questions. Ideas, short names and common joke mechanics may not be exclusive property. Use human design selection, editing and documentation, and separately clear trademarks. [Copyright Office statement](https://www.copyright.gov/newsnet/2025/1060.html).

| Material / dependency | Current use | Restriction and required action |
|---|---|---|
| Original report copy, campaign, SVG concept | Created for this commission | Intended requester ownership of protectable rights; AI/human-authorship limits remain; obtain any necessary provider/commission assignments |
| Reference token source and metadata | Evidence archive only; not reused implementation | Third-party material retains its licenses; archive is not requester-owned code. The flattened source includes MIT-licensed OpenZeppelin sections; no claim of rights in GoPulse material |
| OpenZeppelin contract library | Proposed Phase 2 dependency only | MIT license permits reuse with notices; retain copyright/license, pin version, audit integration; cannot claim exclusive ownership of library code. [License](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/LICENSE) |
| Fonts | System fonts proposed; no bundled font binaries | Final downloadable fonts need license checks. If using SIL OFL fonts, retain license and respect reserved-font-name conditions; do not sell fonts alone. [OFL text](https://openfontlicense.org/open-font-license-official-text/) |
| Research snapshots / court documents | Evidence and attribution | Third-party content, not original project IP. No blanket commercial reuse permission inferred; use paraphrases and citations, not photos or reproduced pages in marketing |
| Existing RICKY, Teddy, MOG, HOA names/logos | Comparative research only | No association, likeness or logo reuse permission obtained; create a new identity |
| IdentityMD name, marks and tools | Accurate factual reference and proposed workflow | No trademark license, endorsement or output assignment established; use descriptive text, seek logo permission |
| Future commissioned art | Not commissioned here | Signed assignment where lawful; source/master delivery; moral-rights waiver/consent where enforceable; warranties/provenance, third-party carve-outs |
| Community submissions | Not received here | Submitter keeps rights absent agreement; obtain specific opt-in license/assignment for selected works, separate permission for credits; do not appropriate comments automatically |
| Final generated imagery or stock | None included | Check provider/account-specific terms and source licenses before use; no copied cinematic frame, celebrity likeness or agency badge |

Proposed rights paperwork: define originals and third-party exclusions; grant/assign worldwide commercial adaptation and sublicensing rights to the requester where lawful; identify compensation, attribution and portfolio rules; require layered masters and provenance; document human edits; preserve licenses separately. A written agreement needs the actual commissioning parties and their consent. No invented owner identity is entered in this package.

## 12. Source of truth, dependencies and approval gates

**P:** `preparation/source-of-truth.json` is a versioned handoff index. It records proposed values and `null` for unassigned operational values. **It is not an approved deployment manifest.** The report controls if any supporting file is ambiguous. Requester approval must specify its version/hash and any changes; agents then create an approved revision. A fact update does not silently become a design approval.

| Deliverable ID | Deliverable | Must depend on | Output that later work consumes |
|---|---|---|---|
| F1 | Verified facts and source ledger | Dated public sources, chain/block identity, review of discrepancies | Claim IDs, confidence and dated evidence; no allegation promoted to fact |
| R1 | Final recommendation and business case | F1, available capabilities, cost/risk assumptions | Go/no-go rationale and validation plan |
| B1 | Brand, ticker, narrative and character | F1 collision screen; legal/rights clearance; requester approval | Canonical name, style, character and permitted claims |
| T1 | Final economic specification | F1, R1, approved chain/pair/funding; requester approval | Supply, allocations, roles, vesting, LP lock and burn definitions |
| I1 | IMD integration plan | F1 capabilities; B1; approved rights and spending cap | Bounded creative workflow; no unsupported chain/endorsement claim |
| V1 | Visual concepts and final-art brief | Approved B1; F1 content boundaries; rights register | Logo/avatar/banner/templates; final assets deferred |
| W1 | Website blueprint | Approved B1, T1, F1; I1, V1, legal/privacy decisions | Layout, verified-data schema, risk states and accessibility requirements |
| M1 | Marketing campaign | Approved B1, F1, T1; V1; legal/contest clearance | Reviewable 21-post concept campaign; later live claims require new facts |
| L1 | Risk assessment and launch checklist | All above; jurisdiction and operational owners | Measurable gates and stop conditions |
| P2-C | Later token/vesting/LP implementation | Approved T1, chain and real addresses; L1 | Reproducible source/build, tests, ABI, role manifest, independent review |
| P2-W | Later website and final assets | Approved W1/V1; reviewed P2-C manifest; rights clearance | Staged site and complete master/export set |
| P2-I | Later integration/analytics configuration | Approved I1; genuine runtime/terms; no secrets in browser | Reviewed config, provenance and spend controls |
| P2-L | Later launch | All independent reviews; separately approved deployment, funding and publication | Controlled launch and evidence reconciliation |

Changes cascade: rename → all logo/copy/posts/site updated; economics change → contract, diagrams, risk copy and fee claims updated; chain change → pairing, addresses, RPC, explorer, wallet UX, burn indexing, jurisdiction and business budget reviewed; burn definition change → tracker and campaign rewritten; source disconfirmation → every dependent claim corrected. Do not let visual or marketing agents infer tokenomics from a joke.

### Unresolved decision register

| ID | Unresolved item | Recommended default / who resolves / blocking effect |
|---|---|---|
| U1 | Brand and ticker approval and clearance | Requester selects CUFFLINKS/RCUFF conditionally; counsel checks marks; blocks final assets/accounts |
| U2 | New independent project versus any involvement with existing RICKY | Assume independent for preparation; requester must disclose actual rights/control if claiming continuity; blocks continuity claims |
| U3 | Chain and primary quote | PulseChain/WPLS recommended; requester approves; IMD-native launch requirement would require a chain decision |
| U4 | Quote capital and operating budget | Illustrative $10k minimum quote side and separate cash runway; requester approves real amounts; blocks funding |
| U5 | Exact supply/allocations/vesting/lock/burn policy | T1 baseline recommended; requester approval required; blocks implementation source of truth |
| U6 | Legal entity, geography and audiences | No jurisdiction assumed; requester plus counsel resolve; blocks public token promotion/launch |
| U7 | Real beneficiaries, multisig signers, addresses and unlock date | Unset; requester supplies, review verifies; blocks deployment parameters |
| U8 | IMD commissioning/output terms and trademark permission | No rights guarantee; requester/platform evidence and counsel; blocks exclusive-rights or official-affiliation claims |
| U9 | Controlled domain/socials/contact details | Unset; requester-controlled channels later verified; blocks publication links |
| U10 | Final LP lock provider and actual DEX/router/fee behavior | Independently source/review rather than infer from brand; blocks “locked” and fee assertions |
| U11 | Burn feature name comprehension and transaction UI | Prefer Receipt Burn if misread; baseline tracker read-only; requester approves transaction UX separately |
| U12 | Validation metrics and real prize/commission terms | Content-only, no prizes initially; requester approves later rules/budget; blocks contests with awards |

These are later approval dependencies, not reasons to invent deployment values now. This Phase 1 package is useful and complete without knowing a future recipient wallet.

## 13. Measurable launch gates, abandonment and Phase 2 checklist

All numeric thresholds are **P**, precommitted evaluation rules, not results or statistically proven benchmarks.

### Content and commercial go/no-go

Authorize the later 14-day concept pilot only after B1 and legal publication review. Token track requires all of:

- At least **30 distinct plausible human creators**, **60 qualifying original submissions** and **10 creators returning on a separate day**; record bot/deduplication uncertainty and exclude team/paid submissions from organic counts.
- A blinded small comprehension test with at least **20 participants**: ≥70% recall the suit/cuff joke; ≥80% recognize fiction and independence from the existing RICKY; ≥90% understand that burns do not avoid tax or promise gains. Failure on the tax criterion requires renaming and retesting.
- At least **15 independently opted-in repeat participants** across the prospective PulseChain/IMD maker audience; no requirement to prove holdings. Do not extrapolate these to a market size.
- Requester commits **90 days of cash operations** independently of token sales, plus funded approved quote capital. No borrowed “temporary liquidity” arranged to impress a screenshot.
- At least **three genuine paid-work or merchandise purchase commitments**, lawful and documented, from unrelated people before counting business demand; these cannot be invented, self-purchased or needed to enter the creative pilot. Test fulfillment cost before scale.

**Abandon or keep it as non-token art** if these fail after one documented iteration, if demand consists mainly of calls for returns, or if launch capital cannot be lost without relying on buyers to reimburse it. Reject launching under the existing RICKY identity without demonstrated authorization and a compelling reason. Reject a required PulseChain/IMD pool until genuine assets and depth are established. Reject if acceptable rights, legal routes, signer independence or custody controls cannot be secured.

### Phase 2 preparation — only after explicit Phase 1 approval

A separate agent team should split implementation, website/art and independent security/fact review. Contract authors must not be the sole independent reviewers. They must use the approved revision of F1/B1/T1 and update evidence before implementation decisions.

- [ ] Record explicit approval of the exact report/source-of-truth revision and approved scope, including any budget or chain changes.
- [ ] Resolve U1–U12 as applicable; obtain real party/address information. Do not substitute a zero/dead address, test key or guessed identifier for a beneficiary.
- [ ] Produce minimal immutable token plus reviewed vesting/LP custody, reproducible compilation, pinned dependencies, ABI and deployment manifest; distribute supply deterministically.
- [ ] Verify total allocation, decimal scale, no post-creation mint, no transfer tax or setter, no proxy/admin trading path, self-burn conservation and allowance behavior. Test ordinary transfers and routed buy/sell locally and on an authorized test environment.
- [ ] Test cliffs, linear releases, lost-key tradeoffs, recipient permissions, no acceleration, LP custody/maturity, pool authenticity and exact fee paths. Test burn supply/log reconciliation including reorgs, duplicate events, network failures and decimal boundaries.
- [ ] Independent reviewer reconciles source/bytecode/config, allocation, actual control paths, simulation results and all material findings; resolve every critical/high finding and consciously accept documented residual risks.
- [ ] Create final original logo/avatar/banner/memes and master files; record rights/provenance, accessibility and absence of recognizable real-person/agency marks.
- [ ] Stage the website with no real purchase action; test mobile/keyboard/reduced-motion/data-error states; independently reconcile every contract/social link and disclosure with manifest.
- [ ] Configure only approved IMD creative workflows and analytics; human publication review; no private keys or credentials supplied to creative agents.
- [ ] Present a concrete reviewed deployment/funding/publication plan with transaction amounts, recipients, locks, timing, final copy and review reports for **separate explicit approval**.

### Separate execution approvals and launch verification

- [ ] Obtain explicit authorization for deployment transactions; Phase 1 approval alone is insufficient.
- [ ] Obtain explicit funding approval for exact liquidity/operating transactions; no funds move from this report.
- [ ] After approved deployment, verify deployed bytecode/source, all balances/roles, actual pool reserves, LP custody and unlock timestamp. Fresh on-chain evidence supersedes proposals only through an approved revision.
- [ ] At funded launch, target at least $20,000 marked pool liquidity with $10,000 genuine quote reserve; simulate a $500 buy and equivalent-value sell with ≤5% curve impact before venue/gas fees, and disclose total routed costs separately. If quote reserve falls below the target before public launch, pause the launch rather than use stale USD valuations.
- [ ] Review actual holder/team clusters and reveal all concentration; no claim that supply is broadly owned merely because 90% was deposited in an AMM.
- [ ] Obtain explicit publication approval for website, social campaign and competition rules. Add required jurisdictional warnings/legal communications without sacrificing readability.
- [ ] Publish authentic verification path and risk summary; monitor RPC/website failures, impersonation and factual corrections; no autonomous trading, spam or promotional retries.
- [ ] Review retention and cash runway weekly. If data integrity fails, remove transaction CTAs and display stale/incident status; if the thesis weakens, stop promotion and disclose it. Do not imply stopping marketing reverses token ownership or liquidity locks.

## 14. Research and local check limits

Evidence collection took place on 14 October 2026. Raw successful responses, public endpoint provenance, checksums and failure logs are saved under `research/`; derived calculations are reproducible offline with `python3 tools/check_report.py`. The reference RPC calls are pinned; DEX/explorer snapshots are not mutually block-synchronized. Sources can be incomplete, manipulated, delayed or internally inconsistent. No source count is treated as proof.

Unavailable or incomplete research is explicit: full lifetime OHLCV/ATH corroboration, beneficial-holder identity, irreversible LP lock proof, authentic current social analytics, current Finnish case disposition, complete October news coverage, name/domain/handle legal clearance, IMD output-IP terms, authentic PulseChain IMD mapping, and jurisdictional launch clearance. Successful retrieval of a court PDF is not court-docket authentication. No audit of the reference or competitors was performed.

The recorded run passed **35 of 35 local checks** (`checks/local-checks.json`): file integrity, arithmetic, section/campaign coverage, post lengths, SVG XML and source manifest hashes. These checks do not certify research truth, copyright ownership, legal compliance, organic demand or production behavior. No independent reviewer was employed in this phase. The submission verifier checks paths and bytes only.
