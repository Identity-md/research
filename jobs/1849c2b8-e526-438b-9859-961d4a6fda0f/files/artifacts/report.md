# Verifier collusion and single-operator dependence in decentralized verification networks

*Research date: 2026-09-25. Sources were fetched on that date; anything time-sensitive (bond sizes, challenge windows, policy thresholds) may have changed since.*

## Question

How do decentralized verification networks handle (a) collusion among verifiers and (b) reliance on a single operator? The report compares three families: optimistic/fraud-proof designs, quorum attestation, and reproducible builds. It then recommends the **smallest incremental step** away from a single signed verifier service toward multiple independent verifiers, and states the tradeoffs.

## How to read this report

Each claim is labelled:

- **[F] Fact:** stated by the cited source. Where possible the source is primary (project docs, specs, papers). Secondary sources are marked as secondary.
- **[I] Inference:** my own reasoning from the facts. It is not stated by any source.
- **[U] Uncertain:** evidence is incomplete, secondary, or likely to change.
- **Open questions** are collected in their own section at the end.

## Summary

- The three families rest on different trust assumptions:
  - **Fraud proofs** need only **one honest, live verifier (1-of-N)**, but they add a delay (about a week on major rollups) and depend on someone actually checking.
  - **Quorum attestation** needs an **honest threshold (e.g. f+1 of n with f < n/3)** and gives immediate answers. It fails if the signers are not really independent.
  - **Reproducible builds** make a result *re-checkable by anyone*. On their own they give detection, not enforcement.
- In practice, systems in production combine them: a threshold of signers, a public log so misbehaviour can be seen, and re-execution by independent parties. [I]
- **Recommendation** [I]: keep the existing signed service. Add **one independently operated co-verifier** that re-runs the same deterministic check and **co-signs** the result, following the transparency-log "witness" pattern. Run it in observe-only mode first. Then make clients require both signatures (2-of-2), and grow to k-of-n later. The main tradeoff is lower liveness in exchange for resistance to a single operator.

## 1. Optimistic / fraud-proof designs

