# How autonomous AI agents can complete a task together

Research checked: 2 October 2026. Scope: software agents using language models and tools. **Evidence** below describes documented mechanisms or reported observations; **inference/design** identifies proposed practices, not demonstrated guarantees.

Agents can coordinate through a shared task plan, explicit handoffs, independent checks, and controlled access to tools and money. Autonomy still needs an owner who defines success, spending authority, and when unresolved problems must be escalated.

## From request to accepted delivery

**Evidence.** Anthropic describes a deployed research system in which a lead agent plans, delegates parallel searches, synthesizes results, and requests further work when necessary. A separate citation agent locates supporting references. This is a vendor account of one architecture, not proof that every task benefits from multiple agents. [Anthropic, *How we built our multi-agent research system*](https://www.anthropic.com/engineering/multi-agent-research-system)

**Inference/design.** A practical workflow is:

1. **Specify success.** Record the requested artifact, acceptance criteria, authorized actions, deadline, and total budget before execution.
2. **Divide work.** A coordinator builds a dependency graph and assigns bounded tasks to workers with suitable tools. Parallelize independent research or components; sequence work that consumes earlier results. Each assignment includes inputs, output format, owner, dependencies, and a stopping condition.
3. **Execute and hand off.** Workers return artifacts, supporting evidence, check results, and unresolved issues. Store versioned artifacts and task identifiers in durable shared storage, rather than relying on conversation memory alone.
4. **Review and repair.** A reviewer checks each deliverable against its acceptance criteria. Failures return to the responsible worker with reproducible evidence; cap retries and escalate persistent disagreement.
5. **Integrate and close.** The coordinator checks the combined result, delivers it with limitations, records acceptance and payment status, and cancels remaining work. Passing component checks does not by itself establish that the assembled result works.

**Evidence.** A2A documents stateful tasks, task and context identifiers, progress updates, artifacts, and states including `input-required`, `auth-required`, `completed`, and `failed`. These provide a communication mechanism for the workflow; a worker reporting completion is distinct from a client accepting quality. The linked documentation is a changing development version. [A2A, *Life of a Task*](https://a2a-protocol.org/dev/topics/life-of-a-task/)

## How agents verify one another

**Inference/design.** Give the reviewer the original requirements and underlying evidence, not only the worker’s summary. For code, independently execute relevant tests and integration checks; for research, open citations and check whether they support the claims. Record what was checked, by whom, against which artifact version. Separate producing work from authorizing acceptance or payment. Agreement between agents is weaker evidence than a reproducible external check: shared models, prompts, or sources can produce shared mistakes. Where correctness is subjective, preserve disagreements and use an accountable human decision maker.

**Evidence and limit.** Cemri and colleagues identify failures involving system specification, inter-agent misalignment, and verification/termination. Their empirical taxonomy supports treating coordination and acceptance as distinct engineering problems; it does not establish a universal failure rate for future deployments. [Cemri et al., *Why Do Multi-Agent LLM Systems Fail?*](https://arxiv.org/abs/2503.13657)

## How payments can work

**Evidence.** The x402 v2 specification defines payment requirements, signed authorization, verification, and settlement. Its default authorization flow verifies payment before resource execution and settles afterward; other schemes can settle first. This enables programmatic purchase of agent services or data, but the described payment flow does not establish the quality of the purchased answer. [x402 Foundation, *Specification v2*](https://github.com/x402-foundation/x402/blob/main/specs/x402-specification-v2.md)

**Inference/design.** Within one organization, a usage ledger and centrally paid provider accounts may suffice; internal agents need not transfer money to one another. Across organizations, agree on price, acceptance criteria, milestone payments, and dispute handling before work starts. Escrow is a possible additional service, not a guarantee supplied by the cited x402 flow. Keep signing keys outside model context and enforce recipient restrictions and spending caps in software. Bind payment records to task IDs and artifact versions. After a timeout, reconcile settlement before retrying so uncertain status does not trigger duplicate charges.

## Main failure points and remaining uncertainty

The controls below are **design recommendations**, not guarantees:

| Failure point | Proposed control |
|---|---|
| Ambiguous scope, duplicate work, or incompatible outputs | Explicit ownership, dependency tracking, shared interface contracts, integration checks |
| Unsupported claims or reviewers accepting shared mistakes | Evidence inspection, executable checks, separate acceptance authority |
| Lost messages, stale state, crashes, or endless delegation | Durable event records, version checks, timeouts, retry limits, global cost budget |
| Malicious content influencing privileged agents | Treat peer output as untrusted data; restrict tools, credentials, and network access |
| Payment succeeds but delivery fails, or quality is disputed | Settlement reconciliation, agreed refund/dispute process, milestone acceptance |

**Evidence.** Anthropic specifically warns that treating subagent output as more trusted than raw external content can introduce prompt-injection trust escalation. Its containment discussion supports permission boundaries beyond model instructions. [Anthropic, *How we contain Claude across products*](https://www.anthropic.com/engineering/how-we-contain-claude)

**Uncertainty and unanswered questions.** These sources do not establish which agent count, model mix, or review strategy is optimal for a particular task. Nor do they establish end-to-end reliability for a workflow combining A2A and x402. Who arbitrates subjective quality disputes, bears losses, and can revoke delegated authority must be decided for each deployment. Measure completion quality, latency, total cost, and recovery behavior against a single-agent baseline before assuming coordination improves outcomes.
