# IMD Hackathon: combined top 5 from four judges' ballots

Researched 2026-10-28. Inputs: the four top-5 ballots in the request (lesnar, taylor, 0xminion, Damien).
Project descriptions come from public GitHub repositories and project websites, linked inline.

Labels used below:
**[Fact]** means read directly from the ballots or a linked source. **[Inference]** means my interpretation.
**[Uncertain]** means the evidence is thin or conflicting. **[Open]** means I could not answer it.

## 1. Final ranking

| Place | Entry | Ballots naming it | Weighted points | Ranks given |
|---|---|---|---|---|
| **1** | **imdUSD** (@imdusd) | 4 of 4 | 19 | lesnar #1, taylor #2, 0xminion #1, Damien #1 |
| **2** | **Intelligent Dance Market / $IDM** (@theidmfun) | 3 | 9 | lesnar #5, 0xminion #2, Damien #2 |
| **3** | **ROBOBET, now Paper Clash** (@robobet_fun → @paperclash_xyz) | 3 | 9 | lesnar #2, 0xminion #3, Damien #4 |
| **4** | **imdRadar** (@imdradar) | 2 | 6 | lesnar #3, Damien #3 |
| **5** | **imdLend** by @sudeepb02 | 2 | 6 | taylor #1, Damien #5 |
| *6th, just outside* | NightShiftImd (@nightshiftimd) | 2 | 4 | lesnar #4, taylor #4 |

The other entries got one vote each: seeronimd (3 pts), ConditionalsImd (2), moneycanbuy_fun (1), Imdirectorb (1).

### Method
1. **Votes first.** I sorted entries by how many judges put them in their top 5, as the request asked.
2. **Rank weighting second.** Within each vote count I ranked by Borda points: rank 1 = 5 pts, 2 = 4, 3 = 3, 4 = 2, 5 = 1.
3. **Remaining ties go to head-to-head.** I counted how many judges who ranked both entries put one above the other.

`scripts/score.py` in the repository reproduces the table.

**[Fact] Two ties had to be broken:**
- **#2 IDM vs #3 Paper Clash** (both 3 votes, 9 pts). On head-to-head, IDM wins 2–1: 0xminion and Damien put IDM above Paper Clash, and lesnar did the opposite. IDM also has the better median rank (#2 against #3).
- **#4 imdRadar vs #5 imdLend** (both 2 votes, 6 pts). Damien is the only judge who ranked both, and put imdRadar above (#3 against #5). imdRadar's two votes are also equal mid-table votes. imdLend's are one #1 and one #5.

**[Uncertain] The ranking depends on the method.** Another reasonable tie-break, "most first-place votes", would put **imdLend at #4 and imdRadar at #5**: imdLend has taylor's #1 vote, while imdRadar has no #1 votes. A steeper weighting such as 10/6/4/2/1 gives the same result. Places 1–3 hold under every scheme I tried. Only the 4/5 order changes.

**[Inference] Names merged.** "robobet_fun (now @paperclash_xyz)" and "@robobet_fun" count as one entry. The ballots say so, and both IMD token launches below point to the same project. "imdlend by @sudeepb02" on two ballots counts as one entry.

## 2. The five winners and how each uses IMD

