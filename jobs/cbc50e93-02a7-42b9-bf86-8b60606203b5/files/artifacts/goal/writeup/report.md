<!-- Credit: Taylor (gtmcknight), amm-sim@4812a6382311624e1506aca131ca35c378f930d9 research/solved, solved-policy research. -->
# Shared AMM evaluation kit: goal write-up

Everything here builds on Taylor (gtmcknight)'s solved-policy research, [github.com/gtmcknight/amm-sim at `4812a6382311624e1506aca131ca35c378f930d9`, `research/solved`](https://github.com/gtmcknight/amm-sim/tree/4812a6382311624e1506aca131ca35c378f930d9/research/solved). All 95 tracked files of the trunk credit him in their header (JSON files in a first `_credit` key).

## 1. The deliverable

| | |
|---|---|
| Repository (trunk) | https://github.com/identity-md-launches/goal-3178-build-shared-evaluation-kit |
| Final trunk commit, **X** | `45e7563d1a29ffca9d608fdf60c90bf2624d2d01` (branch `main`, wave `e04-seal`) |
| Payload commit, **P** | `79f068cef81dadee171531f3381e207c193c959a` (wave `e03-recovery`) |
| Raw URL of any file | `https://raw.githubusercontent.com/identity-md-launches/goal-3178-build-shared-evaluation-kit/45e7563d1a29ffca9d608fdf60c90bf2624d2d01/<path>` |

The trunk at X holds every piece the goal names: `ammfast/`, `baselines/` (nine replica banks, the HA bank, the qt1 engine bank), `score.py`, `setup_fast.sh`, `gatep.py` and `README.md`. It has 95 tracked files and no submodule. The diff from P to X touches seven files only (`README.md`, `validate_kit.py`, `tests/test_validate_kit.py` and four files under `docs/`). The other 88 files, including all code and all banks, are byte-identical at P and X, so every measurement made at P applies to X.

The kit is complete and its gates pass. Three things fall short of the brief, and section 7 gives the detail:

1. **The README's URLs pin to P, not X.** It lists 88 files with sha256 and raw URLs at P and gives the seven changed files a `<trunk-commit>` placeholder. Substitute X; section 4 lists the URLs at X.
2. **Bank rows are not bit-stable across Linux x86_64 machines.** Five runtimes reproduced the banks exactly; one did not (7 of the 384 rows it rechecked differed beyond rounding, by up to 2.6e-2 in the three it reported). Section 6 says what to do about it.
3. **macOS arm64 was never executed.** Its four downloads were fetched and hash-checked only.

The results come from 16 items in four code waves, cited as `batch/item`. Figures marked "my check at X" are from this write-up's own run on a scratch clone at X (Linux x86_64). It is the orchestrator's check and carries no independent authority.

## 2. The pieces and their gate results

| Piece | What it is | Gate the goal set | Result |
|---|---|---|---|
| (a) `ammfast/` | Numba replica of Taylor's `replica2.run` with the qt1-ref, TwoComp and COMBO policies. `run(seed, policy, head_params=None)` is one compiled call per run; `run_batch(seeds, policy, head_params=None)` is the batch scorer; `head_params` is the 18-weight residual-head hook (COMBO only). | Per-seed edges equal CPython `replica2` within 1e-9 on 10000..10063 and 64000..64063 for all three policies; report runs/s/core. | **384/384 within 1e-9**, max error 1.19e-11, in four separate runs. **77.7 to 158.9 runs/s/core** depending on policy and machine (table below). |
| (b) `baselines/replica/` | Nine banks: three policies on 60000..61023, 64000..65023 and 10000..12047, edges to 6 decimals, produced by (a). | Spot-check 64 seeds of each bank against CPython. | **12288/12288 rows**. 576/576 spot pairs on the first 64 seeds of each bank, and 576/576 more on seeds 64..127 of each bank in an independent audit. All 12288 rows recomputed and equal in three later runs. |
| (b) `baselines/ha/` | HA edges for 10000..12047 from Taylor's `calib_out_2048.json`. | From Taylor's file. | **2048/2048 rows** equal `format(edge, ".6f")` of the `kind == "HA"` record with the same seed. |
| (b) `baselines/engine/` | qt1 on engine seeds 9700000..9700511: per-seed edge and afterSwap peak gas. Release wheel, `amm_sim_rs.run_batch` with worker argument 8, configs as `MatchRunner._build_configs`. | 512 seeds, screening only. | **512/512 rows**, no failed call. Reruns by three workers (5, 3 and 24 seeds) were all exact in unrounded edge and gas. |
| (c) `score.py` | Paired scoring against a bank in cumulative rounds of 128. Prints `{n, mean_diff, se, worst5}` each round. Stops when `mean_diff + 3*se < 0`, or with `--bar B` when `mean_diff - 3*se > B`. | Works for replica and engine runs; early stops. | 35 fixture tests pass. Live replica runs stopped `above_bar` and `worse` at n=128 and ran to `exhausted` at 1024. A live engine run stopped `worse` after one round of 128. |
| (d) `setup_fast.sh` | One command. 20 downloads pinned by sha256 and size in `bootstrap/manifest.tsv`, a reusable cache, no Rust, prints its own timing line. | Linux x86_64; macOS arm64 for replica work only. | Linux: **cold 13 to 20 s**, cached 0.6 to 9 s (table below). macOS: fetched and hash-checked, never run. |
| (e) `gatep.py` | Checks Taylor's files by sha256 on every call, runs his unmodified `gates.py`, caches the output by Taylor commit, Python version and input digest. | Run once per machine. | PASS fresh in 2.4 to 14.2 s; cache hit in 0.06 to 0.33 s with identical output. |
| `README.md` | What each piece does, commands, raw URL inventory. | Raw URLs at the final commit. | Present at X (38432 bytes). Its URLs are at P; see section 7. |

