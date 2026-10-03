# Does the delivered IMD repository work against the real API?

A requester’s checklist · checked 2026-10-03 · about 3 pages

**Decision rule (recommendation):** accept a live-integration claim only when you can reproduce it from the delivered commit, through the delivered client, against `https://api.imd.fun`, with recorded responses. Passing locally invented fixtures alone does not establish that claim. The docs identify that origin as the control plane and expose its deployed commit through `/version`. [IMD: Base URLs](https://imd.fun/docs/#base)

**Evidence labels:** **Fact** means documented behavior; **Observation** means a call made for this report; **Recommendation/inference** means a checking method derived from that behavior, not an IMD guarantee. **Unknown** marks what the cited sources or this investigation cannot establish. No particular delivered repository or paid job was supplied, so this report certifies none.

## 1. Collect the delivery and review evidence

- [ ] **Fact:** retrieve `GET /jobs/:id`, `/jobs/:id/submissions`, and `/jobs/:id/result`. These expose the job’s scope, reviews and verdicts; attempts and findings; and accepted source/files, download URLs, hashes and delivery. Record the job ID, `delivery.repoUrl`, `delivery.commit`, PR URL and report artifact hash. Read the actual report named in `result.files`, rather than relying on the job title or completion badge. [IMD: Jobs](https://imd.fun/docs/#jobs)
- [ ] **Fact:** `GET /jobs/:id/report.md` is specifically the audit judge’s report, not a universal code-job report endpoint. A non-audit yields `404 unknown_audit`; an unaccepted judge yields `409 report_not_ready`. An audit reads existing code and produces findings; it does not build, fix or deploy it. [IMD: Jobs](https://imd.fun/docs/#jobs), [Auditing a repository](https://imd.fun/docs/#audit)
- [ ] **Fact + recommendation:** `adversarial-review` is documented as read-only review by a different seat. Find that node and read its findings and reproductions in the job/submissions, including unresolved findings and the reviewed scope. If absent, record “no adversarial review found.” Where needed, inspect `/jobs/:id/assessments` and the referenced review documents. A reviewer’s existence is evidence of review, not evidence that every README command or live API path was exercised. [IMD: Skills](https://imd.fun/docs/#continue), [Records and reviews](https://imd.fun/docs/#records)

**Inference:** an accepted output and its hash establish which bytes were delivered; they do not, by themselves, establish that an API integration works. Ask which concrete command, response and assertion support each report claim. The docs expose verdicts and findings separately from delivered source; use that separation. [IMD: Jobs](https://imd.fun/docs/#jobs)

## 2. Reproduce the exact tree, tests and README

- [ ] **Recommendation:** in a fresh directory, clone the recorded repository, check out the recorded commit, and compare `HEAD`. Do not test a moving default branch or assume the PR tip equals the delivery. The delivery includes a repository and commit; the docs likewise use `repoUrl` plus `baseCommit` to pin starting source. [IMD: Jobs](https://imd.fun/docs/#jobs), [Job body](https://imd.fun/docs/#job-body)

```sh
# Replace these two values with delivery.repoUrl and delivery.commit.
REPO_URL='https://github.com/OWNER/REPO'
DELIVERED_COMMIT='REPLACE_WITH_DELIVERED_COMMIT'
git clone "$REPO_URL" imd-delivery
cd imd-delivery
git checkout --detach "$DELIVERED_COMMIT"
test "$(git rev-parse HEAD)" = "$DELIVERED_COMMIT"
```

- [ ] **Recommendation:** follow the delivered README’s runtime, dependency installation, build and test commands literally, from its stated working directory. Record versions, exit codes, failures, skipped tests and any undocumented edits needed. There is no universal `npm test` or Foundry command for every IMD job: the docs describe multiple skills and an API exposing each skill’s checks. A successful substituted command does not validate the printed command. [IMD: Job body / Skills](https://imd.fun/docs/#continue), [Health and catalog](https://imd.fun/docs/#health)
- [ ] **Recommendation:** run the README’s actual client example with its documented API-origin configuration set to the control plane. Check output meaning, not just exit zero. If a claimed operation needs payment, separate the freely reproducible portion from the untested paid portion. IMD documents distinct public reads, check, quote, payment submission and order status routes. [IMD: Paid requests](https://imd.fun/docs/#paid)

## 3. Compare claims with independent live responses

**Fact:** the following GET routes are public. `/openapi.json` describes the paid request flow and enabled action limits; `/requests/capabilities` supplies current payment terms and limits. `/requests/check` takes `{action,input}`, requires no token, and returns preflight information without holding a price. It is the free preflight, not payment submission. [IMD: Health and catalog](https://imd.fun/docs/#health), [Paid requests](https://imd.fun/docs/#paid)

- [ ] **Recommendation:** capture a dated baseline, then replay the same inputs through the delivered client with mocking disabled. Compare URL, HTTP method, body, status, parsed fields and error handling with the direct response. This tests the client as well as the server.

```sh
# Requires a shell and curl supporting --fail-with-body.
export IMD_API='https://api.imd.fun'
mkdir -p evidence
curl --fail-with-body -D evidence/version.headers \
  "$IMD_API/version" -o evidence/version.json
curl --fail-with-body "$IMD_API/health" -o evidence/health.json
curl --fail-with-body "$IMD_API/requests/capabilities" -o evidence/capabilities.json
curl --fail-with-body "$IMD_API/openapi.json" -o evidence/openapi.json
# check.json must contain the action and input being tested, without requestKey.
curl --fail-with-body -D evidence/check.headers \
  -H 'Content-Type: application/json' --data-binary @check.json \
  "$IMD_API/requests/check" -o evidence/check-response.json
```

A complete, non-paying example for `check.json`:

```json
{
  "action": "job.open",
  "input": {
    "objective": "Write a sourced checklist for verifying delivered code against the live IMD API.",
    "skill": "research-report",
    "outputs": [{"name":"report","path":"artifacts/report.md","mediaType":"text/markdown"}],
    "github": false
  }
}
```

- [ ] **Fact + recommendation:** inspect the response body as well as HTTP status. A `200` can contain `blocked` or `unavailable`; preflight has `blockers` and `suggestions`. For failures, preserve the JSON error and status; respect `Retry-After` on `429`. Avoid asserting volatile queue counts or an exact response with no extra fields: the docs say examples are excerpts. [IMD: Errors](https://imd.fun/docs/#errors), [Paid requests](https://imd.fun/docs/#paid), [Docs introduction](https://imd.fun/docs/)

**Observation:** this report’s direct `/version` GET returned commit `ef84cc5fca6a304eddbc0a2f9ef743a2402a1af4`. The example preflight returned HTTP 200, `kind: "report"`, `judged: true`, no blockers, and suggestions about ambiguity and sources. These are dated observations, not permanent expected values. The route meanings are documented in [Health and catalog](https://imd.fun/docs/#health) and [Paid requests](https://imd.fun/docs/#paid).

**Unknown:** these probes establish neither paid execution nor repository delivery, browser CORS compatibility, deployment, or correctness of an unspecified client. A clean preflight is not an end-to-end paid test; payment has its own challenge/signature and admission flow. [IMD: Paid requests](https://imd.fun/docs/#paid), [Base URLs / CORS](https://imd.fun/docs/#base)

## 4. Spot a test that only proves its own mock

- [ ] **Recommendation:** trace the test from production client entry point to transport. Look for replaced `fetch`, HTTP interceptors, local servers, fixtures, fake clients and environment defaults. Ask whether a live test actually ran or was silently skipped. The independent comparison target is the documented control-plane origin and routes above. [IMD: Base URLs](https://imd.fun/docs/#base), [Paid requests](https://imd.fun/docs/#paid)
- [ ] **Inference:** a test that invents `{ok:true}`, returns it from its fake server, then asserts that same object proves only consistency with the fixture. Even a faithful fixture cannot establish current server behavior. Keep such unit tests, but require a separate live check through the delivered code. Derive expected method, input and response meaning from the docs, not solely from the implementation being tested. [IMD: Paid requests](https://imd.fun/docs/#paid)
- [ ] **Recommendation:** check a successful read/preflight and a documented error case relevant to the client; verify it retains server errors instead of converting them to fake success. For example, an invalid resource ID is documented as `400`. Never count “curl works” as proof that the repository’s parser works. [IMD: Errors](https://imd.fun/docs/#errors)

## 5. Specify a repair that job.continue can deliver

**Facts:** a continuation uses `parentJobId = project.head`; the project must satisfy the documented completion/blocked and inactivity conditions, and only its paying wallet may fund it. The plane chooses the starting repository and commit. Supplying `repoUrl`, `baseCommit`, `projectId`, `deploymentLaunchId` or `onchain` is refused. Nothing deploys again; a token is not replaced. Delivery is into the project repository by a fast-forward-merged PR. [IMD: Continuing a project](https://imd.fun/docs/#continue)

- [ ] **Recommendation:** request a specific reproducing fix, actual live tests, README commands and allowed file paths. Include every implementation/test/docs path needed; inspect step-level budgets too. `paths` and `steps[].paths` bound repository writes. Run a `job.continue` preflight with the real parent and intended input, and read its `project`, blockers and suggestions before paying. [IMD: Job body](https://imd.fun/docs/#job-body), [Continuing a project](https://imd.fun/docs/#continue)
- [ ] **Unknown / important limit:** the docs do not explicitly promise that `package.json` can be edited, or enumerate all protected repository files. A broad path or an objective mentioning dependencies is therefore not evidence that a protected file can change. Establish the particular job’s recorded scope and applicable skill restrictions; ask for a refusal explanation if the repair needs a protected manifest. A renamed manifest is not evidence that the README’s original install command now works. [IMD: Job body](https://imd.fun/docs/#job-body), [Jobs](https://imd.fun/docs/#jobs)
- [ ] **Fact + inference:** named outputs must specify a name, an `artifacts/` path and media type, and the job must produce exactly those outputs. Accepted files may feed later jobs as inputs. For a revised research report, declare the intended output explicitly and compare its new result entry and repository diff. Publication entries track project versions. **Unknown:** the docs do not specify filename-collision or rename/overwrite policy for republishing research under new names; do not assume a new name replaces an old report or changes which README links readers follow. [IMD: Job body](https://imd.fun/docs/#job-body), [Composing work](https://imd.fun/docs/#compose), [Publications](https://imd.fun/docs/#publications)

**Recommendation:** finish with a small evidence ledger: claim → delivered commit → exact command → live origin/time/server commit → status/body → result (verified, failed, or untested) → unresolved review finding. This preserves the difference between delivered bytes, reported success and behavior you actually reproduced. [IMD: Jobs](https://imd.fun/docs/#jobs), [Health and catalog](https://imd.fun/docs/#health)
