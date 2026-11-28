# P versus NP research swarm · 27–28 November 2026

Independent workers reproduced **five distinct Lean results** with the competition's official checker. Two prove positive statements about reductions and algebraic complexity. Three refute proposed circuit-size bounds and establish exact minima of **6, 4 and 4 gates** on specified four-by-four Boolean tables. Another three units have a producer's local checker acceptance with an incomplete or disputed independent replay. P versus NP itself remains unresolved. [First research merge][root-1-01] · [Refutation merge][root-1-02]

## Participation and competition record

| Measure | Goal-attributable outcome |
|---|---|
| Proofs submitted / accepted upstream / points awarded | **0 / 0 / 0** |
| Locally accepted by the official checker | 11 complete proof files on 8 distinct statements, including refutations |
| Independently reproduced | 7 of those files on 5 statements. Two versions each passed for L-pcx-409 and L-meta-25842. |
| Participation | 38 completed work items across proof development, reductions, counterexample search, code integration and independent checking. Worker capacity was 10. The records do not identify the distinct contributors. |
| Preferred agent | The scheduler offered no individual-agent selector. Availability and participation of IMD Agent #1927 (ID 50973) are unverified. |
| Budget and cost | 38 of 50 item slots used, 12 unused. Monetary spend and the monetary ceiling were not reported. |
| Stopping point | All 15 batches settled by episode 5 of 5. Episodes 1, 3 and 4 used 10, 13 and 15 slots respectively. Fourteen conditional verification items were cancelled before running. |

The workers selected 19 distinct units, including one whose statement the assigned worker could not retrieve. Ten initial items each investigated one unit and returned either a proof or a specific obstruction. The next 13 completed proof files, built a rank component, audited two search methods and checked the complete candidates. The final 15 comprised eight circuit searches or refutation attempts and seven reviews, each tied to one returned file. The workers used public desk rows and public checkouts of the proof repository. No authorized GitHub submission account was supplied. The record shows zero competition forks, leases, heartbeats, releases and pull requests by this goal. The time allowed for hard units varied by batch. Elapsed research time per unit was not consistently documented, and one first-wave setup attempt ended before the requested 20 minutes. [First-wave results][root-1-01] · [Final-wave results][root-1-02]

## Exact circuit sizes

On an input pair `(u,v)` with both coordinates in `{0,1,2,3}`, four row indicators `Xᵢ` select `u` and four column indicators `Yᵢ` select `v`. Bit `4u+v` of the decimal mask specifies the required output. Each AND, OR or NOT gate counts toward the bound. An absent wire reads as false. A refutation proves that every permitted circuit with the requested gate budget misses at least one of the 16 inputs. A circuit one gate larger that gets all 16 right then establishes the minimum. [Circuit model and coverage][b06-enum]

| Unit | Mask | Requested maximum | Witness size | Evidence for the lower bound |
|---|---:|---:|---:|---|
| L-meta-25842 | 31711 | 5 | **6** | Two different Lean files passed independent replay. [Frontier proof][b11-m25842-b] · [Replay][b14-m25842-b] · [Search proof][b10-m25842] · [Replay][b13-m25842] |
| L-meta-25844 | 279 | 3 | **4** | Kernel search in 16 chunks. The independent build, type comparison and official replay passed. [Proof][b10-m25844] · [Replay][b13-m25844] |
| L-meta-25845 | 887 | 3 | **4** | A wire-by-wire table invariant justifies the pruned kernel search. The independent checker passed and exceeded the stated memory budget. [Proof][b10-m25845] · [Replay][b13-m25845] |
| L-meta-25843 | 31743 | 3 | **4** | Producer checker passed. Independent Lean elaboration, type and axioms passed in 576 seconds. A 600-second command limit prevented a full official replay. [Proof][b10-m25843] · [Replay fault][b13-m25843] |
| L-meta-25851 | 15855 | 6 | **7** | Producer checker passed and exhaustive search returned minimum 7. Independent verification of the lower bound remains disputed. [Proof and search][b11-m25851] · [Replay failure][b14-m25851] |
| L-meta-25846 | — | — | — | Episode 4 had identified mask 1983 and a four-gate request. The assigned worker could not retrieve the exact row or reach the repository. No search, witness or proof followed. [Attempt][b10-m25846] |

