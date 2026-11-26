**Fifteen unit semicircles: verified published tie**

The delivered packing passes the pinned official local scorer at **R = 2.948526950912552**, or **2.94852695** to eight decimal places. It is approximately **0.000003049087448 below the literal target 2.94853**. It reproduces the published packing: **no search produced a meaningful improvement over that packing's full-precision radius**. This is a published tie, not a new record. The comparison uses the requester's stated leaderboard figure; no live leaderboard priority claim is made. Nothing was submitted and no sign-in was performed.

The final witness and successful separate verification come from **topology-check-r3/best (b14-best)**. The coordinates also match the public fork at commit `d27ef1e3b9cbaeeb998c25fc8b76ae1d54ec3a79`, after six-decimal rounding. That equality was checked again while preparing this report. [Published coordinates](https://raw.githubusercontent.com/rorz/shape-packing-challenge/d27ef1e3b9cbaeeb998c25fc8b76ae1d54ec3a79/solution.json).

This assignment permits one delivered file, `report.md`. The named files are therefore supplied below as complete, extractable payloads: **solution.json**, **official-score.json**, **plot.svg**, **decisions.json**, **geometry_scorer.py**, and **geometry_test.py**. The extraction recipe preserves their exact bytes, including the solution's absence of a trailing newline. No temporary input path is needed to recover them.

<svg xmlns="http://www.w3.org/2000/svg" width="372" height="372" viewBox="0 0 372 372"><rect width="100%" height="100%" fill="white"/><circle cx="185.99" cy="185.99" r="176.91" fill="none" stroke="red" stroke-width="1.5"/><path d="M186.31,196.16 A60,60 0 0 0 251.14,95.18 Z" fill="#9cf" fill-opacity="0.6" stroke="#036" stroke-width="1"/><text x="241.4" y="164.3" font-size="12" text-anchor="middle">0</text><path d="M301.65,223.70 A60,60 0 0 0 206.60,296.95 Z" fill="#9cf" fill-opacity="0.6" stroke="#036" stroke-width="1"/><text x="237.6" y="242.9" font-size="12" text-anchor="middle">1</text><path d="M91.26,193.01 A60,60 0 0 0 210.65,205.11 Z" fill="#9cf" fill-opacity="0.6" stroke="#036" stroke-width="1"/><text x="148.2" y="229.9" font-size="12" text-anchor="middle">2</text><path d="M256.90,193.09 A60,60 0 0 0 336.27,103.09 Z" fill="#9cf" fill-opacity="0.6" stroke="#036" stroke-width="1"/><text x="316.8" y="170.0" font-size="12" text-anchor="middle">3</text><path d="M248.82,31.91 A60,60 0 0 0 156.56,108.65 Z" fill="#9cf" fill-opacity="0.6" stroke="#036" stroke-width="1"/><text x="185.4" y="53.5" font-size="12" text-anchor="middle">4</text><path d="M143.51,17.45 A60,60 0 0 0 141.65,137.43 Z" fill="#9cf" fill-opacity="0.6" stroke="#036" stroke-width="1"/><text x="115.6" y="81.0" font-size="12" text-anchor="middle">5</text><path d="M79.60,62.10 A60,60 0 0 0 97.44,180.76 Z" fill="#9cf" fill-opacity="0.6" stroke="#036" stroke-width="1"/><text x="61.8" y="129.4" font-size="12" text-anchor="middle">6</text><path d="M92.18,132.17 A60,60 0 0 0 211.44,145.52 Z" fill="#9cf" fill-opacity="0.6" stroke="#036" stroke-width="1"/><text x="148.8" y="169.7" font-size="12" text-anchor="middle">7</text><path d="M141.85,120.89 A60,60 0 0 0 234.11,44.15 Z" fill="#9cf" fill-opacity="0.6" stroke="#036" stroke-width="1"/><text x="205.2" y="107.3" font-size="12" text-anchor="middle">8</text><path d="M287.99,150.87 A60,60 0 0 0 235.45,42.98 Z" fill="#9cf" fill-opacity="0.6" stroke="#036" stroke-width="1"/><text x="286.0" y="89.1" font-size="12" text-anchor="middle">9</text><path d="M31.70,146.51 A60,60 0 0 0 106.91,240.02 Z" fill="#9cf" fill-opacity="0.6" stroke="#036" stroke-width="1"/><text x="48.3" y="214.2" font-size="12" text-anchor="middle">10</text><path d="M31.76,250.75 A60,60 0 0 0 151.46,259.24 Z" fill="#9cf" fill-opacity="0.6" stroke="#036" stroke-width="1"/><text x="89.7" y="285.9" font-size="12" text-anchor="middle">11</text><path d="M304.51,317.33 A60,60 0 0 0 193.44,362.75 Z" fill="#9cf" fill-opacity="0.6" stroke="#036" stroke-width="1"/><text x="238.8" y="319.0" font-size="12" text-anchor="middle">12</text><path d="M95.93,335.03 A60,60 0 0 0 181.35,250.74 Z" fill="#9cf" fill-opacity="0.6" stroke="#036" stroke-width="1"/><text x="157.6" y="316.1" font-size="12" text-anchor="middle">13</text><path d="M247.15,265.71 A60,60 0 0 0 342.19,192.46 Z" fill="#9cf" fill-opacity="0.6" stroke="#036" stroke-width="1"/><text x="311.2" y="254.5" font-size="12" text-anchor="middle">14</text><text x="5" y="14" font-size="12">R=2.94852695</text></svg>

The red circle is the official enclosing circle; labels 0–14 are array indices. This b14 SVG rounds pixel coordinates for display; scoring uses the JSON.

**Final scoring evidence.**

| Measurement | Result |
|---|---|
| Official local validity | `true`; no errors |
| Official radius, full reported precision | 2.948526950912552 |
| Radius, eight decimals | 2.94852695 |
| CLI display, six decimals | 2.948527 |
| MEC centre | (−0.0001819080616875258, 0.00013448997007248039) |
| Maximum official polygon intersection area | 9.997822348073146e-7, pair (2,13) |
| Containment excess, maximum | 1.98507876802978e-13, within the official 1e-9 allowance |
| Solution | 15 objects, 45 finite numbers, all six decimals |
| Exact solution byte count | 700, UTF-8, no trailing newline |
| Solution SHA-256 | `57135c157acfa62d0b5f833d0dc111f8c6b12324841fc01fb21d52f2295a6c77` |
| Plot SHA-256 | `c1da0959768c984d138ee0bbec3c1e5ae39a761948bd1a5e1b665fd41bd54ce4` |

b14 reports a fresh, unmodified clone of the [official repository](https://github.com/benedictbrady/shape-packing-challenge) at **`78a78626f098cd236f3a09bb2cb242f72951599d`**, successful `uv sync`, and a sample score of **3.500000**. It reread the finalist bytes through the official loader and ran both the CLI and `validate_and_score`. Its checker performed no optimization and used no producer scorer code. b13 separately re-scored the identical published witness at the same radius. Earlier successful executions, baseline-check-r2/published and moves-check-r2/best, are documented in the goal notes and root-1-02. These are distinct verification jobs and reported producer-independent executions; there is no separate identity audit of their contributors.

The official loader rounds **x, y and theta**, including angles, before scoring. Its overlap test uses **4096 arc-point inscribed polygons** and rejects a pair when the polygon intersection area is **greater than 1e-6**. The public description says intersection area **below 1e-6**; the finalist's polygon maximum is strictly below that value, so the equality convention does not affect it. The official MEC uses boundary samples followed by analytic farthest-point refinement. [Rules](https://www.paradigm.xyz/puzzles/packing/about), [pinned loader](https://github.com/benedictbrady/shape-packing-challenge/blob/78a78626f098cd236f3a09bb2cb242f72951599d/run.py), [pinned geometry](https://github.com/benedictbrady/shape-packing-challenge/blob/78a78626f098cd236f3a09bb2cb242f72951599d/src/semicircle_packing/geometry.py), [pinned scorer](https://github.com/benedictbrady/shape-packing-challenge/blob/78a78626f098cd236f3a09bb2cb242f72951599d/src/semicircle_packing/scoring.py).

**Structure and the limit reached by the search.**

There are **zero full-disk pairs**: no two pieces have a common disk centre and complementary orientations. Two near-antiparallel diameter contacts, **(1,14)** and **(4,8)**, slide along their flats by approximately **0.85303787** and **0.31901274** respectively. These displaced seams permit arrangements that rigid disks would not permit.

Nine pieces, **3,4,5,6,9,10,11,13,14**, put curved arcs near the rim, with their disk centres approximately R−1 from the MEC centre. Piece **12** points its curved side inward; its outward diameter forms a chord whose **two endpoints** approach the enclosing circle. The five interior pieces are **0,1,2,7,8**. The layout has no apparent rotational or mirror symmetry and is not a pair of exact concentric rings. At a boundary-distance tolerance of 1e-10, only **5,10,14** support the rounded MEC; at 3e-6, ten pieces are near the boundary. The checkers' longer lists of eight “tight supports” use a looser tolerance and should not be read as eight exact supports. [Evidence: b01-published, b11-angle-phase, b11-seam-integer, b13-best, b14-best; goal notes, episodes 3–4.]

Thirty of the 105 pairs have positive official polygon intersections, and 29 exceed 9e-7. Many contacts are therefore close to their allowed area. Several continuous local solves suggested radii around **2.94852655**, but their rounded coordinates failed validation or retained constraint residuals. Those are optimizer diagnostics, not attained scores. A coordinate step is 1e-6, larger than the approximately 4e-7 continuous radius gain being sought in that basin. This helps explain the local/grid stagnation; it does not prove optimality.

The seam-integer variant re-scored at **2.9485269509125516**, only 4.44e-16 below the published witness. It translates all centres by (−9,+7)×1e-6 and changes three angles while its supporting arcs move rigidly. That last-bit difference is floating-point noise, so the original published witness remains the delivered configuration. Newly generated archive and contact-release candidates were valid but worse. The best entirely fresh alternative across the campaign was the **relaxed ring candidate, 2.9535295831518282**, which abandoned exact ring radii. All of these are finite search outcomes, without a global optimum or topology-exclusion proof. [b11-seam-integer; b13-best; b14-best; b02-rings-312-411.]

**Official validity differs from true circular-area validity.**

The repaired scorer and its audit find six pairs whose true circular intersections exceed 1e-6 even though the official inscribed polygons pass. The maximum true area is **1.0013726918707471e-6**, on pair **(1,3)**. Thus this witness is **official-local valid**, but is neither a zero-overlap packing nor a packing satisfying a true-circular-area cap of 1e-6. The objective explicitly requires the official local scorer, which is the acceptance basis here. [b09-geometry, b10-geometry.]

| Pair | High-precision circular area | Official polygon area |
|---|---:|---:|
| (1,3) | 1.0013726918707471e-6 | 9.99594025502215e-7 |
| (1,13) | 1.0003480671110788e-6 | 9.985677175080334e-7 |
| (2,11) | 1.0007704081408313e-6 | 9.996466942502033e-7 |
| (3,9) | 1.0007205145887128e-6 | 9.995983747504195e-7 |
| (7,8) | 1.0001613924002808e-6 | 9.990352164717355e-7 |
| (8,9) | 1.0008169502959498e-6 | 9.996957770875582e-7 |

A separate rounded zero-overlap numerical witness from strict-homotopy has **R = 2.9486819093371306**, with minimum analytic separating gap **1.064544186135663e-7** across all 105 pairs. It misses the target. It is a floating-point feasible witness, not an interval certificate; its radius must not be substituted for the tolerant winner's score. The ideal zero-overlap area bound is √(15/2) ≈ 2.73861279. [b03-strict-homotopy.]

**Every search strategy.**

The campaign settled **45 items: 37 searches/reproductions and 8 scorer/verification items**. Five of the 50 item slots remained unused. All were accepted by the workflow, but acceptance alone does not certify their numerical claims. The following tables contain all 37 search items, plus one explicitly labelled nested alternative. Scores are official rounded radii as reported by their producers unless a separate check is named. A dash means unmeasured or no retained result; it never means zero or a proof of infeasibility. Source IDs resolve in the provenance table below.

Round 1 used fresh starts except for the public reproduction. “Strict comparison” preserves each report's definition; the column mixes unrounded solves, rounded separation witnesses and polygon-only diagnostics and is not a uniform ranking. Rows unavailable as direct inputs are preserved by root-1-01 and goal notes, episode 2.

| Item | Strategy | Best official R | Strict comparison | Qualification |
|---|---|---:|---:|---|
| repro/published | Public fork reproduction; greedy rounded-coordinate polish | 2.94852695 | — | Delivered tie; 1,428 polish trials found no gain; independently checked by b13/b14 |
| repro/penalty-lbfgs | Multistart L-BFGS with sampled separation penalties | 3.16365945 | 3.1636594507433955 | Producer report; unexplained source flag |
| repro/annealing | Simulated annealing, shifts/rotations/flips/swaps/reinsertion, SLSQP repair | 2.97206264 | 2.97206234 | Strict value is **unrounded**; one threshold comparison mismatch |
| repro/basin-hopping | Basin hopping with fixed-radius repair and shrink | 2.98929011 | 2.98936752 | Separate strict-run official figure 2.98936787 also reported |
| repro/hand-built | Disk, row and ring templates with SLSQP/grid polish | 2.96147487 | 2.961766702 | No full disks in winner |
| topo-r1/no-pairs | Free starts with centre-separation constraints and basin moves | 3.03051443 | 3.03050926 | Strict-search and rounded figures use different precision |
| topo-r1/symmetric | C3/C5/D3/D5/mirror starts, then symmetry release | 2.97035856 | 2.9706151362 | Winner **left symmetry family**; enforced C5 best 2.97281296 |
| topo-r1/flats-to-centre | Outward arcs with inward-facing flats | 2.96321390 | 2.96350083 | Eleven outer arcs, four interior pieces |
| topo-r1/rings-159-267 | 1+5+9 / 2+6+7 starts; asymmetric and mirror | 2.99381251 | 2.99397395 | Winner **left prescribed layers**; no prescribed-count rotational run reported |
| topo-r1/cma-es | CMA-ES with penalty model and SLSQP repair | 3.02081451 | 3.12147221 | Strict column is polygon-zero expanded diagnostic; source flag |
| topo-r1/flats-on-rim | Inward arcs with diameter endpoints on rim | 3.00113305 | 3.00133925 | Seven prescribed rim pieces plus eight free |
| topo-r1/rings-312-411 | Exact concentric 3+12 / 4+11; symmetry variants | 2.98539036 | 2.985694433212322 | Strict value **unrounded**; primary winner exact 4+11 before rounding |
| ↳ nested relaxed candidate | Release equal-radius ring constraints | 2.95352958 | — | Full R 2.9535295831518282; **left family**, not an additional item |
| topo-r1/diff-evolution | Differential evolution, local repair and shrink/grid polish | 3.04084534 | 3.04094273 | 17 of 22 configured runs interrupted; checkpoints retained |
| topo-r1/pairs-7-1 | Seven sliding pairs plus one single | 3.06352356 | — | Zero rigid disks in winner; one polygon-resolution mismatch |
| topo-r1/pairs-6-3 | Six sliding pairs plus three singles | 2.97726863 | 2.97747090 | Strict value **unrounded**; pairs slide, not rigid disks |
| topo-r1/pairs-5-5 | Five sliding pairs plus five singles | 2.95475629 | 2.95494101 | Best constrained fresh family; b02-pairs-5-5 |
| topo-r1/pairs-1-4 | One to four rigid full disks, other pieces free | 2.97438934 | 2.9746295021 | Winner uses one disk; strict figure is rounded comparison |

Every primary result in rounds 2 and 3 retained the same inherited **2.94852695** packing. These 20 primary scores are not 20 new discoveries. “New” below is the producer's best newly generated candidate in its separate new-candidate field; where fields omit non-improving trials, a dash means no retained/measured entry. Fresh-start columns track starts independent of the inherited coordinates. Warm alternative seeds carried from earlier rounds are not fresh starts in the later round.

| Round-2 item (master seed) | Method | Retained R | New R | Fresh R | Evidence/qualification |
|---|---|---:|---:|---:|---|
| polish-r2/polygon-slsqp (22001) | Official polygon constraints, active-set SLSQP and grid repair | 2.94852695 | 2.94852742 | 3.32748271 | Continuous improvement failed rounding |
| polish-r2/interior-point (22002) | Trust-constr with area constraints and integer repair | 2.94852695 | — | 3.31307952 | No validated improvement survived rounding |
| polish-r2/penalty-continuation (22003) | Increasing penalties, L-BFGS-B and SLSQP repair | 2.94852695 | 2.94852764 | 3.04517557 | New full R 2.9485276412344295 |
| polish-r2/coupled-grid (22004) | Joint 2–6 coordinate moves and integer probes | 2.94852695 | — | 5.14808050 | Sparse fresh starts test a local grid method |
| polish-r2/rigid-grid-phase (22005) | Rotation/translation before rounding; coupled integer repair | 2.94852695 | — | 5.90670800 | Fresh starts are sparse controls |
| polish-r2/contact-tangent (22006) | Contact-Jacobian nullspace/release and projection | 2.94852695 | 2.94852695 | 3.07070046 | New coordinates tie; strict rounded comparison 2.94868488 |
| polish-r2/strict-homotopy (22007) | Strict separation to tolerant area continuation | 2.94852695 | 2.94852695 | 3.04956887 | New grid tie; strict rounded witness 2.94868191 |
| moves-r2/reinsert-one (23001) | Gap-ranked one-piece reinsertion and joint repair | 2.94852695 | 2.94854102 | 3.03038767 | New-score array missing; unverified new claim |
| moves-r2/reinsert-block (23002) | Connected 2–3-piece reinsertion and polish | 2.94852695 | 2.94852695 | 3.29790142 | Tying descendant checked by moves-check-r2 |
| moves-r2/pi-flips (23003) | Single/double π flips, SLSQP and lattice repair | 2.94852695 | 2.94852894 | 3.01029057 | New-score array missing; unverified new claim |
| moves-r2/basin-small (23004) | Small perturbations with SLSQP repair | 2.94852695 | 2.94852982 | 3.01927618 | New checked by moves-check-r2; strict 2.94868491 |
| moves-r2/basin-wide (23005) | Wide basin moves, swaps, repair/compression | 2.94852695 | 2.94852854 | 2.95421813 | New checked by moves-check-r2; strict 2.94868666 |
| moves-r2/sliding-pairs (23006) | Small sliding-seam monotone moves | 2.94852695 | — | 6.45338247 | No strict decreases from baseline/pairs seed; weak compression |
| moves-r2/relaxed-rings (23007) | Boundary/core exchange with COBYLA repair | 2.94852695 | — | — | No new valid retained layout; short search and source flag |

The separate block-reinsertion figure **2.94853103** lacks its own coordinate witness and is not promoted to a verified result. Polygon SLSQP's strict rounded comparison is **2.9486827155047965**; the interior-point, continuation and grid items supply no strict witness. Full newly generated scores independently checked in round 2 were **2.9485285423028933** (wide basin), **2.9485298229650656** (small basin), and the block descendant tie. Those checks are preserved in the episode-3 notes and root-1-02; they are not new executions by this writer.

| Round-3 item (master seed) | Method | Retained R | New R | Fresh R | Evidence/qualification |
|---|---|---:|---:|---:|---|
| lattice-r3/seam-integer (33001) | Joint seam integer branches and polygon cuts | 2.94852695 | 2.94852695 | 3.07591093 | b13 checked new variant; last-bit difference is noise |
| lattice-r3/angle-phase (33002) | θ+2πk representatives and joint xy-grid repair | 2.94852695 | 2.94852733 | 3.06356374 | b13 checked new and fresh |
| topology-r3/ring-contact-release (33101) | Release contacts, nullspace moves, SLSQP repair | 2.94852695 | 2.94852836 | 3.04180845 | b14 checked new; fresh remains producer report |
| topology-r3/pair-release (33102) | Sequential five-pair release with annealing penalties | 2.94852695 | 3.34252870 | 3.34252870* | Same fresh candidate in both columns; warm repair failed |
| topology-r3/archive-basin (33103) | Contact-graph archive, wide basin hops, integer polish | 2.94852695 | 2.94852759 | 2.96599371 | b14 checked both; strict comparison 2.94868451649399 |
| topology-r3/boundary-core (33104) | Boundary/core swaps and separating-line SLSQP | 2.94852695 | — | — | No feasible repair in six runs, including two timeouts |

*Pair-release placed its fresh winner in `best_new` and left `best_fresh.score` null; the repeated number is an explicitly attributed reclassification, not a second measurement. It substituted simulated annealing when SLSQP was unavailable. Boundary/core's intermediate radii near 4.5 are origin-centred optimization diagnostics, not valid MEC scores. Neither result excludes its family. The two lattice items' strict figure 2.9486819093371306 is the inherited homotopy witness, not a new strict discovery.

The round-3 checked full radii are **2.9485273274133084** (angle new), **3.0635637448870696** (angle fresh), **2.9485275887783664** (archive new), **2.948528363861881** (ring new), and **2.9659937146857023** (archive fresh). Retained candidates were shared between rounds, with the published witness as fallback and fresh starts alongside it. b13 tested three distinct leaders plus the published witness; b14 likewise tested three challengers plus the published witness. Neither checker repaired or optimized the inputs.

**Scorer and verification ledger.**

| Item | One-piece assignment | Outcome |
|---|---|---|
| scorer-audit-r2/geometry | Audit reusable geometry scorer | Near-coincident double-counting defect found; superseded by b09/b10 |
| baseline-check-r2/published | Independently check published fallback | Executed clean-clone official check; 2.94852695; historical evidence in notes/root-1-02 |
| polish-check-r2/best | Check polish leaders | **Did not execute** official scoring; copied producer figures and supplied a wrong hash; excluded as certification |
| moves-check-r2/best | Check move leaders | Executed; baseline and selected challengers valid; its SVG has reversed halves and is excluded |
| geometry-fix-r3/geometry | Repair reusable scorer | b09 repaired area integration; source and tests embedded below |
| geometry-check-r3/geometry | Independently audit repaired scorer | b10 passed new fixtures and replay; no counterexamples |
| lattice-check-r3/best | Check lattice leaders | b13 executed; translated new variant is a numerical tie; baseline also passes |
| topology-check-r3/best | Check topology leaders | b14 executed; original published witness wins; chosen certificate and plot |

The repaired overlap routine partitions the intersection into disjoint vertical slices and integrates their circular/linear boundaries. Coincident centres use a sector formula; nonzero displacements use the slice calculation. This fixes the earlier approximate 3e-6 double count for `(0,0,0)` against `(1e-6,0,3.141593)`: the repaired area is **1.999999999999297e-6**. Its analytic mode uses actual circular boundaries; its compatible mode builds the official polygons. Its MEC exchanges finite boundary witnesses with analytic farthest points, returning a numerical upper/lower estimate and convergence status. These are binary64 numerical methods, not exact arithmetic or directed interval proofs. [b09-geometry.]

b09 tested **570 pair fixtures**, **40 packs**, **1,800 coordinate-rounding comparisons**, and reported **31 official repository tests passed**. b10 then used a separate reference and seeds: **296 raw pairs**, **33 packs**, **495 rounding comparisons**. It found worst analytic area error **5.612014475374415e-16** against a 65-digit reference, **zero compatible polygon area differences**, and maximum MEC radius difference **5.758504784125762e-12** from the official implementation. The analytic/official disagreements on the six published contacts are expected polygon bias, separate from the repaired defect. The audit did not author or modify the repair; it disclosed use of the supplied producer sources and added its own checks. The merged root's suggestion that the auditor was not independent is not supported by b10's actual independence statement.

b09 measured approximately **33.8 μs per analytic pair** versus **10.6 ms per polygon pair** on its fixtures. The own MEC gives **2.948526950912714** on the finalist. Compatible mode matches official overlap decisions but differs in the MEC's last digits; ranking uses the official score.

During this write-up, the preserved scorer and Decimal reference were executed in memory on **all 570 producer pair fixtures**: maximum absolute area difference **4.440892098500626e-16**. The own MEC converged, and the six analytic rejections reproduced. The writer also checked the solution's schema, precision, hashes, public-source equality and all 15 SVG arc endpoints/directions. **No new official-scorer execution is claimed in this write-up**; official numbers above are the retained independent checker evidence.

**Evidence corrections and limits.**

The primary b14/b10 measurements identify maximum polygon overlap at **(2,13)**; root-1-01's assignment to (13,14) is incorrect. Root-1-02's description of the seam variant as a 1e-5 shift is imprecise; the shift is (−9,+7)×1e-6. b13's prose incorrectly equates angle-phase's primary array with its new candidate; the primary is the published fallback. These corrections use the actual arrays and measurements.

Serialization alone explains several legitimate solution hashes, but not polish-check-r2's mismatch: its text actually hashes to `7fbff0f1f22ea7936d1b35fafb2334b9608d0b01e40029b67e00848e7d88c8aa`, not its claimed `cefac336…`. Its copied validity and unmeasured containment are excluded. The reversed moves-check-r2 plot is superseded by b14's correctly directed SVG; its numerical scoring evidence remains usable. The boundary-support and inward/outward wording are resolved in the structure description above.

The workflow flagged sources for repro/penalty-lbfgs, topo-r1/cma-es, moves-r2/relaxed-rings, scorer-audit-r2/geometry, polish-check-r2/best and topology-r3/pair-release. It supplied no specific reasons; this report does not invent them. The nonwinning figures remain attributed producer reports. Some searches were interrupted or had failed repairs; checkpoints and null results are distinguished from successes. The searches are not exhaustive and the prescribed ring counts were not explored under every possible symmetry.

There is **no goal-owned code repository or merged commit**: the handed `trunk` is `null`, and all 14 batches were research batches. The official repository and pinned commit above identify the scorer; the public fork and its pinned commit identify the reproduced packing. The embedded reusable scorer is a research output, not an unreported trunk build.

**Batch scope and decision record.**

The retained batch excerpts explicitly assign one method, one family, one scorer, or one verification report to each item. The full briefs are truncated in `goal.json`; the notes and returned schemas preserve their requested contents. This table records those per-item contracts rather than inventing new work or launching batches. All results are JSON; each numerical search was to return rounded poses and official validity/score, and each check was to disclose failures.

| Batch | Items | One item's work | Required contents recorded in notes/results |
|---|---:|---|---|
| repro | 5 | Reproduce/search with its assigned method | 15 poses, official/strict scores, structure, runs, scorer checks/source |
| topo-r1 | 12 | Search its assigned fresh topology | Poses/scores, family and departures, structure, runs and scorer checks |
| polish-r2 | 7 | Apply one assigned local/grid strategy | Inherited/new/fresh scores and poses, seeds, checkpoints, strict comparison, checks |
| moves-r2 | 7 | Apply one assigned move strategy | Same search evidence, distinguishing warm alternatives from fresh starts |
| scorer-audit-r2 | 1 | Audit one reusable scorer | Source, tests, official comparisons, threshold counterexamples and limitations |
| baseline-check-r2 | 1 | Certify the published fallback | Tested JSON/hash, full/eight-decimal score, MEC, areas, containment, plot, independence |
| polish-check-r2 | 1 | Certify polish leaders plus fallback | Same certificate fields; execution and failures disclosed |
| moves-check-r2 | 1 | Certify move leaders plus fallback | Same certificate fields; no optimization |
| geometry-fix-r3 | 1 | Repair the identified scorer defect | Repaired source/tests, hashes, regression and random/tight/rounding checks |
| geometry-check-r3 | 1 | Audit that repair | New reference checks, counterexamples/errors, gate and independence statement |
| lattice-r3 | 2 | Run one assigned lattice strategy | Baseline/new/fresh arrays and scores, seeds, source, checkpoints and checks |
| topology-r3 | 4 | Run one assigned topology-release strategy | Same search fields, explicit failed repairs and family departures |
| lattice-check-r3 | 1 | Certify lattice leaders | Deduplicated top candidates plus baseline, exact bytes/hash, scores/MEC/areas/plot |
| topology-check-r3 | 1 | Certify topology leaders | Same certificate fields; choose the lowest actually passing candidate |

The closing decision is one JSON object in the supplied reference's shape. It records the completed campaign and tie deliverable, with no further work proposed.

<!-- file: decisions.json bytes: 746 sha256: ecfb452d260fd251f0f7f0a25c02c4d693a7bcee9898b700ab3522225a9757da encoding: utf8 -->
```json
{
  "notes": "Close the settled campaign: 45 accepted items comprise 37 searches/reproductions and 8 scorer/check items. Deliver the published witness independently scored by topology-check-r3/best at 2.948526950912552, below the literal 2.94853 target but a published tie, not a novel record. Use its exact solution bytes and correctly oriented plot. Preserve every strategy result, disclose true-area threshold disagreements and exclude unexecuted certification. The scorer repair passed its later audit. No pending work or code trunk; five item slots unused. No submission or sign-in. This is the closing record for the single-file write-up, not a request for further actions.",
  "spawn": [],
  "read": [],
  "cancel": [],
  "finish": true
}

```

**Recovering the delivered files.**

Each marked fenced block contains a file payload. The test harness is gzip/base64 encoded to fit this single report; the other payloads are plain UTF-8. To extract all six files, save this report and run the following standard-library Python recipe from a directory where you want a new `packing-delivery` folder. It validates every digest before writing and refuses to overwrite existing files. Copying just the JSON array is also sufficient to score the packing, though formatting changes its byte hash.

```python
from pathlib import Path
import base64
import gzip
import hashlib
import re

report = Path("report.md").read_bytes()
pattern = rb"(?m)^<!-- file: ([a-zA-Z0-9_.-]+) bytes: ([0-9]+) sha256: ([0-9a-f]{64}) encoding: (utf8|gzip-base64) -->\n```[^\n]*\n(.*?)\n```"
payloads = {}
for match in re.finditer(pattern, report, re.S):
    name = match[1].decode("ascii")
    data = match[5]
    if match[4] == b"gzip-base64":
        data = gzip.decompress(base64.b64decode(data))
    assert name not in payloads and Path(name).name == name
    assert len(data) == int(match[2]), name
    assert hashlib.sha256(data).hexdigest() == match[3].decode("ascii"), name
    payloads[name] = data
assert set(payloads) == {
    "solution.json", "official-score.json", "plot.svg", "decisions.json",
    "geometry_scorer.py", "geometry_test.py"
}
target = Path("packing-delivery")
target.mkdir(exist_ok=False)
for name, data in payloads.items():
    with (target / name).open("xb") as output:
        output.write(data)
print("Extracted", len(payloads), "files with verified SHA-256 digests")
```

For an optional official replay, clone the official repository into a separate working directory, checkout the pinned commit, run `uv sync`, and run `uv run python run.py` on its unchanged sample first. Then pass the extracted solution's path to `uv run python run.py <solution-path> --save-plot <plot-path>`. From that clone, the following API call produces eight decimals (set the path to the extracted file):

```python
from run import _load_solution
from semicircle_packing.scoring import validate_and_score
result = validate_and_score(_load_solution("../packing-delivery/solution.json"))
assert result.valid, result.errors
print(repr(result.score), f"{result.score:.8f}", result.mec)
```

`geometry_scorer.py` is the unchanged b09 source. Python 3.10+ alone runs its analytic mode: `python3 geometry_scorer.py solution.json --mode analytic`. The finalist intentionally returns six analytic overlap rejections. To compute its own radius regardless of overlaps, import `exact_mec` and `placement` and call `exact_mec([placement(row, True) for row in rows])`; inspect `converged` and `gap`. Compatible mode needs **NumPy and Shapely**. The unchanged `geometry_test.py` additionally needs a synced pinned official checkout; run it through that checkout's Python with `--official-dir <checkout-path>`. The full official replay and full harness are **not an offline dependency bundle**; this report installs or vendors no third-party packages. Its payload extraction and analytic calculations require no network. The retained official checks establish the recorded score independently of any future dependency installation.

**Exact file payloads.**

`solution.json` — the selected b14 bytes; indices match the plot.

<!-- file: solution.json bytes: 700 sha256: 57135c157acfa62d0b5f833d0dc111f8c6b12324841fc01fb21d52f2295a6c77 encoding: utf8 -->
```json
[{"x":0.545425,"y":0.672150,"theta":-0.570778},{"x":1.135484,"y":-1.238740,"theta":2.227365},{"x":-0.584124,"y":-0.217653,"theta":-1.671787},{"x":1.843118,"y":0.631801,"theta":-0.722762},{"x":0.278186,"y":1.928675,"theta":2.264578},{"x":-0.723715,"y":1.809349,"theta":3.126118},{"x":-1.624637,"y":1.076193,"theta":-2.992325},{"x":-0.569810,"y":0.785952,"theta":-1.682231},{"x":0.032918,"y":1.724683,"theta":-0.877015},{"x":1.261991,"y":1.484613,"theta":0.453135},{"x":-1.944933,"y":-0.121111,"theta":-2.464295},{"x":-1.573106,"y":-1.149938,"theta":-1.641622},{"x":1.049635,"y":-2.567295,"theta":1.958950},{"x":-0.789401,"y":-1.781407,"theta":-0.792106},{"x":1.811166,"y":-0.718041,"theta":-0.914204}]
```

`official-score.json` — a compact certificate transcription from the successful checks, with the true-area distinction retained.

<!-- file: official-score.json bytes: 1593 sha256: a6bc7c99687613f5233ad626bbb194941f1ce225fdf18416d7a661c2a3679e4c encoding: utf8 -->
```json
{
  "official_valid": true,
  "official_score_full": 2.948526950912552,
  "official_score_8dp": "2.94852695",
  "cli_score_6dp": "2.948527",
  "mec": {
    "cx": -0.0001819080616875258,
    "cy": 0.00013448997007248039,
    "radius": 2.948526950912552
  },
  "max_polygon_pair_area": 9.997822348073146e-07,
  "max_polygon_pair": [
    2,
    13
  ],
  "max_containment_excess": 1.98507876802978e-13,
  "solution_sha256": "57135c157acfa62d0b5f833d0dc111f8c6b12324841fc01fb21d52f2295a6c77",
  "solution_bytes": 700,
  "official_repository": "https://github.com/benedictbrady/shape-packing-challenge",
  "official_commit": "78a78626f098cd236f3a09bb2cb242f72951599d",
  "verification_result": "topology-check-r3/best",
  "verification_execution_status": "executed",
  "verification_errors": [],
  "corroborating_verification_result": "lattice-check-r3/best (published baseline entry)",
  "published_source": "https://raw.githubusercontent.com/rorz/shape-packing-challenge/d27ef1e3b9cbaeeb998c25fc8b76ae1d54ec3a79/solution.json",
  "result_kind": "published tie/reproduction; no new record",
  "literal_target": 2.94853,
  "approximate_margin_below_literal_target": 3.049087448e-06,
  "improvement_over_published": 0,
  "true_circular_area_threshold_valid": false,
  "true_circular_area_exceeding_pairs": [
    [
      1,
      3
    ],
    [
      1,
      13
    ],
    [
      2,
      11
    ],
    [
      3,
      9
    ],
    [
      7,
      8
    ],
    [
      8,
      9
    ]
  ],
  "max_true_circular_pair_area": 1.0013726918707471e-06,
  "writeup_reexecuted_official_scorer": false
}

```

`plot.svg` — the selected b14 figure; unit radius maps to 60 pixels, with the y-axis reflected for display.

<!-- file: plot.svg bytes: 3072 sha256: c1da0959768c984d138ee0bbec3c1e5ae39a761948bd1a5e1b665fd41bd54ce4 encoding: utf8 -->
```svg
<svg xmlns="http://www.w3.org/2000/svg" width="372" height="372" viewBox="0 0 372 372"><rect width="100%" height="100%" fill="white"/><circle cx="185.99" cy="185.99" r="176.91" fill="none" stroke="red" stroke-width="1.5"/><path d="M186.31,196.16 A60,60 0 0 0 251.14,95.18 Z" fill="#9cf" fill-opacity="0.6" stroke="#036" stroke-width="1"/><text x="241.4" y="164.3" font-size="12" text-anchor="middle">0</text><path d="M301.65,223.70 A60,60 0 0 0 206.60,296.95 Z" fill="#9cf" fill-opacity="0.6" stroke="#036" stroke-width="1"/><text x="237.6" y="242.9" font-size="12" text-anchor="middle">1</text><path d="M91.26,193.01 A60,60 0 0 0 210.65,205.11 Z" fill="#9cf" fill-opacity="0.6" stroke="#036" stroke-width="1"/><text x="148.2" y="229.9" font-size="12" text-anchor="middle">2</text><path d="M256.90,193.09 A60,60 0 0 0 336.27,103.09 Z" fill="#9cf" fill-opacity="0.6" stroke="#036" stroke-width="1"/><text x="316.8" y="170.0" font-size="12" text-anchor="middle">3</text><path d="M248.82,31.91 A60,60 0 0 0 156.56,108.65 Z" fill="#9cf" fill-opacity="0.6" stroke="#036" stroke-width="1"/><text x="185.4" y="53.5" font-size="12" text-anchor="middle">4</text><path d="M143.51,17.45 A60,60 0 0 0 141.65,137.43 Z" fill="#9cf" fill-opacity="0.6" stroke="#036" stroke-width="1"/><text x="115.6" y="81.0" font-size="12" text-anchor="middle">5</text><path d="M79.60,62.10 A60,60 0 0 0 97.44,180.76 Z" fill="#9cf" fill-opacity="0.6" stroke="#036" stroke-width="1"/><text x="61.8" y="129.4" font-size="12" text-anchor="middle">6</text><path d="M92.18,132.17 A60,60 0 0 0 211.44,145.52 Z" fill="#9cf" fill-opacity="0.6" stroke="#036" stroke-width="1"/><text x="148.8" y="169.7" font-size="12" text-anchor="middle">7</text><path d="M141.85,120.89 A60,60 0 0 0 234.11,44.15 Z" fill="#9cf" fill-opacity="0.6" stroke="#036" stroke-width="1"/><text x="205.2" y="107.3" font-size="12" text-anchor="middle">8</text><path d="M287.99,150.87 A60,60 0 0 0 235.45,42.98 Z" fill="#9cf" fill-opacity="0.6" stroke="#036" stroke-width="1"/><text x="286.0" y="89.1" font-size="12" text-anchor="middle">9</text><path d="M31.70,146.51 A60,60 0 0 0 106.91,240.02 Z" fill="#9cf" fill-opacity="0.6" stroke="#036" stroke-width="1"/><text x="48.3" y="214.2" font-size="12" text-anchor="middle">10</text><path d="M31.76,250.75 A60,60 0 0 0 151.46,259.24 Z" fill="#9cf" fill-opacity="0.6" stroke="#036" stroke-width="1"/><text x="89.7" y="285.9" font-size="12" text-anchor="middle">11</text><path d="M304.51,317.33 A60,60 0 0 0 193.44,362.75 Z" fill="#9cf" fill-opacity="0.6" stroke="#036" stroke-width="1"/><text x="238.8" y="319.0" font-size="12" text-anchor="middle">12</text><path d="M95.93,335.03 A60,60 0 0 0 181.35,250.74 Z" fill="#9cf" fill-opacity="0.6" stroke="#036" stroke-width="1"/><text x="157.6" y="316.1" font-size="12" text-anchor="middle">13</text><path d="M247.15,265.71 A60,60 0 0 0 342.19,192.46 Z" fill="#9cf" fill-opacity="0.6" stroke="#036" stroke-width="1"/><text x="311.2" y="254.5" font-size="12" text-anchor="middle">14</text><text x="5" y="14" font-size="12">R=2.94852695</text></svg>
```

`geometry_scorer.py` — b09's repaired scorer, unchanged, SHA-256 `c066a965ea2c847709dc9c509ab4ad9ab0dd95d1a131cfca16402f57af36fed9`.

<!-- file: geometry_scorer.py bytes: 11817 sha256: c066a965ea2c847709dc9c509ab4ad9ab0dd95d1a131cfca16402f57af36fed9 encoding: utf8 -->
```python
"""Unit-semicircle geometry. Triples are (disk-center x, y, curved-side radians)."""
import argparse
from dataclasses import asdict, dataclass
from itertools import combinations
import json
import math
import random

OVERLAP_TOL = 1e-6
ARC_POINTS = 4096


def placement(row, round6=False):
    """Parse a triple or placement object and optionally round as in run.py."""
    if isinstance(row, dict):
        row = (row["x"], row["y"], row["theta"])
    x, y, theta = map(float, row)
    if not all(map(math.isfinite, (x, y, theta))):
        raise ValueError("placements must be finite")
    if round6:
        return round(x, 6), round(y, 6), round(theta, 6)
    return x, y, theta


def _root(x):
    """Half-chord height, factored for stability at the rim."""
    x = min(abs(x), 1.0)
    return math.sqrt((1.0 - x) * (1.0 + x))


def _root_integral(a, b):
    """Integral of sqrt(1-x*x) on [a,b], using a local angle difference."""
    a, b = max(-1.0, a), min(1.0, b)
    if a >= b:
        return 0.0
    ca, cb = _root(a), _root(b)
    width = b - a
    dot = a*b + ca*cb
    cross = width * (1.0 + dot) / (ca + cb) if a*b > 0 else b*ca - a*cb
    angle = math.atan2(cross, dot)
    # For tiny circular caps, avoid subtracting two nearly equal O(angle) terms.
    if angle < 0.05:
        s = angle*angle
        angle_minus_sin = angle*s*(1/6 - s*(1/120 - s*(1/5040 - s/362880)))
    else:
        angle_minus_sin = angle - math.sin(angle)
    one_plus_cos_sum = ((ca + cb)**2 + width**2) / 2.0
    return (angle_minus_sin + one_plus_cos_sum*math.sin(angle)) / 2.0


def _sweep_frame(delta, unit, na, nb):
    # The normals' y components must stay away from zero to bound both slopes.
    h = math.sqrt(0.5)
    candidates = [(1., 0.), (0., 1.), (h, h), (-h, h)]

    def to_frame(p, basis):
        x, y = p
        c, s = basis
        return c*x + s*y, c*y - s*x

    basis = max(candidates, key=lambda v: min(abs(to_frame(n, v)[1])
                                              for n in (na, nb)))
    return [to_frame(v, basis) for v in (delta, unit, na, nb)]


def exact_overlap_area(a, b):
    """True intersection area for unrounded triples, computed in binary64."""
    ax, ay, at = a
    bx, by, bt = b
    dx, dy = bx-ax, by-ay
    distance = math.hypot(dx, dy)
    if distance >= 2.0:
        return 0.0
    na = math.cos(at), math.sin(at)
    nb = math.cos(bt), math.sin(bt)
    if distance == 0:
        # Shared disk: half of the angular width of the intersecting sectors.
        cross = na[0]*nb[1] - na[1]*nb[0]
        dot = na[0]*nb[0] + na[1]*nb[1]
        return 0.5*math.atan2(abs(cross), -dot)

    # Divide by the largest component before normalizing even subnormal offsets.
    scale = max(abs(dx), abs(dy))
    ux, uy = dx/scale, dy/scale
    norm = math.hypot(ux, uy)
    (dx, dy), (_, uy), na, nb = _sweep_frame((dx, dy), (ux/norm, uy/norm), na, nb)
    centres = ((0.0, 0.0), (dx, dy))
    lo, hi = max(-1.0, dx-1.0), min(1.0, dx+1.0)
    if lo >= hi:
        return 0.0
    cuts = [lo, hi]

    def split(x):
        if lo < x < hi:
            cuts.append(x)

    # Split at every support crossing to keep the envelope fixed per slice.
    height = math.sqrt(max(0.0, (1.0-distance/2)*(1.0+distance/2)))
    split(dx/2 - height*uy)
    split(dx/2 + height*uy)

    lines = []
    for (lx, ly), (nx, ny) in zip(centres, (na, nb)):
        slope = -nx/ny
        intercept = ly - slope*lx
        lines.append((slope, intercept, ny > 0.0))
        norm = math.hypot(nx, ny)
        for cx, cy in centres:
            signed = (cx-lx)*nx + (cy-ly)*ny
            offset = signed/norm
            if abs(offset) <= 1.0:
                foot_x = cx - offset*(nx/norm)
                extent = _root(offset)*(ny/norm)
                split(foot_x - extent)
                split(foot_x + extent)
    ma, qa, _ = lines[0]
    mb, qb, _ = lines[1]
    if ma != mb:
        split((qb-qa)/(ma-mb))

    cuts = sorted(set(cuts))
    pieces = []
    for left, right in zip(cuts, cuts[1:]):
        mid = left + (right-left)/2
        upper, lower = [], []
        for cx, cy in centres:
            height = _root(mid-cx)
            upper.append((cy+height, cy, cx, 1))
            lower.append((cy-height, cy, cx, -1))
        for slope, intercept, is_lower in lines:
            y = slope*mid + intercept
            (lower if is_lower else upper).append((y, y, 0., 0))
        up, up_base, up_x, up_sign = min(upper)
        down, down_base, down_x, down_sign = max(lower)
        if up > down:
            chord = (up_sign*_root_integral(left-up_x, right-up_x)
                     if up_sign else 0.0)
            bottom = (down_sign*_root_integral(left-down_x, right-down_x)
                      if down_sign else 0.0)
            area = math.fsum(((up_base-down_base)*(right-left), chord, -bottom))
            pieces.append(max(0.0, area))
    return min(math.pi/2, math.fsum(pieces))


def polygon(sc):
    """Construct exactly the pinned scorer's 4096-point polygon."""
    import numpy as np
    from shapely.geometry import Polygon
    x, y, theta = sc
    angles = np.linspace(theta-math.pi/2, theta+math.pi/2, ARC_POINTS)
    return Polygon(list(zip(x + np.cos(angles), y + np.sin(angles))))


def polygon_overlap_area(a, b):
    if math.hypot(a[0]-b[0], a[1]-b[1]) > 2.0:
        return 0.0
    return polygon(a).intersection(polygon(b)).area


def _farthest(sc, q):
    x, y, nx, ny = sc
    dx, dy = x-q[0], y-q[1]
    length = math.hypot(dx, dy)
    if length == 0.0:
        return (x+nx, y+ny), 1.0
    if dx*nx + dy*ny >= 0.0:
        return (x+dx/length, y+dy/length), length+1.0
    tx, ty = -ny, nx
    if dx*tx + dy*ty < 0.0:
        tx, ty = -tx, -ty
    return (x+tx, y+ty), math.hypot(dx+tx, dy+ty)


def farthest_point(sc, q):
    x, y, theta = sc
    return _farthest((x, y, math.cos(theta), math.sin(theta)), q)[0]


def _dist(a, b):
    return math.hypot(a[0]-b[0], a[1]-b[1])


def _pair(a, b):
    return ((a[0]+b[0])/2, (a[1]+b[1])/2), _dist(a, b)/2, (a, b)


def _triple(a, b, c):
    ux, uy = b[0]-a[0], b[1]-a[1]
    vx, vy = c[0]-a[0], c[1]-a[1]
    det = 2*(ux*vy - uy*vx)
    if abs(det) <= 8*math.ulp(1.0)*math.hypot(ux, uy)*math.hypot(vx, vy):
        return max((_pair(p, q) for p, q in combinations((a, b, c), 2)),
                   key=lambda circle: circle[1])
    uu, vv = ux*ux + uy*uy, vx*vx + vy*vy
    x, y = (vy*uu-uy*vv)/det, (ux*vv-vx*uu)/det
    return (a[0]+x, a[1]+y), math.hypot(x, y), (a, b, c)


def _point_circle(points, eps):
    points = list(points)
    random.Random(42).shuffle(points)
    centre, radius, support = points[0], 0.0, (points[0],)
    for i, a in enumerate(points):
        if _dist(a, centre) <= radius+eps:
            continue
        centre, radius, support = a, 0.0, (a,)
        for j in range(i):
            b = points[j]
            if _dist(b, centre) <= radius+eps:
                continue
            centre, radius, support = _pair(a, b)
            for k in range(j):
                c = points[k]
                if _dist(c, centre) > radius+eps:
                    centre, radius, support = _triple(a, b, c)
    return centre, radius, support


def _support_bound(q, points):
    """Lower bound from the variance of a boundary-point distribution."""
    if len(points) < 2:
        return 0.0
    if len(points) == 2:
        return _dist(*points)/2
    a, b, c = points
    ux, uy = b[0]-a[0], b[1]-a[1]
    vx, vy = c[0]-a[0], c[1]-a[1]
    det = ux*vy - uy*vx
    if det == 0.0:
        return max(_dist(p, r)/2 for p, r in combinations(points, 2))
    x, y = q[0]-a[0], q[1]-a[1]
    wb, wc = (x*vy-y*vx)/det, (ux*y-uy*x)/det
    weights = [max(0., w) for w in (1.-wb-wc, wb, wc)]
    total = math.fsum(weights)
    weights = [w/total for w in weights]
    return math.sqrt(math.fsum(weights[i]*weights[j]*_dist(points[i], points[j])**2
                               for i, j in combinations(range(3), 2)))


@dataclass(frozen=True)
class MEC:
    x: float
    y: float
    radius: float
    lower_bound: float
    gap: float
    point_residual: float
    iterations: int
    converged: bool
    numerical_padding: float


def exact_mec(shapes, atol=2e-12, max_iterations=80):
    """MEC via finite point exchange and an analytic farthest-point oracle.

    Radius is an upper estimate at the reported centre. A witness distribution
    gives a lower estimate. The bracket has a floating-point safety allowance,
    not directed-rounding certification. Inspect converged/gap before claiming
    the requested accuracy.
    """
    shapes = list(shapes)
    if not shapes or not math.isfinite(atol) or atol <= 0 or max_iterations < 1:
        raise ValueError("expected nonempty shapes, positive atol and iterations")
    ox, oy, _ = shapes[0]
    local = [(x-ox, y-oy, math.cos(t), math.sin(t)) for x, y, t in shapes]
    scale = max(1., *(abs(v) for p in local for v in p[:2]), abs(ox), abs(oy))
    if not scale < 1e90:
        raise ValueError("coordinates outside the MEC numerical range")
    # Account for rounding of the world-coordinate centre.
    padding = 32*math.ulp(scale)
    points = []
    for x, y, nx, ny in local:
        points.extend(((x-ny, y+nx), (x+ny, y-nx), (x+nx, y+ny)))
    lower = 1.0
    upper = math.inf
    for iteration in range(1, max_iterations+1):
        q, sample_radius, support = _point_circle(points, 4*math.ulp(scale))
        lower = max(lower, _support_bound(q, support)-padding)
        world = ox+q[0], oy+q[1]
        relative_q = world[0]-ox, world[1]-oy
        far = [_farthest(sc, relative_q) for sc in local]
        current = max(distance for _, distance in far)
        if current+padding < upper:
            upper, best = current+padding, world
            residual = max(0., current-sample_radius)
        gap = upper-lower
        if 0 <= gap <= atol:
            break
        additions = [p for p, d in far if d > sample_radius and p not in points]
        if not additions:
            break
        points.extend(additions)
    return MEC(*best, upper, lower, gap, residual, iteration, 0 <= gap <= atol,
               padding)


def score(rows, mode="analytic", round6=True):
    """Validate a 15-pack. Mode selects overlap only; both modes use analytic MEC."""
    if mode not in ("analytic", "compatible"):
        raise ValueError("mode must be analytic or compatible")
    shapes = [placement(row, round6) for row in rows]
    if len(shapes) != 15:
        return {"valid": False, "score": None, "mec": None, "overlaps": [],
                "error": f"expected 15 semicircles, got {len(shapes)}"}
    cache = {}
    overlaps = []
    for i, j in combinations(range(15), 2):
        a, b = shapes[i], shapes[j]
        if _dist(a, b) > 2.0:
            continue
        if mode == "analytic":
            area = exact_overlap_area(a, b)
        else:
            for k in (i, j):
                if k not in cache:
                    cache[k] = polygon(shapes[k])
            area = cache[i].intersection(cache[j]).area
        exceeds = area >= OVERLAP_TOL if mode == "analytic" else area > OVERLAP_TOL
        if exceeds:
            overlaps.append((i, j, area))
    if overlaps:
        return {"valid": False, "score": None, "mec": None, "overlaps": overlaps}
    mec = exact_mec(shapes)
    return {"valid": True, "score": mec.radius, "mec": asdict(mec), "overlaps": []}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("solution")
    parser.add_argument("--mode", choices=("analytic", "compatible"), default="analytic")
    parser.add_argument("--unrounded", action="store_true")
    args = parser.parse_args()
    with open(args.solution) as source:
        print(json.dumps(score(json.load(source), args.mode, not args.unrounded), indent=2))

```

`geometry_test.py` — b09's original deterministic test harness and 70-digit Decimal reference, unchanged, SHA-256 `34b92ada72d9699ac741f69dfc31f365b96e2a0ec85983364300072802671fba`. b10's separate audit results are summarized above; this file is the producer harness, not b10's independent test suite.

<!-- file: geometry_test.py bytes: 18075 sha256: 34b92ada72d9699ac741f69dfc31f365b96e2a0ec85983364300072802671fba encoding: gzip-base64 -->
```text
H4sIAAAAAAACA608a4+jSJLf61dwSCeBjSnzsI1Lw+jmtmfvWlrttnbm7ovPQhjSLroxsICry93q
/34RkZmQYFzdc3ulaRsyIyMjI+Od6dF1/ddXllza+JAzLb6kWavFpzgrmlZrn5lWZUXBUi0vkzjX
qrr8yBIAKFIt1t6xJDtD63/UjBVaWcdJzmxd1x+yc1XWAFWfqrhu2MOxLs9aUuY5jM3KotEEwJ/K
S9GymvencQsI4qZhXX/cpFnSim4xmeiSc8eN9s7i1CUlIHsV4MdLkbRlmXe48voSJXHyLKjJYN5B
f1KeD1kRE30WLjS9yKmruH3Os4OE/ACvcokfm7KQz2elvQYOlWc+vGXn6pgBc0Xf7wy/4/r6LquB
IWV9FXDZuYOpWH2MEsEe3n1i5Zm19TVqkrJmtYQ0/vbfv/79L798iH7/218sjb3GSRudWSIfyxdW
53EVxTWLYVl5nLAzK1rrQXvrryrz66ksRqNpYvPh4cP7v2qhpm+CeBOs3fVxuQ2S1PXWRy9ebg8H
Nzm4vnvcuNuVs9puU/3h33/97XcYsaNJjaW98le+u7K0pb3euA48LKBts9xsAtPSDMd2vJUf+NDs
2K4XbODJtV13461XJifcwAGB77g+jXWdzXrlEfx642yCDUcT+J7jBDSN5wRLh2A3gGjtSjwwdhM4
wdrSHHvrBuvNiuZa+ytOCw3wNkgj4FtuPX9raZ7tuGvA3BED07r+2tsg0HKzdrZIi2tvt67nrgSa
1XobOEjLJlhtVy4nNnBdz+lpWXruFgl2YFJ/HXhEcLDZLJ0VXxFMu906CAD8WTse4vNXHvBLoWXr
+1uPj3VcB/6IGH/tw4YQMQ4w23OWa6LB8bdbL+Dk+M7a7VgDS/G3a29Fo1dr3E7i0irYyjVtgq1P
bAWCA8dfbjiHty4g79EEQMJ6zbtgG3y+D1vHd5c+QO0ffvmvd+9/jz788v7vv4GUfBXjgM/mEzJ0
6Xgbdw2MWfvAr4At1hZ1O7J/6fnBEjbe2Wy2qzX2cxTAZMeRMMBFL1jDWpfAWY4DeLTtut3lylu5
wQrkcdWjgBUFEsQBhsPeubCta49jCBQMgbPegpg5gee5PmH4BpoCC3pn6CAxPuiCC1IK7NtsPRBr
H1TH97zAc4HqpRuAOG83iANo3Kyc5Spwl9uND7sJA70lMHjtL9cgo+4y2G7hK9DNh18//MZncGBG
FxoeHv6ts3TGOX5tsi8s9JfbtfmQsqPWZEVSNkZrPtH6WhhstPMP703tX4FfM3ig9uwIXT9py6fO
TLTaPNQQQIxbhJp4BmsJ1iaFrxS+C3aKmn9cwGAA6tYC0kC++4dFO2tp1Cfodujp8zPaRiDViA+N
kTYARQ+JaWo/a7DAnoi00WahOsWjZgDVn8wZfs4d0+xBk2nQhcOBFVBcAFDTzHENyTxNup5PuGhO
Zc3aS10QLPAYWQnuqnCNq6W9CmYC065DpolBCw66IFgJ+joJ+uH9osO7UIHDcBL60eXTsrxhwOKl
2VPys/Y6OUBM8GppVw79BRZ/fXyl52NZa5GWFejATszwzR7FF+0RmDE3nPmX2RfTbv5RtwZHAD7q
bGkvcX5hFm3sFwv/85TtxR1FsJstxUbcqQUg7RoJFfIeex8/DffDVffDWc8IWOxJWrYGOKqDIFsA
xbvlfnaAj3m8c/DJ2Qv4pC6b5v4IZ78QI5ZyRHM5tBDo3JtmgaAgwDhUmacoawhWOrWTEieVUcUC
OtSIURl6f1heY+SlpT1n4NNfwHc3AgvEbA16VeycNRALsNT4+kJb+IJbyIFRGPIShO0F/j1n30zE
tFdn/JJVBuKyCOPOedqbUsTrJKrLsm2MF9BhCOeYXME5PsHUyG7oeRlIQ4bLbQkCKKGN5yNh66Hx
RiZ3nJjqOQOMXDZfgHOAFljJUZbHY8ParhttBco6GGBAuBDoZ/gyFy+Soo5sdcE7mGveZKdixhHP
sXWGxo2Yhz3IP3CU4EBMaqNxnVosXHROcnN54KsKBMTA72HvTnXcMi3Js6piqQVwGWwIxNLA1oZC
6DSLIaRjNby12mbZBbVpdsrahkJpUqGsfR6EuIaJcW/SKgoOL3YF4SQwabPsWpEmtMOXKkdvUBkQ
K8cmckVtOajG8Dk7Iqc7OT/giH4aWEHNUOwMsQX4CV80rocDNuUExidqO/fCuUnsjXcu7PIBPpX5
uaY0A6J5myWQKsBC1OLiavD5nwZhbWFpZ0AkUA66pMqSPKGMckuAI3A1C5Rs/vLoqtNhO00lV6z9
HGr+0xTuzhqTmfucJYzCaHLXSg/yI+tFyx2t4SP6yUU2aOObIPgBLhdAxL7ssr1kEz2Kpe+Ewsu/
EhK7uufM7uOwO1X3X04mZ/i4NwfAkFIUTNgCFHJEPYRIs+ZTD5CqHMU/YaZCxdqkuAMwytTmSiuh
hh6acTgFMhEEpEY+9laTGLFAnyeYMufPAyuq/l06nhhGPq+BUvMGRgjBBVei/RRyQrk282bOAZQL
Tuli4O/UvwZITvLeEeTmNBgsOql7sHoaTBEx8JL1Igfm8U1DZ2Y09aLJTW0h28CtgdAvEph0uB3I
A7K/iwLd3kCy0Z7xnWSTWw3MQWVCOGIOhqdUK4BGvm2i9WmKrxlGOQ56DaF+gpWDQGmgCGAOswK8
v9oY52VxAvXMUkUsmWkJZ08v0wK4208tBhER2c4tESiYaAudBULNCFT1hbfT2GC+WZEaxoLoXCAG
YDW9zPHFvOEocvPpHroYfAug46L2SIz/Ac14B77NlDH5XXU4Z2gJhCZMbZgBEHMi3ZzN3DnxYOYS
r2jbiag5EjVDXKgSd5VhKL58r6TtYeDcQaDNcejQBwL9aNRZ1S9Hx7gGMWrQbscVgyiHIt+nf9Kz
gtaD70jYSG4ofoAJGojfYdY2Rr7ziYfL7kKad0bzai7eGa+0H80Vn6/DPSx6s/TOIKy3QoJyznGC
1SfrM6EzHdFSbNRR/FuKLyRTQyWBBOMHEE5hnDtzd9b72J7KLkq72dhjXsYtxXndDGa3rQcsQYKR
KT83wwB8h9VCA8NZQ3/VLU2/4gcxTAfuwgCTxx/wRB4XMMgg7pi9Ag7WGBJlgQEuL+PZf6cvw9tA
7u1sOLXXjOWppsNYoAbmMZY2VmPwH9VqqECA7yL39/iwhlVxzauMKDkIMDOcpT2bMSKNKVGmg1Ui
zzS5eKVULVQHYsHRrjJ0aUt77XcNHL4LwQgW6EF0AqKnqmtaIMSye52LV0Ds7LvUEIwneDgK30SF
1FAWZCk0dtFaLzSCYwWL60hEE7d8S2dEAPq5C7yLV/B89CoizFHM5KyXyjQxqF8M6heDjKXwnMLz
ATVtB3tqX4oMRp/V2F7Jd9dmr8oNWAX0IAaW2LDyRZVBKs6tzF0GEa2/H6+NywuuqqdiJjhqUuuc
0M5S6pYvRGEH13ObwmSaeCH2z8UX2hs1UOxj6pFYSJRDzRXEtrjkIskmt4G/KPzO4wMDRwJK3iim
zegQGzpGavBPp0rllgqpZk+CNYI85jGpjc3LiiafWQFCgA7KZYsNCfH6BuWID8cYS+pEm73dWhp8
8BmWyyX/dkbswJC8X/2gi+fd0I/LvvGriuB4/oT/5N6znD9nU/4zPpQvKF/c1vVJZMd7bugxbeZr
mimV/ilvLBDinLhX2r+EmsJEc9rt5iUGSbfRxaS5xz9ix3DAQV2nQvyQyzz3Ga/2MHJleP6DJz/g
LnDE4nbpGA+COGDx2xBCyYEsmsOcEHUBhtP19sOC3Ar2Tz33MYQ9wfq2e2O5jvoBwoinr9k36+vH
byCVeKxBaRY9fJSuBPKmokEjw1J0UsIShsSWV/51hS+BH6MRqVAhuiRe24EQAl47W0gopOijNeQN
g8LR7HXRzK7zFsOP2es8wWeJek7wgsAqzsACP7PkE3njLMniPMIjH3LZ/FWc/Fjab+wMLTVslyw7
4akU2IDPZd2Aic2Kl7jO0EUDveJAD+suX79Z/SsvDHWQ/GSrUQfwQuIz+ITnMgcNwHgMdhXmOcQN
yzPKMXfAa/5PFKFeI3lSdcjihvSYbzD35hGuVInQFDtGlRHY/rHf71e4I0i7qfKsNfQn3YRsaN8X
hBWZvj1p45KtRDVHVjPOorcUgNV1iYleJ/3dwB7mVJeXCmAmqFMLFRwVhIG0TfaJtQaNxI0x6VWH
Wcr80rKIYHU8xhkZCRq7o3F71HoMr+IQiQ6xLFTE+bXNkpCfDvIlhR3J3zliJAuoEhDSp1JC4paA
L+QnzQOVX/Uqj0Rwhbe0CS6JwcRF5MLAfqCJ7Ldk1KtMcQ85ilERn7ECg2SQHO0GqzX05nNc6ZxG
0xr1kYEAm8wAQDUWMRkIz8ajUTARCxcjjbfYqA4+TA2+mbou28l5uYmytw4enY7QKn0Kvv1QVFKW
kwFD0Z3SB2KUubi10DdWYYesHSnaEFBAhJT/jZstTsqkV+FE/qRthrLE93I0DA0LTDF1Ej7S7hKF
H31gbyqNGez64P0wqFqSGX++VnhcMXFqgD7ftUcMptC6N3HTXrqDGth1o4xNm7L/hofnxqgbjJCN
KxvrD2dCKND2HOPOgrfeKh2N+vlG58a+xeCMMycn/SnsNW8+0v3exBBsj2DCIaCIjJsVDIshAsxK
rtLS0WyhNAb/pNmDMKOCIOMAoJx5U8bP0lQyw3tUggBxL4BBrhJ2q3H1/chPelaZstOaB8gnNxCi
yUlrOkTeefA72Afkg0xQSKVPVAMtqnxj9R/k1rr1ds5evlm6OVFsw2ntS5WCtTMwCggNRGnizZ6s
rCO650TKHCq3D8gvcsAJnDIQ6WodHFDlHA+8cV2iLjA2kkeunUTelIVyMF2BP0h0wE4RvyHaxdxl
ucTsp/dBaoTTUSTiiQcFYwNLkpSTGmKDsuZRhvfHZUrMs2M7neuCvh/KTl/XkKJHAcpOpwkBOhTR
DD0NHemfYzBxlvz6vb6Iz8EBJmkrdx6h8myKGJW2matZE95ErRFaB7L9Yd94q8Q3biq8abF66Y/S
rIlPNaO7Vk3Yx7UP9+1C9NJEnYnE224NGOronDXgLCBYb8Ll7eixZQtvTR2XuZB/CUXKWRrJvQjl
A7BrIFRdspB8ukkWwPLjpbs4pWP/DLVMyR3o+tlN3jBVUXMDb7kRlcYmPldUcME7dTYib4zBjI86
WUzgio0gumnDvqYRL9uKVAg2IoXFdbh23Y03o+aSIyqAVJclKHH8DMukTAFCN2oGeecPGBHq1eWQ
Z80zS3WrK0Bi1ieLc6OKVKDqB4ZPuHK1+uRRYdAcFa3GUD5A+VgamWodFqpSot2xnWD2ilUO+Mbc
j69W5Ji85qlyqE8ZaP2dHTnqDd3cxGRXWbEaGFbd+SOnnc9EPokTJE3ouFinJtZNhVvIi2wBFow8
WhpV17yeOCzU0voGfOCDLYFkzKVx761bHoB3hVFZXLqpDTor8z67uFiP2EUVasGF5zg/nmo6UFGS
UbxqYGmfIAS9pCemllVFgRILc/ANrLE0rF75lrYJqBDo+XTfEL5Xa36rz9IQ1DTVS1shTTEzPmlz
zV6Zj04EjgT/Dc7QcfKRH5fFhwK0Kz5iit5ashxRXRGpQW9ZcRTUK55QLlYyaLpsC9TmrDAksEkX
/tQ7QLjnsneXPWXzKZHwZh9hbS90jE1SA7xQ3vAwX30lIj7+4K7i5BHODhv7+OhN7W1vdrLiBL4x
q5Csr9/UOhN3y3Qlp7icGZ6HGbDBtr+lQwL+jXvYtayo0qluJeYoWD3QaS6aiKStZ0j8GcN+Qd4O
5+zLuQf+ImUbsqs7WSXw05597IbecAtF0FRuABwYQKANQBFBacMrwgbQYnGmrENy3eZOJz+h760e
pG+8ySAGaHnCfijL3MAiOt74EC9KhWWwA12CuBsgurfRPP9DisR+3itPZWd22wo5UFmnSpXpBI6+
lwE6Yry98m2AQwtV72aDwQU3ReePeGP8SSEWMIR07dzAHvNRF46a+8GJugQKAxoTXOY4+u9y7DdL
W3Ji+3OdQZJCTpYcc3o5V43BmTUoJGcHXGAkFBP9t4EIhlDC/XzPMwP6/fi4lHOq0/vGxjqnfcUP
XirnFhWHq7Tsp8LsHb9c9Go/s1dD+EhimOLFBKkTQSnJwvcRDGgektG0cY0mVr3mP7oyIEcDlAyx
DHVdQ2gSTQjAxSCddnOIfUGT/lEy+vh0qN1636FPkqL0/78RI1NvlZTJySXgD04tpKInubNMat3C
pjZeLhoOT9oLllJksfmo98Fvo4GVpssQXz9+00TlQ+9OICweYagzC5hG30+K7nAyhTqe4ICxF6VJ
Bc4aQw2ZdqbLDd1PRwwh+SPNVWrYHTYcCStRI/83hPQYo4sYX8sQs1lIBuo0fl0ny3fYA9kK8OeE
tyiBp9hyiiusFrn8gFSsHjomUSAJAIzj6jjNLvweJrb+zFvz8jOrowPS1CGD7vsYseDZo+sr9nit
kZettypVkwVlEYcNBe22KDIhpqQGXEx7IsZ4KXagvL5LbZSEZuJgkN+Zhb3y7FWHAKsaYjy/bu7a
Wz9Yuevtarl13NXKvUfwcF3dhbCumRYhr/GK0727yKRqD1TUGFNo3hs+2uMFlhbpxpJY80A4qPB4
Swk6+C7EoIJDpwC0lHC4MiUzDtIqPOpfh/1PdnCE0PK7xyW9/Yto6eENK6xBOYFgJmzaj8wEPAj5
r+9QuPEiBr+a3KltCA8/ckPorV37rmEVodUoUCMtIp1Ulc0aoZOx3Kei/FxoqguH4Fge9+MPqsw9
v38w1c+jZ/nWhc/3Byh3Pdwex57fhbg/g3s7Az/pxetRMFSM7RNHNK7ybjuqNq2y5/6tRVdt8Zvm
VFGOe2oBBPP5O5uY4A6lgymxOoLXX8o8xOsqa4uKVfizS37WHoqyjyAGo3qOZUSTaOwH8kuiShc6
gJ+15RgbjxB2+z7NoEFKFx3bQ+Q7c9ajXGSisChqfBMFPBBRvEDAoi4JIaWrswaXiSkuxeHmzF/d
Du9SzKiLh+Vcuz7/1IHGlTXKcsLh69u1RVxcRHSEzeVs1Dt/r4TbXM/MHy5PUlFwUJpUbNMbcDvF
70zYIZJilJ4oiRvGeUdtWJss64SlvQBFeXbOWmmkuChMLAANGTdjIH0gKSEdCJHMUH0HxNLSZtHb
XBjVW7OijWrWZCkEWALfsPH/ipqrFzCsgM8bi8tnEnHGUZnj+AenAecrp6LCd7dfofwVXjdNaSrz
wGcpAtYfnElRd069osb3eDSBE6N6Lr08jFeUyuIF6s9xDs4XMBRpE1ISYJGbDvFD3hw9x1kh73lQ
eZPuWogfqdu/1KcLqt8H6jFS1iR1ViGtYRSlZRJFpjLSjtM0isUQQ18sJA8XkMvj+fq1YiGm7FSB
jy95S2928jmVxeo7iCjhXtC5mIJGGMv6hBmGGElfOLbpf3qFbyJnp9tKyl2VQcedvH5Q28ZjkhSo
Cl1zrv9PIYIq8bvz5nKo6jJhTTNovfJX/ht7aoN8APKENsbf90swsO94uiGrZ3SJnggcVERAncr8
hRmyeoguKVQmtulYIiovbXVpjZ1+yuiUavEnrN23tUHX6aGhZi8L4hX2/uevv7zDSAlXHlLZwQbY
rDIG7khMhj9y/euNY/nDBEDG2V4a6lpUaMdykMQfivj4HwwDqYe86RNLF/i/EmjCohwugh+hXBu7
4lVZpBYrrB0ZZr8v9aWQGxFhnSaS5yo9SNMlsKR24GRs+f8fkEP7HNcagPPTJ7WtkSf+b+JHpwzf
nYiIokcETjsScTR6IzwyB6PORYdSeQo8JqoGIvWVN7xA1hsBq9x/+0HKB+dZgwMj9XyM/5hjyFPr
eyu5RS3rjEoVWSSiBca8FYtbKnPtjL7QMf3/e3Dfvj8kLgUppRrrzv/6AaJk5dTm7UrN6NxEEDxK
MxFofAdP7NBtEnEsRldueJlHpmBfddpq/YnOE0bYzJkg4C4jdNV5AJKpchHfiQoEdGAuKbJQ+QJq
HgI1YCzwpDBlmLfwO9Y8Cqmu7TM4FFRUYQNFFRZLsD9uEPBAAAi4hgKJodOrTj/EjCuWKz2iQVcd
K/ErFArCo0L6tLhuAHtBEztH2pYtWOSBi53i0SD+kp4DAsMcUoqoiAtxFIDeGBxVFOH2RRFl7VGE
vjmKdPnrYnTUD/8LA9iPgZtGAAA=
```

**Input provenance.**

These 30 archival input IDs and digests identify the evidence. Individual results take precedence over merged summaries. Unavailable individual round-1 results and historical checks use the roots and episode notes in `.imd/reads/goal.json`. Roots are summaries, not extra search items. All 30 input digests were checked.

| Input ID | Result | SHA-256 |
|---|---|---|
| root-1-01 | root merge 1-01 | `6ef8589a60b2cba2f7036174b73843cff033be7d65f3b105df64837e04ec937e` |
| root-1-02 | root merge 1-02 | `1e3cd17d8e997e3a660a6859a197e5f3777173f552979a6f07c9fa07d246ec07` |
| b09-geometry | geometry-fix-r3/geometry | `34c479ab0bc9e51b5befaab3cdb5d8d056d68222827862035e235ff905c37862` |
| b10-geometry | geometry-check-r3/geometry | `d5ed91529b6f9c1a60ef3be131189f1998c8d3d21012c9ae8d42fab2b9926bc5` |
| b11-seam-integer | lattice-r3/seam-integer | `1903253e2ca37d77ec51994d6ae7d201d60bfa776baf12621243d9064a701607` |
| b11-angle-phase | lattice-r3/angle-phase | `31952075a3d7cdccb6c0f29cf7374dfa222cd7614e15b250ab75214194eda7f1` |
| b12-ring-contact-release | topology-r3/ring-contact-release | `1fb99c005c55a6fe7fae317dee8fbe5de8d0178460fda443a6bf7c444756bd10` |
| b12-pair-release | topology-r3/pair-release | `435944d4a8e55d9116e319cfc75397b5a9bd8ea4e00366657dbd7c0f83fec486` |
| b12-archive-basin | topology-r3/archive-basin | `50ec99cad81568bfd54a21d518238c2630051150c78828c226aa901122be82da` |
| b12-boundary-core | topology-r3/boundary-core | `74f95387382f9458f6f83af300e47708bf741ab2840a4b8c0a5c9436484fd484` |
| b13-best | lattice-check-r3/best | `c4b69c933806c5113c776f1cead5414b46287d9c8df6410bc650b667636311a3` |
| b14-best | topology-check-r3/best | `402e38827a49501934b276114375450fc2fc37284c13c30cf9e8c8868d4467e3` |
| b03-contact-tangent | polish-r2/contact-tangent | `5781687979291f49c82737b3bfebe463d8d89a2500ad545128efdf7a4084d7c8` |
| b03-coupled-grid | polish-r2/coupled-grid | `b3519f1e89a0f16eb4cdfe837e71d1953f3deb5d9ba409f0fe1ba64c9ea584eb` |
| b03-interior-point | polish-r2/interior-point | `82523378e710240f307107aa73da75fe5cf1700fa692d277f8cf3e6dd5e36c25` |
| b03-penalty-continuation | polish-r2/penalty-continuation | `b17f669c325befb0ee44127c1a46e9987d825f3ec802296f9828e58e40bb889c` |
| b03-polygon-slsqp | polish-r2/polygon-slsqp | `cbeb680f92bf18ad1093b903416f076eca0672014d250c4ca8e8a63a38d8455b` |
| b03-rigid-grid-phase | polish-r2/rigid-grid-phase | `0ffe806a6202ef363f2f075bd43b3c317bd543ac317f66e1b79618e53215e7ac` |
| b03-strict-homotopy | polish-r2/strict-homotopy | `bbe0a5151e6e15a8df726decc40039557a29ac87e77542f1990b0010dc593f4b` |
| b04-basin-small | moves-r2/basin-small | `d364c8376db2aab396a0bfb93ae356699c8c6e7b65ce9cffe0f4a8a130e1e475` |
| b04-basin-wide | moves-r2/basin-wide | `65d0dfda56244b1f735392b9542deb46a3c1801f0e1f951805870f15b9cf0e04` |
| b04-pi-flips | moves-r2/pi-flips | `1dfd6d27bb05cc0eae2bed1141efaf0db204b6fafae8fcafd28fe9fb015e7028` |
| b04-reinsert-block | moves-r2/reinsert-block | `41cc231da369479fd5f47ff4c9036ce63196bc0e1ede0097b4fc6e1039a3b52b` |
| b04-reinsert-one | moves-r2/reinsert-one | `7444ca1f0ef7f516148b1568cb99847991ff0e36a97bf91d46eda4151ab922c4` |
| b04-relaxed-rings | moves-r2/relaxed-rings | `6f15bebddde2e90c3d54f3630dfa30b0807a8775f333ece0219e395d79ca4436` |
| b04-sliding-pairs | moves-r2/sliding-pairs | `612f701bca774ebc8599a9c145da5a4055f8e63f74ec26b8688bb19b7c021d5d` |
| b01-published | repro/published | `89ffaa96cbc8f60cbce1ebe7c61e0bfac270d013b5aff71bc9d5c7da1a374161` |
| b02-pairs-5-5 | topo-r1/pairs-5-5 | `e5a5fe2cd0aa58f0b6d60d12a66e3a2976b628f1bdfcb42757ae89188f58ec61` |
| b02-rings-312-411 | topo-r1/rings-312-411 | `708b6b93a9c8c13123d15f70c8185ebcf6008bfc84058ad55aa4665b307df04a` |
| b01-annealing | repro/annealing | `8f979bb6b01c9cb949349334957d1beb220831ee63038857fcf71b73cecf3e47` |
