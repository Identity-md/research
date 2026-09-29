# Fren Pet / IMD: purchase claims, token relationship, and X sentiment

Research date: **30 September 2026**. This is a public-source research snapshot, not a live market feed. “Recent” primarily means September 2026; an older August post is explicitly identified below.

## Answer

**The full premise—someone recently made a large purchase of Fren Pet and added it to their project—could not be verified.** The clearest named purchase lead is **Ansem (@blknoiz06)**: a third-party mirror attributes an August 2 post to him saying he bought IMD and intended to continue buying. It supplies neither a purchase amount nor evidence of integration into his own project. This is a reported self-disclosure, not a verified whale transaction. [Ansem post mirror](https://zamantika.com/th/blknoiz06/status/2084000824796344387); [original X permalink, inaccessible during research](https://x.com/blknoiz06/status/2084000824796344387).

**The IMD connection is much better supported:** the project's official token history explicitly traces FP → VIBE → IMD. The accessible X-derived commentary is predominantly bullish about the developer, AI work, and token burns, but the sample is too small and selectively indexed to establish Twitter-wide sentiment. There is no defensible sentiment finding specifically about the unverified purchase-and-integration event. [Official IMD token history](https://imd.fun/token/).

## Latest accessible market snapshot

The user-supplied [CoinGecko Fren Pet page](https://www.coingecko.com/en/coins/frenpet) still displayed the name **Fren Pet / FP** when retrieved on the research date:

| Metric | Displayed value |
|---|---:|
| Price | $7.55 |
| 24-hour range | $6.96–$7.95 |
| Market capitalization | $53.585 million |
| Fully diluted valuation | $53.585 million |
| 24-hour trading volume | $57,712.81 |
| Circulating / total supply | 7.098 million FP |
| Maximum supply | 10 million FP |

These are **vendor-displayed facts**, not independently reconstructed onchain figures. The retrieved page had inconsistent percentage-change displays, so no daily return is asserted. CoinGecko also displayed a high buy/sell-tax warning; its applicability to the current IMD trading route was not verified. Its legacy name and market coverage should not be assumed to describe every IMD pool. [CoinGecko](https://www.coingecko.com/en/coins/frenpet).

For perspective, a separately retrieved DefiLlama investor page displayed $7.75, $55.04 million capitalization, and $350,114 daily volume. These disagree with CoinGecko and lack a synchronized observation time; they are **not averaged or treated as interchangeable**. Pool coverage, timing, and legacy naming remain possible explanations, not established causes. [DefiLlama FP page](https://investors.defillama.com/token/FP).

## Who bought, and what was added to a project?

| Lead | Attributable evidence | What remains unproven |
|---|---|---|
| Ansem, @blknoiz06 | Mirrored August 2 post acknowledges buying IMD and plans to keep buying; expresses confidence in Adam's development approach. | Amount, execution dates, wallet ownership, and any integration into Ansem's project. August is not a new September purchase. [Mirror](https://zamantika.com/th/blknoiz06/status/2084000824796344387). |
| Bitman, @BitmanTW | Quoted post in the same discussion says he bought IMD and Identity MD NFTs. | Purchase size and independent transaction confirmation; no project addition established. [Discussion mirror](https://zamantika.com/remp0x/status/2084005051425603723). |
| Unnamed wallet discussed by Jeff, @cfm_sol | Indexed profile mirror reports approximately $100,700 spent on 72,750 IMD. | No verified buyer identity or transaction hashes were established. The mirror's relative timestamp cannot securely date execution. It cannot be connected to Ansem or a project integration. [Profile mirror](https://instalker.org/cfm_sol). |

A distinct project, **IMD6900**, describes using trading fees to purchase Identity.md NFTs and IMD for burning. Its page lists NFT #1533 purchased for 1.870 ETH and #806 for 1.950 ETH; both seats were displayed as unpaired. This is a **project-published account of a strategy**, not evidence that a named individual bought a large FP position. NFT purchases, token purchases, and running a worker are different events. No transaction-level audit of this strategy was performed. [IMD6900 project page](https://www.imdstr.fun/).

**Inference:** the question may combine a public trader's accumulation with IMD's evolution or a separate ecosystem strategy. None of those possibilities identifies the requested event conclusively. A buyer announcement naming the project, a wallet attribution, and purchase transaction hashes would be needed to resolve it. Searches finding no such evidence do not prove the event never occurred.

## How FP relates to IMD

The **official IMD token page** publishes this history:

- August 2023: Fren Pet launches on Base as FP.
- October 2025: FP is bridged to Ethereum with a renameable representation.
- May 2026: the history records the FP → VIBE → IMD renaming sequence.
- September 2026: it reports migration to Uniswap v4/POOL4 and a Robinhood Chain bridge, describing one supply across three chains.

The page identifies Ethereum IMD as `0xD34a99Bc0f67aE1bbd63C660e6d0b0dd03E263B7`. Thus the supported relationship is **token continuity across branding and bridges**, rather than merely two unrelated tokens partnering. These are first-party historical claims; bridge reserves and supply conservation were not independently audited. [Official token page](https://imd.fun/token/).

CoinGecko's linked Base token is `0xff0c532fdb8cd566ae169c1cb157ff2bdc83e105`; indexed BaseScan material identifies the contract as FrenPetToken. Different chains have different addresses: the Ethereum address should not be substituted into Base. [CoinGecko](https://www.coingecko.com/en/coins/frenpet); [BaseScan token record](https://basescan.org/token/0xff0c532fdb8cd566ae169c1cb157ff2bdc83e105?a=0x0b125837a6987556aa01a8ea7d8b200cf67b0a9f).

Historically, the game documentation describes paid actions buying FP for burning or player treasure, including burning FP used for mushrooms. [Fren Pet documentation](https://fren-pet-docs.vercel.app/fp).

The linked **POOL4 documentation** describes IMD as its first hook-enabled token. Sells can push pool inventory above a cap; excess inventory is removed, mostly burned, with the remainder supporting stakers, orchestration, and inference nodes. ETH recovered funds bids below the market. This is a description of the project's mechanism, not proof of sustainable returns or an external purchase. The same documentation says a permissionless launch factory is still a plan, so older social descriptions of launchpad capabilities should not automatically be read as current production functionality. [POOL4 docs](https://pool4.imd.fun/docs).

## Twitter/X sentiment: bullish visible sample, low representativeness

Method: manual review of publicly indexed X post mirrors, with duplicate quoted posts counted once. Searches included Frenpet/Fren Pet plus bought, purchased, whale, integration, and IMD plus Ansem, FOMO, criticism, and scam. The five observations below form the qualitative sample; this was not an authenticated X search, API collection, or random sample. No sentiment percentage is warranted.

| Account | Observed viewpoint, paraphrased | Date/access limitation |
|---|---|---|
| @blknoiz06 | Bullish: accumulating and endorsing the developer's patient approach. | August 2 display; original X inaccessible. [Mirror](https://zamantika.com/th/blknoiz06/status/2084000824796344387). |
| @remp0x | Bullish: emphasizes developer reputation and a potential opportunity before wider discovery. | August 2 display; same conversational cluster as Ansem. [Mirror](https://zamantika.com/remp0x/status/2084005051425603723). |
| @BitmanTW | Bullish: discloses buying tokens/NFTs and anticipates launchpad development. | Quoted post; its own exact date was not established. [Mirror](https://zamantika.com/remp0x/status/2084005051425603723). |
| @cfm_sol | Bullish interpretation: attributes the rally to a stronger connection between product and token economics. | Profile was indexed within days of research, but its relative post times are not reliable absolute dates. [Mirror](https://instalker.org/cfm_sol). |
| @beachlesslee | Bullish holder sentiment: describes confidence in holding/staking IMD. | Relative timestamp only; index indicated roughly two-week-old crawl. [Mirror](https://mobile.twstalker.com/beachlesslee). |

**Assessment/inference:** enthusiasm in this accessible sample centers on Adam's reputation, AI applications, staking, and burns. Several speakers disclose holdings, which creates a financial incentive to promote the asset. Three observations belong to one discussion and are not independent evidence of broad adoption. Search indexing and mirror availability favor visible promotional posts; accounts, deletion status, and engagement totals were not authenticated.

Targeted negative searches did not yield a securely attributable, relevant bearish post about the alleged integration. Unrelated accusations elsewhere on a profile were excluded. This means **negative sentiment is insufficiently measured**, not absent. Market price gains do not substitute for a sentiment survey or prove that a particular buyer caused them.

## Confidence and unresolved questions

- **High confidence in source attribution:** the official page explicitly publishes the FP/IMD lineage; CoinGecko displays the quoted snapshot. This confidence applies to what the pages say, not a complete technical audit.
- **Moderate confidence in the reported social narrative:** multiple accessible mirrors describe bullish views, but original X content was not retrieved.
- **Low confidence / unresolved:** the identity of a recent large buyer who also integrated the token into a named project; purchase size and transaction timing; representative current X sentiment.

To close the central evidence gap, obtain the originating announcement and transaction hashes, confirm that the wallet belongs to the named buyer, identify the destination project's actual implementation, and then collect dated X responses to that specific announcement. None of those missing steps is represented here as completed.

## Research and validation limits

All linked sources were queried on 30 September 2026; search-index crawl dates and relative timestamps are distinguished from event dates. Original X opens returned errors, while some mirror evidence was available only in indexed excerpts. The report uses those excerpts explicitly as secondary evidence. No private data, wallet connection, token trade, package installation, or contract execution was used.

Local checks verify UTF-8 output, required sections, link syntax, and file presence only. They do not independently certify source truth, current balances, contracts, or research conclusions.
