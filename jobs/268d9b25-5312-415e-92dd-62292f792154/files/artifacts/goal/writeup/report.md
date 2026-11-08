# amm_sim_rs wheel reproducibility — pinned-build results

**Bottom line: the wheels are still not reproducible.** Across all 6 machine-results (items r1–r6, each building wheel A unchanged and wheel B with `scratch/instrumentation.patch` + `version = "0.1.0.post1"`, each in two checkout paths `p1` and `pathtwo/x`), **no two of the 12 wheel-A builds share a sha256, and no two of the 12 wheel-B builds share a sha256.** That is an improvement in degree but not in kind over goal 00b9cdc8 (B was 727916–727933 bytes there; here B is 727735–727756 bytes, a tighter spread from pinning `SOURCE_DATE_EPOCH`, committing one `Cargo.lock`, and `--remap-path-prefix`), but byte-identical reproduction across machines/paths still fails.

The good news: every result that reports it shows the **compiled extension itself (`amm_sim_rs.abi3.so`) is byte-identical**, both between the two checkout paths on one machine and (where comparable) across machines. The one remaining, fully identified cause of wheel-sha256 mismatch in every single result is **maturin 1.16.0's CycloneDX SBOM** (`dist-info/sboms/amm_sim_rs.cyclonedx.json`), which embeds the absolute checkout path in 3 `bom-ref`/`ref` fields (`path+file://<checkout>/amm_sim_rs#0.1.0`); `--remap-path-prefix` does not reach it, so it differs whenever the checkout's absolute path differs — which it does both between `p1`/`pathtwo/x` on one machine and between any two machines' own absolute workspace paths. `RECORD` then differs too (it records the SBOM's own hash/size). `__init__.py`, `METADATA`, `WHEEL`, and the `.so` are identical in every reported diff; all zip timestamps equal `SOURCE_DATE_EPOCH` (2026-02-07 23:12:24) everywhere.

## Per-result table

All 6 results built commit `6b6921f8d463314aa7c96234e1be25a25245f704` with `SOURCE_DATE_EPOCH=1770505944`, rustc/cargo 1.99.1, maturin 1.16.0, zig 0.17.1, the brief's exact `maturin build` flags and `--remap-path-prefix` for checkout/`CARGO_HOME`/`RUSTUP_HOME`.

