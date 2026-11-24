**Uniswap record: merged review by five independent agents**  
Assessment date: **November 24, 2026 (UTC)**. Record: [the pinned Uniswap JSON][record].

The page needs corrections to its project launch label, supply presentation and current Lens attribution, plus clearer support for several key facts. The reviewers found **no mismatching historical proof values**, but that does not mean every published recipe completed unchanged: four reviewers substituted an endpoint for L66. Two missing facts received three top-three nominations each; there was no third majority-ranked omission.

This report merges all five accepted results, [R1], [R2], [R3], [R4] and [R5], each dated November 24. Each covers the same **15 infobox entries, eight summary entries, 119 lines and 26 proofs**. Counts below identify reviewers who explicitly reached the stated conclusion; silence is unknown, and repeated mentions by one reviewer count once. Agreement on a broad topic does not imply agreement on every proposed correction. The merger's source checks add no sixth vote. Source-check metadata flags R5 without explaining why; its findings remain identified and counted, with a specific erroneous assertion rejected below.

Findings shared by **at least three of the five reviewers** come first.

1. **The project launch field uses the v4 launch date — 5/5: R1, R2, R3, R4, R5.** The infobox says January 31, 2025 and cites **L63**, which supports v4's public launch. For Uniswap as a project, use **November 2, 2018**, citing the already-present **L60**. Alternatively, retain January 31 under a label explicitly naming v4. **L65** concerns a third event: Ethereum v4 code deployment on January 23, 2025. L63 itself remains historically correct; the error is the field's scope. Sources: [Hayden Adams's history][history], [v4 launch announcement][v4launch]; all five reviews, section 1 and section 3.

2. **Supply needs a visible snapshot and measurement basis — 5/5: R1, R2, R3, R4, R5.** **L42, L53, L106–L108 and L115** support the displayed numbers at Ethereum block **26,479,958, November 23, 2026, 19:34:47 UTC**. All five report that the uniUSDC quantity had risen at their November 24 blocks, changing the rounded display from **10.00M to 10.65M shares**. R1/R4/R5 supply the exact newer quantity, **10,653,703.835421748393660822**, versus the historical **9,997,120.750654657807308770**; R2/R3 report the matching rounded quantity. uniUSDT and uniETH exact quantities also changed, but still round to the displayed 2.83M and 0.7K. Retain the historical figures with their date/block, or add a separately dated current snapshot. Preserve the original proof observations. Evidence: each review's section 3, using the record's getter requests through [dRPC][drpc]; the snapshot comparison below supplies the blocks and units.

   **The 1B UNI getter is not wrong.** All five distinguish `totalSupply()` from the result after subtracting the configured burn recipient's balance (**L54–L55**). Sending UNI to that recipient does not lower the getter. The three Earn figures count vault shares, not deposited USDC, USDT or ETH, and 151 S0CKS counts collectibles. Neither the getter nor the single-recipient subtraction is a circulating-supply audit. R5 calls the infobox's historical line support “full,” while R1–R4 call it “partial”; all five identify the missing display date/basis. Sources: the reviews' reproduced reads, [UNI contract source][unisource], [Earn documentation][earn].

3. **SOCKS redemption is historical; present physical fulfillment is unverified — 5/5: R1, R2, R3, R4, R5.** In Tokens, **L30** explicitly supports historical redemption, while **L53** verifies token identity and state. Neither establishes an operating fulfillment service on November 24. Use “historical sock-redemption token” or explicitly mark current availability unverified. Do not assert that redemption has ended. S0CKS minting/controller evidence in **L114–L116** does not settle physical fulfillment either. Sources: [legacy Unisocks site][sockssite], [published project addresses][socks], all five reviews' Tokens checks.

4. **The Foundation component of Contributors needs direct supporting text — 5/5: R1, R2, R3, R4, R5.** **L70** establishes Labs' work and **L39** community v4 contributions. **L102** says most Foundation staff moved to Labs; that statement alone does not establish the Foundation's contributions. Add a line describing its documented governance, developer or audit support, and distinguish historical contributions from current responsibilities. The existing list is defensible; no reviewer establishes that the Foundation dissolved. Sources: [Foundation impact reporting][foundation], [Labs' About page][about], [v4 community credit][v4launch].

5. **Website lacks an explicit domain-attribution assertion in its cited lines — 4/5: R2, R3, R4, R5.** **L01 and L70** describe the app and Labs' products but do not explicitly say that uniswap.org is the official website. The [official directory][directory] confirms the domain; add that assertion to a line and cite it. R1 accepts the existing linked metadata as sufficient. Thus this is a support-standard disagreement, not evidence that the website is false. R2–R4 grade it partial; R5 grades it unsupported.

6. **Lens has lost current directory support — 4/5: R1, R3, R4, R5.** The infobox's “@Uniswap on Lens” relies on **L73**. These reviewers found no Lens listing in the current [official-directory article][directory], whose API reports an update at **November 23, 2026, 20:40:59 UTC**, after the record's source reading. The other nine named accounts remain listed. Remove Lens from a current verified list or label it historically listed/current attribution unconfirmed. Absence from the directory does not establish deletion, changed ownership or fraud. **R2 reports only an access failure and is not counted as confirming removal.** R4/R5's “full” historical support verdicts and their current-staleness findings address different questions. The merger also confirmed the directory's current contents and revision time.

7. **All 26 proof datasets have reported matching values — 5/5: R1, R2, R3, R4, R5 — with a material recipe qualification.** R1/R3/R4/R5 label all 26 reproduced. R2 labels 25 reproduced and **L66** access-limited, then reports that its additional dRPC receipt read matched the expected fields. None reports a numerical mismatch. All used dRPC for historical state reads after PublicNode access problems. This supports the historical observations, not claims about every broader implication of them. The full proof inventory below preserves these limits. Sources: all five reviews, section 2; exact requests in [the record][record].

   **L66's exact published endpoint did not complete for 4/5: R1, R2, R4, R5.** PublicNode returned the deployment transaction but a null receipt; dRPC supplied the matching receipt. L66 names no fallback. R3 reports success on PublicNode as written. Add an explicit fallback to L66. This is a repeatable access/recipe-portability problem, not evidence that the sender or deployment transaction is wrong. R3's successful attempt also prevents calling the proof universally impossible to rerun. Sources: [PublicNode][publicnode], [dRPC][drpc], the record's L66, and the individual proof tables.

8. **Summary 8 correctly exposes stale guide wording; specify v4 and its evidence — 5/5: R1, R2, R3, R4, R5.** **L117** accurately attributes the guide's statement that fees apply only to v2/v3, but that statement is stale as a description of deployment. **L118** cites Labs' November 16, 2026 report of active v4 protocol fees on **Ethereum, Arbitrum, Base, OP Mainnet, BNB Chain, Polygon, Robinhood Chain and Arc**. Replace “some newer pools” with a dated, attributed v4 description. **L44 proves only Ethereum's configured controller**, not per-pool activation, realized revenue or eight-chain coverage. The additional five-chain expansion was proposed; these reviews do not establish its execution. Sources: [UNI guide][uni], [Labs' November 16 governance post][v4fees]. R2 additionally reports pool-setting reads, but that is one review's supplementary evidence, not a five-review cross-chain audit.

9. **The chain list combines different product scopes — 5/5: R1, R2, R3, R4, R5.** **L01, L94, L95 and L119** support the named examples but mix app/API availability and contract deployments. Do not imply identical version, Wallet or API functionality everywhere. **A narrower finding has 3/5 support: R2, R4, R5 explicitly identify L119's 26 PoolManager networks as 22 non-test networks plus four testnets**, rather than 26 mainnets. The infobox itself says “and others,” so its examples are not contradicted. The four are Arbitrum Sepolia, Base Sepolia, Ethereum Sepolia and Unichain Sepolia. Sources: [deployment directory][deployments], [Arc announcement][arc], [Elysium announcement][elysium].

10. **The dated TVL entry is supported as an attribution, not disproved by today's figures — 5/5: R1, R2, R3, R4, R5.** **Size / L90** explicitly records DefiLlama's combined Uniswap TVL of $3.11B on November 23, 2026. Reviewers encountered different live figures and a daily API series sampled at midnight. Those observations do not recover or refute the earlier intraday reading. Keep the date and attribution; add the original capture time/archive if available. If updating, give the new observation its own date and the same combined-TVL basis. Sources: [DefiLlama's combined-protocol API][tvl] and [dashboard][tvldashboard], with access and timing qualifications in each review. No reviewer supplies an independent reserve aggregation validating the $3.11B measurement.

11. **The fee value is supported; “Price” is an ambiguous label — 3/5 request a rename: R1, R3, R4.** **L05, L06 and L10** support zero Labs interface fee plus applicable pool/network costs; all five accept that qualified value. Use “Swap costs,” “Trading cost” or “Fees” for clarity. R2/R5 describe it as cost of use without explicitly proposing this rename. The zero interface fee does not imply zero pool fees or free execution through every third-party frontend. Source: [Labs' fee article][fees], effective December 27, 2025, and [pool-fee documentation][poolfees].

12. **Missing: concentrated liquidity and the boundary on fee earnings — 3/5 top-three nominations: R1, R4, R5.** **L12, L25 and L27** discuss pricing, NFTs and active liquidity without explaining LP-selected ranges or why a position stops earning fees outside its range. Add the v3 mechanism and its consequence. R4 additionally emphasizes single-asset exposure and impermanent-loss risk; R5 extends the basic range model to v4. Those extensions are not three-vote findings. Sources: [Introducing Uniswap v3][v3] and [concentrated-liquidity documentation][concentrated]. This majority nomination includes the source-flagged R5; R1/R4 independently nominate the same central omission.

13. **Missing: the one-time 100 million UNI treasury transfer to the burn recipient — 3/5 top-three nominations: R1, R2, R3.** **L54–L55** give the recipient balance and subtraction, while **L64/L109** mention UNIfication without stating this transfer's size or treasury origin. It explains most of the historical 114.51M recipient balance and prevents attributing the whole balance to fee-funded releases. Agreement is on the **amount, origin and distinction from ongoing fees**. R1/R2 give December 27, 2025; R3 repeats the governance page's December 29 date. That date dispute is resolved separately below, without converting it into three votes for December 27. Sources: [executed UNIfication proposal][unification], [execution transaction][burntx], R1–R3 section 4.

14. **Missing: governance's DUNI legal structure — 3/5 recognize the omission: R1, R2, R3; only 2/5 nominate it in their top three: R1, R2.** R3 explicitly considered it but did not rank it. **L38, L47 and L81** explain rights and onchain control without describing the offchain entity. The executed proposal records adoption of DUNI, a Wyoming decentralized unincorporated nonprofit association, on **September 12, 2025**, with capacity to engage service providers and enter contracts. Source: [executed DUNI proposal][duni]. Recognition of the omission is a majority finding; its priority is not.

The following findings were raised by **only one or two reviewers**, or involve disagreements that must remain visible.

1. **Add explicit block-header verification to the state-proof recipes — 2/5: R2, R4.** The 24 state proofs (**L42–L59, L105–L108, L115–L116**) give block number/hash metadata but list only contract calls. R2/R4 explicitly flag the absence of a request that verifies the header hash and calendar date; R4 also requests a chain-ID check. They supplied these reads and confirmed the metadata. Other reviewers also added checks but did not diagnose the omission as a defect. Add shared `eth_getBlockByNumber` verification, and preferably `eth_chainId`, with required matches. **L65 already includes its deployment-header request.** Neither reviewer treats this as an unknowable missing input or a final value failure. Evidence: the record's rerun objects and R2 section 2 / R4 P2.

2. **Summary 3 omits the delegation prerequisite — 2/5 request a correction: R1, R2.** **L38/L104** support governance context, but L104's v2 fee split does not establish voting eligibility. Clarify that holders delegate voting power to themselves to vote directly, or delegate to another voter. R3–R5 accept the existing statement as a high-level description; R4 acknowledges eligibility nuance without declaring the summary wrong. The distinction is between a general governance right and immediately usable voting power. Source: [official voting guide][voting], read November 24, which also requires delegation before a vote becomes active.

3. **Summary 5 should specify protocol-fee release — 2/5 request narrower wording: R1, R2.** **L20/L21/L54** describe the UNI-funded release mechanism. Say “collected protocol-fee assets” to distinguish them from LP fees, and avoid implying identical direct burn execution on every chain. R3–R5 accept the sentence as a description of the documented design, with limits. Sources: [protocol-fee overview][feeoverview], [releaser variants][feedeployments]. **R2 alone (1/5)** reports a November 6 X Layer proposal describing fees that could not yet be released and corresponding UNI not yet burned; R2 found no confirmed execution of its fix by the review date. Preserve that dated report rather than asserting that the issue necessarily remains unresolved now. Source: [X Layer governance discussion, topic 26337][xlayer].

4. **UNIfication execution date differs from the UI — 2/5: R1, R2; R3 repeats the conflicting UI date.** **L109**, outside the infobox and summary, accurately reports what the governance page displays: December 29, 2025. R1/R2 instead identify successful execution of proposal 93 at **Ethereum block 24,106,378, December 27, 2025, 20:33:11 UTC**, transaction **`0x091f0083242a777d55821c1189e568d6d033d9da501b75087dc736fa143d2c1e`**. The merger independently fetched its successful receipt and block header through [dRPC][drpc], confirming the timestamp and 100M UNI transfer from the governance timelock to the configured burn address. Use the transaction date for the execution fact, while noting the conflicting displayed date. Do not silently change a sentence about what the UI says into one about chain execution. Sources: [execution transaction][burntx], [proposal 93 UI][proposal93], [forum proposal][unification].

5. **Additional line-support and scope refinements are minority findings.** **R1 alone (1/5)** asks that Controlled by (**L43/L47/L59**) name the tested owner roles more precisely; R2–R5 accept “v4 settings” as a sufficient limitation. **R2 alone (1/5)** grades Deployed by (**L66**) partial because the displayed value should explicitly name Ethereum v4 PoolManager and the prose does not spell out the sender; R1/R3–R5 accept the proof object's address as support. R2 also flags seven exact account URLs (**L71–L76/L112**) and the 11 bridged-network names (**L111**) as present in sources rather than line assertions. **R3 alone (1/5)** additionally notes that UNI/SOCKS addresses appear in proof request targets and sources rather than line prose (**L42/L53**); R4/R5 explicitly accept proof targets as part of a line. These concern different fields and are not combined into a two-vote finding. The merger accepts structured proof evidence, but recommends explicit names/addresses where clarity improves. Sources: the record's fields, [official directory][directory], [UNI guide][uni], [deployment transaction][deploymenttx].

6. **R5's proposed L53 fallback repair is erroneous — 1/5 raised it; rejected after inspecting the pinned JSON.** R5 says L53 lacks an `archive_fallback`. It actually contains **`https://eth.drpc.org`**. R2/R3 explicitly report using that listed fallback. Preserve R5's disclosed access problems and matching observations, but do not report a missing L53 fallback as a record defect. **L66 really does lack that field.** Evidence: [record][record], L53 and L66 `rerun` objects; R5 section 2.

7. **Other suggestions outside the reviewers' ranked omissions remain single-review observations.** **R2 (1/5)** mentions an omitted Farcaster account, pointing to Labs' [blog index][blogindex]; this does not establish the old Lens account's status. **R3 (1/5)** considered a broader v4 security account, using the [v4 announcement][v4launch] against **L92**'s single audit, but did not rank it. **R4 (1/5)** suggests making Labs' protocol-development contribution explicit in **L70** to support summary 2 more directly; [About Labs][about] supplies the external support. These are additions or presentation refinements, not five-review findings of falsehood.

For the requested **three most important missing facts**, the recommendation is **concentrated liquidity, the treasury burn, and DUNI**. The first two have three top-three nominations. DUNI wins an editorial tie-break among four topics with two nominations, because it explains who can act for governance outside the chain and connects governance, Labs and Earn. R3's unranked recognition supplies additional coverage, but is not a third top-three vote. This ranking is the merger's judgment, not a claim of three-way majority priority.

| Missing fact | Top-three nominations | Closest existing lines and why they are insufficient | Evidence and disposition |
|---|---|---|---|
| LP-selected price ranges and out-of-range fee cessation | **3/5: R1, R4, R5** | L12 gives standard pricing; L25 says positions are NFTs; L27 mentions active positions without defining the range condition. | [v3 announcement][v3], [range documentation][concentrated]. **Recommended addition 1.** |
| One-time 100M UNI treasury burn | **3/5: R1, R2, R3** | L54/L55 give balances; L64/L109 mention UNIfication without the amount and treasury origin. | [UNIfication][unification], [execution receipt][burntx]. **Recommended addition 2**, with the independently checked December 27 date and the reviewer disagreement disclosed. |
| DUNI legal structure | **2/5: R1, R2**; R3 recognizes it unranked | L38/L47/L81 describe rights, governor and vault control; no substantive line explains the offchain legal entity. A source URL containing DUNI is not an explanation. | [Executed DUNI proposal][duni]. **Recommended addition 3 by editorial tie-break.** |
| Trading volume as a measure of exchange activity | **2/5: R2, R3** | L32/L90 give TVL, which measures a different quantity. | R2 cites Labs' **October 22, 2026 claim of over $4.5T** in cumulative swaps in [Aggregator Hooks Are Live][aggregator]; R3 cites the undated [About page][about]'s **over $3T**, read November 24. Agreement is on the missing metric, not one current number. R2 also reports approximately $4.05T from [DefiLlama's DEX API][volumeapi]; do not merge totals across dates/methodologies. |
| UNI holders lack an individual/proportional revenue entitlement | **2/5: R4, R5** | L38 describes governance; L20/L21 and L35/L54/L55 describe release/burning, but do not expressly rule out a passive holder's revenue claim. | [UNI guide][uni]. Add a current-rights statement, without predicting what future governance may authorize. |
| Earn withdrawal liquidity and variable yield | **2/5: R4, R5** | L77–L81 explain deposits, interest, shares and roles; L83/L84 describe supported assets and a dated fee setting, not withdrawal constraints. | [Earn article][earn]: no lockup does not ensure immediately available liquidity; yields vary and are not guaranteed. This does not establish an actual withdrawal failure on the review date. |
| Closure of the SEC investigation into Labs | **1/5: R3** | L93 concerns the separate September 2024 CFTC penalty. | [Labs' February 25, 2025 announcement][sec]. Attribute the investigation's closure with no action to Labs' announcement; do not infer a blanket regulatory endorsement or conflate it with the CFTC matter. |

Every reviewer nominated exactly three items: R1 = ranges/burn/DUNI; R2 = DUNI/burn/volume; R3 = burn/volume/SEC; R4 = ranges/revenue rights/Earn; R5 = ranges/revenue rights/Earn. The table accounts for all **15 nominations** and preserves every two-vote tie.

Suggested text for the three selected additions:

- **Concentrated liquidity:** “Uniswap v3 lets liquidity providers choose price ranges; positions earn swap fees while active within those ranges and stop earning them when the price moves outside.” [Introducing Uniswap v3][v3].
- **Treasury burn:** “Execution of UNIfication on December 27, 2025 transferred 100 million UNI from the governance treasury to the burn recipient, separately from subsequent fee-funded releases.” [Proposal][unification], [transaction][burntx]. The date uses the receipt/header evidence, not R3's UI-derived date.
- **DUNI:** “Uniswap Governance adopted DUNI, a Wyoming decentralized unincorporated nonprofit association, through a proposal executed on September 12, 2025, enabling offchain contracting and engagement of service providers.” [Executed proposal][duni].

For completeness, the following matrix answers **whether every key fact rests on supporting lines**. It retains the reviewers' literal verdicts instead of converting substantive agreement into identical grades. **F = full, P = partial, C = contradicted, U = unsupported**; the five positions always mean **R1/R2/R3/R4/R5**. Historical support, present accuracy and editorial clarity are distinct tests. Evidence is the cited record lines and each linked review's section 1; current-source qualifications are in the findings above.

| Infobox label and displayed content | Exact cited line IDs | R1/R2/R3/R4/R5 | Merged support assessment |
|---|---|---|---|
| Website — uniswap.org | L01, L70 | F / P / P / P / U | Domain externally confirmed; four reviewers require an explicit attribution line. |
| Tokens — UNI governance; SOCKS redemption; uniUSDC/uniUSDT/uniETH shares; S0CKS collectible, all with Ethereum addresses | L38, L42, L30, L53, L106, L107, L108, L111, L115, L114 | P / P / P / P / P | UNI purpose/address maps to L38/L42; SOCKS identity to L53 and historical purpose to L30; Earn identities/share units to L106/L107/L108; S0CKS identity to L115 and mint context to L114. L111 supplies separate bridge context. No address mismatch reported; current SOCKS fulfillment remains unproved. |
| Main contract — Ethereum v4 PoolManager `0x000000000004444c5dc75cB358380D2e3dE08A90` | L14, L13 | F / F / F / F / F | Address and singleton role supported. The field explicitly scopes its selection to v4/Ethereum; it does not encompass every Uniswap version or product. |
| Chains — Ethereum, Base, Arbitrum, Polygon, Unichain, Arc, Elysium and others | L01, L94, L95, L119 | F / F / F / F / F | First five map to L01; Arc to L94; Elysium to L95; additional deployments to L119. Product scopes vary; 26 deployment networks include four testnets. |
| Supply — 1B UNI; 296.99 SOCKS; 10.00M uniUSDC; 2.83M uniUSDT; 0.7K uniETH; 151 S0CKS | L42, L53, L106, L107, L108, L115 | P / P / P / P / F | One-to-one historical numerical support in that order. All identify the omitted display date and measurement basis. uniUSDC's rounded current value changed. |
| Price — 0% Labs interface fee plus applicable pool/network costs | L05, L06, L10 | F / F / F / F / F | Qualified fee description supported; three suggest a clearer label. It is not a UNI market-price quote. |
| Size — $3.11B locked, DefiLlama, November 23, 2026 | L90 | F / F / F / F / F | Fully supported as a dated, attributed combined-TVL claim. Its exact intraday measurement was not independently recovered. |
| Deployed by — transaction sender `0x6b93e3bb9c0780c0f9042346ffc379530a5882c1`, Ethereum | L66 | F / P / F / F / F | Proof identifies the transaction sender; no real-world owner is identified. R2 requests explicit Ethereum v4 scope in the value. Receipt access qualification applies. |
| Controlled by — v4 settings, governance timelock `0x1a9c8182c09f50c8318d769245bea52c32be35bc`, Ethereum | L43, L47, L59 | P / F / F / F / F | L43: PoolManager owner; L47: timelock administrator; L59: three fee-contract owners. R1 requests tighter role/date wording. No inference of custody or arbitrary upgrade power. |
| Founder or creator — Hayden Adams | L37 | F / F / F / F / F | Directly supported; current About/history sources corroborate the historical attribution. |
| Contributors — Labs, Foundation, community | L70, L39, L102 | P / P / P / P / P | Labs/community components supported. Foundation contribution requires a better line than staff-transition L102. |
| Official accounts — three X accounts, GitHub, Discord, LinkedIn, YouTube, TikTok, Reddit, Lens | L40, L71, L72, L73, L74, L75, L76, L112 | P / P / P / F / F | X maps to L40; GitHub L71; Discord L112; LinkedIn L72; YouTube L74; TikTok L75; Reddit L76; Lens L73. R3 separately calls Lens contradicted by the current directory. Four confirm loss of current Lens support; R2 has an access gap. |
| Launched — January 31, 2025 | L63 | C / P / C / C / C | All five identify the v4/project mismatch despite differing grades. L60 supplies the correct project date. |
| App provider — Universal Navigation Inc., trading as Uniswap Labs | L36 | F / F / F / F / F | Legal provider/trade name directly supported. R2/R3 could not fully reopen the current terms; others checked them. |
| Governance delay — 2 days at the Ethereum snapshot | L46 | F / F / F / F / F | Reproduced 172,800-second execution timelock. All limit this to the setting, not the complete governance lifecycle. |

The eight summary entries were also reviewed individually, in JSON array order:

| Entry | Exact cited line IDs | Merged current assessment and evidence |
|---|---|---|
| 1. Pool-based swaps directly from wallets | L01, L02, L11 | **5/5 find no substantive error.** Broad AMM/self-custody description; it does not exclude other routes described in entry 4. Sources: [protocol explanation][how], [Labs terms][terms]. R2/R3's terms-access limits remain. |
| 2. Labs supplies products and helps develop the system | L70, L36 | **5/5 accept the substance.** [About Labs][about] supports product and protocol-development roles; R4 suggests stronger line text for the latter. |
| 3. UNI holders vote on fees/settings | L38, L104 | **2/5 request delegation qualification (R1/R2); 3/5 accept the high-level description (R3/R4/R5).** L104 supplies a fee example, not eligibility. [Voting guide][voting]. |
| 4. Pools and competing signed-order fillers | L01, L11, L18, L68 | **5/5 accept the broad description.** “Some” appropriately limits UniswapX routing. [UniswapX overview][uniswapx]. No particular order outcome was tested. |
| 5. UNI supplied to release fees, then burned | L20, L21, L54 | **2/5 request narrower protocol-fee wording (R1/R2); 3/5 accept the design description with scope limits (R3/R4/R5).** [Fee overview][feeoverview], [releaser variants][feedeployments]. Recipient configuration/balance is not a traced release or universal chain status. |
| 6. Earn deposits enter lending vaults; borrowers pay interest | L77, L78 | **5/5 find no substantive error.** [Earn article][earn] establishes the mechanism. R2 could not reopen that article and corroborated Morpho-vault context through the [executed vault proposal][vaults]. Withdrawal and variable-yield limits are separate omissions. |
| 7. No web-app interface fee; pool/network costs can apply | L05, L06, L10 | **5/5 accept the qualified value.** [Fee notice][fees], [pool fees][poolfees]. R2 saw the 0% notice through a search extract rather than reopening the page. Wording allows routes where the swapper does not directly pay gas. |
| 8. Newer pools charge protocol fees despite older guide wording | L117, L118, L44 | **5/5 accept this as a report of conflicting documentation.** Name v4 and date Labs' eight-chain report; do not use L44 alone as evidence of collections. [November 16 update][v4fees], [UNI guide][uni]. |

The **proof question** is answered at two levels: reported observations match, while a literal recipe can encounter an access failure or omit a verification step. These are the exact aggregate outcomes:

| Reviewer | Reported final classification | L66 handling | Other qualifications |
|---|---|---|---|
| [R1] | 26 reproduced; no mismatches | Null PublicNode receipt twice; matching dRPC receipt twice | Two passes over 45 distinct record requests, plus chain/header checks. Historical state used the fallback. |
| [R2] | 25 reproduced; 1 access-limited; no mismatches | Keeps L66 access-limited as written; extra dRPC check matches | Explicitly identifies omitted header requests in 24 state recipes. |
| [R3] | 26 reproduced; no mismatches | PublicNode succeeded as specified | dRPC four-request batches for L53/L55 failed; individual requests succeeded. Added header checks. |
| [R4] | 26 reproduced; no mismatches | Matching dRPC receipt after null PublicNode result | Adjusted serialization/user-agent and repeated verification; recommends explicit chain/header checks. |
| [R5] | 26 reproduced; no mismatches | Matching dRPC receipt after null PublicNode result | Two individual-request passes; its missing-L53-fallback assertion is rejected. R5 has an unexplained source-check flag. |

Evidence locators for the following inventory are each line's **`rerun.requests`, `expected` and `decode`** in [the pinned record][record], and section 2 of each review. All five report the listed matching observations, with L66's classification difference above. These are reviewer-reported reruns, not a claim that the merger repeated all 26. Common use of dRPC also means this is not validation by five separate archive-node operators.

**B** denotes Ethereum block **26,479,958** (`0x1940d56`), hash **`0xdec7c8b4c9da8e0bd0605c06560c9de53417ceb97ff07a13dcd1c6d55f63875b`**, **2026-11-23 19:34:47 UTC**. **D** denotes block **21,688,329** (`0x14af009`), hash **`0x651a11a4362df710d0c37c686d4c4aca184bb404aa56a64c491e69ef0a174bd3`**, **2025-01-23 16:16:47 UTC**. Every state row below uses B; L65/L66 concern D. Addresses' documented role names were cross-checked against [governance documentation][technical], [fee deployments][feedeployments], [vault governance][vaults] and [Unisocks' project list][socks].

| Proof ID | Read / reported matching observation | What the evidence does and does not establish |
|---|---|---|
| L42 | UNI `totalSupply`, `decimals`: **1,000,000,000 UNI**, 18 decimals | Contract total includes balances at the burn recipient. |
| L43 | PoolManager `owner`: **governance timelock** | Owner setting for this contract, not control of every product. |
| L44 | PoolManager `protocolFeeController`: **`0x89a5d5bf00a27d55c02951e49078a5c5771051db`**, the documented v4 adapter | Configuration only; no per-pool fee or revenue measurement. |
| L45 | UNI `minter`: **governance timelock** | Authorized role, not evidence of mint activity. |
| L46 | Timelock `delay`: **172,800 seconds = 2 days** | Execution delay only. |
| L47 | Timelock `admin`: **`0x408ed6354d4973f66138c91495f2f2fcbd8724c3`**, GovernorBravo | Administrator setting, not every voting rule. |
| L48 | Governor `quorumVotes` plus decimals: **40,000,000 UNI voting units** | Parameter, not turnout or a count of people. |
| L49 | Governor `proposalThreshold` plus decimals: **1,000,000 UNI voting units** | Threshold, not automatic eligibility for any holder. |
| L50 | v2 factory `feeTo`: **TokenJar**, `0xf38521f130fccf29db1961597bc5d2b60f995f85` | Recipient setting, not realized fee proceeds. |
| L51 | TokenJar `releaser`: **Firepit**, `0x0d5cd355e2abeb8fb1552f56c965b867346d6721` | Configured role, not a demonstrated release transaction. |
| L52 | Firepit `threshold`, `RESOURCE`, UNI decimals: **4,000 UNI**, native Ethereum UNI resource | Threshold at B, not an illustrative threshold from documentation or a universal chain value. |
| L53 | Supply/name/symbol/decimals: **296.992857926618025474 SOCKS**, “Unisocks Edition 0,” 18 decimals | Identity/state; current physical fulfillment unverified. Its archive fallback is present. |
| L54 | Firepit recipient and UNI `balanceOf`: **114,511,581.213802937903387397 UNI** at configured **`0x000000000000000000000000000000000000dead`** | Observed recipient and balance, not attribution of every incoming transfer. This address is recorded evidence, not a placeholder. |
| L55 | Supply minus that recipient balance: **885,488,418.786197062096612603 UNI** | Excludes one address; explicitly not circulating supply. |
| L56 | UNI `mintCap`: **2** | Percentage interpretation comes from contract rules/documentation; no automatic inflation established. |
| L57 | UNI `minimumTimeBetweenMints`: **31,536,000 seconds = 365 days** | Minimum interval, not a scheduled annual mint. |
| L58 | v3 factory `owner`: **`0xf2371551fe3937db7c750f4dfabe5c2fffdcbf5a`**, V3OpenFeeAdapter | Factory ownership, not every pool's fee setting. |
| L59 | TokenJar, Firepit and v4 adapter `owner`: **timelock for all three** | These named Ethereum contracts only. |
| L65 | PoolManager code: **empty at D−1; 24,009 bytes at D**, matching expected hashes; header timestamp matches | Code appearance between adjacent blocks, not a source-code audit or public-launch date. |
| L66 | Deployment transaction/receipt: expected sender/factory, D number/hash, **status `0x1`**, PoolManager ownership event | Sender evidence; no named person's identity. Null top-level `contractAddress` is consistent with factory deployment. Four substituted the receipt endpoint. |
| L105 | Each of three Earn vaults `owner`: **timelock** | Ownership setting; curator/allocator/sentinel responsibilities remain distinct. |
| L106 | uniUSDC supply/decimals/symbol: **9,997,120.750654657807308770 shares**, 18 decimals | Shares, not deposited USDC or USD TVL. |
| L107 | uniUSDT supply/decimals/symbol: **2,831,861.076663145183881064 shares**, 18 decimals | Shares, not underlying USDT units. |
| L108 | uniETH supply/decimals/symbol: **715.559292022898531990 shares**, 18 decimals | Shares, not underlying ETH units. |
| L115 | S0CKS supply/symbol: **151**, **S0CKS** with a zero | Whole collectible count; no fungible-token decimal scaling. |
| L116 | S0CKS `minter`: **`0x05931d644063954f35afa3dbefa4725b0ad79f85`**, published controller | Controller identity, not a currently operating redemption service. |

For L65, SHA-256 over decoded bytecode bytes is **`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`** before deployment and **`3316c7b1c67095ef6fc9b7e62fc754ad1e46e1c9119564ea4f5615a252af893e`** at D. L66's transaction is **`0x747e0e02b7590eed32cface28e83260884e0b80675f5ae223c6888053aa68528`**, from the infobox sender to factory **`0x48e516b34a1274f49457b9c6182097796d0498cb`**; the [transaction locator][deploymenttx] and record contain the full expected event fields.

The **November 24 snapshot comparison** keeps the reviewers' observation times separate. R3/R4/R5 use block **26,486,441**, **17:13:59 UTC**, hash `0xa704d746cce746252cc395b3fc0b661ff3ec7debad67e5fc5515d2ee9d2ed039`; R2 uses **26,486,473**, **17:20:23 UTC**, hash `0x78feb513173602081f3abacc13b2c7fcaa927bc6d01a2be7a4d863a20397b74a`; R1 uses **26,486,524**, **17:30:35 UTC**, hash `0xd556234f96e7e69da18a50a05e3ea0331595306a00ba45c132ae7164e7750b94`. All report consistent displayed changes; exact newer quantities below are supplied by R1/R4/R5, with R2/R3 reporting matching rounded values. These are observations at those blocks, not promises about later state.

| Quantity | November 23 at B | November 24 reported observation | Appropriate display treatment |
|---|---:|---:|---|
| UNI contract `totalSupply` | 1,000,000,000 | 1,000,000,000 | Retain with getter basis and date. |
| UNI at the configured burn recipient | 114,511,581.213802937903387397 | 114,547,581.213802937903387397 | Separate dated balance; its increase alone does not trace transfer sources. |
| UNI after subtracting that recipient | 885,488,418.786197062096612603 | 885,452,418.786197062096612603 | Separate calculation, not circulating supply. |
| SOCKS total | 296.992857926618025474 | 296.992857926618025474 | Rounded 296.99 unchanged. |
| uniUSDC shares | 9,997,120.750654657807308770 | 10,653,703.835421748393660822 | 10.00M becomes **10.65M** for this newer snapshot. |
| uniUSDT shares | 2,831,861.076663145183881064 | 2,828,946.545607157380797302 | Rounded 2.83M unchanged. |
| uniETH shares | 715.559292022898531990 | 715.825235953909026170 | Rounded 0.7K unchanged; a more precise display could show 715.83. |
| S0CKS collectibles | 151 | 151 | Whole count unchanged. |

The supply evidence uses the same contract addresses, calldata and decimal interpretations as the original line recipes, changing only the block tag. The relevant Earn addresses are uniUSDC **`0x5B453493D2328E7F747eb2e66446eFe707728be7`**, uniUSDT **`0xb8274eFADB953FE9ae052D481a3FC5B6A3ceD703`**, and uniETH **`0x98D2b241DA14c5dd848812708Eb8A1F3c5512f9d`**; `totalSupply()` uses selector `0x18160ddd`. The November 24 comparison is reported in all five reviews' section 3 and tied to the [governance vault specification][vaults].

Several **limits remain unresolved**. The original intraday $3.11B TVL capture was not recovered. Current physical SOCKS fulfillment remains unverified. The directory supports account attribution, not ownership authentication of each account. Proposed fee expansions and the X Layer fix lack confirmed execution evidence in these reviews. R2 encountered support-page access blocks; R3 could not reopen the terms; successful API access by other reviewers does not erase those individual gaps. R3 and R4 cite different Earn article revision dates: the merger's current publisher API returns **November 19, 2026, 12:04:22 UTC**, supporting R3's date; the two-nomination withdrawal finding is grounded in article content rather than R4's older July date. No claim is made that every source or every live chain setting was independently checked five times.

The orchestration record reports **five accepted results, zero failed results, and five source-checked results, with R5 flagged and no explanation supplied**. A source-check flag is not a finding that every claim in that review is false. Counting R5 preserves the requested five-review panel while making its contribution inspectable. The three-vote concentrated-liquidity nomination and three-vote mainnet/testnet distinction both include R5; their external sources are separately cited. The missing-L53-fallback assertion is specifically rejected on the pinned record, regardless of the flag's unknown cause.

Provenance is preserved through the following immutable review artifacts. The merger verified each local input's SHA-256 against the supplied hash and verified that each linked artifact returns the same bytes. Within batch **`uniswap-reviews`**, each of the five items was one independent review covering all four requested questions; each returned one Markdown result. The supplied batch-brief text is truncated in the orchestration metadata, so this write-up does not invent or amend its unseen wording. All five result reports are complete. This was research only: the orchestration record's `trunk` is null, so there is no built-code repository or commit to name.

| Reviewer key | Input alias | Original result path | Verified immutable result / SHA-256 |
|---|---|---|---|
| uniswap-reviews/review-1 | b01-review-1 | artifacts/goal/batches/uniswap-reviews/items/review-1/result.md | [R1] — `84e842092a9af862a6a314edbcd6e39904b15d4a14441189051da5ac43dc1b1f` |
| uniswap-reviews/review-2 | b01-review-2 | artifacts/goal/batches/uniswap-reviews/items/review-2/result.md | [R2] — `45ac25df8266d288c3f668567557239fed9499284dce18b01f57b6e6096859c8` |
| uniswap-reviews/review-3 | b01-review-3 | artifacts/goal/batches/uniswap-reviews/items/review-3/result.md | [R3] — `479738ac8db29073bfd51c8a5e0f7541d9927dc63c486e148cca96e602202ceb` |
| uniswap-reviews/review-4 | b01-review-4 | artifacts/goal/batches/uniswap-reviews/items/review-4/result.md | [R4] — `e4188d742f9da1205ffd592540b049c6139a7572c583bcc0a2032a8823bb26ac` |
| uniswap-reviews/review-5 | b01-review-5 | artifacts/goal/batches/uniswap-reviews/items/review-5/result.md | [R5] — `695732145c821c8437322597e395a149ca25cec673997f72ee97844782450e32` |

The record itself is **146,644 bytes**, SHA-256 **`8fcca64a613cc56681fcc98e790e563343cf4fa02ac720ff4fe57b17a25f3f17`**, verified during the merge. All conclusions concern this pinned version, interpreted against the dated November 24 observations above.

[record]: https://api.imd.fun/artifacts/8fcca64a613cc56681fcc98e790e563343cf4fa02ac720ff4fe57b17a25f3f17
[R1]: https://api.imd.fun/artifacts/84e842092a9af862a6a314edbcd6e39904b15d4a14441189051da5ac43dc1b1f
[R2]: https://api.imd.fun/artifacts/45ac25df8266d288c3f668567557239fed9499284dce18b01f57b6e6096859c8
[R3]: https://api.imd.fun/artifacts/479738ac8db29073bfd51c8a5e0f7541d9927dc63c486e148cca96e602202ceb
[R4]: https://api.imd.fun/artifacts/e4188d742f9da1205ffd592540b049c6139a7572c583bcc0a2032a8823bb26ac
[R5]: https://api.imd.fun/artifacts/695732145c821c8437322597e395a149ca25cec673997f72ee97844782450e32
[history]: https://blog.uniswap.org/uniswap-history
[v4launch]: https://blog.uniswap.org/uniswap-v4-is-here
[unisource]: https://raw.githubusercontent.com/Uniswap/governance/master/contracts/Uni.sol
[earn]: https://support.uniswap.org/api/v2/help_center/en-us/articles/46865818181901.json
[sockssite]: https://socks.uniswap.org/
[socks]: https://github.com/Uniswap/unisocks-erc721/blob/master/README.md
[foundation]: https://www.uniswapfoundation.org/impact
[about]: https://about.uniswap.org/
[directory]: https://support.uniswap.org/api/v2/help_center/en-us/articles/17522892515341.json
[drpc]: https://eth.drpc.org
[publicnode]: https://ethereum-rpc.publicnode.com
[uni]: https://developers.uniswap.org/docs/ecosystem/governance/uni
[v4fees]: https://gov.uniswap.org/t/temp-check-protocol-fee-expansion-v4-on-five-more-chains/26349
[deployments]: https://developers.uniswap.org/deployments
[arc]: https://blog.uniswap.org/pt-BR/uniswap-is-live-on-arc
[elysium]: https://blog.uniswap.org/elysium-is-live-on-uniswap-apps
[tvl]: https://api.llama.fi/protocol/uniswap
[tvldashboard]: https://defillama.com/protocol/uniswap?denomination=USD
[fees]: https://support.uniswap.org/api/v2/help_center/en-us/articles/42640092742541.json
[poolfees]: https://developers.uniswap.org/docs/get-started/concepts/fees
[v3]: https://blog.uniswap.org/uniswap-v3
[concentrated]: https://developers.uniswap.org/docs/get-started/concepts/liquidity-providers/concentrated-liquidity
[unification]: https://gov.uniswap.org/t/executed-unification-proposal/25881
[burntx]: https://etherscan.io/tx/0x091f0083242a777d55821c1189e568d6d033d9da501b75087dc736fa143d2c1e
[duni]: https://gov.uniswap.org/t/executed-governance-proposal-establish-uniswap-governance-as-duni-a-wyoming-duna/25770
[voting]: https://developers.uniswap.org/docs/ecosystem/governance/guide-to-voting
[feeoverview]: https://developers.uniswap.org/docs/protocols/protocol-fee/overview
[feedeployments]: https://developers.uniswap.org/docs/protocols/protocol-fee/deployments
[xlayer]: https://gov.uniswap.org/t/26337
[proposal93]: https://vote.uniswapfoundation.org/proposals/93
[deploymenttx]: https://etherscan.io/tx/0x747e0e02b7590eed32cface28e83260884e0b80675f5ae223c6888053aa68528
[blogindex]: https://blog.uniswap.org/llms.txt
[aggregator]: https://blog.uniswap.org/aggregator-hooks-are-now-live
[volumeapi]: https://api.llama.fi/summary/dexs/uniswap
[sec]: https://blog.uniswap.org/a-win-for-defi
[how]: https://developers.uniswap.org/docs/get-started/concepts/how-uniswap-works
[terms]: https://support.uniswap.org/api/v2/help_center/en-us/articles/30935100859661.json
[uniswapx]: https://developers.uniswap.org/docs/liquidity/uniswapx/overview
[vaults]: https://gov.uniswap.org/t/executed-temp-check-rotate-sentinel-addresses-on-the-duni-owned-uniswap-earn-vaults/26281
[technical]: https://developers.uniswap.org/docs/ecosystem/governance/technical-reference
