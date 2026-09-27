# TWTIME Twitch Channel Points faucet: feasibility report and build-prompt outline

**Prepared:** 2026-09-27 (UTC)  
**Question:** What prompt should an IdentityMD swarm receive to launch a `TwitchTime` (`TWTIME`) token, a Channel Points–driven distribution contract, and a viewer website?

## Executive verdict

**Do not ask the swarm to launch the product exactly as described.** Two independent blockers exist:

1. **Policy blocker (confirmed fact):** Twitch says Channel Points may not be exchanged for items with value outside Twitch and explicitly prohibits exchanging them for real or virtual currencies. A transferable blockchain token is, at minimum, a virtual currency/item usable outside Twitch. Launching `10 TWTIME` per Point would therefore appear prohibited. This is a product-policy assessment, not legal advice. Obtain written Twitch approval before building or launching this exchange. [Twitch Channel Points Acceptable Use Policy](https://legal.twitch.com/en/legal/channel-points-acceptable-use-policy)
2. **UX/API blocker (confirmed fact plus inference):** Twitch's documented Channel Points API lets the broadcaster's authorized app create fixed-cost rewards, read redemptions, and mark them fulfilled/canceled. EventSub reports redemptions. The documented API has no viewer endpoint that spends an arbitrary number of Points and no endpoint exposing a viewer's Channel Points balance. Consequently, an external website cannot directly perform the requested spend or prove the user's current balance through the documented API. A viewer must redeem a fixed-cost reward in Twitch's UI; Twitch itself enforces whether the viewer can afford it. [Twitch API reference](https://dev.twitch.tv/docs/api/reference), [EventSub subscription types](https://dev.twitch.tv/docs/eventsub/eventsub-subscription-types/)

The best prompt is therefore a **gated prompt**: first demand written Twitch approval or a compliant redesign; only then permit implementation and production deployment. If approval is obtained, use a catalog of fixed-cost reward denominations, not a free-form Point input. Examples: 100, 500, 1,000 and 5,000 Points, yielding 1,000, 5,000, 10,000 and 50,000 TWTIME respectively.

## What is known

### Confirmed facts

| Fact | Product consequence | Evidence |
|---|---|---|
| Points have no monetary value and cannot be purchased or exchanged outside Twitch; the policy prohibits trading them for real or virtual currencies. | The proposed direct Points-to-ERC-20 exchange must not launch without Twitch's written approval. | [Channel Points Acceptable Use Policy](https://legal.twitch.com/en/legal/channel-points-acceptable-use-policy) |
| Creating a custom reward requires a broadcaster user access token with `channel:manage:redemptions`; `broadcaster_id` must match the token's user, minimum reward cost is 1, and the broadcaster must be Affiliate or Partner. | Broadcaster onboarding is required; this is not a viewer-authorized operation. | [Create Custom Rewards](https://dev.twitch.tv/docs/api/reference#create-custom-rewards) |
| A reward has one integer `cost`; a channel may have at most 50 custom rewards (enabled plus disabled). | Arbitrary positive whole-number spends are not represented by one reward. Use a bounded denomination catalog if approved. | [Create Custom Rewards](https://dev.twitch.tv/docs/api/reference#create-custom-rewards) |
| The documented Channel Points endpoints are create/delete/get/update rewards, get redemptions, and update redemption status. There is no documented endpoint for a viewer to initiate a redemption or read a viewer's Point balance. | The website cannot truthfully offer “enter any amount and spend”; redemption must occur in Twitch's viewer UX. | [Twitch API reference, Channel Points section](https://dev.twitch.tv/docs/api/reference) |
| `channel.channel_points_custom_reward_redemption.add` includes redemption ID, Twitch user ID, reward ID and cost; it requires broadcaster authorization with `channel:read:redemptions` or `channel:manage:redemptions`. | A trusted backend can derive the issuance amount from Twitch's event, never from browser input. | [EventSub redemption event](https://dev.twitch.tv/docs/eventsub/eventsub-subscription-types/#channelchannel_points_custom_reward_redemptionadd) |
| EventSub webhook delivery is at least once; messages must be HMAC verified and duplicates/replays handled. | Store both EventSub message IDs and redemption IDs and make issuance idempotent. | [Handling webhook events](https://dev.twitch.tv/docs/eventsub/handling-webhook-events) |
| An unfulfilled redemption may be changed to `FULFILLED` or `CANCELED`; canceling refunds the viewer's Points. Only the app that created the reward may update it. | Fulfill only after durable on-chain success; cancel/refund on permanent failure according to an explicit operations policy. | [Update Redemption Status](https://dev.twitch.tv/docs/api/reference#update-redemption-status) |
| ERC-20 defines standard supply, balance, approval and transfer behavior. | A normal transferable `TWTIME` would be an outside-Twitch virtual token, reinforcing the policy concern. | [ERC-20 standard](https://eips.ethereum.org/EIPS/eip-20) |

### Inferences and recommendations (not facts supplied by Twitch)

- **Separate contracts:** use one immutable/capped ERC-20 token and one distributor/faucet contract. Separation reduces the distributor's authority and lets the distribution mechanism be replaced without replacing the token.
- **Prefer pre-funded distribution:** mint a declared capped supply to a multisig treasury and fund the distributor. Do not give the Twitch bridge unlimited mint power. This creates an auditable maximum liability.
- **Backend is an oracle:** a smart contract cannot independently inspect Twitch. A trusted service must verify EventSub and submit a chain transaction. Document this trust explicitly.
- **Wallet binding:** after Twitch OAuth, issue a short-lived nonce containing Twitch user ID, wallet address, chain ID, domain and expiry; require an EIP-191/EIP-712 wallet signature; consume the nonce once. Never use reward `user_input` as proof of wallet ownership.
- **Exactly-once issuance:** use the Twitch redemption ID as an immutable claim key in the distributor (`processed[hash(redemptionId)]`). Database uniqueness and on-chain uniqueness are both required.
- **Amount arithmetic:** for an 18-decimal token, `tokenUnits = rewardCost * 10 * 10^18`, with checked arithmetic. The cost must come from the authenticated Twitch event and must match an allowlisted reward ID/cost pair.
- **Gas:** because the user is spending Points, not native chain gas, a service relayer should submit distributions and pay gas. This is a central operational dependency.
- **Do not dynamically change one reward's cost per viewer:** simultaneous viewers and event races make this unsafe. Fixed denominations are deterministic and Twitch checks affordability in its own UI.
- **No “balance” claim in the external site:** the Twitch API evidence reviewed does not support displaying the user's current Point balance. Say “Twitch will confirm whether you have enough Points” and link/open the channel reward UI.

## Prompt outline with known details filled in

Copy the following into the swarm only after replacing every bracketed decision. The compliance gate is intentional.

```text
You are a product, smart-contract, backend, frontend, security, QA, DevOps and compliance swarm. Deliver a production-ready TWTIME distribution product, but obey the stop gate below.

GOAL
Build TwitchTime, ticker TWTIME. For each successful Twitch custom Channel Points reward redemption, distribute exactly 10 TWTIME per Point actually spent. Points and issuance amounts are positive integers. The authoritative amount is the fixed reward cost in Twitch's authenticated redemption event, never a browser-provided value.

STOP GATE — REQUIRED BEFORE CODE OR DEPLOYMENT
The Twitch Channel Points Acceptable Use Policy says Points cannot be exchanged for outside-Twitch items of value or virtual currencies. Do not implement or deploy the Points-to-TWTIME exchange until the owner supplies written Twitch approval explicitly covering this product. Save the approval reference and reviewed policy version in the launch decision record. If approval is absent, produce only: (a) a compliance-risk memo, (b) a compliant alternative design that provides only an on-Twitch, non-transferable experience, and (c) mockups with all transaction/distribution actions disabled. Do not launch a workaround.

PRODUCT SCOPE AFTER THE GATE PASSES
- One broadcaster/channel: [TWITCH CHANNEL LOGIN AND ID]. The broadcaster must be Affiliate or Partner.
- Supported chain: [CHAIN NAME AND CHAIN ID]. Production RPC provider: [PROVIDER]. Block explorer: [URL].
- Create fixed-cost Twitch rewards using channel:manage:redemptions. Initial denominations: [100, 500, 1000, 5000] Points. Corresponding outputs: [1000, 5000, 10000, 50000] TWTIME.
- The website supports Twitch login, wallet connection, signed Twitch-to-wallet binding, denomination selection, clear instructions to redeem the matching reward in Twitch, live/polling status, transaction link, and claim history.
- Do not claim the website can read a viewer's Point balance or spend Points directly. Do not accept a free-form amount. Twitch's redemption UI is the only spend surface, and Twitch determines affordability.

TOKEN CONTRACT
- ERC-20 name TwitchTime, symbol TWTIME, 18 decimals.
- Supply model: capped fixed supply of [MAX SUPPLY] TWTIME minted at deployment to [MULTISIG TREASURY]; no public mint and no bridge mint authority.
- Decide and document whether transfers are [TRANSFERABLE / RESTRICTED]. This must match Twitch's written approval and legal review.
- Use a pinned, vendored and audited contract library version. Include license notices and source verification.
- State admin model, multisig threshold, pause behavior, upgradeability decision, and renunciation/timelock plan. No single EOA production owner.

DISTRIBUTOR CONTRACT
- Pre-funded by the treasury and authorized relayers are controlled by [MULTISIG/TIMELOCK].
- distribute(redemptionHash, recipient, wholePointCost) computes 10 * wholePointCost TWTIME using token base units, rejects zero, rejects a zero recipient, rejects reused redemptionHash, and emits an indexed distribution event.
- Enforce per-redemption and aggregate limits: [LIMITS]. Include pause and role rotation. Use checks-effects-interactions and test malicious/non-standard token behavior as applicable.
- Never put raw Twitch names or OAuth data on-chain. Hash the redemption ID with a domain separator that includes chain ID and distributor address.

TRUSTED BACKEND / TWITCH INTEGRATION
- Implement broadcaster OAuth Authorization Code flow server-side, request only channel:manage:redemptions, validate state, encrypt refresh tokens at rest, rotate secrets, and support revocation/reauthorization.
- Create and persist app-created fixed-cost reward IDs. Accept events only for the configured broadcaster and allowlisted reward ID/cost pairs.
- Receive channel.channel_points_custom_reward_redemption.add through HTTPS EventSub webhooks. Verify Twitch HMAC against the raw body with constant-time comparison, reject stale events, store EventSub message IDs, and acknowledge quickly before asynchronous processing.
- Database constraints make EventSub message ID and redemption ID unique. Use a durable state machine: RECEIVED -> VALIDATED -> TX_SUBMITTED -> CONFIRMED -> TWITCH_FULFILLED, with explicit retry/dead-letter states.
- Bind Twitch user ID to a wallet through a short-lived, single-use nonce and wallet signature containing domain, Twitch ID, wallet, chain ID and expiry. Define whether rebinding is permitted and its cooldown [POLICY].
- Before sending, re-fetch/validate the redemption where useful; derive the amount only from Twitch data. Submit through a relayer. Wait [CONFIRMATIONS] confirmations, then mark the Twitch redemption FULFILLED.
- On permanent delivery failure, mark CANCELED so Twitch refunds Points, subject to [TIMEOUT AND MANUAL REVIEW POLICY]. Never cancel after tokens were successfully delivered. Reconcile Twitch, database and chain continuously.
- Handle chain reorgs, stuck/replaced transactions, depleted distributor funds, expired broadcaster tokens, reward changes/deletion, EventSub revocation, duplicate/out-of-order events and provider outages.

FRONTEND
- Pages: landing/how it works, Twitch login/callback, wallet binding, reward denomination chooser, redemption instructions, pending/success/failure status, history, FAQ, privacy/terms/risk disclosures, and support contact.
- Show all quantities as whole Twitch Points and exact TWTIME output. Validate positive integers even though denominations are fixed.
- Never request broadcaster management scope from viewers. Viewer Twitch OAuth is for identity only, using the minimum scopes required. Keep all client secrets and relayer keys server-side.
- Provide accessible responsive UX and honest state language: “Redeem on Twitch,” not “Spend from this website.” Do not display a made-up Point balance.

SECURITY, PRIVACY, LEGAL AND OPERATIONS
- Threat-model forged/replayed webhooks, OAuth CSRF, account/wallet takeover, binding races, duplicate issuance, reward-cost drift, DB rollback, compromised relayer, admin compromise and privacy leakage.
- Add rate limits, structured audit logs without secrets, monitoring/alerts, backups, key rotation, least privilege, incident runbooks and an emergency pause drill.
- Publish privacy policy, terms, token risk disclosures, data retention/deletion process and support contact. Obtain jurisdiction-specific counsel for securities, consumer, tax, sanctions/AML, minors and promotion/sweepstakes questions before launch.
- Obtain independent smart-contract audit and application penetration test. Resolve critical/high findings before mainnet.

DELIVERABLES
- Monorepo with contracts, backend, frontend, database migrations, infrastructure-as-code, deployment scripts, pinned/vendored dependencies and reproducible offline builds.
- Architecture and sequence diagrams; trust/centralization disclosure; ADRs for chain, supply, transferability, upgradeability, custody, relaying and failure/refund semantics.
- Unit, integration, invariant/fuzz and end-to-end tests. Include Twitch webhook fixtures, duplicate/replay cases, denomination mismatch, zero/overflow boundaries, chain reorg and refund/no-double-pay scenarios.
- Staging deployment on [TESTNET], verified source, seeded rewards for a Twitch test channel, monitoring dashboards and operator runbooks.
- Production deployment only after the stop gate, audit, pen test, owner acceptance and go-live checklist all pass. Record contract addresses, compiler/settings, library versions, git commit, multisig owners and deployment transactions.

ACCEPTANCE TESTS
1. A 500-Point Twitch redemption by a bound viewer results in exactly 5,000 TWTIME base-token-equivalent credited once after required confirmations.
2. Duplicate EventSub deliveries and repeated relayer calls cannot distribute twice.
3. Unknown reward, altered cost, wrong broadcaster, bad/stale HMAC, unbound wallet, zero amount and already processed redemption all fail safely.
4. Insufficient Twitch Points is rejected by Twitch's redemption UI; the external website makes no unsupported balance assertion.
5. Permanent pre-delivery failure reaches CANCELED and refunds Points; post-delivery failures never refund or pay twice and are escalated for reconciliation.
6. Secrets never enter browser bundles, logs, repository history or on-chain data.

REPORTING RULES
Separate verified facts, assumptions, design choices, risks and open decisions. Cite primary documentation. Stop and request owner decisions rather than inventing token economics, chain, legal approval, custody or admin policy.
```

## Decisions still required from the owner

These are not implementation details the swarm should invent:

1. **Twitch approval:** Has Twitch given written permission for this exact virtual-token redemption? This is the launch-blocking question.
2. **Purpose and transferability:** What can TWTIME do? Is it freely transferable/tradable, non-transferable, or redeemable for anything? These facts drive policy and legal analysis.
3. **Chain and gas:** Ethereum mainnet, an L2, or another EVM chain? Who pays relayer gas, under what budget and rate limits?
4. **Supply:** Fixed cap, initial allocation, treasury vesting, liquidity, burns and whether any market will be created. Suggested default: capped supply, pre-funded distributor, no bridge mint role.
5. **Denominations and limits:** Which fixed Point costs; per-user, per-stream/day and total campaign caps; cooldowns; and distributor reserve policy?
6. **Custody/governance:** Multisig signers/threshold, timelock, emergency pauser, relayer key custody and incident authority.
7. **Wallet binding:** Can one Twitch account bind multiple wallets? Can it rebind after compromise, and how is recovery adjudicated?
8. **Failure semantics:** Confirmation depth, fulfillment timeout, when to cancel/refund, and who handles exceptions where chain delivery and Twitch status diverge?
9. **Audience/jurisdictions:** Countries served, age restrictions, sanctions screening, privacy retention and tax treatment. Qualified counsel should decide legal obligations.
10. **Brand and operations:** Domain, visual identity, support address/SLA, privacy controller, hosting/database/RPC vendors, monitoring and launch owner.

## A compliant alternative if Twitch approval is not obtained

Keep the reward wholly inside Twitch and make it non-transferable: for example, a stream interaction, temporary on-stream recognition, voting input, or other creator-provided channel benefit consistent with Twitch's policy. Do **not** label an off-chain balance “TWTIME” and later convert it to tokens; that would preserve the substance of the prohibited exchange. A separate ERC-20 can exist only as an unrelated product with no issuance, eligibility, allocation or preferential access based on Channel Points.

## Evidence boundaries and uncertainty

- **Fact:** The cited Twitch pages describe the documented API and policy as reviewed on 2026-09-27.
- **Inference:** “No documented endpoint” means the requested external spend/balance workflow is unsupported by the public documentation reviewed; it does not prove Twitch has no private/internal capability.
- **Inference:** Treating a transferable ERC-20 as a prohibited virtual currency/item of outside value is the straightforward reading of the policy, but only Twitch can authoritatively approve its own platform use and qualified counsel can give legal advice.
- **Unknown:** No written Twitch approval, chain, token supply, transfer rules, jurisdiction, contract ownership, infrastructure choices or launch budget were supplied.
- **Not assessed:** This report is not a smart-contract audit, legal opinion, tax analysis, data-protection impact assessment or confirmation that `TWTIME` is available as a trademark/ticker.

## Primary sources

- [Twitch Channel Points Acceptable Use Policy](https://legal.twitch.com/en/legal/channel-points-acceptable-use-policy)
- [Twitch API reference: Channel Points](https://dev.twitch.tv/docs/api/reference)
- [Twitch EventSub subscription types](https://dev.twitch.tv/docs/eventsub/eventsub-subscription-types/)
- [Twitch: Handling webhook events](https://dev.twitch.tv/docs/eventsub/handling-webhook-events)
- [Twitch OAuth access tokens](https://dev.twitch.tv/docs/authentication/getting-tokens-oauth/)
- [Twitch access-token scopes](https://dev.twitch.tv/docs/authentication/scopes/)
- [Twitch Developer Services Agreement](https://legal.twitch.com/en/legal/developer-agreement/)
- [ERC-20 standard](https://eips.ethereum.org/EIPS/eip-20)
- [OpenZeppelin Contracts 5.x ERC-20 documentation](https://docs.openzeppelin.com/contracts/5.x/api/token/erc20)

