# The Crypto Market on 30 September 2026

**Question:** What state is the crypto market in right now, and what is driving it?

**Snapshot time:** 2026-09-30, about 09:40–09:47 UTC. Prices move all the time. Every number below is a point-in-time reading and may already be out of date when you read it.

**Evidence labels used throughout**

| Label | Meaning |
|---|---|
| **[F-API]** | A fact read directly from a public data API during this session. The raw response is saved in `artifacts/data/`. |
| **[F-PRIMARY]** | A fact confirmed on the issuing body's own page (for example, the Federal Reserve). |
| **[F-SECONDARY]** | A fact reported by a news outlet. I read the article but could not check it against the original data source. |
| **[SNIPPET]** | Seen only in a search-result summary. I could not open the page (HTTP 403 or timeout), so treat it as weak evidence. |
| **[INFERENCE]** | My own reading of the evidence. It is not a sourced fact. |

---

## 1. Summary

- **Where the market stands** **[F-API]**: The total crypto market is worth about **$2.88 trillion**, with $91 billion traded in the last 24 hours. Bitcoin is at **about $83,500**. That is **−27% over one year** and **−34% below its all-time high** of $126,080, set on 2025-10-06. It is also **about +43% above its 12-month low** of roughly $58,600 (daily close, 2026-07-01). Ethereum is at about $2,687, down 36% over one year and 46% below its high.
- **Recent direction** **[F-API]**: Over the last 30 days most large coins rose: BTC +6%, ETH +9%, SOL +15%, XRP +9%. Over the last 7 days they fell back: BTC −3.6%, XRP −7%. Bitcoin peaked near $86,600 (daily close) on 2026-09-22 and has pulled back from there.
- **What is driving it** (sourced facts; which ones matter most is my judgement):
  1. **Money has returned to US spot Bitcoin ETFs.** Year-to-date net flows went from about −$5.7 billion on July 13 to about +$0.9 billion by September 24. The largest single day of 2026 was +$999 million on September 21 **[F-SECONDARY]**.
  2. **The Fed raised interest rates.** On 2026-09-16 it lifted its target range to 3.75–4.00%, its first increase since 2023 **[F-PRIMARY]**. Higher rates are usually a headwind for speculative assets.
  3. **A major US crypto bill stalled.** The CLARITY Act, which would set rules for crypto markets, failed a procedural vote in the Senate on 2026-09-15 (49–50; it needed 60) **[F-SECONDARY, NPR]**.
  4. **A major exchange was hacked.** About $387.5 million was stolen from the exchange Bitget on 2026-09-24. Bitget says its user protection fund covers the loss **[F-SECONDARY]**.
- **Overall reading** **[INFERENCE]**: The market is **recovering inside a larger downtrend**. The rebound since July is real and has been backed by ETF buying. However, prices are still far below last year's highs, the value locked in DeFi apps is down about 39% from a year ago, and both interest rates and US regulation are working against the market right now.

---

## 2. Market data (facts)

### 2.1 Whole market — CoinGecko `/global` [F-API]

| Metric | Value |
|---|---|
| Total market cap | $2,884 billion |
| 24h trading volume | $91.4 billion |
| 24h change in market cap | −2.15% |
| Bitcoin's share of total value | 58.3% |
| Ethereum's share | 11.4% |
| USDT + USDC share (the two largest stablecoins) | 8.95% (6.37% + 2.58%) |

Source: <https://api.coingecko.com/api/v3/global> (saved as `artifacts/data/global.json`)

### 2.2 Largest assets — CoinGecko `/coins/markets` [F-API]

The 7d, 30d and 1y columns are percentage price changes. "vs ATH" means how far the price is below its all-time high.