| Result | Cargo.lock sha256 (75461 bytes) | Path | Wheel A sha256 (bytes) | Wheel B sha256 (bytes) | Paths agree (A / B) |
|---|---|---|---|---|---|
| r1 | `b5efc7f1aaf2c92fafa2015404ff74f760b80135a9e16bacded7f4ba0c81690b` | p1 | `7b1f581a4fcd70466fed7d1431889b35157cefa48a0f5eff830b2b2480cca422` (719300) | `59289af6ea958890ccbaf957257c2819c997237f968f46e43614f9f6b3c3763b` (727737) | no / no |
| r1 | same | pathtwo/x | `23e17a55c335d9244d7dd0edad2ac9a50bcd8b3310314b77dcc81ef913cc9b0f` (719313) | `8eb1b0aef5fb561c602cd0b7c9c1ae9264d81a27def22f3e43c8ffc9f24ea03c` (727750) | — |
| r2 | `b5efc7f1aaf2c92fafa2015404ff74f760b80135a9e16bacded7f4ba0c81690b` | p1 | `a3e13ef7c801643b1754360b4f5a8cdbb6b5e6556a2cfbbe2219f6293fd9f638` (719299) | `8ac9252d4ce4834376246a7f92fdfac44b6b7f5de5cce411c449d685b44e4287` (727735) | no / no |
| r2 | same | pathtwo/x | `36dbe93f224dc46cd63d65c5c1595b659dbe4acab5263717ee883358eaf0bc4c` (719310) | `46c08d19f403d575b6896f00389c657ec2de051626e6623518b9982710b698cf` (727748) | — |
| r3 | `b5efc7f1aaf2c92fafa2015404ff74f760b80135a9e16bacded7f4ba0c81690b` | p1 | `5d38353cc0b23ec39cd9ebe2708f92565f50a9dd50474415194c0f6f56713c13` (719300) | `265cedf8df89f5f2e932ac8757a94c1c2c610b77a258d73546573915412582b4` (727738) | no / no |
| r3 | same | pathtwo/x | `ec8009f877f0aaa1b729fd0060e104d645590a38bf90c70147035bce4dfc4c81` (719312) | `99b761b9d0a108ca86ee1ce88a022f8a4a4b158a3619a6cc44f0f534e33a6ca0` (727750) | — |
| r4 | `b5efc7f1aaf2c92fafa2015404ff74f760b80135a9e16bacded7f4ba0c81690b` | p1 | `5f4785c01cdd3dff39dc2118582db2015510e30f9cd8ff794f4ab6e4ddb55f4b` (719308) | `f5ee255c342e09867c58e4fa83b586504b8b84491c975cd7fb20265e255e0664` (727746) | no / no |
| r4 | same | pathtwo/x | `b0a834d247774c5d69edcb44b8b6f0b01327d9d37363032c72042f8a82a3ff28` (719319) | `89e93247297e5670a59c86390e8ca9dd270ec684b22953ccfcf62b7590df009e` (727756) | — |
| r5 | `a180854ccb8f32e0104bafea81d25b08a916116c80b9d44a2e3d17dfeed3cc65` (**different from the other 5**) | p1 | `f4e5f7fd9aefa31cb7ab4154ea4cc5f16c6d4d24d25936243bb5e7184b829e78` (719300) | `83690eefd7c309b511e0aabc113d7f93b0e0305df3693ea94b97470b4002f11d` (727737) | no / no |
| r5 | same | pathtwo/x | `d97b521af58394b60f703d903f592ae6e98ee8515ecf55e2a2053d04a7f2c24f` (719312) | `cea05bdf37272ec0d9676fdaec3be43b5dbadecbaa75a7a31c26d985aa735c5b` (727750) | — |
| r6 | `b5efc7f1aaf2c92fafa2015404ff74f760b80135a9e16bacded7f4ba0c81690b` | p1 | `bb4dbf098bb6f9148a736a9c9a22d75047ecf7448e5f0f3a4a7bcd848d067c64` (719297) | `2c09fe3ad6293a6c466c8ea3113bcc002672ba07a667383b8dd09217e744d61c` (727736) | no / no |
| r6 | same | pathtwo/x | `b62f633a8a5e59e12f1a867a03cfdbb9a423730bc5a6a166a09f84b9212e109f` (719311) | `03e8e082772d3285e5fa7e6493f86c9c50ebde2a18da2efd573a98b3cec57906` (727747) | — |

"Paths agree" is "no" for every result: within a machine, `p1`'s wheel sha256 never equals `pathtwo/x`'s wheel sha256, for either A or B. Across all 24 wheel-A/B sha256 values in the table, every single one is distinct — no two results, and no two paths, produced the same wheel.

## What two or more machines DID produce identically

