# Quarry tokenomics: a buy-and-hold treasury with optional rock fractions

**Research date:** 11 October 2026  
**Question:** How should Quarry use an ERC-20 and trading activity to acquire EtherRocks, keep the originals in a treasury, and potentially make smaller collectible pieces available?

## Recommendation

Build Quarry in two layers, and make the relationship between them explicit:

1. **$QUARRY is the market/activity token.** Trading fees from one or more named, supported pools fund a publicly visible ETH acquisition balance. When the balance can buy an acceptable listed EtherRock, a permissionless caller can execute the purchase and receive a disclosed execution reward. The ERC-20 itself should not promise holders a pro-rata claim on the rocks, ETH revenue, or redemption unless that is actually the product and has been legally reviewed.
2. **The EtherRock remains a separately accounted treasury asset.** Each acquisition should be reported by token ID, transaction, purchase cost and current custodian. State whether a Rock may leave only through redemption of all its fractions, or can never leave. Those are different designs.
3. **Test pieces separately, after the first buy-and-hold loop works.** If smaller pieces are the goal, first pilot one Rock with 100 fungible ERC-1155 “stone” units tied to that exact Rock. Let users trade those units. Only add the 100:1 pebble subdivision if the pilot shows that buyers need finer granularity. If the full original can be redeemed, require the complete set of that Rock’s fractions to be burned before transferring it out.

This keeps the initial tokenomics legible and leaves room for “chips” later without promising that future products will be issued. It also resolves the main incompatibility in the proposal: *a Rock that is never allowed to leave the vault cannot at the same time be redeemable by fraction holders.* A full-set redemption can be a narrowly defined exception to “we do not sell the Rock”; it is still a transfer out of the treasury and needs to be described as such.

## Evidence and design implications

### What the reference projects and token standards establish