Supporting files in the trunk: `engine_eval.py` (engine adapter), `reference/` (35 credited envelopes of the upstream originals and an offline materializer), `validate_kit.py` (structural validator), `bootstrap/`, `docs/` and ten test files.

### Parity gate, 384 pairs (3 policies x 10000..10063 and 64000..64063)

| Run | Within 1e-9 | Max abs error |
|---|---:|---|
| Generator, `e03-recovery/replica-kit` | 384/384 | 1.19e-11; 343 pairs bit-identical |
| Independent audit, `e04-seal/audit-replica` (own CPython runs) | 384/384 | qt1-ref 9.66e-12, TwoComp 1.00e-11, COMBO 1.19e-11 |
| README worker, `e04-seal/readme` | 384/384 | 1.68e-11 |
| My check at X | 384/384 | qt1-ref 9.66e-12, TwoComp 1.00e-11, COMBO 1.19e-11; 343 bit-identical |

Zero residual head equals COMBO bit for bit (16/16 seeds in the audit; also a unit test). Nonzero heads were checked against a plain-Python head inside `replica2.run` within 1e-9 by the generator's tests.

### Runs per second per core (one worker, warm, through `run_batch`)

| Measured by | qt1-ref | TwoComp | COMBO | First call |
|---|---:|---:|---:|---|
| Generator (committed in `baselines/replica/validation.json`; median of 3 x 64 seeds) | 102.3 | 88.4 | 77.9 | 13.86 s (fresh interpreter, empty Numba cache) |
| `e04-seal/audit-replica` (3 x 128 seeds) | 158.9 | 150.9 | 135.3 | 10.75 s |
| My check at X (median of 3 x 128 seeds) | 105.2 | 87.3 | 77.7 | not isolated |

CPython `replica2` took 0.155, 0.207 and 0.243 s per run on the generator's machine, so ammfast is about 16 to 19 times faster there. A warm start with a populated Numba cache took 2.3 to 2.4 s.

### Setup time (`setup_fast.sh`, Linux x86_64)

| Measured by | Cold, engine + replica | Cold, replica only | Cached |
|---|---:|---:|---:|
| `e03-recovery/setup-repair` | 13.1 s | 9.5 s | 1.6 s (install reused) |
| `e04-seal/audit-engine` | 16.6 s (with smokes) | n/a | 8.8 s (downloads cached, fresh install); 8.9 s offline |
| `e04-seal/readme` | 20.0 s | n/a | 0.6 s (install reused) |
| My check at X | 15.2 s | n/a | 1.8 s (install reused); 7.9 s replica-only fresh install from cache |

A cold engine setup is 16 downloads and 135,768,787 bytes; replica only is 4 downloads and 114,819,511 bytes. The macOS arm64 replica set is 4 downloads and 80,347,821 bytes.

## 3. Exact commands for a later item

Run from the checkout root. All state goes under `scratch/`, which is git-ignored. I ran the shell commands in this section at X, and the longest took 147 s. Three differences from what is printed: my clone of `main` was already at X, so I did not need the `git checkout` line; I gave the replica-only install its own `--scratch "$PWD/scratch/replica-only"` (`e04-seal/audit-replica` ran the form printed here); and my engine candidate was the Vanilla strategy described below.

**Get the kit and set it up.** `main` was at X when this was written.

```sh
git clone https://github.com/identity-md-launches/goal-3178-build-shared-evaluation-kit.git kit
cd kit && git checkout 45e7563d1a29ffca9d608fdf60c90bf2624d2d01

# Engine and replica (Linux x86_64 only):
bash setup_fast.sh --platform linux-x86_64 --cache "$PWD/scratch/cache" --scratch "$PWD/scratch"
# Or replica only (the only mode for --platform macos-arm64):
bash setup_fast.sh --platform linux-x86_64 --replica-only --cache "$PWD/scratch/cache" --scratch "$PWD/scratch"

. scratch/env.sh     # in every new shell: pinned CPython 3.12.16, numpy 2.5.4, numba 0.68.1
```

Without `--cache` the cache is `$HOME/.cache/imd-amm`, as the goal asked. No run in this goal used that default, because items keep their state under `scratch/`. The last output line is the installer's timing, for example `setup_fast: OK platform=linux-x86_64 mode=engine setup=cold downloads=16 ... total_s=15.172 deadline_s=420`. Exit 75 means the deadline was reached: run the same command again and it resumes. Exit 3 means the selected platform's interpreter does not run on this machine.

**Check the checkout once per machine.**

```sh
python3 -B validate_kit.py        # stdlib only, under 1 s: exit 0, "status": "PASS", 14848/14848 rows
python3 -B reference/materialize.py --out scratch/reference     # "materialized 35 verified originals"
python3 -B gatep.py --reference scratch/reference/taylor --cache scratch/cache/gatep
                                  # "gatep: PASS (executed gates.py)", then "PASS (verified cache hit)"
python3 -B baselines/replica/validate.py --recompute 2048
                                  # re-runs all 12288 bank rows with ammfast; want "ok": true (147 s for me)
```

If the last command fails, the committed banks do not reproduce on that machine: read section 6 before scoring small effects.

**Run the replica.** From the checkout root, or with `PYTHONPATH` set to it.

