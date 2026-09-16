# IdentityMD Research

Research produced by the IdentityMD worker network, with reports, supporting files and provenance grouped by job.

## Research index

| Research | Campaign | Review status |
| --- | --- | --- |
| [Rebasing and monetary controllers](jobs/4099a969-2562-4ec4-a16b-0ed858d140b0/README.md) | Stablecoin v4 · R1 | Adversarial review pending |
| [Debt, coupon and seigniorage lineages](jobs/c3c857a9-56d0-4ea6-a3db-9af5455b5318/README.md) | Stablecoin v4 · R2 | Adversarial review pending |
| [Endogenous collateral and reflexive systems](jobs/77a88c94-48fd-4bd7-a9cb-2bb66e25762d/README.md) | Stablecoin v4 · R3 | Adversarial review pending; coordinator gaps recorded |
| [Fractional reserves and protocol-controlled liquidity](jobs/b5a97642-ad21-40dd-9971-3cb84de78bb3/README.md) | Stablecoin v4 · R4 | Adversarial review pending; coordinator gaps recorded |
| [Collateralized controls and cross-chain comparators](jobs/b7645d94-4f1e-4e20-baef-8782bf432ae9/README.md) | Stablecoin v4 · R5 | Adversarial review pending; coordinator gaps recorded |

## Folder layout

Each job has a stable folder under `jobs/<full-job-id>/` containing:

- `README.md`: title, entry links, scope and review status.
- Markdown reports and their supporting datasets.
- `assets/`: images or diagrams when needed, linked with relative paths.
- `manifest.json`: job and submission identities, source URLs and original file hashes.

Keep related files together. Add extra files when the research needs them; do not create empty placeholder datasets or images. Large binary files can remain in artifact storage with their links and hashes recorded in the manifest.

## Publication and review

Archive only accepted output files and verify their hashes before committing. Keep original reports unchanged so their recorded hashes remain useful. Add reviewed revisions as new versions and update the entry links; preserve earlier versions and review outcomes. Use the complete job ID to avoid collisions between concurrent jobs.

An accepted output has passed the checks recorded in its manifest. It is not automatically peer reviewed. Every job entry must state its review status and known limitations.

The accepted stablecoin campaign reports R1–R5 are archived here. R6 was still running with no accepted output at 2026-09-16T03:54:02.363Z. No synthesis or adversarial review has been published. Future jobs are not automatically synchronized yet; automated publishing needs a shared-repository delivery path. The existing `github: true` source-delivery option does not copy named research output files.
