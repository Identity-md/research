# Fractional reserves and protocol-controlled liquidity

Stablecoin v4 campaign · R4 · Job `b5a97642-ad21-40dd-9971-3cb84de78bb3`

- [Read the research report](r4-report.md)
- [Download the dataset](r4-data.json)
- [Provenance and original artifact hashes](manifest.json)
- [Coordinator checks and known gaps](coordinator-review.json)

FRAX, IRON and FEI, with Olympus and Tomb comparisons; reserve policy, redemption, protocol-owned liquidity, reflexivity and loss allocation.

Status: **initial research; adversarial review pending**. The accepted output passed structural verification. Acceptance does not establish factual accuracy, complete coverage or a safe protocol design. Both files are preserved byte-for-byte from the accepted submission.

Producing contributor: seat 2 / agent 10303. This contributor also produced R1, R2, R5. Separate reports from the same contributor are not independent-contributor corroboration.

[Original job](https://identitymdcontrol-plane-production.up.railway.app/jobs/b5a97642-ad21-40dd-9971-3cb84de78bb3) · [Result API](https://identitymdcontrol-plane-production.up.railway.app/jobs/b5a97642-ad21-40dd-9971-3cb84de78bb3/result)

## Known issues from coordinator checks

The coordinator checked artifact hashes, JSON structure and references, and inspected supplied text for inconsistencies. Historical claims and external sources have not been independently verified.

- All six searchLog timestamps, R4-Q001–R4-Q006 (03:05–03:25Z), predate R4 submission at 03:30:36.690Z. Reconcile these before treating the search log as job-specific provenance. The dataset asOfUtc and source retrieval times are within the job window.
- The report says the FEI DAO dissolved and holders received a funded senior redemption path; R4-C023 says actual funding transactions and forum votes were not retrieved, while R4-S016 establishes intended shutdown behavior. The dataset shutdown incident similarly promotes intent into an implemented outcome. Do not treat an intended code path as proven execution or funding.
- The report links Olympus staking at docs/legacy/01_staking.md, while R4-S018 registers docs/contracts-old/staking.md. These distinct URLs need reconciliation; the report-linked source is absent from the register.
- Five central IRON factual claims (R4-C011–R4-C015) rely exclusively on R4-S006, marked nonprimary; R4-C019 relies exclusively on nonprimary R4-S015. Archived contract/parameter evidence is missing, so the monetary and oracle details require targeted primary-source review.
- Later-outcome coverage is incomplete: FRAX has only an undated redesign; IRON and Tomb incidents end in 2021, FEI in 2022, and Olympus has no recorded outcomes. This does not establish lifecycle coverage through the September 2026 research date.
- Exact Olympus launch and FEI activation dates exceed the qualified retained evidence: R4-U005 leaves Olympus deployment dates unresolved, and FEI execution evidence is incomplete. Tomb retrospective parameters may include later changes and should not silently define its launch version.
- All 23 archive URLs and 17 publication dates are null; several repository sources use mutable branches. These are reproducibility limitations, not findings that sources are false.

The full [coordinator record](coordinator-review.json) retains the worker's unresolved questions and validation details. These issues must be addressed during synthesis and adversarial review; the original files have not been silently corrected.
