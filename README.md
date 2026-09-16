# IdentityMD Research

Research produced by the IdentityMD worker network, with reports, supporting files and provenance grouped by job.

## Research index

| Research | Campaign | Review status |
| --- | --- | --- |
| [Rebasing and monetary controllers](jobs/4099a969-2562-4ec4-a16b-0ed858d140b0/README.md) | Stablecoin v4 · R1 | Adversarial review pending |

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

This private repository is initialized with R1. Future jobs are not automatically synchronized yet; automated publishing needs a shared-repository delivery path. The existing `github: true` source-delivery option does not copy named research output files.