| # | Asset | Price (USD) | Mkt cap ($bn) | 7d | 30d | 1y | vs ATH | ATH date |
|---|---|---|---|---|---|---|---|---|
| 1 | BTC | 83,520 | 1,678 | −3.6% | +6.2% | −27.0% | −33.8% | 2025-10-06 |
| 2 | ETH | 2,688 | 328 | −2.6% | +9.4% | −36.2% | −45.7% | 2025-08-24 |
| 3 | USDT | 1.00 | 184 | 0.0% | 0.0% | −0.1% | — | — |
| 4 | BNB | 765 | 102 | −3.6% | +10.7% | −25.5% | −44.2% | 2025-10-13 |
| 5 | XRP | 1.51 | 95 | −7.3% | +9.2% | −47.9% | −58.6% | 2025-07-17 |
| 6 | USDC | 1.00 | 74 | 0.0% | 0.0% | 0.0% | — | — |
| 7 | SOL | 119.21 | 70 | +0.3% | +14.9% | −43.4% | −59.4% | 2025-01-19 |
| 8 | TRX | 0.338 | 32 | −1.7% | +0.4% | +0.5% | −21.6% | 2024-12-03 |
| 10 | ZEC | 1,407.55 | 24 | −13.7% | +70.1% | +1,975% | −55.9% | 2016-10-28 |
| 11 | HYPE | 86.45 | 19 | −10.5% | +6.4% | +92.1% | −11.8% | 2026-09-23 |
| 12 | DOGE | 0.0943 | 15 | −7.2% | +13.2% | −59.6% | −87.1% | 2021-05-07 |
| 13 | LINK | 14.39 | 11 | +10.6% | +26.9% | −33.3% | −72.7% | 2021-05-09 |
| 14 | XMR | 541.11 | 10 | −4.6% | +3.6% | +83.8% | −32.2% | 2026-01-14 |
| 17 | ADA | 0.248 | 9 | −4.3% | +25.1% | −69.1% | −92.0% | 2021-09-01 |

Source: <https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=20&price_change_percentage=7d,30d,1y> (saved as `artifacts/data/top.json`).

Rank #9 is "FIGR_HELOC", a tokenised home-equity loan product. It is left out of the table because it is not a traded crypto-native asset, but it is in the raw file.

### 2.3 Bitcoin over the past 12 months — CoinGecko daily closes [F-API]

| Date (~30-day steps) | BTC close (USD) |
|---|---|
| 2025-10-01 | 114,088 |
| 2025-11-30 | 90,832 |
| 2026-01-29 | 89,212 |
| 2026-02-28 | 65,891 |
| 2026-04-29 | 76,332 |
| 2026-06-28 | 59,953 |
| 2026-07-28 | 63,701 |
| 2026-08-27 | 79,018 |
| 2026-09-26 | 84,076 |

- Lowest close in the last 12 months: **$58,566 on 2026-07-01**. Highest: **$124,740 on 2025-10-07**.
- Highest close in the last 90 days: **$86,597 on 2026-09-22**.
- Source: `artifacts/data/btc365.json`

### 2.4 Stablecoins, DeFi and derivatives [F-API]

| Metric | Now | Comparison | Source |
|---|---|---|---|
| Total USD stablecoin supply | $311.2 billion | $307.3 billion a month ago; $296.1 billion a year ago (+5.1% YoY) | DefiLlama <https://stablecoins.llama.fi/stablecoincharts/all> |
| DeFi total value locked (TVL) | $94.5 billion | $85.6 billion a month ago (+10.4%); $156.0 billion a year ago (−39.4%) | DefiLlama <https://api.llama.fi/v2/historicalChainTvl> |
| Binance BTCUSDT perpetual funding rate (last period) | −0.0007% | Close to zero | Binance <https://fapi.binance.com/fapi/v1/premiumIndex?symbol=BTCUSDT> |
| Binance BTCUSDT open interest (USD) | $7.73 billion | $8.48 billion 30 days ago (−8.8%) | Binance `openInterestHist` |
| Deribit BTC historical volatility (latest value) | 35.4 | The lookback window is not stated in the response | Deribit `get_historical_volatility` |

A note on these terms:
- **TVL** is the value of crypto deposited in DeFi apps. It is priced in USD, so it falls when token prices fall even if nobody withdraws.
- **Funding rate** is the periodic payment between long and short traders on perpetual futures. Near zero means neither side is paying much to hold its position.
- **Open interest** is the total value of futures positions still open.

### 2.5 Sentiment — Alternative.me Crypto Fear & Greed Index [F-API]

- **Today: 71 ("Greed").** The last 7 readings were between 70 and 74. The 30-day range was 50 to 78, with the low (50) on 2026-09-17, the day after the Fed rate hike, and the high (78) on about 2026-09-22.
- Source: <https://api.alternative.me/fng/?limit=31>

---

## 3. What is driving the market (facts, with sources)

