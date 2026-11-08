# Pinned amm-challenge simulator wheels (commit 6b6921f8): write-up

**Goal:** build `benedictbrady/amm-challenge` at commit `6b6921f8d463314aa7c96234e1be25a25245f704` as Linux x86_64 Python wheels. Wheel A is the unchanged engine. Wheel B is the engine plus the gas-counter patch, as version `0.1.0.post1`. With these wheels, later AMM goals can `pip install` the engine and skip compiling Rust.

**Sources:** the four item results `item-w1`..`item-w4` under `.imd/reads/artifacts/`, which are `artifacts/goal/items/w{1..4}/result.json`. Their SHA-256 values are given in the brief. Every figure below is copied from those results unless another source is named.

## Result: the first item to pass is **w1**

All four seats (w1, w2, w3, w4) report `"blocked": null`, and every one reports both wheels passing both gates. Taken in item order, w1 is the first, so w1 is the named item.

### w1 wheels

| Wheel | File name | sha256 | bytes | Artifact URL |
|---|---|---|---|---|
| A (engine unchanged) | `amm_sim_rs-0.1.0-cp310-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.whl` | `ad0b5723ead0f6e29e376bea5dcbe971c4ef4d7d2f8dd612b064902f3ad224e7` | 719690 | https://api.imd.fun/artifacts/ad0b5723ead0f6e29e376bea5dcbe971c4ef4d7d2f8dd612b064902f3ad224e7 |
| B (instrumented, 0.1.0.post1) | `amm_sim_rs-0.1.0.post1-cp310-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.whl` | `93ade3a3b8070298d1dcc9a87d1de5971f58119c4856e4ee6921d269b9ad14d1` | 727926 | https://api.imd.fun/artifacts/93ade3a3b8070298d1dcc9a87d1de5971f58119c4856e4ee6921d269b9ad14d1 |

**Availability:** on 2026-11-08, while writing this, both artifact URLs answered **HTTP 404**. w1 says so itself: "The api.imd.fun URL only works once the plane has uploaded wheel B under that sha256." The URLs are therefore the addresses where the wheels are expected after upload. They are not yet confirmed to serve the files. A later brief should not rely on them until they resolve. The `sha256sum -c` line in the setup block catches a wrong or missing file.

### w1 gate numbers (exactly as w1 reports them)

- **CH mean edge, seeds 0..999, wheel A:** `525.5258821780834`
- **CH mean edge, seeds 0..999, wheel B:** `525.5258821780834`
  - w1 also gives the Decimal mean of the edges as `525.52588217808343827`.
  - Method, per w1: one `run_batch(CH, Vanilla, MatchRunner._build_configs() for n=1000, 8 workers)`, mean computed as the float sum / 1000.
- **V2 afterSwap, wheel B:** calls `21580`, oog `3`, max_ok_gas `243554`, init_max `236377`
  - w1's notes add `ok 21577` and `afterInitialize calls 2`.
  - The harness was run as `harness.py V2.sol 10043 10045 --other V2.sol`, and both runs gave identical numbers.
  - The harness exits with code 2 because the OOGs mark the run invalid. w1 says this is expected.

**Inputs w1 says it verified:** CH.sol sha256 `6dd68f77a70900319460215374143dbd5d924198450a46d9f5f91f6b1e3d35c3`. V2.sol, after the two replacements, each found exactly once: sha256 `28417e116f57f1029fdd1803832e852574902c1ae7253c05657f317db76da4ab`. Both match the brief.

**Toolchain w1 reports:** rustc 1.99.1 (58cf8f9c3 2026-10-13), maturin 1.16.0, zig 0.17.1, Python 3.12.3. Seconds: toolchain 19, build_a 29, build_b 11, gate 87.

