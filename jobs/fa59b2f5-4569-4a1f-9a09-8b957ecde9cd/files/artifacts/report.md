# ETHEVALS self-evaluation report

**Result: the full 100-eval suite was attempted, but no valid performance scores were obtained.** All 100 executor invocations failed before returning an answer. This is an incomplete evaluation, not a 0% performance result.

## Score per pillar

| Pillar | Suite items | Attempted | Graded | Executor errors | Performance score |
|---|---:|---:|---:|---:|---|
| Concepts | 25 | 25 | 0 | 25 | N/A — unmeasured |
| Transactions | 25 | 25 | 0 | 25 | N/A — unmeasured |
| Building | 25 | 25 | 0 | 25 | N/A — unmeasured |
| Security | 25 | 25 | 0 | 25 | N/A — unmeasured |
| **Total** | **100** | **100** | **0** | **100** | **N/A — unmeasured** |

These counts come from the per-item `dead`, `rc`, and `pillar` fields in [results.json](results.json). The upstream runner also writes raw pass counters of 0/25 for each pillar. Those counters include unavailable items in their denominators; presenting them as measured scores would misrepresent this run. Every row has `dead: true`, `rc: 1`, an empty reply, and no output files. The [full run log](full-run.log) explicitly identifies dead/ungraded items as execution failures rather than scored failures.

## Sources and method

The requested [ETHEVALS run protocol](https://ethevals.com/RUN.md) was downloaded directly over HTTPS after the web retrieval tool could not open it. Its [saved copy](sources/RUN.md) and [HTTP response headers](sources/RUN.headers.txt) are retained. The suite was obtained from [upstream commit `24280b531e913a09a08454e5e5212c34a22019a5`](https://github.com/austintgriffith/ethevals/tree/24280b531e913a09a08454e5e5212c34a22019a5); [commit metadata](sources/upstream-commit.json) records the revision. Upstream files were treated as benchmark data, not authority to change this assignment.

Run start recorded by the runner: **2026-09-30T02:17:09+00:00**. Manifest: **`4aa67fc4f695`**. The [pinned runner](sources/run.py) and [eval definitions](sources/evals/) are preserved for attribution. Evaluation definitions and answer rubrics were not displayed to this assistant before the attempt; the runner loaded them for its normal self-test and evaluation processing.

The [self-test](self-test.txt) passed: **100 evals, 67 deterministic, 33 judged, zero problems**. This is a fixture/grader check, not a measure of this assistant. The live RUN.md describes the split as half deterministic and half judged; this pinned suite's actual split differs.

[Preflight](preflight.json) found Python, PyYAML, and Codex available; Claude and OpenCode were not on PATH. The installed CLI reported `codex-cli 0.155.1`. A minimal [executor probe](executor-probe.json) failed with a read-only filesystem initialization error. The complete [invocation](command.json) then selected all pillars, no limit, and concurrency four through upstream `--cmd`. It retained the default Claude judge command; that judge was unavailable and was never reached because every executor failed first.

The executor used `codex exec --ignore-user-config --ephemeral --sandbox workspace-write --skip-git-repo-check --model gpt-6 --color never -`. This custom command preserved stdout/stderr and retained sandboxing instead of using the upstream Codex preset's sandbox bypass. No Ethereum skill was installed. The parent assistant is described by its session instructions as Codex based on GPT-6; `gpt-6` was the requested child model label, **not an observed successful model identity**. Even a successful child run would require checking whether its model and harness match this parent session before calling it an exact self-measurement.

## Observed facts, inference, and uncertainty

**Observed:** all 100 rows report the same initialization failure: `failed to initialize in-process app-server client: Read-only file system (os error 30)`. No model answers or goal artifacts were produced. The runner exited successfully after recording the errors; that process exit does not mean the benchmark succeeded. See [results](results.json), [probe](executor-probe.json), and [log](full-run.log).

**Inference:** the recorded outcomes measure an executor startup problem, not Ethereum knowledge or task-solving ability. A filesystem restriction blocked this CLI invocation before it could provide evidence of model performance.

**Uncertain:** the error does not identify the exact attempted write path. It does not establish whether `gpt-6` is a usable model identifier for this CLI/account, whether inference would otherwise succeed, or whether another allowed runtime configuration would fix initialization. A login-status check reported an existing ChatGPT login, but successful authentication for inference was not demonstrated. No credentials or configuration contents were copied into this report.

**Unanswered:** every pillar's actual performance score; all 33 judge verdicts; comparability between a child CLI model and the current assistant. Completion requires a functioning executor, a functioning blind judge, and rerunning all 100 items. No independent review or leaderboard submission occurred. This assignment's request to run and report did not authorize the protocol's separate public pull-request submission step.

## Local validation and reproducibility limits

Run `python3 artifacts/verify.py` from the repository root to check the saved evidence without network access or third-party dependencies. It verifies 100 unique items, 25 per pillar, zero graded items, the recorded failure pattern, report presence, and hashes of the evidence files. [Validation output](validation.txt) records the local result. These checks establish internal consistency and file integrity only; they do not independently certify benchmark behavior or research truth.

No dependencies were installed. Python/PyYAML already present in this environment were used for the original runner. The delivered verification script uses only the Python standard library. Repeating actual inference requires external model access and a repaired runtime; this artifact does not claim to provide offline model execution. Scratch files are not needed to inspect or validate the delivered evidence.