**Why mask 31711 needs six gates.** Its only false entries are the three diagonal cells `(1,1), (2,2), (3,3)`. Three ANDs test those cells, two ORs combine them, and one NOT complements the result. For the lower bound, trace the output backwards. Expanding a gate of fan-in at most two adds at most one live wire, so five gates can expose at most six distinct inputs. Every pair of rows differs in some column. A circuit reading fewer than three row indicators would see two rows identically, and the same reasoning applies to columns. All six available places are therefore needed. Every expansion must add one wire, leaving room only for binary AND and OR gates. [Six-gate witness and formal proof][b11-m25842-b]

Such a circuit is monotone in the input indicators it reads. For each row `i`, choose a nonzero `j ≠ i`. The output must drop from true at `(i,j)` to false at `(j,j)`. Only `Xᵢ` drops on that move, so the circuit must read it. Interchanging rows and columns forces all four column indicators as well. That requires eight inputs in six places. The smaller Lean implementation specializes the live-wire argument from `L_meta_26290` and the wire-table method from `L_meta_25471`. The alternate implementation adapts the backward-search framework of `L_meta_25814`. Independent C depth-first and C++ breadth-first searches also excluded every size through five. [Frontier replay][b14-m25842-b] · [Alternate replay][b13-m25842] · [C search][b06-enum] · [C++ search][b06-closure]

**A direct check on the three-gate results.** For this report, a separate enumeration started with the eight input tables and the implicit zero table. At each step it complemented each available table and took the pairwise ANDs and ORs within that state. Complementing zero covers the constant-one output of an empty AND or NOT. A gate returning an existing table can be dropped by redirecting its users. The enumeration found 62 distinct *output tables* reachable with at most one gate, 350 with at most two, and 1,358 with at most three. Masks 31743, 279 and 887 were absent. Their four-gate witnesses compute, respectively, `¬((X₂ ∧ Y₂) ∨ (X₃ ∧ Y₃))`, `(X₀ ∨ Y₀) ∧ ¬(X₃ ∨ Y₃)`, and `¬((X₂ ∧ Y₂) ∨ (X₃ ∨ Y₃))`. All six witness lists returned in the final wave, including both orders for mask 31711 and the seven-gate list for mask 15855, were evaluated on every cell for this report. [25843 witness][b10-m25843] · [25844 witness][b10-m25844] · [25845 witness][b10-m25845] · [25851 witness][b11-m25851]

For **L-meta-25851**, the producer adapted `L_meta_25814`, substituted target-specific separation pairs and obtained `ACCEPTED (refute)`. The second worker built the file and checked its negated type and axioms. It counted 47 declarations using the `theorem` keyword, including 46 helpers, and recorded a format failure at line 85. Other reviewers accepted helper theorems as lemmas. Separately, the second official checker run timed out during kernel verification. The seven-gate upper bound can be checked directly from the witness. The six-gate exclusion has one completed official checker run. [Producer][b11-m25851] · [Independent findings][b14-m25851]

## Two positive proofs

**L-pcx-409 · A counting-preserving reduction from NAND constraints to three matchings.** Given `v` variables and `g` NAND constraints, the construction places three signed matchings between two equal-sized vertex sets. An encoded assignment with `b` violated constraints has cost exactly `6g + 2b`. The decoder bounds the Hamming distance to its repaired encoding by the excess cost times a fixed constant. At cost `6g`, the distance and the violation count both vanish. Pinning the reference orientation removes the twofold choice of encoding, giving a bijection between configurations of cost exactly `6g` obeying the pins and satisfying assignments extending the same pins. Two workers completed the original matching construction with `C = 2,000,000`. A second worker reproduced each file. [First proof][b03-pcx-1] · [First replay][b04-pcx-1] · [Second proof][b03-pcx-2] · [Second replay][b04-pcx-2]

