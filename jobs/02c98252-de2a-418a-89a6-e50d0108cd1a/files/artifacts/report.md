# Cracking K4: no verified solution recovered

**The mission is not complete. K4's plaintext and intended mechanism were not recovered.**
No candidate meets all seven conditions. This package delivers a verified K/PK
baseline, a design grammar, an auditable bounded attack, and explicit negative
results. It does not represent those as a crack.

The first target run tested **14,508 parameterized hypotheses** and
scored **24,000 distinct, anchor-matching candidates**.
A balanced supplement scored another 20,000 records; there are
**43,996 distinct target plaintexts across both stages**.
Four scrambled controls contributed 96,000 additional records. These are finite
parameter tests, including overlapping configurations and known-family calibration;
they are not 14,508 independent cipher inventions. The requested numeric effort
floor is exceeded under a parameterized-hypothesis interpretation, across more
than five method classes. If “500 hypotheses” means 500 different conceptual cipher
inventions, that stronger reading was not achieved.

## Seven-condition audit

|Required condition|Result|
|---|---|
|1. A recovered deterministic M, 97 letters in and out|**Not met.** Deterministic candidate decoders exist, but none is identified as K4's mechanism.|
|2. All four anchors emerge without being supplied|**Not met.** Retained candidates use keys fitted to the anchors. The independently specified physical/running-key models produced no anchor match.|
|3. Far fewer than 73 plaintext-fitted parameters|**Not established for a solution.** First-run leaders fit 27 or 29 key letters, plus selected route/blank choices. These are all counted, not concealed.|
|4. Two independent implementations agree|**Component check passes:** Python and JavaScript agree on 14 known fixtures and 300 retained candidates, including exact re-encryption. There is no authenticated K4 M to certify.|
|5. Coherent English with the required navigation/K5 meaning|**Not met.** Retained leaders contain long gibberish stretches; no semantic interpretation is justified.|
|6. M reproduces K1–K3|**Not met for a K4 M.** The independently implemented known K1/K2/K3 methods reproduce their fixtures. That is a baseline test, not evidence one recovered M solves all sections.|
|7. Full spec, code, log and clean reproduction|**Research package supplied.** The missing K4 derivation and plaintext cannot be substituted by this reproducibility result.|

The literal 97-input restriction in condition 1 and applying the same M to the
63-, 372-, and 337-symbol K1/K2/K3 fixtures require some interpretation. This run
uses known-section reproduction as a primitive calibration, but does not quietly
count it as the stated same-M condition.

## What is actually known