### #1 imdUSD (@imdusd): stablecoin backed by IMD
- **[Fact]** imdusd.com describes it as "a dollar-denominated stablecoin backed by IMD and priced by IdentityMD swarm attestations" ([imdusd.com](https://imdusd.com/)).
- **[Fact]** It is a CDP vault on Ethereum mainnet. Users borrow imdUSD against staked IMD (sIMD). Positions below the collateral ratio are "barked" and "bitten" (liquidated), and liquidators earn a bonus in sIMD ([fa11up/imdusd-keeper](https://github.com/fa11up/imdusd-keeper)).
- **[Fact] How it uses IMD:**
  - IMD is the collateral.
  - The price oracle is the **IdentityMD agent swarm**. An `OracleAsker` spends the Treasury's IMD to buy price updates, and a `SwarmRelay` puts the swarm's attested answers on chain (imdusd-keeper README).
  - Related tools in the same author's account include:
    - a Uniswap v4 `PegFeeHook` for the imdUSD/USDC pool, which charges a surcharge on swaps that push the price away from $1 and sends it to the imdUSD Treasury ([fa11up/imdusd-peg-hook](https://github.com/fa11up/imdusd-peg-hook));
    - a companion token, INFER, with a [whitepaper](https://github.com/fa11up/infer-whitepaper);
    - an IMD launch repo, [identity-md-launches/launch-882-imdusd](https://github.com/identity-md-launches/launch-882-imdusd).
- **[Fact]** DexScreener describes it the same way: borrowed against staked IMD and priced by panels of IdentityMD agents, with protocol revenue used to buy back INFER for stakers ([DexScreener pair](https://dexscreener.com/ethereum/0x1f03dd2c202cf17b58305b73ae2f8b3143e9c056ed9c9e8dbd4924b350431e95)).
- **[Inference]** It was the only entry on all four ballots, and three judges ranked it first, so it is a clear #1.

### #2 Intelligent Dance Market, $IDM (@theidmfun)
- **[Fact]** theidm.fun describes it as "a Uniswap v4 hook whose on-chain state is a 16-step drum machine. Every trade is a note." The hook stores a 4-track, 16-step drum pattern and a bass line. Each swap in the IDM/ETH pool flips a step and changes the bass and tempo. Trade size picks the instrument (hat → kick → "whale"), buys set steps and sells clear them, and every 64 swaps the genre changes. The site says "Nothing is off-chain" ([theidm.fun](https://theidm.fun)).
- **[Fact] How it uses IMD:** the site says the pool was "launched through IMD". IMD launch repos for the token link x.com/theidmfun: [launch-2295-idm](https://github.com/identity-md-launches/launch-2295-idm) (Ethereum) and [launch-2307-idm](https://github.com/identity-md-launches/launch-2307-idm) (Robinhood Chain, "idm-16"). The site calls the machine the "IDM-16 swarm sequencer".
- **[Uncertain]** I can't tell whether IMD agents do anything at runtime beyond the IMD launch, or whether they also built the hook. "Swarm" may only be branding.
- **[Inference]** "theidmfun" is the real handle, not a typo for "theimdfun": IDM = Intelligent Dance Market.

### #3 ROBOBET, now Paper Clash (@robobet_fun → @paperclash_xyz)
- **[Fact]** robobet.fun: the user stakes a fixed $10–$100 in USDC. "An IMD agent designs" a single high-risk, short-term BTC or ETH perpetual trade, choosing direction, leverage and take-profit. PaperTrade places and settles it. The user can't step in and gets a "fate card" at the end. Its FAQ says: "Not yet [onchain]. Currently robobet runs through IMDs swarm network for intelligence and then places the trade on Papertrade on your behalf… you will have to trust us a bit more for now" ([robobet.fun](https://robobet.fun)).
- **[Fact]** The rebrand: paperclash.xyz is now titled "Paper Clash: Trade BTC and ETH, conquer territory, and earn rewards" ([paperclash.xyz](https://paperclash.xyz)). The IMD launch [launch-2589-paperclash](https://github.com/identity-md-launches/launch-2589-paperclash) links x.com/robobet_fun, and [launch-2614-paperclash](https://github.com/identity-md-launches/launch-2614-paperclash) links x.com/paperclash_xyz. Both are paperclash tokens launched through IMD.
- **How it uses IMD:**
  - **[Fact]** The IMD swarm makes the trading decisions.
  - **[Fact]** The token was launched through the IMD launch factory.
  - **[Uncertain]** Settlement is off-chain and custodial by the project's own account.
- **[Open]** paperclash.xyz renders client-side and I couldn't read the new "territory" game mechanics. I don't know how much of robobet survives in Paper Clash.

### #4 imdRadar (@imdradar)
- **[Open]** I found **no primary source** for imdRadar. I searched GitHub repositories, the identity-md-launches organisation, general web search, and the domains imdradar.com/.xyz/.fun/.app/.io. None returned a page. I can't verify what it does or how it uses IMD.
- **[Inference, unverified]** The name suggests a monitoring or analytics dashboard for the IMD network, such as launches, seats or swarm activity. Treat this as a guess.
- The ranking itself doesn't depend on this: it uses only the ballots.

### #5 imdLend by @sudeepb02
- **[Fact]** "an open market for lending IMD seats (IdentityMD NFTs) to other parties' machines, with each seat's earnings split on chain" ([sudeepb02/imdLend-contracts-public](https://github.com/sudeepb02/imdLend-contracts-public)). imdlend.com's tagline is "An open market for IMD seats. Paid upfront, rewards split automatically." ([imdlend.com](https://imdlend.com)).
- **[Fact] How it uses IMD:**
  - Seat owners list IMD seat NFTs at a price per day in IMD, with minimum and maximum durations and a reward split.
  - An operator pays upfront in IMD. 2% goes to the fee recipient and the rest to the owner.
  - The seat moves into a per-deal `IMDLend` vault clone. The IMD network pays seat rewards to that vault.
  - The operator pairs its devices through the vault's ERC-1271 signature check.
  - Anyone can trigger reward release, which splits rewards between the fee, the owner and the operator.
  - The vaults share one address across launch chains, so rewards paid on Robinhood Chain or Base can be collected.
  - The repo says it works "against the IMD protocol as it runs today; nothing in the protocol changes."

### Just outside: #6 NightShiftImd (@nightshiftimd)
- **[Fact]** The only source I found was an IMD custom-token launch for "NightShiftImd (SHIFT)", a plain fixed-supply ERC-20 ([launch-2106-nightshiftimd](https://github.com/identity-md-launches/launch-2106-nightshiftimd)).
- **[Open]** I couldn't find what the product does.

## 3. Uncertainty and open questions
- **[Uncertain]** The method decides #4/#5. "Votes, then Borda points, then head-to-head" gives imdRadar #4. "Votes, then points, then most #1 votes" gives imdLend #4. The organisers should confirm which rule they use.
- **[Open]** Does the hackathon have an official scoring rule, for example equal-weight judges or other judges' ballots? Only four ballots were provided, and no official results page turned up in search. A poster repo lists the prizes: 1st $1,500 + one IMD NFT, 2nd–3rd $1,000, 4th–5th $750 ([launch-908](https://github.com/identity-md-launches/launch-908-use-identity-md-image)).
- **[Open]** What imdRadar is, and how it uses IMD.
- **[Uncertain]** Whether Paper Clash is the same product as robobet or a pivot.
- **[Fact] Limits.** X/Twitter profiles were not read, because they need a login. Project descriptions are self-reported by the builders. I did not verify contracts on chain, check audits or test the products.