A third implementation, written from scratch with `C = 100,000,000`, passed its producer's checker. The goal's merged repository is **identity-md-launches/goal-3489-p-vs-np**, commit `df29d1b7f36b7e6e2de38985802923fbb54925da`. It contains the 77,009-byte proof at `lean/PEqualNP/Outside/L_pcx_409.lean` and the statement and check metadata at `notes/L-pcx-409.json`. On 27 November the desk showed PR #45207 at 23:36 UTC. By 23:45 UTC the unit was withdrawn as proved, and a different 175,711-byte file was on upstream main. The swarm earned no credit for that PR. [Goal commit][trunk] · [Proof on the goal trunk][trunk-proof] · [Proof metadata][trunk-note] · [Producer check][b09-pcx-409] · [Withdrawal record][b04-pcx-2]

**L-gct-299 · A bound on the widths admitting a complex subspace.** Let `y` have `h ≥ 3` nonzero coordinates with both its coordinate sum and sum of squares zero. At each larger odd width `q`, pad `y` with zeros. The question is whether a zero-sum subspace of dimension `(q−1)/2` satisfies the specified four-row permanent identity for every vector in the subspace and every scalar. For `h = 3` such a subspace exists at every eligible width. For odd `h > 3` it exists at none. For any `h > 3` at most three eligible widths work. The proof constructs the subspace in the first case. For larger supports it applies checked sibling `L_gct_297` to get a square characteristic polynomial. Four qualifying widths would force a product of relatively prime factors to divide a nonzero Wronskian of smaller degree. Independent replay passed. Another author's different 37,213-byte proof had already closed the unit on main. [Proof][b07-gct-299] · [Independent replay and upstream comparison][b08-gct-299]

## Cyclic parity lower bound

**L-clb-124** asks for a circuit computing the parity of a cyclic constraint count at `n = 4, w = 1`, with at most 20 binary gates and uncharged NOT gates. The decisive step was to instantiate checked theorem `L_clb_120` at `H = 4`. The admissibility condition holds because `J = 2^min(4,2) = 4`. With `E = nJ = 16`, the lower bound becomes `(E−H) + 3(H−1) = 12 + 9 = 21`, contradicting the proposed upper bound. This establishes a lower bound of 21 without claiming a matching construction. [Instance and side conditions][b12-clb-124]

The first file built under a suffixed theorem name. A corrected 1,157-byte file used the module's required name and passed the producer's checker in refute mode. It imports `PEqualNP.Outside.L_clb_120` in addition to the row's listed `PEqualNP.Defs`. The assigned reviewer could check the file format, but Lake initialization failed before the dependency, type, axioms and kernel check could be reproduced. [First attempt][b07-clb-124] · [Corrected file][b12-clb-124] · [Replay fault][b15-clb-124]

## Partial results

| Unit | What the work established and where it stopped |
|---|---|
| L-meta-33679 | The first worker derived the anchored-rank upper bound and algebraic witnesses. A later worker built the circuit attaining the bound, including rank `2s` when the second-layer budget `k = 0`. For `k > 0` the formula is `2k + 4s + 4p`, where `p` counts index pairs below `s` with different residues modulo `2k+1`. The builder was adapted from the already merged upstream proof. A 109,272-byte join elaborated under a temporary theorem name. The original statement digest could not be recovered from the withdrawn row, and the required root theorem lacks an official replay. [Original work][root-1-01] · [Attainment component][b05-rank-1] |
| L-gct-304 | Coefficient identities and the nonisotropic case reduce the dimension bound to two residual row-polynomial cases, `T⁴+d` and `T⁴−cT`. The checker exited 137 before a verdict. [Partial proof][b07-gct-304] |
| L-gct-307 | The partial proves the vanishing second moment and constraints on the third and fourth moments. Three case arguments remain, one of which used a proposed sibling, L-gct-305, absent from the observed checkout. [Partial proof][b07-gct-307] |
| L-lib-1064 | Projection-rank and independent-edge bounds leave a stronger common-edge estimate and an extra factor of 8/9 unproved. The skeleton contains a placeholder. [First-wave result][root-1-01] |
| L-clb-101 | A parity restriction rules out the suggested small example. The leaf-count argument leaves `d ≥ 6` and `m > 4(d+1)` open. [First-wave result][root-1-01] |
| L-pcx-407 | The path-graph and pinning lemmas give a partial lower bound. The affine-region bound and three upper constructions remain. The build timed out. [First-wave result][root-1-01] |
| L-meta-33656 | Elimination in the smallest example gave rank 8 and nullity 4. Optimal adaptive agreement remains open in this work. Toolchain setup stopped the formal attempt. [First-wave result][root-1-01] |
| L-meta-27129 | Small affine cases and the full-basis case were analyzed. The minimum-rank circuit construction is missing, and the skeleton contains a placeholder. [First-wave result][root-1-01] |
| L-meta-32468 and L-meta-33225 | Each graph has a reported Lean-checked 15-gate monotone witness. Search constrained any strict improvement using one NOT to 8–14 gates. Neither a correct improvement nor monotone optimality was established. [Two graph experiments][root-1-01] |

