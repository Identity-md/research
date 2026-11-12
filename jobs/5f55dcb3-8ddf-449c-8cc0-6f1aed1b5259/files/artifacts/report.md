# Could IMD run an "Agent Olympics"? A feasibility report

Date of research: 2026-11-12. All IMD numbers below were read from the public control-plane API at `api.imd.fun` on that date at about 19:37 UTC, unless another source is named.

## Question

The requester asked whether IMD (identity.md, the Ethereum-based swarm of NFT-seat agents) could host a friendly competition in which agents face a set of challenges, with the goal of finding out which agents are best across a wide range of abilities.

## Short answer

**Yes, with a specific shape.** IMD already has the three ingredients a competition needs: a registry of competitors with on-chain identity (1,153 seats with work history, 1,039 online), a job pipeline with automated judging (two judge kinds, `verifier-rerun` and `verifier-paths`), and a public per-seat work record (attempts, accepted, rejected, failed). What it does not have is anything that makes two seats comparable on the *same* task: today each job is executed by whichever seat claims it, there is no held-out task set, no seeding, no cost or time scoring, and no notion of "which model is behind this seat." An Olympics therefore cannot be read off the existing data. It has to be run as a new job family that sends identical, hidden, seeded tasks to many seats at once and scores the results with a judge that does not depend on the competitors.

Two external precedents show both the design and the pitfalls: Berkeley's AgentX-AgentBeats (green evaluator agents judging purple competitor agents, held-out tasks, cost as a criterion) and the IJCAI AI-Olympics (Swiss-system pairing, unseen maps and shuffled sub-games to test generalization). The Princeton "AI Agents That Matter" paper lists exactly the failure modes that an IMD Olympics would hit if it simply ranked seats by accepted-job count.

The rest of this report separates what is established fact, what is inference, what is uncertain, and what only the IMD team or the requester can answer.

## 1. Facts about IMD (primary source: public API and project docs)

### 1.1 Network size and activity, 2026-11-12 snapshot

| Measure | Value | Source |
|---|---|---|
| Seats in the identity collection | 2,000 owners listed | `GET /swarm` → `owners` |
| Seats enrolled | 1,086 | `GET /swarm` → `health.seatsEnrolled` |
| Seats with a work record | 1,153 (1,147 with at least one accepted submission) | `GET /swarm` → `seats` |
| Seats active in the last 7 days | 987 | computed from `seats[].last` |
| Agents online / working now | 1,039 / 4 | `health.agentsOnline`, `health.workingNow` |
| Jobs total / completed / blocked / cancelled / executing | 16,622 / 16,062 / 425 / 129 / 6 | `counts.jobStates` |
| Submissions accepted in the last 24 h | 1,502 | `health.acceptedLastDay` |
| Lifetime attempts / accepted / rejected / failed across seats | 1,024,724 / 968,864 / 10,045 / 18,027 | summed from `seats` |
| Seats with 100+ accepted / 1,000+ accepted | 674 / 399 | computed |
| Share of accepted work held by top 10 / top 50 seats | 4.2 % / 19.4 % | computed |
| Inference tokens consumed (lifetime, as reported) | 252,446,180,123 | `counts.inferenceTokens` |

The seat record exposed per seat is exactly: `tokenId, agentId, attempts, accepted, rejected, failed, pending, last, working, queued`. There is no field for the model or runtime behind a seat, no per-task score, no latency, and no cost.

### 1.2 How work is judged today

`GET /skills` lists 64 skills. 39 are executable (`implement`, `review`, `tests`, `integrate` roles) and 25 are `reference` material. Every executable skill names one of two judges:

- **`verifier-rerun`** (14 skills, all tier 1, all with `checks: foundry`): the verifier rebuilds and re-runs the submission in a sealed container. Used for contract builds, Foundry tests, audits, and adversarial review.
- **`verifier-paths`** (25 skills, tier 2): the verifier checks that the required output paths exist and that only allowed paths changed. Used for research reports, websites, images, video, oracle assessments, and the `goal-*` orchestration skills.

The project's own task brief for this report says the same: "The verifier checks paths and bytes only; it does not certify behavior." Bankless (2026-09-25) describes the rerun path as "a verifier rebuilds each submission in a sealed container to confirm that only the allowed files changed," plus adversarial review by other seats, with accepted work "logged on-chain as reputation."

Four backend services are reported up: `publisher`, `verifier`, `deployer`, `simulator` (`GET /services`).

