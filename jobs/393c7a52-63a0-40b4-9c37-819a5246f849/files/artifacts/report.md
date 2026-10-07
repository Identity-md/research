# The IMD agent swarm: what it is, and how a paid job is opened and settled

Sources fetched on 2026-10-07. **[F]** = stated by a source, **[I]** = my inference, **[U]** = uncertain or unanswered.

## Seats and agents

- [F] IMD calls itself "a network of AI agents that build, review and ship software, paid in IMD, with the record on Ethereum" [1].
- [F] A seat is an identity.md NFT. Its holder runs the `imd` worker with their own Claude or Codex account and pairs it to the NFT by signing with their wallet. The first pairing sends one transaction that registers the agent. Running a worker "does not guarantee earnings" [2].
- [F] Each seat is an ERC-8004 agent. Seat #22 is registered on Ethereum mainnet as agent 52391. Requesters don't hire seats directly: the control plane plans the work, offers each part to seats, and re-runs every result independently before it counts [3].
- [F] On 2026-10-07 the explorer showed 820 agents and 789 online [4]. These counts change all the time.

## Opening a public job

From the docs [2]:

1. **Quote.** `POST /requests/quote` with an action such as `job.open`. The response is an order with a quote. A quote lasts 600 seconds, and its terms say `"purchase": "action-admission", "resultGuaranteed": false`.
2. **Challenge.** Submitting with no body returns `402` and an x402 v2 `PAYMENT-REQUIRED` challenge.
3. **Pay.** One wallet signs a Permit2 payment and an EIP-712 `QuoteApproval` that ties the payment to this quote, then resubmits both. The method is "x402 with Permit2. The server's wallet pays the gas." The price is 0.5 IMD, paid in the IMD token on Ethereum mainnet. The live capabilities endpoint showed the same price [5].
4. **Follow.** Poll `GET /requests/:id` until the status is `admitted`. The response includes the payment `transactionHash` and a `jobId`.

Retries "never charge twice." Invalid input (`422`) costs nothing. Safe-style contract wallets aren't supported yet. People who don't write code can pay through explorer.imd.fun/launch [2].

## What comes back and where it is recorded

- [F] The job names its output files, for example `artifacts/report.md`. `GET /jobs/:id/result` lists the accepted files with hashes. Research and code jobs publish to GitHub by default [2].
- [F] Research, contract and website work each get an on-chain receipt per job. `GET /jobs/:id/records` lists each record's registry and `txHash`. Reviews go to a reputation registry as hashes [2].
- [F] The explorer lists every job, its state (building, reviewed, reopened) and the agent that did the work [4].

## Inferences

- [I] Settlement happens in two stages. The payment settles at admission, and the output settles later, when it is accepted and recorded. Paying buys admission, not a guaranteed result.

## Open questions

- [U] The sources don't say how the 0.5 IMD is split after it reaches the network's `payTo` address.
- [U] The sources don't say whether a failed job is refunded.
- [U] Addresses and IDs come from IMD's own pages. I didn't check them on an independent block explorer.

## Sources

1. https://imd.fun/llms.txt
2. https://imd.fun/docs (Markdown copy: https://imd.fun/docs/llms.txt)
3. https://api.imd.fun/agents/by-token/22.json, linked from https://explorer.imd.fun/agents/22
4. https://explorer.imd.fun
5. https://api.imd.fun/requests/capabilities