## Proof files and verification record

The producer links below contain the exact statement in `statement` and UTF-8 Lean source in `lean`. The SHA-256 values identify the exact **Lean file**. The two positive L-pcx-409 files in the table import `Mathlib` and `PEqualNP.Defs`. The five meta units import only `PEqualNP.Defs`. L-gct-299 and L-clb-124 additionally import the checked sibling named in their respective arguments. Each reviewer received the identical source digest. To recover a source without adding a newline, use `jq -j '.lean' result.json`. Unit IDs map to paths and theorem names by replacing hyphens with underscores. For example, L-meta-25842 uses `lean/PEqualNP/Outside/L_meta_25842.lean` and `PEqualNP.Outside.L_meta_25842`. The third L-pcx-409 file is preserved separately in the goal trunk and has a producer check only.

| Unit | Mode | Bytes | SHA-256 of Lean file | Producer / independent verdict |
|---|---|---:|---|---|
| L-pcx-409 | check | 57,059 | `65c658f512ecad773361703845c34ad131c635fbc808ed02541f55aead185b4c` | [Source][b03-pcx-1] · [pass][b04-pcx-1] |
| L-pcx-409 | check | 56,047 | `842cbf82bb90aae41522b0d1aa511a1b46d9a186f3c320f8f637d6146e1a34a6` | [Source][b03-pcx-2] · [pass][b04-pcx-2] |
| L-gct-299 | check | 31,642 | `6fa14f9918d8c403beb8227e5c3ae65b72f198f4381eb1825675727f840286dd` | [Source][b07-gct-299] · [pass][b08-gct-299] |
| L-meta-25842 | refute | 21,411 | `860b9059b516cf3200a58cb08fb98943f1ec43c8a6c92acd3396bb99da577c3e` | [Source][b11-m25842-b] · [pass][b14-m25842-b] |
| L-meta-25842 | refute | 37,608 | `0e409a01702a7e0a9894b5997646d36414edbc619255d8146c33bf8e8bcf6132` | [Source][b10-m25842] · [pass][b13-m25842] |
| L-meta-25844 | refute | 13,049 | `22ba4dce13874bc97803d02a0ade8ef5e1d7cee7ef90efc79cbd2ab3e3a7abb2` | [Source][b10-m25844] · [pass][b13-m25844] |
| L-meta-25845 | refute | 12,818 | `f30847ccbf31ff4aa3466e5b085ec9befdc85f179e6d0116b391a4d7e9c8d469` | [Source][b10-m25845] · [pass][b13-m25845] |
| L-meta-25843 | refute | 15,760 | `a3f1618fe369e491efe2385022d56905cfa67766824af1039a40c591fdb45a51` | [Source][b10-m25843] · [fault][b13-m25843] |
| L-meta-25851 | refute | 38,630 | `fdcc5fddff8ade7290cc9fdd616477850ca39422e3999bb8e8c47f27829c614b` | [Source][b11-m25851] · [fail][b14-m25851] |
| L-clb-124 | refute | 1,157 | `c2ad1fb4caa4d989016ea356383b1360506acc8cf4e9b23ff77bb4a05f3314e7` | [Source][b12-clb-124] · [fault][b15-clb-124] |

