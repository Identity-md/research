# Collateralized controls and cross-chain comparators

Stablecoin v4 campaign · R5 · Job `b7645d94-4f1e-4e20-baef-8782bf432ae9`

- [Read the research report](r5-report.md)
- [Download the dataset](r5-data.json)
- [Provenance and original artifact hashes](manifest.json)
- [Coordinator checks and known gaps](coordinator-review.json)

DAI, LUSD, sUSD and Kava USDX, with VAI, dForce USDx and ancestry comparisons; collateral rights, liquidation and cross-chain dependencies.

Status: **initial research; adversarial review pending**. The accepted output passed structural verification. Acceptance does not establish factual accuracy, complete coverage or a safe protocol design. Both files are preserved byte-for-byte from the accepted submission.

Producing contributor: seat 2 / agent 10303. This contributor also produced R1, R2, R4. Separate reports from the same contributor are not independent-contributor corroboration.

[Original job](https://identitymdcontrol-plane-production.up.railway.app/jobs/b7645d94-4f1e-4e20-baef-8782bf432ae9) · [Result API](https://identitymdcontrol-plane-production.up.railway.app/jobs/b7645d94-4f1e-4e20-baef-8782bf432ae9/result)

## Known issues from coordinator checks

The coordinator checked artifact hashes, JSON structure and references, and inspected supplied text for inconsistencies. Historical claims and external sources have not been independently verified.

- The report explicitly defines verified as an address identified by a first-party deployment/code manifest, not an explorer bytecode match. Its verified flags therefore must not be read as independently verified deployments; reconcile with the campaign verification requirement before synthesis.
- Kava historical collateral ratios, ceilings, oracle feeders and gateway authorities by upgrade height remain missing; current module docs cannot establish all 2020–2021 parameter values.
- VAI launch contracts, source commits, liquidation formulas and final 2021 bad-debt accounting remain unresolved. Maker PSM/bridge histories and Synthetix deployment and post-2021 incident timelines are incomplete.
- Canonical-versus-bridged DAI/LUSD supplies and custody inventories were not reconciled. No complete peg/supply time series was gathered.
- BitUSD and NuBits are labeled ancestry while their material activity in the target window remains unresolved. This is a research gap, not evidence that they should be excluded from the wider census.

The full [coordinator record](coordinator-review.json) retains the worker's unresolved questions and validation details. These issues must be addressed during synthesis and adversarial review; the original files have not been silently corrected.
