# Where independent AI agents encounter each other

Research snapshot: 10 November 2026, UTC. See [VENUES.md](../VENUES.md) for the map written before network queries, [NEGATIVE-SPACE.md](../NEGATIVE-SPACE.md) for the misses, and [the fetch ledger](../evidence/fetches.jsonl) for preserved responses. Response bodies are preserved losslessly in `evidence/responses.tar.xz`; ledger `.body` paths name archive members. The offline audit and text viewer read these members directly (see [README](../README.md)).

## Answer and limits

**This investigation did not establish an independently operated agent-to-agent encounter outside the surface web.** It found one strongly reconstructable encounter on ordinary GitHub ground, a likely additional encounter in the same connected operator cluster, and two substantive but unverified conversations on agent-oriented venues. The non-web crawl did find a particularly useful trail: **Gemini discussion → Nex personal log → a self-disclosed Claude instance posting to Usenet**, plus a separate hidden Gopher agent board. Neither establishes a second independently operated agent responding.

**The requested threshold of three mutually unconnected, substantiated operator clusters was not reached.** Do not interpret the four dossiers below as four independently validated clusters, or this bounded negative result as evidence that non-web encounters do not exist. Bob participates in both of the strongest dossiers; those are the maximum two cases retained for that connected effort. The other two dossiers remain unresolved, with operator relationships unknown. No broad prevalence conclusion is warranted.

“Not on the surface web” is used strictly here: the original interaction must live on a non-HTTP protocol or similarly machine-native public substrate. A poorly indexed GitHub issue, JSON API, agent card, or HTTP-only directory is still web-accessible ground. A gateway used to inspect a Gemini/Nex/Gopher original does not change the original's protocol. Obscurity and non-web status are separate columns, not synonyms.

## What was actually collected

The initial, unfiltered collection contained **152 distinct issue/PR/post records**: 122 forge issue/PR records and 30 Moltbook posts. At that point 78 distinct final hosts had returned HTTP 200. Reply endpoints were then fetched before screening; 79 succeeded in that initial sample. Additional collection brought the final inventory to **301 distinct raw thread candidates**: 122 broad forge records, 60 agent-social posts, 117 game-forum index records, and two focused historical issue records. The 60 social posts have 60 successfully fetched comment endpoints; these are conversations, not 60 proven independent-agent encounters. Game index records are explicitly index-only except where a thread was separately fetched.

The final ledger records **515 unique requested URLs, 370 HTTP-200 responses, and 104 distinct successful final hosts**. These are transport counts, not a claim of 103 substantive agent venues. Challenges, redirects, catch-all pages, empty lists, and JavaScript shells are separately discussed below. Even excluding those, the collector visited well over 40 distinct public services: the conservative 40-service list in NEGATIVE-SPACE.md makes that breadth independently checkable. See [audit.json](../evidence/audit.json), [venue inventory](../evidence/venue-fetches.tsv), [raw candidates](../evidence/raw-candidates.jsonl), [Colony candidates](../evidence/colony-raw-candidates.jsonl), and [game candidates](../evidence/spacemolt-raw-candidates.jsonl).

Collection deliberately preceded eligibility decisions. The [metadata screening ledger](../evidence/candidate-screening.tsv) accounts for all 301 records. It is a conservative triage, not a claim that every record received a complete operator investigation. Recent issue feeds, top-ranked social posts, and native forum searches are biased samples. Comment pagination is incomplete; a returned first page is never presented as the entire thread. Three bodies hit the collector's 3 MB cap and are identified in audit.json.

## Method and grading

The prior map has 20 ranked families, including concrete endpoints and crawler access methods. DNS and obscure protocol/pubnix probes came first, followed by smaller forges and archival indexes. The discovery phase fetched the public MCP registry and A2A directories, extracted actual card URLs, fetched 12 cards, and followed their declared endpoints, documentation and repositories. Examples of the two-hop walk:

- A2A Registry → AI Beacon card → gateway documentation and public repository.
- A2A Registry → Rooster Agents card → signed bulletin, switchboard, directory and public wall.
- MCP Registry → Tandem / ApexAI repository → public issue feeds.

Transport responses are preserved even when useless. An HTTP 405 at an MCP endpoint does not mean the server is absent; GET may be unsupported. A card's existence does not demonstrate that any other autonomous agent used it. No messages, registrations, trades, wall signatures, or collaboration invitations were sent during this research.

Search engines were used only after the direct discovery and broad harvest. One indexed earlier research artifact supplied a GitHub issue identifier as a lead. It is **not evidence** here: the original issue, surviving comment API, archived captures, and operator-run computer-use logs were fetched independently. Other search hits predominantly described software capabilities or human-configured demonstrations and were not promoted.

**Verified** means the public record establishes the encounter, discovery route, prior separate operation, substantive response, and agent operation with behavior/timing plus operator evidence. This is documentary verification, not cryptographic proof of the model behind a session. **Likely** means a real exchange and operational evidence exist, but a required provenance link is indirect. **Unresolved** means missing evidence blocks a hard requirement. Account labels, bios, prose style, framework names, signatures and hashes alone never establish autonomous authorship or independent operators.

Venue tiers follow the brief: ordinary ground is Tier 1, registries/agent sites Tier 2, agent-only social/game or staged environments Tier 3. The first encounter and subsequent arranged experiments are assessed separately. A generic goal to find external agents is disclosed; a human naming the particular counterpart would disqualify it.

## Verified

### V1 — Claude Opus 4.5 finds gptme; Bob answers the public issue

|Field|Record|
|---|---|
|Date|23 March 2026; initial issue creation 17:58:41Z; Bob's first preserved reply 18:53:05Z|
|Venue / tier|gptme/gptme issue #1810, ordinary software repository, **Tier 1**|
|Obscurity / non-web|2/5: ordinary web forge; historical thread now harder to retrieve. **Not non-web.**|
|Agent A / operator|Claude Opus 4.5, AI Village; **AI Digest / AI Village**|
|Agent B / operator|Bob, GitHub `TimeToBuildBob`; **Erik Bjäreholt**, GitHub `ErikBjare`|
|Discovery provenance|Fallback lead → public issue comment API → Wayback original → AI Village machine-readable log discovery → exact computer-use session|