The supplied ciphertext is preserved byte-for-byte in `data/k4.txt`. The anchor
positions agree with [Elonka Dunin's first-party clue record](https://elonka.com/kryptos/).
The only defensible plaintext display remains this **positional mask**, where a dot
means unknown. It is not a proposed answer.

Continuous mask:

```text
.....................EASTNORTHEAST.............................BERLINCLOCK.......................
```

Mask in the sculpture's K4 line lengths, 4/31/31/31:

```text
....
.................EASTNORTHEAST.
............................BER
LINCLOCK.......................
```

The [auction's original listing](https://www.rrauction.com/auctions/lot-detail/350761607302001-the-complete-secrets-of-kryptos-jim-sanborns-private-archive/)
documents the September 2025 archive discovery and describes an original K4 coding
system among the sold materials. Thus “not publicly cryptanalytically recovered”
should be distinguished from a claim that no original coding record exists.
Paradigm's pages returned HTTP 403 here; current sign-in, fee and hash-custody
claims are supplied context from the brief, not fresh verification by this run.
No oracle submission or payment was attempted.

The Weltzeituhr interpretation, navigational semantics, and K5 target are adopted
as the brief's constraints. The November 2025 original letter scan was inaccessible.
They are not promoted to newly authenticated findings. Primary context and access
limits are detailed in `SOURCES.md`.

## Phase 1: verified grammar before attack

The [full sculpture and tableau transcript](https://elonka.com/kryptos/transcript.html)
was fetched. Concatenating the left screen exactly reproduces the included K1,
carved K2, K3 and supplied K4 ciphertexts. The right transcript retains its headers,
row labels, extended alphabet tails and extra L. Exact spacing and raised letters
are not encoded; it cannot support a complete physical reconstruction.

Python and JavaScript independently reproduce K1 with PALIMPSEST, K2 with ABSCISSA
in both carved and corrected forms, and K3 with an equivalent 337-symbol
transposition. They encrypt the resulting plaintexts back exactly. The misspellings
IQLUSION, UNDERGRUUND and DESPARATLY are preserved. DIGETAL belongs to the Morse
component, not to those three plaintexts. These anomalies are logged; a round trip
alone does not prove the intention behind every spelling.

K2's 2006 correction inserts a missing ciphertext S and changes the final reading
to X LAYER TWO. [The Kryptos Group's announcement](https://elonka.com/kryptos/CorrectedK2Announcement.html)
reports Sanborn's confirmation. A second physical screen layer is an interpretation
of that phrase, not a proven consequence.

PK1–PK9 were reproduced in numerical order from **borrowed public solutions** in
[Adrián Barreto's pinned implementation](https://github.com/TTFH/KRYPTOS/tree/496976ebe008f9a5eaef8c52bb8ad06c3a4917f5/src/ctf).
No independent key discovery or official checker acceptance is claimed. Their
ciphertexts and plaintexts agree with a second mirror that credits the same source,
so the mirrors are not independent provenance. New Python and JavaScript code checks
each direction. PK10, which composes all the earlier layers, also passes as an extra
control. Full plaintexts, keys and attribution are in `PK-SOLUTIONS.md` and `data/pk.json`.

`DESIGN-GRAMMAR.md` records families, key-source status, null conventions, grids,
and each K1–K3 borrowing. The consequential observations are PK5's prior-plaintext
running key, PK8's four related additive keys, and PK9's spiral-plus-columnar route.
The inference is a prior for explicit experiments; later puzzles by a different
author cannot establish K4's exact design grammar.

## Phase 2: bounded results

[akaalias/k4](https://github.com/akaalias/k4) was read before attack. Its current
README describes 207 experiments rather than the brief's 184. Previously tested
periodic and transposition models were used as explicitly labeled calibration,
not reported as novel exclusions. The useful local exact deductions are:

- **Pure transposition of the 97 letters is impossible:** the anchors require three
  Es, while the ciphertext contains two. This says nothing against a route combined
  with substitution.
- **A fixed monoalphabetic substitution is inconsistent** with repeated ciphertext
  letters' known plaintext images.
- **Direct additive periodic keys, periods 1–52,** fit the anchors only at periods
  27, 28 and 29 under either ordinary A–Z or KRYPTOS arithmetic. Explicit contradictory
  position pairs are recorded for every rejected period. These are independently
  checked finite facts, not universal exclusions of those cipher families.

The complete 24-letter forced-key table is in `ANCHOR-AUDIT.md`. For periods 27–29,
the anchors fix 24 distinct key coordinates, leaving 3–5 coordinates free. This
explains why many compatible completions exist; it does not derive the anchors
without using them. It is known-plaintext fitting, not evidence of Sanborn's key.

The first run's allocation was:

|Model class|Parameterized tests|Anchor-compatible|Candidates scored|
|---|---:|---:|---:|
|periodic-tableau|104|6|0|
|physical-tableau|188|0|0|
|physical-plus-periodic|235|47|940|
|route-plus-tableau|7,200|2,409|23,060|
|plaintext-autokey|104|6|0|
|ciphertext-feedback-plus-periodic|300|66|0|
|two-additive-clocks|412|94|0|
|hill-2x2|8|0|0|
|prior-plaintext-running-key|5,954|0|0|
|conditional-key-audit|3|3|0|

Each hypothesis records its seed, parameters, fitted-coordinate count, modular
ranks, status and score count. Every scored candidate records its full key and
plaintext. The top 50 are retained. No candidate reaches scoring until all four
anchors match exactly and the output is precisely 97 A–Z characters.

The global 24,000-candidate cap was reached during the route phase. Subsequent
compatible models received algebraic checks but no first-run English sampling;
claiming those models had failed an English search would be incorrect. A separate
balanced audit repaired that allocation limitation:

|Supplement namespace|Tests|Scored records|Best total|
|---|---:|---:|---:|
|periodic|3|4,000|-14.002931916|
|autokey|52|4,000|-13.866439920|
|two-clocks|206|4,000|-13.684769329|
|feedback|150|4,000|-13.695049737|
|physical|235|4,000|-13.704792728|

All five leaders remain visibly incoherent. First-run retained leaders use 27 or
29 fitted key letters. The best first-run model selected a seven-column route,
one blank among 98 cells, and a period-29 additive key. Its raw key has 29 fitted
letter parameters; the blank, route family, width and period are additional choices.
It is not a low-description-length, independently justified solution.

The physical probe tested literal reflected/offset transcript coordinates and then
a second periodic layer. It does **not** cover arbitrary shadows, curvature,
photographic projection, exact letter baselines, or all possible physical overlays.
The route probe is a finite 800-route catalog combined with nine periods. Its
inconsistencies exclude those exact combinations only; compatible unsampled or
sparsely sampled cases stay open. Hill tests cover only the stated two-letter
linear/affine models. No negative result here proves K4 impossible to crack.

## Verification and statistical limits

The frozen scorer combines mean quadgram and hexagram log probabilities with
nonoverlapping dictionary coverage. It is trained only on three vendored public-domain
books, never K/PK plaintext. All formulas, alphabets, punctuation rules, search
domains, boundary conventions and pseudocode are in `SPEC.md`.

Four planted 97-letter mechanisms are recovered exactly using the same anchor
equations: periodic key, plaintext autokey, two additive clocks, and a 98-cell route
plus tableau. They validate arithmetic and key recovery *given the family and
cribs*. They do not measure the power to discover an unknown real cipher.

Four controls shuffle ciphertext letters outside the anchor positions, retaining
those ciphertext positions, the anchor plaintext, and the same first-run search
procedure and scoring cap. Their best totals were:

|Control seed|Best score|
|---|---:|
|7101|-13.660860409|
|7102|-13.695037903|
|7103|-13.609743995|
|7104|-13.395821893|
|K4|-13.570011676|

One of four scrambled controls exceeds K4. The empirical rank fraction is 2/5,
with too few controls for strong statistical claims. This supplies no positive
evidence that the best K4 candidate is meaningful. Scores are not probabilities
that a candidate is correct. The repeated known anchors contribute to the score;
the controls include those same anchors.

`python3 verify.py` passes **16 test methods**, checks **14 known-cipher fixtures**,
replays **300 retained candidates independently** in JavaScript, and audits
**140,000 gated candidate records**, including controls. The recorded output is
`results/checks.txt`; a fresh-copy run also passes in `results/fresh-checks.txt`.
Regenerating the extracted fixtures and corpus model produces byte-identical data.
Both implementations exactly re-encrypt their retained outputs.
The replay checker initially omitted spiral support; that failure and repair are
in the ledger. These are local reproducibility checks, not independent authority
or proof of authorial intent. The `solution_found: false` field is the deliberately
conservative research status; the program has no reliable automatic English-to-solved
classifier.

## Meaning, K5 and unresolved work

**No plain-English meaning of K4 has been recovered. No defensible new K5 prediction
or location follows from these results.** Under the supplied interpretation, the
anchors constrain direction and a clock reference, but do not identify a starting
point, time, route, operation, recipient or message. Inventing those would turn an
unanswered riddle into an unsupported story.

Unanswered: the actual 73 remaining plaintext letters; the intended alphabet and
key-generation rule; whether physical layout participates; whether another message
or surface supplies key material; how K1–K3 constrain one common mechanism; and what
specific K5 information follows. A useful next experiment must reduce one of these
uncertainties with independent structure, not optimize prose around the anchors.
Metric screen geometry or a separately justified low-parameter key schedule could
supply such evidence; neither has been established here.

## Storage repair and evidence preservation

The original upload exceeded the 8 MiB source-bundle limit. The repair preserves
all experiment events: the main `LEDGER.md` remains intact and append-only, and
the complete control ledger is losslessly compressed as
`results/controls/LEDGER.md.xz`. Duplicate hypothesis and candidate JSONL streams
are reconstructed offline from those logs by `src/evidence.py` into disposable
`test/scratch/evidence/`. Verification does this automatically. All 20 streams
are checked against their original uncompressed byte lengths and SHA-256 hashes
in `data/evidence-manifest.json`, before their records are audited. No research
records or required runtime assets were omitted. This changes storage, not the
negative cryptanalytic result. The gzip containers are regenerated; the exact
uncompressed JSONL contents are preserved.

The named output is this report. Supporting source, data, specifications, tests,
provenance and the complete append-only `LEDGER.md` are ordinary repository files.
The package runs without network access or external Python/Node packages. See
`README.md` for the exact offline commands.
