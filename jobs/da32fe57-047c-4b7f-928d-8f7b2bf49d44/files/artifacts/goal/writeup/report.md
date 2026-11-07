# Re-decision of T's per-spread switches

## Decision

Among the supplied pooled measurements, `cut-s2-on` is the only one-entry flip that clears the requested screen: its gain on spread 2 is +0.891348 per seed with SE 0.235613 (greater than 2 SE), its worst reported paired run is −38.609181, and its candidate/T runtime ratio is 1.000339. The resulting proposed line is:

```python
ON = dict(cancel=(2, 3, 4), cut=(1, 2, 4), postjump=(1,), premium=(), deadband=(3,))
```

Its reported expected overall gain over T is +0.214815 per seed (SE 0.057375) over 2,000 pairs. This is a one-flip candidate measurement, not a fresh measurement of a combined strategy. [M2]

**Is it worth submitting? No, not as the requested evidence-complete result.** The cut-s2 summary is promising and passes the numeric screen, but the supplied workspace has only the four merge summaries: it has none of the item JSON files or per-seed arrays needed to report or independently check every pair. Also, two flips did not reach 2,000 pairs. Thus the requested every-seed deliverable remains incomplete. If submitting only a candidate based on the available summary were acceptable, `cut-s2-on` is the sole candidate to advance; the current evidence package should not be represented as the completed 2,000-seed comparison. [M1–M4]

## Ranked flips

Ranked by mean paired gain on the spread being changed, highest to lowest. `d` is candidate total edge minus T total edge, so positive favors the flip. SE is the reported standard error of that spread mean. Worst is the smallest reported paired delta, with its seed. `n` is the number of paired seeds in the supplied pool; for complete flips this is 2,000, including zero deltas on other spreads. Runtime is the reported candidate/T ratio. All figures below are transcribed from the supplied merge summaries; the source artifacts contain no per-seed score pairs in this workspace. [M1–M4]

| Rank | Flip | n | Spread gain ± SE | Worst paired delta (seed) | Runtime C/T | Source |
|---:|---|---:|---:|---|---:|---|
| 1 | deadband-s1-on | 2,000 | +3.195743 ± 2.662921 | −108.141189 (1001483) | 1.014453 | M4 |
| 2 | cut-s1-off | 2,000 | +1.0172 ± 2.7010 | −313.4653 (1000631) | 0.9980 | M1 |
| 3 | cut-s2-on | 2,000 | +0.891348 ± 0.235613 | −38.609181 (1000194) | 1.000339 | M2 |
| 4 | deadband-s4-on | 2,000 | +0.685092 ± 0.329523 | −76.496089 (1000166) | 1.026768 | M4 |
| 5 | cut-s3-on | 2,000 | +0.158357 ± 0.510038 | −37.940630 (1000147) | 1.004538 | M2 |
| 6 | deadband-s3-off | 2,000 | +0.075701 ± 0.366351 | −40.757606 (1000800) | 0.977109 | M4 |
| 7 | premium-s1-on | 2,000 | 0 ± 0 | 0 (all ties) | 1.000 | M3 |
| 8 | premium-s2-on | 2,000 | 0 ± 0 | 0 (all ties) | 0.999 | M3 |
| 9 | premium-s3-on | 1,707 | 0 ± 0 | 0 (all ties) | 1.003 | M3 |
| 10 | postjump-s1-off | 1,723 | −0.026992 ± 0.065380 | −8.336815 (1000087) | 0.999173 | M2 |
| 11 | cancel-s4-off | 2,000 | −0.0417 ± 0.1135 | −26.3426 (1000501) | 1.0016 | M1 |
| 12 | postjump-s2-on | 2,000 | −0.085428 ± 0.037774 | −11.089412 (1001915) | 1.001045 | M2 |
| 13 | postjump-s3-on | 2,000 | −0.14533 ± 0.0603 | −21.641 (1000052) | 1.002 | M3 |
| 14 | postjump-s4-on | 2,000 | −0.20956 ± 0.1084 | −35.687 (1000841) | 1.001 | M3 |
| 15 | premium-s4-on | 2,000 | −0.240940 ± 0.351027 | −100.704836 (1001855) | 1.000836 | M4 |
| 16 | cut-s4-off | 2,000 | −0.278599 ± 0.237429 | −27.304220 (1001420) | 0.996613 | M2 |
| 17 | cancel-s2-off | 2,000 | −0.4844 ± 0.1896 | −45.4122 (1000194) | 0.9869 | M1 |
| 18 | deadband-s2-on | 2,000 | −0.754502 ± 0.361895 | −102.577573 (1001986) | 1.016209 | M4 |
| 19 | cancel-s3-off | 2,000 | −0.9496 ± 0.1255 | −20.2586 (1001181) | 1.0009 | M1 |
| 20 | cancel-s1-on | 2,000 | −3.0291 ± 1.0313 | −291.3374 (1001629) | 0.9927 | M1 |

