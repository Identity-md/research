# L-meta-4732: status report

## Outcome

The step is **not proved**. None of the three things the goal asks for exists: no Lean
file proving L-meta-4732 outright, no check of such a file by a second holder's machine,
and no pull request on `open-goat/pequalnp-proofs` adding it. This report cannot stand in
for the proof submission the goal asks for; it is a merge of four independent attempts
([A1]-[A4]) that all reach the same conclusion and the same gap.

All four angles agree: the step reduces, by proofs already present in the prebuilt
project, to a single missing lemma (called `dirty` below). None of the four could prove
that lemma, refute it, or find it already proved anywhere in the project.

## What was established (as reported)

1. **The statement is tight and consistent.** [A1]-[A4] each independently enumerated the
   52 incidences and 234 quadrangles of PG(2,3) (points/lines 0..12, incidence `p` on `l`
   iff `p - l mod 13 in {0,1,3,9}`) and simulated the obvious "per-line OR-AND, then OR"
   circuit. That circuit meets every hypothesis of the step and has exactly 63 gates when
   the omitted pair `(0, x6)` is a real incidence (`x6` in `{0,4,10,12}`), and 64 gates
   otherwise. No run found a counterexample or a 62-gate circuit, and none of the four
   claims the statement is false.

2. **A counting argument explains why 63 is the right bound in the easy case.** [A4]:
   covering the 51 non-excused incidences with stars costs `(sum of star sizes) + stars -
   1`, and at least 13 stars are needed (the 51-pair incidence graph still admits a
   perfect matching), giving `51 + 13 - 1 = 63`. This argument only applies when no AND
   gate is nested inside another AND gate's cone ("flat" case); the general case with
   nested ANDs is the open part.

3. **The project already contains a reduction of the full statement to three premises.**
   All four items checked, with the prebuilt Lean 4.36.0 toolchain and project sources,
   that the lemma `R_meta_4732_639` discharges the step's exact statement (as given in
   `step.json`) given three premises:
   - `flat` — proved, matches `L_meta_7293`: a good circuit with no AND nested inside
     another AND's cone has at least 63 gates.
   - `clean` — proved, matches `L_meta_7295`: in a smallest good circuit with fewest
     nested AND pairs, every gate has two distinct inputs, and every nested AND is true
     on some quadrangle input.
   - `dirty` — **not proved by any of the four items, and not found elsewhere in the
     project.**
   Each item independently elaborated the composed term (e.g. `R_meta_4732_639
   L_meta_7293 L_meta_7295 dirty` in [A1]) against the step's posted statement with no
   error and no `sorry`, printing axioms `propext`, `Classical.choice`, `Quot.sound` only.

4. **The missing premise `dirty`**, with `S := singerLines3`, `neg Q := incidenceInput Q
   (missLines S Q)`, and `good omitted C := Monotone2 C ∧ ReadsBack 26 C ∧ (∀ p l, p ∈ S l
   → p ≠ 0 ∨ l ≠ omitted → C accepts incidenceInput {p} {l}) ∧ (∀ Q, IsQuadrangle S Q → C
   rejects neg Q)`, reads:
   > `∀ omitted C, good omitted C → C.size < 63 → (∀ D, good omitted D → C.size ≤ D.size)
   > → (∃ i j, AND i, AND j, InCone 26 C i j) → (∀ g ∈ C.gates, g has exactly two distinct
   > inputs) → (∀ i j, AND i, AND j, InCone 26 C i j → ∃ Q, IsQuadrangle S Q ∧ wire (26+i)
   > is true on neg Q) → False`
   In words: a smallest separating circuit with fewer than 63 gates cannot contain an AND
   gate nested inside another AND gate's cone. This is the whole remaining difficulty of
   the step — a real case analysis over circuits with nested AND gates, for which the
   project's own neighbouring lemmas (`L_meta_5158`/`L_meta_5162` for one nested pair,
   `L_meta_7293` for zero) only cover restricted counts, per [A1]/[A4].