**Check against the V2 audit artifact:** the audit artifact `02c134d9ed51858f06d02b6dec25e6922016490f11e3a8174af512a6a77b6569` (https://api.imd.fun/artifacts/02c134d9ed51858f06d02b6dec25e6922016490f11e3a8174af512a6a77b6569) breaks the V2 result down by seed, in its `gas.oog_by_seed` field:
- seed 10043: oog 2, afterSwap_calls 10570, max_ok_gas 243554
- seed 10044: oog 1, afterSwap_calls 11010

It also gives `max_ok_afterInitialize` 236377. Adding the two seeds gives 10570 + 11010 = 21580 calls and 3 OOG, which matches the gate on seeds 10043 and 10044. So the harness's `10043 10045` range does not include its end. The audit's total of `oog: 4` covers seeds 10000..10127, which includes a further OOG at seed 10057, so it is not the gate figure.

**Reference release:** the reference release page at https://github.com/gtmcknight/amm-sim/releases/tag/sim-6b6921f8 lists wheel names identical to w1's. Its sha256 values are different (A `11fcc274…`, B `6c6a439e…`). When read on 2026-11-08, that page did not show the CH or V2 gate numbers; it points to the audit artifact for them. All four seats built different bytes (see below), so these builds are not byte-reproducible. The different hashes are consistent with each seat building its wheels itself rather than downloading the reference wheels, which the goal requires.

## Setup block for later briefs (from w1's `install_block`)

w1's `install_block` already contains wheel B's artifact URL. It is reproduced as given, with no changes:

```sh
# from the amm-challenge checkout at 6b6921f8d463314aa7c96234e1be25a25245f704, uv on PATH
uv venv --python 3.12 .venv && . .venv/bin/activate
curl -sSLf https://api.imd.fun/artifacts/93ade3a3b8070298d1dcc9a87d1de5971f58119c4856e4ee6921d269b9ad14d1 -o amm_sim_rs-0.1.0.post1-cp310-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.whl
echo '93ade3a3b8070298d1dcc9a87d1de5971f58119c4856e4ee6921d269b9ad14d1  amm_sim_rs-0.1.0.post1-cp310-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum -c -
uv pip install ./amm_sim_rs-0.1.0.post1-cp310-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.whl numpy py-solc-x==2.1.0 pyrevm==0.3.7
uv pip install --no-deps -e .
```

**Notes on the block:**
- It installs wheel B. w1 reports B's CH result as identical to A's, and B also exposes `gas_stats`.
- A brief that wants the unpatched engine should replace the wheel name and hash with wheel A's from the table above.
- w1 tested the block with the local wheel file in a fresh venv. It has not been tested against the live URL, which returned 404 when checked (see above).

## Other items

- **w2: passed.**
  - Wheel A: `21f22b4c876c909061c6eab642ce4ef7adb746f5ed5c8fd358c0510f004ac572` (719673 bytes). Wheel B: `517aeeda6b3527fcdfafda50d50862b0701b23024b660d29aa66cc562cba361a` (727932 bytes).
  - CH A `525.5258821780834`, CH B `525.5258821780834`.
  - V2 on B: calls 21580, oog 3, max_ok_gas 243554, init_max 236377.
- **w3: passed.**
  - Wheel A: `b261b075a6af5d26c0ad79af59bb0dc7af63c7843153b5d7461e76ef1ee89f7a` (719678 bytes). Wheel B: `0b0453dd0abc16604b2f4ae904fcc04c55322eca05cfb48a5e8dbac3a2d35a8b` (727916 bytes).
  - CH A `525.5258821780834`, CH B `525.5258821780834`.
  - V2 on B: calls 21580, oog 3, max_ok_gas 243554, init_max 236377.
  - w3 describes the harness seeds as "10043..10044". This agrees with the end-exclusive range shown above.
  - w3's `install_block` assumes the checkout is at `.cache/amm-challenge`.
- **w4: passed.**
  - Wheel A: `b9e0f32e97bec8b8a6ee996c93bafbabd902d4d593d1db900f64fe63343ef1e0` (719711 bytes). Wheel B: `213b677a7735766eb490e1da6416bc0945ea5e6765ef306430dd19af7ee03e2d` (727933 bytes).
  - CH A `525.5258821780834`, CH B `525.5258821780834`.
  - V2 on B: calls 21580, oog 3, max_ok_gas 243554, init_max 236377.

No item was blocked, and no item missed a gate. All four report the same toolchain versions (rustc 1.99.1, maturin 1.16.0, zig 0.17.1, Python 3.12.3). They report the same gate numbers to every digit, but each produced different wheel bytes.

## Caveats

**Sources that did not hold when re-read.** The brief says some sources failed when their machines read them again: 1 source for w1, 1 for w2, 2 for w3. The item results do not include a sources list, so this write-up cannot tell which URL failed in each case. The cited inputs are the CH file, the V2 artifact, the audit artifact and the reference release. Two of these were re-read here:
- **Audit artifact:** it resolved, and its V2 gas numbers agree with the gate.
- **Reference release page:** it resolved, but it does not state the gate numbers. A claim citing it for those numbers would not hold.

In every item, the gate figures are the item's own measurements on its own wheels, not quotes from a source. The CH and V2 file hashes match the brief. So the failed sources do not change which item passed or the numbers above. They do weaken anything an item claims *only* on the strength of an outside page. w3 has the most flagged sources (2). Its figures agree exactly with w1, w2 and w4.

**Wheel URLs.** No artifact URL for any item was confirmed to serve its wheel at the time of writing; w1's two URLs were checked and returned 404. Upload is the plane's job, and none of the items did it.

**What was not checked independently.** This write-up did not rebuild or re-run any wheel. All gate numbers are as the items report them.