The screen is gain greater than twice SE, worst run no worse than about −60, and runtime ratio within 15% of T. Only `cut-s2-on` meets all three. `deadband-s4-on` narrowly clears the gain test (+0.685092 versus 2 SE = 0.659046), but its worst run is −76.496089, so it fails the worst-run screen. `deadband-s1-on` and `cut-s1-off` fail the gain and worst-run screens; their large positive means are highly uncertain. No other flip clears 2 SE. [M1–M4]

## Coverage and evidence limits

The intended comparison calls for 20 flips × 2,000 paired seeds = 40,000 pairs. The supplied merge summaries report 18 flips at 2,000, `postjump-s1-off` at 1,723, and `premium-s3-on` at 1,707: 39,430 reported pairs, 570 short. The missing counts are 277 and 293 respectively. The summaries describe premium-s3 as all exact ties on its measured seeds, but that does not supply the missing 293 comparisons. [M2, M3]

I reproduced the review's file-availability concern in this workspace: `.imd/reads/artifacts/` contains only `merge-01` through `merge-04`; the referenced `artifacts/goal/items/.../result.json` files and per-seed arrays are absent. In particular, there is no per-seed baseline score, candidate score, or paired delta table for `cut-s2-on` or for the other flips. Therefore the table above reports pooled summary evidence only. The individual worst-seed figures and aggregate arithmetic are reported by the merge artifacts but cannot be traced to raw rows here; this report does not claim to have rerun the simulator or verified those rows. [M1–M4]

The merges describe their pooled moments as worker-produced measurements from the pinned simulator commit, and record caveats about flagged source citations, differing timing scopes, and execution provenance. Those are qualifications on the supplied results, not independent reproduction. Runtime ratios are used only for the requested coarse threshold; recorded timings are not a controlled benchmark. [M1–M4]

## Sources and calculation basis

- **M1:** supplied `.imd/reads/artifacts/merge-01`, “per-spread flips of T's ON line: cancel s1–s4, cut s1.” Reports per-spread pooled gain, SE, worst run, and runtime for those five flips. The item files it identifies are absent from this workspace.
- **M2:** supplied `.imd/reads/artifacts/merge-02`, “paired re-decision results.” Reports cut s2–s4 and postjump s1–s2, including the incomplete counts, the proposed `cut-s2-on` line, and overall gain +0.214815 ± 0.057375. Its source registry names item JSON artifacts not present in this workspace.
- **M3:** supplied `.imd/reads/artifacts/merge-03`, “one-entry flips of T's ON line — postjump-s3, postjump-s4, premium-s1, premium-s2, premium-s3.” Reports the pooled estimates and identifies premium s1–s3 as exact ties in the measured records, with premium s3 incomplete.
- **M4:** supplied `.imd/reads/artifacts/merge-04`, “premium and deadband switches.” Reports the remaining five flips and their pooled moments, worst runs, and runtime ratios.
- The task identifies the simulator as [danrobinson/prediction-market-challenge at commit b244530ee2a6247b5f930830eeca9dd950da0e7e](https://github.com/danrobinson/prediction-market-challenge/tree/b244530ee2a6247b5f930830eeca9dd950da0e7e) and the T artifact as [the supplied strategy artifact](https://api.imd.fun/artifacts/79af781a0f1882f2a291e045f803714b52128f9938480d54fb43360417b381ac). These links identify the stated provenance; they do not replace the absent per-seed experiment records.

The merge summaries define `d = candidate.total_edge − T.total_edge`; they pool equal-weight seed deltas and calculate SE from paired-delta moments. The ranked values retain each merge's displayed precision; no extra precision is inferred. Overall gain refers to the mean delta across all seeds, while the ranking metric is the mean delta on the changed spread. [M1–M4]