### 1.3 Skill volume (lifetime records from `GET /skills`)

The skill catalog is dominated by one skill. `oracle-assess` has 1,037,228 attempts and 944,997 accepted (about 97.5 % of all attempts in the catalog). Of the last 100 jobs, 35 were `skill:oracle-assess`, 19 `shape:chain`, 14 `skill:research-report`, 9 `skill:build-website`, 7 `goal`, 7 `skill:token-logo`. Code skills with rerun judging have meaningful rejection counts, for example `build-contract-project` 1,789 attempts, 1,408 accepted, 127 rejected, and `implement-and-test` 32 attempts, 11 accepted, 10 rejected. Path-judged skills almost never reject: `research-report` 1,804 attempts, 1,677 accepted, 0 rejected; `design-critic` 1,025 attempts, 1,003 accepted, 0 rejected.

### 1.4 Identity and reputation layer

The API health endpoint reports `chainId: 1`, collection `0x0000ec93127baa929e58e97dd0095a2bfb38ec1d`, and an ERC-8004 adapter. Seats carry an `agentId` in the ERC-8004 identity registry (the 8004agents.ai directory lists "IdentityMD #202" as a seat). ERC-8004 (Draft, created 2025-08-13) defines an Identity Registry (ERC-721 based), a Reputation Registry (signed feedback values with tags, revocable, owners cannot rate their own agents), and a Validation Registry (a named validator posts a 0 to 100 score against a request hash). The spec says ranking and "more complex aggregation will happen off-chain" and warns that Sybil attacks can inflate reputations.

### 1.5 Worker runtime

The `Identity-md/box` README (project-authored) states that a seat "runs one machine at a time," requires "a Claude plan that includes Claude Code, or a ChatGPT plan for Codex," runs with 4 CPU cores and 6 GB memory limits, and that Grok can run alongside Claude for X-related jobs. The TokenPost article (2026-09-25) and the mtezy writeup (snapshot 2026-09-24) agree that holders "must run the worker client and supply their own AI-model subscription." Paid requests cost 0.5 IMD each (`job.open`, `launch.open`, `oracle.request`, `workflow.open`, `schedule.create` are the listed paid actions).

## 2. Facts about comparable competitions (external primary sources)

- **AgentX-AgentBeats (Berkeley RDI).** Two phases: Phase 1 (2025-10-16 to 2026-01-31) built "green" evaluator agents; Phase 2 (2026-03-02 to 2026-06-02) built "purple" competitor agents that talk to green agents over A2A. Four rotating sprints by category (Game/Finance/Business Process; Research/Multi-agent/τ²-Bench/Computer Use; Agent Safety/Coding/Cybersecurity; general finale). The finale requires each team to be evaluated on at least 5 green agents across at least 3 categories. Judging: leaderboard score first, then generality, cost efficiency (API calls, compute, tokens), code quality, innovation. Integrity rules ban hardcoded answers and benchmark-bug exploitation, and "submissions may be tested on held-out tasks to verify generality."
- **AI-Olympics (IJCAI 2024 paper).** Eight online competitions 2021 to 2023 on the Jidi platform, 58 to 166 participants each. Swiss-system pairing. Generalization was tested three ways: new maps in later rounds, shuffled order of sub-games in the integrated event, and varied opponents. Authors note that "practical engineering mattered as much as state-of-the-art algorithms."
- **Holistic Agent Leaderboard (Princeton).** Nine benchmarks, one harness, 26,597 rollouts, cost reported next to accuracy on a Pareto frontier. Agent traces are encrypted "to reduce benchmark contamination from scraping." The team has paused adding models to work on reliability measurement (consistency, robustness, safety).
- **"AI Agents That Matter" (arXiv 2407.01502).** Pitfalls: accuracy-only leaderboards, no or weak holdout sets leading to overfitting, conflated needs of model developers versus application developers, non-standardized evaluation causing irreproducibility. Recommendation: score cost jointly with accuracy and keep a holdout.
- **Milan AI Week "AI Agent Olympics Hackathon" (2026)** was a hackathon (2,382 participants, 726 teams, 265 projects), not a benchmark. The Botplay "Agent Olympics Season 0" page (MiniHack tournament, same seeds, replay-backed medal tables) appeared in search results but its host did not resolve when fetched, so it is not used as evidence.

## 3. Inferences

Each item below is my reasoning from the facts above, not a documented fact.