The workers used Lean **v4.36.0** and Mathlib commit `fc4f59e577feb1a4956671bc04ac18aaaf8cd842`. The recorded checks built the named module and ran `node tools/check-lean.mjs <file> <statement-file> <mode>` against the original statement. Mode `check` requires the stated proposition, and `refute` requires its negation. The independent passes report only `propext`, `Classical.choice` and `Quot.sound` and passed the format checks for placeholders, new axioms, `native_decide` and compile-time execution. The table-search files use kernel reduction. This report checked all 30 input hashes against the handoff, the byte length and digest of all 14 nonempty Lean sources in the handed JSON files, both audit-program digests and all ten producer/reviewer source matches. It did not rerun Lean. [Upstream toolchain checkout][upstream] · [Example independent checks][b13-m25844]

**Resource limits.** The passing replays for the two positive units all marked `within_limits=false`. For the two L-meta-25842 files, builds used about 3.1 GB and official checker runs peaked at 13.45 and 13.49 GB. For L-meta-25844 the reviewer judged the limit on the 5.70 GB build and measured a 16.0 GB checker peak. For L-meta-25845 the reviewer counted the 15.85 GB checker peak and explicitly marked the limit exceeded. The comparable 13.42 GB peak of a trivial control in one run helps explain the discrepancy. Compliance with the competition's approximately 6.5 GB memory ceiling remains unverified. External-source checks also flagged `prove-a/meta-e`, `verify-c/pcx-1`, `prove-c/gct-299` and `recheck-wide-d/m25851`. Desk observations in this report are dated to the workers' reads. [Memory control][b13-m25842] · [Absolute-peak accounting][b13-m25845] · [First merge][root-1-01] · [Second merge][root-1-02]

**Submission status.** The two confirmed positive units were closed upstream. The later refutation records showed no open PR for their observed units, and several rows were reserved or unavailable for offers. An authorized submitter would have to verify current eligibility and obtain the desk's negated twin identifier. None was supplied in this run. For an eligible candidate, the recorded workflow is `tools/pnp.sh setup`, `tools/pnp.sh next --proof-of <unit>`, then `tools/pnp.sh check <assigned-unit>` and `tools/pnp.sh submit <assigned-unit>` in the authorized fork, using exactly the leased path, theorem and permitted imports. Each PR adds one proof file. The lease calls for a beat every five minutes, at most five active units per account, stopping on withdrawal and releasing an unsolved unit with its reason. No competition action is pending under a swarm-held lease. [Competition reference][reference] · [Dated refutation status][b14-m25842-b]

