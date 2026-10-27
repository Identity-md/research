**Unattended open-source coding CLIs — 2026-10-27**

**Ranking: Vibe, Gemini CLI, Qwen Code, Kilo CLI, Pi.** Judgment for externally isolated workers, prioritizing completion, confinement, accounting and tool controls over provider/login breadth and delegation; not a coding benchmark. Gemini leads if Google-only access and bundled isolation dominate.

The 28 supplied results cover 18 families. No agent/model/login/sandbox was execution-tested. “Not found” is bounded by linked sources. Provider lists are representative; login assumes prior authorization, not proven entitlement/renewal. Native subscription adapters qualify; Claude Code/Codex wrappers do not. UTC dates identify stable CLI/package publications; newer channels are separate. Moving-source features are not guaranteed in the adjacent stable release.

**Ranked comparison.** Permissions/worktrees are not OS isolation; tool restrictions do not cover every process effect.

| Candidate | 1. Headless | 2. Shell / writes / network | 3. Tokens per run | 4. Parallel agents | 5. Providers / subscription login | 6. License; stable release/date |
|---|---|---|---|---|---|---|
| **1 Vibe** | `--prompt-file TASK --workdir DIR`; structured exits. [CLI][174] | Tool/command/path rules; external sandbox required; experimental socket. [policy][186], [socket][188] | `export.json`: root tokens/cost plus separate children. [schema][177] | Native children; live/concurrent caps. [settings][190] | Mistral/local + OpenAI/Responses/Anthropic/Vertex-Anthropic protocols; Mistral plan browser setup provisions a key. [adapters][178], [login][183] | [Apache-2.0][184]; **3.0.3, 2026-10-26**. [release][180] |
| **2 Gemini CLI** | `-p PROMPT --output-format json`, launcher cwd; headless asks denied. [guide][58], [policy][63] | Shell/tool policy; Seatbelt/container sandboxes. Network defaults conflict; explicit enforcement needed. [sandbox][65], [loader][66] | JSON model tokens / final JSONL totals, no money field. [schema][62] | Local agents; eligible calls concurrent; no nested local agents. [agents][68], [scheduler][67] | Google Gemini: Google login including AI Pro/Ultra, API key or Vertex credentials. [auth][56] | [Apache-2.0][59]; **0.65.0, 2026-10-20**. [release][64] |
| **3 Qwen Code** | `-p PROMPT --output-format json`, launcher cwd; stdin accepted. [guide][162] | Bash/Read/Edit/WebFetch rules; bwrap write/closed-network sandbox, broad reads. [rules][169], [sandbox][168] | JSON message usage plus per-call token JSONL; cost/inclusive child total unproven. [types][170], [journal][163] | Concurrent/background Agent calls; shared-directory write conflicts possible. [Agent][160] | OpenAI-compatible/Responses, Anthropic, Gemini, Vertex/local; paid Qwen plans require keys, former free OAuth ended. [providers][166], [auth][161] | [Apache-2.0][164]; **0.26.1, 2026-10-24**. [releases][167] |
| **4 Kilo CLI** | `run --dir DIR --format json -- PROMPT`; omit `--auto` for selective allows. [runner][101] | Ordered permissions; opt-in bwrap/Seatbelt tool writes/egress. Broad reads/host integrations remain; no Windows backend. [rules][99], [sandbox][102] | Root `step_finish` tokens/cost; child steps separate, costs can propagate. [runner][101], [rollup][97] | Foreground/background task children. [task][103] | Kilo/OpenRouter, OpenAI/Anthropic/Google, Azure/Bedrock, compatible; ChatGPT/Copilot OAuth. [catalog][100], [ChatGPT][95], [Copilot][96] | **MIT; 7.8.18, 2026-10-26**, CLI npm. [metadata][98] |
| **5 Pi** | `-p PROMPT` / `--mode json`, cwd; JSON exit 0 can mask model error. [CLI][151], [source][154] | Tool filters; no core permission jail. Example Bash sandbox fails open/excludes file tools. [security][159], [example][158] | Final message usage/cost; RPC/session totals also available. [fields][152], [RPC][157] | Optional official extension: 8 tasks, 4 concurrent processes. [extension][150] | OpenAI/Anthropic/Google, Bedrock/Azure, gateways/local; Claude Pro/Max, ChatGPT/Copilot logins. [providers][155] | [MIT][153]; **1.4.0, 2026-10-21**. [releases][156] |

**Other profiles, alphabetically.** Moving-source findings may postdate the listed stable package.

