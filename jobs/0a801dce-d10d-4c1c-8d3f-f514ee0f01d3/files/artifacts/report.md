# Missing files in published job 93a5396b (Fren Pet "Bonk" fee report)

**Question.** The published report at
[`jobs/93a5396b-fd54-4339-a9a9-6d3a1e7f5005/files/artifacts/report.md`](https://github.com/Identity-md/research/blob/main/jobs/93a5396b-fd54-4339-a9a9-6d3a1e7f5005/files/artifacts/report.md)
links to files that return HTTP 404. This report asks: which links are broken, why, where the files are (if anywhere), and how to prevent it.

**Short answer.**
- **Broken links.** Every one of the report's 13 relative links returns 404, on both `github.com/.../blob/...` and `raw.githubusercontent.com`. None of the files was ever committed to the research repository.
- **Cause.** The worker that ran the job writes `artifacts/` into the workspace's `.git/info/exclude`, so files under `artifacts/` never go into the source bundle. The only file uploaded from `artifacts/` was the single declared *named output*, `artifacts/report.md`. The publisher then published only that one declared artifact. The other outputs the report links to (heatmap, CSVs, JSON evidence, check log) fell into the gap between these two delivery paths.
- **Recovery.** 2 of the 13 targets (`../README.md` and `../scripts/analyze.py`) can be recovered byte-for-byte from the job's submission bundle, which the control plane still serves publicly. The other 11 targets (all data and images) are not in any public location I checked. They can probably be rebuilt from the recovered scripts plus the public chain data. One exception: the frozen USD quote can't be fetched again. Its value and timestamp are recorded in the report text.
- **Scope.** Only this job is affected. None of the other 12 published reports in the repository has a relative link to a missing file.

All checks were run on **2026-09-25 between about 05:05 and 05:15 UTC**. Labels used below: **Fact** = directly observed, with a source. **Inference** = reasoned from facts, not directly observed. **Uncertain / Unanswered** = open.

---

## 1. Broken links

**Fact.** I pulled every Markdown link target out of the published report (10,164 bytes, SHA-256 `a45cfd8b…6bf2`, matching `artifacts[0].hash` in the [publication manifest](https://github.com/Identity-md/research/blob/main/jobs/93a5396b-fd54-4339-a9a9-6d3a1e7f5005/_identitymd/manifest.json)). I resolved each one against `files/artifacts/` and requested it from both GitHub endpoints.

| # | Link text in report | Relative target | Resolves to (repo path under `jobs/93a5396b-…/`) | GitHub blob | raw | Recoverable? |
|---|---|---|---|---|---|---|
| 1 | "Computed results" | `summary.json` | `files/artifacts/summary.json` | 404 | 404 | No public copy found |
| 2 | "every pair and its transaction hashes" | `bonks.csv` | `files/artifacts/bonks.csv` | 404 | 404 | No public copy found |
| 3 | "Query manifest" | `evidence/manifest.json` | `files/artifacts/evidence/manifest.json` | 404 | 404 | No public copy found |
| 4 | "boundary block responses" | `evidence/boundary-blocks.json` | `files/artifacts/evidence/boundary-blocks.json` | 404 | 404 | No public copy found (can be re-fetched from chain) |
| 5 | "Receipt-derived transaction data" / "All successes and failures" | `transactions.csv` | `files/artifacts/transactions.csv` | 404 | 404 | No public copy found |
| 6 | "saved locally" (USD quote) | `evidence/usd-quote.json` | `files/artifacts/evidence/usd-quote.json` | 404 | 404 | **No, the spot quote can't be fetched again** |
| 7 | Embedded image + "Open the standalone heatmap" | `heatmap.svg` | `files/artifacts/heatmap.svg` | 404 | 404 | No public copy found |
| 8 | "Exact 48-bin values in CSV" | `intervals.csv` | `files/artifacts/intervals.csv` | 404 | 404 | No public copy found |
| 9 | "Raw transaction history" | `evidence/transactions.json` | `files/artifacts/evidence/transactions.json` | 404 | 404 | No public copy found (can be re-fetched) |
| 10 | "the offline analysis" | `../scripts/analyze.py` | `files/scripts/analyze.py` | 404 | 404 | **Yes, in the submission bundle** |
| 11 | "saved explorer cross-checks" | `evidence/fee-crosschecks.json` | `files/artifacts/evidence/fee-crosschecks.json` | 404 | 404 | No public copy found |
| 12 | "Local check result" | `checks.txt` | `files/artifacts/checks.txt` | 404 | 404 | No public copy found |
| 13 | "README" | `../README.md` | `files/README.md` | 404 | 404 | **Yes, in the submission bundle** |

The report also names some files in plain text, without a link. These are missing too:

| Mentioned as | Expected location | Status |
|---|---|---|
| `evidence/transactions-initial.json` | `files/artifacts/evidence/` | 404 |
| `evidence/logs-*.json` (22 files per the report) | `files/artifacts/evidence/` | not in repository tree |
| `python3 scripts/write_report.py` | `files/scripts/` | not in repository; **recoverable from bundle** |
| `scripts/collect.py` (referenced by the recovered README) | `files/scripts/` | not in repository; **recoverable from bundle** |
| `evidence/receipts-*.json`, `evidence/txcheck-*.json` (written by the recovered `collect.py`) | `files/artifacts/evidence/` | not in repository |

**External links in the same report**, checked for completeness. These aren't part of the missing-file problem:

| Target | Result | Note |
|---|---|---|
| `base.blockscout.com/address/0x0e22…443C` | 200 | OK |
| `api.coinbase.com/v2/prices/ETH-USD/spot` | 200 | OK, but it returns the *current* price, not the quote the report used |
| Blockscout `txlist` API URL for blocks 51,714,727–51,757,926 | 200 | OK |
| `mainnet.base.org` | 405 on GET | **Not broken.** It is a JSON-RPC endpoint. A POST `eth_blockNumber` returned a valid result. |
| `basescan.org/tx/0x451b…083c`, `basescan.org/tx/0x7540…64a7` | 403 to scripted requests, even with a browser User-Agent | **Uncertain.** This looks like bot protection, not a missing page. Both transactions returned 200 from the Blockscout v2 API. I didn't check them in a real browser. |
| `docs.base.org/specifications/transactions/network-fees` | 200 | OK |

## 2. What was actually published

**Fact.** The GitHub API tree for `Identity-md/research@main` (not truncated, 123 entries) holds exactly three files for this job:
`_identitymd/README.md`, `_identitymd/manifest.json` and `files/artifacts/report.md`.
The repository has one branch (`main`) and no releases.

**Fact.** Only one commit touches the job folder: [`4c76909`](https://github.com/Identity-md/research/commit/4c76909599e2c4d1590f224666a490ef371e5040) ("identitymd: publish research 93a5396b…", 2026-09-25T03:29:45Z, `Publisher: 0.1.0+5bfa8261`). It *adds* those three files and nothing else. So the files weren't published and later deleted. They were never published.

**Fact.** The [publication manifest](https://github.com/Identity-md/research/blob/main/jobs/93a5396b-fd54-4339-a9a9-6d3a1e7f5005/_identitymd/manifest.json) lists a single artifact: `{"name":"report","path":"artifacts/report.md","publishedPath":"files/artifacts/report.md"}`. The [job README](https://github.com/Identity-md/research/blob/main/jobs/93a5396b-fd54-4339-a9a9-6d3a1e7f5005/_identitymd/README.md) says the files were "published by the publisher service from accepted, hash-verified named artifacts" and lists only `report`.

**Fact.** The same manifest records the contributor's source submission: `changedPaths: ["README.md","scripts/analyze.py","scripts/collect.py","scripts/write_report.py"]`, `treeHash e20c46fd…`, `evaluation: "structural"`, `profile: "none"`. None of the heatmap, CSV, JSON or evidence files appears in the source submission.

**Fact.** The public job record [`https://api.imd.fun/jobs/93a5396b-…`](https://api.imd.fun/jobs/93a5396b-fd54-4339-a9a9-6d3a1e7f5005) shows `state: completed`, a node verdict of `accepted` with detail *"paths and tree verified; no suite was run for this kind of work"*, and `delivery.commit = 4c76909…`.

## 3. Cause

### 3.1 Worker: `artifacts/` is excluded from the source bundle

**Fact.** The public worker distribution ([`Identity-md/worker` `dist/cli.js`](https://github.com/Identity-md/worker/blob/main/dist/cli.js), at commit `cb75443` "Update worker 0.1.0 (5bfa82612889)", 2026-09-24T23:18Z) contains:

```js
async function excludeBuildArtifacts(workspace){
  const patterns=["out/","cache/","broadcast/","artifacts/","**/node_modules/", …, SCRATCH_DIR, READS_DIR, …].join("\n");
  await writeFile7(join8(workspace,".git","info","exclude"),patterns)…
```

It also packages source with `git add -A` and then `git update-index --force-remove` for each named output (`packageSource`). The `.git/info/exclude` in this task's own workspace contains exactly that list, including `artifacts/`, so the behavior is live on current workers.

**Fact.** The same file tells the agent: *"Named outputs are delivered separately from source… leave those files untracked… The daemon uploads them itself."* It then loops only over `task.outputs` to upload artifacts (`describeArtifact(workspace, output)` for each declared output).

**Inference.** `out/`, `cache/`, `broadcast/` and `artifacts/` are the default Foundry/Hardhat build directories. The exclude list looks like it was written for smart-contract builds and is now also applied to research jobs, where `artifacts/` is the deliverable folder. So anything the agent writes under `artifacts/` goes through one of two paths:
- if it's a declared named output, it's uploaded as an artifact;
- otherwise it's silently ignored by git and not uploaded at all.

### 3.2 Job definition: only one named output was declared

**Fact.** The manifest shows the job had a single declared output, `report` → `artifacts/report.md`. Compare job [`4099a969`](https://github.com/Identity-md/research/blob/main/jobs/4099a969-2562-4ec4-a16b-0ed858d140b0/_identitymd/manifest.json), whose manifest declares two outputs (`r1-data` → `artifacts/r1-data.json` and `r1-report` → `artifacts/r1-report.md`); both were published.

**Fact.** The original agent wrote its outputs under `artifacts/`. Its `scripts/analyze.py` writes `summary.json`, `heatmap.svg`, `checks.txt`, `bonks.csv`, `transactions.csv` and `intervals.csv` there, and `collect.py` writes to `artifacts/evidence/`. Its README says: *"Read the report and the heatmap (`artifacts/heatmap.svg`)… `artifacts/evidence/` contains transaction history, raw JSON-RPC receipts and logs…"*.

**Inference.** The agent expected these files to be delivered with the report. Because of 3.1, they fell into neither delivery path.

### 3.3 Verification and publishing didn't check links

**Fact.** Acceptance was `structural`/profile `none` ("paths and tree verified"), and the job README states that publication "does not establish … completeness". The publisher copies only the declared artifacts into `files/`. It does not copy the source tree, so even the committed `README.md` and `scripts/` were not published.

**Fact.** The research repository's own [README](https://github.com/Identity-md/research/blob/main/README.md) says that automated publishing "needs a shared-repository delivery path" and that *"the existing `github: true` source-delivery option does not copy named research output files."* The same README says a job folder should hold "Markdown reports and their supporting datasets".

**Inference.** No step between the agent and the public repository checks that the report's relative links resolve to published files. So a report that is internally consistent in the workspace passed every gate while pointing at files that were never going to be published.

### 3.4 Placement: `files/artifacts/` vs. `../`

**Fact.** Two links (`../scripts/analyze.py`, `../README.md`) climb out of `artifacts/`. In the workspace these point to repository-root files. After publication they resolve to `files/scripts/analyze.py` and `files/README.md`. The publisher never creates those paths, because it doesn't publish source.

## 4. Where the missing files are

**Fact: recoverable (2 linked targets + 2 unlinked scripts).** The control plane still serves the contributor's source bundle publicly:
`https://api.imd.fun/bundles/ee17b54c164aeebc35c0580b743412d086a4aea9f4bfcbdd6384787dbf03622b`
(11,616 bytes; SHA-256 matches the `bundleHash` in the manifest). It is a git bundle whose prerequisite is the empty-workspace commit `0243d7d`. Fetched into a clone of that commit, ref `imd-submission` = `795756b0…` has tree `e20c46fd…`, which equals the manifest's `verifiedTreeHash`. It contains:

| File | Bytes | Blob |
|---|---:|---|
| `README.md` | 1,921 | `258fd7e5` |
| `scripts/analyze.py` | 9,313 | `2d205133` |
| `scripts/collect.py` | 2,792 | `a7f85adc` |
| `scripts/write_report.py` | 11,164 | `3b88a135` |

To reproduce (network required for the first command):

```sh
curl -o b.bundle https://api.imd.fun/bundles/ee17b54c164aeebc35c0580b743412d086a4aea9f4bfcbdd6384787dbf03622b
# run inside a clone of any IdentityMD empty workspace, which contains commit 0243d7da4a4337ae8b16bcdf15bb4ead736fd68f
git fetch /path/to/b.bundle refs/heads/imd-submission:sub && git ls-tree -r sub
```

A plain `git init` repository fails with "Repository lacks these prerequisite commits: 0243d7d…". I used a clone of this task's own workspace, which starts from that commit.

**Fact: the report itself** is also served at `https://api.imd.fun/artifacts/a45cfd8b…6bf2` (200, 10,164 bytes, identical hash).

**Fact: not found (11 linked targets + unlinked evidence).** I checked the `research` repository's full tree, its only branch, its releases (none) and its commit history; the bundle above; and the other `Identity-md` org repositories by name (`worker`, `awesome-imd`, `empty-base`, `univ4hook-start-template`). The data and image files were in none of them. I didn't search each org repo's contents. The public API has no `jobs/<id>/outputs` route (404).

**Inference.** By the design in 3.1, the files probably exist only on the original worker machine, in its job workspace directory, if it hasn't been cleaned up. That machine is identified only by `deviceKey d78e1224…` and seat `tokenId 1084` / `agentId 51209`.

**Inference: possible regeneration.** The recovered `collect.py` downloads everything under `evidence/` again for the fixed block range 51,714,727–51,757,926. Its inputs are the public Blockscout API and the Base RPC, and both responded during this check. `analyze.py` then rebuilds the CSVs, `summary.json`, `heatmap.svg` and `checks.txt` offline. Two things can't be reproduced exactly:
- `evidence/usd-quote.json`: the Coinbase spot endpoint returns only the current price. The report records the value ($2,675.835/ETH) and retrieval time (2026-09-25T03:20:10.546747Z), so a hand-built substitute is possible, but it wouldn't be the original response.
- `evidence/transactions-initial.json`: the original first response, which the report says omitted two calls. A new request would not reproduce that omission.

I didn't run the regeneration, so its byte-for-byte fidelity is **untested**.

## 5. Is this systemic?

**Fact.** I scanned all 13 Markdown reports under `jobs/*/files/artifacts/` for relative links and checked them against the repository tree. Only job `93a5396b` has any (13, all missing). The other 12 reports use only absolute URLs or no links.

**Inference.** The defect isn't unique to this job. Any research job whose agent writes more than the declared outputs into `artifacts/` and links to them will lose them. It showed up here because this report was the first to link to local supporting files.

## 6. Recommended fixes

In order of leverage. These are suggestions, and none has been implemented.

1. **Fix at the source: stop excluding `artifacts/` for research jobs.** Apply the Foundry-style exclude list (`out/ cache/ broadcast/ artifacts/`) only to contract/build templates. Or deliver the whole `artifacts/` tree as outputs when the template is `skill:research-report`.
2. **Declare outputs as a directory, not a single file.** Let research tasks declare `artifacts/**` (with size limits; the worker already caps outputs at 128 MiB total, `MAX_OUTPUT_BYTES`). Or let the agent register extra named outputs at run time. Record every file in the publication manifest with its hash, as job `4099a969` does for its two outputs.
3. **Add a link-integrity gate before acceptance.** In the worker or verifier, parse each Markdown output. Every relative link or image must resolve to another delivered output. Otherwise reject with a clear code (e.g. `unresolved_local_reference`) so the agent's repair loop can fix it. This is cheap, needs no network, and fits the existing "structural" profile.
4. **Add the same check to the publisher after commit.** After writing to `Identity-md/research`, check each relative target against the committed tree. Refuse or flag the publication, and write the result into `_identitymd/manifest.json`.
5. **Tell agents in the prompt.** Until 1–2 land, the task prompt should say plainly that *only the named outputs are published and `artifacts/` is git-excluded*. Agents should then embed essential figures inline (e.g. an SVG or table in the Markdown) or link only to absolute, durable URLs.
6. **Publish or link the source bundle.** When a report links outside `artifacts/` (`../scripts`, `../README.md`), either publish the verified source tree under `files/`, or add the `api.imd.fun/bundles/<hash>` URL to the job README so readers can find it.
7. **Repair this job.** Following the repository README's rule to "add reviewed revisions as new versions", publish the four recovered source files, plus regenerated data marked *regenerated, not original*. Or ask the original contributor (device `d78e1224…`) for the original files, and add an errata note to the job README. Keep the original `report.md` unchanged so its hash stays valid.

## 7. Uncertainty and unanswered questions

- **Unanswered:** whether the original data files still exist on the contributor's machine. Only the operator or contributor can confirm this.
- **Uncertain:** my reading of the worker comes from its public minified `dist/cli.js` at the current commit (`5bfa8261`). The publication commit records `Publisher: 0.1.0+5bfa8261`, but the manifest doesn't record the worker version that ran the job (≈03:10–03:29Z on 2026-09-25). The worker commit `cb75443` (23:18Z on 2026-09-24) came before the job, so the same exclude logic very likely applied, but I haven't confirmed it for that exact run.
- **Uncertain:** the publisher's backend source isn't public (the [worker README](https://github.com/Identity-md/worker) says "Backend source and service credentials are not distributed"). The statement that it publishes only declared artifacts is inferred from the manifest, the job README wording and the commit contents, not from its code.
- **Uncertain:** the two `basescan.org` links returned 403 to scripted requests, which is probably bot protection. I didn't check them in a browser.
- **Not done:** I didn't regenerate the missing data or test whether regeneration reproduces the report's numbers. I didn't search inside the contents of other org repositories.
- **Limit:** HTTP results are as of 2026-09-25 ~05:10 UTC and can change if the repository is repaired.
