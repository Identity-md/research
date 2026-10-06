# IMD Viral Wars — v2.1 targeted correction and minimal validation plan (report v3)

**Date:** 6 October 2026, about 23:50 UTC.
**Scope:** This is a targeted correction of [report v2](https://github.com/Identity-md/research/blob/main/jobs/38fe2057-037c-4a4a-b0b5-14651a90c5f5/files/artifacts/report-v2.md), archived at `evidence/v3/report-v2.md`. It replaces v2 §2.3–2.4 (measurement window), §4.5 and §6 item 4 (treasury and allocation), and the token-pilot row of §7 (voting snapshots). It also amends Gate C in §8. Every other v2 section stands unless this document says otherwise.
**Evidence:** Raw captures are under `evidence/v3/`, with `evidence/v3/SHA256SUMS`. They are reproducible with `scripts/capture_v3_evidence.py` (public reads only) and `scripts/funds_flow_v21.py` (the model).
**IMD control plane observed:** commit `7471272e37c4fbd51b40f02c0659da1d2cf5aa35` (`evidence/v3/imd-version.json`). **Ethereum state read at block 26,136,703.**

Labels, as in v2:

- **[Fact]**: stated by a cited primary source, or observed directly on chain or in a live API response today.
- **[Inference]**: my reasoning from facts.
- **[Assumption]**: an untested planning input.
- **[Proposal]**: a design choice.
- **[Unknown]**: an open question.

All prices and volumes are illustrations.

---

## 0. Answer in brief

1. **The fee currency is now known, and it is mixed.** **[Fact]** On the mainnet IMD launch factory, the 1.25% pool fee is collected by `claimFees(launchNumber)`. It is paid out in **both pool currencies**: IMD from buys, and the launch token from sells. The split is exactly **80% to the launch's requester (paying wallet) and 20% to a network fee recipient**. This was observed in all 27 claims made to date, across 10 launches. Any address can call the claim. A RED/IMD pool will therefore pay the treasury in **IMD + RED**, and a BLUE/IMD pool in **IMD + BLUE** (§2, E4–E6).
2. **The original rule can operate as intended.** "Fees from both teams, after operating costs, fund the winner of that round" is implemented by:
   - taking the operating share from *all* receipts;
   - **selling the loser's token receipts into the loser's pool for IMD**;
   - using that IMD to buy the winner's token and burn it.

   At the modelled sizes this costs the round's budget about 1.3–1.6% (the 1.25% pool fee, small price impact and gas). Most of the pool fee returns to the treasury in a later period (§4.4). v2 §4.5 escrowed the loser's token for that team's next win. That is a **product change** and is withdrawn.
3. **v2's treasury accounting was internally inconsistent.** v2 §4.3 assumes operations receive 20% of all fee revenue, but v2 §4.5 applied the 20% to IMD receipts only. In the worked example that gives operations 11.5% of receipts. v2.1 applies 20% to all receipts, valued at each swap's own execution price (§4.2–4.3).
4. **Measurement:** the score now covers the whole interval **[T_open, T_close]**, measured from a verified zero baseline at publication, not from a 15-minute snapshot. Snapshot selection is a total order over reads. The API returns **no counter-freshness timestamp**, so response time and counter freshness are kept separate (§3).
5. **Voting:** seven daily snapshots prove presence at seven instants, not holding. v2.1 uses the **exact minimum balance over the whole window, replayed from Transfer logs**, and keeps the snapshots only as a cross-check (§5).
6. **Still undemonstrated, and these decide go/no-go:**
   - a smart-contract (multisig) wallet as payer and fee recipient: every observed recipient is an EOA;
   - the fee path for the specific launch kind chosen for RED/BLUE: only `custom_token` launches have claims on record;
   - the owner of the fee contract can change the network fee recipient, and has done so;
   - third parties can add liquidity and dilute the treasury's 1%;
   - the tokens have no `burn()`.

   The validation checklist in §6 addresses these first.

---

## 1. Correction log (v2 → v2.1)

| # | v2 text | Problem | v2.1 correction | Basis |
|---|---|---|---|---|
| 1 | §4.5: loser-token fees “held in escrow and burned when that team next wins” | It funds the **loser**, breaking “both teams' fees fund the winner of that round”. | Loser-token receipts are sold for IMD, and the IMD buys and burns the winner's token in the same round. Escrow is listed only as a product-change alternative (C). | §4.3–4.4, model |
| 2 | §4.5: “fees in IMD fund operations (20%)” | Operations get 20% of IMD only, about 11% of all receipts, which contradicts the §4.3 model. | 20% of **all** receipts, valued in IMD at execution prices. Ledger states: accrued → claimed → allocated → spendable / executed. | §4.2 |
| 3 | No collection periods; draws mean “no burn” | Fees had no deterministic round assignment. Draws, no-contests, delayed claims, unused budgets and season ends were unspecified. | Half-open 24-hour fee periods assigned by **accrual block**, never by claim time. Explicit roll-forward and season-end rules. | §4.5 |
| 4 | §2.3: opening snapshot at T_open + 15 min, score = close − open | This drops the first 15 minutes of plays. v2 also required `public` status, but `batchGetStats` does not return it. | Scored interval [T_open, T_close] with a verified zero baseline. Deterministic read ordering. Missing-data rules. Freshness is measured, not assumed. | §3, E10 |
| 5 | §1.2, §6: fee split evidenced only by a dry-run | A dry-run is acceptance, not execution. | Mainnet execution evidence (27 claims) separated from dry-run text, with stated limits. Minimal validation plan. | §2, §6 |
| 6 | §7: “7-day minimum makes flash loans … useless” | Seven snapshots prove presence at seven blocks, not continuous holding. | Continuous minimum via Transfer-log replay, plus a stated residual risk (renting for the whole week). | §5 |
| 7 | §8 Gate C: “fee currency and claim path confirmed on Sepolia” | **[Fact]** Sepolia offers launch pairings with ETH only, so an IMD pair cannot be rehearsed there (capabilities). | Fee currency and claim path are established from mainnet records (done here). The RED/BLUE launch has its own post-launch check (§6, V7). | E2 |
| 8 | (new) | **[Fact]** Launch tokens expose only the 9 standard ERC-20 functions, with no `burn`. | A burn is a transfer to `0x…dEaD`. Burned supply is reported as the dead-address balance, because `totalSupply` does not fall. | E8 |
| 9 | (new) | **[Fact]** The network fee recipient changed on chain mid-life for launch 737. **[Inference]** Third-party liquidity can dilute the treasury's 1%. | Both are monitored and are pass/fail items (§6, V4–V5). | E5, E7 |

---

## 2. Evidence register: acceptance vs demonstrated execution

| ID | Evidence | Type | What it proves | What it does **not** prove |
|---|---|---|---|---|
| E1 | `POST /requests/check` for RED, `evm_project` and `univ4_hook`, mainnet, `pairWith: "imd"` (`evidence/v3/imd-check-red-*.json`, 23:43 UTC) | **Dry-run (acceptance)** | The live control plane states fixed facts: “Trading fee: 1.25% of every trade: 1% to you, 0.25% to IMD, claimable any time”; “Pool: paired with IMD, opening at a 2,500 IMD market cap”; plain transfers; 1B supply; 80% to the pool. The only blockers are input-shape ones (`bad_path_count`), not chain or policy ones. | That a launch will be admitted, that it will deploy, or how fees are collected. |
| E2 | `/launch/policies` v29 (univ4_hook, chain 1): `feeTiers [12500]`, IMD cap 2,500 IMD, `treasuryBps 1000`, `liquidityBps 8000`. `/requests/capabilities`: Sepolia pairings are ETH only. Payment is x402 v2 `exact`, `permit2`, EIP-712 quote approval, on eip155:1. | **Policy text** | The intended configuration and which chains and pairings are open. | That contracts enforce it. |
| E3 | Deployment receipt of launch 829 (custom_token, IMD pair), [tx `0xe9bb3a…`](https://eth.blockscout.com/tx/0xe9bb3ace45bffb8fc222cbdad3f50c1afad0ea343f97be147bb2497d2cf60ff1) | **On-chain execution** | `PoolManager.Initialize` with fee `12500`, tickSpacing 60, currency0 = IMD. A single `ModifyLiquidity` whose sender is the **factory** (`0xff03…7120`) over ticks [−887220, 128940]: a single-sided position from the opening price down to the minimum tick. | That `univ4_hook`-kind launches use the identical path. |
| E4 | Factory `fees()` → **LaunchFees** `0x12c9…3863`: `poolFee()=12500`, `MAX_POOL_FEE()=100000` (10%), an unlabelled getter `0xcd26a197()` returning 8000, `feeRecipient()=0x3f25…1f22`, `owner()=treasury()=0x047f…b7b7`. Setters present: `setPoolFee`, `setFeeRecipient`, `setTreasury`, `transferOwnership`. | **On-chain read** (source **unverified** on Blockscout and Sourcify) | The fee is a 1.25% Uniswap v4 *static LP fee*. A static fee is fixed per pool at initialisation: `DYNAMIC_FEE_FLAG = 0x800000`, and only dynamic-fee pools can be updated ([LPFeeLibrary](https://github.com/Uniswap/v4-core/blob/46c6834698c48bc4a463a86d8420f4eb1d7f3b75/src/libraries/LPFeeLibrary.sol), [PoolManager.updateDynamicLPFee](https://github.com/Uniswap/v4-core/blob/46c6834698c48bc4a463a86d8420f4eb1d7f3b75/src/PoolManager.sol)). **[Inference]** `setPoolFee` affects future launches only. 8000 bps matches the observed 80% requester share, but no setter for it is visible (selector scan, not source). | The contract's full logic, because the source is unverified. |
| E5 | **All 27 `claimFees(uint64)` transactions** to the factory, blocks 26,129,313–26,135,240, decoded (`evidence/v3/onchain-launchfees-claims.json`, raw receipts in `onchain-claimfees-raw.json`) | **Demonstrated execution** | 27/27 succeeded, for launches 737, 739, 740, 741, 745, 747, 751, 754, 757 and 812 (all `custom_token`; 739 and 747 are ETH-paired, the rest IMD-paired). Each claim: a zero-delta `ModifyLiquidity` (fee poke) → both currencies transferred from `PoolManager` to the factory → paid **80.0% / 20.0%** in **each** currency to the requester and the network recipient. For example, [launch 737](https://eth.blockscout.com/tx/0xd751270d5e5a49352c5151065f41e0d29d37de40b73f5c089f9002aa8c4e7259): 83.0399 IMD and 3,549,202 ZTO collected → 66.4319 IMD and 2,839,362 ZTO to requester `0x7b8c…0479`, 16.6080 IMD and 709,840 ZTO to the network. Callers include unrelated addresses (e.g. `0x8d11…9162`, `0xa658…0df1`, `0xcefd…bd65`), and payment still goes to the requester. Funds are pushed; nobody has ever called `withdraw`. Gas used: 149k–304k at 0.26–1.33 gwei (≈ $0.10–$1.10 at ≈$2,700/ETH). | That a **contract wallet** can receive these funds: all 9 recipients have no code. That `evm_project` or `univ4_hook` kinds are claimed the same way: launch 823 (evm_project) has no claim yet, and there is no live mainnet univ4_hook launch under v29 (#825 parked). |
| E6 | Requester = fee recipient: launch records 737 and 812 (`requester` = `0x7b8c…0479` and `0x6bf1…606c`) match the 80% payees | **API + chain** | “1% to the paying wallet” as executed. | Whether the recipient can be changed after launch. **[Unknown]** |
| E7 | Network recipient history for launch 737: block 26,129,313 paid `0x047f…b7b7`; block 26,129,347 onward paid `0x3f25…1f22` | **On-chain execution** | **[Fact]** The network-side recipient is read at claim time and was changed by the LaunchFees owner during a launch's life. | Whether the 80% requester share can change. It has no visible setter, but the source is unverified. |
| E8 | Bytecode selectors of launch tokens `0x0593…1b67` (evm_project) and `0xd782…a68e` (custom_token) | **On-chain read** | Only `name, symbol, decimals, totalSupply, balanceOf, transfer, transferFrom, approve, allowance`. **No `burn`, no vote checkpoints.** | Behaviour on `transfer(address(0))`, which is **[Inference]**: OpenZeppelin-style tokens revert on it. |
| E9 | `ModifyLiquidity` logs for pools 737, 812 and 740 (Blockscout, `evidence/v3/blockscout-modifyliquidity-*.json`). Pool guard hook `0x784f…6000` | **On-chain read** | So far only the factory has added liquidity. The hook's address flags (low 14 bits = `0x2000`) enable only `BEFORE_INITIALIZE` ([Hooks.sol](https://github.com/Uniswap/v4-core/blob/46c6834698c48bc4a463a86d8420f4eb1d7f3b75/src/libraries/Hooks.sol) flags). **[Inference]** Nothing stops a third party from adding in-range liquidity and taking a pro-rata share of the 1.25%. | That this will happen. |
| E10 | YouTube [`videos.batchGetStats`](https://developers.google.com/youtube/v3/docs/videos/batchGetStats) (updated 14 Sep 2026): each item returns only `id`, `etag`, `snippet.publishTime`, `statistics.{viewCount, likeCount, commentCount}` and `contentDetails`, plus `summary` | **Primary doc** | No privacy-status field and **no “counter as of” timestamp**. | How stale `viewCount` can be. |
| E11 | Uniswap v4 [SwapMath](https://github.com/Uniswap/v4-core/blob/46c6834698c48bc4a463a86d8420f4eb1d7f3b75/src/libraries/SwapMath.sol): “feeAmount The amount of input that will be taken as a fee”. `Swap` event carries `amount0, amount1, sqrtPriceX96, liquidity, tick, fee` ([IPoolManager](https://github.com/Uniswap/v4-core/blob/46c6834698c48bc4a463a86d8420f4eb1d7f3b75/src/interfaces/IPoolManager.sol)) | **Primary source** | LP fees accrue in the swap's input currency, which explains E5. Per-swap fee accounting can be rebuilt from events. | — |
| E12 | Permit2 [SignatureVerification](https://github.com/Uniswap/permit2/blob/cc56ad0f3439c502c246fc5cfcc3db92bb8b7219/src/libraries/SignatureVerification.sol): if the signer has code, it calls `IERC1271.isValidSignature` | **Primary source** | The Permit2 transfer leg accepts contract-wallet signatures. | That IMD's off-chain x402 verifier and its EIP-712 quote approval accept EIP-1271. **[Unknown]** |

Market context (secondary, time-sensitive): IMD ≈ **$8.9** (DexScreener, 23:45 UTC). The ZTO/IMD pool (launch 737) showed about $741k of 24-hour volume and a 3,810 IMD quote-side reserve (`evidence/v3/dexscreener-*.json`). This shows that IMD-paired launch pools do trade and generate claimable fees. I did not reconcile volume against claims.

---

## 3. Corrected measurement window (replaces v2 §2.3–2.4)

### 3.1 Scored interval

- **[Proposal]** The scored interval is **I = [T_open, T_close]**, where T_open = d 12:00:00 UTC is the scheduled `publishAt` for both videos, and T_close = T_open + 48 h.
- The score is **S = C − B**, where:
  - **B** is the baseline at T_open. B = 0 when the video is verified non-public before T_open (§3.2).
  - **C** is the canonical closing value (§3.3).
- The T_open + 15 min read is kept **only as a diagnostic**, and is never subtracted. This corrects v2, which excluded the first 15 minutes of plays.

### 3.2 Opening verification (deterministic)

1. **Pre-open reads.** Both collectors read at T_open − 10 min and T_open − 1 min, in one `batchGetStats` request containing both IDs, with an API key only.
   - **[Inference, calibrate]** A private or scheduled video is absent from `items` or listed in `summary.failedVideoIds`.
   - Absence at both pre-open reads verifies “not public before T_open”, so B = 0.
2. **First public read.** Collectors poll every 30 s from T_open. The first read that contains an ID marks that video's observed go-live time, `g`.
3. **Start symmetry.** The round is valid if, for both videos, `g ∈ [T_open, T_open + 120 s]`.
   - If a video goes live late for platform-side reasons: **no contest** (§4.5).
   - If a team's own scheduling error causes the lateness: **forfeit**.
   - If a video is visible at a pre-open read (published early): **forfeit by that team**. B is not reconstructed.
4. **[Fact]** `batchGetStats` has no status field (E10). v2's “both must be `public`” is replaced by “both present in an unauthenticated response”.
5. **[Unknown]** Whether `snippet.publishTime` records the scheduled time or the actual flip time. It is recorded but not used for scoring until calibration shows which it is.

### 3.3 Closing value: total order over reads

- **Valid read:** HTTP 200, parseable JSON, **both** IDs present with a `viewCount`, and empty `failedVideoIds`.
- **Ordering key:** reads are ordered by `(Date header, collector rank A=0 / B=1, collector sequence number)`.
- **Selection:** C (for both teams together) comes from the **first valid read with Date ≥ T_close and ≤ T_close + 10 min**.
  - Fallback: the **last valid read with Date in [T_close − 10 min, T_close)**.
  - Otherwise the round is **unverifiable** and becomes a no contest.
- Both teams' values always come from the **same response**. No value is ever interpolated or reconstructed from a later read (v2 rule kept).
- **Cadence:** collectors read every 60 s over [T_close − 15 min, T_close + 15 min], so each side of the cutoff has about 10 candidates.

### 3.4 Missing and anomalous data

| Case | Rule |
|---|---|
| One ID missing from a response | That read is invalid for both teams. Use the next read in order. |
| A counter falls between consecutive valid reads by more than 1% + 20 | Flag it. Use the selected read as is, and attach the flag to the oracle question. |
| A collector is down | The other collector's reads are used under the same ordering. Both down for the whole closing window → unverifiable. |
| A and B both have a primary-window read and disagree on the winner, or differ by more than 2% + 50 | Dispute (v2 rule). |
| Video deleted, made private, or changed owner before T_close | Team-side → forfeit. Platform-side (strike or takedown) → no contest. |

### 3.5 Response time vs counter freshness

- **[Fact]** The HTTP `Date` header is when Google's front end produced the response, at 1-second resolution. The response carries no timestamp for when `viewCount` was last computed (E10).
- **[Inference]** C is therefore defined as “the count YouTube reported in the first response at or after T_close”, **not** “plays up to T_close”. The `etag` changes when the response content changes, so it can show a value is unchanged, but its semantics are undocumented.
- **[Proposal] Calibration (C1–C3):**
  - poll every 30 s for 2 h around T_open and T_close;
  - record the interval between observed value changes per video;
  - publish its median and 95th percentile (`u95`).
- **[Proposal] Draw band:**

  ```
  |S_red − S_blue| ≤ max(1% · max(S), 100, r · u95)
  ```

  where `r` is the larger video's average plays per second over the last hour before T_close. Staleness then cannot flip a close result.

---

## 4. Corrected treasury and allocation (replaces v2 §4.5 and §6 item 4)

### 4.1 What the treasury receives

- **[Fact, E5/E11]** In each pool, each trade pays 1.25% of its **input**:
  - buys pay in IMD;
  - sells pay in the team token.
- **[Fact]** 80% of that fee reaches the requester.
- Per fee period the treasury therefore receives three currencies:
  - IMD (from both pools' buys);
  - RED (from RED sells);
  - BLUE (from BLUE sells).
- **[Proposal] Mandatory configuration:** both launches are paid **from the treasury wallet**, so that it is the fee recipient. If V2 (§6) fails for a contract wallet, see the fallback in V2.

### 4.2 Ledger states (accrued ≠ claimed ≠ spendable)

| State | Definition | Where it sits | How it is measured |
|---|---|---|---|
| **Accrued** | The fee earned by the factory's position but not yet collected. It includes the 20% network part. | Inside `PoolManager`, owned by nobody yet | **[Proposal]** Replay `Swap` events for the pool. The fee is `fee/1e6` of each swap's gross input, attributed to the factory position while it is the only in-range liquidity (V5). The treasury's part is 80% of that. |
| **Claimed** | Received by the treasury through `claimFees`, by anyone, at any time (E5) | Treasury wallet, per currency | Factory payment events (`0x212133fc`) to the treasury address |
| **Allocated** | Claimed funds assigned to a fee period, and split into an **operations reserve** and that period's **round burn budget** | Sub-ledger. Two wallets are recommended: ops and burn. | Ledger entries keyed by period |
| **Spendable operating funds** | The operations reserve held in the currency of the expense, net of committed obligations | Ops wallet | IMD is spendable directly on IMD actions (0.5 IMD each). Cash costs require selling IMD (e.g. the IMD/USDC pool). The pool fee and gas are expenses. |
| **Executed** | Burned (sent to `0x…dEaD`) or spent | Dead address, or a payee | Transaction hashes, published per round |

- **Valuation rule [Proposal]:** each fee unit is valued in IMD **at the execution price of the swap that paid it**, which is IMD out divided by tokens in, from the same `Swap` event.
  - This is deterministic and replayable.
  - Manipulating it would require trading at a bad price, which pays the pool fee to the treasury.
- **Operating share [Proposal; restores the economic model]:** `ops_n = 20% × (IMD_n + value(RED_n) + value(BLUE_n))`.
  - It is taken **from IMD receipts first**, then in kind if IMD falls short.
  - Taking it in IMD avoids selling team tokens to pay costs.
  - In value terms it is identical to 20% of each currency.

### 4.3 Allocation rule and alternatives

**[Proposal] v2.1 canonical (B).** For fee period F_n assigned to round R_n with winner W and loser L:

1. Operations take `ops_n` (§4.2).
2. W-token receipts are **burned in kind**.
3. L-token receipts are **sold into the L/IMD pool for IMD**.
4. All remaining IMD (the IMD receipts minus `ops_n`, plus the sale proceeds) **buys W and the bought W is burned**.
5. The price-impact cap and tranching rules of v2 §4.4 apply to steps 3 and 4.

| Option | What happens | Status |
|---|---|---|
| **A. Convert everything to IMD first, then allocate** | Sell W and L receipts for IMD, take 20%, buy W, burn | **Faithful to the rule.** It costs an extra round trip on the W receipts. In the example it burns **0.4–0.7% fewer** W tokens than B. |
| **B. v2.1 canonical** | As above | **Faithful.** The burn of W receipts is value-equivalent to selling and rebuying them, minus costs. **Sponsor to confirm** that an in-kind burn counts as “buy-and-burn”. Otherwise use A. |
| C. v2 §4.5: escrow L receipts until L wins; ops only on IMD | — | **Product change.** It funds the loser, and operations get about 11% instead of 20%. Rejected. |
| D. Each pool's token fees burn its own token | — | **Product change.** The loser gets supply reduction. |
| E. Draw → burn both 50/50 | — | **Product change.** It funds a non-winner. See §4.5 for the roll-forward rule. |

### 4.4 Conversion costs and price impact

**Pool model [Inference from E3].** The single-sided position runs from the opening price to the minimum tick, so each pool trades as a constant-product curve:

- virtual IMD reserve `x = 2,000 + net IMD bought so far`, where 2,000 = 800M pooled tokens × the opening price of 2.5×10⁻⁶ IMD;
- token reserve `y = k/x`.

**Real IMD depth is only what buyers have put in.**

**Costs of converting L receipts, per round:**

- the 1.25% pool fee. **[Inference]** 80% of this fee, paid in L, comes back to the treasury in the next period, where it is allocated to *that* period's winner. Net system leakage is 0.25%;
- price impact;
- gas for a swap. Swap gas is **[Assumption]** 150k–250k. Observed claim gas was 149k–304k, which is ≈ $0.10–$1.10 at today's 0.26–1.33 gwei. At 20 gwei, 300k gas ≈ 0.006 ETH ≈ $16.

**Modelled impact** (`evidence/v3/funds-flow-model-output.txt`):

| Sale of L receipts, as a share of L's *real* IMD reserve | Real reserve 200 IMD | Real reserve 1,000 IMD |
|---|---|---|
| 1% | spot −0.18%, effective −1.34% | spot −0.66%, effective −1.57% |
| 5% | −0.89% / −1.69% | −3.21% / −2.85% |
| 10% | −1.77% / −2.13% | −6.27% / −4.40% |
| 25% | −4.34% / −3.42% | −14.6% / −8.76% |

“Effective” is the received price versus spot, including the 1.25% fee.

**Rules [Proposal]:**

- convert L receipts in tranches of at most the size that moves L's spot by 2%, at least 1 hour apart;
- skip any execution whose expected gas exceeds 2% of the tranche value, and batch it into the next period, still earmarked to the same round;
- use a private transaction route against front-running. Which route is **[Unknown]**: to be selected.

**[Inference]** Selling L receipts pushes the loser's price down. That pressure is inherent in the original rule, which v2 §4.5 hid. At normal sizes it is about 1 period of L's own sell fees, which is small relative to L's sell volume.

### 4.5 Fee periods and round assignment

1. **Periods.** `F_n` = all blocks with timestamp in **[D_n 12:00:00, D_{n+1} 12:00:00) UTC**. They are half-open and non-overlapping. Each block belongs to exactly one period.
2. **Assignment.** `F_n → R_n`: the 24-hour fee period that starts at a round's T_open belongs to that round, and only that round.
   - Pre-season fees, from launch to D1 12:00, form `F_0` and are assigned to **R1**.
   - Fees from D28 12:00 onward form `F_post` and are assigned to the **next season's R1**.
3. **Delayed or third-party claims.** Assignment follows the **accrual block** (§4.2), never the claim time.
   - A claim covering several periods is split by the replayed accruals.
   - Any rounding residue (claimed minus replayed) goes to the latest period in the claim.
   - The settlement executor calls `claimFees` itself if a settled period is still unclaimed.
4. **Draw or no contest.** R_n's budget **rolls forward** to the next round in the same season that produces a winner. It is added to that round's own budget.
5. **Forfeit.** If one team forfeits, the other team is the winner of R_n's budget. If both forfeit, it is a no contest.
6. **Unused buyback budget** (from the price-impact cap, failed transactions or the gas skip). It stays **earmarked to the same round and winner** and is executed in later tranches. It is never reassigned to the other team. Anything still unexecuted 7 days after season end is reported each day until done.
7. **Season end.**
   - Roll-forward balances with no later decisive round in the season go to the **season winner**: the most rounds won, with a tie broken by the last decided round.
   - **Operations-reserve surplus** above 30 days of forecast operating costs is moved to the burn budget of the next decisive round. This follows from “ALL remaining funds” (v1 brief).
   - Dust below 0.01 IMD-equivalent carries forward.
8. **Disputes.** The budget waits in *Allocated* until the attestation's dispute window closes (v2 §2.6). It is executed only on a final result.

### 4.6 Updated funds-flow example (one period, RED wins)

These are illustrative inputs from `scripts/funds_flow_v21.py`. Before the period:

- RED has 3,000 IMD of net buys (virtual x = 5,000; price 1.56×10⁻⁵ IMD);
- BLUE has 1,000 IMD (x = 3,000; price 5.63×10⁻⁶ IMD).

Period trading: RED pool buys 700 / sells 500 IMD-equivalent; BLUE pool buys 400 / sells 300. Combined 1,900 IMD-equivalent (≈ $17k at $8.9).

| Step | IMD | RED | BLUE |
|---|---:|---:|---:|
| Pool LP fees (1.25% of inputs) | 13.75 | 380,201 | 637,887 |
| Network 20% | −2.75 | −76,040 | −127,577 |
| **Claimed by treasury (80%)** | **11.00** | **304,161** | **510,310** |
| Value in IMD (execution prices; end spot shown) | 11.00 | 5.14 | 3.07 |

Total receipts are **19.21 IMD-equivalent**, which is 1.01% of volume.

| Allocation | Amount |
|---|---|
| Operations (20% of all) | **3.84 IMD**, taken from IMD receipts. Under the v2 rule this would be 2.20 IMD (11.5%). |
| Sell 510,310 BLUE (loser) | → 3.02 IMD. BLUE spot −0.20%; effective −1.35% vs spot. |
| Buy RED with 11.00 − 3.84 + 3.02 = **10.18 IMD** | → 593,897 RED. RED spot +0.39%. |
| Burn | 304,161 RED in kind + 593,897 bought = **898,058 RED to `0x…dEaD`** (≈ 15.18 IMD at spot) |
| Option A (convert all first) instead | 891,805 RED burned (−0.70%) |
| Option C (v2 §4.5) instead | 817,531 RED burned, and 510,310 BLUE escrowed for BLUE's next win (product change) |
| Feedback into F_{n+1} | The buyback pays 0.127 IMD in fees, and the BLUE sale pays 6,379 BLUE. 80% of each returns as next-period receipts. |

If **BLUE wins** instead: 304,161 RED are sold for 5.07 IMD, and 12.23 IMD buys 2,002,694 BLUE. With 510,310 BLUE burned in kind, **2,513,003 BLUE** are burned (A: −0.36%).

### 4.7 Effect on the v2 sustainability numbers

- v2's cash-only break-even of **$32,500/day** holds only under the v2.1 rule (20% of all receipts).
- **[Inference]** Under v2 §4.5, operations would receive about 11–12% of receipts in a market where buys and sells balance. That puts break-even near **$55,000–$60,000/day**.
- Cash costs also need IMD→USD conversion: the pool fee plus gas, which is small at current gas prices.
- Use IMD at ≈$8.9 (not $9.14) for re-pricing. 54.5 IMD ≈ $485.

---

## 5. Corrected vote-weight rule (replaces the token-pilot row of v2 §7)

- **[Inference]** A minimum over 7 daily snapshot blocks proves the address held at least *m* at **7 instants**. It does not prove that it held *m* between them. Exposures:
  - **Predictable-snapshot borrowing.** The snapshot block is “first block after 00:00”, and transfers are untaxed (E1). A cooperating holder can lend tokens to a voter just before each snapshot and take them back after, for gas only.
    - The lender's own weight falls by the same amount, so this **moves** weight rather than creating it.
    - It does let weight be rented while the economic exposure stays with someone else.
  - **Buy before / sell after each snapshot.** This costs about 2 × 1.25% plus price impact per snapshot, and v2's daily rule makes the timing known in advance.
  - **Flash loans** cannot change an end-of-block balance. A buy and a sell in adjacent blocks can.
  - **[Fact, E8]** The tokens have no checkpoints (`getPastVotes`), so on-chain historical voting power is not available.
- **[Proposal] v2.1 rule:**
  - weight = **the exact minimum balance over the whole window** [first block ≥ window start, last block < vote close];
  - it is computed by replaying every `Transfer` event of the token from the launch block. **[Inference]** An OpenZeppelin-style ERC-20 emits `Transfer` on every balance change, and V9 tests this;
  - any dip, even for one block, lowers the weight;
  - the 7 daily snapshot reads are kept as a cross-check, so that a replay bug is caught;
  - exclusions as in v2, plus `0x…dEaD`, the factory, the treasury and the ops wallet.
- **Residual risk (stated, not solved):**
  - anyone can still rent tokens for the *entire* window;
  - **[Unknown]** whether a lending market will list RED or BLUE. Check before each vote, and publish a concentration report (top-10 share), as v2 required.

---

## 6. Minimal validation checklist (ordered by what decides go/no-go)

Every check is read-only or uses spending already in the v2 budget. Nothing here requires a deployment by this project before Gate C.

| # | Check | Method | Pass | Fail → consequence | Status today |
|---|---|---|---|---|---|
| **V1** | Fee currency and split | Decode factory `claimFees` receipts (E5) | Both pool currencies paid; 80/20 in each, ±1 wei | — | **PASS** for `custom_token` launches: 27/27 |
| **V2** | Treasury wallet can be the payer and fee recipient | Pay one budgeted 0.5 IMD action (e.g. A1) from the intended multisig on mainnet. Read `GET /requests/paid-by/<multisig>`. | Order `paid`, payer = the multisig | Fallback: a dedicated EOA pays, and a per-period sweep to the multisig is published. Key-custody risk is recorded. | **Not run**. All observed recipients are EOAs. |
| **V3** | The launch kind for RED/BLUE uses this fee path | Before paying: `/requests/check` for the exact final inputs (E1 shows facts only). After launch: one claim. | `token_trading_fee` fact unchanged, no chain/policy blockers; the first `claimFees(n)` pays IMD + RED to the treasury | Choose the kind with demonstrated claims (`custom_token`), or hold. | Dry-run **PASS** (facts only); execution **not demonstrated** for `evm_project` and `univ4_hook` |
| **V4** | Parameter stability | Read LaunchFees `feeRecipient`, `0xcd26a197()`, `owner` at each period close; watch for setter transactions | Requester share stays 8000 bps | Pause allocation; recompute the model. | Requester share 8000 today. **Network recipient already changed once** (E7). |
| **V5** | No LP dilution | For each pool, list `ModifyLiquidity` senders each period | Only the factory has in-range liquidity | Accrual replay switches to `feeGrowthInside` via v4 [StateView](https://github.com/Uniswap/v4-periphery/blob/9969eec44cfdf07e24b41de47f40276a58401976/src/lens/StateView.sol). The treasury share falls below 1%, so update §4.7. | **PASS** for pools 737, 812 and 740 today |
| **V6** | Accrual replay reconciles with claims | Replay `Swap` events between two claims of an existing IMD-paired pool (e.g. launch 737) | Replayed 80% fees = claimed amounts, within 0.01% per currency | The period-assignment rule (§4.5.3) cannot be executed as written. | **Not run**. Free, and the next thing to do. |
| **V7** | End-to-end on the real pools (post Gate C) | One small buy and one small sell on each of RED/IMD and BLUE/IMD, then `claimFees` | Treasury receives IMD + RED (and IMD + BLUE) = 1% of each input, ±rounding | Stop before the first scored round. | Pending launch |
| **V8** | Burn path | Send 1 bought RED to `0x…dEaD`; read balances | Dead balance increases; dashboards report circulating = total − dead | — | **[Inference]** Will pass. Plain `transfer`. |
| **V9** | Transfer-log completeness (voting) | Compare the Transfer-replay balance with `balanceOf` at 7 random blocks, for 20 holders | 100% equal | Fall back to snapshot reads, and label the residual risk. | Not run |
| **V10** | Measurement calibration (§3.2–3.5) | Run in C1–C3 | Pre-open absence observed; both `g` within 120 s; `u95` published; 0 invalid closes | No scored rounds until it passes | Not run (Gate A) |

**Priority:** V1 → V6 → V2 → V3 → V4/V5 determine whether the two-token, winner-funded burn can operate. V7–V10 confirm execution.

---

## 7. What is known, inferred, uncertain and unanswered

- **Facts established in this revision:**
  - mixed-currency fee receipts with an exact 80/20 split, and permissionless push-based claims, on the mainnet factory (E3–E6);
  - a static 1.25% pool fee (E4);
  - a network recipient that its owner can change, and has changed (E7);
  - tokens without `burn` or checkpoints (E8);
  - Sepolia cannot pair with IMD (E2);
  - `batchGetStats` has no status or freshness field (E10).
- **Inferences:**
  - the constant-product virtual-reserve model and its price-impact figures;
  - `setPoolFee` affects only future pools;
  - the 8000 getter is the requester share, with no setter;
  - third-party LP dilution is possible;
  - Transfer-replay completeness.
- **Uncertainties:**
  - the LaunchFees and factory **source is unverified**, so their behaviour is known only from executions and selectors;
  - counter staleness on YouTube;
  - what `publishTime` means;
  - gas prices and IMD price.
- **Unanswered questions:**
  - Can the requester (fee recipient) be a contract wallet? Can it be changed after launch?
  - Do `evm_project` and `univ4_hook` launches route through the same `claimFees`?
  - What do `owed()` and `withdraw()` do when a push fails?
  - Will lending markets list RED or BLUE?
  - Does the sponsor accept an in-kind burn of winner receipts (Option B), or require literal conversion (Option A)?
  - Legal treatment of the buybacks (unchanged from v2).

## 8. Sources

- **IMD:**
  - [API docs](https://imd.fun/docs/) (Launches: “Trading fee … 1.25% of every trade …, 1% to the paying wallet and 0.25% to the network. Anyone can call the distribution.”);
  - [`/launch/policies`](https://api.imd.fun/launch/policies);
  - [`/requests/capabilities`](https://api.imd.fun/requests/capabilities);
  - `POST /requests/check` (archived);
  - launch records [737](https://api.imd.fun/launches/030c609a-ae99-4a2b-9950-2941535ab63d), [812](https://api.imd.fun/launches/0a98bce4-2d50-4d55-ac93-81805c792de7), [829](https://api.imd.fun/launches/4b6fade4-991e-4b19-9745-bcdbf93f382b), [825](https://api.imd.fun/launches/3ded72c6-510b-490c-a6ae-ac8b21704a7f).
- **On chain (Ethereum mainnet):**
  - factory [`0xff03…7120`](https://eth.blockscout.com/address/0xff03410d0fe5fa8f7f59f743de35e333d9857120);
  - LaunchFees [`0x12c9…3863`](https://eth.blockscout.com/address/0x12c9e1007262afac205567457f5826a9416a3863);
  - LaunchRegistry [`0x7c9d…fe23`](https://eth.blockscout.com/address/0x7c9d5ee697bff5ac4f10e2e54d3f40c44e48fe23) (verified);
  - PoolManager `0x0000…8a90`;
  - the 27 claim transactions are listed in `evidence/v3/onchain-launchfees-claims.json`.
- **Uniswap:**
  - v4-core @ `46c6834` (SwapMath, LPFeeLibrary, Hooks, PoolManager, IPoolManager);
  - v4-periphery StateView @ `9969eec`;
  - Permit2 SignatureVerification @ `cc56ad0`.
- **YouTube:**
  - [videos.batchGetStats](https://developers.google.com/youtube/v3/docs/videos/batchGetStats) (updated 2026-09-14);
  - [videos resource](https://developers.google.com/youtube/v3/docs/videos) (updated 2026-09-16; `viewCount` counts from when a video “begins to play (includes autoplay …)” from 24 Aug 2026).
- **Market (secondary):** DexScreener IMD, read at 23:45 UTC on 6 Oct 2026 through its [API](https://api.dexscreener.com/latest/dex/tokens/0xd34a99bc0f67ae1bbd63c660e6d0b0dd03e263b7). The web page refuses scripted reads; responses are archived in `evidence/v3/dexscreener-*.json`.

*Limits: this is a desk review by one contributor using public reads only. No credential was used, and nothing was paid, signed or deployed. The fee contracts' source is unverified. No independent reviewer has checked this revision.*