- EtherRock’s own site describes the project as launched in 2017, says only 100 Rocks can ever be available, and says the Ethereum contract tracks purchases, sales and owners. This establishes the scarce, serial collection premise, not that every Rock is currently available for purchase or that a particular market listing is fairly priced. [EtherRock project site](https://etherrock.com/)
- The relevant PunkStrategy precedent is the **TokenStrategy** project documented by its operator. Its $PNKSTR trades routed through a Uniswap v4 hook incur a stated 10% fee: 8% buys CryptoPunks, 1% goes to FundingWorks NFT holders, and 1% to the TokenWorks team. Its documentation also explicitly says trades are not forced through the hook. This is a useful mechanism precedent, but it is not evidence that high fees reliably create volume, that all exchange activity is charged, or that its economics are durable. [PunkStrategy documentation](https://docs.tokenstrategy.com/punkstrategy-the-ecosystem-token)
- That project’s live strategy page describes accumulation only after the machine has enough ETH and says the first entity to trigger the process earns a reward. That supports using an explicit threshold and caller incentive instead of implying that purchases happen autonomously whenever a listing appears. [TokenStrategy PunkStrategy page](https://www.tokenstrategy.com/strategies/0xc50673edb3a7b94e8cad8a7d4e0cd68864e33edf)
- ERC-20 defines the interchangeable transfer/approval interface used by wallets and exchanges; it does not give holders rights to a treasury asset by itself. ERC-721 tracks distinct NFTs individually. ERC-1155 can represent multiple token types and quantities within one contract, including fungible and non-fungible types, and supports batch transfers. Those standards provide useful implementation building blocks; they do not define Quarry’s legal ownership, redemption promise or secondary-market liquidity. [ERC-20](https://eips.ethereum.org/EIPS/eip-20), [ERC-721](https://eips.ethereum.org/EIPS/eip-721), [ERC-1155](https://eips.ethereum.org/EIPS/eip-1155)
- A Uniswap v2 pool has to be seeded with both tokens; its pool documentation says the first provider sets the starting price, and fees accrue pro rata to liquidity providers. Therefore, a token having a fee-funded treasury does not itself create depth for trading. Liquidity needs its own plan and counterparties. [Uniswap v2 pool mechanics](https://developers.uniswap.org/docs/protocols/v2/concepts/pools)

### Suggested mechanics

**Trading and acquisition loop.** Start with a plain, conventional ERC-20 and a disclosed initial supply/allocation plan. Define a fee schedule only for supported trading venues. Avoid implying that an ERC-20 standard fee applies to every transfer: the PunkStrategy reference itself warns that swaps can avoid its v4 hook. For each supported pool, publish the actual fee, fee recipient, fee asset, conversion rule, any allocations other than acquisition, and the contract or account holding the proceeds. If fees accumulate in $QUARRY, selling that inventory for ETH adds sell pressure; if fees arrive as ETH or a stablecoin, conversion and purchase-power accounting differ. Choose and disclose one path rather than leaving this implicit.

Use a threshold-based buying rule: retain enough for gas, set a maximum price/slippage rule and approved marketplace path, buy only against a verifiable listing, and expose the accumulated balance and trigger status on-chain. A keeper or any caller may advance a purchase, with a fixed or formulaic bounty stated in advance. Do not represent an off-chain marketplace monitor as on-chain automation. Make unused fees and failed purchase attempts observable. Do not set a fee percentage from the PunkStrategy example alone; test candidate rates against pool depth, swap cost, expected acquisition frequency and ordinary-user willingness to trade.

**Token purpose.** Use $QUARRY to participate in the Quarry market, vote on narrowly scoped acquisition preferences if desired, or access platform functions that actually exist. A vote may rank which listings the buyer should inspect or cap spending, while execution stays within published rules. Avoid letting a token vote quietly change custody or redemption promises. Describe the ERC-20 as having no direct pro-rata title to treasury Rocks unless the project intends that claim and has counsel assess it.

**Small pieces.** A Rock → 100 stones → 100 pebbles per stone design means **10,000 pebble units per Rock** (arithmetic from the proposal). Treat each original Rock as its own token ID: one Rock’s shares should not be interchangeable with another’s, since serial items may differ. ERC-1155 is a reasonable fit for per-Rock balances and batched transfers; it does not guarantee that NFT marketplaces will display or support the items well. “Easy to sell” is a hypothesis to test, not a property conferred by fractionalization.

For a first release, choose one of these coherent models:

| Model | What a holder owns | Can the original leave? | Main consequence |
|---|---|---|---|
| **Permanent display pieces** | A collectible with no ownership or redemption claim on the Rock | No | Best matches permanent treasury custody, but pieces do not provide fractional economic ownership of the EtherRock. Describe the distinction plainly. |
| **Redeemable fractions** | A contract-defined fractional claim represented by units backed by one escrowed Rock | Yes, after all units for that Rock are assembled and burned | A full-set holder can reclaim the original; the treasury is permanent only until redemption. Needs explicit custody, redemption, default and legal terms. |
| **100 stones, then optional pebbles** | Begin with 100 units per Rock; add a 100:1 conversion to 10,000 pebble units only after observing demand | Depends on the chosen redemption rule | Lower initial product complexity; subdivision adds token, UX, marketplace and accounting work. |

An ERC-721 “stone” collection makes each stone individually unique, even if all stones of a particular Rock are intended to be interchangeable. For interchangeable shares, use fungible balances (ERC-1155 amounts, or a separate ERC-20 per Rock) and reserve ERC-721 for the original or genuinely distinct artifacts. If you want one stone itself to be a collectible NFT, explain what makes stone #1 distinct from stone #2 beyond its fraction percentage.

**Market liquidity.** Fractional units can lower the ticket size and may make a listing easier to place, but do not manufacture buyers. Plan who seeds a market, in what assets, and whether the project treasury or a market maker can withdraw that liquidity. Uniswap’s docs explain that liquidity providers must supply paired assets and can retrieve their proportional liquidity and fees; they do not promise that a pool will remain deep. Report trading depth and realized sales alongside nominal volume. Do not use transfer-tax rebates or emissions to make wash trading appear to be demand.

**Supply, emissions and fees.** Favor a fixed initial $QUARRY supply, with no discretionary minting, or publish a tightly specified mint authority and cap before launch. Do not promise that rising trading volume mechanically raises the Rock count at a predictable rate: purchase availability, prices, fees, liquidity and slippage all intervene. Report at least (a) genuine acquisition-fee receipts, (b) conversion and execution costs, (c) number and cost of Rocks acquired, (d) reserve balance, and (e) supported-pool liquidity and depth. Gross volume alone is a poor success metric.

**Do not launch SILLICON or Chips as a speculative second token yet.** First establish whether $QUARRY has sustained trading that is not mostly incentive-seeking, whether people want to trade pieces, and what function a later asset would serve. If pebbles can be ground into SILLICON, define a real, scarce use for burning them; a second token without demand or utility only adds another market and another set of promises.

## Risks and limits

- **Volume is not assured by tokenomics.** A fee creates an expense for routed trades and a funding source when trades occur. It does not force trades to occur. A high fee may reduce the incentive to trade or push traders to other routes. This is a design inference; neither the cited project’s self-description nor token standards prove what Quarry’s market response will be.
- **Treasury accumulation concentrates custody risk.** Buyers rely on the vault and its administrators or immutable code to preserve the Rock. State key/control arrangements, emergency powers, upgradeability, and whether the community can authorize a sale. Publish verifiable holdings and avoid treating an explorer balance alone as proof of beneficial ownership.
- **Fractional backing and redemption add legal and operational obligations.** In the EU, MiCA’s recitals say fractional parts of a unique, non-fungible crypto-asset should not themselves be considered unique and non-fungible; a large series is also an indicator of fungibility. In the U.S., the SEC’s April 2026 educational guidance says a fractionalized digital collectible may be a security, and separately explains that promises of managerial efforts plus the other Howey elements can bring crypto-asset offers within securities laws. These are jurisdiction- and fact-specific points, not a classification of Quarry. Get jurisdiction-specific advice before sale/marketing, especially if a fraction is pitched as ownership, investment, profit or redemption. [MiCA, recital 11](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32023R1114), [SEC, Crypto Assets and the Federal Securities Laws](https://www.sec.gov/resources-small-businesses/capital-raising-building-blocks/crypto-assets-federal-securities-laws), [SEC, Transactions Involving Crypto Assets](https://www.sec.gov/resources-small-businesses/capital-raising-building-blocks/transactions-involving-crypto-assets)
- **Token/NFT ownership is not automatically intellectual-property ownership.** This report has not reviewed EtherRock’s complete terms, art rights, or whether Quarry-branded “stones” or “pebbles” can use the original imagery. Get rights advice and publish clear terms before minting derivative pieces.
- **This is a tokenomics design brief, not a market valuation or audited contract specification.** It does not establish current floor price, Rock availability, venue liquidity, token demand, tax treatment, or whether the precedent can be copied safely. Current prices and holder data were not used because they would change quickly and are not needed to make the structural recommendation.

## Facts, inferences and unanswered questions

**Sourced facts:** EtherRock’s website states 100 total; TokenStrategy’s documentation describes the specified 10% routed-trade split and explicitly says routing through the hook is not mandatory; ERC-20, ERC-721 and ERC-1155 specify token interfaces; Uniswap’s docs describe seeding and liquidity-provider fee mechanics; the cited EU and SEC materials describe regulatory factors relevant to fractions and promotional promises.

**Inferences/recommendations:** Separate the trade token from the Rock custody/fraction layer; charge only on clearly named supported routes; keep a thresholded, observable acquisition process; pilot one Rock and 100 units before adding pebbles; evaluate liquidity through depth and real fills, not volume alone. These follow from the cited mechanics but have not been validated by Quarry user research or simulations.

**Unanswered product decisions:**

1. Is the collection intended to be held forever, or may a full set of fractions redeem and remove a Rock?
2. Do $QUARRY holders receive only activity/governance utility, or any asset, income, vote or redemption rights?
3. What chain, trading venue(s), initial supply/distribution, fee asset, acquisition split, operating budget and liquidity-seeding source will Quarry use?
4. Are stones/pebbles collectible wrappers, fractional ownership claims, or purely in-game units? What legal entity or persons will custody and administer the original Rocks?
5. In which countries will the token and any fractions be offered or promoted, and who will make those offers?
6. What measurable evidence would justify the second subdivision and possible SILLICON/Chips product?

Resolve questions 1–4 before contract design; get legal advice on 4–5 before offering fractions. The core $QUARRY/treasury experiment can be specified and tested without prematurely deciding the future SILLICON or Chips concept.