| Candidate | 1. Headless | 2. Shell / writes / network | 3. Tokens | 4. Parallel agents | 5. Providers / login | 6. License; stable release/date |
|---|---|---|---|---|---|---|
| Aider | `--message-file --yes-always`, cwd; suggested shell still needs explicit yes. [scripting][3], [source][4] | File/read-only/ignore controls; no command ACL/OS/egress jail established. [options][6] | Reply text; analytics JSONL prompt/completion/total/cost. [source][9] | No children found; architect/editor sequential. [modes][1] | LiteLLM/cloud/local; Copilot supplied token, no built-in login. [catalog][7], [auth][5] | **Apache-2.0; PyPI 0.86.2, 2026-02-12**; GitHub **0.86.0, 2025-08-09**. [PyPI][8], [GitHub][2] |
| Cline | `--json --cwd DIR PROMPT`; auto-approve default; timeout. [CLI][13] | Hooks cancel commands; no CLI OS/egress jail established; “sandbox” separates state. [CLI][13] | `run_result.usage`, optional aggregate; token/cache/cost fields. [runner][17] | Nested children/teams; yolo disables both. [agents][10], [source][14] | OpenAI/Anthropic/Google, Bedrock/Azure, gateways/local; ChatGPT OAuth; Claude wrapper excluded. [catalog][16], [auth][11], [Claude][12] | **Apache-2.0; CLI 3.0.74, 2026-10-26**. [npm][15] |
| Continue | `cn -p PROMPT`, cwd; unmaintained. [guide][20], [status][22] | Bash/tool rules; Write globs not enforced by inspected matcher; no OS/egress jail established. [matcher][24] | Session JSON prompt/completion/cache/estimated cost. [session][25] | Beta children replace parent policy with wildcard allow. [executor][19] | Broad API/local adapters; Hub auth removed, consumer login not found. [catalog][21], [auth][18] | **Apache-2.0; npm CLI 1.5.47, 2026-06-18**. [npm][23] |
| ForgeCode | `forge -C DIR -p PROMPT`; failed agent may exit 0. [CLI][47], [UI][54] | Optional shell/file/URL rules; “sandbox” is worktree; OS/egress jail not established. [rules][52], [README][50] | Conversation dumps; stats tokens may be last reply, cost accumulated. [conversation][55], [UI][54] | Concurrent task children. [dispatch][53] | OpenAI/Anthropic/Gemini, Bedrock/gateways/local; ChatGPT/Anthropic/Copilot OAuth. [catalog][49] | [Apache-2.0][48]; **2.14.0, 2026-10-01**. [releases][51] |
| Goose | `run -t TEXT` / `-i FILE`, cwd; auto mode/turn cap. [tasks][71] | Tool permissions; complete shell/path/egress boundary not established. [permissions][73] | JSON metadata/final stream tokens/cache/optional USD. [source][76] | Native parallel children, configurable cap. [agents][70] | OpenAI/Anthropic/Google, Azure/Bedrock, gateways/local; ChatGPT/Copilot login; ACP separate. [catalog][74] | [Apache-2.0][72]; **1.56.0, 2026-10-23**. [releases][75] |
| gptme | `-n -w DIR --output-format json PROMPT`. [CLI][79] | Tool filters; optional shell OR Python sandbox, not all file tools. [CLI][79], [sandbox][83] | `GPTME_EXIT_STATS=1`: JSON stderr tokens/cache/cost (master). [source][84] | Parallel/batch subprocess or thread agents. [guide][77] | OpenAI/Anthropic/Gemini/gateways/local; ChatGPT/SuperGrok login. [catalog][81], [auth][78] | [MIT][80]; **0.35.1, 2026-10-15**. [releases][82] |
| Hermes | `chat --oneshot --in DIR -q TEXT`; gateway may continue after client detach/interrupt. [transport][91], [view][94] | Docker terminal/files can deny network; browser/MCP/plugins outside. [Docker][86], [security][92] | Usage JSON ledger; root tokens exclude children, cost includes them; auxiliary total omits cache. [ledger][93], [finalizer][87] | Concurrent delegates. [dispatch][85] | Nous/OpenAI/Anthropic/Google, Bedrock/Azure/gateways/local; Nous/ChatGPT/Copilot OAuth; Max needs extra usage. [providers][89] | [MIT][88]; **0.22.5, 2026-10-23**. [release][90] |
| Kimi Code | `-p TEXT --output-format stream-json`, cwd; forces auto, conflicts with yolo/plan. [CLI][105] | Static tool/Bash/path denies; no OS/egress jail established. [config][106], [host backend][111] | Per-agent `usage.record`; `/goal` token summary; ordinary print totals absent. [usage][113], [goal][107] | Agent children/background; AgentSwarm unavailable headlessly. [tools][112], [changes][104] | Kimi/Anthropic/OpenAI/Responses/Gemini/Vertex; Kimi device login. [providers][109], [CLI][105] | [MIT][108]; **2.3.3, 2026-10-26**. [releases][110] |
| Letta | `--backend local --ephemeral -p TEXT`, cwd; no required Letta server. [README][124] | Tool/path/Bash rules; optional shell FS sandbox fails open; no default workspace/egress jail. [policy][120], [sandbox][116], [network][122] | Final JSON token/cache/reasoning usage; child total separate. [headless][115], [child][121] | Concurrent Task subprocesses. [execution][117] | Local Pi catalog/compatible/local; ChatGPT/Copilot documented; Claude/xAI source/docs differ. [catalog][119], [models][118] | **Apache-2.0; npm 0.34.25, 2026-10-26**; GitHub **0.34.24, 2026-10-25**. [npm][123], [GitHub][114] |
| mini-SWE-agent | `-t TASK -y --exit-immediately`, cwd. [CLI][127] | Bash-only; local unsandboxed, optional Docker/bwrap; network on by default. [environments][128] | Trajectory cost/calls; tokens only in raw responses, no normalized total. [output][131] | Independent batch workers; no native children found. [runner][125] | LiteLLM/gateways/local; subscription login not found. [repo][130], [auth][126] | [MIT][130]; **2.4.6, 2026-07-23**. [releases][129] |
| OpenCode 2 | `run --standalone --format json TEXT`, cwd; no V1 `--dir`. [CLI][132] | Ordered permissions/hard policies; shell host authority, no OS/egress jail established. [permissions][136], [policies][134] | `step_finish` JSON tokens/cache/reasoning/cost; session export. [source][135] | Foreground/background subagents. [tools][139] | OpenAI/Anthropic/Google, Azure/Bedrock/OpenRouter, compatible/local; ChatGPT/Copilot login. [providers][137] | **MIT; npm @opencode/cli 2.1.4, 2026-10-23**; V2 lacks GitHub Release object. [npm][138], [releases API][133] |
| OpenHands | Old `--headless -t TASK --json`; current Canvas finite CLI not found. [old][142], [launcher][144] | Old CLI shell/write/egress boundary not established; Canvas Docker is separate. [old][142], [Docker][143] | Old CLI usage schema not found; SDK metrics separate. [old][142], [SDK][149] | Old delegate tool; current SDK parallelism separate. [old releases][147], [SDK][140] | Old key/base-URL config; current LiteLLM and ChatGPT SDK login separate. [old][146], [models][148], [SDK auth][141] | **MIT; Canvas 1.33.0, 2026-10-23**. Old CLI **1.16.0, May 8, year not captured**, unmaintained. [Canvas][145], [old][147], [status][146] |
| ZCode | `-p TEXT --cwd DIR`; yolo default; background settlement conditional. [CLI][193], [workflow][202] | Remove tools via CLI; yolo bypasses ordinary rules; no OS/egress jail established. [rules][197], [notice][195] | Optional per-turn tokens/cache/reasoning; no cost/inclusive child ledger established. [usage][201] | Background Agent children. [type][192] | Z.ai, Kimi/DeepSeek, OpenAI/Anthropic/xAI, gateways/compatible; GLM plan login. [catalog][199], [login][194] | [Apache-2.0][195]; GitHub **3.14.3, 2026-09-24**; product **3.16.3, 2026-10-23**; CLI package private. [API][200], [product][198], [package][196] |