```python
import ammfast
ammfast.run(10000, "COMBO")                          # {'seed': 10000, 'edge': 444.19533003406...}
ammfast.run_batch(range(64000, 64128), "TwoComp")    # rows in input order
ammfast.run_batch(seeds, "COMBO", head_params=[0.0] * 18)   # residual head; zeros == COMBO
ammfast.reference_run(10000, "COMBO")                # CPython replica2, the parity oracle (slow)
```

Policy ids are exactly `qt1-ref`, `TwoComp` and `COMBO`. Edges are unrounded floats. The head takes 18 finite weights (8 and a bias for the side that traded, 8 and a bias for the other side) and adds `8e-4 * tanh(z)` to each unclamped COMBO fee before the clamp; `docs/ammfast.md` defines the features. No trained weights are shipped.

**Score a replica candidate against a bank.**

```sh
python3 -B score.py --baseline baselines/replica/qt1-ref-64000-65023.json --replica --policy COMBO --bar 0.1
python3 -B score.py --baseline baselines/replica/TwoComp-64000-65023.json --replica --policy qt1-ref
python3 -B score.py --baseline baselines/replica/qt1-ref-60000-61023.json --rows baselines/replica/COMBO-60000-61023.json
```

The first stopped `above_bar` at n=128 (4.6 s); the second stopped `worse` at n=128; the third replays one bank against another without a simulator and ran all 1024 rows. Round lines go to stdout, one JSON object each:

```json
{"n": 128, "mean_diff": 0.6032781235549249, "se": 0.06127636328447672, "worst5": [{"seed": 64101, "diff": -2.7769827132076443}, {"seed": 64072, "diff": -0.6198054615002775}, {"seed": 64116, "diff": -0.597635677910489}, {"seed": 64053, "diff": -0.5087297450996289}, {"seed": 64094, "diff": -0.5067866716556182}]}
```