### 3.1 ETF flows

These figures come from secondary reporting of Farside Investors data. I could not open Farside directly (HTTP 403).

- US spot Bitcoin ETFs were about **−$5.69 billion** year-to-date at their low on **2026-07-13**. By 2026-09-23/24 they had recovered to **+$886.8 million** year-to-date: $6.58 billion of net inflow since mid-July. **[F-SECONDARY]** CoinMarketCap Academy, citing Farside: <https://coinmarketcap.com/academy/article/bitcoin-etf-inflows-turn-positive-2026>
- There were **$2.84 billion** of inflows over the six sessions from Sept 17 to Sept 24. The largest day was **$999 million on Sept 21**, the biggest single day of 2026. **[F-SECONDARY]** same source.
- For comparison, the full-year 2025 inflow was $21.35 billion, so 2026 is far behind. **[F-SECONDARY]** same source.
- Reported without an original data source:
  - Weekly inflows of $2.39 billion through Sept 25. **[SNIPPET]** The Coin Republic: <https://www.thecoinrepublic.com/2026/09/27/bitcoin-etf-inflows-hit-2026-record-as-btc-price-holds-above-84k/>
  - More than $66 million of inflows on Sept 29, a ninth day in a row. **[SNIPPET]** Invezz: <https://invezz.com/news/2026/09/30/bitcoin-holds-firm-as-etf-inflows-continue-analysts-assess-rallys-strength/>

### 3.2 Interest rates