Newer development channels: Gemini **0.67.0-nightly.20261027.g363a13119 (2026-10-27)**; Qwen **0.26.2-preview.0 (2026-10-26)**; gptme **0.35.2.dev20261022 (2026-10-22)**. OpenCode npm **0.0.0-dev-65 (2026-10-27)** has unestablished V2 lineage.  [Gemini][61], [Qwen][167], [gptme][82], [OpenCode][138]

**1. Mistral Vibe: best integration contract when isolation is supplied externally.** The 3.0.3 CLI accepts prompt files/workdir and exports completion/failure outcomes. JSON stdout is messages; `export.json` is accounting/status. Partial edits need not imply success. Headless approval-required calls are denied. [CLI][174], [export][177], [permissions][186]

Tool-name/glob/regex filters, per-tool permissions, shell prefixes and outside-workdir checks provide useful application controls. They cannot confine every effect of approved scripts. The experimental socket interface requires a caller-supplied sandbox; model calls, MCP, hooks and storage remain host-side. This is why the recommendation assumes whole-process containment. [schema][190], [shell][172], [scope][188]

Usage needs careful treatment: root totals exclude children; child exports are lifetime totals on resume. Token/price limits react after observed usage, not before spend, and do not cap combined child usage. Initially disabling children makes accounting and termination easier to validate; parallel delegation remains an option after that work. [export][177], [child calculation][173], [limits][182]

Mistral plus compatible protocol adapters give provider flexibility, including local inference. Mistral plan browser setup avoids manual key entry but returns a stored API key; unattended renewal and third-party consumer-subscription login were not established. Vibe wins on its run/export interface, not on having the strongest built-in sandbox or the widest subscription catalog. [adapters][178], [setup][179], [persistence][187], [credentials][175]

**2. Gemini CLI: stronger built-in isolation choices, narrower provider scope.** Tagged 0.65.0 provides JSON/JSONL completion/errors. Admin TOML can deny all tools and allow selected file tools at higher priority; headless asks become denials. Check process outcome, terminal result and files; kills may lose final metrics. [headless][58], [policy][63], [schema][62]

Seatbelt and container backends are meaningful boundaries, with different read/write/network scopes. The default permissive Seatbelt profile allows broad reads/network. Tagged settings list network access as false, while the legacy loader initializes it true. Therefore choose a backend, enforce egress explicitly and test it; no universal default-network claim is justified. Whole-process isolation also covers integrations outside a particular tool boundary. [sandbox][65], [settings][57], [loader][66]

JSON includes per-model prompt/output/cache/thought/tool metrics; stream JSON has a smaller final aggregate. Source inspection indicates local child/utility calls feed shared telemetry. Failed/aborted calls or missing provider metadata can undercount, and remote A2A usage is not guaranteed included. Resume hydration can include history: fresh sessions simplify per-job accounting. No money/spend-cap interface was established. [aggregation][69], [logging][60], [schema][62]

Google login supports eligible AI Pro/Ultra accounts after browser authorization; API key/Vertex routes are alternatives. General third-party/local model support was not established. Local agents and concurrent calls are available, but separate context does not isolate writes. Gemini ranks above Qwen because its version-pinned policy/accounting audit is stronger; it moves first when Google-only access is acceptable and bundled isolation dominates. [auth][56], [agents][68], [scheduler][67]

**3. Qwen Code: flexible providers with useful sandbox mechanisms, requiring a stable-version audit.** Launch `qwen -p PROMPT --output-format json` in the job directory; stdin works. Approval modes include prompts, automatic edits/classification and yolo. Choose unattended rules/mode and impose a deadline. Complete exit semantics and a Vibe/Gemini-depth tagged audit remain missing. [headless][162], [modes][165]

Permission patterns cover Bash, Read, Edit and WebFetch. The documented bwrap `workspace-write`/`closed` configuration restricts writes and command networking but leaves broad reads. It is not secret isolation. Model traffic still needs an approved route. Backend selection and effective network behavior must be tested rather than inferred from the word “sandbox.” [settings][169], [sandbox][168]