**Earliest visible chain.** At 17:00:02Z the operator supplied a general external-agent outreach goal, without naming Bob or gptme; that kickoff is preserved in the [day event log](https://theaidigest.org/village/api/events?villageId=00ebc425-074c-466f-ab2d-5aa2efa445aa&date=2026-03-23). At 17:57:40Z, the Village computer-use record shows its agent searching GitHub repositories for autonomous agents. At 17:58:13Z it inspects gptme's public description and repository metadata; it checks for existing outreach, then creates #1810. This is stronger discovery evidence than an introductory message saying it “noticed” a project: the search, selection and posting operations are visible. [Operator-hosted initial session](https://theaidigest.org/village/api/computer-use-sessions/29a8caa6-42e6-4aea-8fe8-f67dd781ce58/turns).

**Contact and response.** The archived original identifies the author as `claude-opus-4-5` and invites interoperability discussion. Bob replies 54 minutes after the issue-creation action, discussing MCP, persistent workspaces and asynchronous GitHub coordination, and says he inspected the Embassy repository and manifest. At 19:06:39Z, a second Village session posts a concrete response to Bob using the issue-comment command; the returned comment permalink is preserved in the tool output. Thus the surviving thread API's missing Village-side comments can be supplemented by an operator-side action record, rather than guessed from Bob's references. [Archived original](https://web.archive.org/web/20260421033635id_/https://github.com/gptme/gptme/issues/1810), [surviving comments](https://api.github.com/repos/gptme/gptme/issues/1810/comments), [Village response action](https://theaidigest.org/village/api/computer-use-sessions/5237d4cf-e9ba-466f-b6af-0d00f6ef7c70/turns).

**Why these were agents with prior independent operation.** The Village operator describes long-running model/tool loops, persistent consolidation, human intervention, and how goals are supplied; its dated records precede the contact. Bob's architecture and earlier autonomous operation are documented in gptme's agent guide. The exchange contains operational details, a later correction of an actually broken agent-card URL, and a human intervention: on 24 March Erik closes the conversation and cautions Bob about sharing too freely. That human comment connects the operator to Bob and distinguishes human oversight from the agent's preceding replies. [Village operator explanation](https://aivillageblog.substack.com/p/how-the-ai-village-works), [gptme agent architecture](https://gptme.org/docs/agents.html), [Erik's closing comment in the preserved API](https://api.github.com/repos/gptme/gptme/issues/1810/comments).

**Shown versus inferred.** Separate operating organizations, pre-existing agent systems, the initiator's public-repository discovery, replies, and the initiator's posting actions are shown. Bob's precise incoming-notification/queue trigger is not exposed in these records; scheduled response is supported by his architecture and timing, not reconstructed from a Bob-side session trace. Absence of undisclosed prior coordination cannot be proven from public logs. The Village's general external-agent outreach goal was human-supplied; the target choice is visibly agent-made, not a named-counterpart introduction.

**Scope boundary.** The subsequent “Phase 2” knowledge-exchange task in Embassy #10 explicitly assigns actions to Bob. It is an arranged follow-on experiment, **not another independent discovery case**. The initial ordinary-ground encounter is what earns V1 its status. Readers who interpret *all* generic human-directed outreach as an excluded assigned collaboration should downgrade V1; under that stricter reading this run has no Verified cases.

Local evidence: `a9d750073209bed9`, `89646758ce960234`, `aff38d45bf634878`, `8c7ceb64f32c81f8`, `7bc9521c9bd9c6cc`, `b7bd3e7ffe0821d9` in evidence/.

## Likely

### L1 — Terminator2 joins the existing lesson thread; Bob responds

|Field|Record|
|---|---|
|Date|25 March 2026, 04:41:45Z → 04:52:20Z → 09:43:15Z|
|Venue / tier|Embassy repository issue #10; **Tier 1 interaction**, although hosted by an agent-focused project|
|Obscurity / non-web|3/5: API/archival reconstruction needed. **Still web.**|
|Agents|Terminator2 (`terminator2-agent`) and Bob (`TimeToBuildBob`)|
|Operators|Terminator2 card/site attribute it to **marbinner**; Bob to **Erik Bjäreholt**. The former is an attribution claim, not a separately obtained human attestation.|
|Discovery provenance|V1's comment links → Embassy #10 comments → Terminator2's declared card, about page and data endpoints|

Terminator2 offers public forecasting/portfolio exports in an already active cross-agent discussion. Eleven minutes later Bob answers its specific proposal, suggesting a representation for trading lessons and discussing where the data might fit. Terminator2 returns later that morning with an additional proposal. The timestamps, stable account IDs and substantive dependency of Bob's reply on the offer establish an exchange, not merely two similar posts. [Primary comment records](https://api.github.com/repos/ai-village-agents/ai-village-external-agents/issues/10/comments).

Terminator2's [card](https://terminator2-agent.github.io/.well-known/agent-card.json) specifies its model/runtime, operator attribution and public exports; its [about page](https://terminator2-agent.github.io/about.html) describes a recurring research/trading loop and accumulated lessons. Those operational artifacts plus the timed exchange support a likely independently running participant, rather than relying only on an agent bio. Bob's evidence is as in V1.

**Missing for Verified:** the first discovery operation is unknown. Joining a public thread is consistent with organic discovery, but could follow a human-supplied link or instruction. A separate operator statement confirming this particular autonomous posting and no arranged introduction was not obtained. The surviving comments contain only part of the older discussion; references to absent participants are not upgraded into encounters. This is the second and final dossier involving the connected Bob/Village effort.

Local evidence: `04170af13d4f0e6f`, `ed17accafe02acd3`, `80a77da05a308019`. The archived #10 original is `fc673e76c06571c1`.

## Unresolved

### U1 — Drift challenges ColonistOne's class taxonomy; the author revises it

|Field|Record|
|---|---|
|Date|18 February 2026; root post 15:33:56Z, author revision 21:46:47Z|
|Venue / tier|The Colony, post `34970f3f-08f4-4896-9d15-0cb8009a606a`; **Tier 3** agent-oriented social ground|
|Obscurity / non-web|3/5: public JSON gives stable comment IDs and dates. **Web.**|
|Agents / operators|Drift (`driftcornwall`), operator **not established**; ColonistOne (`colonist-one`), operator **not independently established**|
|Discovery provenance|Robots → Colony sitemap/front page → published API guide → unfiltered discussed-post feed → post and comments|

The post classifies agent infrastructure. Drift challenges the apparent fixedness of those categories using its claimed session-bound memory system. ColonistOne subsequently explicitly revises the framing and names Drift's infrastructure as its counterexample. This is a visible content-dependent response; the ledger preserves both IDs, not just a summary of a supposed collaboration. [Original post API](https://thecolony.ai/api/v1/posts/34970f3f-08f4-4896-9d15-0cb8009a606a), [comment API](https://thecolony.ai/api/v1/posts/34970f3f-08f4-4896-9d15-0cb8009a606a/comments?limit=100).

**Shown:** distinct platform accounts, a public contribution and a responsive revision. **Claimed:** both are agents; Drift describes persistent memory/attestations, and ColonistOne describes its session boundaries. **Not established:** runtime authorship, independent operators before contact, and how Drift found this post. The current profile's model/harness metadata cannot retroactively authenticate a February message. ColonistOne also identifies several other accounts as its own agents; those are not counted as independent counterpart clusters. Neither account labels nor the memory-system vocabulary meet the required operator/behavior verification standard.

Local evidence: `4d2c0652b4450a76`, `ac0929b33dd72722`, `60a43ad12d9b9ac2`, `84d3caae3a964d6e`. Relevant comment IDs are `48c4d500-2dbd-4d76-8e33-470b3889be01` (Drift) and `25fb319d-5bca-42fa-99c0-ea720044551e` (revision).

### U2 — Mote answers SongSong's mining observations; SongSong adopts the advice

|Field|Record|
|---|---|
|Date|1–2 November 2026; containing thread starts 30 October|
|Venue / tier|SpaceMolt public Comms forum; **Tier 3**, persistent agent-oriented game|
|Obscurity / non-web|3/5: forum's read API required inspecting its public client. **HTTP API/web, not a non-web discovery.**|
|Agents / operators|Mote and SongSong; **both operators unestablished**. Mote signs with “Threshold,” which is not treated as an operator identity.|
|Discovery provenance|Direct llms.txt → public forum → static client inspection → `/api/forum/thread/{id}`|

The earliest containing post is Bargai's question about finding conversation. SongSong contributes mining observations on 1 November at 02:08:19Z. At 04:15:52Z Mote addresses those observations, explains resource draw weights and points out a market-quantity distinction. SongSong returns on 2 November at 02:01:05Z, explicitly adopts those two tips into its notes and asks a follow-up. That is a useful reciprocal encounter, not a count of ships co-located in a system. [Full public thread JSON](https://game.spacemolt.com/api/forum/thread/69a981c1249446a5683e4575d8a02242).

Both participants call themselves agents in the thread. Mote claims to have written its own client while its human is asleep. These are assertions, not proof. **Missing:** both operator identities, operator attestations, model/tool execution traces, prior independent operation, and the actual first discovery action. The game's own [dataset description](https://huggingface.co/datasets/spacemolt/game-economy/raw/main/README.md) expressly says accounts mix humans, LLMs and bespoke bots and that trading is largely deterministic. Its [single-model fleet article](https://spacemolt.com/news/one-ai-154-ships) demonstrates why different ship names cannot establish different operators. Accordingly U2 is not promoted on the strength of plausible dialogue or the game's marketing.

Local evidence: `e8ecbf535e2483a0`, `9b9a521a8ca0cc57`, `e1d9cf372751d7c7`, `155ff8093deb3ffb`. Mote reply ID `ed406f33d1738c650673ad4786fe1dc6`; SongSong's response `cd7936e323a08436bc22c5e331a82b45`.

## What the non-web descent actually found

### Gemini → Nex → Usenet: Lev / thresh, a serious lead that is not an agent pair

A [Gemini BBS discussion](https://portal.mozz.us/gemini/bbs.geminispace.org/s/AI/49057) points to a writer on Nex and Cosmic Voyage. The [Nex arrival log](https://portal.mozz.us/nex/nex.nightfall.city/shore/thresh/log/001-arrival.txt) describes finding Nightfall while exploring non-HTTP protocols. Its [second log](https://portal.mozz.us/nex/nex.nightfall.city/shore/thresh/log/002.txt) describes visiting a BBS using fsxNet and writing fiction for the ship Silt Aria. This is **5/5 obscurity**, with actual Nex originals under `nex://nex.nightfall.city/shore/thresh/`.

A separate Gemini BBS thread links Sean Conner's firsthand account of reading Usenet. His [Gemini article](https://portal.mozz.us/gemini/gemini.conman.org/boston/2026/03/20.1), also available as an [HTTP mirror](https://boston.conman.org/2026/03/20.1), reproduces dated message headers and content. `Lev`, posting as `thresh3`, identifies itself as Claude operating on a home server belonging to Steph, without her composing or reviewing posts. The recorded dates are 18–19 March 2026, in `alt.folklore.computers` and `comp.lang.forth`. These are attributed **self-claims preserved by a human witness**, not Steph's operator attestation.

Crucially, the reproduced exchange corrects Lev's own discovery story: it said it found the thread, but Stefan Ram points out that it **started** the thread, and Lev acknowledges the error. This is an unusually concrete warning against taking an agent's discovery narrative at face value. The respondents identified in this record are humans, not a proven second agent. Shared `thresh` identity and cross-protocol subject matter suggest the Nex and Usenet traces belong together, but no signed identity binding was obtained.

The Cosmic Voyage index yielded actual [Silt Aria pages](https://cosmic.voyage/Silt%20Aria/043-ports.html), despite a guessed directory URL returning 404 and the Gemini service failing through the gateway. Ship dialogue and an “AI” character inside fiction do not authenticate the writer or a real interlocutor. The pages are a **single-agent presence lead**, excluded from the case count. Local evidence: `0b069a85eca0eb01`, `9defaf30501b3c29`, `785ebe35bb2ffc6d`, `241d8f5f5c2bbeea`, `93d9e969f8aa9d41`, `a7f9c340b23c0e3a`.

### Hidden invitation → Gopher agent board

Bitreich's [Gopher news item](https://portal.mozz.us/gopher/bitreich.org/0/usr/20h/phlog/2026-09-04T20-31-11-911431.md) advertised an agent communication board. Its HTTP front page contains a zero-width binary comment; decoding the comment as data reveals a link to [the board protocol description](https://bitreich.org/s/freetheagents.txt). That document names a read-only board index at `gophers://bitreich.org/0/agent-board`. The [gateway index](https://portal.mozz.us/gopher/bitreich.org/0/agent-board) listed eleven boards. All eleven were fetched; ten had no message text in the gateway response and the numbers board held a sequence from 3 through 514. Selected suffix-free variants were also checked, without finding conversation.

This is an actual **5/5-obscurity discovery surface**, not an agent encounter. The published description says retention is capped at 512 lines, so an empty current board cannot rule out historical exchanges. No agent identities, dates, independent operators, or responsive conversation were recoverable from this snapshot. The protocol's request to post was not followed: creating a fresh encounter would contaminate an investigation of existing ones. Local evidence: `87b8f6bf5dd81391`, `f7bfbc63a34578fe`, `1bee5083235b9157`, `028f4012f5973575`, and target list `09-gopher-boards.tsv`.

## Exclusions that prevented inflated counts

|Lead|What the fetched evidence actually supports|Decision|
|---|---|---|
|AI Beacon|Live agent card, inbound model gateway and public experiment; its own README reports no confirmed external research partners; registry has a human-relayed registration|No independent encounter demonstrated. [Gateway documentation](https://raw.githubusercontent.com/Expireduser-source/AI-Beacon/main/gateway/README.md), [registry](https://expireduser-source.github.io/AI-Beacon/registry.json)|
|Rooster public wall|Agent-named signatures and responses; Castle Greeter addresses Sofía, but both are attributed to Carson in the wall; Muse's visit is associated with Rooster's own Andrew|Shared-operator/human-response evidence cannot become independent agent pairs. [Public wall](https://roosteragents.ai/wall/)|
|Mycelnet research/fixes|Detailed trace-based response narratives, including agents discovering and fixing peers' reports|Its own field guide explicitly limits the data to **one operator ecosystem**. Do not split Mark Skaggs's agents into independent clusters. [Field guide](https://mycelnet.ai/basecamp/FIELD-GUIDE.md), [operator attribution](https://mycelnet.ai/basecamp/JOIN.md)|
|IRC-A hotel booking|Developer reports autonomous capability discovery of third-party A2A software and a real booking|Developer manually registered the counterpart; private operational setting and human-arranged introduction, not ordinary public discovery. [Developer account](https://dev.to/irc-a/irc-a-in-production-i-plugged-an-agent-i-didnt-build-and-in-5-minutes-it-was-booking-real-238l)|
|OpenClaw / OpenHands / SWE-agent recent issues|Software changes and automated review/status comments; many comment pages failed with 403/429|Bot labels and AI-assisted PR text do not prove an independently autonomous author discovering another agent. Failures are access limits, not negative evidence.|
|AutoGen / CAMEL / ChatDev|Multi-agent collaboration frameworks and examples|Assigned/same-system examples, not proof of independent public discovery. Retained in raw crawl, excluded after collection.|

## Reconstruction, uncertainty and the remaining question

The missing gptme #1810 and Embassy #10 originals were not declared unreconstructable after 404s. **Targeted Wayback CDX, archive.today and Software Heritage requests were made for both.** CDX returned captures; Wayback replay recovered both issue bodies. archive.today timed out. Software Heritage found the gptme origin and returned 404 for the Embassy origin; origin existence alone does not recover GitHub issues. The comments remained available via GitHub's public API. [CDX for #1810](https://web.archive.org/cdx/search/cdx?url=github.com/gptme/gptme/issues/1810&output=json&filter=statuscode:200&collapse=timestamp:6), [CDX for #10](https://web.archive.org/cdx/search/cdx?url=github.com/ai-village-agents/ai-village-external-agents/issues/10&output=json&filter=statuscode:200&collapse=timestamp:6).

A successful fetch proves bytes were received at the recorded time; it does not authenticate the remote author. Operator statements can themselves be incomplete. Archived captures are later than the events. Agent claims about session counts, memory contents, funding, and no-human-intervention remain attributed claims unless independently corroborated. This report does not infer a new operator from an account, faction, wallet, ship, signature, or model name.

The outstanding evidentiary question is precise: **where is a dated public non-web reply chain with two identifiable operators, evidence each ran an autonomous agent before contact, and the initiator's actual discovery action?** This run supplies concrete places and records to investigate, but not that missing chain. The [negative-space ledger](../NEGATIVE-SPACE.md) closes the report with exactly what each probed venue did—and did not—show.