5. **No existing project file proves `dirty`.** [A1] and [A4] searched the ~5591-5592
   `L_meta_*` files under `PEqualNP/Outside` for any statement with hypothesis `size < 63`
   on this circuit family; none was found. The only files with that hypothesis are
   reduction (`R_meta_*`) files, which assume it rather than prove it. [A2] confirms that
   `L_meta_4732.lean` (the step's own would-be proof file) does not exist in the public
   repository (404), and that `L_meta_7297.lean` — a guessed id for `dirty` — also does
   not exist.

6. **SAT search cannot settle it either way in the time available.** [A4]: exact monotone
   circuit synthesis with kissat 4.0.2 reproduced the known star counts for small
   sub-instances (1 line, 2 lines, 2 lines minus one incidence), but found no answer in
   470s per run for 3 lines, the order-2 analogue, or the real 62/63-gate instance (5
   seeds); runs at sizes already known satisfiable also timed out, so these timeouts are
   not themselves evidence for or against the bound.

7. **A mathematical sketch, not a proof.** [A3] gives one construction illustrating how
   nested ANDs can, in principle, filter a shared "bad" monomial cheaper than the flat
   star count predicts (e.g. a 5-gate circuit covering three incidences where the flat
   count would need 4 stars for the same coverage), and argues `dirty` must show every
   such sharing costs at least what it saves. This is offered as a starting point for
   whoever continues, not as a closed argument.

8. **Packaging is feasible once `dirty` is proved.** [A2]/[A4]: inlining `L_meta_7293`
   (76268 bytes), `L_meta_7295` (63415 bytes) and `R_meta_4732_639` (16723 bytes) into one
   `PEqualNP.Outside.L_meta_4732` file comes to 156406 bytes before `dirty` is added,
   comfortably under the 524288-byte single-file limit the project uses elsewhere (per
   [A2]), though well over the 64000-byte limit this write-up itself is held to.

## Where disagreements exist

None. All four items independently reach the same verdict (`dirty` is the sole gap), the
same byte counts for the three source files (16723 / 76268 / 63415), the same axiom list
(`propext`, `Classical.choice`, `Quot.sound`), and the same negative result (no
counterexample, no existing proof of `dirty`, no decisive SAT answer). [A3] alone offers a
partial constructive sketch toward a proof strategy; the other three stop at stating the
gap.

## Sources

- [A1]: `item-angle-1` result, SHA-256 `86689f7559a55f80a1fc9a73039cbdf7bf0ecea85e8f878b3c63cc053f10b2f4`.
- [A2]: `item-angle-2` result, SHA-256 `60b6ac7a5de201c093485fa6fb3f76cb463a62f81619cc57559f827ec99aad2b`.
- [A3]: `item-angle-3` result, SHA-256 `5878edda9bd3ac4e44a702e4c1661ee91790f2807dc68920c383cea640d9fe70`.
- [A4]: `item-angle-4` result, SHA-256 `4839a05098a74c44aa5e7bb2ae8a6d2b8afa9baa6ef63f338b441efbf4edd8f0`.

These four results are not themselves delivered as files in this submission (per the
task's input description, they are not tracked in Git); this write-up is the only
delivered artifact, assembled from their content. No result supplied its Lean harness
script, its enumeration/simulation script, or its kissat logs, so the figures above (gate
counts, byte sizes, axiom lists, SAT run times) are reported as stated by [A1]-[A4] and
were not independently re-run by this write-up step.

Project files the four items name, which a reader can check directly against the public
repository `open-goat/pequalnp-proofs` under the path `lean/PEqualNP/Outside/` (the items
themselves write the path as `PEqualNP/Outside/`, omitting the `lean/` prefix): the
existing reduction `R_meta_4732_639.lean` (16723 bytes per [A1]-[A4]) and the two proved
lemmas it depends on, `L_meta_7293.lean` (76268 bytes, the `flat` premise) and
`L_meta_7295.lean` (63415 bytes, the `clean` premise). This write-up did not fetch those
files itself; the paths and byte counts above are as reported consistently across all
four items, and a prior independent review of this report confirmed those three files and
sizes exist at that path on the repository's `main` branch. `L_meta_4732.lean` itself and
any file proving `dirty` are not present there, per [A2].

## Recommended next step

Post `dirty` (as stated in item 4 above) as its own step so it can be attacked directly,
since all four independent attempts agree it is the entire remaining gap and none found a
way to shortcut it. If it is proved, assembling the single `L_meta_4732.lean` file
described in item 8 and opening the pull request is mechanical. Until `dirty` is proved
(or the requester chooses to accept the step as unproved), there is no Lean file, no
second-holder check, and no pull request to point to.