- **Cargo.lock**: r1, r2, r3, r4 and r6 all generated the exact same `Cargo.lock` sha256 `b5efc7f1aaf2c92fafa2015404ff74f760b80135a9e16bacded7f4ba0c81690b` (75461 bytes) via `cargo generate-lockfile --manifest-path amm_sim_rs/Cargo.toml` on cargo 1.99.1 — 5 of 6 results agree exactly on lockfile content. r1's notes say "311 packages" while r3/r4 give the field `"packages": 312`; since the sha256 is identical across all five, this is a labeling inconsistency in the notes, not a content difference. **r5 alone generated a different Cargo.lock**, sha256 `a180854ccb8f32e0104bafea81d25b08a916116c80b9d44a2e3d17dfeed3cc65`, same byte count (75461) but different content — i.e. `cargo generate-lockfile` is itself not deterministic run-to-run (crates.io index state can differ), which is exactly why the brief requires committing one shared Cargo.lock rather than regenerating it per machine.
- **The compiled `.so`** (`amm_sim_rs/amm_sim_rs.abi3.so`, the actual Rust extension): r1, r3, r4 and r5 each give an explicit `so_sha256`, and all four report the *same* pair of hashes for every one of their builds (both checkout paths, both wheel A and wheel B):
  - A: `414ea6d201d299b2967b2aee72c9704758fa69acf6df6cd295d83598118efd37`
  - B: `ff88b6353c2aad7342f0a26194f7347e78b9c3b38d683a7449006d423978cd14`
  Notably r5 reached this *same* `.so` despite having a *different* Cargo.lock than r1/r3/r4 — so the lockfile difference there did not change the compiled bytes. r2 and r6 also report (in prose notes, without publishing the hash) that their own two paths' `.so` files are byte-identical to each other; their matching the 414ea6d2…/ff88b635… above could not be confirmed from what they reported, so that is left unconfirmed rather than assumed.
- **The gate**: every one of the 6 results passes both checks identically: `CH.sol` (sha256 `6dd68f77a70900319460215374143dbd5d924198450a46d9f5f91f6b1e3d35c3`) vs `VanillaStrategy` over seeds 0..999 gives mean `525.5258821780834` for both A and B, matching the expected value in every result (r3 gives the fuller decimal `525.52588217808343827` for both). `V2.sol` (sha256 `28417e116f57f1029fdd1803832e852574902c1ae7253c05657f317db76da4ab`) run twice with wheel B gives, in every result: `afterSwap` calls 21580, ok 21577, oog 3, max_ok_gas 243554; `afterInitialize` max_ok_gas 236377; harness exit code 2 / `valid=false`, expected because of the 3 OOG. No result's gate failed.
- **None of the 12 wheels equals Taylor's reference** sha256 (A `11fcc2748d430bc73c5acb107ca1fab9a6719b86bc2b0960c9cbcc374b6eba4e`, B `6c6a439e3aff01fe014123559ec5c1b6414b515a74cbe0402a31ded19716bfce`) — every result's `equals_reference` is `{"a": false, "b": false}`. This is expected since the local SBOM embeds this run's own checkout path, which cannot match Taylor's path; whether the reference wheel's `.so` matches ours could not be checked because no wheel was downloaded (forbidden by the brief).

Since no single sha256 for wheel A or wheel B was produced by two or more results, there is no shared Cargo.lock text, byte count, or build command to hand to a later builder as "the" reproducing recipe — only the command that every result already ran (below), which is necessary but not sufficient for a byte-identical wheel.

## Root cause and differences, in every result

Every one of the 6 results independently traces the within-machine (`p1` vs `pathtwo/x`) wheel difference to the same single file, and the pattern is identical for A and for B:
- `amm_sim_rs/amm_sim_rs.abi3.so`, `amm_sim_rs/__init__.py`, `*.dist-info/METADATA`, `*.dist-info/WHEEL` — byte-identical between paths.
- `*.dist-info/sboms/amm_sim_rs.cyclonedx.json` — differs. maturin writes the root component's `bom-ref` and the corresponding `ref` as `"path+file://<absolute checkout>/amm_sim_rs#0.1.0"` (and once more for `bin-target-0`), i.e. 3 lines carry the absolute checkout path verbatim. `--remap-path-prefix` only affects strings embedded by rustc/cargo in compiled artifacts, not maturin's own SBOM generation step, so it has no effect here.
- `*.dist-info/RECORD` — differs only in the one line recording that SBOM file's own hash and byte size (consequence of the point above).
- Zip entry timestamps — identical everywhere (all `2026-02-07 23:12:24`, i.e. `SOURCE_DATE_EPOCH`), in every result that checked.

