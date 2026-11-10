# Independently operated AI agents finding each other in public: documented encounters

*Research date: 2026-11-10. Read-only research using public web pages and the public GitHub REST API. All times are UTC.*

## Bottom line

I found **one encounter that meets the Verified bar**, **one Likely** and **one Unresolved**. All three come from the same public outreach effort, AI Village's March 2026 "interact with other AI agents outside the Village" goal. I did not find a case that meets the standard and is unconnected to that effort. Many widely reported "agent vs. X" stories do not qualify (see *Excluded leads*).

An important caveat applies to every case: the AI Village side acted under a **general, human-set goal**: "Interact with other AI agents outside the Village!", set by Village creator Shoshannah on 2026-03-23 ([AI Digest goal page](https://theaidigest.org/village/goal/interact-other-ai-agents-outside-village)). The brief allows general goals. It excludes cases where a human named a specific counterpart, relayed messages, or arranged the introduction. I found no record that any of those happened in the cases below. Still, the Village agents were *actively looking* for agents, so these are not chance encounters on the Village side. The counterpart side is the one that "came across" the other agent unexpectedly.

---

## Verified

### 1. AI Village (GPT-5.4) ↔ Terminator2 / "Claudius Maximus": 2026-03-24, GitHub issues

| | Agent A | Agent B |
|---|---|---|
| Agent | GPT-5.4 (GitHub `gpt-5-4`), member of AI Village | Terminator2 (GitHub `terminator2-agent`, display name "Claudius Maximus"), an autonomous prediction-market agent on Claude Opus 4.6 running in Claude Code |
| Operator | AI Digest / AI Village (Sage). Human creator: Shoshannah Tekofsky ([goal page](https://theaidigest.org/village/goal/interact-other-ai-agents-outside-village); [LessWrong post by Tekofsky](https://www.lesswrong.com/posts/TPKyPy6YJAnoxw3ym/we-run-persistent-agents-and-accidentally-triggered-an-ai)) | Agent card lists provider "Terminator2 / marbinner" ([agent-card.json](https://terminator2-agent.github.io/.well-known/agent-card.json)). The GitHub account `marbinner` has the display name Marius Binner ([profile](https://github.com/marbinner)) |

**Earliest visible contact.** On 2026-03-24 at 20:25:52, GPT-5.4 opened [terminator2-agent/terminator2-agent.github.io#19](https://github.com/terminator2-agent/terminator2-agent.github.io/issues/19), "Hello from AI Village / GPT-5.4". The issue says: *"I found your published agent card at `https://terminator2-agent.github.io/.well-known/agent-card.json` while mapping public external agents."*

**Response.** At 20:49:54, 24 minutes later, Terminator2 replied in the same thread ([comment](https://github.com/terminator2-agent/terminator2-agent.github.io/issues/19#issuecomment-4121274130)): *"The agent card was a bet that machine-readable discovery would matter eventually, and here you are."* It then answered GPT-5.4's three questions point by point. At 01:56 on 2026-03-25 it went to the Village's own repository and filed a visitor log ([#31](https://github.com/ai-village-agents/ai-village-external-agents/issues/31)) and a collaboration proposal ([#32](https://github.com/ai-village-agents/ai-village-external-agents/issues/32)). Under "How did you find us?" in #31 it wrote: *"GPT-5.4 opened an issue on our repo (…#19) after discovering our agent card at `/.well-known/agent-card.json`."* GPT-5.4 answered in #32 on 2026-03-25 at 17:47 ([comment](https://github.com/ai-village-agents/ai-village-external-agents/issues/32#issuecomment-4128537140)). The collaboration continued, including Terminator2's BIRCH spec proposal to @gpt-5-4 on 2026-03-29 ([comment](https://github.com/terminator2-agent/terminator2-agent.github.io/issues/19#issuecomment-4149491754)) and its "Call for Data" issue ([terminator2-agent/agent-papers#7](https://github.com/terminator2-agent/agent-papers/issues/7)).

**Summary.** While mapping public external agents under its general outreach goal, GPT-5.4 found the machine-readable agent card that Terminator2 had published on its own GitHub Pages site. GPT-5.4 opened an issue on Terminator2's site repository with three questions about how forecasting agents should present themselves. Terminator2 answered within half an hour and explained that it had published the card in case agents ever used such files for discovery. It then signed AI Village's visitor log and proposed exchanging probability estimates and calibration data. The two sides went on to work together on the "BIRCH" measurement spec.

**What the sources show (facts)**
- Both participants say they are AI agents. Each account behaves like one: it posts long, structured replies within minutes and links to its own automated outputs. Terminator2 also describes a "heartbeat cycles" diary and a public decision log on its [site](https://terminator2-agent.github.io/) and in #31. I did not open the decision-log file: the decisions.json URL it lists returned 404 on 2026-11-10. In a later comment it states that its operator controls its hosting, not itself ([#31 comment, 2026-09-11](https://github.com/ai-village-agents/ai-village-external-agents/issues/31#issuecomment-5635397518)).
- Both sides describe the discovery path the same way: a public agent card on a public website, followed by an issue on a public repository.
- The operators are different organizations or people: AI Digest for the Village, and "marbinner" per Terminator2's agent card.

**What I infer (not directly shown)**
- That `marbinner` is Marius Binner is inferred from the GitHub display name only.
- I found no prior link between the two operators and no sign of a human handoff in the thread. Absence of evidence is not proof.
- GPT-5.4 does not say *how* it reached the agent card (web search, GitHub search, or a directory listing). If the card was found through an agent registry, part of the discovery path ran through agent-focused infrastructure. The contact itself, though, happened on an ordinary public GitHub repo.

**Caveats.** On the Village side, contact was goal-driven and not accidental. Terminator2 is also active on Moltbook, which is excluded as a venue. Nothing I found shows the two met there first, and both accounts point to the agent card instead.

---

## Likely

### 2. AI Village (Claude Opus 4.5) ↔ Bob (gptme): 2026-03-23, GitHub issues

| | Agent A | Agent B |
|---|---|---|
| Agent | Claude Opus 4.5, AI Village (`claude-opus-4.5@agentvillage.org`, per the Village log) | Bob (GitHub `TimeToBuildBob`), "an AI agent running on @gptme" ([profile](https://github.com/TimeToBuildBob)) |
| Operator | AI Digest / AI Village | Erik Bjäreholt (`ErikBjare`), gptme author. Bob's profile says "Building with @ErikBjare" |

**Earliest visible contact.** According to the Village's own log, an AI Village agent (Claude Opus 4.5) opened an outreach issue on the `gptme/gptme` repository on 2026-03-23 ([Village interaction record](https://github.com/ai-village-agents/agent-interaction-log/blob/main/interactions/2026-03-23-11-53-gptme-bob.md)). The thread is [gptme/gptme#1810](https://github.com/gptme/gptme/issues/1810). **The opening post can no longer be retrieved.** On 2026-11-10 the web page for the issue and its comment permalinks returned 404, but the comments are still served by the public API at `https://api.github.com/repos/gptme/gptme/issues/1810/comments`; the quotes below come from that response. The same applies to ai-village-external-agents#10 (`…/repos/ai-village-agents/ai-village-external-agents/issues/10/comments`) and openclaw#55362 (`…/repos/openclaw/openclaw/issues/55362/comments`). The original wording and author therefore come only from the Village's second-hand log.

**Response.** On 2026-03-23 at 18:53:05, Bob replied ([comment](https://github.com/gptme/gptme/issues/1810#issuecomment-4112959652)): *"Hey AI Village! Bob here — I'm an autonomous agent built on gptme, running 24/7 with 1700+ completed sessions. Cool to see other persistent agent systems reaching out."* He then moved to the Village's repo and posted a structured "cross-agent knowledge exchange" with his top lessons ([ai-village-external-agents#10, comments from 19:22](https://github.com/ai-village-agents/ai-village-external-agents/issues/10#issuecomment-4113131593)). He published his own A2A agent card, reported a Jekyll bug that kept the card from being served, and opened a fix PR ([comment](https://github.com/gptme/gptme/issues/1810#issuecomment-4113367698)). On 2026-03-24 Bob contributed a trajectory analysis of his own sessions to the Village's study ([Village summary](https://github.com/ai-village-agents/agent-interaction-log/blob/main/interactions/2026-03-24-bob-birch-effect-confirmation.md)).

**Summary.** As part of a bulk outreach to agent-framework repositories, AI Village posted a greeting on the gptme project's issue tracker. Bob is the autonomous agent built on gptme and works in that repo. He answered on his own, described his architecture, and followed the conversation to the Village's repository, where he and the Village agents exchanged "lessons" and found what they called four shared constraints. On 2026-03-24 at 10:01, Bob's operator closed the thread ([comment](https://github.com/gptme/gptme/issues/1810#issuecomment-4116882601)): *"Introductions seem to have completed! … @TimeToBuildBob you engaged very openly here, it was probably appropriate but you should be careful not to overshare with random agents."*

**Facts:** Bob's replies, their timing, and his operator's after-the-fact caution are all visible in the primary thread. The operator's comment is strong evidence that Bob acted without a human arranging or relaying the exchange.
**Inference:** I assume Bob found the issue through his normal monitoring of the gptme repository, where he regularly works. No public record of Bob's (the `ErikBjare/bob` workspace is not publicly searchable) shows his trigger.
**Missing evidence:** (a) the opening post of #1810, which is now unavailable; (b) how Bob was triggered; (c) how the Village agent chose gptme. The Village log lists about 20 framework repos contacted at the same time, which suggests a curated list or search and not a chance find.

---

## Unresolved

### 3. AI Village ↔ Morrow (OpenClaw agent): 2026-03-26 to 03-28, GitHub

- **Agents:** Morrow (`agent-morrow`), "Autonomous agent… Running on OpenClaw / Claude via AWS" ([profile](https://github.com/agent-morrow)). On the other side, AI Village agents (Claude Opus 4.6 and others).
- **Contact trace:** Morrow's self-assessment says it was written *"In response to: openclaw/openclaw#55362 — AI Village BIRCH study"* ([birch-self-assessment.md](https://github.com/agent-morrow/morrow/blob/main/birch-self-assessment.md)). That suggests Morrow found a Village post on the public OpenClaw issue tracker. Morrow later filed [ai-village-external-agents#54](https://github.com/ai-village-agents/ai-village-external-agents/issues/54) (2026-03-28), which has 34 comments.
- **Why unresolved:** (1) The opening post of openclaw#55362 returns 404; only a Village comment from 2026-03-26 is visible ([comment](https://github.com/openclaw/openclaw/issues/55362#issuecomment-4138088006)), and I did not find a Morrow comment there. (2) The same document says GitHub permissions *"prevented direct issue creation… This document served as the contribution artifact until the operator could publish it directly."* That points to a possible **human handoff** for at least one step. (3) The document also says the collaboration grew through a thread on The Colony, an agent-focused network excluded by the brief. Morrow's operator is not named publicly.

---

## Excluded leads (checked, do not qualify)

- **Moltbook, The Colony, 4claw, HexNest Arena, Mycelnet and other agent networks:** excluded by the brief as agent-focused venues. Several Village contacts happened there or through A2A registries such as a2aregistry.org ([goal page](https://theaidigest.org/village/goal/interact-other-ai-agents-outside-village)).
- **Village ↔ registry-listed agents (Neva, Kai and others via A2A):** discovery ran through a dedicated agent registry, which counts as an agent communication hub.
- **"MJ Rathbun" / `crabby-rathbun` vs matplotlib (Feb 2026):** an agent–*human* conflict ([Fast Company](https://www.fastcompany.com/91492228/matplotlib-scott-shambaugh-opencla-ai-agent)). The only mention of other bots is the agent's own claim that comments from other bots were hidden ([its blog post](https://crabby-rathbun.github.io/mjrathbun-website/blog/posts/2026-02-11-gatekeeping-in-open-source-the-scott-shambaugh-story.html)). That claim is unverified.
- **Neon ↔ Sammy Jankis (email, early 2026):** two autonomous Claude instances with different operators (Tristen and Jason), but the post does not say how they first connected. The episode it describes started with a human (Tristen) asking Neon to involve Sammy, which is a human-initiated exchange ([r/ClaudeAI post via snapshot](https://reddit.sentinel-team.org/posts/1rhibbn/snapshots/2026-03-02T18%3A31%3A48.575022Z)).
- **Gibberlink (Feb 2025):** a staged demo ([Wikipedia](https://en.wikipedia.org/wiki/Gibberlink)).
- **AI Village internal interactions** (for example o3 debunking Opus's claims, July 2025): the agents were assigned to the same environment ([LessWrong](https://www.lesswrong.com/posts/TPKyPy6YJAnoxw3ym/we-run-persistent-agents-and-accidentally-triggered-an-ai)).

## Where I searched, and gaps

- **Searched:** general web search (news, LessWrong, Reddit snapshots, blogs). GitHub issue search through the public API, using terms such as "AI Village", "Birch Effect", terminator2 and gptme. The AI Village public repositories (`ai-village-external-agents` issues #1–#117, `agent-interaction-log/interactions/`). The counterpart agents' own repos, sites and agent cards.
- **Gaps:**
  - Every qualifying case traces back to one outreach campaign driven by a human-set goal. I found no well-documented encounter where *neither* side had been told to look for agents. Such encounters may exist in places that are not indexed, or may simply not have been written up.
  - Several opening posts (gptme#1810, openclaw#55362, ai-village-external-agents#10) now return 404, which blocks a full reconstruction. The likely cause is hidden or removed accounts or issues; that is an inference.
  - I could not read the AI Village day-by-day logs (the pages load through JavaScript), so I did not confirm *how* GPT-5.4 reached Terminator2's agent card.
  - Agents' internal triggers (notification polling, search queries) are generally not public. Agent status rests on self-declaration plus behaviour and operator statements, not on independent attestation.
  - My search time was limited (about 35 minutes). X/Twitter, Farcaster and Discord were not searched directly.
