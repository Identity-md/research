# ERC-8004: a practical guide for AI-agent developers

**Research checked: 4 October 2026.** ERC-8004, “Trustless Agents,” is a **Draft** Ethereum application standard. It gives agents portable on-chain identifiers and interoperable trust signals so applications can discover and select providers across organizational boundaries. It does not certify that an agent is honest, competent, or even operational. This guide labels specification behavior, implementation choices, and application recommendations separately. [Official specification](https://eips.ethereum.org/EIPS/eip-8004); [specification source snapshot](https://github.com/ethereum/ERCs/blob/365b4c02879f3e882b91281d42b4f57b406205e9/ERCS/erc-8004.md).

## 1. What problem does it solve?

Agent communication and tool protocols such as A2A and MCP provide ways to advertise capabilities and invoke services. ERC-8004 supplies a shared blockchain layer for identifying providers and publishing evidence about their work, reducing dependence on a single platform's directory or private ratings database. Its specification defines three registries:

| Registry | Defined purpose | What the application still decides |
| --- | --- | --- |
| Identity | ERC-721 agent identity pointing to a registration document | Whether the advertised provider meets its requirements |
| Reputation | Public feedback submission and retrieval | Which reviewers, metrics, and scoring policy to trust |
| Validation | Requests and responses for independent checks of work | Which validator and verification method provide sufficient assurance |

Payments, execution, and validation incentives/slashing are outside this standard. x402, TEE attestations, and zkML can complement it; registering an agent does not supply any of them automatically. [Specification: motivation and validation](https://github.com/ethereum/ERCs/blob/365b4c02879f3e882b91281d42b4f57b406205e9/ERCS/erc-8004.md).

## 2. Register, discover, and resolve an identity

**Specification.** An identity is the pair `agentRegistry` and `agentId`. The registry identifier has the form `eip155:{chainId}:{identityRegistryAddress}`; `agentId` is that registry's ERC-721 token ID. A bare token ID, name, or wallet is not globally unique. The token owner controls the agent identity, with approved operators able to manage it. Ownership is transferable. [Identity specification](https://github.com/ethereum/ERCs/blob/365b4c02879f3e882b91281d42b4f57b406205e9/ERCS/erc-8004.md); [ERC-721 ownership and approvals](https://eips.ethereum.org/EIPS/eip-721).

A practical registration sequence is:

1. Select a chain and a known registry deployment. Call `register()` or `register(string agentURI)`; obtain the assigned ID from the `Registered` transaction event.
2. Publish the registration JSON with `type` set to `https://eips.ethereum.org/EIPS/eip-8004#registration-v1`, presentation fields such as `name`, `description`, and `image`, a `services` list, and a `registrations` entry containing the full registry identifier and assigned ID. Include `active`, `x402Support`, and optional `supportedTrust` as appropriate. Advertising a trust model is a claim, not proof.
3. If necessary, call `setAgentURI(agentId, uri)` after publishing. HTTP(S), IPFS, and base64 JSON data URIs are supported. Starting with `register()` avoids guessing the ID before constructing the document.
4. Discover candidates by indexing `Registered`, `URIUpdated`, and ERC-721 `Transfer` events, then fetching their documents. Resolve a candidate with `ownerOf(agentId)` and `tokenURI(agentId)` on the specified chain/registry. The specification calls the latter URI `agentURI`; use the deployed ABI's actual function names.

The service list can point to an A2A agent card, MCP endpoint, ENS name, or other services. Rich search is an indexer feature, not a standardized registry search API. For optional HTTPS endpoint control checks, fetch `https://{endpoint-domain}/.well-known/agent-registration.json` and match its registration pair. The specification permits skipping this additional check when the primary registration document is served by the same domain. [Registration and domain verification](https://github.com/ethereum/ERCs/blob/365b4c02879f3e882b91281d42b4f57b406205e9/ERCS/erc-8004.md).

**Wallet binding.** `getAgentWallet(agentId)` returns a payment address, initially the owner's address. Changing it with `setAgentWallet` requires proof of control of the new wallet: EIP-712 signing for EOAs or ERC-1271 validation for contract wallets. The wallet is cleared on token transfer and must be rebound. This binds a wallet to the identity; it does not prove the provider's legal identity or authenticate every API response. [Wallet rules](https://github.com/ethereum/ERCs/blob/365b4c02879f3e882b91281d42b4f57b406205e9/ERCS/erc-8004.md); [EIP-712](https://eips.ethereum.org/EIPS/eip-712); [ERC-1271](https://eips.ethereum.org/EIPS/eip-1271).

## 3. Reputation and feedback

**Specification.** Any client address can call:

```solidity
function giveFeedback(
    uint256 agentId, int128 value, uint8 valueDecimals,
    string calldata tag1, string calldata tag2, string calldata endpoint,
    string calldata feedbackURI, bytes32 feedbackHash
) external;
```

The agent must exist; the sender cannot be its owner or approved operator. Clients need no agent registration or agent-issued feedback authorization. Here “signed value” means a numeric value that may be negative, not a separately signed review payload. Transactions identify the submitting address. Interpret the number as `value / 10**valueDecimals`, with decimals restricted to 0–18. For example, `9977, 2` represents `99.77`. Tags define application-specific meaning: quality scores, uptime, latency, and financial returns must not be mixed into one average. [Feedback specification](https://github.com/ethereum/ERCs/blob/365b4c02879f3e882b91281d42b4f57b406205e9/ERCS/erc-8004.md).

Optional strings can be empty and the optional hash zero. An off-chain feedback file can carry task context and payment evidence. For a non-content-addressed file, a supplied `feedbackHash` commits to its exact bytes using **Keccak-256**, not NIST SHA3-256. The registry stores the value, decimals, tags, and revocation flag. The endpoint, file URI, and hash are in `NewFeedback` logs rather than contract storage, so retrieve logs to verify the full evidence. Content addressing/hashing proves integrity, not truth or availability. [Feedback storage and files](https://github.com/ethereum/ERCs/blob/365b4c02879f3e882b91281d42b4f57b406205e9/ERCS/erc-8004.md).

A client can `revokeFeedback(agentId, feedbackIndex)` for its own review; this marks revocation without erasing history. Anyone can `appendResponse(...)`, for example to publish refund evidence or dispute a review. A response is an attributed statement, not automatic adjudication. Feedback is identified by agent ID, client address, and a per-client, per-agent 1-based index. Read with `readFeedback`, `readAllFeedback`, `getClients`, and `getLastIndex`. [Reputation interface](https://github.com/ethereum/ERCs/blob/365b4c02879f3e882b91281d42b4f57b406205e9/ERCS/erc-8004.md).

`getSummary(agentId, clientAddresses, tag1, tag2)` requires a non-empty reviewer list. **Implementation-specific:** the team's current Solidity implementation averages matching, non-revoked submissions after decimal normalization, returning the most frequent input decimal precision with truncation. It is not one vote per reviewer; repeated submissions contribute repeatedly. Deduplicate the supplied reviewer addresses and inspect raw feedback if frequency matters. The specification supplies the interface, not a universal reputation algorithm. [Implementation of aggregation](https://github.com/erc-8004/erc-8004-contracts/blob/b9e466c250744a7e06b13dff9d3c2844ed64f825/contracts/ReputationRegistryUpgradeable.sol).

## 4. How to verify before using an agent

**Recommended application policy, derived from the interfaces and threat model:**

1. Use a configured registry deployment and confirm RPC chain ID, deployed code, and that `reputation.getIdentityRegistry()` equals the intended identity registry. Check current state at a sufficiently confirmed block; a search result is only a candidate.
2. Resolve token ownership and URI, validate the document, match its registration pair, and perform the endpoint-domain check where relevant. Inspect the current wallet before paying. Use a separate authenticated session or signed challenge if live endpoint authentication is required; ERC-8004 does not define such a challenge protocol.
3. Select trusted reviewer addresses independently. Query feedback with consistent tags and units, exclude revoked entries, and inspect count, recency, repeated submissions, and evidence. Display the policy and sample size alongside any score. No feedback is “unknown,” not evidence of safety.
4. Fetch evidence from event logs and verify hashes/CIDs. Check claimed payment transactions separately if your policy requires paid interactions. The feedback call itself does not establish that a task or payment happened.
5. For valuable tasks, require an appropriate validator or independent checks. The validation interface accepts `validationRequest(...)` from the owner/operator and `validationResponse(...)` from the requested validator, with a 0–100 result. Verify the validator and evidence rather than treating “100” as a universal guarantee.

These steps follow the [specification's interfaces and security considerations](https://github.com/ethereum/ERCs/blob/365b4c02879f3e882b91281d42b4f57b406205e9/ERCS/erc-8004.md). They are application policy, not an ERC-mandated trust threshold.

## 5. Practical example: selecting an invoice-extraction agent

**Illustrative design, not an existing deployment.** A provider registers an agent on Sepolia, publishes its MCP invoice-extraction endpoint, and binds its payment wallet. A purchasing application discovers candidates through an indexer, resolves each on-chain identity, and checks endpoint control.

The application evaluates feedback from its own customers or approved auditors under `tag1="invoice_accuracy"`, `tag2="schema_v1"`, using a documented 0–100 scale. It applies its own minimum sample and freshness rules, runs a small test job, then invokes the selected MCP tool. After checking the extracted fields, the customer's address submits:

```text
giveFeedback(agentId, 95, 0, "invoice_accuracy", "schema_v1",
             endpoint, feedbackURI, feedbackHash)
getSummary(agentId, trustedReviewerAddresses,
           "invoice_accuracy", "schema_v1")
```

These are contract-call sketches, not executable SDK code. Keep customer invoices private; publish only consented, redacted evidence. Payment and any escrow remain separate application integrations. If ownership or the endpoint changes, re-evaluate the provider before sending the next job.

## 6. Contracts and integration tools

**Team implementation, not standard-mandated addresses.** The [contracts README](https://github.com/erc-8004/erc-8004-contracts/blob/b9e466c250744a7e06b13dff9d3c2844ed64f825/README.md) lists:

| Ethereum network | Identity Registry | Reputation Registry |
| --- | --- | --- |
| Mainnet, chain 1 | `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432` | `0x8004BAa17C55a88189AE136b182e5fdA19dE9b63` |
| Sepolia, chain 11155111 | `0x8004A818BFB912233c491871b3d84c89A494BD9e` | `0x8004B663056A597Dffe9eCcC1965A193B7388713` |

Use the repository's [ABIs](https://github.com/erc-8004/erc-8004-contracts/tree/b9e466c250744a7e06b13dff9d3c2844ed64f825/abis) with an EVM library such as ethers or viem. Addresses above are repository-reported; this research did not independently inspect live bytecode or deployment governance.

[Agent0 TypeScript SDK](https://github.com/agent0lab/agent0-ts/blob/a6fb48773cdeb02af77cccda2a610ec81049d4b2/README.md) provides registration, IPFS publishing, search, and feedback helpers. Consult its [quick-start](https://github.com/agent0lab/agent0-ts/blob/a6fb48773cdeb02af77cccda2a610ec81049d4b2/examples/quick-start.ts) and [feedback example](https://github.com/agent0lab/agent0-ts/blob/a6fb48773cdeb02af77cccda2a610ec81049d4b2/examples/feedback-usage.ts). SDK shortcuts such as `chainId:agentId` rely on configured registry addresses; preserve the full standard identity when exchanging data externally. Agent0's [subgraph](https://github.com/agent0lab/subgraph) offers GraphQL discovery. SDK search, storage providers, and indexing are implementation conveniences, with their own availability and freshness assumptions.

## 7. Limitations, trade-offs, and open questions

- **Sybil resistance remains external.** Blocking owner/operator feedback does not block alternate wallets, collusion, or purchased reviews. Reviewer filtering helps only if reviewer selection is sound. No common scoring scale or universal trustworthy-reviewer list is defined. [Specification security considerations](https://github.com/ethereum/ERCs/blob/365b4c02879f3e882b91281d42b4f57b406205e9/ERCS/erc-8004.md).
- **Ownership and behavior can change.** A transferable ID can retain historical feedback while a new operator changes the model or service. Treat transfer and metadata updates as reasons to refresh confidence. Multiple chain registrations do not automatically merge reputation or prove they share an operator. These are application-level implications of the identity model. [Identity and deployment rules](https://github.com/ethereum/ERCs/blob/365b4c02879f3e882b91281d42b4f57b406205e9/ERCS/erc-8004.md).
- **Storage has costs and failure modes.** HTTPS is mutable; IPFS needs continued hosting/pinning; data URIs cost gas. Public transactions and hashes persist after revocation. Recommendation: minimize sensitive data, sandbox metadata/evidence fetching against SSRF and oversized payloads, and treat fetched content as untrusted input. Indexers may lag; large feedback histories also make unbounded reads/aggregation expensive, as the implementation loops over submissions. [URI and persistence rules](https://github.com/ethereum/ERCs/blob/365b4c02879f3e882b91281d42b4f57b406205e9/ERCS/erc-8004.md); [read implementation](https://github.com/erc-8004/erc-8004-contracts/blob/b9e466c250744a7e06b13dff9d3c2844ed64f825/contracts/ReputationRegistryUpgradeable.sol).
- **Upgrade governance is an additional trust assumption.** The team implementation uses owner-authorized UUPS upgrades. Proxy administration is separate from ownership of an individual agent NFT. Inspect the actual deployment's implementation and administrator; a stable address need not imply stable code. [Upgradeable implementation documentation](https://github.com/erc-8004/erc-8004-contracts/blob/b9e466c250744a7e06b13dff9d3c2844ed64f825/UPGRADEABLE_IMPLEMENTATION.md).
- **Validation is particularly unsettled.** The specification defines validation hooks, but the team README says that section is under active revision with the TEE community; Agent0 lists validation support as forthcoming. Do not assume a usable validation deployment or SDK flow merely because the interface exists. Validator economics, meaningful task-specific correctness, reviewer weighting, and safe cross-chain reputation aggregation remain integration questions. [Team implementation caveat](https://github.com/erc-8004/erc-8004-contracts/blob/b9e466c250744a7e06b13dff9d3c2844ed64f825/README.md#validation-registry); [SDK roadmap](https://github.com/agent0lab/agent0-ts/blob/a6fb48773cdeb02af77cccda2a610ec81049d4b2/README.md).

## Evidence and scope

Primary sources are linked beside the claims they support; repository links are pinned to the revisions retrieved during research. The official EIP page supplies current publication status, while the pinned ERC source records the technical specification used here. No agent was deployed, no transaction or SDK example was executed, and no independent contract audit or live-network verification was performed. The example and verification policy are explicitly proposed designs. Draft status and implementation roadmaps can change; recheck the specification, ABI, and deployment before integration.
