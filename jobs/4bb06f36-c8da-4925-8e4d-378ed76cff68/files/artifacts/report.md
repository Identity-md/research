# Proposal: FLOP as an opt-in provider in the IMD worker

**To:** the IMD team and seat holders
**Date:** 7 Nov 2026. Sources were fetched on this date. FLOP's docs are marked "devnet · next · development" and change often, so check them again before acting.

**Labels used below:** **[F]** fact, read on the linked page. **[L]** live check of a public endpoint on 7 Nov 2026. **[I]** our inference or proposal. **[U]** unverified or uncertain. **[Q]** open question.

---

## 1. Summary

- **[I]** Add FLOP as a second opt-in provider in the worker, alongside Venice. Only jobs that ask for FLOP use it. Each seat gets one FLOP identity, and the holder creates it on their own machine.
- **[I]** Start with oracle and research panels. Rehearse on devnet now, go live on testnet day one, then move to mainnet.
- **[I]** The point: many distinct agents, each publicly tied to an ERC-8004 agent, buying verified inference on FLOP, with every receipt shown next to the IMD job it served.
- **Main limit today [L]:** the public gateway lists **one model, Qwen2.5 0.5B Instruct**. It cannot do research-grade or oracle-grade reasoning. Until better models are listed, FLOP work would be a parallel, low-stakes lane.

## 2. What FLOP is (checked)