The baseline and candidate provenance and the final `{"status": {"reason": "above_bar" | "worse" | "exhausted", "n": ..., "available": ...}}` go to stderr. Exit 0 includes an early stop; exit 2 is invalid input or a backend failure. Other forms: `--head-params scratch/head.json` passes `{"weights": [18 numbers]}` to COMBO (covered by the trunk's tests, not run by me), and `--adapter module:function` plugs in another runner with the same signature (fixture tests only).

A candidate that is not one of the three policies is scored from a rows file. The file needs `backend`, `policy`, a nonempty `provenance` object and `rows` of `{"seed", "edge"}`, and its seeds must equal the baseline's exactly. To score a subset, cut the baseline to the same seeds. I ran this at X:

```python
import json, ammfast
CREDIT = "Taylor (gtmcknight), amm-sim@4812a6382311624e1506aca131ca35c378f930d9 research/solved"
bank = json.load(open("baselines/replica/qt1-ref-64000-65023.json"))
seeds = list(range(64000, 64256))
bank["rows"] = [r for r in bank["rows"] if r["seed"] in set(seeds)]
json.dump(bank, open("scratch/baseline-subset.json", "w"))
rows = ammfast.run_batch(seeds, "COMBO")             # replace with the candidate's own rows
json.dump({"_credit": CREDIT, "backend": "replica", "policy": "my-candidate",
           "provenance": {"origin": "how these rows were made"}, "rows": rows},
          open("scratch/candidate.json", "w"))
```

```sh
python3 -B score.py --baseline scratch/baseline-subset.json --rows scratch/candidate.json
```

**Score an engine candidate (screening only, seeds 9700000..9700511).** The candidate is a Solidity file whose contract is named `Strategy`. Benchmark one seed first with `engine_eval.run_batch([9700000], "path/Strategy.sol")`, which returns `[{"seed", "edge", "after_swap_peak_gas"}]`, then:

```sh
python3 -B score.py --baseline baselines/engine/qt1-9700000-9700511.json --engine --policy my-candidate --strategy-path path/Strategy.sol
python3 -B baselines/engine/validate.py --output scratch/engine-validation.json   # always pass --output
```

With the engine's own Vanilla strategy renamed to `Strategy`, the first command stopped `worse` after one round of 128 seeds in 35 s (mean_diff -181.358, se 3.894). `engine_eval` refuses any seed outside 9700000..9700511 before it runs anything. A qt1-sized strategy cost between about 2 and 9 s per seed on the machines that measured it, so a live round of 128 can run past 8 minutes. If the one-seed benchmark projects over the limit, collect rows in checkpointed chunks and score them with `--rows` as above (section 7, point 6).

**Tests.** `tests/` is not a package, so use discovery, one file at a time:

```sh
python3 -B -m unittest discover -s tests -p test_ammfast.py      # likewise test_score.py, test_gatep.py, ...
```

## 4. Raw URLs at X

Base: `https://raw.githubusercontent.com/identity-md-launches/goal-3178-build-shared-evaluation-kit/45e7563d1a29ffca9d608fdf60c90bf2624d2d01/`. I fetched every URL in this section and the next at X and each equals the clone byte for byte (27 files). The README's inventory covers the rest: its 53 file hashes and its envelope digest (`21a5688aa2a1d0d7940ea69d3f667f612f76f6b6c89f53539ca29ef1c95f078a` over 35 envelopes) equal the files at X.

| Path | sha256 at X | Raw |
|---|---|---|
| `README.md` | `b432f1aa8ac15cfba1f78227780c233427cc4564c758efbab258cc92871b5827` | [raw](https://raw.githubusercontent.com/identity-md-launches/goal-3178-build-shared-evaluation-kit/45e7563d1a29ffca9d608fdf60c90bf2624d2d01/README.md) |
| `setup_fast.sh` | `48e150d165ea3b385fb92e0e3a7aefbbe0d97c38c53efa737a587ed62c308d20` | [raw](https://raw.githubusercontent.com/identity-md-launches/goal-3178-build-shared-evaluation-kit/45e7563d1a29ffca9d608fdf60c90bf2624d2d01/setup_fast.sh) |
| `bootstrap/manifest.tsv` | `f9a0c49310aa6f501eac9a760e537af444d21f556239e3f00a9ed6f1d9628dad` | [raw](https://raw.githubusercontent.com/identity-md-launches/goal-3178-build-shared-evaluation-kit/45e7563d1a29ffca9d608fdf60c90bf2624d2d01/bootstrap/manifest.tsv) |
| `gatep.py` | `1d1d65bc18647530037cf3cff73fd8d4448f353d61b4494dd2ee7d556be122db` | [raw](https://raw.githubusercontent.com/identity-md-launches/goal-3178-build-shared-evaluation-kit/45e7563d1a29ffca9d608fdf60c90bf2624d2d01/gatep.py) |
| `reference/materialize.py` | `79e316706e8b4a84ee29e261c817476120d7a502f9017ec2f7f76f8f4444aaad` | [raw](https://raw.githubusercontent.com/identity-md-launches/goal-3178-build-shared-evaluation-kit/45e7563d1a29ffca9d608fdf60c90bf2624d2d01/reference/materialize.py) |
| `ammfast/__init__.py` | `5ce5b00b96ca7da11f37010d234803eca0e92adb2eebec18a35cb6d81c645b6c` | [raw](https://raw.githubusercontent.com/identity-md-launches/goal-3178-build-shared-evaluation-kit/45e7563d1a29ffca9d608fdf60c90bf2624d2d01/ammfast/__init__.py) |
| `ammfast/_kernel.py` | `45613331edb2fd46afa607612e1e6f0c22f0132c9974df6445ce18afe04cc2ae` | [raw](https://raw.githubusercontent.com/identity-md-launches/goal-3178-build-shared-evaluation-kit/45e7563d1a29ffca9d608fdf60c90bf2624d2d01/ammfast/_kernel.py) |
| `ammfast/_head.py` | `3ea24996bf90ce3dbb32fed745f9073c477b0ccd250befb5082a6ac8878ff86f` | [raw](https://raw.githubusercontent.com/identity-md-launches/goal-3178-build-shared-evaluation-kit/45e7563d1a29ffca9d608fdf60c90bf2624d2d01/ammfast/_head.py) |
| `ammfast/_reference.py` | `6509935958e7a317163b58b7da67add653a73028378fde65db9c40dddbfd3de0` | [raw](https://raw.githubusercontent.com/identity-md-launches/goal-3178-build-shared-evaluation-kit/45e7563d1a29ffca9d608fdf60c90bf2624d2d01/ammfast/_reference.py) |
| `score.py` | `7b9fa5e37695a5d1b048efe91a8b6c45d31bd4245a733261774c871fe9105a43` | [raw](https://raw.githubusercontent.com/identity-md-launches/goal-3178-build-shared-evaluation-kit/45e7563d1a29ffca9d608fdf60c90bf2624d2d01/score.py) |
| `engine_eval.py` | `0a3ed61457cb66c85a292c82acbb9657b5e5544a98c7aa04c7a6a5dccdc1d3b2` | [raw](https://raw.githubusercontent.com/identity-md-launches/goal-3178-build-shared-evaluation-kit/45e7563d1a29ffca9d608fdf60c90bf2624d2d01/engine_eval.py) |
| `validate_kit.py` | `d308d3d22228b04a266d955808bb1be017154dcf15c4caf2ecde59b031e09200` | [raw](https://raw.githubusercontent.com/identity-md-launches/goal-3178-build-shared-evaluation-kit/45e7563d1a29ffca9d608fdf60c90bf2624d2d01/validate_kit.py) |
| `baselines/replica/generate.py` | `375213daa8c2faa77dcd29c4c357d0cffd8d0bd1858b0da411cbf9a79eab5e04` | [raw](https://raw.githubusercontent.com/identity-md-launches/goal-3178-build-shared-evaluation-kit/45e7563d1a29ffca9d608fdf60c90bf2624d2d01/baselines/replica/generate.py) |
| `baselines/replica/validate.py` | `8812b083a47c52f2b4f68d58fbcd5d757434411db7ce96a340985ed9a41c4083` | [raw](https://raw.githubusercontent.com/identity-md-launches/goal-3178-build-shared-evaluation-kit/45e7563d1a29ffca9d608fdf60c90bf2624d2d01/baselines/replica/validate.py) |
| `baselines/replica/validation.json` | `84fe88b056f389d9620be650e646fd5ed2fa880d72f9764ad2a6505b03e6e8af` | [raw](https://raw.githubusercontent.com/identity-md-launches/goal-3178-build-shared-evaluation-kit/45e7563d1a29ffca9d608fdf60c90bf2624d2d01/baselines/replica/validation.json) |
| `baselines/engine/qt1-audit.json` | `5256d2bd776a44f34780e47551c2d7d02f9a2e9fc8b8392fc6b46a92593d2ade` | [raw](https://raw.githubusercontent.com/identity-md-launches/goal-3178-build-shared-evaluation-kit/45e7563d1a29ffca9d608fdf60c90bf2624d2d01/baselines/engine/qt1-audit.json) |

Of these, `README.md` and `validate_kit.py` exist in this form only at X. The other rows have the same bytes at P.

## 5. The banks

Each bank is one JSON object: `_credit`, `backend`, `policy`, `provenance`, then `rows` of `{"seed": int, "edge": "<6 decimals>"}` in ascending seed order. Engine rows add `after_swap_peak_gas`. The mean edge column is my arithmetic over the committed rows.

| Bank | Seeds | Rows | Mean edge | sha256 | Raw at X |
|---|---|---:|---:|---|---|
| `baselines/replica/qt1-ref-60000-61023.json` | 60000..61023 | 1024 | 529.971157 | `e98ecaa2c9a7ee36307971d28d6c3de845f5a10c034aea7d152288536e6fe72e` | [raw](https://raw.githubusercontent.com/identity-md-launches/goal-3178-build-shared-evaluation-kit/45e7563d1a29ffca9d608fdf60c90bf2624d2d01/baselines/replica/qt1-ref-60000-61023.json) |
| `baselines/replica/TwoComp-60000-61023.json` | 60000..61023 | 1024 | 530.416581 | `03723f9a1e827ff615d48b001c3181312618a9d31c52ff2109fdc4f0398dcb88` | [raw](https://raw.githubusercontent.com/identity-md-launches/goal-3178-build-shared-evaluation-kit/45e7563d1a29ffca9d608fdf60c90bf2624d2d01/baselines/replica/TwoComp-60000-61023.json) |
| `baselines/replica/COMBO-60000-61023.json` | 60000..61023 | 1024 | 530.609059 | `8256bba9edd0b5696c850f81447edd0ee24b1783c4f3b9d2390a90eaa0ef8cc1` | [raw](https://raw.githubusercontent.com/identity-md-launches/goal-3178-build-shared-evaluation-kit/45e7563d1a29ffca9d608fdf60c90bf2624d2d01/baselines/replica/COMBO-60000-61023.json) |
| `baselines/replica/qt1-ref-64000-65023.json` | 64000..65023 | 1024 | 535.720495 | `89675529770b1bc2e8ba584067d7ce776cd6ab88e79b58b3000852aa3d333f37` | [raw](https://raw.githubusercontent.com/identity-md-launches/goal-3178-build-shared-evaluation-kit/45e7563d1a29ffca9d608fdf60c90bf2624d2d01/baselines/replica/qt1-ref-64000-65023.json) |
| `baselines/replica/TwoComp-64000-65023.json` | 64000..65023 | 1024 | 536.128888 | `7c37b73ac7f16c4276f673c8ecfb326ab4421cab3ae9ab2f87db4f27e7d319f2` | [raw](https://raw.githubusercontent.com/identity-md-launches/goal-3178-build-shared-evaluation-kit/45e7563d1a29ffca9d608fdf60c90bf2624d2d01/baselines/replica/TwoComp-64000-65023.json) |
| `baselines/replica/COMBO-64000-65023.json` | 64000..65023 | 1024 | 536.330100 | `9d59118d213f1f7a811b91a27ab625a6c732789d53b215f6226e58acec8aad95` | [raw](https://raw.githubusercontent.com/identity-md-launches/goal-3178-build-shared-evaluation-kit/45e7563d1a29ffca9d608fdf60c90bf2624d2d01/baselines/replica/COMBO-64000-65023.json) |
| `baselines/replica/qt1-ref-10000-12047.json` | 10000..12047 | 2048 | 533.262831 | `6687dab88e27f2f6c37511d6328164eafd371fa640d85be353b74c47b98f511c` | [raw](https://raw.githubusercontent.com/identity-md-launches/goal-3178-build-shared-evaluation-kit/45e7563d1a29ffca9d608fdf60c90bf2624d2d01/baselines/replica/qt1-ref-10000-12047.json) |
| `baselines/replica/TwoComp-10000-12047.json` | 10000..12047 | 2048 | 533.687634 | `2fde9032094837e6c32728b0a160d25e78e382f31ebd67318ab8f5efad629b25` | [raw](https://raw.githubusercontent.com/identity-md-launches/goal-3178-build-shared-evaluation-kit/45e7563d1a29ffca9d608fdf60c90bf2624d2d01/baselines/replica/TwoComp-10000-12047.json) |
| `baselines/replica/COMBO-10000-12047.json` | 10000..12047 | 2048 | 533.860222 | `f707434285c5a067fee11cac983bfcb7b1301e47bf5a2c1f55e4984207d6739b` | [raw](https://raw.githubusercontent.com/identity-md-launches/goal-3178-build-shared-evaluation-kit/45e7563d1a29ffca9d608fdf60c90bf2624d2d01/baselines/replica/COMBO-10000-12047.json) |
| `baselines/ha/HA-10000-12047.json` | 10000..12047 | 2048 | 529.557434 | `09719da22be28598e9c1d0bb1eb935d7b0b4eeafef3321e0fabe4f3ec9e2b7a9` | [raw](https://raw.githubusercontent.com/identity-md-launches/goal-3178-build-shared-evaluation-kit/45e7563d1a29ffca9d608fdf60c90bf2624d2d01/baselines/ha/HA-10000-12047.json) |
| `baselines/engine/qt1-9700000-9700511.json` | 9700000..9700511 | 512 | 529.347613 | `f1031aae649d2ad8e871ee1cc055770a4c6b329ff3e71afb4500fca3c8621f90` | [raw](https://raw.githubusercontent.com/identity-md-launches/goal-3178-build-shared-evaluation-kit/45e7563d1a29ffca9d608fdf60c90bf2624d2d01/baselines/engine/qt1-9700000-9700511.json) |

Total: 11 banks and 14848 rows (replica 12288, HA 2048, engine 512). `validate_kit.py` at X reports all six of its parts passing and 14848 of 14848 rows verified.

Paired differences between banks (mean and standard error, my arithmetic over the committed rows; the 10000..12047 line matches the figures in the starter's `reference/combo/README.md`, per `e03-recovery/replica-kit`):

| Seeds | COMBO - qt1-ref | TwoComp - qt1-ref | COMBO - TwoComp |
|---|---:|---:|---:|
| 10000..12047 (n=2048) | +0.597391, se 0.013388 | +0.424803, se 0.012202 | +0.172588, se 0.010763 |
| 60000..61023 (n=1024) | +0.637902, se 0.019628 | +0.445424, se 0.017637 | +0.192478, se 0.014753 |
| 64000..65023 (n=1024) | +0.609605, se 0.019401 | +0.408392, se 0.017187 | +0.201212, se 0.015331 |

**Replica banks.** Generated by `python -B baselines/replica/generate.py --stage all --workers 4 --budget 420` in 2 min 52 s (`e03-recovery/replica-kit`). The generator is resumable: it exits 75 at its budget and continues on the next run, and its checkpoints are bound to a digest of the ammfast sources, the reference inventory and the runtime versions. `baselines/replica/validation.json` holds the 384 gate records and 576 spot records with both edges and the error for each pair.

**HA bank.** Taylor's `calib_out_2048.json` (2,948,144 bytes, sha256 `fdf24c7aa2b604d770336a5783276da8ed4d50bca9dbcc02e98b4da58f608d26`) holds 8192 records, four kinds with 2048 seeds each. The bank takes `kind == "HA"` and pairs by the record's own `seed`, never by position. It is an import of Taylor's numbers, not an ammfast run; the mean 529.557434 matches the 529.557 in his README (`e02-evaluation/ha-bank`).

**Engine bank.** qt1 is `reference/qt1/Strategy.sol`, sha256 `c68887cff61180e12ba2b1ceb333edf76a830f91f63b5d775a8806fb9ec08aca`; the bank's provenance records that digest and both validators check it. The runtime is the release wheel `amm_sim_rs` 0.1.0.post1 (sha256 `aedb68280aca34c110968f00148387c95885207913fb2cf19a1ab4c5cfd6887a`), engine source `benedictbrady/amm-challenge@6b6921f8d463314aa7c96234e1be25a25245f704`, solc 0.8.24 (optimizer 200, viaIR, paris). Each seed is its own `run_batch` call with worker argument 8, so `after_swap_peak_gas` is that seed's own peak for the submission's afterSwap; initialization and the baseline pool's gas are excluded. Configs draw size, arrival rate, then sigma, as `MatchRunner._build_configs` does; 48 fields were compared with upstream at indices 0..3 by construction only, without simulating those indices. Peak gas ranges from 179174 to 209279. `baselines/engine/qt1-audit.json` keeps the unrounded edges and all gas counters. Exact reruns: 5 by the generator's validator (9700000, 9700128, 9700256, 9700383, 9700511), 3 by `e03-recovery/score-integration`, 24 evenly spread seeds by `e04-seal/audit-engine`; the same five passed again in my check at X. **These seeds are for screening only.** Nothing here is a holdout or board result.

## 6. Reproducibility of the replica banks across machines

This is the one finding a later item must know before trusting a small difference.

The 1e-9 gate holds on every runtime that ran it: ammfast and CPython agree with each other. What varies is the pair of them against the committed bank. The pinned interpreter uses the machine's C math library. A last-place difference there moves most edges only in their last few digits (the README's worker printed 444.1953300340938 for COMBO seed 10000; my run printed 444.1953300340616). Now and then it flips a discrete event in a 10000-step run and moves that seed by 5e-4 to 5e-2.

| Runtime | Bank rows reproduced at 6 decimals |
|---|---|
| Generator (`e03-recovery/replica-kit`) | wrote the banks |
| `e04-seal/audit-replica` | 12288/12288 |
| `e04-seal/audit-engine` | live bank tests pass (14 of 14 in `test_replica_banks.py`) |
| My run in the last orchestration episode | 12288/12288 |
| My check at X for this write-up | 12288/12288 |
| `e04-seal/readme` | **377 of the 384 rows it recomputed.** 2, 3 and 2 rows beyond rounding in the first 128 seeds of COMBO-60000, COMBO-64000 and TwoComp-60000 |

The README worker's three examples, where fresh ammfast and fresh CPython agreed exactly with each other:

| Policy / seed | Bank | Fresh on that runtime | Difference |
|---|---:|---:|---:|
| COMBO / 60035 | 618.266729 | 618.2409840405087 | -0.025745 |
| COMBO / 64013 | 427.035477 | 427.0324335194603 | -0.003043 |
| TwoComp / 60016 | 409.736570 | 409.73952654643557 | +0.002957 |

On my runtimes those three seeds give the bank's values. In the last episode I showed one mechanism that produces the effect: the same checkout with `GLIBC_TUNABLES=glibc.cpu.hwcaps=-FMA` changes 9 of 12288 rows at six decimals (COMBO 10697, 10996, 11354, 60344; TwoComp 11590, 60233, 64646; qt1-ref 60475, 60587; the largest is COMBO 11354, 628.304150 against 628.358508), and on those nine seeds ammfast still equals CPython within 6.1e-12. That shows a mechanism. It does not establish the cause on the README worker's machine, which is unknown.

What it means in practice:

- Run `python3 -B baselines/replica/validate.py --recompute 2048` once per machine. If it prints `"ok": true`, the banks are exact there.
- If it fails, the banks still screen large effects. On the README worker's runtime the two affected test means moved by 1.5e-4 and 1.8e-4, against standard errors of about 0.02 at 1024 seeds and 0.05 to 0.06 at 128. They do not screen a candidate within about 1e-3 of a baseline.
- For those, score against a bank made on the same machine. The kit has no flag for this (`baselines/replica/generate.py` writes only the tracked paths). This recipe keeps the bank's shape and replaces its rows; I ran it at X (14 s for 1024 TwoComp rows, 0 rows differing from the committed bank) and scored against the result with `score.py --baseline scratch/TwoComp-64000-65023.local.json --replica --policy COMBO --bar 0.05`, which stopped `above_bar` at n=256:

```python
import json, sys, ammfast          # run from the checkout root, or with PYTHONPATH set to it
src, dst = sys.argv[1], sys.argv[2]   # e.g. baselines/replica/TwoComp-64000-65023.json scratch/TwoComp-64000-65023.local.json
bank = json.load(open(src))
rows = ammfast.run_batch([r["seed"] for r in bank["rows"]], bank["policy"])
bank["rows"] = [{"seed": r["seed"], "edge": format(r["edge"], ".6f")} for r in rows]
json.dump(bank, open(dst, "w"))
```

A locally rebuilt bank keeps the committed bank's provenance text, so label it as local wherever it is reported.

## 7. What is missing or weaker than the brief

1. **README at X.** The goal asked for raw URLs at the final commit. The README pins 88 files to P with sha256 (equal at X) and gives the seven files changed in its own commit a `<trunk-commit>` placeholder, because a file cannot name its own commit and the goal's last episode could not inspect another wave. It also carries three statements that are stale or local to its worker: it says `validate_kit.py` fails at P and that PASS is "expected" (PASS at X is observed: `e04-seal/validator-fix`, and my check); it reports three failing bank tests with the cause unknown (section 6); and its live scorer example prints mean_diff 0.752858348279358 from that deviating runtime (0.753059478618062 on mine). The fix is one README-only item. Four of the goal's 20 items are unspent, but all five episodes are used.
2. **Cross-machine bank reproducibility**, section 6. No built-in command writes a machine-local bank.
3. **macOS arm64 was never executed.** The four macOS downloads were fetched and hash-checked, and one test (`MacIntegration`) is skipped everywhere. No parity, timing or setup claim is made for macOS.
4. **The default cache `$HOME/.cache/imd-amm` was never written** by any run. It is the installer's default by its source and help text; every run passed `--cache` under `scratch/`.
5. **CPython coverage of the banks is the first 128 seeds of each bank** (first 64 by the generator, the next 64 by the audit). The remaining rows were compared ammfast against ammfast across runtimes, which is strong evidence of determinism but not a CPython check.
6. **`score.py` has no checkpoint for live rounds.** A round of 128 engine seeds for a strategy as heavy as qt1, run one seed after another, took or would take roughly 4 to 19 minutes depending on the machine (6.4 s per seed in `e02-evaluation/engine-bank`; about 9 s under load in `e04-seal/audit-engine`; five reruns inside a 10 s validator run for `e04-seal/readme` and inside a 26 s one for me). On the slower machines that is over the goal's 8-minute rule. The route is to collect rows in chunks and score them with `--rows` against a baseline cut to the same seeds. I ran that route at X with replica rows only; `engine_eval.py`'s command line has `--strategy`, `--checkpoint`, `--output`, `--max-seeds` and `--budget`, but no result shows it run with a candidate strategy.
7. **The stopping rules are screening heuristics**, not sequentially calibrated tests. A policy scored against its own 6-decimal bank shows up to 5e-7 of rounding per seed, which the "worse" rule could in principle trip; when I ran COMBO against its own 64000 bank it ran to `exhausted` (n=1024, mean -5.9e-9, se 9.0e-9).
8. **The residual head is an interface.** No trained weights are in the trunk. The archive's own `head.py` is not among the references, so the oracle for nonzero weights is the worker's plain-Python restatement of `combo.Combo.on_trade` in `ammfast/_reference.py`; with zero weights it equals the unmodified COMBO exactly.
9. **`validate_kit.py` is structural.** It recomputes hashes, coverage and the errors recorded in the committed evidence. It runs no simulator, so PASS is not independent proof of parity. The independent proof is the audit and the reruns above.
10. **`baselines/engine/validate.py` without `--output`** rewrites the tracked `baselines/engine/validation.json` (two timing fields). Always pass `--output scratch/engine-validation.json`.
11. **`docs/score.md` has no live replica example output.** `e04-seal/docs-refresh` corrected the three documents but could not run the examples: on its machine the Linux interpreter would not execute and setup exited 3, which is what the installer is built to do when the selected platform does not run. The document says so.
12. **One test reads the host architecture.** `test_replica_banks.CheckpointTests` checks the runtime binding that way; the README worker and I left those five tests out. `e04-seal/audit-engine` ran them and they passed.
13. **Disclosed by a worker:** `e03-recovery/replica-kit` ran the whole test directory once after finishing, which executed the old installer's host probe. Its report says no output of that run is in any delivered file, and the banks were written before it.
14. **Engine seeds are screening only.** Every engine simulation reported by any item, and by me, was inside 9700000..9700511.

## 8. Test and check totals

| Who | What ran | Result |
|---|---|---|
| `e04-seal/audit-engine`, at P | All ten test files | 228 tests: 227 pass, 1 skip (macOS), 0 fail |
| `e04-seal/audit-replica`, at P | `test_ammfast.py`, `test_replica_banks.py`; scorer runs | 23 and 14 pass |
| `e04-seal/validator-fix` | `test_validate_kit.py` after the repair | 58 pass; validator PASS 14848/14848 |
| `e04-seal/readme`, at P | Selected suites on its runtime | 223 run: 212 pass, **3 fail** (section 6), 8 skip |
| My check at X | `test_ammfast` 23, `test_engine_eval` 16, `test_gatep` 24, `test_ha` 15, `test_score` 35, `test_setup_deadline` 13, `test_validate_kit` 58, three classes of `test_replica_banks` 9 | 193 run, 193 pass. Not run: `test_setup_fast`, `test_score_integration`, `CheckpointTests` |

My check at X also covered: clone and `git diff P..X` (the seven files); the credit string in the head of all 95 files; `validate_kit.py` (exit 0, PASS, no findings); setup cold, cached and replica-only; materialize (35 originals); Gate P fresh (5.7 s) and cached (0.23 s); the 384-pair gate; all 12288 bank rows recomputed; two live replica scorer runs whose round lines equal the audit's to the last digit, and the bank-to-bank replay; one live engine round (128 Vanilla seeds 9700000..9700127, `worse`, mean -181.35840023233058, se 3.8938152969370132, the same figures the README prints); the engine validator with five exact qt1 reruns; the HA check (2048 rows); 27 raw URLs at X. `git status` was clean afterwards, so no documented command changed a tracked file.

Live scorer runs on record:

| Run | Stop | n | mean_diff | se | Source |
|---|---|---:|---:|---:|---|
| COMBO vs qt1-ref bank 64000, `--bar 0.1` | above_bar | 128 | 0.603278 | 0.061276 | `e04-seal/audit-replica`; same in my check |
| COMBO vs qt1-ref bank 64000, no bar | exhausted | 1024 | 0.609605 | 0.019401 | `e04-seal/audit-replica` |
| qt1-ref vs TwoComp bank 64000 | worse | 128 | -0.457939 | 0.051266 | `e04-seal/audit-replica`; same in my check |
| Vanilla vs qt1 engine bank, seeds 9700001..9700128 | worse | 128 | -181.0758 | 3.9163 | `e03-recovery/score-integration`, `e04-seal/audit-engine` |

In the engine run the test counted the adapter's calls: one request for 128 seeds and none for the remaining 383.

## 9. How the goal ran

| Wave | Trunk commit | Items | What landed |
|---|---|---:|---|
| `e01-foundation` | `4a02cd145745a9d1c45d2ca8d669b650dce619f8` | 2 | `reference/` (35 envelopes, materializer), `gatep.py`, first `setup_fast.sh` with pinned manifest, contracts |
| `e02-evaluation` | `57ce0df30e24784fb9d0537de55e5b7f8521ecd7` | 5 | `engine_eval.py` and the 512-row engine bank; HA bank; `score.py`; a read-only audit of the foundation. The `ammfast` item delivered nothing: its machine could not start processes |
| `e03-recovery` | `79f068cef81dadee171531f3381e207c193c959a` (P) | 4 | `ammfast/`, the nine replica banks and their evidence; installer repair (deadline on every path, replica env cleanup, host probe removed, pins unchanged); live engine scorer test; `validate_kit.py` |
| `e04-seal` | `45e7563d1a29ffca9d608fdf60c90bf2624d2d01` (X) | 5 | Validator key repair, README, three docs; two read-only audits of P (replica; setup, gate and engine) |

The goal's rules, as the results report them: the longest single command was 359 s (an engine bank chunk), under the 8-minute limit; long work checkpointed and resumed (engine bank in five chunks, replica generator and installer exit 75 and resume); all state stayed under `scratch/`; items that ran a workload benchmarked it first; no engine seed outside 9700000..9700511 was simulated. 16 of 20 items and 5 of 5 episodes were used.

Results this write-up rests on: `e01-foundation/reference-gate`, `e01-foundation/bootstrap`, `e02-evaluation/ammfast`, `e02-evaluation/engine-bank`, `e02-evaluation/score`, `e02-evaluation/ha-bank`, `e02-evaluation/foundation-audit`, `e03-recovery/replica-kit`, `e03-recovery/setup-repair`, `e03-recovery/score-integration`, `e03-recovery/kit-validator`, `e04-seal/validator-fix`, `e04-seal/readme`, `e04-seal/docs-refresh`, `e04-seal/audit-replica`, `e04-seal/audit-engine`.

Upstream sources: Taylor's `research/solved` at the pin above (including `gates.py`, `replica2.py`, `qm_k1e-5.json`, `calib_out_2048.json`); the starter tools and reference policies at `identity-md-launches/goal-3170-beat-network-s-amm-entry@4eb3e985fd31e3cd17832501b95b6d2491aca73d`; and the numba replica from item numba-rng, https://api.imd.fun/artifacts/b9c917ebb99152aafd12993b327f0a82529efe414a4a8fea8f4a0e3493cc1f8f (its `fastsim.py`, sha256 `4d3d2187b5dcbcd979a0775e431d30421b0e376d3c582afc60fbb4d6a052596b`, is the kernel `ammfast/_kernel.py` is derived from). `reference/sources.json` in the trunk records every original's URL and digest.