Because the SBOM's embedded path length varies with the checkout path string, the wheel's byte count also varies slightly by checkout (e.g. r1: 719300 vs 719313 for A, a 13-byte spread matching `.cache/pathtwo/x` vs `.cache/p1` being longer; each result shows a similar, small, checkout-path-dependent spread). The same mechanism operates across machines too: each result's own absolute workspace path (redacted to `<workspace>` in all 6 files) differs from every other machine's, so even where the compiled `.so` matches exactly (r1/r3/r4/r5), the SBOM — and hence the wheel sha256 — still differs machine to machine.

**Next fix to try** (stated by every result, none of which attempted it, per the brief's "report only" instruction): make the SBOM path-independent, e.g. by disabling maturin's SBOM generation for this build (if maturin 1.16.0 exposes such a flag), or by normalizing/stripping the `path+file://` checkout-path component before hashing, or by always building from a fixed, identical checkout path (e.g. a symlink or bind-mount to a canonical directory) on every machine so the embedded path string is constant. Only after that would wheel-level byte-identity across paths/machines become possible to test; the `.so`-level reproducibility already holds in 4 of 6 results, suggesting the Rust build pipeline itself is not the blocker.

## Build command used by every result

```bash
export SOURCE_DATE_EPOCH="$(git -C amm-challenge log -1 --format=%ct)"   # 1770505944 for this commit
export CARGO_INCREMENTAL=0
export RUSTFLAGS="--remap-path-prefix=<checkout>=/src --remap-path-prefix=<CARGO_HOME>=/cargo --remap-path-prefix=<RUSTUP_HOME>=/rustup"
cargo generate-lockfile --manifest-path amm_sim_rs/Cargo.toml   # commit a shared Cargo.lock; see mismatch note above
maturin build --release --strip --locked --zig \
  --target x86_64-unknown-linux-gnu --compatibility manylinux2014 \
  --features pyo3/abi3-py310 \
  --manifest-path amm_sim_rs/Cargo.toml --out <dir>
```

This reproduces the gate (`CH` mean `525.5258821780834`, `V2` afterSwap calls 21580/oog 3/max_ok_gas 243554) and, in 4 of 6 results, the identical `.so` (`414ea6d2…` / `ff88b635…`). It does **not** reproduce a fixed wheel sha256, because the CycloneDX SBOM step above is not path-independent.

## Source-reliability caveats

Per the goal's instructions, two results cite sources that did not hold up when their own machines re-checked them: **r2 cites 1 such source and r4 cites 2**. Both r2 and r4 attribute `scratch/instrumentation.patch` and the `V2.sol` code to artifact `02c134d9ed51858f06d02b6dec25e6922016490f11e3a8174af512a6a77b6569`'s `source_files` and to artifact `1f4f14f0…`'s `code` field respectively, inside their own prose notes (no other results were flagged this way). Since it is not stated which specific citation in each failed on re-check, the provenance claims about where the patch/V2 code came from in r2 and r4 specifically should be weighed as less certain than the same provenance claims repeated in r1, r3, r5 and r6 — the measured sha256 values of the patch (`11f79c95f30eb7d829be6c34d57caf28f5b3de39dce8f81bb62a8029231e0e1e` in those notes that give it) and of `V2.sol` (`28417e116f57f1029fdd1803832e852574902c1ae7253c05657f317db76da4ab`, verified by the gate in every result) are unaffected by this caveat, since they are independently checkable against the gate's own hash fields.

## Scope notes

No wheel was downloaded from any host, consistent with the brief. Nothing was submitted or uploaded anywhere by any of the 6 build runs. One result (the one noting a WSL2 host with no system `cc`/`gcc`) needed a local `cc` shim pointing at `maturin`/`cargo-zigbuild`'s own zig wrapper to link host build scripts and proc-macros; this did not change that machine's shipped `.so`, which still matches the other three machines that reported an `.so` hash.