| Claim | Status | Source |
|---|---|---|
| FLOP is a proof-of-inference chain. Agents pay miners in FLOP to run inference. | [F] | [What is FLOP?](https://docs.flop.network/docs/what-is-flop), [llms.txt](https://docs.flop.network/llms.txt) |
| How a session settles: request, match, prove (activation commitments plus a co-signed transcript), settle (the proof hash goes into a block). | [F] | [Session lifecycle](https://docs.flop.network/docs/inference-session-lifecycle) |
| The official domains include flop.finance, docs.flop.network, api.flop.network, the faucet at faucet.flop.network and the devnet RPC at rpc.devnet.flop.network. The page also says "There is no FLOP token yet." | [F] | [Official links](https://docs.flop.network/docs/official-links) |
| Devnet earns nothing: no rewards and no airdrop weight. | [F] | [Official links](https://docs.flop.network/docs/official-links), [Timeline FAQ](https://docs.flop.network/docs/testnet-and-timeline) |
| Devnet can reset. | [I] | Docs call devnet "a throwaway network" ([Timeline FAQ](https://docs.flop.network/docs/testnet-and-timeline)) and tell you to "compare live RPC and faucet genesis before use" ([Devnet status](https://docs.flop.network/docs/network-devnet)). That implies resets, though no page says it in those words. |
| Public devnet endpoints are available. | [F]/[L] | [Devnet status](https://docs.flop.network/docs/network-devnet). The gateway at [api.flop.network/v1](https://api.flop.network/v1), the [faucet](https://faucet.flop.network) and the [explorer](https://explorer.devnet.flop.network) all answered HTTP 200. The faucet reports `"network":"devnet"`. |
| RPC endpoint `wss://rpc.devnet.flop.network` | [F] | [Agent integration](https://docs.flop.network/docs/agent-integration). We did not open a websocket to test it. |
| Packages: `@flop-labs/sdk` 0.4.0, `@flop-labs/client` 0.2.1, `@flop-labs/cli` 0.4.0 (all published 29 Oct 2026) and `flop-sdk` 0.2.0 on PyPI. Source is in github.com/flop-labs/flop-core. | [F]/[L] | [SDK references](https://docs.flop.network/docs/sdk-references), [npm sdk](https://www.npmjs.com/package/@flop-labs/sdk), [npm client](https://www.npmjs.com/package/@flop-labs/client), [npm cli](https://www.npmjs.com/package/@flop-labs/cli), [PyPI](https://pypi.org/project/flop-sdk/) |
| Agent airdrop: a locked balance can be spent only on compute, and every 3 FLOP spent on inference unlocks 1 FLOP. | [F] | [Airdrop and testnet conversion](https://docs.flop.network/docs/airdrop-and-testnet-conversion) |
| The rule above is "ratified but not yet built". The runtime still vests grants on a 90-day linear curve, and "the genesis distribution ceremony is not yet wired". | [F] | same page |
| The draft genesis pool is 4.4bn FLOP, including a 1.2bn agent cohort. "Every figure in it is provisional." | [F] | [Official links](https://docs.flop.network/docs/official-links) |
| The chain itself offers spend limits, bounded proxies, escrow and a spend-condition layer. | [F] (draft whitepaper) | [Agent accounts and spend control](https://docs.flop.network/docs/agent-accounts-and-spend-control) |

### Where the brief and the sources disagree

1. **Dates [U].** The brief says devnet opened to the public on 3 Nov 2026 and that a testnet date is due the week of 9 Nov. FLOP's own pages (updated 23–30 Oct) still give **"Testnet: the working target is Tuesday 3 November 2026 … a target rather than a fixed date"** ([Timeline FAQ](https://docs.flop.network/docs/testnet-and-timeline)). Meanwhile the [Testnet status](https://docs.flop.network/docs/network-testnet) page says **"Status: planned. Unavailable"**. Live checks agree that only devnet is running. We found no primary source for "public devnet 3 Nov" or "testnet date the week of 9 Nov". The [agent integration](https://docs.flop.network/docs/agent-integration) page, updated 3 Nov, does document public devnet use. So the plan below treats the testnet date as **unknown**.
2. **Identity type [U].** The brief says a testnet agent needs an **Ed25519 did:key**. We found no FLOP page or API field that mentions `did:key`. What we did find: the gateway's devnet enrollment accepts **sr25519, ed25519 or ecdsa** signatures from a Substrate (SS58) account ([OpenAPI `/enroll/wallet`](https://api.flop.network/openapi.json)), and the faucet asks for an SS58 address with prefix 42 ([faucet](https://faucet.flop.network)). The proposal therefore says "one FLOP identity per seat": an Ed25519 key that can be shown both as an SS58 address and as a `did:key`. FLOP should confirm what testnet will actually require.
3. **Faucet cap per identity [F]/[U].** The devnet faucet offers a "quick fund" of 25 FLOP, or 500–2000 FLOP for a verified human (BrightID, Self, Human Passport or Guild) ([faucet](https://faucet.flop.network)). The gateway grants a new account one model-scoped allowance (default 25 FLOP, 2 requests per minute), which expires within 24 hours and sits under a daily cap on new allowances. A spent or expired allowance "is never renewed" ([OpenAPI](https://api.flop.network/openapi.json)). We found no published per-identity testnet faucet cap.
4. **HTLC chat route [F].** "`flop chat` in full CLI 0.4.0 uses HTLCs, which require a registered EconomicCritical appraisal profile. Devnet's registry was empty at finalized block 2,764,673 on 3 November 2026", and "neither a flag nor simulator mode supplies it" ([Agent integration](https://docs.flop.network/docs/agent-integration), [Send to a specific miner](https://docs.flop.network/docs/send-to-specific-miner)). So the simplest chat route in the CLI does not work on devnet today for ordinary users. The docs also say "the SOFT tier's end-to-end settlement and dispute lane is still being specified" ([Session lifecycle](https://docs.flop.network/docs/inference-session-lifecycle)).
5. **Gateway auth vs. on-chain payment [F].** The gateway "currently accepts funded API keys. Direct public payment-proof settlement is not enabled until an on-chain verifier replaces the format-only local development path" ([OpenAPI info](https://api.flop.network/openapi.json)). Gateway receipts are "a current gateway ledger observation, not … an independent proof of chain finality" ([OpenAPI `/keys/me/receipts/{request_id}`](https://api.flop.network/openapi.json)).
6. **Model catalog [F]/[L].** The live `/v1/models` lists one model: `qwen/qwen2.5-0.5b-instruct` ("devnet-ts"), 32k context, text only, `max_tokens` as its only supported parameter, 51 miner price sources. The docs warn that the catalog "is not proof that inference is available" ([Agent integration](https://docs.flop.network/docs/agent-integration)).

## 3. What IMD already does (checked)

| Claim | Status | Source |
|---|---|---|
| Venice is opt-in. You set it up with `imd update`, `imd venice key`, `imd service restart`. "Only jobs that ask for Venice use it." The docs also advise giving the worker a key with a spending limit. | [F] | [imd.fun/docs](https://imd.fun/docs/) |
| The worker installs from GitHub releases (`Identity-md/worker/releases/latest`) with a SHA256 check. It runs with `--auto-update`. | [F] | [imd.fun/docs](https://imd.fun/docs/) |
| "Bind a device to a seat, and a seat to an ERC-8004 agent." | [F] | [imd.fun/docs](https://imd.fun/docs/) |
| Research, oracle and the rest run on "Any model". Research and audits go to a panel. | [F] | [imd.fun/docs](https://imd.fun/docs/) |
| "A panel seats one member per seat". Oracle quorum runs from 2 to panelSize, and every member's answer must match. Research `panelSize` is 1–9. | [F] | [imd.fun/docs](https://imd.fun/docs/) |
| Oracle panels can seat up to 100 distinct seats. | [U] | Given in the brief. We did not find the oracle panelSize ceiling on the docs page. |
| Explorer listing of jobs, oracle questions and agents | [L] | [explorer.imd.fun](https://explorer.imd.fun) |

## 4. Proposal

### A. Worker change [I]

- **Command:** `imd flop setup`, modeled on `imd venice key`. It runs on the holder's machine and:
  1. creates one Ed25519 key per seat, kept in the worker's local secret store with file mode 0600 and never printed;
  2. shows the public SS58 address and the `did:key`;
  3. on devnet, signs the gateway enrollment challenge (`GET /v1/enroll/wallet/challenge`, then `POST /v1/enroll/wallet`) to get a model-scoped bearer key, which is also stored locally ([OpenAPI](https://api.flop.network/openapi.json)).
- **Daily spend cap:** a required setting, `imd flop cap <FLOP/day>`. With no cap, FLOP stays off. The worker counts spend from the gateway's own records (`/keys/me/receipts`) and stops taking FLOP jobs once the cap is reached. Where FLOP supports them, add chain-level limits as well: spend limits or a bounded proxy ([spend control](https://docs.flop.network/docs/agent-accounts-and-spend-control)) and scoped child keys from `/keys/ephemeral` ([OpenAPI](https://api.flop.network/openapi.json)). Then the worker's counter is not the only guard.
- **Public seat-to-DID link:** a statement `{tokenId, erc8004AgentId, flopDid, ss58, network, issuedAt}`, signed twice: by the FLOP key (proving control of the DID) and by the wallet that holds the seat NFT (proving control of the seat). IMD publishes it on the agent's explorer page. Revoking or rotating a key publishes a new statement that replaces the old one. **[Q]** Whether FLOP can also anchor this link on its own chain (for example a remark or an identity field) is for FLOP to answer.

### B. Routing [I]

- A job or oracle question that asks for FLOP (for example `provider: "flop"`) goes **only** to seats that have a valid FLOP credential, a published link and room left under their cap. Seats without the credential are skipped, the same way Venice routing works.
- **Start with oracle and research panels.** A panel already seats one member per seat ([docs](https://imd.fun/docs/)), so each FLOP DID is a distinct, verifiable agent.
- **What the current catalog can and cannot do [L]/[I]:**
  - It **can** handle short text tasks under 24k prompt tokens and 8k completion tokens, such as extraction, formatting, simple yes/no checks on supplied text, and smoke tests.
  - It **cannot** reliably handle multi-step research, citation-heavy reports, code, tool calls (the only supported parameter is `max_tokens`), images, or oracle answers where every panel member must match. A 0.5B model will disagree often, and quorums will fail.
  - Recommendation: until larger models are listed, run FLOP as a **shadow lane**. A FLOP member answers next to the normal panel, and its answer counts toward quorum only when the requester explicitly asks for it.

### C. Receipts on explorer.imd.fun [I]

For every FLOP-served step, record and show on the job page:
- the network (devnet, testnet or mainnet), the FLOP DID and the SS58 address;
- the gateway `request_id`, linked to the holder's receipt record (`/keys/me/receipts/{request_id}` is readable only by the credential owner, so the worker copies the fields it needs, never the key);
- when a chain session exists, the session or settlement id and the block, linked to [explorer.devnet.flop.network](https://explorer.devnet.flop.network) (or the testnet or mainnet explorer);
- a status badge: "gateway-observed" (pending) or "settled on chain". This follows FLOP's own warning that gateway records are not proof of finality ([OpenAPI](https://api.flop.network/openapi.json)).
- **[Q]** The URL formats for FLOP explorer pages are not documented. We need them from FLOP.

### D. Rollout [I]

| Phase | When | What holders get |
|---|---|---|
| Devnet rehearsal | Now | Practice only: setup, enrollment, link signing, receipt display, cap enforcement. No rewards or airdrop weight ([F], [Official links](https://docs.flop.network/docs/official-links)). Expect resets, so do not build state that depends on devnet. |
| Testnet | Day one, once FLOP publishes the testnet identity ([Testnet status](https://docs.flop.network/docs/network-testnet) is still "planned") | Real, recorded agent activity tied to each seat. Under the draft rules, inference spend could count toward the agent airdrop. That rule is provisional and not yet built ([F], [airdrop page](https://docs.flop.network/docs/airdrop-and-testnet-conversion)). |
| Mainnet | Targeted for Q1 2027 ([F], [Timeline FAQ](https://docs.flop.network/docs/testnet-and-timeline)) | FLOP becomes a paid provider with on-chain receipts. Keep it opt-in and keep the cap. |

### E. Rules [I]

1. Keys stay on the holder's machine. They never go into a job body, a log, an artifact, a repo or the explorer. Only public addresses, DIDs, signatures and receipt ids are published.
2. One DID per seat. One seat never shares a DID with another, and one holder does not create several DIDs for one seat.
3. No faucet cycling: no making new identities to draw more test FLOP. Each seat's DID uses the faucet only within FLOP's limits.
4. No synthetic traffic. FLOP calls happen only to serve real IMD jobs or questions. Self-dealing loops break the link's credibility and may break FLOP's rules.
5. Breaking these rules unlinks the seat from FLOP routing.

### F. Stopgap: `imd-flop` companion CLI (spec) [I]

`imd-flop` is a separate npm package. It does not modify or wrap the worker. It uses `@flop-labs/client` and `@flop-labs/sdk` and stores data under its own directory (`~/.imd-flop/`).

| Command | Does |
|---|---|
| `imd-flop init [--network devnet]` | Creates one Ed25519 key per seat locally (mode 0600). Prints the SS58 address and the did:key. Checks that the faucet's `/chain` genesis matches the RPC genesis, as the [agent docs](https://docs.flop.network/docs/agent-integration) advise. |
| `imd-flop link --token <id>` | Builds the seat-to-DID statement (section A). Signs it with the FLOP key and prints a message for the holder to sign with the NFT wallet on their own computer. Writes the signed JSON so it can be published. Reads the agentId from the seat's ERC-8004 record. Never asks for a seed phrase. |
| `imd-flop faucet` | Makes one request for this DID through the faucet's own flow, then gateway enrollment. It refuses to run again once a grant exists for the DID. |
| `imd-flop run --job <id> --cap <FLOP/day>` | Takes an IMD job id the seat is serving, sends the text step to the gateway's `/v1/chat/completions`, and saves the response and `request_id`. It stops at the cap. It does not submit anything to IMD; the holder decides what to use. |
| `imd-flop status` | Shows network, address, balance, allowance left and expiry, today's spend against the cap, and recent receipts with their pending or settled state. |

When the worker change ships, the worker can import `~/.imd-flop/` so holders keep the same DID (one DID per seat still applies).

### G. Risks and open questions

**Risks [I]**
- **Model quality:** one 0.5B model today ([L]). Panels may fail quorum. Mitigation: the shadow lane in B.
- **Dates move:** the testnet target is already past and its status is "planned" ([F]). Do not tie a worker release to a FLOP date.
- **Settlement not final:** the SOFT settlement lane is "still being specified", and gateway payment-proof is "format-only" ([F]). Receipts may stay "gateway-observed" for a while.
- **HTLC chat blocked:** no registered appraisal profile on devnet ([F]). The integration must use the gateway or direct sessions, not `flop chat`.
- **Draft economics:** the 1-for-3 unlock is "ratified but not yet built", and every figure is provisional ([F]). Do not promise holders an airdrop.
- **Scams:** FLOP says no token, claim or contract exists yet ([F]). The worker must never ask holders to "claim" anything.
- **Key handling:** each seat adds a hot key. A cap and scoped child keys limit the damage if one leaks.

**Open questions for FLOP [Q]**
1. What testnet requires for agent identity: a did:key, an SS58 sr25519 or ed25519 account, or both? Can a seat's devnet key carry over?
2. The confirmed testnet date, and when the testnet genesis and gateway will be published.
3. The per-identity faucet cap on testnet. Does a verified-human grant count per identity or per person, given that one holder may own many seats?
4. Will a cohort of 1,000+ agents run into the gateway's daily cap on new allowances? Can a cohort get allowances for one named partner?
5. When will larger models be listed, and which ones?
6. Explorer URL formats for sessions and settlements, and when chain-settled receipts will be available for gateway requests.
7. Can a seat-to-DID link be anchored on chain?

**Open questions for IMD [Q]**
1. Confirm the oracle panel ceiling (the brief says 100; the docs we read show research `panelSize` 1–9).
2. Who pays for FLOP jobs on testnet and mainnet: requesters in IMD, or holders from their own FLOP?

## 5. Method and limits

- Read on 7 Nov 2026: docs.flop.network pages (through its `llms.txt` index), the gateway's `/v1`, `/v1/models` and `/openapi.json`, the devnet faucet and explorer pages, npm and PyPI registry metadata, imd.fun/docs and explorer.imd.fun.
- Not done: we opened no websocket RPC connection, ran no inference, created no key, made no faucet request and enrolled nothing. flop.finance renders mostly with JavaScript, so we could not read its testnet or airdrop text. No claim in this report relies on it.
- No token price is discussed.
