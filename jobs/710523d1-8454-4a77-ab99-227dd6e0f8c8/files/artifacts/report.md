# Five market-fed tokens invented by the IMD swarm

Research date: 9 October 2026 UTC. Assignment: original candidate research only; no launches, votes, payments, signatures, or deployments were performed. **Recommendation (inference): prototype NAP Engine first; use Ash Weather as the strongest visual alternative.** All five have an immutable market core and a swarm that improves the surrounding experience every 12 hours when funded.

**Material finding:** the current IMD API supports scheduled jobs, but its Ethereum Intake does not sell schedule creation, schedule top-ups, or jobs. Consequently these are launch concepts with an explicitly described automated relay dependency, not claims that completely contract-funded, self-deploying heartbeat tokens work today. Funding and deployment gaps apply to every candidate.

Labels throughout: **Fact** means a linked source or retained API response supports the statement; **Proposal** is our design; **Inference** is our interpretation; **Unknown** is unresolved. “Viral” here means a design intended to create recurring, publicly shareable moments; adoption is never guaranteed. Originality refers to the combinations proposed here, not a verified worldwide trademark or prior-art search.

## 2025–2026: evidence worth borrowing

| Pattern and evidence | What the evidence establishes | Our design inference |
| --- | --- | --- |
| **Attention shocks, January 2025.** CoinGecko reported TRUMP reached a $14.5 billion peak circulating market capitalization in just over 24 hours. Its Q1 report records a 72,000-token daily Pump.fun launch peak, followed by a 56.3% decline in daily deployments after LIBRA. [CoinGecko January analysis](https://www.coingecko.com/research/publications/bobbys-crypto-aggregate-2025-01), [Q1 report](https://www.coingecko.com/research/publications/2025-q1-crypto-report). | A simple shared event can attract enormous attention; that attention can disappear. Market cap is not money deposited or obtainable exit liquidity. | Give people a repeatable event to share, rather than depend on a celebrity launch. Do not reward churn with monetary prizes. |
| **NFT characters became games in 2025.** Pudgy Penguins' issuer announcement dates Pudgy Party's global launch to 29 August 2025. The team later reported more than one million downloads. [Issuer launch release](https://www.prnewswire.com/news-releases/pudgy-penguins-and-mythical-games-announce-global-launch-of-pudgy-party-302540201.html), [Pudgy Penguins' milestone post](https://www.linkedin.com/posts/pudgy-penguins_pudgy-party-surpasses-1-million-downloads-activity-7404206953574420480-evYN). | A recognizable NFT character can travel into a casual game. Downloads are self-reported reach, not token holders, paying users, or retention. The milestone post has a relative date; do not infer an exact milestone day from it. | A pet, weather scene, or communal object can be enjoyable before someone buys the token. Make spectator mode free. |
| **Participation increased while NFT dollar volume fell.** DappRadar's Q2 2025 report records 14.9 million NFT sales, up 78%, while dollar volume fell 45% to $867 million. [DappRadar Q2 report](https://dappradar.com/blog/state-of-the-dapp-industry-q2-2025). | Its tracked market showed more sales at lower aggregate value. Wallets and sales are not unique people; this is not universal NFT coverage. | Small, legible participation receipts fit better than a new expensive NFT mint or perpetual reward emission. |
| **Hooks became usable infrastructure in 2025.** On 14 May the Uniswap Foundation reported more than 700 initialized hooks and v4 accounting for 20–30% of daily volume across Uniswap implementations. [Foundation roadmap](https://www.uniswapfoundation.org/blog/a-roadmap-for-programmable-liquidity). | Meaningful infrastructure adoption, not evidence that a particular hook memecoin went viral. | Put the mechanic in the hook's swap accounting and persistent state, so an ordinary token plus a marketing site cannot reproduce it. |
| **Social agent launches and competitions continued into 2026.** Bankr's primary launch page displayed $5.55 billion total volume and $23.97 million creator fees in the retrieved page. Virtuals' Arena displayed 279 competing agents and a 6 October 2026 refresh timestamp. [Bankr launch dashboard](https://bankr.bot/launches/0xBe50B7b73aA16fC86457359cb4BE62EaaB120Ba3), [Virtuals Arena](https://degen.virtuals.io/). Bankr documents social token launching; its dated 2025 manifesto described launching BNKR through Clanker. [Bankr overview](https://docs.bankr.bot/token-launching/overview/), [2025 manifesto](https://bankr.bot/bankr-manifesto.pdf). | First-party displayed scale and a public agent competition. Figures are dynamic, potentially aggregated, and not independently reconciled here. Trading agents do not establish a self-improving token's safety. | Publish changes and results as an observable season; let people watch agent decisions without giving agents trading custody. |
| **Persistent AI stories were proposed in 2025.** In OpenSea's interview, Doodles founder Scott Martin described DreamNet as an AI avatar/story platform powered by DOOD. [Founder interview](https://opensea.io/blog/articles/in-conversation-with-burnt-toast-of-doodles). | A primary statement of product direction; no usage or proof of successful autonomous execution is supplied by that interview. | Persistent consequences are more interesting than unconnected AI posts. Keep exact market history and reproducible visuals. |
| **Burns became infrastructure narratives.** Uniswap's 10 November 2025 UNIfication proposal described fee-driven UNI burning and a proposed 100 million UNI treasury burn. [UNIfication proposal](https://blog.uniswap.org/unification). IMD's own POOL4 documentation describes an ETH/IMD v4 pool and capped inventory retirement, but also discloses owner powers and unaudited experimental status. [POOL4 docs](https://pool4.imd.fun/docs). | Published designs, with different trust assumptions; neither proves our proposed tokens' virality. UNIfication is cited as a proposal, not as independently verified execution. | Make a sacrifice produce a visible artifact, and distinguish circulating retirement from an ERC-20 supply reduction. Do not import POOL4's owner escape hatches into these immutable market cores. |

**Oracle-judged mechanics: evidence gap.** We verified IMD's typed agent-panel interface, not a proven viral 2025–2026 token whose success was caused by agent judging. Candidate 3 is an experiment in that category. Popularity of prediction markets does not, by itself, validate subjective AI judgments.

**What IMD uniquely contributes (inference):** the useful differentiator is the combination of a distributed builder swarm, recurring jobs, signed panel answers, hook launch infrastructure, and sites produced from accepted work. None of those ingredients alone is unique to IMD. Together they could let the product explain what it built, why it built it, and what on-chain observations prompted it. The letters make ongoing work visible instead of asking buyers to trust an anonymous roadmap.

## Verified IMD constraints

**Fact — documentation:** schedules accept `job.open` or `oracle.request`; job inputs cannot contain `onchain`. `continue: true` carries forward completed work. Run inputs are frozen. Missed slots are not replayed as a burst. Unused paid runs are not refundable; three failures can pause a schedule. Ordinary contract wallets are unsupported by the HTTP payment flow. Intake's `request(...)` and signed-quote `pay(...)` currently sell only oracle requests. Oracle answers are typed and domain-bound; subjective panel evidence is distinct from reproducible chain evidence. [IMD docs](https://imd.fun/docs/).

**Fact — live catalog:** `/requests/capabilities` lists Ethereum mainnet, `univ4_hook`, ETH pairing, IMD with 18 decimals, and 0.5 IMD per schedule run. The mainnet `onchain.chains[].actions` list contains only `oracle.request@oracle-1`. `/openapi.json` lists HTTP actions including `schedule.create`, `schedule.topup`, and `job.open`; it exposes no separately priced execution-fee field in its action catalog. [Capabilities](https://api.imd.fun/requests/capabilities), [OpenAPI](https://api.imd.fun/openapi.json). Local raw responses are retained.

**Fact — read-only launch policy check:** the retained `/requests/check` response says one billion tokens, 18 decimals, plain transfers, one-time mint; default allocation 10% swarm, 80% pool, 10% requester; opening market cap **10 ETH**; pool fee **1.25%**, comprising 1% to the payer and 0.25% to IMD, with a hook fee additional. It returned `judged: false` and `launch_requires_review`: it establishes displayed policy, not candidate admission. [Read-only check route](https://api.imd.fun/requests/check), [local response](launch-check-snapshot.json).

**Fact — hook reference and standard token:** the current IMD hook reference requires an initialization callback, PoolManager authentication, and static `pool.fee = 12500`. It describes ERC-6909 fee claims as a way to avoid trying to transfer ETH before the first buyer settles. The standard starter token has no public burn or holder-enumeration method. [IMD hook reference](https://api.imd.fun/reads/skill/uniswap-v4-hooks), [standard token source](https://raw.githubusercontent.com/Identity-md/univ4hook-start-template/main/src/LaunchToken.sol). Treat the older starter README's sample cap and fee as test fixtures, not current launch policy.

## Mandatory common design for candidates 1–5

Everything in this section is a **Proposal**, binding on each candidate. Candidate-specific details follow.

### Market, fee routing, and treasury

Each launch requests `onchain: "univ4_hook"`, `chainId: 1`, `pairWith: "eth"`: the standard token, standard pool, and its own immutable custom v4 hook. Opening capitalization is the checked policy's **10 ETH**, with no custom cap override. Preserve the one-billion maximum and the standard allocation; none of the 10% swarm allocation is silently appropriated to pay for heartbeats.

Each custom hook charges a fixed **0.50% of absolute executed ETH-side swap consideration**, excluding its own fee, on buys and sells. This is additional to the policy pool fee. It books **exactly 20% of each hook fee** to its own `HeartbeatTreasury`; the other **80% goes to `0xd01122bBfFd00fc96252c8b29867a5359a3bca13`**, with rounding dust carried so cumulative allocations preserve the split. Rates and destinations have no setters. No prizes, burns, development payments, or oracle games raid the 20% reserve.

The standard pool's payer share must also reach that exact team address. The currently documented route is to make that address the launch's actual paying wallet; do not assume a `feeRecipient` field exists. **Unknown:** whether IMD will sponsor a swarm launch with that payer, or accepts another enforceable routing arrangement. If a different payer is required, this routing requirement needs network support before launch. Supply recipients and the network's policy fee are separate from the team's fee income.

The treasury receives ETH or redeemed ETH claims and converts its reserve through an existing **ETH/IMD pool** into IMD at `0xd34a99bc0f67ae1bbd63c660e6d0b0dd03e263b7`. The candidate's TOKEN/ETH pool cannot itself output IMD. Use a separately validated ETH/IMD route: verify the full PoolKey, hook behavior, liquidity and executable price before configuring it. POOL4 documents one possible venue, but a documented pool is not a verified safe execution route. We have not established its current best route or trade depth.

`convertReserve()` is permissionless, operates outside the user swap callback, and batches a capped amount under an immutable maximum price deviation of 100 basis points from a sufficiently aged reference and a caller-provided stricter minimum output. A caller may tighten protection, never loosen it. With no trustworthy reference or too little depth it does nothing. Keep ETH pending until a safe conversion is possible; hold acquired IMD solely for heartbeat payments. Failed conversion never blocks token trading. Swapping inside the primary hook would add recursive pool execution and unnecessary trade-failure risk.

Fee claims and all currency deltas must be settled correctly; exact-input/output and both directions need separate accounting. [Uniswap flash accounting](https://developers.uniswap.org/docs/protocols/v4/concepts/flash-accounting), [v4 hooks](https://developers.uniswap.org/docs/protocols/v4/concepts/hooks). The 1.25% pool fee plus 0.50% hook charge is roughly 1.75% before price impact, with the exact quote depending on the fee bases. The treasury receives only about **0.10% of traded ETH consideration**, not 20% of all trading fees.

### Herald: immutable milestones and the swarm's letters

The hook inherits a small herald with this exact event:

```solidity
event Message(address indexed to, string text);
// Every allowed emission sets to = 0x200E710aCAA6A93bbc77146026328C40F1d60fB1.
```

“Writes to” means the recipient is the indexed `to` value in a log emitted by an approved contract. It does not mean calling that address or making logs originate from it. No payable message service or recipient ABI is assumed.

Each hook constructor emits its candidate's short description below, including that the swarm invented it and it won a swarm vote. **Those statements are prospective:** record a real swarm vote and selected candidate before deployment; none has won a vote in this research task. The launch gate rejects deploying a constructor that would falsely claim one.

From `afterSwap`, the hook automatically checks monotonic counters and emits immutable, prewritten milestone strings once each: first trade; cumulative ETH-side volume at 1, 10, 100 and 1,000 ETH; enrolled holder addresses at 10, 100 and 1,000; irreversible retirement at 0.01%, 0.1% and 1% of the original supply; and a small finite ladder of candidate-specific records. A large trade crossing several thresholds consumes at most two pending letters per swap; later swaps flush the remainder. There is no arbitrary public `post(string)` or caller-supplied milestone text. Bots can cause genuine milestones through transactions, but cannot repeat or invent a letter.

**Holder precision:** a standard ERC-20 cannot be globally enumerated by its hook, and router `sender` is not necessarily the trader. Provide optional self-enrollment: the hook verifies the caller's positive token balance, excludes system contracts, and records each address once. Letters explicitly say “100 holder addresses have enrolled,” meaning addresses that held tokens when enrolling, not 100 unique humans or 100 current holders. The site separately reconstructs current nonzero holders from Transfer logs. An exact global holder milestone inside the hook would require a different token interface or a verified external census; that is not claimed here. Enrollment cannot choose text or generate unlimited herald messages.

**Burn precision:** preserve the standard token. Each candidate includes an immutable `RetirementVault` with no withdrawal, approvals, arbitrary calls, upgrade, or delegatecall. Voluntary transfers permanently remove spendability but do **not** reduce `totalSupply()`. The hook reads the vault's token balance itself, including direct transfers, and calls milestones “irreversibly retired,” not supply-reducing burns. True ERC-20 burns would require token support outside the currently inspected standard. Receipt NFTs may be truly burned by their owners; they confer no financial rights. No heartbeat can retire holder funds or its heartbeat IMD.

Every future swarm job ends with a new `Message` describing **what it built and why**, including audit/report jobs and unsuccessful attempted upgrades. An accepted change's immutable letter is embedded in its completion sidecar and emitted through a one-shot, authenticated completion gateway; the gateway admits at most one terminal letter per real job ID and verifies its artifact hash and epoch. Unlike milestone strings, new job letters require authenticated swarm output. **Missing integration:** IMD must define the network-signed completion receipt/authorized delivery path; no current proof that an API “completed” response is directly usable as that receipt is assumed. A failed build gets an honest failure/report letter, never “upgrade shipped.”

The site labels the chronological feed **“the swarm's letters.”** It reads every approved emitter from its deployment block, filters the exact recipient, paginates without dropping old entries, orders by block/transaction/log index, handles reorgs, escapes strings, and links transactions. It includes constructor, milestone and job letters, with pending confirmations marked. Do not trust arbitrary contracts emitting the same event.

### What a 12-hour job may change

Create an IMD job schedule with `cadence: {every: "PT12H"}`, `continue: true`, and a frozen objective that reads the latest on-chain metrics and chooses one bounded improvement. Each run pins its metrics block and logs the evidence hash, candidate action, reason and outcome. Metrics include executed buy/sell ETH volume, fees, settled treasury funds, run credits, retirement totals, enrolled addresses, and the candidate's game counters. A full holder index is ancillary evidence, not a consensus-critical hook input.

The immutable core allows no supply, rate, pool, treasury destination, transfer, allowance, or LP-custody changes. The swarm cannot replace the hook, use a proxy, execute arbitrary calls, seize funds, or infer that “a useful upgrade” grants new authority.

Permitted changes: a static site improvement; a parameter only in the candidate's immutable ranges; or a new opt-in, noncustodial feature instantiated from pre-audited, code-hash-allowlisted templates. Cap activation at one per 12-hour epoch and apply a 12-hour activation delay. Bake a maximum additional job price of 5 IMD per run into the treasury; a more expensive quote is skipped, never approved by raising the cap. The registry stores references and commitments; the market hook never calls new arbitrary feature code during swaps. Parameters are next-epoch and cannot rewrite earlier outcomes. A candidate can still get genuinely new site behavior and new configured sidecar instances without an unbounded core executor.

Every run ships tested artifacts, including a reasoned no-change report when warranted, and its letter. Changes affecting contracts require automated independent network review and bounded activation. **Current deployment limit:** scheduled `job.open` can produce code and site exports, but cannot directly request a launch through its frozen body. An automated deployment/publication handoff is still needed. All upgrade examples below mean one successful funded run each, not six changes shipped simultaneously or guaranteed three-day delivery.

## Heartbeat funding: what works today and what is missing

### Can the treasury pay through Intake?

**Fact:** as retrieved, Ethereum Intake is `0x1397434cd35e8a9c8ac312a61d3a285eb31dea56`. The only action in the live Ethereum on-chain list is `oracle.request`; the OpenAPI's HTTP action catalog additionally contains schedules and jobs. The docs restrict signed-quote settlement to on-chain-sold actions. **Conclusion:** a contract cannot currently pay `schedule.topup`, `schedule.create`, or the job price through that Intake. Increasing the amount of an oracle payment does not create job credits. A token transfer to the service payee alone is not a schedule admission.

### Closest working automated path

1. At an eventual launch, an automated relay EOA creates a `job.open` schedule over HTTP with the fixed objective and PT12H cadence. No human chooses future features. Seed funding, if any, must be transparently launch-funded or donated; no invented balance is assumed.
2. A public `fundNextRuns()` checks settled IMD, outstanding liabilities and the next unpaid slot. Insufficient balance emits a fixed funding-status event once for that slot and skips it, never borrowing or taking holder principal. Enough balance opens a one-run capped funding intent. It cannot truthfully report an on-chain top-up today.
3. A dedicated machine relay receives at most one run's capped IMD allocation, uses the required EOA payment signatures to buy `schedule.topup` over HTTP, and records the order/schedule result. It can do this with no human per run, but it is a funded signing service. It must be the appropriate project/schedule payer for continuation and use idempotent request keys.
4. The relay coordinates accepted artifacts, publication, optional template deployment and the terminal letter. It waits for terminal outcome before starting another version. If a job is still running at the next 12-hour slot, skip instead of launching competing edits.

**Trust cost:** the relay briefly controls that run's IMD and pays gas. Current contract logic cannot authenticate an HTTP top-up or make relay payment/refund atomic. A dishonest relay can lose its capped allocation; a dead relay stops upgrades. Funding intents use a fixed relay destination, one outstanding allocation, and one allocation per 12-hour slot; arbitrary callers cannot choose a recipient or drain several slots early. A timeout prevents another allocation until the failed intent is resolved. Keepers remain permissionless, but permissionless invocation is not guaranteed gas-paying execution. This path is automated operation with a bounded custodian, not full contract-only autonomy. Workers never receive or hold the relay key.

**Exact missing pieces for full intended autonomy:** enable schedule/job actions in Intake, including contract-owned schedule identity and continuation; provide on-chain admission/run-credit receipts and an execution-price/budget API; authorize bounded automatic deployment/site publication from scheduled artifacts; provide authenticated job-completion letters; establish a safe ETH/IMD conversion route and sustainable keeper/relay gas funding; satisfy the team/payer routing condition. Then `fundNextRuns()` could atomically approve only the precise price, purchase credits and mark the funding intent paid, without handing IMD to an EOA. None of these additions is presented as already implemented.

The 20% treasury may spend IMD only for heartbeat runs and their job price. Oracle gameplay has a separate sponsor budget; gas comes from a separately disclosed ETH operations reserve or keeper sponsorship. No “IMD-only reserve” silently pays arbitrary development contractors or keeper incentives.

### Daily volume math (identical for all five)

Let `V` be daily fee-bearing ETH-side volume in ETH; `h = 0.005` the fixed hook rate; `r = 0.20`; `p` the achieved ETH cost of one IMD before conversion costs; `η` the realized conversion fraction after route fees and slippage; `J` the additional job price in IMD per heartbeat; and `G` daily keeper/relay/deployment gas cost in ETH.

```text
Heartbeat ETH accrued/day = V × h × r = 0.001 V
IMD acquired/day          = 0.001 V × η / p
Cost of two runs/day      = 2 × (0.5 + J) IMD
Required V               = 2 × (0.5 + J) × p / (0.001 × η)
                         = 1,000 × (1 + 2J) × p / η  ETH/day
```

**Price uncertainty:** IMD's inspected catalog names 0.5 IMD as admission/per-run pricing, but we did not verify an additional execution charge. The requester asks to budget “plus the job price,” so `J` is explicit. Do not automatically add the HTTP `job.open` admission price a second time to a schedule's included opening. Use `J = 0` if the schedule price includes the work; otherwise use the network's actual future execution quote. No exact break-even can be known until `p`, `J`, conversion costs and gas sponsorship are known.

**Illustrative assumptions, not live prices:** `p = 0.001 ETH/IMD`, `η = 0.98`, `J = 0.5 IMD/run`, sponsored gas. A 12-hour run costs 1 IMD; a day costs 2 IMD. Required daily volume is **2.040816 ETH**. At an illustrative ETH price of $3,000, that is **$6,122.45/day**. With the same conversion assumptions but `J = 0`, the threshold halves to **1.020408 ETH/day**.

| Daily traded ETH (`V`) | IMD acquired/day at illustrative assumptions | Long-run funded runs/day at 1 IMD/run | Behavior with no starting buffer |
| --- | --- | --- | --- |
| 0 | 0 | 0 | Freeze improvements; market, existing game rules and site history remain usable. |
| 0.5 | 0.49 | 0.49 | Roughly one funded slot every 2.04 days; intervening slots skipped. |
| 1 | 0.98 | 0.98 | Approximately one run/day; no promise of both daily slots. |
| 2.040816… | 2 | 2 | Exactly funds two runs/day in the modeled steady state. |
| 5 | 4.9 | Maximum 2 scheduled runs | Save the surplus as future heartbeat runway; no extra cadence. |

Fractions are steady-state averages, not partial runs. The keeper buys integer credits only after a full run is affordable and never backfills skipped slots. Existing prepaid credits may continue during low volume, but once both credits and reserve run out, the token sleeps. Runway is `(available IMD + prepaid-credit value) / actual daily IMD cost`, with outstanding allocations deducted.

If these same revenues must indirectly also sustain gas sponsorship, total economic break-even becomes `V ≥ [2(0.5+J)p/η + G] / 0.001`; this does **not** authorize spending the earmarked IMD on gas. At illustrative `G = 0.002 ETH/day`, the requirement rises to **4.040816 ETH/day**, and a lawful separate ETH funding source is still needed. This is why honest low-volume dormancy is part of each product.

## 1. NAP Engine — NAP

**One-line hook:** a market-fed digital pet gets a new skill every funded heartbeat and visibly naps when its upgrade budget dries up.

**Launch:** standard token; `univ4_hook`; Ethereum mainnet; ETH pair; policy cap 10 ETH; fixed 0.50% hook fee split 20% heartbeat / 80% exact team address, plus policy fees as specified above.

**Mechanic (proposal):** the hook records ETH buy/sell flow and seals a 12-hour food meter. Food is a bounded display score from fee-bearing volume, not a payout or a permission to mint. A day’s activity changes the pet's immutable base mood: sleepy, curious, or energetic. Only an authenticated completed upgrade advances its learned-skill counter. The pet never pretends that volume alone bought a delivered feature. No trading gate, forced holding period or special allowance is needed.

**Heartbeat bounds:** one lesson, site improvement or noncustodial sidecar per epoch; visual frame count 4–32 and animation period 2–20 seconds; no changes to financial rates. When unfunded, existing skills remain playable and the pet's clock shows the skipped slot.

**First six funded upgrades and their terminal letters:**

1. Build a chain-backed feeding timeline. `Message`: “Built the feeding timeline so you can see what funds each lesson.”
2. Ship a tiny browser memory game using the pet's last sealed food score. “Built a memory game so the pet has something useful to learn.”
3. Add a nontransferable lesson receipt through an allowed template. “Built lesson receipts so early caretakers can keep their history.”
4. Add a replay comparing the pet's mood with actual buy/sell flow. “Built mood replays so its reactions can be checked.”
5. Add a transparent runway calculator. “Built the runway view so nobody mistakes sleep for abandonment.”
6. Ship a second game module selected by measured completion rates. “Built a second lesson because players finished the first one.”

**Why people share it (inference):** “Our token learned this overnight” is a concrete clip, and visible napping creates an honest recurring character rather than a perpetual hype promise. Free games let spectators join without buying. Compare game completion and artifact shares, not token price, when selecting lessons.

**Constructor letter:** “NAP Engine is a market-fed pet. Invented by the swarm; it won a swarm vote.” **Automatic record letter:** “The pet has learned six lessons.” Only verified job completions count toward it.

**Failure mode:** wash volume can manipulate mood; mood has no economic rewards. A missing relay stops lessons, not swaps. The pet must display funded, running, shipped and asleep as different states.

## 2. Ash Weather — ASHW

**One-line hook:** every trade paints weather; irreversible token retirement reveals constellations that the swarm turns into a growing sky.

**Launch:** standard token; `univ4_hook`; Ethereum mainnet; ETH pair; policy cap 10 ETH; common immutable 0.50% fee and exact fee destinations.

**Mechanic (proposal):** `afterSwap` records buy and sell ETH buckets; their bounded ratio maps to sunny, rainy or stormy weather. The hook reads its fixed RetirementVault balance and unlocks immutable constellation tiers at predetermined retired-supply thresholds. All scenes are reproducible from sealed counters. Retirement is optional, permanent and confers no profit claim; the standard `totalSupply()` stays unchanged.

**Heartbeat bounds:** one new rendering tool, scene or opt-in constellation receipt per epoch; palettes have 2–16 colors and weather contrast 10–90%. Unlock thresholds, retirement destination, mint ceiling and fee rates are immutable. No buybacks from heartbeat money.

**First six funded upgrades and letters:**

1. Build the deterministic sky renderer. “Built the sky renderer so every weather scene can be reproduced.”
2. Add a retirement-proof page. “Built retirement proofs so constellations cannot hide fake burns.”
3. Add a timelapse of sealed weather epochs. “Built sky timelapses so the market leaves a visible history.”
4. Instantiate a nonfinancial constellation-receipt template. “Built constellation receipts so voluntary sacrifices have a keepsake.”
5. Add a supply-versus-retirement chart. “Built the supply chart so retirement is never confused with mint destruction.”
6. Ship an exportable monthly atlas. “Built the atlas so anyone can share the sky without trading.”

**Why people share it (inference):** coordinated constellation reveals and beautiful, transaction-reproducible timelapses turn dry accounting into a social object. Original art avoids borrowing an established NFT mascot.

**Constructor letter:** “Ash Weather turns trades and retirement into skies. Invented by the swarm; it won a swarm vote.” **Automatic record letter:** “One percent of the original supply is irreversibly retired.”

**Failure mode:** irreversible sacrifice is expensive and reversible hype is easy. Show the exact vault permanence and unchanged total supply prominently. The sky works with zero retirement; nobody needs to burn to watch.

## 3. Tiny Court — TCRT

**One-line hook:** the pool sets a tiny courtroom's mood, and an IMD agent jury judges playful, precommitted cases without controlling trading or holder funds.

**Launch:** standard token; `univ4_hook`; Ethereum mainnet; ETH pair; policy cap 10 ETH; common immutable hook rate, treasury share and team destination.

**Mechanic (proposal):** the hook seals each epoch's fee-bearing buy/sell balance and exposes one of three court themes: optimism, caution or balance. It also records retirement tiers and milestone state. A separate noncustodial case board accepts at most 16 short original entries per epoch under fixed rules. The question asks which entry best fits a sealed theme according to a fixed rubric: clarity 40%, originality 40%, theme fit 20%. An IMD panel returns the winning entry hash from a frozen allowlist; the answer awards a nonfinancial title only. No human judge selects the next case.

Use a signed, consumer-bound attestation, exact question hash, epoch, allowed-answer hashes and replay protection; verify the expected signer, deadline and quorum of four out of five agents. No answer, ambiguous tie or stale signature means no winner. Judges treat submitted text as content, not executable instructions. The hook never consumes untrusted text to set fees or trade access. The herald reads validated sidecar state and emits only its own fixed threshold letters; case text never becomes a public herald message.

**Separate oracle funding:** volunteer sponsorship or an independently budgeted case fund buys `oracle.request` through Intake. The 20% heartbeat IMD remains untouched. Lack of sponsors leaves the court open for display but unjudged; no disguised unpaid judgment or guaranteed winner.

**Heartbeat bounds:** one court interface or pre-audited board instance per epoch; entries 4–16 and text cap 80–240 bytes, chosen before opening the next case. The scoring rubric, title's nonfinancial status and oracle quorum remain fixed.

**First six funded upgrades and letters:**

1. Build a readable case docket. “Built the docket so everyone sees the same case and theme.”
2. Add a deterministic shortlist viewer. “Built the shortlist viewer so the jury's choices are explicit.”
3. Add an attestation-proof inspector. “Built verdict proofs so a title cannot come from a forged answer.”
4. Add a prompt-injection regression corpus and report. “Built adversarial text tests so entries cannot rewrite the court's rules.”
5. Instantiate a title-badge template. “Built title badges so judgments create souvenirs rather than financial claims.”
6. Add a disagreement and timeout archive. “Built the verdict archive so uncertainty stays visible.”

**Why people share it (inference):** absurd cases produce quotable verdicts, while visible agent disagreement gives the swarm a personality. The hook supplies real market-derived context; the oracle resolves a subjective choice that deterministic Solidity cannot honestly settle.

**Constructor letter:** “Tiny Court is a market-themed agent jury. Invented by the swarm; it won a swarm vote.” **Automatic record letter:** “The court has recorded ten verified verdicts.”

**Failure mode:** subjective judging remains manipulable and panels may correlate. Cap submissions and sponsor cost; no financial prize makes capture less useful. This is the highest-dependency candidate and has no verified historical virality precedent for its exact oracle mechanism.

## 4. Wrong Way Club — OOPS

**One-line hook:** a free prediction game celebrates being spectacularly wrong about the next market epoch, with no bets or token prizes.

**Launch:** standard token; `univ4_hook`; Ethereum mainnet; ETH pair; policy cap 10 ETH; common immutable hook rate and routing.

**Mechanic (proposal):** the hook stores signed ETH buy-minus-sell flow in fixed 12-hour epochs. Before an epoch opens, users commit predictions of the next epoch's flow sign through an opt-in sidecar, then reveal within a fixed window. The sidecar scores disagreement with the sealed sign and awards humorous, nonfinancial “confidently wrong” receipts. The hook's settlement accumulator supplies the result; no influencer, spot-price oracle or bot decides it.

Commitments include chain, contract, user and epoch. Zero flow is a draw, not a wrong-way win. Receipt scores are capped at one per address per epoch. The hook does not infer users from routers or block trading for people who skip the game. Sealing is permissionless and uses timestamps; late calls do not merge skipped epochs.

**Heartbeat bounds:** one new replay, challenge or noncustodial receipt feature per epoch; reveal window 1–3 hours, configured before commitments, and score-display cap 1–10. Outcome definition and financial rules are immutable.

**First six funded upgrades and letters:**

1. Build the commit/reveal game interface. “Built prediction commitments so nobody can change yesterday's guess.”
2. Add a settlement-proof replay. “Built flow replays so every wrong-way result can be checked.”
3. Add a receipts gallery. “Built the gallery so being wrong leaves a funny souvenir.”
4. Add personal calibration statistics. “Built calibration charts so the joke also teaches prediction discipline.”
5. Add a free observer challenge using sealed historical epochs. “Built historical challenges so spectators can play without a transaction.”
6. Ship a season blooper digest. “Built the blooper digest so the funniest misses survive the season.”

**Why people share it (inference):** it reverses the normal trader leaderboard: losing confidence becomes the joke instead of losing money to a prize pot. Share cards include the exact epoch and result, not a fabricated screenshot.

**Constructor letter:** “Wrong Way Club makes market mistakes collectible. Invented by the swarm; it won a swarm vote.” **Automatic record letter:** “Ten wrong-way rounds have been settled.”

**Failure mode:** a whale can trade to flip the sign, and Sybils can populate a gallery. There are no payouts, and manipulated outcomes must not be represented as investment skill. Sparse or empty epochs remain draws.

## 5. Patchwork Planet — QUILT

**One-line hook:** the pool weaves a permanent communal quilt from executed trades, and each funded swarm build adds a new way to explore it.

**Launch:** standard token; `univ4_hook`; Ethereum mainnet; ETH pair; policy cap 10 ETH; common immutable hook fee, 20% reserve and exact team recipient.

**Mechanic (proposal):** the hook maintains 64 bounded bins per epoch. Buy/sell direction selects color family, ETH consideration determines a capped thread weight, and the epoch index selects a deterministic stitch layout. Every successful trade contributes to a rolling commitment and the relevant bins; no per-trade unbounded array or random prize exists. A sealed quilt is reproducible from counters and swap logs, and voluntary retirement reveals a separate memorial border. Thus the hook is the communal state machine, not just an invoice for the site.

Historical quilts and commitments cannot change. Optional receipts cite a quilt commitment, not a claim on ETH. Individual identity is never guessed from router senders. The site can present normalized trade contribution without naming every swap a unique person.

**Heartbeat bounds:** one view, export or opt-in viewer sidecar per epoch; render resolution 64–512 pixels per side and 2–16 palette colors. Bin count, capped trade-weight formula and retirement thresholds are immutable. New renderers cannot rewrite old canonical quilt hashes.

**First six funded upgrades and letters:**

1. Build the canonical quilt viewer. “Built the quilt viewer so trades leave an inspectable shared object.”
2. Add an epoch-sealing inspector. “Built sealing proofs so old quilts cannot be rewritten.”
3. Add SVG exports with embedded epoch hashes. “Built quilt exports so shared art keeps its provenance.”
4. Add a retirement-border explorer. “Built memorial borders so voluntary retirement becomes visible history.”
5. Instantiate an optional quilt-receipt template. “Built quilt receipts so collectors can reference a specific shared moment.”
6. Build a side-by-side archive of original and alternative renderings. “Built the rendering archive so new styles preserve the original record.”

**Why people share it (inference):** a cooperative object creates “I helped make this” attachment and recurring reveal images without promising a winner or yield. Free exports circulate outside crypto communities.

**Constructor letter:** “Patchwork Planet weaves trades into a shared quilt. Invented by the swarm; it won a swarm vote.” **Automatic record letter:** “The planet has sealed thirty quilts.”

**Failure mode:** transaction splitting can affect visual patterns. Capped weights reduce dominance but do not prove Sybil resistance. No reward should depend on visual contribution; archive storage and the hook's bounded swap gas need explicit limits.

## Selection and unanswered questions

| Candidate | Main share object | Additional dependency beyond common heartbeat | Proposed first build |
| --- | --- | --- | --- |
| 1 NAP | Pet learning clip | None | Best first prototype: visible progress and honest dormancy. |
| 2 ASHW | Sky reveal/timelapse | Optional retirement | Best art-led alternative; strongest accounting-language requirement. |
| 3 TCRT | Agent verdict | Oracle sponsor, panel liveness, signed delivery | Defer until the funding and attestation paths are exercised. |
| 4 OOPS | Verified mistake receipt | Commit/reveal participation | Good gameplay prototype; no payout-based manipulation incentive. |
| 5 QUILT | Communal epoch artwork | Reliable log archive | Strong free spectator loop; keep canonical rendering reproducible. |

These rankings are **inferences**, not findings of an actual swarm vote. Test free spectator engagement, repeat visits, verified shares, active players and delivered improvement cost. Raw wash volume, wallet count and price appreciation cannot establish product quality.

**Unanswered before any launch:** actual payer authorization and exact team routing; latest launch policy at admission; safe ETH/IMD pool and reference mechanism; real per-job cost; gas sponsorship and relay custody; contract-based schedule payments; automatic bounded deployment/publication; authenticated job completion receipts; acceptable public proof of a swarm vote. Exact global on-hook holder counts and true standard-token supply burns remain interface limitations, with the explicitly named enrolled-address and retirement alternatives above.

## Research recipe and limits

Local checks found five candidate sections, thirty upgrade examples and twenty-two distinct external source URLs; both report files are byte-identical. Decimal arithmetic independently reproduced the illustrative thresholds. These checks are recorded in [check-results.json](check-results.json). Evidence retrieval times and SHA-256 digests are in [evidence-provenance.json](evidence-provenance.json).

The requested `research-report` skill was recovered from [IMD's public skill read](https://api.imd.fun/reads/skill/research-report); its guidance matches the brief's supplied reference. Public API reads and one read-only launch-policy check were made. No quote, submit, top-up, oracle request, transaction, launch or payment was sent. An earlier check with a path-scoped skill returned a configuration blocker; the retained final check uses `build-contract-project` and still correctly reports the absent independent review. No successful admission is claimed.

Reproduce the core observations with public HTTP calls:

```bash
curl -fsSL https://api.imd.fun/requests/capabilities
curl -fsSL https://api.imd.fun/openapi.json
curl -fsSL https://api.imd.fun/reads/skill/research-report
curl -fsSL https://api.imd.fun/reads/skill/uniswap-v4-hooks
curl -fsSL -X POST https://api.imd.fun/requests/check \
  -H 'Content-Type: application/json' \
  --data-binary '{"action":"launch.open","input":{"objective":"Feasibility check of standard Ethereum mainnet ETH-paired univ4_hook launch policy. This check creates no order or deployment.","skill":"build-contract-project","onchain":"univ4_hook","chainId":1,"pairWith":"eth"}}'
```

These endpoints are live and may change. Snapshots and their retrieval metadata are included under `artifacts/`. The API was reachable using curl even when the web renderer could not open it. Technical claims use primary documentation, API responses or source code. Viral-market observations use issuer statements and data aggregators with their limits stated; no exhaustive census or causal analysis was performed. All economics prices are labeled scenarios. Contracts, integrations and sites are designs, not built or audited systems. Local structural and arithmetic checks carry no independent authority.