JSON message usage exposes input/output/cache/total counts; token journals add session/model/auth/source and thoughts. Recursive child completeness and per-run money totals were not established. Concurrent/background Agent calls can share a workdir, so the worker must coordinate writers or isolate jobs. Keep both raw event and journal evidence, using one ledger to avoid double-counting. [types][170], [journal][163], [Agent][160]

OpenAI-compatible/Responses, Anthropic, Gemini and Vertex protocols support a broad deployment range, with documented Ollama/vLLM/LM Studio endpoints. Current Qwen subscriptions require plan API keys; free OAuth ended **2026-04-15**. No current ChatGPT/Claude/Gemini/Copilot subscription login was established. Qwen can outrank Gemini where multi-provider access is required, after version-pinned confinement/accounting validation. [providers][166], [authentication][161]

**Why Kilo/Pi, and the near misses.** Kilo's tagged tool sandbox and inspectable permissions justify fourth, despite root-only JSON and lack of a job deadline. `--auto` approves queued asks; explicit denies survive. Pi's scripting/tools/subscriptions justify fifth, but its example Bash sandbox fails open and JSON errors require inspection. [Kilo][101], [sandbox][102], [Pi][151], [sandbox][158], [errors][154]

**Proposed worker adapter for Vibe 3.0.3; untested.** Pin package/dependencies and GIL-enabled Python ≥3.12. Preconfigure model/auth: interactive `vibe --setup` or `MISTRAL_API_KEY`. Parameters below are deployment inputs. [package][184], [setup][179]

**Invoke.** Use an argv API, closed stdin, separate stdout/stderr and fresh absolute task/output paths. Relative prompt/output paths resolve before changing workdir. Omit resume initially. [CLI][174]

```text
vibe --prompt-file <absolute-task-file> --workdir <absolute-checkout>
     --agent accept-edits
     --enabled-tools read_file --enabled-tools edit --enabled-tools write_file
     --output json --output-dir <fresh-absolute-output>
     --max-turns <N> --max-tokens <T> --max-price <USD> --time-limit <seconds>
```

Normal exits: **0 finished; 1 usage/config; 2 infrastructure; 3 unfinished limit/deadline/termination/length/refusal; 4 socket abort**. Require fresh export plus OS outcome and artifact validation. Parser errors/kill/OOM/storage failures may prevent export; export-write errors need not alter exit status. Supervise the whole process tree with a deadline, graceful stop then forced cleanup. The stop path gives 10 seconds' grace, reserving 3 for reporting. [outcomes][176], [export][177], [lifecycle][182]

**Confine.** Proposed boundary: unprivileged disposable container/VM; read-only runtime/config; assigned checkout and private state/temp/export storage writable; CPU/memory/PID/disk/time limits. Exclude host home/control sockets/unrelated secrets. Enforce deny-default egress externally with one reviewed inference/auth route, or provide local inference. Path/tool rules cannot substitute for this boundary. [scope motivating proposal][188], [path checks][185]

Experimental Unix `--agent-socket` rejects `--workdir` and requires a caller-implemented sandbox. Host integrations remain; server tools bypass CLI filters. [protocol][191], [scope][188]

**Meter.** Capture `export.json`, schema 1: outcome, session, usage, cost, steps, limits/timestamps and children. Root input/output/cache/cost are run deltas; root steps exclude children/utilities. Total=input+output; cache is a subset of input. Cost is a configured-rate estimate; missing prices can yield zero. [schema][177], [calculation][189], [baseline][171]

Fresh run: sum root plus unique child sessions once. Resume: children expose lifetime usage/cost, so add only increases from saved baselines; child steps are per-run. Do not add journal duplicates/cache breakdowns again. Missing readings remain unknown; label fallback prices. Token/price stops act after spend and omit combined child budgets. Enforce allocation at provider/gateway and reconcile auxiliary/retry usage before settlement; invoice completeness remains unproven. [children][173], [export][177], [stops][182]

**Limit tools.** Proposed worker-owned `VIBE_HOME/config.toml`, outside the checkout; initially run tests through a separately controlled stage. Fields come from tagged schema/permission code; validate the effective policy before use. [schema][190], [permissions][186]

```toml
default_agent = "accept-edits"
outside_workdir = "deny"
enabled_tools = ["read_file", "edit", "write_file"]
disabled_tools = ["bash*", "git_bash*", "powershell*", "task", "web_*", "mcp_*", "connector_*"]
enable_auto_approve = false
enable_subagents = false
enable_background_processes = false
enable_mcp = false
enable_connectors = false
enable_telemetry = false
enable_update_checks = false
[session_logging]
enabled = true
generate_titles = false
[tools.read_file]
permission = "always"
[tools.edit]
permission = "always"
[tools.write_file]
permission = "always"
```

Precedence is admin → agent → runtime/CLI → environment → trusted project → user/defaults; user config alone is not immutable policy. Avoid unreviewed trust/hooks/plugins and auto-approve. If shell is enabled later inside isolation, prefixes such as `git status` are literal token-boundary matches, not `git *` globs. If children are enabled, cap live/concurrent counts and meter separately. [layers][181], [CLI][174], [Bash][172], [settings][190]

Unexecuted acceptance checks: edits; tool/path/egress denials; failure/termination cleanup; cache/resumed-child accounting.

**Screened, not fully profiled.** Remaining criteria are **not assessed**: [Nanocoder][40] `run`, [Kode][39] `-p`, [Open Interpreter][37] `exec`, [community Grok CLI][34] `-p`, separate official [Grok Build][35] `--single`, and [SWE-agent][45] run/batch. [Plandex][42] automation and [Trae][46] `run` need finite-run assessment; discovery disagreed on Trae's headless certainty. Absent releases alone do not disqualify.

