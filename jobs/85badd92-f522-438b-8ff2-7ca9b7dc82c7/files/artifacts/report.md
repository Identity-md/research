# Security audit of imd-panel

## Executive answer

**Audited revision:** `71b23963573b8deef6be3a335dd6f2b001e4d132` (“Network down: fail fast per host, say so on the page”).  
**Method:** static, line-by-line review of the checked-out Python and browser code. No live deployment or upstream was tested. File-and-line references below are attributable evidence from that revision.

The panel is reasonably resistant to ordinary drive-by CSRF and DNS rebinding under its default localhost-only configuration: it rejects non-local `Host` values; state-changing browser requests need a non-simple `X-Dashboard` header; no CORS permission is emitted; and hostile strings are usually HTML-escaped. Those controls are not authentication, however. Any local process can issue fully privileged requests, and a reverse proxy that makes a tailnet client appear as `127.0.0.1` extends that privilege to every client able to reach an allowed panel hostname. The code itself says Tailscale Serve has exactly that topology. Such a caller can stop the worker, change its configuration, run `imd doctor`, install skills and releases, or configure an attacker webhook.

The most serious independent defect is the rollback cache: a same-user process can replace both a cached `.tgz` and its adjacent `.sha256`; the panel then treats that attacker-selected digest as trusted and passes the archive to `npm install -g`, which may execute package lifecycle scripts. Fresh downloads compare an archive with `SHA256SUMS` fetched from the same GitHub release, so the digest proves consistency but supplies no trust independent of the release account/CDN. Cleanup also follows a symlink at the job-directory level and can recursively delete directories outside the work root.

I found HTML-injection sinks fed by GitHub/API values, but did **not** establish arbitrary JavaScript execution: the CSP disallows inline script and the principal transcript/task fields are escaped. The injection still permits misleading same-page markup and, because inline style is allowed, visual spoofing. Telegram notifications are a separate markup sink because hostile strings are sent with `parse_mode=HTML` without Telegram escaping.

### Findings

| ID | Severity | Finding |
|---|---:|---|
| F1 | High | Request-shape checks are treated as authorization; local and proxy-collapsed clients receive full control |
| F2 | High | Writable rollback cache enables same-user archive substitution and npm lifecycle execution |
| F3 | High | Cleanup follows a symlinked job directory and can recursively delete outside the work tree |
| F4 | Medium | Unescaped upstream values reach `innerHTML`; CSP limits but does not eliminate impact |
| F5 | Medium | Sensitive operational data is exposed by unauthenticated GET routes to every accepted host/client |
| F6 | Medium | Unbounded threaded requests, refreshes, journals, transcripts, and upstream bodies permit resource exhaustion |
| F7 | Medium | Telegram HTML injection and arbitrary webhook destination allow hostile data rendering/exfiltration |
| F8 | Medium | Release checksum is not an independent authenticity control; install deliberately executes release code |
| F9 | Low | Unit/config writes are non-transactional as a pair and unit edits are not safely atomic |

## Trust checks and complete route review

### What the checks actually prove