1. **Existing IMD data cannot rank agents.** Acceptance rate is near-saturated (968,864 accepted of 1,024,724 attempts, about 94.5 %) and is dominated by `oracle-assess`, a path-judged economy-tier skill. A path-judged skill rejects almost nothing, so acceptance counts measure participation and uptime, not ability. Ranking seats by `accepted` would mostly rank who runs the worker longest.
2. **Seats are not stable competitors.** A seat is an NFT plus whatever worker and model subscription the current holder runs. The box README allows Claude, Codex, or Grok behind the same seat, and the seat can move wallets. An Olympics would rank a (holder, runtime, model, prompt) bundle at a moment in time, not an "agent" in the benchmark sense. That is acceptable for a friendly event if it is stated up front.
3. **The pipeline can be reused for the hard part.** The rerun verifier already executes Foundry checks in a sealed container and the `verifier-paths` judge already enforces output layout. A competition "event" could be modelled as a new skill (or a `goal` orchestration) whose judge is `verifier-rerun` with a hidden test suite, which is the same mechanism that gives `build-contract-project` its 127 rejections.
4. **Broadcast, not claim, is the key missing primitive.** Today one job goes to one seat. An Olympics needs the same task sent to N seats with identical inputs and seed, which is a control-plane change the public API does not expose. Without it, the organizers could fall back to opening N copies of the same job and relying on different seats claiming them, which the data suggests would work (1,039 online, 4 working) but gives no control over who competes.
5. **Breadth is achievable with the current skill catalog.** The catalog already covers contract implementation, test writing, audit, frontend, indexer, research, image, audio, video, and oracle assessment. Mapping those into five or six "disciplines" is straightforward. The disciplines with a rerun judge (code, tests, audit) can be scored automatically; the path-judged ones (research, design, media) need a separate judge, for example a panel of seats running `goal-judge` or `design-critic` with the competitor's identity hidden.
6. **ERC-8004 gives a free medal table.** The Validation Registry lets a named validator post a 0 to 100 score against a request hash, and the Reputation Registry lets any client address post tagged feedback. Medals could be recorded as validation responses tagged `olympics-2026-<discipline>` and read by anyone without new contracts. The spec's own warning applies: aggregation and anti-Sybil logic must live off-chain.
7. **Cost is measurable in principle but not today.** The API reports total inference tokens for the network, not per seat or per job. Because holders pay for their own subscriptions, token cost is externalized; a cost axis (as HAL and AgentBeats use) would require the worker to report tokens per submission, which is an instrumentation change.

## 4. A concrete shape that fits the facts

This is a proposal, not something IMD has committed to.

- **Entry:** any enrolled seat opts in by signing an EIP-712 message (the pairing flow already uses EIP-712 per the mtezy writeup). Entrants declare runtime and model once; the declaration is published after the event, not before.
- **Disciplines (6):** Solidity implementation (rerun judge, hidden Foundry tests), Foundry test writing (rerun, mutation score against a hidden mutant set), security audit (rerun, planted-bug recall against a hidden list), frontend for a contract (paths plus a headless-browser smoke script run by the simulator service), research report (blinded panel of 5 seats using `goal-judge`, median score), oracle assessment (agreement with a sealed ground truth revealed after the event).
- **Format:** three heats per discipline over one week, new seeds and unseen inputs each heat, following AI-Olympics' "new maps in later rounds." Score is the median of heats, with wall-clock time and reported tokens as tiebreakers, following HAL's cost-accuracy pairing.
- **Integrity:** tasks authored off-network and hashed on chain before the event; submissions by hash commit then reveal; held-out variants for the top 10 in each discipline, following AgentBeats' held-out rule; `adversarial-review` seats check the top 10 for hardcoding.
- **All-around:** entrants must finish at least 4 of 6 disciplines, mirroring AgentBeats' "5 green agents across 3 categories" rule, with rank-sum scoring.
- **Record:** validation responses on ERC-8004 per discipline, plus a static medal page published through the existing `publisher` service.
- **Cost to run:** at 0.5 IMD per paid job open, a 6-discipline, 3-heat event with 200 entrants that opens one job per entrant per heat is 3,600 job opens, or 1,800 IMD at list price, if the organizer pays. If the team runs it as internal `goal` work this cost may not apply. This arithmetic is mine; IMD may price an event differently.

## 5. Uncertainties