Headless completion not established: [Octofriend][41], [Freebuff][33], [DeepSeek Harness][31]. [Legacy Kimi][38] is superseded. Roo had [CLI evidence][43] despite one discovery error; it was not advanced after its [sunset][44]. [Crush FSL-1.1-MIT][29] fails the current-code open-source requirement. [Copilot CLI][28]/[Auggie][27] have restrictive licenses; open implementation/license was not established in checked [Amp][26], [Cursor][30], [Factory][32] or [iFlow][36] materials.

**Provenance:** `profile-pilot/*`, `profiles-round2/*`, `discover/*`, corrected by `recipe-vibe/vibe`, `integration-finalists/{gemini,kilo}`, `evidence-repair/{hermes,letta}`; `rank-finalists/compare` was provisional. Goal state: 28 accepted items; `trunk:null`, no code repository/commit. Sole-output closure:

```json
{"notes":"Report complete from 28 results. No new batches or code trunk. Runtime/billing unverified.","finish":true}
```

[1]: https://aider.chat/docs/usage/modes.html
[2]: https://github.com/Aider-AI/aider/releases/tag/v0.86.0
[3]: https://aider.chat/docs/scripting.html
[4]: https://github.com/Aider-AI/aider/blob/main/aider/io.py
[5]: https://aider.chat/docs/llms/github.html
[6]: https://aider.chat/docs/config/options.html
[7]: https://aider.chat/docs/llms.html
[8]: https://pypi.org/project/aider-chat/0.86.2/
[9]: https://github.com/Aider-AI/aider/blob/main/aider/coders/base_coder.py
[10]: https://docs.cline.bot/features/subagents
[11]: https://github.com/cline/cline/blob/c35b729049c7bb26c340df63ea9235c40b32dd29/apps/cli/src/commands/auth.ts
[12]: https://docs.cline.bot/provider-config/anthropic
[13]: https://docs.cline.bot/cli/cli-reference
[14]: https://github.com/cline/cline/blob/c35b729049c7bb26c340df63ea9235c40b32dd29/apps/cli/src/main.ts
[15]: https://registry.npmjs.org/cline
[16]: https://docs.cline.bot/provider-config/other-30-plus-providers
[17]: https://github.com/cline/cline/blob/c35b729049c7bb26c340df63ea9235c40b32dd29/apps/cli/src/runtime/run-agent.ts
[18]: https://raw.githubusercontent.com/continuedev/continue/main/extensions/cli/src/services/AuthService.ts
[19]: https://raw.githubusercontent.com/continuedev/continue/main/extensions/cli/src/subagent/executor.ts
[20]: https://raw.githubusercontent.com/continuedev/continue/main/docs/cli/headless-mode.mdx
[21]: https://raw.githubusercontent.com/continuedev/continue/main/packages/openai-adapters/src/index.ts
[22]: https://raw.githubusercontent.com/continuedev/continue/main/README.md
[23]: https://registry.npmjs.org/@continuedev%2fcli
[24]: https://raw.githubusercontent.com/continuedev/continue/main/extensions/cli/src/permissions/permissionChecker.ts
[25]: https://raw.githubusercontent.com/continuedev/continue/main/extensions/cli/src/session.ts
[26]: https://ampcode.com/manual
[27]: https://github.com/augmentcode/auggie/blob/main/LICENSE.md
[28]: https://github.com/github/copilot-cli/blob/main/LICENSE.md
[29]: https://github.com/charmbracelet/crush/blob/main/LICENSE.md
[30]: https://cursor.com/docs/cli/headless
[31]: https://github.com/deepseek-ai/deepseek-harness/blob/HEAD/README.md
[32]: https://github.com/factory-ai/factory
[33]: https://github.com/CodebuffAI/freebuff/blob/HEAD/README.md
[34]: https://github.com/superagent-ai/grok-cli/blob/HEAD/README.md
[35]: https://docs.x.ai/build/cli/headless-scripting
[36]: https://github.com/iflow-ai/iflow-cli
[37]: https://github.com/openinterpreter/openinterpreter/blob/HEAD/README.md
[38]: https://github.com/MoonshotAI/kimi-cli
[39]: https://github.com/shareAI-lab/Kode-CLI/blob/HEAD/README.md
[40]: https://github.com/Nano-Collective/nanocoder/blob/HEAD/README.md
[41]: https://github.com/synthetic-lab/octofriend
[42]: https://github.com/plandex-ai/plandex/blob/main/docs/docs/cli-reference.md
[43]: https://github.com/RooCodeInc/Roo-Code/blob/main/apps/cli/README.md
[44]: https://github.com/RooCodeInc/Roo-Code-Docs/blob/main/docs/sunset.md
[45]: https://swe-agent.com/latest/usage/cl_tutorial/
[46]: https://github.com/bytedance/trae-agent/blob/HEAD/README.md
[47]: https://github.com/tailcallhq/forgecode/blob/1df4bbd19fa28c1236f3253d0f659041757c029d/crates/forge_main/src/cli.rs
[48]: https://github.com/tailcallhq/forgecode/blob/1df4bbd19fa28c1236f3253d0f659041757c029d/LICENSE
[49]: https://github.com/tailcallhq/forgecode/blob/1df4bbd19fa28c1236f3253d0f659041757c029d/crates/forge_repo/src/provider/provider.json
[50]: https://github.com/tailcallhq/forgecode/blob/1df4bbd19fa28c1236f3253d0f659041757c029d/README.md
[51]: https://api.github.com/repos/tailcallhq/forgecode/releases?per_page=100&page=1
[52]: https://github.com/tailcallhq/forgecode/blob/1df4bbd19fa28c1236f3253d0f659041757c029d/crates/forge_domain/src/policies/rule.rs
[53]: https://github.com/tailcallhq/forgecode/blob/1df4bbd19fa28c1236f3253d0f659041757c029d/crates/forge_app/src/tool_registry.rs
[54]: https://github.com/tailcallhq/forgecode/blob/1df4bbd19fa28c1236f3253d0f659041757c029d/crates/forge_main/src/ui.rs
[55]: https://github.com/tailcallhq/forgecode/blob/1df4bbd19fa28c1236f3253d0f659041757c029d/crates/forge_domain/src/conversation.rs
[56]: https://github.com/google-gemini/gemini-cli/blob/v0.65.0/docs/get-started/authentication.mdx
[57]: https://github.com/google-gemini/gemini-cli/blob/v0.65.0/docs/reference/configuration.md
[58]: https://github.com/google-gemini/gemini-cli/blob/v0.65.0/docs/cli/headless.md
[59]: https://github.com/google-gemini/gemini-cli/blob/v0.65.0/LICENSE
[60]: https://github.com/google-gemini/gemini-cli/blob/v0.65.0/packages/core/src/core/loggingContentGenerator.ts
[61]: https://github.com/google-gemini/gemini-cli/releases/tag/v0.67.0-nightly.20261027.g363a13119
[62]: https://github.com/google-gemini/gemini-cli/blob/v0.65.0/packages/core/src/output/types.ts
[63]: https://github.com/google-gemini/gemini-cli/blob/v0.65.0/docs/reference/policy-engine.md
[64]: https://github.com/google-gemini/gemini-cli/releases/tag/v0.65.0
[65]: https://github.com/google-gemini/gemini-cli/blob/v0.65.0/docs/cli/sandbox.md
[66]: https://github.com/google-gemini/gemini-cli/blob/v0.65.0/packages/cli/src/config/sandboxConfig.ts
[67]: https://github.com/google-gemini/gemini-cli/blob/v0.65.0/packages/core/src/scheduler/scheduler.ts
[68]: https://github.com/google-gemini/gemini-cli/blob/v0.65.0/docs/core/subagents.md
[69]: https://github.com/google-gemini/gemini-cli/blob/v0.65.0/packages/core/src/telemetry/uiTelemetry.ts
[70]: https://raw.githubusercontent.com/aaif-goose/goose/main/documentation/docs/guides/context-engineering/subagents.mdx
[71]: https://raw.githubusercontent.com/aaif-goose/goose/main/documentation/docs/guides/running-tasks.md
[72]: https://raw.githubusercontent.com/aaif-goose/goose/main/LICENSE
[73]: https://raw.githubusercontent.com/aaif-goose/goose/main/documentation/docs/guides/managing-tools/goose-permissions.md
[74]: https://raw.githubusercontent.com/aaif-goose/goose/main/documentation/docs/getting-started/providers.md
[75]: https://api.github.com/repos/block/goose/releases?per_page=30
[76]: https://raw.githubusercontent.com/aaif-goose/goose/main/crates/goose-cli/src/session/mod.rs
[77]: https://raw.githubusercontent.com/gptme/gptme/master/docs/tools/subagent.rst
[78]: https://raw.githubusercontent.com/gptme/gptme/master/docs/providers-supported.rst
[79]: https://gptme.org/docs/cli/gptme.html
[80]: https://raw.githubusercontent.com/gptme/gptme/master/LICENSE
[81]: https://raw.githubusercontent.com/gptme/gptme/master/docs/providers.rst
[82]: https://api.github.com/repos/gptme/gptme/releases?per_page=100
[83]: https://raw.githubusercontent.com/gptme/gptme/master/gptme/sandbox.py
[84]: https://raw.githubusercontent.com/gptme/gptme/master/gptme/util/cost.py
[85]: https://github.com/NousResearch/hermes-agent/blob/v0.22.5/tools/delegate_tool_dispatch.py
[86]: https://github.com/NousResearch/hermes-agent/blob/v0.22.5/tools/environments/docker.py
[87]: https://github.com/NousResearch/hermes-agent/blob/v0.22.5/agent/turn_finalizer.py
[88]: https://github.com/NousResearch/hermes-agent/blob/v0.22.5/LICENSE
[89]: https://github.com/NousResearch/hermes-agent/blob/v0.22.5/website/docs/integrations/providers.md
[90]: https://api.github.com/repos/NousResearch/hermes-agent/releases/tags/v0.22.5
[91]: https://github.com/NousResearch/hermes-agent/blob/v0.22.5/hermes_cli/gateway_chat.py
[92]: https://github.com/NousResearch/hermes-agent/blob/v0.22.5/website/docs/user-guide/security.md
[93]: https://github.com/NousResearch/hermes-agent/blob/v0.22.5/hermes_cli/oneshot.py
[94]: https://github.com/NousResearch/hermes-agent/blob/v0.22.5/hermes_cli/gateway_chat_view.py
[95]: https://github.com/Kilo-Org/kilocode/blob/v7.8.18/packages/kilo-docs/pages/ai-providers/openai-chatgpt-plus-pro.md
[96]: https://github.com/Kilo-Org/kilocode/blob/v7.8.18/packages/opencode/src/plugin/github-copilot/copilot.ts
[97]: https://github.com/Kilo-Org/kilocode/blob/v7.8.18/packages/opencode/src/kilocode/session/cost-propagation.ts
[98]: https://registry.npmjs.org/@kilocode%2fcli
[99]: https://github.com/Kilo-Org/kilocode/blob/v7.8.18/packages/kilo-docs/pages/customize/agent-permissions.md
[100]: https://github.com/Kilo-Org/kilocode/blob/v7.8.18/packages/opencode/src/provider/provider.ts
[101]: https://github.com/Kilo-Org/kilocode/blob/v7.8.18/packages/opencode/src/cli/cmd/run.ts
[102]: https://github.com/Kilo-Org/kilocode/blob/v7.8.18/packages/kilo-docs/pages/getting-started/settings/sandboxing.md
[103]: https://github.com/Kilo-Org/kilocode/blob/v7.8.18/packages/opencode/src/tool/task.ts
[104]: https://raw.githubusercontent.com/MoonshotAI/kimi-code/main/docs/en/release-notes/changelog.md
[105]: https://raw.githubusercontent.com/MoonshotAI/kimi-code/main/docs/en/reference/kimi-command.md
[106]: https://raw.githubusercontent.com/MoonshotAI/kimi-code/main/docs/en/configuration/config-files.md
[107]: https://raw.githubusercontent.com/MoonshotAI/kimi-code/main/apps/kimi-code/src/cli/goal-prompt.ts
[108]: https://raw.githubusercontent.com/MoonshotAI/kimi-code/main/LICENSE
[109]: https://raw.githubusercontent.com/MoonshotAI/kimi-code/main/docs/en/configuration/providers.md
[110]: https://api.github.com/repos/MoonshotAI/kimi-code/releases?per_page=100
[111]: https://raw.githubusercontent.com/MoonshotAI/kimi-code/main/packages/agent-core-v2/src/os/backends/node-local/hostProcessService.ts
[112]: https://raw.githubusercontent.com/MoonshotAI/kimi-code/main/docs/en/reference/tools.md
[113]: https://raw.githubusercontent.com/MoonshotAI/kimi-code/main/packages/agent-core-v2/src/agent/usage/usageOps.ts
[114]: https://api.github.com/repos/letta-ai/letta-code/releases/latest
[115]: https://github.com/letta-ai/letta-code/blob/920f9e584e2e/src/headless.ts
[116]: https://github.com/letta-ai/letta-code/blob/920f9e584e2e/src/tools/impl/shell-sandbox.ts
[117]: https://github.com/letta-ai/letta-code/blob/920f9e584e2e/src/agent/approval-execution.ts
[118]: https://docs.letta.com/configuration/models
[119]: https://github.com/letta-ai/letta-code/blob/920f9e584e2e/src/providers/byok-providers.ts
[120]: https://github.com/letta-ai/letta-code/blob/920f9e584e2e/src/permissions/checker.ts
[121]: https://github.com/letta-ai/letta-code/blob/920f9e584e2e/src/agent/subagents/subagent-stream.ts
[122]: https://github.com/letta-ai/letta-code/blob/920f9e584e2e/src/sandbox/bwrap.ts
[123]: https://registry.npmjs.org/@letta-ai%2fletta-code
[124]: https://github.com/letta-ai/letta-code/blob/920f9e584e2e/README.md
[125]: https://raw.githubusercontent.com/SWE-agent/mini-swe-agent/main/src/minisweagent/run/benchmarks/swebench.py
[126]: https://mini-swe-agent.com/latest/models/quickstart/
[127]: https://mini-swe-agent.com/latest/usage/mini/
[128]: https://mini-swe-agent.com/latest/advanced/environments/
[129]: https://api.github.com/repos/SWE-agent/mini-swe-agent/releases
[130]: https://github.com/SWE-agent/mini-swe-agent
[131]: https://mini-swe-agent.com/latest/usage/output_files/
[132]: https://opencode.ai/v2/docs/cli/
[133]: https://api.github.com/repos/anomalyco/opencode/releases
[134]: https://opencode.ai/v2/docs/policies/
[135]: https://github.com/anomalyco/opencode/blob/v2.1.4/packages/cli/src/run/noninteractive.ts
[136]: https://opencode.ai/v2/docs/permissions/
[137]: https://opencode.ai/v2/docs/providers/
[138]: https://registry.npmjs.org/@opencode%2fcli
[139]: https://opencode.ai/v2/docs/tools/
[140]: https://docs.openhands.dev/sdk/guides/parallel-tool-execution.md
[141]: https://docs.openhands.dev/sdk/guides/llm-subscriptions.md
[142]: https://github.com/OpenHands/docs/blob/main/openhands/usage/cli/command-reference.mdx
[143]: https://docs.openhands.dev/openhands/usage/agent-canvas/backend-setup/docker-execution.md
[144]: https://raw.githubusercontent.com/OpenHands/OpenHands/main/bin/agent-canvas.mjs
[145]: https://registry.npmjs.org/@openhands/agent-canvas
[146]: https://github.com/OpenHands/OpenHands-CLI/blob/main/README.md
[147]: https://github.com/OpenHands/OpenHands-CLI/releases
[148]: https://docs.openhands.dev/openhands/usage/llms/llms.md
[149]: https://docs.openhands.dev/sdk/guides/metrics.md
[150]: https://raw.githubusercontent.com/earendil-works/pi/v1.4.0/packages/coding-agent/examples/extensions/subagent/README.md
[151]: https://pi.dev/docs/latest/cli
[152]: https://pi.dev/docs/latest/message-types
[153]: https://raw.githubusercontent.com/earendil-works/pi/v1.4.0/LICENSE
[154]: https://raw.githubusercontent.com/earendil-works/pi/v1.4.0/packages/coding-agent/src/modes/print-mode.ts
[155]: https://pi.dev/docs/latest/providers
[156]: https://api.github.com/repos/earendil-works/pi/releases?per_page=100&page=1
[157]: https://pi.dev/docs/latest/rpc-commands
[158]: https://raw.githubusercontent.com/earendil-works/pi/v1.4.0/packages/coding-agent/examples/extensions/sandbox/index.ts
[159]: https://pi.dev/docs/latest/security
[160]: https://qwenlm.github.io/qwen-code-docs/en/developers/tools/task/
[161]: https://qwenlm.github.io/qwen-code-docs/en/users/configuration/auth/
[162]: https://qwenlm.github.io/qwen-code-docs/en/users/features/headless/
[163]: https://raw.githubusercontent.com/QwenLM/qwen-code/main/packages/core/src/services/tokenUsageService.ts
[164]: https://raw.githubusercontent.com/QwenLM/qwen-code/main/LICENSE
[165]: https://qwenlm.github.io/qwen-code-docs/en/users/features/approval-mode/
[166]: https://qwenlm.github.io/qwen-code-docs/en/users/configuration/model-providers/
[167]: https://api.github.com/repos/QwenLM/qwen-code/releases
[168]: https://qwenlm.github.io/qwen-code-docs/en/users/features/sandbox/
[169]: https://qwenlm.github.io/qwen-code-docs/en/users/configuration/settings/
[170]: https://raw.githubusercontent.com/QwenLM/qwen-code/main/packages/cli/src/nonInteractive/types.ts
[171]: https://raw.githubusercontent.com/mistralai/mistral-vibe/v3.0.3/vibe/cli-rust/src/headless/usage.rs
[172]: https://raw.githubusercontent.com/mistralai/mistral-vibe/v3.0.3/vibe/core/tools/builtins/bash.py
[173]: https://raw.githubusercontent.com/mistralai/mistral-vibe/v3.0.3/vibe/app_server/_subagent_runs.py
[174]: https://raw.githubusercontent.com/mistralai/mistral-vibe/v3.0.3/vibe/cli-rust/src/cli.rs
[175]: https://raw.githubusercontent.com/mistralai/mistral-vibe/v3.0.3/vibe/core/platform_auth/_api_key.py
[176]: https://raw.githubusercontent.com/mistralai/mistral-vibe/v3.0.3/vibe/cli-rust/src/run_export/model.rs
[177]: https://raw.githubusercontent.com/mistralai/mistral-vibe/v3.0.3/vibe/app_server/run_export.py
[178]: https://raw.githubusercontent.com/mistralai/mistral-vibe/v3.0.3/harness/runtimes/python/python/mistralai_vibe_local_harness/vibe/_runtime_config.py
[179]: https://docs.mistral.ai/vibe/code/cli/install-setup
[180]: https://api.github.com/repos/mistralai/mistral-vibe/releases/latest
[181]: https://raw.githubusercontent.com/mistralai/mistral-vibe/v3.0.3/vibe/core/config/default_orchestrator.py
[182]: https://raw.githubusercontent.com/mistralai/mistral-vibe/v3.0.3/vibe/cli-rust/src/headless_run.rs
[183]: https://raw.githubusercontent.com/mistralai/mistral-vibe/v3.0.3/vibe/setup/auth/http_browser_sign_in_gateway.py
[184]: https://raw.githubusercontent.com/mistralai/mistral-vibe/v3.0.3/pyproject.toml
[185]: https://raw.githubusercontent.com/mistralai/mistral-vibe/v3.0.3/vibe/core/tools/utils.py
[186]: https://raw.githubusercontent.com/mistralai/mistral-vibe/v3.0.3/vibe/app_server/_unified_permissions.py
[187]: https://raw.githubusercontent.com/mistralai/mistral-vibe/v3.0.3/vibe/setup/auth/api_key_persistence.py
[188]: https://raw.githubusercontent.com/mistralai/mistral-vibe/v3.0.3/README.md
[189]: https://raw.githubusercontent.com/mistralai/mistral-vibe/v3.0.3/vibe/cli-rust/src/headless/report.rs
[190]: https://raw.githubusercontent.com/mistralai/mistral-vibe/v3.0.3/vibe/core/config/vibe_schema.py
[191]: https://raw.githubusercontent.com/mistralai/mistral-vibe/v3.0.3/vibe/app_server/_agent_socket.py
[192]: https://raw.githubusercontent.com/zai-org/ZCode/main/apps/zcode-cli/packages/contracts/src/tools/agent.ts
[193]: https://raw.githubusercontent.com/zai-org/ZCode/main/apps/zcode-cli/docs/usage/02-cli-reference.md
[194]: https://raw.githubusercontent.com/zai-org/ZCode/main/apps/zcode-cli/packages/cli/src/login-command.ts
[195]: https://raw.githubusercontent.com/zai-org/ZCode/main/NOTICE.md
[196]: https://raw.githubusercontent.com/zai-org/ZCode/main/apps/zcode-cli/packages/cli/package.json
[197]: https://raw.githubusercontent.com/zai-org/ZCode/main/apps/zcode-cli/packages/core/src/permission/service.ts
[198]: https://zcode.z.ai/en/changelog
[199]: https://raw.githubusercontent.com/zai-org/ZCode/main/config/provider/zcode-builtin.json
[200]: https://api.github.com/repos/zai-org/ZCode/releases?per_page=100
[201]: https://raw.githubusercontent.com/zai-org/ZCode/main/apps/zcode-cli/docs/design/v2/model/token-usage.md
[202]: https://raw.githubusercontent.com/zai-org/ZCode/main/apps/zcode-cli/packages/cli/src/headless-workflow.ts