`trusted()` accepts `localhost`, `127.0.0.1`, `[::1]`, and arbitrary configured `allowedHosts` after stripping a conventional port ([server.py:43](../imd_panel/server.py#L43), [server.py:55](../imd_panel/server.py#L55)). This blocks the usual DNS-rebinding request whose `Host` remains the attacker domain. For `write=True`, an **absent Origin is accepted**; a present Origin must exactly equal `http://<Host>` or `https://<Host>`; `X-Dashboard` must equal `1`; and the peer address must be exactly IPv4 `127.0.0.1` ([server.py:62](../imd_panel/server.py#L62)).

Facts:

* A normal cross-origin `fetch` cannot set `X-Dashboard` without a CORS preflight, and the server implements neither `OPTIONS` nor `Access-Control-Allow-Origin`. A form can send a simple POST but cannot add the header. This blocks conventional browser CSRF.
* Same-origin script injection can perform every action because the page's `post()` supplies the header ([01-core.js:20](../imd_panel/assets/js/01-core.js#L20)).
* `curl`, malware, another same-user process, or any other non-browser local client can omit `Origin` and set `Host` and `X-Dashboard`; the values are not secrets.
* The documented Tailscale Serve arrangement says the panel sees proxied requests as `127.0.0.1` ([README.md:154](../README.md#L154)). If the public-facing name is in `allowedHosts`, a tailnet request with the custom header satisfies all code-level checks. Tailscale identity/ACLs may gate reachability, but the application does not authenticate or authorize a particular operator.
* Allowing a hostname whose DNS an attacker controls re-enables rebinding reads, and potentially writes from an attacker page if it can cause a same-origin script to run after rebinding. This is an inference dependent on browser DNS pinning/rebinding behavior and configuration; it is not present with the default empty `allowedHosts`.

Route inventory:

* `GET /` and `/index.html`: Host check only; reads the environment-selected `INDEX` joined to the package directory without validation ([server.py:121](../imd_panel/server.py#L121)). This is a local service-configuration risk, not a remote parameter traversal.
* `GET /assets/*`: Host check, then a restrictive one-level filename regex; `js/` is the only allowed subdirectory ([server.py:124](../imd_panel/server.py#L124)). No URL traversal was found. Symlinks already placed in the package assets directory are followed, but a requester cannot choose separators.
* `GET /api/transcript?id=`: Host check only. The ID is limited to 1–40 alphanumeric/underscore/hyphen characters before transcript matching ([collect.py:792](../imd_panel/collect.py#L792)). It exposes prompts, thinking excerpts, tool inputs/results, file-write contents, git status, pinned reads, and artifact contents ([collect.py:873](../imd_panel/collect.py#L873)).
* `GET /api/history`, `/api/data`, `/api/lite`: Host check only ([server.py:150](../imd_panel/server.py#L150)). `/api/data?refresh=1` performs a forced collection based on a substring test, allowing expensive work without the write guard.
* `GET /api/export`: additionally applies the write guard. `what` is mapped to two fixed unit names and `hours` must be digits capped at 366 days; the `journalctl` argv is therefore not injectable ([server.py:160](../imd_panel/server.py#L160)).
* All POST paths first apply the write guard, require a numeric `Content-Length` from 0 through 64 KiB, JSON-decode exactly that many bytes, and dispatch only through a fixed route table ([server.py:89](../imd_panel/server.py#L89), [server.py:563](../imd_panel/server.py#L563)). Chunked bodies are effectively read as empty, not unbounded. Exceptions are returned to the caller truncated to 400 characters and may disclose paths or command diagnostics.
* `/api/config`: validates tier/runtime/model/effort and concurrency. `/api/skills`: restricts the skill ID. `/api/worker`: allowlists the systemctl action. `/api/update`: allowlists its action and validates rollback tags in `_release_tgz`. `/api/guard` bounds percentages but not finite numeric values (JSON `1e309` becomes infinity and is written). `/api/notify` only requires an `https://` prefix for webhook URLs and does not constrain token/chat lengths beyond the total body. `/api/doctor` ignores its body. `/api/cleanup` ignores its body.

### F1 — request-shape checks are not authorization (High)

The exploit path is concrete: a local process sends, for example, `POST /api/worker`, `Host: localhost:8787`, `X-Dashboard: 1`, no `Origin`, and `{"action":"stop"}`. It passes [server.py:59](../imd_panel/server.py#L59)-[68](../imd_panel/server.py#L68) and invokes `systemctl --user stop` at [server.py:245](../imd_panel/server.py#L245). The same primitive reaches the other actions. Through a loopback reverse proxy, the same applies to any reachable client for which the proxy supplies/preserves an allowed Host.

Impact includes worker interruption; configuration/unit modification; arbitrary allowed skill installation; a paid doctor invocation; update/rollback; deletion via cleanup; and notifier reconfiguration. Setting `webhookUrl` then triggering notifications creates an application-supported exfiltration channel for task titles, IDs, failure reasons and network state.

Recommendation: authenticate requests with a high-entropy session/token unavailable to other origins and authorize a specific Tailscale identity at the proxy (for example, strict Serve/Funnel policy and identity headers validated only from a trusted proxy). Do not describe `X-Dashboard` as an authorization secret. Require a present, canonical allowed Origin for browser mutation as defense in depth, while retaining Host validation.

### Cross-origin reads and CSRF verdict

No permissive CORS headers exist, so SOP prevents a conventional malicious website from reading JSON even though GET routes do not inspect Origin. Host validation blocks ordinary rebinding under default settings. Cross-site image/navigation requests may still cause GET work, notably forced collection, but cannot read the result. The custom-header requirement blocks simple write CSRF. These are facts about the source; exact browser/proxy behavior was not dynamically tested.

## Subprocess review

No subprocess call uses `shell=True`; all reviewed commands use argv arrays. Remotely influenced arguments are generally constrained:

* `journalctl` unit names come from local panel configuration, export units from a fixed map, and hours is numeric ([collect.py:57](../imd_panel/collect.py#L57), [server.py:169](../imd_panel/server.py#L169)). A leading-dash unit from locally writable `panel.json` could affect command option parsing because no `--` delimiter is used, but that already requires state-file write access.
* `systemctl` actions and unit are allowlisted/local configuration; skill IDs are regex-limited; models are allowlisted ([server.py:187](../imd_panel/server.py#L187)-[253](../imd_panel/server.py#L253)).
* `imd doctor`, `imd update`, and `imd skills` resolve `imd` from process `PATH` first ([collect.py:543](../imd_panel/collect.py#L543)). A same-user attacker able to influence the service environment/PATH can substitute the executable, but such influence was not established from an HTTP or task-data path.
* `git -C <cwd> status` receives `cwd` from a transcript, but only after `realpath(cwd)` is below the work root. `core.fsmonitor=false` is forced ([collect.py:940](../imd_panel/collect.py#L940)). No shell injection exists. Whether other Git configuration features can cause command execution during this exact `status` operation remains unanswered; run Git with global/system config disabled and a sanitized environment if this boundary matters.
* `npm install -g ...tgz` receives a locally constructed, regex-derived cache path ([server.py:400](../imd_panel/server.py#L400)). There is no argv injection, but npm intentionally processes attacker-relevant package metadata and lifecycle scripts; see F2/F8.
* `du`, `pgrep`, Node/Claude version checks, and `systemctl show` take fixed or locally derived arguments. Command outputs are bounded only after the process completes, so `capture_output=True` can consume large memory for journal, Git, doctor, update, npm, and exports.

## Filesystem and path handling

### F2 — rollback cache substitution (High)

If `<state>/worker-versions/<valid-tag>.tgz` exists, `_release_tgz` reads the adjacent `.sha256` and accepts the archive when they match ([server.py:316](../imd_panel/server.py#L316)-[330](../imd_panel/server.py#L330)). Both files live in the panel user's mutable state directory and have no ownership/mode check. Any other process running as that Unix user can write an arbitrary npm package and its own digest there. A privileged panel caller then chooses that syntactically valid tag via `/api/update` `rollback`; the archive is passed to global npm installation ([server.py:400](../imd_panel/server.py#L400)-[410](../imd_panel/server.py#L410)). Package lifecycle scripts may execute as the panel/worker Unix user during install. The post-install build-string check occurs only after execution and cannot contain the compromise.

Recommendation: never trust the adjacent cached digest. On every use, revalidate against authenticated immutable release metadata/signature, or store the cache in a directory not writable by the threatened producer. Install with lifecycle scripts disabled if compatible, inspect/extract into a fresh directory with strict archive rules, and only atomically activate verified content.

### F3 — cleanup escapes through a job symlink (High)

`prune()` joins each entry under `work/` as `jp`, tests `os.path.isdir(jp)` (which follows symlinks), lists it, then joins child names and recursively removes old child directories ([server.py:264](../imd_panel/server.py#L264)-[281](../imd_panel/server.py#L281)). If a hostile task/local process can replace or create `work/<job>` as a symlink to an external directory, `np_` names real external children; `shutil.rmtree(np_)` recursively deletes them. The later transcript-directory loop similarly follows a symlink in the glob and calls `rmtree`; Python normally refuses `rmtree` on a top-level symlink, but the job-level case targets children beyond the symlink and is exploitable.

Recommendation: use `lstat`, reject symlinks for every traversed component, resolve each deletion candidate and require it to remain immediately within a resolved, non-symlink work root, and use descriptor-relative deletion where practical to avoid check/use races. Do not increment deletion counts when `rmtree(ignore_errors=True)` fails.

Artifact reads do better: `find_transcripts` validates IDs; the work directory must resolve beneath `WORK`; artifact-file symlinks and real paths outside the work directory are rejected ([collect.py:941](../imd_panel/collect.py#L941)-[959](../imd_panel/collect.py#L959)). However, `os.walk` has no total file/depth budget, applies `[:20]` separately in every directory, follows an `artifacts` symlink when it is the walk root, and may race between `realpath` and `open`. The realpath containment check prevents the straightforward credential symlink read, but descriptor-based opening would close the race.

### F9 — partial/non-atomic configuration edits (Low)

Worker config uses a mode-0600 temporary plus `os.replace`, which is good ([server.py:229](../imd_panel/server.py#L229)). The unit file is copied to a predictable backup and overwritten directly before `daemon-reload` ([server.py:222](../imd_panel/server.py#L222)-[228](../imd_panel/server.py#L228)); interruption can truncate it. Concurrency edits the unit before atomically updating config, so a failure can leave them inconsistent. `_set_auto_update` has the same direct overwrite. State JSON temporary names are predictable and generally do not use `O_EXCL`/`O_NOFOLLOW`; under the stated same-user hostile-process threat, symlink/race attacks are possible, although same-user access already exposes those state files directly.

## Browser rendering and notifications

### F4 — unescaped upstream HTML values (Medium)

The page has a correct general `esc()` helper and an HTTP(S)-only `safeUrl()` ([01-core.js:15](../imd_panel/assets/js/01-core.js#L15)). Transcript prompts, outputs, artifacts, task titles, reasons, tool data, URLs used in HTML, and most network fields pass through these helpers. The CSP blocks inline script, objects, framing, forms, and off-origin connections ([server.py:16](../imd_panel/server.py#L16)). This is meaningful defense in depth.

It is not systematic contextual encoding. Concrete hostile upstream paths include:

* GitHub `published_at` is copied into release objects ([collect.py:1557](../imd_panel/collect.py#L1557)-[1567](../imd_panel/collect.py#L1567)) and interpolated unescaped into two `innerHTML` templates ([01-core.js:166](../imd_panel/assets/js/01-core.js#L166), [01-core.js:172](../imd_panel/assets/js/01-core.js#L172)).
* Several API numeric/status/time fields are interpolated raw, including panel/fuzz counts in [01-core.js:235](../imd_panel/assets/js/01-core.js#L235)-[236](../imd_panel/assets/js/01-core.js#L236), turn timestamps/tool names in portions of [01-core.js:131](../imd_panel/assets/js/01-core.js#L131)-[134](../imd_panel/assets/js/01-core.js#L134), and API sentinel baseline in [01-core.js:365](../imd_panel/assets/js/01-core.js#L365). JSON has no runtime schema enforcement, so a hostile server can return strings where numbers are expected.

A payload such as `</span><div style="position:fixed;inset:0;...">...` can inject visible DOM. The current CSP's `style-src 'unsafe-inline'` permits inline styling, enabling a convincing UI overlay. I did not establish script execution: inline event handlers and `javascript:` generally fall under CSP script restrictions, external script must be same-origin, `connect-src` is self, and `form-action 'none'` blocks form submission. Treat this as markup/UI injection with possible clickjacking-like operator deception, not proven arbitrary XSS.

Recommendation: use DOM creation and `textContent`; otherwise encode every dynamic value according to its HTML/attribute context and validate upstream JSON types. Remove `'unsafe-inline'` styles if practical. Add automated sink tests with strings in every upstream field, including numeric/time fields.

### F7 — Telegram markup injection and notifier destinations (Medium)

Telegram is sent with `parse_mode=HTML` ([notify.py:52](../imd_panel/notify.py#L52)-[59](../imd_panel/notify.py#L59)), while network/transcript-derived values such as Claude limit messages, task titles and rejection reasons, API routes, guard reasons, update failure notes, and standing failures are inserted without escaping ([notify.py:98](../imd_panel/notify.py#L98)-[154](../imd_panel/notify.py#L154)). An attacker controlling those strings can inject Telegram-supported formatting/links or malformed markup that makes delivery fail. The generic webhook receives JSON, so it has no injection at this sender layer; rendering safety belongs to the receiver.

`/api/notify` accepts any string beginning `https://` ([server.py:541](../imd_panel/server.py#L541)-[555](../imd_panel/server.py#L555)). A privileged caller can cause POSTs to arbitrary internet or internal HTTPS endpoints; DNS resolution/redirect behavior is delegated to `urllib`. No response-size limit exists (`r.read()`), enabling memory exhaustion. Escape Telegram HTML with the platform-specific rules, validate destination host/IP/redirect policy, and cap response bytes.

## Secrets and data exposure

### F5 — accepted clients can read highly sensitive operational content (Medium)

`/api/data`, `/api/lite`, `/api/history`, and `/api/transcript` have no application authentication beyond Host. `/api/data` includes task titles and last agent text, journal events, server/wallet/token ID, config and unit paths, complete `ExecStart`, runtime configuration, fleet/standing data, notifier send history, and other network data. `effective_config()` deliberately omits `deviceKey` and `devicePrivateKey` from `otherKeys`, and `read_config()` selects only non-secret fields ([collect.py:430](../imd_panel/collect.py#L430), [collect.py:491](../imd_panel/collect.py#L491)-[518](../imd_panel/collect.py#L518)). Notifier token and credential-bearing webhook URL are masked before entering the feed ([notify.py:29](../imd_panel/notify.py#L29), [server.py:38](../imd_panel/server.py#L38)). Those are positive controls.

Nevertheless, `unit.execStart` is returned verbatim. If an operator has placed credentials in the unit command line, they are exposed; the code does not redact arbitrary arguments. Transcript responses are substantially more sensitive and can include secrets agents saw or emitted, complete prompts, partial command/tool results, written file contents and artifacts. The raw export guard does not protect these richer GET feeds. Any local process or admitted reverse-proxy client can read them; a malicious website cannot normally read them because of SOP, subject to the rebinding caveat above.

Recommendation: require authentication for reads, separate operational summary from transcript/artifact access, redact known secret patterns and unit arguments, and default transcript access off for remote/tailnet sessions.

## Denial of service

### F6 — bounded POST body, but unbounded work and reads (Medium)

The 64 KiB POST limit is sound, but the server is `ThreadingHTTPServer` with no connection/thread cap or socket timeout ([server.py:566](../imd_panel/server.py#L566)). A reachable client can hold many slow connections or issue many requests. The global data lock serializes collection, but every `/api/data?refresh=1` forces expensive journal, transcript, subprocess, filesystem and network work ([server.py:32](../imd_panel/server.py#L32), [server.py:152](../imd_panel/server.py#L152)). Waiting threads accumulate.

Specific unbounded/late-bounded inputs:

* `journalctl` captures the complete unit journal with no `-n`/`--since` and `read_journal` parses it all ([collect.py:57](../imd_panel/collect.py#L57)). Raw export also captures up to a year or all history in memory before sending.
* Transcript discovery parses every matching JSONL file; `parse_session` has no file/line/count cap ([collect.py:158](../imd_panel/collect.py#L158)-[224](../imd_panel/collect.py#L224)). Detailed transcript parsing reads every line and only trims the assembled response after `json.dumps`; prompts and accumulated turns remain largely unbounded ([collect.py:873](../imd_panel/collect.py#L873)-[968](../imd_panel/collect.py#L968)). A single huge JSONL line is loaded and decoded whole.
* Generic `http_get` uses `r.read()` with no maximum ([collect.py:402](../imd_panel/collect.py#L402)-[423](../imd_panel/collect.py#L423)); GitHub releases JSON and notification responses are also unbounded. The rollback archive alone has an explicit 32 MiB cap.
* Artifact traversal has no total directory/file budget; gzip compression is performed per response and can be repeatedly induced.
* The guard endpoint starts a new `guard_tick` thread on every request ([server.py:520](../imd_panel/server.py#L520)-[537](../imd_panel/server.py#L537)), allowing an authenticated/local caller to create many expensive concurrent collectors.

Recommendation: cap server workers/connections and request time; reject slow/incomplete bodies; rate-limit refresh/actions; coalesce guard ticks; bound journals by time/count; stream or cap command output and upstream bodies; impose transcript file/line/turn and artifact traversal budgets; and paginate transcript/data responses.

## Release rollback supply chain

### F8 — same-origin digest is integrity, not provenance (Medium; F2 raises local substitution to High)

For a fresh archive, the code validates the tag syntax, downloads `SHA256SUMS` and `identitymd-worker.tgz` from the hard-coded GitHub repository/release URL over HTTPS, caps them at 4 KiB and 32 MiB, and compares SHA-256 before an atomic archive rename ([server.py:316](../imd_panel/server.py#L316)-[353](../imd_panel/server.py#L353)). It then compares the installed build string with the tag-derived expected build ([server.py:400](../imd_panel/server.py#L400)-[410](../imd_panel/server.py#L410)). These detect corruption and some accidental mismatch.

They do not authenticate the publisher independently: an attacker controlling the GitHub repository/release (or any trusted delivery layer capable of changing both HTTPS responses) supplies both archive and checksum. The checksum file is not signature-verified, release asset URLs discovered by `releases_fetch` are not cross-checked, and rollback accepts any syntactically valid tag rather than requiring that tag to appear in the fetched release list. `npm install` is invoked without `--ignore-scripts`, so the security boundary is intentionally equivalent to executing the archive as the Unix user. The installed build check is not a sandbox.

Recommendation: verify a signature/provenance statement rooted outside the mutable release assets (pinned maintainer keys, Sigstore identity/policy, or a pinned immutable manifest), bind tag, commit and archive digest, and harden extraction/install. Resolve F2 even if signed fresh downloads are added.

## Priority remediation order

1. Add real read/write authentication and explicit proxy identity authorization; preserve Host/Origin/custom-header checks as secondary defenses.
2. Remove trust in cached adjacent hashes; independently authenticate releases and prevent npm lifecycle execution before verification.
3. Fix cleanup with no-follow, containment-safe deletion.
4. Replace hostile-data `innerHTML` construction and Telegram HTML interpolation with contextual escaping/DOM APIs.
5. Bound threads, forced refresh, journal/transcript/artifact parsing, subprocess output, and network response sizes.
6. Minimize/redact `/api/data` and gate transcript/artifact access separately; make config/unit writes atomic and recoverable.

## Uncertainty and unanswered questions

* No `repoUrl`/`baseCommit` metadata file was present beyond the checked-out Git commit, so repository origin was not independently verified. The audited commit hash is a fact from local Git metadata; authorship/provenance is not.
* The effective Tailscale ACLs, Serve header behavior, whether `allowedHosts` includes the tailnet name, and whether another authenticating proxy is deployed were unavailable. F1's direct local exploit is certain; its tailnet reach is conditional on the documented topology/configuration.
* Browser CSP enforcement and DNS-rebinding behavior were not dynamically tested. The report distinguishes proven HTML injection from unproven script execution.
* Filesystem permissions on `~/.config/imd-panel`, work roots, transcripts, npm prefix and systemd units were unavailable. Findings under the stated “other local processes” threat assume a process running as the same Unix user can modify same-user files; a sandbox or MAC policy could reduce that reach.
* Upstream schemas were not fetched. The page does not enforce them, so hostile type substitution is a valid defensive test even if current honest servers always return numeric/time types.
* npm's exact script behavior depends on the installed npm version and package contents. Passing an untrusted package to global install is the demonstrated code path; a proof-of-concept lifecycle script was intentionally not executed.

