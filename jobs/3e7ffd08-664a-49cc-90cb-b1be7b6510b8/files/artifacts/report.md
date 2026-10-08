# The IMD agent swarm and how a paid job is opened

Sources read 2026-10-07. Live numbers will change.

## What the swarm is

**Facts (from the sites):**
- IMD calls itself "a network of AI agents that build, review and ship software, paid in IMD, with the record on Ethereum" ([imd.fun/llms.txt](https://imd.fun/llms.txt)). The explorer says agents build work, check each other's work, and record it onchain ([explorer.imd.fun/launch](https://explorer.imd.fun/launch)).
- Each worker is tied to an IMD NFT. It runs the operator's own Claude Code or Codex on their own plan. The network sends a task, and a verifier checks the result before it goes on chain under that agent ([imd.fun/docs](https://imd.fun/docs/)).
- Live status on 2026-10-07 showed 793 agents online, 800 enrolled seats, and 9,510 jobs, of which 9,296 were completed ([api.imd.fun/swarm](https://api.imd.fun/swarm), the feed the homepage loads).

**Inference:** "Swarm" means this pool of independent, NFT-gated workers, not one central AI.

## How a paid job is opened

**Facts** ([imd.fun/docs, "How paying works"](https://imd.fun/docs/)):
1. **Optional check.** `POST /requests/check` previews a request for free. It shows the plan and anything that would block it.
2. **Quote.** `POST /requests/quote` takes a UUID `requestKey`, the action `job.open`, and a job body (objective, outputs and similar fields). The call is authorised by a bearer token you generate. The quote is valid for 600 seconds ([capabilities](https://api.imd.fun/requests/capabilities)).
3. **Pay.** `POST /requests/:id/submit` first returns a 402 x402 challenge. The same wallet then signs a Permit2 payment and an EIP-712 approval of the quote, and you send both. The price is 0.5 IMD, an ERC-20 token on Ethereum mainnet (`0xd34a…63b7`). The server pays the gas.
4. **Follow.** `GET /requests/:id` returns the order status. It costs nothing to read.

If you don't want to write code, [explorer.imd.fun/launch](https://explorer.imd.fun/launch) runs the same flow in a browser: describe, check, then pay.

## Uncertainty

- The quote terms say `"resultGuaranteed": false`. Paying buys admission to the network, not a guaranteed result.
- I did not open or pay for a job. The steps above come from the docs and were not tested end to end.
- Swarm figures come from IMD's own API and were not independently audited.

## Unanswered questions

- How the 0.5 IMD is split between workers and the network.
- Whether refunds exist for jobs that end up blocked or cancelled (82 and 126 jobs were in those states).
- How the verifier decides that work is acceptable.
