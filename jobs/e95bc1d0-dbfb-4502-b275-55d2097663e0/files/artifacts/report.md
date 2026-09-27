# Growing Swarm Pepe: five ideas, one killed, one video

**Snapshot.** Ethereum mainnet, **block 26066817** (2026-09-27 05:51:11 UTC), unless a number
says otherwise. Logs cover the NFT's deployment block **26054542** (2026-09-25 12:43 UTC) up to
26066817.
**Labels used below.** **[F]** means I checked it directly (chain call, verified source, or a
public API response). **[I]** means I inferred it from facts. **[U]** means unverified or unknown.
**Reproduction.** The scripts and raw data are in `evidence/` (see `README.md`).

---

## 0. What exists today (verified)

### Contracts

| Item | Finding | Source |
|---|---|---|
| Source | Both contracts are verified, **exact match**, solc 0.8.26. SwarmPepe is `SwarmPepe_1.sol`, OZ v5 `ERC721 + Ownable2Step + IERC2981`. PixelArt is `PixelArt.sol`. | [F] Sourcify v2 API; Blockscout agrees |
| Proxy | None. EIP-1967 implementation and admin slots are zero. `ART()` returns `0x07Fd…3FcA` and is declared `immutable`. | [F] `cast storage` / `cast call` @26066817 |
| Constants | `MAX_SUPPLY` = 5000, `MAX_PER_WALLET` = 3, `ROYALTY_BPS` = 1000. | [F] @26066817 |
| State | `totalMinted` = **766**, `mintOpen` = true, `owner` = `royaltyReceiver` = `0x9073…1859`, `pendingOwner` = 0. | [F] @26066817 |
| Owner's own slot | `allowance(owner)` = 3, but the owner's `claim()` reverts with `OwnerCannotMint`. | [F] @26066850 |
| Owner ETH | 0.02256 ETH | [F] @26066817 |

**Two corrections to the brief:**

1. The owner can do **five** things, not four. OZ `Ownable` gives `renounceOwnership()`
   (selector `0x715018a6`, present in the deployed bytecode). Also, `grant(…, 0)` *revokes* a
   slot, because allowance is overwritten, not added. Renouncing would freeze the allowlist
   forever at 2595 slots, so none of the ideas below should ever call it. [F]
2. `minterOf(id)` says "who minted this token, regardless of who holds it now". It actually
   returns `address(0)` for every revealed token, because it reads `_commit`, which `reveal()`
   zeroes. I checked `minterOf(1)` = 0 @26066817. Minter provenance survives **only** in the
   `Minted(to, tokenId, mintBlock)` event. Any second contract that needs the minter must take
   it from logs or a Merkle root, not from this function. [F]

### What `tokenURI` actually returns

I checked tokens #1, #343 and #766 @26066817.

- The result is `data:application/json;base64,…`. It contains the `name`, a fixed
  `description`, an `image` that is `data:image/svg+xml;base64` (a 24×24 grid of `<rect>`s,
  480 px), and exactly **five** attributes: Skin, Eyes, Mouth, Hat, Accessory. [F]
- #1 is Light Green / Side Eye / Cigarette / None / Chain (24 rects). #766 is Light Green /
  Plain / Smile / None / None (20 rects). #343 is **Gold** / Plain / Smile / None / Earring
  (21 rects). [F]
- The renderer also draws three things that are **not** in the attributes: background (8
  colours, `seed % 8`), shirt (5 colours), and hat colour (4–5 per hat type). Across the 766
  tokens there are **562** distinct combinations of the five declared traits, but **763**
  visually distinct pictures. 118 groups share declared traits but look different. [F]
  Computed from `Revealed` seeds; 14 tokens were cross-checked against on-chain
  `PixelArt.attributes()`.
- Unrevealed tokens show `placeholderSVG()` with a single `Status: Unrevealed` attribute. [F]
  Source; none exist right now.

### Mint, reveal and allowlist mechanics (from source, and observed)

- `claim()`, `claim(n)`, or a **0-ETH transfer** to the contract mints what the wallet is owed.
  There is no proof and no calldata. [F]
- The allowlist is an on-chain mapping. Slots are capped at 3 per wallet for its **lifetime**:
  `minted[]` never resets, so re-granting a wallet that has minted gives it nothing new. [F]