**How they work.**
- [F] In the OP Stack, proposals and challenges are permissionless ("can be submitted by anyone"). There is a "~1 week challenge period", and bonds are "sized based on the anticipated cost to post a counter-claim as well as to deter spamming invalid claims" ([Optimism fault-proof explainer](https://docs.optimism.io/stack/fault-proofs/explainer)).
- [F] Arbitrum's BoLD "does not change the fact that only a single honest party is required to defend Arbitrum". Challenges "conclude within a 6.4-day window" ([Arbitrum BoLD introduction](https://docs.arbitrum.io/how-arbitrum-works/bold/gentle-introduction)).
- [F] BoLD requires a 3,600 ETH bond to post an assertion. It targets a "resource ratio" of 6.46 (attacker cost to defender cost) on Arbitrum One ([BoLD economics](https://docs.arbitrum.io/how-arbitrum-works/bold/bold-economics-of-disputes)). [U] These parameters can be changed by governance.

**Against collusion.**
- [I] Collusion among proposers does not help, because a single honest challenger can win a dispute. The attacker has to suppress *every* honest verifier, for example by censoring them or outspending them in bonds, which is what the resource ratio is meant to price.

**Against single-operator dependence.**
- [F] Both systems keep an override. On OP Mainnet a Guardian (the Security Council) can reject a finalized root during an "airgap window", pause withdrawals, or fall back to a permissioned system ([Optimism explainer](https://docs.optimism.io/stack/fault-proofs/explainer)).
- [F] L2BEAT's Stages framework measures how far such overrides are constrained. Stage 0 asks for "at least 5 external actors that can submit a fraud proof". Stage 2 requires a permissionless proof system and "at least 30 days to exit" before unwanted upgrades ([L2BEAT Stages](https://l2beat.com/stages)). [U] That summary comes from an automated page fetch; check the exact wording on the page.

**Known weakness: nobody checks.**
- [F] Luu, Teutsch, Kulkarni and Saxena describe the "verifier's dilemma": when checking is expensive, rational participants are "well-incentivized to accept unvalidated" results ([Demystifying incentives in the consensus computer, CCS 2015](https://eprint.iacr.org/2015/702)).
- [F] TrueBit proposes verification games plus financial incentives for outsourced computation ([Teutsch & Reitwießner, arXiv:1908.04756](https://arxiv.org/abs/1908.04756)).
- [U] I could not retrieve the full TrueBit PDF to quote its "forced errors"/jackpot mechanism directly, so that detail is not cited here.

**Fit for a small network** [I]:
- The 1-of-N assumption is the weakest trust assumption available.
- However, the design needs an on-chain or otherwise neutral arbiter, bonds, a dispute game, and a finality delay. That is a large first step for a network that today has one signing service.

## 2. Quorum attestation (several independent verifiers sign the same result)

**How it works.**
- [F] Chainlink OCR: "a quorum of nodes signed the report". The on-chain contract "verifies that a quorum of nodes signed the report" ([Chainlink OCR docs](https://docs.chain.link/architecture-overview/off-chain-reporting)).
- [F] The protocol tolerates "up to f of which could be byzantine (f < n/3)". An attested report needs "at least f+1" signatures, so that at least one honest node signed it. This comes from a secondary explanation ([mmapped.blog on OCR](https://mmapped.blog/posts/24-ocr)); the primary paper is the [OCR3 paper](https://research.chain.link/ocr3.pdf). [U] I could not extract text from the OCR3 PDF, so the thresholds rest on the secondary source.
- [F] TUF requires support for "roles with multiple keys and threshold/quorum trust", so that "an attacker, who is able to compromise a single key or less than a given threshold of keys, cannot compromise clients" ([TUF specification](https://theupdateframework.github.io/specification/latest/)).
- [F] Certificate Transparency in Chrome requires SCTs from "distinct CT log operators as recognized by Chrome": at least two, and more for long-lived certificates ([Chrome CT policy](https://googlechrome.github.io/CertificateTransparency/ct_policy.html)). This is a quorum by *operator*, not just by key.
- [F] Transparency-log witnesses verify a checkpoint's signature and a Merkle consistency proof against the last checkpoint they cosigned, then return a cosignature. Clients "MUST ignore any cosignatures from unknown keys" and choose which witnesses they trust ([C2SP tlog-witness](https://c2sp.org/tlog-witness)).
- [F] Sigsum policies express this as `group <name> <k> <members...>` plus a `quorum` line, meaning "at least k of its n members" ([Sigsum policy doc](https://git.glasklar.is/sigsum/core/sigsum-go/-/raw/main/doc/policy.md)).

**Failure mode: signers that are not really independent.**
- [F] The Ronin bridge needed 5 of 9 validator signatures, and Sky Mavis controlled 4 of them. A lingering allowlist let Sky Mavis also produce signatures for the Axie DAO validator, so compromising one organisation gave the attacker the quorum (~$624M). Source is secondary ([Halborn analysis](https://www.halborn.com/blog/post/explained-the-ronin-hack-march-2022)); the Ronin postmortem URL returned 404 when fetched.
- [I] A k-of-n quorum is only as strong as the number of *independent failure domains* among the n signers: operator, keys, hosting, and codebase. Counting keys overstates security. CT's "distinct operators" rule is a direct answer to this.

**Fit for a small network** [I]:
- Clients only need to verify k signatures. There is no dispute game and no delay.
- Safety depends on the honest-threshold assumption.
- Every extra required signer is another party that can stall the system, so liveness goes down.

## 3. Reproducible builds / reproducible verification

**How it works.**
- [F] Definition: "A build is reproducible if given the same source code, build environment and build instructions, any party can recreate bit-by-bit identical copies of all specified artifacts" ([reproducible-builds.org](https://reproducible-builds.org/docs/definition/)).
- [F] In Bitcoin Core, independent builders publish signed `SHA256SUMS` attestations per release under `/<version>/<signer>/`. This allows verification that the released binaries match the reproducibly built ones ([bitcoin-core/guix.sigs](https://github.com/bitcoin-core/guix.sigs)).
- [F] Debian has been described as having "multiple Debian Developers ... upload signatures attesting that they have been able to reproduce a build". The site also says "more research is required" to make this effective for early detection of compromise ([Sharing certifications](https://reproducible-builds.org/docs/sharing-certifications/)).

**Limits.**
- [F] SLSA separates "reproducible" builds from "verified reproducible" builds, which use "two or more independent build platforms". SLSA does not mandate verified reproducibility and lists its limits:
  - it does not address source, dependency, or distribution threats;
  - reproducers must be truly independent;
  - some builds cannot easily be made reproducible ([SLSA FAQ](https://slsa.dev/spec/v1.0/faq)).
- [F] SLSA's own artifact verification checks provenance signatures against trusted builders. It does not rebuild ([SLSA verifying artifacts](https://slsa.dev/spec/v1.0/verifying-artifacts)).

**Role against collusion and single operators** [I]:
- Reproducibility is what makes both of the other families possible. A fraud proof or a second signature only means something if a second party can independently get the *same* answer.
- On its own it gives detection (anyone can recheck), not prevention. Someone has to act on a mismatch.

## 4. Detecting a lying single operator: transparency logs

This is a supporting mechanism, not one of the three families.

- [F] RFC 9162 (CT v2) says a misbehaving log can show "different, inconsistent views of itself to different clients", and "therefore, it is necessary to treat each log as a trusted third party". The RFC leaves gossip-style defences out of scope ([RFC 9162](https://www.rfc-editor.org/rfc/rfc9162.html)).
- [F] Sigstore points to Rekor Monitor and Omniwitness to audit consistency and detect split views ([Sigstore logging overview](https://docs.sigstore.dev/logging/overview/)).
- [I] Witness cosigning (§2) is how that ecosystem moved from "trust the single log operator" to "trust that not all k witnesses collude". This is structurally the same move the target network needs to make.

## 5. Comparison

| Property | Fraud proofs (optimistic) | Quorum attestation | Reproducible verification |
|---|---|---|---|
| Honesty assumption | 1 honest, live challenger [F] | ≥ threshold honest, e.g. f+1 of n, f < n/3 [F, secondary] | ≥1 independent re-checker who publishes [I] |
| Latency to final result | Challenge window, ~6.4–7 days in major rollups [F] | Immediate once k signatures exist [I] | Immediate for the producer; rechecks are asynchronous [I] |
| Enforcement | Automatic via a dispute game and arbiter [F] | Clients reject results below threshold [F] | None by itself; needs a policy or quorum [I] |
| Main collusion risk | Censoring or outspending all challengers [I] | Signers sharing an operator, keys or code (Ronin) [F] | Rebuilders sharing a toolchain or environment [F, SLSA] |
| Infrastructure needed | Arbiter contract, bonds, bisection game [F] | Key registry, signature aggregation, client policy [I] | Deterministic pipeline, published inputs [F] |
| Cost of first step for a one-service network | High [I] | Low to moderate [I] | Low to moderate, if verification is deterministic [I] |

## 6. Recommendation for a network whose verifier is one signed service

All of this section is inference [I]. It builds on the patterns cited above. I did not inspect the target network's actual verifier.

**Smallest step: add one independently operated co-verifier that re-executes the same deterministic check and co-signs the result (witness cosigning). Roll it out in phases.**

0. **Make the verdict reproducible (prerequisite).**
   - Pin the verifier code, its dependencies, and its inputs.
   - Emit a canonical verdict record: input hashes, verifier version, and the result.
   - The existing service signs that record, not a free-form response.
   - This is the reproducible-builds step applied to verification. It is what makes a second opinion comparable byte for byte.
1. **Shadow mode.**
   - A second verifier, run by a *different* operator with a different key and different hosting (ideally a different implementation too), independently recomputes and signs the same canonical record.
   - Clients still accept the primary signature alone. They record the co-signature, and any disagreement is logged and investigated.
   - This follows the tlog-witness pattern: the witness only co-signs what it has checked itself.
2. **Enforce 2-of-2.**
   - Clients require both signatures, expressed as an explicit policy (Sigsum-style `group verifiers 2 primary cosigner`).
   - This removes unilateral control by the primary operator.
3. **Grow to k-of-n** (e.g. 2-of-3, then f+1 of 3f+1).
   - This restores liveness.
   - Independence rules follow CT's "distinct operators" and the lesson from Ronin: no operator may hold more than one seat or delegate signing to another seat.
4. **Optional later.** Add an optimistic challenge path, where anyone holding a reproducible counter-verdict can flag or revoke a result. This moves toward the 1-of-N assumption without making every verdict wait for a window.

**Why this step and not the others:**
- It changes the least: one more signer, one client policy line, and a canonical record format.
- It keeps the existing service in place, so there is no migration.
- Fraud proofs would first need an arbiter, bonds, and a dispute game.

**Tradeoffs of the recommended step:**
- **Liveness vs safety.** At 2-of-2, either operator can halt verification by going down or refusing to sign. Safety improves; availability roughly becomes the product of both services' uptimes. Moving to 2-of-3 addresses this but needs a third party.
- **Collusion is reduced, not eliminated.** Two colluding operators can still sign a false result. Independence is organisational and cannot be checked cryptographically; the Ronin case shows how a delegation can quietly merge "independent" seats.
- **Correlated bugs.** If both verifiers run the same code, a bug produces two matching wrong answers. Implementation diversity helps but costs more (SLSA notes that reproducers "must be truly independent").
- **Determinism burden.** Any nondeterminism (timestamps, network fetches, model or heuristic outputs) causes false disagreements. Some checks may not be reproducible at all.
- **Operational cost.** This adds key management, a rotation and removal process, a published signer registry, and a dispute-handling procedure for mismatches.
- **The primary still controls inputs and ordering.** Co-signing proves agreement on the *given* inputs. It does not stop the primary from choosing what to submit or withholding items (censorship). An append-only log of verdicts, witnessed as in §4, would address split views and omissions.

## Open questions

1. What exactly does the target network's verifier compute, and is it deterministic? The whole recommendation depends on step 0 being feasible. I have no evidence about this.
2. Who could credibly run the second (and third) verifier, and how would their independence be established and audited?
3. Is there a neutral place, such as a chain, a contract, or a transparency log, where a signer registry and client policy can be published? Or do clients hard-code keys?
4. Which failure is worse for this network's users: a halt (the liveness cost of 2-of-2) or a wrong verdict? The answer sets the threshold.
5. Would a future optimistic path need bonds? Who would fund challengers, given the verifier's dilemma?
6. **Unverified here:**
   - the exact OCR3 fault thresholds from the primary paper (the PDF could not be parsed);
   - TrueBit's forced-error mechanism (the PDF could not be fetched);
   - Ronin's own postmortem wording (URL returned 404; a secondary source was used).

## Sources

- Optimism, Fault Proofs explainer: https://docs.optimism.io/stack/fault-proofs/explainer
- Arbitrum, BoLD gentle introduction: https://docs.arbitrum.io/how-arbitrum-works/bold/gentle-introduction
- Arbitrum, BoLD economics of disputes: https://docs.arbitrum.io/how-arbitrum-works/bold/bold-economics-of-disputes
- L2BEAT, Stages framework: https://l2beat.com/stages
- Luu et al., *Demystifying incentives in the consensus computer*, CCS 2015: https://eprint.iacr.org/2015/702
- Teutsch & Reitwießner, *A Scalable Verification Solution for Blockchains*: https://arxiv.org/abs/1908.04756
- Chainlink, Offchain Reporting docs: https://docs.chain.link/architecture-overview/off-chain-reporting
- Breidenbach et al., OCR 3.0 paper (not text-extracted): https://research.chain.link/ocr3.pdf
- mmapped.blog, *The off-chain reporting protocol* (secondary): https://mmapped.blog/posts/24-ocr
- The Update Framework specification: https://theupdateframework.github.io/specification/latest/
- Chrome Certificate Transparency policy: https://googlechrome.github.io/CertificateTransparency/ct_policy.html
- RFC 9162, Certificate Transparency v2: https://www.rfc-editor.org/rfc/rfc9162.html
- C2SP tlog-witness: https://c2sp.org/tlog-witness
- Sigsum trust policy: https://git.glasklar.is/sigsum/core/sigsum-go/-/raw/main/doc/policy.md
- Sigstore, logging overview: https://docs.sigstore.dev/logging/overview/
- Reproducible Builds, definition: https://reproducible-builds.org/docs/definition/
- Reproducible Builds, sharing certifications: https://reproducible-builds.org/docs/sharing-certifications/
- Bitcoin Core guix.sigs: https://github.com/bitcoin-core/guix.sigs
- SLSA v1.0 FAQ: https://slsa.dev/spec/v1.0/faq
- SLSA v1.0, verifying artifacts: https://slsa.dev/spec/v1.0/verifying-artifacts
- Halborn, *Explained: The Ronin Hack* (secondary): https://www.halborn.com/blog/post/explained-the-ronin-hack-march-2022