- On 2026-09-16 the FOMC (the Fed's rate-setting committee) voted **12–0 to raise** the federal funds target range by a quarter point to **3¾–4%**. The statement says "Inflation remains elevated" and "uncertainty remains elevated." **[F-PRIMARY]** <https://www.federalreserve.gov/newsevents/pressreleases/monetary20260916a.htm>
- This is the first increase since 2023. The median Fed official expects rates to end 2026 at about 4.1%, which implies one more hike this year. **[SNIPPET]** CNBC: <https://www.cnbc.com/2026/09/16/fed-rate-decision-september-2026.html>. I tried to read the Fed's own projections PDF but could not parse it: <https://www.federalreserve.gov/monetarypolicy/files/fomcprojtabl20260916.pdf>

### 3.3 US regulation

- **CLARITY Act (crypto market structure bill).** On 2026-09-15 the Senate voted on whether to move the bill forward. It needed 60 votes and got **49 yes to 50 no**. All Democrats voted no, joined by four Republicans (Collins, Hawley, Moran and Tillis). Tillis filed a motion so the bill can be brought back for another vote. For many Democrats, the main sticking point is an ethics clause meant to stop officials from profiting from crypto while in office. **[F-SECONDARY]** NPR (article text checked): <https://www.npr.org/2026/09/15/nx-s1-5968711/clarity-act-crypto-senate-vote>
- **GENIUS Act (stablecoin law).** On 2026-09-24 the Federal Reserve Board asked for public comment on two proposals under the Act:
  - Reserve and capital rules: stablecoins must be fully backed by permissible reserve assets such as short-term Treasury bills.
  - An application process for Fed-supervised banks that want to issue stablecoins.
  - **[F-PRIMARY]** <https://www.federalreserve.gov/newsevents/pressreleases/bcreg20260924a.htm>. There is a 60-day comment period **[F-SECONDARY]** (CoinDesk / The Block).

### 3.4 Security

- **Bitget hack** **[F-SECONDARY]**, Decrypt, 2026-09-25: <https://decrypt.co/379350/bitget-hack-387m-what-happened-why-north-korea-suspect>
  - About **$387.5 million** was stolen on 2026-09-24. Roughly $157 million of it was XRP.
  - According to the CEO, the attackers broke into a backend part of the exchange's wallet system and faked transaction data, so Bitget's own approval process signed off on the transfers. She says they did not steal private keys or forge customer withdrawal requests.
  - North Korean hackers are suspected, but the CEO says the attacker has **not been confirmed**.
  - Bitget says its user protection fund, reported at more than $464 million, covers all losses.
  - Other outlets call it the biggest hack of 2026 so far, for example Fortune: <https://fortune.com/2026/09/25/north-korea-bitget-387-million-crypto-attack/>

---

## 4. My interpretation (inferences, not facts)

1. **This is a recovery inside a bear market, not a new bull market.** [INFERENCE]
   - Bitcoin, ETH, SOL and XRP are all 34–59% below their highs and down 27–48% over one year.
   - Bitcoin's +43% from the July low is a meaningful rally. Even so, it has only regained about half of the drop from the October 2025 high.
2. **The rally seems to be driven mainly by ETF buying rather than borrowed money.** [INFERENCE]
   - ETF inflows are strong. Meanwhile Binance BTC open interest fell 8.8% over 30 days and funding is near zero.
   - Together, that suggests the rise is not being powered by a build-up of leveraged long positions.
   - Weakness: this uses only one exchange's derivatives data.
3. **Sentiment is ahead of fundamentals.** [INFERENCE]
   - A Fear & Greed reading of 71 ("Greed") sits oddly next to prices that are down 27% on the year.
   - The index appears to track recent momentum. After a strong 30 days, that makes it less useful as a longer-term signal.
4. **Crypto is behaving like a risk asset, and macro conditions are against it.** [INFERENCE]
   - The Fed has turned to raising rates, and markets reportedly expect more hikes. That normally hurts assets like crypto.
   - The September rally happened despite that. One secondary source links ETF inflows to a Treasury decision to increase bond buybacks, but I did not verify that claim.
5. **Stablecoins keep growing while DeFi shrinks.** [INFERENCE]
   - Stablecoin supply is up 5% on the year, while DeFi TVL is down 39%.
   - This suggests money is parked in dollar tokens rather than invested in DeFi. Part of the TVL drop is simply lower token prices.
6. **Returns are very uneven across coins.** [INFERENCE]
   - A few tokens have done very well over the year: ZEC (+1,975%), HYPE (+92%) and XMR (+84%).
   - Most large coins are down. The strongest performers are privacy coins and an exchange token, not the broad market.

## 5. Uncertainty and limits

- **Single data providers.** Each figure comes from one provider: CoinGecko, DefiLlama, Binance, Deribit or Alternative.me. I did not cross-check them against other providers, and different providers can differ by a few percent.
- **An unexplained mismatch in the 24h numbers.** CoinGecko shows total market cap down 2.15% in 24h, while BTC and ETH each moved less than 1%. It may come from long-tail assets or from how the index is built. I did not investigate it.
- **ETF flow figures are second-hand.** They come through secondary reporting, because Farside and SoSoValue blocked automated access. The daily numbers may be revised.
- **Some items are weak evidence.** Anything marked [SNIPPET] comes from a search-result summary and not a page I could open. These are the CNBC rate-path details, the Sept 25 weekly total and the Sept 29 flow figure.
- **Derivatives coverage is thin.** It covers only Binance BTCUSDT and one Deribit volatility value. There is no aggregated open interest, options skew or liquidation data.
- **No forecast.** This report describes the market as it is now. It does not predict prices and is not investment advice.

## 6. Questions this report does not answer

1. Why did BTC drop from about $90k (January) to about $58.6k (July)? I did not research what drove the first half of 2026.
2. What were the 2026 flows into Ethereum and other non-Bitcoin ETFs?
3. Did the Bitget hack have any lasting effect on prices or exchange balances? About $157 million of XRP was stolen, and XRP was the weakest large coin over the week (−7.3%). I did not test whether the two are linked.
4. Is the reported Treasury buyback link to ETF inflows real? It comes from a Bloomberg Intelligence quote passed on through CoinMarketCap.
5. Why are ZEC and XMR doing so well: adoption, exchange listings, or short-term speculation?
6. Will the CLARITY Act get another vote before the end of 2026? Secondary sources say it is unlikely before 2027. I did not verify that.
7. How big are on-chain flows, such as exchange reserves, miner selling and long-term holder behaviour? Nothing here measures them.

## 7. Method

- **Market data:** Pulled with `curl` from public APIs on 2026-09-30 between 09:43 and 09:47 UTC. The raw JSON is saved in `artifacts/data/`.
- **News and policy:** Found with web search. I then opened the Federal Reserve pages, the NPR article, Decrypt and CoinMarketCap Academy and read the claims in them.
- **Pages I could not open:** Farside, Caleb & Brown and the CNBC article (HTTP 403), and the Fed projections PDF (could not be parsed). Claims that depend on them are labelled.