- `reveal(uint256[])` is permissionless. The seed is
  `keccak256(blockhash(mintBlock+1), id, minter, this)`. It reaches back through EIP-2935 for up
  to **8191 blocks (~27 h)**. After that the token stays unrevealed **forever**. [F] Source.
  I recomputed #343's seed from the hash of block 26055816 and it matches its `Revealed` event.

### Observed activity, blocks 26054542 to 26066817 [F]

| Metric | Value |
|---|---|
| `AllowanceSet` events | 889 across 3 grant txs (all `grant(address[],3)`) → **865 distinct wallets, 3 slots each = 2595 slots** |
| Genesis batches (blocks 26054675, 26054685) | 789 wallets. **255 have minted (32.3 %)** |
| Later batch (block 26061303, 2026-09-26 11:23 UTC) | 100 addresses: 76 new, 24 re-grants of genesis wallets (no effect). **1 of the 76 new wallets has minted** |
| Distinct minters | 256 (255 minted 3, 1 minted 1 via `claim(1)`) |
| Unclaimed granted slots | **1829** (2595 − 766) |
| Mint rate | 609 mints in the first ~1800 blocks (~6 h) after `setMintOpen(true)` at 26054787. **34** in the last 7200 blocks (~24 h) |
| Revealed | **766 / 766**. 70 reveal txs, **57 of them from one address** (a keeper) |
| Reveal lag | median 156 blocks, **max 5183** (63 % of the 8191-block window). **230** reveals came >257 blocks after mint, so they relied on EIP-2935 history |
| Holders | **261** (17 of them never minted, so they bought or were sent tokens) |
| Moves after mint | 100 `Transfer`s of 86 tokens in 54 txs: 36 to marketplace contracts (33 to Seaport 1.6), 18 direct `transferFrom` |
| Royalty actually received by `royaltyReceiver` in those 36 txs | about **0.009 ETH + 0.0066 WETH** (Blockscout internal-tx and token-transfer API; may undercount) |
| `ApprovalForAll` | 79 approvals to OpenSea's conduit `0x1E00…3c71` |

Trait counts across the 766 revealed tokens [F]:

| Trait | Counts (value: count) |
|---|---|
| Skin | Green 450, Dark Green 138, Light Green 102, Zombie 50, Stone 19, **Gold 7** (#343, 360, 469, 472, 587, 610, 728) |
| Hat | None 234, Cap 112, Cap Forward 77, Beanie 87, Headband 86, Top Hat 66, Mohawk 87, **Crown 17** |

No token has both Gold skin and a Crown.

### Who has not claimed, and can they? (aggregate only, no identity work)

| Finding | Label |
|---|---|
| 609 allowlisted wallets have never minted. | [F] |
| I simulated `claim()` from each of them with `eth_estimateGas` at head block **26066850**. **604 would succeed right now.** 5 revert: 2 contracts lacking `onERC721Received` (`ERC721InvalidReceiver`), 2 EIP-7702 wallets whose delegate reverts, and 1 that is the owner (`OwnerCannotMint`). | [F] |
| Gas for a 3-token claim is 231,873. At 0.06 gwei (the gas price at ~26066820) that is ≈ 0.000014 ETH ≈ **$0.04** (ETH $2704, CoinGecko 06:01 UTC). | [F] |
| Median ETH balance of the 609 is 0.043 ETH; only 15 hold zero ETH. | [F] @26066837 |
| **Gas money is not what stops them.** | [I] |
| The genesis allowlist is the swarm's own seat holders: 731 of 865 allowlisted wallets own an IMD seat (`GET api.imd.fun/seats/owners`: 2000 seats, 777 distinct owners, read ~06:00 UTC). **46 seat owners are not allowlisted.** | [F] |
| **None** of the 76 new later-batch wallets owns a seat, and only 5 of the 76 hold any IMD, against 24 of a random 100 from genesis. Yet they are active wallets (median nonce 283). | [F] |
| So the swarm's own people converted at 32 %, and outsiders who probably do not know they are listed converted at 1 in 76. | [I] |
| I could not find what produced the 76-wallet batch. The natspec says "oracle's daily picks", but none of the 1500 most recent oracle requests (2026-09-24 20:50 UTC to now) is an address-list question. | [U] |

### Market (OpenSea API v2, read 2026-09-27 06:01 UTC; not pinned to a block)

| Finding | Label |
|---|---|
| 77 sales, 0.837 ETH total volume (58 sales / 0.648 ETH in the last day), floor 0.0128 ETH, 261 owners. The owner count matches mine. | [F] |
| The 10 % creator fee is listed `"required": false`. `trait_offers_enabled`: false. `safelist_status`: `not_requested`. The OpenSea description reads "Most of these pepes don't have owners yet. The swarm is still choosing." | [F] |
| On-chain royalty receipts are ≈1.9 % of OpenSea volume. **Royalties are not a revenue line and no idea below depends on them.** | [I] |

### Swarm (`api.imd.fun`, `explorer.imd.fun`, `imd.fun/docs`, read ~06:00 UTC)

| Finding | Label |
|---|---|
| 458 connected daemons, 102,727 jobs accepted in the last day, 284 paid orders so far. | [F] |
| Paid requests cost **0.5 IMD** each: `job.open`, `launch.open`, `workflow.open`, `oracle.request`. IMD was $7.61 on Uniswap (DexScreener, 06:01 UTC), so **≈ $3.80 per job**. | [F] |
| The swarm publishes static sites to IPFS under `*.site.identitymd.eth` (e.g. `pepes-armed`, `GET /publications?q=pepe`). | [F] |
| The oracle signs EIP-712 attestations (signer `0x5598…2982`) with `address[]` among the answer types (docs). | [F] |
| A Swarm Pepe teaser video already exists: job `e09376af`, delivered 2026-09-26. It is a crowd shot plus stat cards, and its hero pepe was a hand-picked trait set (Gold, Laser, Vape, Crown, Mole) that **no real token has**. | [F] |

### The diagnosis everything below rests on

| Finding | Label |
|---|---|
| Supply can only grow through `grant()`. Even if every current slot were claimed, the collection stops at **2595 of 5000**. | [F] |
| Right now the binding constraint is not grants but *claims*: 1812 tokens are already authorised, and the wallets holding them have both the ETH and a working code path. | [F]/[I] |

---

## The five ideas, ranked

### 1. Tell the 604 wallets they have free Pepes, and make claim-and-reveal one click (do this first)

**Why this is first.** It acts on **1812 tokens that are already authorised on chain**. That is
2.4× everything minted so far. It needs no new trust, no new contract and no money beyond
≈ $4. It also closes the one real operational risk I found, the reveal window, for the tokens
it brings in. Every other idea either adds supply that is not being used yet or adds demand
that the current holder base is too small to feel.

1. **What it is.** A static page where anyone pastes or connects an address and sees
   `allowance`, `minted` and `remaining`. One button calls `claim()`, and two blocks later the
   page calls `reveal([ids])` and shows the picture from `tokenURI`. At the same time, the
   OpenSea description and the X account stop saying "the swarm is still choosing" and start
   saying "allowlisted? send 0 ETH to 0x999c… or open <page>".
2. **What already makes it possible.**
   - `remaining(address)`, `allowance(address)`, `minted(address)`, `claim()`, and the 0-ETH
     `receive()` path.
   - `reveal(uint256[])`, `revealableAt(id)`, `isRevealed(id)`, `tokenURI(id)`.
   - `AllowanceSet` / `Minted` events, to list who is owed.
   - The swarm's IPFS site publishing (`/sites`, `*.site.identitymd.eth`).
   - The owner is an OpenSea collection editor ([F] `editors` field), so the description can be
     changed.
3. **What has to be built.** A **page** (one HTML file, four view calls and two writes) and a
   short **keeper script** that calls `reveal` on anything whose `revealableAt` has passed. The
   keeper should be public, so it no longer depends on the single address that sent 57 of 70
   reveal txs. **No new contract.**
4. **Effort.** Hours by hand. Alternatively, one swarm `build-website` job at 0.5 IMD
   (≈ $3.80). **Money: ≈ $4, or zero if built by hand.**
5. **The number.** **Unclaimed granted slots**, 1829 at block 26066817. To read it, take
   Σ `3·|distinct AllowanceSet accounts with amount 3|` − `totalMinted`. The same value is
   Σ `remaining(a)` over every `AllowanceSet` account, which needs one `eth_call` per address.
   Success is a clear step down in the week after the page and description change go live.
   Background decay is 34 mints a day, so for example it should fall below ~1300 within 7 days.
   Read it with its block height.
6. **Strongest argument against.** It does not solve reach. The only no-identity channels are
   the OpenSea page, X and the swarm's own surfaces, and the 76 outsiders may never look at any
   of them. The 609 may also simply not want a free JPEG: seat owners were told at genesis and
   68 % still did not claim. There is also a cost: floor is 0.0128 ETH on a book that has seen
   77 sales ever. 1800 new, costless tokens will mostly be listed, and the floor will fall
   [I]. Growth in holders can mean a collapse in price, and whoever runs this should decide in
   advance which of the two they are optimising.

### 2. Earned slots: grant to wallets that did accepted work for the swarm, on a published rule

1. **What it is.** A daily script reads which seats had work accepted and grants 3 slots to each
   seat owner who is not already on the list. The rule is published on the page from idea 1 so
   anyone can check it. This turns the tokenURI's own claim, "minted by wallets the swarm picked
   out", from a sentence into a checkable rule, and it aims grants at the population that
   actually converts: 32 % versus 1 in 76.
2. **What already makes it possible.**
   - `grant(address[],uint256)` (onlyOwner) and `allowance(address)`, used to skip wallets
     already listed.
   - `GET api.imd.fun/seats/records` (per seat: `accepted`, `lastWorkedAt`) and
     `GET /seats/owners` (owner per seat token, "read from chain").
3. **What has to be built.** A **script** (cron, one owner-signed tx a day). **No new
   contract.** Grant gas was measured at 2,005,002 for 100 addresses (tx `0xa5b0…1ef6`), which
   is ≈ 0.00012 ETH at 0.06 gwei. The owner's 0.0226 ETH covers well over a hundred such batches
   at today's gas. **Money: under $1 a month at current gas; ~$11 per 100-wallet batch if gas
   went to 2 gwei.**
4. **Effort.** Hours to write. Minutes a day to run, or zero if it runs on a schedule.
5. **The number.** **7-day claim rate per grant batch.** For each `grant` tx, take the new
   accounts in its `AllowanceSet` events. Count how many of them appear as `to` in a `Minted`
   event within 50,400 blocks (7 days), then divide by batch size. The genesis baseline is
   32.3 %, and the 26061303 batch is 1 of 76 so far. If earned-slot batches do not beat the
   outsider batch by a wide margin, stop.
6. **Strongest argument against.** The pool is small. Only **46** seat owners are unlisted today
   ([F], `/seats/owners` ~06:00 UTC), and 777 seat owners × 3 = 2331. That is below the 2595
   already granted, so this can never approach 5000 on its own. Seats are ERC-721s held in a
   separate collection (`0x0000ec93…ec1d`). If a seat can be bought, buying one becomes a way to
   farm Pepe slots [U: I did not check seat transferability or price]. The per-wallet cap binds
   addresses, not people, and the contract says so itself.

### 3. Show the whole picture: a gallery of what the renderer draws but the metadata hides

1. **What it is.** A static gallery that renders every token straight from `seedOf` through
   `PixelArt.renderSVG`. It adds the three visible dimensions the attributes omit (background,
   shirt, hat colour), which is 763 distinct pictures where the metadata sees 562. It also shows
   each token's mint block and reveal block from the events, since `minterOf` no longer works.
   The owner switches on OpenSea **trait offers**, which are currently off, so the 7 Gold and 17
   Crown tokens can be bid on directly.
2. **What already makes it possible.**
   - `seedOf(id)`, `ownerOf(id)`, and `ART.renderSVG(seed)` / `ART.attributes(seed)`. These are
     `pure` and can be called by anyone.
   - `Minted` and `Revealed` events.
   - OpenSea collection settings, since the owner is an editor.
3. **What has to be built.** A **page**. A second contract cannot add traits to OpenSea, because
   OpenSea reads `tokenURI` from the original. So the hidden dimensions can only live on this
   page, never in marketplace filters. **No new contract.**
4. **Effort.** About a day, or one 0.5 IMD swarm site job. **Money: ≈ $4 or zero.**
5. **The number.** **7-day secondary sales count** from `GET api.opensea.io/api/v2/collections/swarm-pepe/stats`
   (`intervals[seven_day].sales`, 77 at 06:01 UTC). The on-chain alternative is to count Seaport
   1.6 `OrderFulfilled` logs that carry this contract address. Compare the 7 days after launch
   against the 7 days before.
6. **Strongest argument against.** Its number does not isolate its effect. Sales move with
   mints, with the floor, with ETH, and with anything posted on X. A page's own traffic is not
   public, so there is no clean way to prove the gallery did anything. The traits it adds cannot
   be filtered on the marketplace where the buying happens.

### 4. SwarmPepeSets: a second contract that records completed trait sets

1. **What it is.** A small **second contract** where a holder submits token ids. It checks on
   chain that they own all of them and that the ids complete a named set, for example "all six
   skins", "all eight hats" or "Crown + Laser". It then emits `SetCompleted(holder, setId, ids)`
   and marks those token ids as spent for that set. This gives people a reason to buy specific
   tokens on the secondary market, readable by anyone, with no off-chain judge.
2. **What already makes it possible.** It reads `SwarmPepe.ownerOf(id)`, `SwarmPepe.seedOf(id)`
   (0 means unrevealed, so reject), and either `PixelArt.attributes(seed)` or, more cheaply, a
   copy of `_pick` with the five weight tables. I verified that my reimplementation matches the
   on-chain `attributes()` on 14 tokens. **The original stays untouched:** the new contract only
   calls `view`/`pure` functions. It never takes custody, never needs approval, and needs no
   owner action on SwarmPepe.
3. **What has to be built.** A **second contract** (about 100 lines, no funds, no admin) and a
   panel on the page from idea 1. Worth one swarm review job before deploying.
4. **Effort.** Days: contract, tests, one swarm adversarial-review job, deploy.
   **Money:** deploy gas, unmeasured; I estimate ~1M gas ≈ 0.00006 ETH at 0.06 gwei. Add
   0.5–1 IMD (≈ $4–8) for swarm build and review jobs.
5. **The number.** **Distinct addresses that emitted `SetCompleted`**, read from the new
   contract's logs. Secondary check: the OpenSea 7-day sales from idea 3.
6. **Strongest argument against.** The market is too thin to be pulled by a game. There are
   77 sales ever, 261 owners and a 0.0128 ETH floor. The headline set ("all six skins") needs one
   of **7** Golds. Tokens can be lent from wallet to wallet to satisfy an ownership check,
   unless proofs are spent per token, which then makes the game feel stingy. And with royalties
   effectively optional (≈1.9 % received), any volume it creates earns the project almost
   nothing.

### 5. GrantGate: hand ownership to a contract that grants on a signed swarm-oracle answer, **KILLED**

1. **What it is.** A **second contract** takes ownership of SwarmPepe through `transferOwnership`
   and `acceptOwnership`. It exposes one public function that calls `grant(addresses, 3)` when
   given an EIP-712 attestation from the swarm oracle signer answering "which wallets qualify on
   day N". It forwards `setMintOpen`, `setRoyaltyReceiver` and `transferOwnership` to a human
   admin. The allowlist would then really be "decided by the swarm" instead of by one key.
2. **What already makes it possible.**
   - `Ownable2Step.transferOwnership` / `acceptOwnership`, and `grant(address[],uint256)`.
   - `GET api.imd.fun/oracle/requests/:id/attestation`: EIP-712 typed data, `address[]` answer
     type, a `consumer.verifyingContract` domain, and signer `0x5598…2982`.
   - **The original stays untouched.** Only the value of `owner()` changes, and every
     `onlyOwner` call now arrives from GrantGate.
3. **What has to be built.** A **second contract**, which becomes the owner, plus a daily
   `oracle.request`. Before the handover, `grant([currentOwner], 0)`. Once the EOA stops being
   owner, `OwnerCannotMint` no longer covers it, and it currently holds 3 slots ([F]
   `allowance(owner)` = 3 @26066817).
4. **Effort.** One to two weeks including review. **Money: 0.5 IMD per daily oracle question,
   about $3.80/day or ~$115/month, plus deploy gas.**
5. **The number.** Share of `AllowanceSet` events whose transaction's `to` is GrantGate, and
   the 7-day claim rate of those batches (the same method as idea 2).
6. **Strongest argument against: why I drop it.** See below.

**Why this is the one I kill.** It moves the single most dangerous lever in the system, the
only address that can ever add supply, into new code. And it buys something that is not
growth. If GrantGate has a bug in its forwarding of `transferOwnership`, the remaining
2405+ tokens can never be allowlisted, **permanently**, because nothing in SwarmPepe can
recover ownership. The benefit is trust-minimising a decision that nobody currently disputes,
and a cron job (idea 2) does the same work for free. The oracle side is also fragile for this
use: an `address[]` answer needs every panel member to return the same list (quorum means
"every one must match", per the docs). 5 of the last 500 oracle requests already ended
`disagreed`, on much simpler questions ([F] `/oracle/requests` ~06:00 UTC). It is also the only
idea with a recurring cash cost (~$115/month) and no demand-side effect at all. This is the
idea that sounds best in a thread, and it is the worst trade here.

---

## Ranking summary

| Rank | Idea | Build | Effort | Money | Number |
|---|---|---|---|---|---|
| 1 | Claim-and-reveal page + signposting | page + keeper script | hours | ≈ $0–4 | unclaimed granted slots (1829 @26066817) |
| 2 | Earned slots on a published rule | script | hours | < $1/mo gas | 7-day claim rate per grant batch (32.3 % / 1 of 76) |
| 3 | Full-picture gallery + trait offers | page | ~1 day | ≈ $0–4 | OpenSea 7-day sales (77 @06:01 UTC) |
| 4 | SwarmPepeSets | second contract | days | ≈ $4–8 + gas | distinct `SetCompleted` addresses |
| ~~5~~ | ~~GrantGate~~ (killed) | second contract (owner) | 1–2 weeks | ~$115/mo | grant share via GrantGate |

---

## Video: "One block decides" (30 seconds)

**Concept.** Follow one real token, **#343**, one of 7 Golds, from its unrevealed placeholder
to finished art. On screen: the actual block hash that decided it, then the renderer drawing
its 21 rects in the exact order the SVG lists them.

| Time | On screen | Asset source |
|---|---|---|
| 0–4 s | The grey placeholder pepe, centred, nearest-neighbour upscaled. Caption: `Swarm Pepe #343 · minted in block 26,055,815`. | `PixelArt.placeholderSVG()`; mint block from the `Minted` event of id 343 |
| 4–10 s | Caption: "its art came from the next block". The hash of block **26,055,816** types out, one hex character per frame: `0x40b24f14…d8ad`. | `eth_getBlockByNumber(26055816).hash` |
| 10–13 s | The hash, `343`, `minter` (label only, no address shown) and the contract address fall into a `keccak256(…)` box. The 78-digit seed comes out. | Seed from the `Revealed(343, seed)` event; reproducibility checked, see §0 |
| 13–25 s | The placeholder is wiped. The 21 rects of `renderSVG(seed)` appear one by one in document order: background `#638596`, then the 9 head rects in Gold `#d8b23c` / `#a8831f`, the 3 shirt rects, eyes, the three mouth rects, and last the gold earring pixel at (6,15). About 0.55 s per rect; the last one lands on a beat. | `tokenURI(343)` decoded SVG, or `PixelArt.renderSVG(seedOf(343))` (identical) |
| 25–28 s | The attribute JSON types in beside it: `Skin: Gold`. Then the line "7 of 766". | `tokenURI(343)` attributes; the count comes from `Revealed` seeds, stated with its block height |
| 28–30 s | Black. `reveal(uint256[]) — anyone can call it.` Then `0x999ce0ce…7bdb`. | Verified source |

**Production notes.**

- It can be rendered by a script: parse the SVG and add one `<rect>` per frame range. One
  0.5 IMD `create-video` swarm job, or an afternoon with ffmpeg. **Money: ≈ $4 or zero.**
- Every number shown must carry the block it came from, in the delivery notes.
- Audio should be original or public domain.

**What makes it different, in one sentence.** Every pixel and every digit on screen can be
checked on chain: the video shows the actual randomness of one real token turning into its art
in the renderer's own draw order. A generic trailer (including the existing one, whose hero
pepe was an invented trait set) shows a mood.

---

## Unanswered questions and uncertainty

| Question | Status | Why it matters |
|---|---|---|
| Who chose the 100 addresses in block 26061303, and by what rule? | [U] No matching oracle request found in the last 1500 | Idea 2's rule should replace or explain it |
| Are IMD seats transferable, and at what price? | [U] Not checked | Determines whether earned slots (idea 2) can be farmed |
| Does the operator control `explorer.imd.fun` or the daemon UI, so a seat owner could see "you have 3 unclaimed Pepes"? | [U] | The only reach channel for idea 1 that does not rely on X or OpenSea |
| Did Blockscout's internal-tx API catch every royalty payment? | [U] My 0.009 ETH + 0.0066 WETH may undercount | It does not change the conclusion unless it is off by 5× or more |
| Is the reveal keeper (57 of 70 reveal txs) operated by the project, and will it keep running? | [U] Worst lag so far is 5183 of 8191 blocks | If it stops for ~27 h, new mints stay unrevealed **forever**. Idea 1's public keeper is the mitigation |
| @swarmpepes on X: follower count and content | [U] Could not read without login | Nothing above relies on it |
| Deploy gas for idea 4 | [U] Estimated, not measured | Small at today's gas either way |