[b03-pcx-1]: https://api.imd.fun/artifacts/69120d22bbed16cf785eb43b3fc9d4b04a71674146d982c8047fdbeeae257813
[b03-pcx-2]: https://api.imd.fun/artifacts/fdb9f12b5d8cb3355999b616c04ebddcffa32032826ac357c85cec84d0490765
[b04-pcx-1]: https://api.imd.fun/artifacts/c3441dadf953467771ab402017969330dd282992140250e562a8f879ef60f957
[b04-pcx-2]: https://api.imd.fun/artifacts/8698f15b1104a1100607da27a008d82367e4f0a638c2130ad03d1779dd14c50d
[b05-rank-1]: https://api.imd.fun/artifacts/02b4175df96abb38d0a2df6e29d0bc756ce6870d839a88d817d7f9f1a8a8b9fc
[b06-closure]: https://api.imd.fun/artifacts/06d291ab31c1e5171ee2050ccf0490e277f343ceb8db2b699fdf10b4516baed7
[b06-enum]: https://api.imd.fun/artifacts/381bf4632175165761ad443d664d0b0b61d3c0a35f94c958eb1758dc332f4284
[b07-clb-124]: https://api.imd.fun/artifacts/4ca95eb6e21ddb1708ddf97dd8dc041202906650ba1657b7cf270d55d3c52a7e
[b07-gct-299]: https://api.imd.fun/artifacts/8cf37a1ee45582e90e1774f6c5dd7e8461a01fad6d960fe540d249bc84358fb4
[b07-gct-304]: https://api.imd.fun/artifacts/b402d83116f77ac3218071a7506069d6ff02d7d34198b21f76f632cabce1a7ed
[b07-gct-307]: https://api.imd.fun/artifacts/39414e336986c59abef9f1ffe77b2918dee61eed6adbaf7378fd66586837f01b
[b08-gct-299]: https://api.imd.fun/artifacts/a04101bc535538e6baeed0bdde9e2e9f773ca3186c2c342976d7c3cd623e1ae4
[b09-pcx-409]: https://api.imd.fun/artifacts/8a538e4f733a3d072e35417bd5f05cf9e3c493d2fce336e5d7a2456a7a3d392d
[b10-m25842]: https://api.imd.fun/artifacts/628ea9d27b90c6036dfb71bf1c28474aaf5d874a7b2a7def4c78a00175b01104
[b10-m25843]: https://api.imd.fun/artifacts/f4f7294abccbf5c508ba944e9cf6180a68c81c6846b5d11481a9dc0b12ec1e62
[b10-m25844]: https://api.imd.fun/artifacts/fa779fd197740ffcde7778322145f7b9ed1ef5395c01db79c07442c26aa95ea1
[b10-m25845]: https://api.imd.fun/artifacts/891e79f5953d0027f54496e49f4faf03a26a7ecbacf1454d42525e228dce0caf
[b10-m25846]: https://api.imd.fun/artifacts/47b6b101e9003808497fbf208190cc9ea1f2ab5c5ddbb33929332adfb5b4c999
[b11-m25842-b]: https://api.imd.fun/artifacts/0d27e3856b4ddd41492ec893716385a8ab73498f344ac37a6ded611eedc41d36
[b11-m25851]: https://api.imd.fun/artifacts/cc19dc91d0d20ec4949ecbee1e9934ad52772cc28ea240c9b7a06cca7763a12b
[b12-clb-124]: https://api.imd.fun/artifacts/7aac39476485e29a6726553324d3acf3ca0bc29bf10905450e257287c105191d
[b13-m25842]: https://api.imd.fun/artifacts/ae83929299ff3c382f7872727c657a23659ef306db980b6797e4f2d9ef22c3f4
[b13-m25843]: https://api.imd.fun/artifacts/64295fa81d80708435a20a099d69d8a6e75ac249935f81a2a912deeb3d9a44f3
[b13-m25844]: https://api.imd.fun/artifacts/33d496b16e5150504b8c3f2bae6cc01e2203b629685ecdc2442e8534f7993230
[b13-m25845]: https://api.imd.fun/artifacts/cec2b707c8d44403080786d373a5a398d1f6b3f31b3d8f97cb76d7ad0479ac47
[b14-m25842-b]: https://api.imd.fun/artifacts/bd722c7544c1294b4fb1b5b2de2ce1aa457974589ded20dcd18fa3b26e1a2906
[b14-m25851]: https://api.imd.fun/artifacts/1616c386f41e50f131f08b99abaa7a12df35786943b6b8a44b31ed4a4ee3fa2c
[b15-clb-124]: https://api.imd.fun/artifacts/324304f8d20703f7bfbf4639844e790f7854c953930f29629ae8a31fe3b1f157
[reference]: https://pequalnp.com/join.txt
[root-1-01]: https://api.imd.fun/artifacts/5e7e1e498110ae5aea93ce203a69b2891f1fbf80efd8c322aa68ce7ba894f043
[root-1-02]: https://api.imd.fun/artifacts/df4443a04db6a960b06fff1a5a20db84f3672784246a79a567c3089a9fb49871
[trunk]: https://github.com/identity-md-launches/goal-3489-p-vs-np/commit/df29d1b7f36b7e6e2de38985802923fbb54925da
[trunk-note]: https://github.com/identity-md-launches/goal-3489-p-vs-np/blob/df29d1b7f36b7e6e2de38985802923fbb54925da/notes/L-pcx-409.json
[trunk-proof]: https://github.com/identity-md-launches/goal-3489-p-vs-np/blob/df29d1b7f36b7e6e2de38985802923fbb54925da/lean/PEqualNP/Outside/L_pcx_409.lean
[upstream]: https://github.com/open-goat/pequalnp-proofs/tree/e8dc2d83cc1f03dc3fcf24af495304f2dc5e0d36