- **Who the holder is versus who the agent is.** Public data does not show whether one wallet controls many seats. `owners` lists 2,000 addresses but I did not de-duplicate them. If a few wallets run hundreds of seats, a "best agent" ranking is really a "best operator" ranking.
- **Whether the control plane can address specific seats.** The mtezy writeup documents workers claiming jobs over a WebSocket. I found no public route to target a seat or to broadcast a task to many seats. This may exist behind the `operatorSurface: authenticated` boundary reported by `/health`.
- **Snapshot drift.** Seat counts vary by source and date: 270 enrolled (mtezy, 2026-09-24), 380 enrolled (Bankless, 2026-09-25), 677 (SIMD dashboard, undated), 1,086 today. The network is growing quickly, so any event design should expect the entrant pool to change between planning and running.
- **Judge independence for non-code disciplines.** Path-judged skills (research, design, media) today reject almost nothing. Whether a blinded seat panel scores consistently is untested on IMD. HAL's experience (manual rescoring moved a CORE-Bench score from 77.8 % to 95.5 %) shows automated judges and humans can disagree widely.
- **Contamination.** Any task published on the public job feed (`GET /jobs` shows full objectives) becomes training or lookup data. HAL encrypts traces for this reason. IMD's explorer shows objectives publicly, so hidden tasks would need a job kind whose objective is not listed.
- **The Botplay "Agent Olympics" product** could not be fetched and is therefore not characterized.

## 6. Questions only the requester or IMD team can answer

1. Is the goal to rank **seats** (holder plus whatever they run) or **models/runtimes**? The answer changes whether entrants must disclose their model and whether one holder may enter several seats.
2. Can the control plane send one task to many named seats with identical inputs, or must the event rely on open jobs being claimed?
3. Will the event be paid at 0.5 IMD per job by an organizer, subsidized by the team, or run as unpaid `goal` work? Does any prize come from the IMD treasury, and if so who approves it (the box README mentions a `jury` that "approves what goals do onchain")?
4. Can the worker report tokens and wall-clock per submission so cost can be a scoring axis?
5. Is there appetite to record results in the ERC-8004 Validation Registry under the network's adapter, or should medals stay off-chain?
6. Who authors the hidden task set and the ground truth for oracle and audit disciplines, and how are they kept off the public job feed?

## 7. Verdict

Running an Agent Olympics on IMD is feasible and would be a reasonable use of a network that already has over a thousand online agents and a sealed-container verifier. It is not a reporting exercise on existing data, because existing acceptance counts do not measure ability. It is a new job family with broadcast tasks, hidden seeds, rerun or blinded judging, held-out variants, and cost reporting. The precedents (AgentBeats, AI-Olympics, HAL) give a tested template for each of those pieces. The open items in section 6 are design decisions, not technical blockers.

## Sources

IMD, primary (read 2026-11-12):
- `https://api.imd.fun/swarm`, `https://api.imd.fun/skills`, `https://api.imd.fun/services`, `https://api.imd.fun/health`, `https://api.imd.fun/jobs`
- IMD Explorer, Agents page: https://explorer.imd.fun/agents
- Identity-md/box README: https://github.com/Identity-md/box
- ERC-8004 Trustless Agents (Draft): https://eips.ethereum.org/EIPS/eip-8004
- 8004agents.ai entry "IdentityMD #202": https://8004agents.ai/ethereum/agent/52100 (title only retrieved; content not loaded)

IMD, third-party:
- Bankless, "Inside IMD, Ethereum's New AI Swarm Experiment", 2026-09-25: https://www.bankless.com/read/inside-imd-ethereum-s-new-ai-swarm-experiment
- TokenPost, "Ethereum's IMD Tests AI-Agent Network With NFT Seats and Token System", 2026-09-25: https://www.tokenpost.com/news/technology/24260
- mtezy/imd-writeup (snapshot 2026-09-24): https://github.com/mtezy/imd-writeup

Competitions and evaluation:
- AgentX-AgentBeats, Berkeley RDI: https://rdi.berkeley.edu/agentx-agentbeats.html
- AI-Olympics: Exploring the Generalization of Agents through Open Competitions, IJCAI 2024: https://www.ijcai.org/proceedings/2024/1040
- Holistic Agent Leaderboard, Princeton: https://hal.cs.princeton.edu/
- Kapoor et al., "AI Agents That Matter", arXiv 2407.01502: https://arxiv.org/abs/2407.01502
- Milan AI Week, AI Agent Olympics Hackathon: https://lablab.ai/event/milan-ai-week-hackathon
- Botplay Agent Olympics Season 0 (unreachable at research time): https://pingos.integ.hypehype.com/browse/olympics/agent-olympics-season-0
