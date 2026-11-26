# Exact integer kernels on Thumbv6m

**This entry is not a takeover candidate.** The best measured integration scored **0.998861–0.998929× former 50** across six seeds, a **0.1071–0.1139%** reduction in S. The worst seed was **6.382%** above the estimated **0.939×** takeover line. All six seeds also missed the internal **0.935×** target. All three functions passed exhaustive local Thumbv6m execution and both host sanitizer builds. RV32IM stayed at **18,960 scored bytes**, with identical scores and a byte-identical object at a common input pathname. [Entry source](#entryc) · [Measurement records](#measurement-records) · [Check records](#check-records)

The 0.939 line comes from the brief's reported 0.9684 ratio for withheld champion 53 and the kit's 0.97 takeover rule (product 0.939348, rounded to the brief's stricter 0.939 line). Champion 53's source and same-seed scores were unavailable, so the comparison here is against former 50. No hotkey was registered, nothing was signed or submitted, and no TAO was spent. [Former-50 source][base] · [Pinned rules][rules]

## Six-seed comparison

Paired local measurements used the pinned kit at `5a32428ad4aa23bce737d50a738ace24ddeeed2e`, the requested fingerprint `2c8fd1f3a6711f0639685319fb25262b02bfecf4c6589c52cb58928270a46322`, and fresh hard pools. Base and merged measurements share the same input digest for each seed. Thumb code plus tables fell from 20,500 to **20,428 bytes**. Lower S is better. The gap column is merged S divided by the same-seed estimated takeover score, minus one. [Measurement records](#measurement-records) · [Pinned scoring implementation][score]

| Seed | Former 50 Thumb S | Merged Thumb S | Merged / base | 0.939 × base S | Gap above line | RV32IM S, both |
|---:|---:|---:|---:|---:|---:|---:|
| 1001 (shared) | 40.35740944 | 40.31212591 | 0.99887794 | 37.89560747 | +6.3768% | 28.48629371 |
| 2002 (shared) | 40.36980096 | 40.32553770 | 0.99890356 | 37.90724310 | +6.3795% | 28.51798843 |
| 3003 (shared) | 40.06372945 | 40.01937504 | 0.99889290 | 37.61984196 | +6.3784% | 28.22021703 |
| 4004 (held out) | 40.20073503 | 40.15724747 | 0.99891824 | 37.74849019 | +6.3811% | 28.39747848 |
| 5005 (held out) | 40.29623993 | 40.25309648 | 0.99892934 | 37.83816929 | +6.3823% | 28.35506277 |
| 6006 (held out) | 40.18381067 | 40.13803369 | 0.99886081 | 37.73259822 | +6.3750% | 28.35806005 |

Thumb means below are retired instructions per call, in typical / wide / hard / uniform order. [Measurement records](#measurement-records)

| Seed | Function | Former 50 | Merged entry |
|---:|---|---|---|
| 1001 | sigmoid | 37.7675 / 28.6190 / 47.7467 / 18.5040 | 37.7580 / 28.5700 / 47.6933 / 18.4900 |
| 1001 | tanh | 37.0715 / 20.6420 / 76.3700 / 14.6950 | 37.0590 / 20.6160 / 75.8667 / 14.6980 |
| 1001 | exp | 42.8235 / 34.6770 / 57.3667 / 20.3690 | 42.8235 / 34.6720 / 57.3367 / 20.3690 |
| 2002 | sigmoid | 37.8705 / 29.1390 / 46.9400 / 18.6330 | 37.8620 / 29.0950 / 46.9000 / 18.6200 |
| 2002 | tanh | 36.8840 / 20.8030 / 71.9500 / 14.2810 | 36.8730 / 20.7780 / 71.4067 / 14.2810 |
| 2002 | exp | 42.9285 / 34.4830 / 60.1467 / 19.8980 | 42.9285 / 34.4820 / 60.1200 / 19.8970 |
| 3003 | sigmoid | 38.0305 / 29.5780 / 45.4500 / 18.4680 | 38.0230 / 29.5240 / 45.4133 / 18.4550 |
| 3003 | tanh | 36.9580 / 19.8670 / 67.5067 / 14.7220 | 36.9510 / 19.8430 / 66.9867 / 14.7250 |
| 3003 | exp | 43.0120 / 34.0880 / 56.5867 / 19.9320 | 43.0120 / 34.0880 / 56.5500 / 19.9320 |
| 4004 | sigmoid | 37.5380 / 28.0960 / 44.9333 / 18.5280 | 37.5335 / 28.0610 / 44.8800 / 18.5160 |
| 4004 | tanh | 36.9155 / 20.6950 / 75.9333 / 14.5410 | 36.9010 / 20.6630 / 75.4433 / 14.5400 |
| 4004 | exp | 43.0215 / 35.3280 / 56.4267 / 20.1300 | 43.0215 / 35.3280 / 56.3933 / 20.1260 |
| 5005 | sigmoid | 37.7600 / 29.2480 / 48.4667 / 18.6640 | 37.7525 / 29.2010 / 48.4200 / 18.6580 |
| 5005 | tanh | 37.1920 / 19.7770 / 76.6700 / 14.4560 | 37.1820 / 19.7540 / 76.1700 / 14.4520 |
| 5005 | exp | 42.8520 / 34.3600 / 57.9667 / 20.3460 | 42.8520 / 34.3570 / 57.9333 / 20.3440 |
| 6006 | sigmoid | 37.8915 / 28.7890 / 43.2167 / 18.3520 | 37.8865 / 28.7570 / 43.1767 / 18.3380 |
| 6006 | tanh | 36.8750 / 20.4780 / 71.8500 / 14.4670 | 36.8635 / 20.4490 / 71.1600 / 14.4700 |
| 6006 | exp | 42.9650 / 35.1160 / 57.4633 / 20.4960 | 42.9650 / 35.1130 / 57.4333 / 20.4970 |

At fixed instruction counts, the 72-byte reduction lowers the size multiplier by 0.0419%. Typical exp is unchanged on all six seeds. The largest per-class instruction gain is in hard tanh, where the mean falls by 0.49–0.69 instructions. These shifts leave the common paths too close to former 50 to approach the takeover line. [Measurement records](#measurement-records) · [Pinned scoring implementation][score]

## Integration

The selected entry combines cold-code factoring, three exp edits, the tanh dispatch hunks and two extra shared tanh returns. Cold-code factoring already shared the third return. The source diff adjusts two blank lines in Thumb code to preserve the RV wrapper source positions for the complete object comparison. [Cold-code factoring][size-code] · [Tanh dispatch][dispatch-order] · [Tanh cold returns][tanh-hard-wide] · [Subnormal guard][exp-guard] · [Negative infinity][exp-neg-direct] · [Overflow transition][exp-reduction-m0]

The merge with both dispatch edits and the sigmoid sign-test hint shrank Thumb by 60 bytes but regressed on all three shared seeds. On seed 1001 the sigmoid typical mean rose from 37.7675 to 37.9595 and wide rose from 28.6190 to 28.6540. The tanh and exp improvements and the size savings did not offset that regression. Adding the sign-test hint to the exp and cold-code changes by themselves tied the same-seed scores. The score-neutral sigmoid guard edit and the unmeasured codegen hints stayed out. [Sigmoid sign-test hint][sig-via-shared] · [Sigmoid guard][sig-guard] · [Codegen notes][codegen-m0] · [Measurement records](#measurement-records)

Candidates were ranked by their worst ratio on the three shared seeds. The fixed selection then went to the three held-out seeds. The source diff below applies to the SHA-256-pinned former-50 entry. [Former-50 source][base] · [Merged diff](#entryc) · [Measurement records](#measurement-records)

| Integration variant | 1001 | 2002 | 3003 |
|---|---:|---:|---:|
| Selected merge | 0.99887794 | 0.99890356 | 0.99889290 |
| Selected merge without two additional tanh return edits | 0.99891453 | 0.99892484 | 0.99894031 |
| Cold code, exp and tanh dispatch without the subnormal exp guard edit | 0.99895057 | 0.99894704 | 0.99896064 |
| Cold code, exp and tanh dispatch without the overflow edit group | 0.99897341 | 0.99897526 | 0.99899390 |
| Cold code, exp and two additional tanh return edits | 0.99903971 | 0.99908997 | 0.99908638 |
| Cold code and exp | 0.99905305 | 0.99908804 | 0.99911059 |
| Cold code, exp and sigmoid sign-test hint | 0.99905305 | 0.99908804 | 0.99911059 |
| Cold code only | 0.99917316 | 0.99918576 | 0.99920971 |
| Cold code, exp, both dispatch parts, sign-test hint and extra returns | 1.00029803 | 1.00031851 | 1.00026125 |
| Cold code, exp, both dispatch parts and sign-test hint | 1.00033468 | 1.00033982 | 1.00030873 |
| Cold code, exp and both dispatch parts | 1.00041868 | 1.00041005 | 1.00038220 |
| Cold code and both dispatch parts | 1.00053897 | 1.00050793 | 1.00048149 |
| Cold code, exp and sigmoid dispatch | 1.00055741 | 1.00057350 | 1.00055272 |

The retained sequence below uses incremental measurements, with each row compared to the previous one. Positive S reductions are improvements. The exp row includes the portable overflow patch with the flagged source claims excluded from the evidence. Removing that group raised S on the shared seeds in the stock-kit ablation. [Measurement records](#measurement-records)

| Retained step | Scored bytes after step | S reduction, 1001 | 2002 | 3003 |
|---|---:|---:|---:|---:|
| Cold-code factoring and hints | 20,460 | +0.0827% | +0.0814% | +0.0790% |
| Three exp changes | 20,444 | +0.0120% | +0.0098% | +0.0099% |
| Tanh dispatch hunks | 20,444 | +0.0139% | +0.0163% | +0.0170% |
| Two additional shared tanh returns | 20,428 | +0.0037% | +0.0021% | +0.0047% |

## Correctness and policy

The kit's local gate accepted the entry against the baseline's normalized hash. The static build and policy result was `PASS {"functions": 42, "bytes": {"rv32im": 18960, "thumbv6m": 20428, "thumbv7em": 21226}, "stack_bound": {"rv32im": 176, "thumbv6m": 312, "thumbv7em": 272}}`. The RV32IM audit rebuilt both sources at the same pathname in a fresh scratch cache and compared their complete ELF objects. The shared SHA-256 was `9fc355d8f1691562012767a9044726cf40172030a927000b7e5ab857c7fcee4c`. The 18,960 scored RV32IM bytes refer to code plus tables. [Check records](#check-records) · [Pinned rules][rules]

| Function | Normal host ASan + UBSan | Forced Thumb C ASan + UBSan | Actual Thumbv6m object in QEMU |
|---|---|---|---|
| sigmoid | 4,294,967,296 words, 0 mismatches | 4,294,967,296 words, 0 mismatches | 4,294,967,296 words, 0 mismatches |
| tanh | 4,294,967,296 words, 0 mismatches | 4,294,967,296 words, 0 mismatches | 4,294,967,296 words, 0 mismatches |
| exp | 4,294,967,296 words, 0 mismatches | 4,294,967,296 words, 0 mismatches | 4,294,967,296 words, 0 mismatches |

The default host selects the RV-side C. The second host build explicitly selected Thumb in a scratch copy. For the host runs, the kit’s ASan+UBSan entry objects and unchanged checking harness were relinked with an OpenSSL SHA-256 wrapper for `er_sha256`. It hashes the same output chunks against the pinned digests. The stock host runs stopped before completion, so exhaustive results for that runner are **UNVERIFIED**. The Thumbv6m checks link the actual entry object and compare against the reference chunk digests. The QEMU ARM binary matched the prior toolkit pin. The measurements checked all scored outputs. Exhaustive RV32IM and Thumbv7em target execution of the merged entry are **UNVERIFIED** in this integration. Duplication against the full submission history and validator acceptance are **UNVERIFIED**. [Check records](#check-records) · [Pinned target checker][stages] · [Prior toolkit dependencies][toolkit] · [Reference digests][digests]

## What the 18 items established

The item scores below are standalone comparisons. Branch layout, literal pools and shared tails can change when patches are combined, so the standalone percentages cannot be added. Each item link identifies a supplied Markdown report. Some of those reports name separate files that were absent from the handoff. Where present, the inline diffs and embedded records are the evidence available to the write-up. Rejected trial variants are UNVERIFIED over the full domain unless a check is specifically noted.

| Item | Result and integration relevance |
|---|---|
| [size-code][size-code] | The strongest standalone result saved 40 scored bytes (20,500 to 20,460) and lowered S by 0.0790–0.0827% across the shared seeds. It shares cold accumulator preparation, joins a tanh refinement return, removes an unreachable sigmoid dispatch edge and adds three layout hints. Its dominant paths stayed at 32, 35 and 41 instructions for sigmoid, tanh and exp. The item reports nine exhaustive checks with zero mismatches. |
| [dispatch-order][dispatch-order] | Thumb S fell 0.0455–0.0601%, with four bytes saved. The positive sigmoid shoulder returns saturation or a quieted NaN before the lookup when the correction is zero. Tanh moves exact tiny-word returns ahead of the medium path and uses a cold layout hint. The exp dispatch trials were dropped. |
| [tanh-hard-wide][tanh-hard-wide] | Merging three refinement calls saved 24 bytes for a standalone S gain of about 0.007–0.009%. Hard instruction means rose slightly and wide was essentially flat. One of the three calls also appears in size-code. The rejected D1 branch removal illustrates why checking the executed Thumb path matters. Default host fullcheck passed, while Thumb targetcheck found 170 mismatches, including input `3c000000`, got `3bffff55`, expected `3bfffeab`. |
| [exp-reduction-m0][exp-reduction-m0] | The overflow-distance rewrite plus two layout hints saved four bytes and reported a local 0.0050–0.0059% S gain, with typical exp unchanged. Its first rewrite saved 336 bytes but raised seed-1001 exp typical from 42.8235 to 53.1170 by losing the load/dispatch arrangement. The item used an independent interpreter after the stock evaluator failed and produced different baseline S values. The handoff flags eight citations as unavailable or unsupported on reread. Those citations carry no weight here. The portable diff and its integer boundary argument were usable for integration, with stock-kit results needed for the score and Thumb verification. The interpreter's full-domain exp digest match is item-reported evidence. |
| [exp-guard][exp-guard] | Folding parity and subnormal midpoint remainder into an unsigned comparison saved eight bytes, improving S 0.0020–0.0036% with no typical exp gain. The normalized-guard rewrites regressed because they stopped reusing flags from formation of the estimate. The subnormal helper is shared with sigmoid and tanh. |
| [exp-neg-direct][exp-neg-direct] | The retained negative-infinity comparison preserves NaN quieting and saves one instruction on one hard case per seed, roughly 0.0002% of S at equal size. The best direct-index trial used 23,676 bytes and scored 1.100220–1.100862× base. It paid dispatch, coefficient and fallback costs on top of the larger table. The 128-cell-per-exponent trial passed exhaustive Thumb exp, while exhaustive host checking of that trial is UNVERIFIED. |
| [exp-neg-direct-b][exp-neg-direct-b] | Empty final diff. Narrowing the negative fast guard to four produced wrong outputs in exponent rows 8–11. The best added row for magnitudes 8–16 still had 12,785 fast-path mismatches with a guard band of 16 in the worker's range harness. Reduction-constant error can cross the side that this guard protects. These were local range experiments with a different measurement fingerprint. |
| [exp-grid-tradeoff][exp-grid-tradeoff] | Empty final diff. A guarded quadratic on the 512-step grid added 12 bytes, raised hard exp by 1.84–2.12 instructions and regressed S by 0.127–0.147%. Few typical calls reach the residual helper. The 256- and 1024-step grids are UNVERIFIED. A separate 1024-step grid was estimated at 3 KiB of extra words and about four typical exp instructions just to cover the size penalty. |
| [exp-wide-edges][exp-wide-edges] | Empty final diff. Exp wide stayed at 34.088–34.677 against a target of 30. A conservative overflow guard scored 1.00125× on seed 1001 and was dropped. Other trial seeds and full-domain correctness are UNVERIFIED. The item's compiler substitution changed its fingerprint. |
| [sig-via-shared][sig-via-shared] | Sigmoid already uses the shared `t_eps` bank. Replacing its 1,572-byte private `t_crows` bank with the existing exp tail increased the typical mean and produced 181, 172 and 195 wrong typical outputs. The retained `t_m6` sign-test hint improved S by about 0.0038–0.0049% at equal Thumb size, with typical unchanged. The item checked 23,068,672 Thumb words around the changed code and had no exhaustive QEMU result. |
| [sig-typ-cells][sig-typ-cells] | Empty final diff. Moving literals into cell descriptors raised S about 2.5%. More live values and the changed load layout outweighed the intended literal-load saving. These are within-item comparisons under a different fingerprint. |
| [sig-small-wide][sig-small-wide] | Empty final diff. The guarded linear shortcut for exponents 116–118 sped up the intended cells but introduced tests and worsened hot negative-table layout. Its wide mean reached 28.529 on seed 1001 (base 28.619, goal 25), while typical climbed from about 37.767 to 38.048 and aggregate S rose about 0.19%. |
| [sig-guard][sig-guard] | Its `t_drj` change narrows the slow window from below 13 to below 8. Exhaustive local enumeration found that the fast path needed correction only at residues 0–5 for that guard, but the change was score-neutral on all three seeds. Enumeration showed little useful slack in the other guards. Loading a mask to shorten a hot guard forced spills and raised seed-1001 sigmoid typical from about 37.77 to 42.62. |
| [tanh-typ-cells][tanh-typ-cells] | Empty final diff. Loading sign/exponent base relative to the bank added a live register and stack alignment instructions (+2.5–2.6% S). Biased indexing emitted a literal plus add (+1.4% S). A quadratic cell design with more cells was estimated and remains UNVERIFIED. |
| [tanh-cutoff-flags][tanh-cutoff-flags] | Empty final diff. The wider exponent-119 cutoff added eight bytes and cost 0.0370% S on seed 1001 because it replaced a shift/zero test with more expensive code. The historical interval enumeration in the item and exhaustive correctness of the trial are UNVERIFIED for this run. |
| [size-pack][size-pack] | Empty final diff. The item reported 99.3% of table bytes read and no duplicate rows. Reducing the exp row stride from 32 to 24 bytes saved a net 88 bytes but added about two exp typical instructions and roughly 1% S. The altered fingerprint limits the use of its absolute scores. |
| [size-cold-tables][size-cold-tables] | Empty final diff. Halving the exp row stride saved a net 180 bytes but broke its multi-register load, adding about three typical exp instructions and over 1.4% S. Reusing pad words for constants saved 32 bytes but increased sigmoid and tanh instruction counts. Reconstructing the 1 KiB hard-path residual table was an estimate and remains UNVERIFIED. |
| [codegen-m0][codegen-m0] | The prose describes three low-exponent hints but supplies no exact diff, score, successful build, or correctness check. All effects are UNVERIFIED. The handoff flags one external citation as unavailable or unsupported on reread. The result supplies no basis for selecting those hints. |

## Where to look next

1. Start with the common negative-exp path. The second negative-exp study counted 41 instructions on the fast exit over the main exponent range. Its breakdown identifies nine instructions for reduction and 12 for the polynomial. Try re-basing the reduction index to remove the large bias from the multiplication by the rounded constant, with the error bound derived for each row. A successful rewrite must take instructions out of the common path. Narrowing the existing guard or extending its range unchanged already produced counterexamples. [Negative exp profile][exp-neg-direct-b] · [Grid study][exp-grid-tradeoff]
2. Design sigmoid and tanh cells around the number of live values that the Thumb code needs. Inspect generated assembly for the common paths and check that they keep the existing multi-register loads and avoid extra stack adjustments before spending time on full measurements. Budget any new table against the pinned score formula. A single typical instruction per call is worth roughly 0.43–0.50% of S at the reported means, while 1 KiB at the baseline costs about 0.59%. [Sigmoid cells][sig-typ-cells] · [Tanh cells][tanh-typ-cells] · [Pinned score][score]
3. For the next substantial change, use the three shared seeds to screen actual codegen and preserve the held-out comparison for a fixed candidate. Require paired input digests and the pinned measurement fingerprint. Check all three actual Thumb functions if a shared helper or table moves. The tanh D1 counterexample shows that a normal-host pass can miss a real Thumb error. [Tanh refinement][tanh-hard-wide] · [Pinned checking rules][rules]

## entry.c

The final entry is the [pinned former-50 entry.c][base] plus this complete unified diff. The base SHA-256 is `88617bb49e36a06cabd7d84ce6fe504ee337f8f41ad7c55bc72f696db94060c3`. Save the fenced diff and apply it with `patch -p1` beside the base `entry.c`. The resulting one-file entry SHA-256 is `3ca88ea3b5a1ff4c015dd064f7fbc21d8a97c3be7527e600f921fd5e3504446c`. The write-up is the sole delivered file, so the patch and records are inlined here.

```diff
--- a/entry.c
+++ b/entry.c
@@ -2821,8 +2821,10 @@
   uint32_t t_rem = (t_q - (t_b * t_f)) >> 15;
   return (t_v + (((uint16_t) t_p) * t_f)) + ((t_rem * t_f) >> 15);
 }
-static uint32_t t_pd2(uint32_t w, uint32_t D3, uint32_t acc, uint32_t e2)
+/* Share the identical unsigned accumulator setup of both cold callers. */
+static uint32_t t_pd2(uint32_t w, uint32_t D3, uint32_t e2)
 {
+  uint32_t acc = (D3 * 0xA000u) << e2;
   uint32_t m = ((w << 9) >> 9) + 0x800000u;
   uint32_t a = (((w << 9) >> 9) + 0x800000u) >> 8;
   uint32_t v = (10u * (((w << 9) >> 9) + 0x800000u)) - D3;
@@ -2864,13 +2866,13 @@
 {
   uint32_t t_e2 = 30u & ~(t_base >> 22);
   uint32_t t_D3 = 3u * t_D;
-  return t_base + t_pd2(t_w, t_D3, (t_D3 * 0xA000u) << t_e2, t_e2);
+  return t_base + t_pd2(t_w, t_D3, t_e2);
 }
 inline static uint32_t t_pd_de2(uint32_t t_w, uint32_t t_D, uint32_t t_base)
 {
   uint32_t t_e2 = 30u & ~(t_w >> 22);
   uint32_t t_D3 = 3u * t_D;
-  return t_base + t_pd2(t_w, t_D3, (t_D3 * 0xA000u) << t_e2, t_e2);
+  return t_base + t_pd2(t_w, t_D3, t_e2);
 }
 inline static uint32_t t_tr(uint32_t t_w, uint32_t t_V)
 {
@@ -2997,22 +2999,22 @@
   {
     return (((t_P + 0x80000000u) >> t_sh) + 1u) >> 1;
   }
-  t_lo = t_P - (t_x << t_sh);
-  if (t_lo > 1u)
-  {
-    goto t_l992716;
-  }
-  if ((t_x & 1u) == 0u)
-  {
-    return t_x >> 1;
-  }
-  t_P = t_sh;
-  t_P = ((t_x << t_P) << 1) + 128u;
-  t_kb += 0x40000u;
-  t_lo = t_exp_res((t_P0 + ((t_kfn * 11640u) >> 16)) - 14530u, (t_kb >> 9) | (t_kb << 23), t_P);
-  t_lo = t_lo - (t_P >> 8);
-  return (t_x >> 1) + ((t_lo << 9) != 0u);
-  t_l992716:
+  /*
+   * Let d = 2^t_sh and r = t_P - t_x*d, with 0 <= r < d.
+   * Making the quotient odd leaves r intact for odd t_x.
+   * For even t_x the residual becomes r - d, which
+   * wraps above 1 as uint32_t and goes to the fast return.
+   */
+  uint32_t t_mid = (t_x | 1u) << t_sh;
+  if (t_P - t_mid <= 1u)
+  {
+    t_P = (t_mid << 1) + 128u;
+    t_kb += 0x40000u;
+    t_lo = t_exp_res((t_P0 + ((t_kfn * 11640u) >> 16)) - 14530u,
+                     (t_kb >> 9) | (t_kb << 23), t_P);
+    t_lo = t_lo - (t_P >> 8);
+    return (t_x >> 1) + ((t_lo << 9) != 0u);
+  }
   return (t_x + 1u) >> 1;
 }
 static const uint32_t t_tanh_sg[4] = {0x3F800000u, 0x3F000000u, 0xBF800000u, 0xBF000000u};
@@ -3191,11 +3193,11 @@
       if (t_Zc == 15u)
       {
         t_cs = 1549087090u;
-        if (t_M >= 0xC2CDBF37u)
+        if (__builtin_expect(t_M >= 0xC2CDBF37u, 0))
         {
           return t_w < 0xC2CFF1B5u;
         }
-        if (t_M >= 0xC2AEAC40u)
+        if (__builtin_expect(t_M >= 0xC2AEAC40u, 0))
         {
           if (t_w < 0xC2AEAC53u)
           {
@@ -3276,7 +3278,7 @@
         goto t_ns;
       }
       new_var12 = t_w;
-      return (!((t_w << 9) != 0u)) ? (0u) : (new_var12 | 0x00400000u);
+      return t_w == 0xff800000u ? 0u : (new_var12 | 0x00400000u);
     }
     return 0;
   }
@@ -3317,7 +3319,7 @@
       {
         goto t_lbp;
       }
-      if ((255u & t_Z) >= 7u)
+      if (__builtin_expect((255u & t_Z) >= 7u, 0))
       {
         return (((t_T - ((uint32_t) (t_S >> 9))) >> 3) >> 5) + (t_kb << 23);
       }
@@ -3350,18 +3352,18 @@
   }
   if (t_s == 15u)
   {
-    if (t_w >= 0x42B17216u)
-    {
-      if (t_w >= 0x42B17218u)
-      {
-        {
-          t_po = &t_infc;
-          goto t_onel;
-        }
-      }
-      return 0x7F7FFF04u + ((t_w - 0x42B17216u) << 7);
-    }
-    goto t_pb;
+    /* This exponent bucket lies strictly within 2^31 words of the cutoff. */
+    uint32_t distance = t_w - 0x42B17216u;
+    if (distance >> 31)
+    {
+      goto t_pb;
+    }
+    if (distance < 2u)
+    {
+      return 0x7F7FFF04u + (distance << 7);
+    }
+    t_po = &t_infc;
+    goto t_onel;
   }
   if (t_s == 137u)
   {
@@ -3579,7 +3581,7 @@
       const struct t_ep *t_bb = (const struct t_ep *) t_b;
       uint32_t t_n = new_var17;
       new_var14 = t_n;
-      if (new_var14 <= 223u)
+      if (__builtin_expect(new_var14 <= 223u, 1))
       {
         new_var10 = t_t;
         t_n = ((uint8_t) (t_bb[((int32_t) t_n) - 226].t_q >> 8)) & (new_var20 = new_var8);
@@ -3599,10 +3601,17 @@
   }
   new_var15 = t_w;
   new_var21 = new_var18 < 115;
-  if (new_var18 < 124)
-  {
-    goto t_l145631;
-  }
+  /* Below 124 the large polynomial is out of range.
+     Exponents below 115 use the exact input-word return,
+     preserving its sign, including signed zero.
+  */
+
+  if (new_var18 >= 124)
+    goto t_medium;
+  if (new_var18 < 115)
+    return t_w;
+  goto t_low;
+  t_medium:
   {
     if (127 == new_var18)
     {
@@ -3634,8 +3643,9 @@
       {
         return t_w - new_var22;
       }
-      new_var = (t_w - ((((t_w << 8) - t_Y) - 8u) >> 8)) + t_tr(t_w, (t_Y >> 4) | 0x18000008u);
-      return new_var;
+      t_hi = (t_w - ((((t_w << 8) - t_Y) - 8u) >> 8));
+      t_V = (t_Y >> 4) | 0x18000008u;
+      goto t_rj;
     }
     new_var3 = t_Y;
     new_var12 = (int32_t) (new_var3 << new_var11);
@@ -3645,7 +3655,7 @@
     if (new_var19)
     {
       uint32_t t_z = (new_var3 << new_var11) + new_var10;
-      if ((255u & t_z) < 7u)
+      if (__builtin_expect((255u & t_z) < 7u, 0))
       {
         {
           t_hi = (t_w + ((uint32_t) (((int32_t) (t_z - (t_w << 8))) >> 8))) + 1u;
@@ -3666,7 +3676,9 @@
           new_var12 = t_w - ((new_var16 - t_z) >> 5);
           return new_var12;
         }
-        return ((((new_var7 - 6u) << new_var6) + (t_z >> 5)) - (-1u)) + t_tr(t_w, (t_z >> 4) + 0x6000001u);
+        t_hi = (((new_var7 - 6u) << new_var6) + (t_z >> 5)) - (-1u);
+        t_V = (t_z >> 4) + 0x6000001u;
+        goto t_rj;
       }
       uint32_t t_dd = (t_w << 6) - t_z;
       if ((t_z & 63u) >= 4u)
@@ -3674,8 +3686,9 @@
         return t_w - (t_dd >> 6);
       }
       {
-        uint32_t t_hi = t_w - ((t_dd - 1u) >> 6);
-        return t_hi + t_tr(t_w, (t_z >> 4) + 0xA000002u);
+        t_hi = t_w - ((t_dd - 1u) >> 6);
+        t_V = (t_z >> 4) + 0xA000002u;
+        goto t_rj;
       }
     }
   }
@@ -3854,13 +3867,6 @@
   goto t_ev11;
 
   return t_tw_low2(t_t, t_r);
-  t_l145631:
-  if (new_var18 < 115)
-  {
-    return t_w;
-  }
-
-  goto t_low;
 }
 struct t_cbank{uint32_t t_p,t_v,t_q;};
 static const struct t_cbank t_crows[]={
@@ -4506,7 +4512,7 @@
       {
         return (new_var3 + (t_U >> 13)) >> 1;
       }
-      if ((t_w * t_w) == 5u)
+      if (__builtin_expect((t_w * t_w) == 5u, 0))
       {
         t_r = &t_eps[t_w & 255u].t_q;
         uint32_t t_c = t_exp_den(t_w);
@@ -4582,10 +4588,6 @@
         {
           goto t_ev14;
         }
-        if (t_c == 24u)
-        {
-          goto t_ev3;
-        }
         if (t_c == 60u)
         {
           goto t_ev18;
@@ -4705,7 +4707,6 @@
     t_d2 = t_d1->t_n;
     t_ev19:
     ;
-
     ;
     ;
     ;
@@ -4723,7 +4724,6 @@
     t_dt = t_d2->t_tb;
     t_ev21:
     ;
-
     ;
     ;
     ;
```

## Measurement records

Compact extracts of the local kit reports. Each seed's records include build size, source and image hashes, input digest, score and target class means and hard-tail counts. Shared-seed screening rows list seed, S, bytes and the four class means for sigmoid, tanh and exp, in that order. They used the same per-seed inputs and pinned kit. [Pinned measurement code][stages]

```jsonl
{"bytes":{"rv32im":18960,"thumbv6m":20500,"thumbv7em":21254},"entry":"former-50","fingerprint":{"measurement":"2c8fd1f3a6711f0639685319fb25262b02bfecf4c6589c52cb58928270a46322","sandbox":"none","verifier":"ebbf9d5cac596a718532b34798dc452e4050d6940594005c44f9a729c699c5a8"},"hard_pool":{"samples":67108864,"sizes":{"exp":414,"sigmoid":534,"tanh":207},"source":"hardscan","threshold_log2_ulps":-18},"images":{"rv32im":"8cdb9ae3f362b7eca11b12e3cf6f8a1a52a6b9880279dfad68922819eca1b44f","thumbv6m":"8ccc26cac9bf7049ad4dc029a713d7663c4a222644fa3b53574cf95dcb7be6e1"},"inputs_sha256":"8a95019108936ba0a8e4085f1551587f58f2478d83746a4aad8915fc78ae9359","sampled":false,"scores":{"rv32im":{"S":28.486293712128862},"thumbv6m":{"S":40.357409443438364}},"seed":1001,"sha256":"88617bb49e36a06cabd7d84ce6fe504ee337f8f41ad7c55bc72f696db94060c3","target_counts":{"rv32im":{"hard_p999":{"exp":83,"sigmoid":152,"tanh":73},"means_typical_wide_hard_uniform":{"exp":[30.3245,24.948,41.57666666666667,13.773],"sigmoid":[29.153,20.177,31.93,12.226],"tanh":[25.7695,14.329,53.06333333333333,9.192]},"stack":8,"wrong":[]},"thumbv6m":{"hard_p999":{"exp":146,"sigmoid":178,"tanh":117},"means_typical_wide_hard_uniform":{"exp":[42.8235,34.677,57.36666666666667,20.369],"sigmoid":[37.7675,28.619,47.74666666666667,18.504],"tanh":[37.0715,20.642,76.37,14.695]},"stack":60,"wrong":[]}},"verdict":"passed"}
{"bytes":{"rv32im":18960,"thumbv6m":20428,"thumbv7em":21226},"entry":"merged","fingerprint":{"measurement":"2c8fd1f3a6711f0639685319fb25262b02bfecf4c6589c52cb58928270a46322","sandbox":"none","verifier":"ebbf9d5cac596a718532b34798dc452e4050d6940594005c44f9a729c699c5a8"},"hard_pool":{"samples":67108864,"sizes":{"exp":414,"sigmoid":534,"tanh":207},"source":"hardscan","threshold_log2_ulps":-18},"images":{"rv32im":"714db1c7d31b0d054d54193503c8f20018b6477696a79343e819b1a16af0bb7d","thumbv6m":"62c15e58bba752795bf9b5ef2bb34edd80f320e8bfbd75b78220744037036a07"},"inputs_sha256":"8a95019108936ba0a8e4085f1551587f58f2478d83746a4aad8915fc78ae9359","sampled":false,"scores":{"rv32im":{"S":28.486293712128862},"thumbv6m":{"S":40.312125906721974}},"seed":1001,"sha256":"3ca88ea3b5a1ff4c015dd064f7fbc21d8a97c3be7527e600f921fd5e3504446c","target_counts":{"rv32im":{"hard_p999":{"exp":83,"sigmoid":152,"tanh":73},"means_typical_wide_hard_uniform":{"exp":[30.3245,24.948,41.57666666666667,13.773],"sigmoid":[29.153,20.177,31.93,12.226],"tanh":[25.7695,14.329,53.06333333333333,9.192]},"stack":8,"wrong":[]},"thumbv6m":{"hard_p999":{"exp":146,"sigmoid":177,"tanh":117},"means_typical_wide_hard_uniform":{"exp":[42.8235,34.672,57.336666666666666,20.369],"sigmoid":[37.758,28.57,47.693333333333335,18.49],"tanh":[37.059,20.616,75.86666666666666,14.698]},"stack":60,"wrong":[]}},"verdict":"passed"}
{"bytes":{"rv32im":18960,"thumbv6m":20500,"thumbv7em":21254},"entry":"former-50","fingerprint":{"measurement":"2c8fd1f3a6711f0639685319fb25262b02bfecf4c6589c52cb58928270a46322","sandbox":"none","verifier":"ebbf9d5cac596a718532b34798dc452e4050d6940594005c44f9a729c699c5a8"},"hard_pool":{"samples":67108864,"sizes":{"exp":444,"sigmoid":614,"tanh":154},"source":"hardscan","threshold_log2_ulps":-18},"images":{"rv32im":"8cdb9ae3f362b7eca11b12e3cf6f8a1a52a6b9880279dfad68922819eca1b44f","thumbv6m":"8ccc26cac9bf7049ad4dc029a713d7663c4a222644fa3b53574cf95dcb7be6e1"},"inputs_sha256":"4725e74fc7c608b4c347b26e2a71d52d768102f14426c675c0e52ae72d3a1213","sampled":false,"scores":{"rv32im":{"S":28.517988427052867},"thumbv6m":{"S":40.36980095734065}},"seed":2002,"sha256":"88617bb49e36a06cabd7d84ce6fe504ee337f8f41ad7c55bc72f696db94060c3","target_counts":{"rv32im":{"hard_p999":{"exp":83,"sigmoid":146,"tanh":73},"means_typical_wide_hard_uniform":{"exp":[30.5165,25.074,43.97666666666667,13.101],"sigmoid":[28.9335,20.403,31.456666666666667,12.301],"tanh":[25.6635,14.599,50.873333333333335,8.854]},"stack":8,"wrong":[]},"thumbv6m":{"hard_p999":{"exp":146,"sigmoid":187,"tanh":117},"means_typical_wide_hard_uniform":{"exp":[42.9285,34.483,60.14666666666667,19.898],"sigmoid":[37.8705,29.139,46.94,18.633],"tanh":[36.884,20.803,71.95,14.281]},"stack":60,"wrong":[]}},"verdict":"passed"}
{"bytes":{"rv32im":18960,"thumbv6m":20428,"thumbv7em":21226},"entry":"merged","fingerprint":{"measurement":"2c8fd1f3a6711f0639685319fb25262b02bfecf4c6589c52cb58928270a46322","sandbox":"none","verifier":"ebbf9d5cac596a718532b34798dc452e4050d6940594005c44f9a729c699c5a8"},"hard_pool":{"samples":67108864,"sizes":{"exp":444,"sigmoid":614,"tanh":154},"source":"hardscan","threshold_log2_ulps":-18},"images":{"rv32im":"714db1c7d31b0d054d54193503c8f20018b6477696a79343e819b1a16af0bb7d","thumbv6m":"62c15e58bba752795bf9b5ef2bb34edd80f320e8bfbd75b78220744037036a07"},"inputs_sha256":"4725e74fc7c608b4c347b26e2a71d52d768102f14426c675c0e52ae72d3a1213","sampled":false,"scores":{"rv32im":{"S":28.517988427052867},"thumbv6m":{"S":40.32553769951748}},"seed":2002,"sha256":"3ca88ea3b5a1ff4c015dd064f7fbc21d8a97c3be7527e600f921fd5e3504446c","target_counts":{"rv32im":{"hard_p999":{"exp":83,"sigmoid":146,"tanh":73},"means_typical_wide_hard_uniform":{"exp":[30.5165,25.074,43.97666666666667,13.101],"sigmoid":[28.9335,20.403,31.456666666666667,12.301],"tanh":[25.6635,14.599,50.873333333333335,8.854]},"stack":8,"wrong":[]},"thumbv6m":{"hard_p999":{"exp":146,"sigmoid":186,"tanh":117},"means_typical_wide_hard_uniform":{"exp":[42.9285,34.482,60.12,19.897],"sigmoid":[37.862,29.095,46.9,18.62],"tanh":[36.873,20.778,71.40666666666667,14.281]},"stack":60,"wrong":[]}},"verdict":"passed"}
{"bytes":{"rv32im":18960,"thumbv6m":20500,"thumbv7em":21254},"entry":"former-50","fingerprint":{"measurement":"2c8fd1f3a6711f0639685319fb25262b02bfecf4c6589c52cb58928270a46322","sandbox":"none","verifier":"ebbf9d5cac596a718532b34798dc452e4050d6940594005c44f9a729c699c5a8"},"hard_pool":{"samples":67108864,"sizes":{"exp":410,"sigmoid":593,"tanh":193},"source":"hardscan","threshold_log2_ulps":-18},"images":{"rv32im":"8cdb9ae3f362b7eca11b12e3cf6f8a1a52a6b9880279dfad68922819eca1b44f","thumbv6m":"8ccc26cac9bf7049ad4dc029a713d7663c4a222644fa3b53574cf95dcb7be6e1"},"inputs_sha256":"74546119d2ab88a5869c516e6b28be50def77cb3c39635ca3b64b4d175ba618b","sampled":false,"scores":{"rv32im":{"S":28.22021703206856},"thumbv6m":{"S":40.06372945286978}},"seed":3003,"sha256":"88617bb49e36a06cabd7d84ce6fe504ee337f8f41ad7c55bc72f696db94060c3","target_counts":{"rv32im":{"hard_p999":{"exp":90,"sigmoid":152,"tanh":73},"means_typical_wide_hard_uniform":{"exp":[30.493,24.664,41.513333333333335,13.115],"sigmoid":[28.8875,20.586,30.65,12.135],"tanh":[25.684,13.904,47.91,9.08]},"stack":8,"wrong":[]},"thumbv6m":{"hard_p999":{"exp":153,"sigmoid":178,"tanh":117},"means_typical_wide_hard_uniform":{"exp":[43.012,34.088,56.586666666666666,19.932],"sigmoid":[38.0305,29.578,45.45,18.468],"tanh":[36.958,19.867,67.50666666666666,14.722]},"stack":60,"wrong":[]}},"verdict":"passed"}
{"bytes":{"rv32im":18960,"thumbv6m":20428,"thumbv7em":21226},"entry":"merged","fingerprint":{"measurement":"2c8fd1f3a6711f0639685319fb25262b02bfecf4c6589c52cb58928270a46322","sandbox":"none","verifier":"ebbf9d5cac596a718532b34798dc452e4050d6940594005c44f9a729c699c5a8"},"hard_pool":{"samples":67108864,"sizes":{"exp":410,"sigmoid":593,"tanh":193},"source":"hardscan","threshold_log2_ulps":-18},"images":{"rv32im":"714db1c7d31b0d054d54193503c8f20018b6477696a79343e819b1a16af0bb7d","thumbv6m":"62c15e58bba752795bf9b5ef2bb34edd80f320e8bfbd75b78220744037036a07"},"inputs_sha256":"74546119d2ab88a5869c516e6b28be50def77cb3c39635ca3b64b4d175ba618b","sampled":false,"scores":{"rv32im":{"S":28.22021703206856},"thumbv6m":{"S":40.01937504056571}},"seed":3003,"sha256":"3ca88ea3b5a1ff4c015dd064f7fbc21d8a97c3be7527e600f921fd5e3504446c","target_counts":{"rv32im":{"hard_p999":{"exp":90,"sigmoid":152,"tanh":73},"means_typical_wide_hard_uniform":{"exp":[30.493,24.664,41.513333333333335,13.115],"sigmoid":[28.8875,20.586,30.65,12.135],"tanh":[25.684,13.904,47.91,9.08]},"stack":8,"wrong":[]},"thumbv6m":{"hard_p999":{"exp":152,"sigmoid":177,"tanh":117},"means_typical_wide_hard_uniform":{"exp":[43.012,34.088,56.55,19.932],"sigmoid":[38.023,29.524,45.413333333333334,18.455],"tanh":[36.951,19.843,66.98666666666666,14.725]},"stack":60,"wrong":[]}},"verdict":"passed"}
{"bytes":{"rv32im":18960,"thumbv6m":20500,"thumbv7em":21254},"entry":"former-50","fingerprint":{"measurement":"2c8fd1f3a6711f0639685319fb25262b02bfecf4c6589c52cb58928270a46322","sandbox":"none","verifier":"ebbf9d5cac596a718532b34798dc452e4050d6940594005c44f9a729c699c5a8"},"hard_pool":{"samples":67108864,"sizes":{"exp":423,"sigmoid":556,"tanh":164},"source":"hardscan","threshold_log2_ulps":-18},"images":{"rv32im":"8cdb9ae3f362b7eca11b12e3cf6f8a1a52a6b9880279dfad68922819eca1b44f","thumbv6m":"8ccc26cac9bf7049ad4dc029a713d7663c4a222644fa3b53574cf95dcb7be6e1"},"inputs_sha256":"e6fe1cddfe2702ee9d2c62e0e778ad695ffc733f47dabf22c7f68a029f6dded6","sampled":false,"scores":{"rv32im":{"S":28.39747848301774},"thumbv6m":{"S":40.200735026570506}},"seed":4004,"sha256":"88617bb49e36a06cabd7d84ce6fe504ee337f8f41ad7c55bc72f696db94060c3","target_counts":{"rv32im":{"hard_p999":{"exp":90,"sigmoid":111,"tanh":92},"means_typical_wide_hard_uniform":{"exp":[30.5835,25.688,41.49,13.37],"sigmoid":[28.8775,19.732,30.316666666666666,12.229],"tanh":[25.618,14.375,52.696666666666665,8.999]},"stack":0,"wrong":[]},"thumbv6m":{"hard_p999":{"exp":154,"sigmoid":187,"tanh":117},"means_typical_wide_hard_uniform":{"exp":[43.0215,35.328,56.42666666666667,20.13],"sigmoid":[37.538,28.096,44.93333333333333,18.528],"tanh":[36.9155,20.695,75.93333333333334,14.541]},"stack":60,"wrong":[]}},"verdict":"passed"}
{"bytes":{"rv32im":18960,"thumbv6m":20428,"thumbv7em":21226},"entry":"merged","fingerprint":{"measurement":"2c8fd1f3a6711f0639685319fb25262b02bfecf4c6589c52cb58928270a46322","sandbox":"none","verifier":"ebbf9d5cac596a718532b34798dc452e4050d6940594005c44f9a729c699c5a8"},"hard_pool":{"samples":67108864,"sizes":{"exp":423,"sigmoid":556,"tanh":164},"source":"hardscan","threshold_log2_ulps":-18},"images":{"rv32im":"714db1c7d31b0d054d54193503c8f20018b6477696a79343e819b1a16af0bb7d","thumbv6m":"62c15e58bba752795bf9b5ef2bb34edd80f320e8bfbd75b78220744037036a07"},"inputs_sha256":"e6fe1cddfe2702ee9d2c62e0e778ad695ffc733f47dabf22c7f68a029f6dded6","sampled":false,"scores":{"rv32im":{"S":28.39747848301774},"thumbv6m":{"S":40.15724746904942}},"seed":4004,"sha256":"3ca88ea3b5a1ff4c015dd064f7fbc21d8a97c3be7527e600f921fd5e3504446c","target_counts":{"rv32im":{"hard_p999":{"exp":90,"sigmoid":111,"tanh":92},"means_typical_wide_hard_uniform":{"exp":[30.5835,25.688,41.49,13.37],"sigmoid":[28.8775,19.732,30.316666666666666,12.229],"tanh":[25.618,14.375,52.696666666666665,8.999]},"stack":0,"wrong":[]},"thumbv6m":{"hard_p999":{"exp":153,"sigmoid":186,"tanh":117},"means_typical_wide_hard_uniform":{"exp":[43.0215,35.328,56.39333333333333,20.126],"sigmoid":[37.5335,28.061,44.88,18.516],"tanh":[36.901,20.663,75.44333333333333,14.54]},"stack":60,"wrong":[]}},"verdict":"passed"}
{"bytes":{"rv32im":18960,"thumbv6m":20500,"thumbv7em":21254},"entry":"former-50","fingerprint":{"measurement":"2c8fd1f3a6711f0639685319fb25262b02bfecf4c6589c52cb58928270a46322","sandbox":"none","verifier":"ebbf9d5cac596a718532b34798dc452e4050d6940594005c44f9a729c699c5a8"},"hard_pool":{"samples":67108864,"sizes":{"exp":434,"sigmoid":584,"tanh":180},"source":"hardscan","threshold_log2_ulps":-18},"images":{"rv32im":"8cdb9ae3f362b7eca11b12e3cf6f8a1a52a6b9880279dfad68922819eca1b44f","thumbv6m":"8ccc26cac9bf7049ad4dc029a713d7663c4a222644fa3b53574cf95dcb7be6e1"},"inputs_sha256":"c2c9124a6d705957c1aa4b947356482954c40979f0e06c38304c8972675f1b26","sampled":false,"scores":{"rv32im":{"S":28.355062768709992},"thumbv6m":{"S":40.29623992603655}},"seed":5005,"sha256":"88617bb49e36a06cabd7d84ce6fe504ee337f8f41ad7c55bc72f696db94060c3","target_counts":{"rv32im":{"hard_p999":{"exp":90,"sigmoid":152,"tanh":90},"means_typical_wide_hard_uniform":{"exp":[30.3865,24.823,42.376666666666665,13.482],"sigmoid":[28.9915,20.427,32.083333333333336,12.294],"tanh":[25.7755,13.661,52.443333333333335,9.131]},"stack":8,"wrong":[]},"thumbv6m":{"hard_p999":{"exp":153,"sigmoid":187,"tanh":117},"means_typical_wide_hard_uniform":{"exp":[42.852,34.36,57.96666666666667,20.346],"sigmoid":[37.76,29.248,48.46666666666667,18.664],"tanh":[37.192,19.777,76.67,14.456]},"stack":60,"wrong":[]}},"verdict":"passed"}
{"bytes":{"rv32im":18960,"thumbv6m":20428,"thumbv7em":21226},"entry":"merged","fingerprint":{"measurement":"2c8fd1f3a6711f0639685319fb25262b02bfecf4c6589c52cb58928270a46322","sandbox":"none","verifier":"ebbf9d5cac596a718532b34798dc452e4050d6940594005c44f9a729c699c5a8"},"hard_pool":{"samples":67108864,"sizes":{"exp":434,"sigmoid":584,"tanh":180},"source":"hardscan","threshold_log2_ulps":-18},"images":{"rv32im":"714db1c7d31b0d054d54193503c8f20018b6477696a79343e819b1a16af0bb7d","thumbv6m":"62c15e58bba752795bf9b5ef2bb34edd80f320e8bfbd75b78220744037036a07"},"inputs_sha256":"c2c9124a6d705957c1aa4b947356482954c40979f0e06c38304c8972675f1b26","sampled":false,"scores":{"rv32im":{"S":28.355062768709992},"thumbv6m":{"S":40.25309647926102}},"seed":5005,"sha256":"3ca88ea3b5a1ff4c015dd064f7fbc21d8a97c3be7527e600f921fd5e3504446c","target_counts":{"rv32im":{"hard_p999":{"exp":90,"sigmoid":152,"tanh":90},"means_typical_wide_hard_uniform":{"exp":[30.3865,24.823,42.376666666666665,13.482],"sigmoid":[28.9915,20.427,32.083333333333336,12.294],"tanh":[25.7755,13.661,52.443333333333335,9.131]},"stack":8,"wrong":[]},"thumbv6m":{"hard_p999":{"exp":152,"sigmoid":186,"tanh":117},"means_typical_wide_hard_uniform":{"exp":[42.852,34.357,57.93333333333333,20.344],"sigmoid":[37.7525,29.201,48.42,18.658],"tanh":[37.182,19.754,76.17,14.452]},"stack":60,"wrong":[]}},"verdict":"passed"}
{"bytes":{"rv32im":18960,"thumbv6m":20500,"thumbv7em":21254},"entry":"former-50","fingerprint":{"measurement":"2c8fd1f3a6711f0639685319fb25262b02bfecf4c6589c52cb58928270a46322","sandbox":"none","verifier":"ebbf9d5cac596a718532b34798dc452e4050d6940594005c44f9a729c699c5a8"},"hard_pool":{"samples":67108864,"sizes":{"exp":392,"sigmoid":559,"tanh":214},"source":"hardscan","threshold_log2_ulps":-18},"images":{"rv32im":"8cdb9ae3f362b7eca11b12e3cf6f8a1a52a6b9880279dfad68922819eca1b44f","thumbv6m":"8ccc26cac9bf7049ad4dc029a713d7663c4a222644fa3b53574cf95dcb7be6e1"},"inputs_sha256":"b6f1d6a6638ec877b3d3fdb702f0b19911165423e2aa6b2165c2e491b2405861","sampled":false,"scores":{"rv32im":{"S":28.358060049651765},"thumbv6m":{"S":40.18381066939278}},"seed":6006,"sha256":"88617bb49e36a06cabd7d84ce6fe504ee337f8f41ad7c55bc72f696db94060c3","target_counts":{"rv32im":{"hard_p999":{"exp":83,"sigmoid":111,"tanh":92},"means_typical_wide_hard_uniform":{"exp":[30.5415,25.21,42.736666666666665,13.744],"sigmoid":[29.088,20.344,29.22,12.009],"tanh":[25.5705,14.078,50.78666666666667,9.052]},"stack":0,"wrong":[]},"thumbv6m":{"hard_p999":{"exp":146,"sigmoid":187,"tanh":117},"means_typical_wide_hard_uniform":{"exp":[42.965,35.116,57.46333333333333,20.496],"sigmoid":[37.8915,28.789,43.21666666666667,18.352],"tanh":[36.875,20.478,71.85,14.467]},"stack":60,"wrong":[]}},"verdict":"passed"}
{"bytes":{"rv32im":18960,"thumbv6m":20428,"thumbv7em":21226},"entry":"merged","fingerprint":{"measurement":"2c8fd1f3a6711f0639685319fb25262b02bfecf4c6589c52cb58928270a46322","sandbox":"none","verifier":"ebbf9d5cac596a718532b34798dc452e4050d6940594005c44f9a729c699c5a8"},"hard_pool":{"samples":67108864,"sizes":{"exp":392,"sigmoid":559,"tanh":214},"source":"hardscan","threshold_log2_ulps":-18},"images":{"rv32im":"714db1c7d31b0d054d54193503c8f20018b6477696a79343e819b1a16af0bb7d","thumbv6m":"62c15e58bba752795bf9b5ef2bb34edd80f320e8bfbd75b78220744037036a07"},"inputs_sha256":"b6f1d6a6638ec877b3d3fdb702f0b19911165423e2aa6b2165c2e491b2405861","sampled":false,"scores":{"rv32im":{"S":28.358060049651765},"thumbv6m":{"S":40.13803369138816}},"seed":6006,"sha256":"3ca88ea3b5a1ff4c015dd064f7fbc21d8a97c3be7527e600f921fd5e3504446c","target_counts":{"rv32im":{"hard_p999":{"exp":83,"sigmoid":111,"tanh":92},"means_typical_wide_hard_uniform":{"exp":[30.5415,25.21,42.736666666666665,13.744],"sigmoid":[29.088,20.344,29.22,12.009],"tanh":[25.5705,14.078,50.78666666666667,9.052]},"stack":0,"wrong":[]},"thumbv6m":{"hard_p999":{"exp":146,"sigmoid":186,"tanh":117},"means_typical_wide_hard_uniform":{"exp":[42.965,35.113,57.43333333333333,20.497],"sigmoid":[37.8865,28.757,43.17666666666667,18.338],"tanh":[36.8635,20.449,71.16,14.47]},"stack":60,"wrong":[]}},"verdict":"passed"}
{"rows":[[1001,40.312125906721974,20428,[37.758,28.57,47.693333333333335,18.49],[37.059,20.616,75.86666666666666,14.698],[42.8235,34.672,57.336666666666666,20.369]],[2002,40.32553769951748,20428,[37.862,29.095,46.9,18.62],[36.873,20.778,71.40666666666667,14.281],[42.9285,34.482,60.12,19.897]],[3003,40.01937504056571,20428,[38.023,29.524,45.413333333333334,18.455],[36.951,19.843,66.98666666666666,14.725],[43.012,34.088,56.55,19.932]]],"screen":"Selected merge","source_sha256":"3ca88ea3b5a1ff4c015dd064f7fbc21d8a97c3be7527e600f921fd5e3504446c"}
{"rows":[[1001,40.31360257310605,20444,[37.758,28.57,47.693333333333335,18.49],[37.055,20.616,75.78333333333333,14.698],[42.8235,34.672,57.336666666666666,20.369]],[2002,40.326396823896964,20444,[37.862,29.095,46.9,18.62],[36.8705,20.777,71.29,14.281],[42.9285,34.482,60.12,19.897]],[3003,40.02127435324784,20444,[38.023,29.524,45.413333333333334,18.455],[36.9485,19.843,66.92,14.725],[43.012,34.088,56.55,19.932]]],"screen":"Selected merge without two additional tanh return edits","source_sha256":"0baa19e54e480e2b6807bf6d8815ba26b55281274292099c575c49c1077e6c01"}
{"rows":[[1001,40.31505714620577,20452,[37.758,28.568,47.696666666666665,18.49],[37.055,20.616,75.78333333333333,14.698],[42.8235,34.67,57.336666666666666,20.369]],[2002,40.327292986981824,20452,[37.862,29.091,46.9,18.62],[36.8705,20.777,71.29,14.281],[42.9285,34.479,60.11666666666667,19.897]],[3003,40.022088761159,20452,[38.023,29.518,45.42,18.455],[36.9485,19.843,66.92,14.725],[43.012,34.083,56.556666666666665,19.932]]],"screen":"Cold code, exp and tanh dispatch without the subnormal exp guard edit","source_sha256":"c5916b2ab017242b76eb64c51ba8ffd5e090f59671e211bce15f027012401096"}
{"rows":[[1001,40.315979017826926,20448,[37.758,28.57,47.693333333333335,18.49],[37.055,20.616,75.78333333333333,14.698],[42.8235,34.679,57.36333333333334,20.369]],[2002,40.32843254603559,20448,[37.862,29.095,46.9,18.62],[36.8705,20.777,71.29,14.281],[42.9285,34.486,60.14666666666667,19.898]],[3003,40.02342125030264,20448,[38.023,29.524,45.413333333333334,18.455],[36.9485,19.843,66.92,14.725],[43.012,34.093,56.57666666666667,19.932]]],"screen":"Cold code, exp and tanh dispatch without the overflow edit group","source_sha256":"c048b82f570e95357bf1e82b0868da42a2fbbb71baef525588f215aeb4dd1d55"}
{"rows":[[1001,40.318654448435275,20432,[37.758,28.57,47.693333333333335,18.49],[37.0735,20.634,75.83333333333333,14.693],[42.8235,34.672,57.336666666666666,20.369]],[2002,40.33306332379151,20432,[37.862,29.095,46.9,18.62],[36.884,20.798,71.43333333333334,14.281],[42.9285,34.482,60.12,19.897]],[3003,40.02712637995322,20432,[38.023,29.524,45.413333333333334,18.455],[36.9595,19.863,67.05333333333333,14.72],[43.012,34.088,56.55,19.932]]],"screen":"Cold code, exp and two additional tanh return edits","source_sha256":"6cfca70e7cb50442b5df78120a48dbfd502c370784034c48f04d34b06991fa4f"}
{"rows":[[1001,40.319192979018176,20444,[37.758,28.57,47.693333333333335,18.49],[37.0695,20.634,75.75,14.693],[42.8235,34.672,57.336666666666666,20.369]],[2002,40.332985407779205,20444,[37.862,29.095,46.9,18.62],[36.8815,20.797,71.31666666666666,14.281],[42.9285,34.482,60.12,19.897]],[3003,40.02809623133074,20444,[38.023,29.524,45.413333333333334,18.455],[36.957,19.863,66.98666666666666,14.72],[43.012,34.088,56.55,19.932]]],"screen":"Cold code and exp","source_sha256":"44ac7523c077baf3bdaeb7e97d544e58fe49087067f5a69b4fde400bb40b6cb3"}
{"rows":[[1001,40.319192979018176,20444,[37.758,28.57,47.693333333333335,18.49],[37.0695,20.634,75.75,14.693],[42.8235,34.672,57.336666666666666,20.369]],[2002,40.332985407779205,20444,[37.862,29.095,46.9,18.62],[36.8815,20.797,71.31666666666666,14.281],[42.9285,34.482,60.12,19.897]],[3003,40.02809623133074,20444,[38.023,29.524,45.413333333333334,18.455],[36.957,19.863,66.98666666666666,14.72],[43.012,34.088,56.55,19.932]]],"screen":"Cold code, exp and sigmoid sign-test hint","source_sha256":"f8bf14973f94b7e45508e51f255f5e99b42d83c7bc9b310bddfc8fa8274c5c65"}
{"rows":[[1001,40.32404049878967,20460,[37.758,28.568,47.696666666666665,18.49],[37.0695,20.634,75.75,14.693],[42.8235,34.677,57.36666666666667,20.369]],[2002,40.33693044256164,20460,[37.862,29.091,46.9,18.62],[36.8815,20.797,71.31666666666666,14.281],[42.9285,34.483,60.14666666666667,19.898]],[3003,40.03206764820558,20460,[38.023,29.518,45.42,18.455],[36.957,19.863,66.98666666666666,14.72],[43.012,34.088,56.586666666666666,19.932]]],"screen":"Cold code only","source_sha256":"bfef9722512964a63d26c739b2c28b45ea12f07928026a2c14047062a735e81f"}
{"rows":[[1001,40.369437321705725,20424,[37.9595,28.654,47.67,18.703],[37.059,20.616,75.86666666666666,14.698],[42.8235,34.672,57.336666666666666,20.369]],[2002,40.38265905462216,20424,[38.0565,29.174,46.913333333333334,18.866],[36.873,20.778,71.40666666666667,14.281],[42.9285,34.482,60.12,19.897]],[3003,40.074196246174104,20424,[38.2205,29.594,45.38666666666666,18.706],[36.951,19.843,66.98666666666666,14.725],[43.012,34.088,56.55,19.932]]],"screen":"Cold code, exp, both dispatch parts, sign-test hint and extra returns","source_sha256":"383b908b0865837bec52de07118011550541629f78ebadda6877f279913d7932"}
{"rows":[[1001,40.37091626224738,20440,[37.9595,28.654,47.67,18.703],[37.055,20.616,75.78333333333333,14.698],[42.8235,34.672,57.336666666666666,20.369]],[2002,40.38351957080408,20440,[38.0565,29.174,46.913333333333334,18.866],[36.8705,20.777,71.29,14.281],[42.9285,34.482,60.12,19.897]],[3003,40.07609833417807,20440,[38.2205,29.594,45.38666666666666,18.706],[36.9485,19.843,66.92,14.725],[43.012,34.088,56.55,19.932]]],"screen":"Cold code, exp, both dispatch parts and sign-test hint","source_sha256":"4bbbc5fc22c88be019dc1c45e605e7028e4423934abfa8e6603427d499d784e9"}
{"rows":[[1001,40.37430626486355,20448,[37.9605,28.654,47.71666666666667,18.703],[37.055,20.616,75.78333333333333,14.698],[42.8235,34.672,57.336666666666666,20.369]],[2002,40.386354527639604,20448,[38.0565,29.174,46.946666666666665,18.866],[36.8705,20.777,71.29,14.281],[42.9285,34.482,60.12,19.897]],[3003,40.079041658103336,20448,[38.2205,29.594,45.42333333333333,18.706],[36.9485,19.843,66.92,14.725],[43.012,34.088,56.55,19.932]]],"screen":"Cold code, exp and both dispatch parts","source_sha256":"9f48436a141e605d01f935101949a609e1897a3364c48cb0671fbb06c9a1fe2f"}
{"rows":[[1001,40.37916101879046,20464,[37.9605,28.652,47.72,18.703],[37.055,20.616,75.78333333333333,14.698],[42.8235,34.677,57.36666666666667,20.369]],[2002,40.39030611161374,20464,[38.0565,29.17,46.946666666666665,18.866],[36.8705,20.777,71.29,14.281],[42.9285,34.483,60.14666666666667,19.898]],[3003,40.08301984009148,20464,[38.2205,29.588,45.43,18.706],[36.9485,19.843,66.92,14.725],[43.012,34.088,56.586666666666666,19.932]]],"screen":"Cold code and both dispatch parts","source_sha256":"e7395c732dc5ff066363d7b52136642bc51cc645810a3822e530c69155040d94"}
{"rows":[[1001,40.379905088735285,20448,[37.9605,28.654,47.71666666666667,18.703],[37.0695,20.634,75.75,14.693],[42.8235,34.672,57.336666666666666,20.369]],[2002,40.39295290749648,20448,[38.0565,29.174,46.946666666666665,18.866],[36.8815,20.797,71.31666666666666,14.281],[42.9285,34.482,60.12,19.897]],[3003,40.08587338298688,20448,[38.2205,29.594,45.42333333333333,18.706],[36.957,19.863,66.98666666666666,14.72],[43.012,34.088,56.55,19.932]]],"screen":"Cold code, exp and sigmoid dispatch","source_sha256":"032c7e70bb09ddf335e0658f26503d75604bece67f9d4f95ab495ecf08279243"}
```

## Check records

Local gate, static report, exhaustive runs, and same-path object audit.

```jsonl
{"gate":{"bytes":{"rv32im":18960,"thumbv6m":20428,"thumbv7em":21226},"competition":"exact-integer-kernels","fingerprint":{"measurement":"2c8fd1f3a6711f0639685319fb25262b02bfecf4c6589c52cb58928270a46322","sandbox":"none","verifier":"ebbf9d5cac596a718532b34798dc452e4050d6940594005c44f9a729c699c5a8"},"kind":"gate","normalised_sha256":"1a44f002ce36dc83eacd6e96e05d7b1650e2f9550a1db55bbcf04b6562455984","reasons":[],"schema":"eik-report-1","sha256":"3ca88ea3b5a1ff4c015dd064f7fbc21d8a97c3be7527e600f921fd5e3504446c","source_bytes":167251,"stack_bound":{"rv32im":176,"thumbv6m":312,"thumbv7em":272},"stage":null,"verdict":"accepted"}}
{"static_check":"PASS {\"functions\": 42, \"bytes\": {\"rv32im\": 18960, \"thumbv6m\": 20428, \"thumbv7em\": 21226}, \"stack_bound\": {\"rv32im\": 176, \"thumbv6m\": 312, \"thumbv7em\": 272}}"}
{"host_digest_wrapper":"#include <stdint.h>\n#include <stdlib.h>\nunsigned char *SHA256(const unsigned char *, size_t, unsigned char *);\nvoid __wrap_er_sha256(const void *data, size_t length, uint8_t out[32])\n{\n    if (SHA256(data, length, out) == NULL)\n        abort();\n}","link_flag":"-Wl,--wrap=er_sha256","stock_and_wrapped_digest_probe":{"stock":{"budget_seconds":320,"chunk_hi":16,"chunk_lo":0,"competition":"exact-integer-kernels","complete":false,"examples":[],"exit":0,"fingerprint":{"measurement":"2c8fd1f3a6711f0639685319fb25262b02bfecf4c6589c52cb58928270a46322","sandbox":"none","verifier":"ebbf9d5cac596a718532b34798dc452e4050d6940594005c44f9a729c699c5a8"},"function":"sigmoid","kind":"fullcheck","mismatches":0,"quick":false,"range_complete":true,"reasons":[],"schema":"eik-report-1","seconds":14.6,"sha256":"7a841bf948626cd94899d532075c16a83d26807bf5a936e57dc41698b10da17b","stage":null,"verdict":"passed","words_checked":16777216},"wrapped":{"chunk_hi":16,"chunk_lo":0,"complete":false,"examples":[],"fn":"sigmoid","mismatches":0,"range_complete":true,"seconds":2.4,"words_checked":16777216}}}
{"same_path_rv32im":{"base":{"object_bytes":90216,"object_sha256":"9fc355d8f1691562012767a9044726cf40172030a927000b7e5ab857c7fcee4c","source_sha256":"88617bb49e36a06cabd7d84ce6fe504ee337f8f41ad7c55bc72f696db94060c3"},"tanh-alt-hard":{"object_bytes":90216,"object_sha256":"9fc355d8f1691562012767a9044726cf40172030a927000b7e5ab857c7fcee4c","source_sha256":"3ca88ea3b5a1ff4c015dd064f7fbc21d8a97c3be7527e600f921fd5e3504446c"}}}
{"build":"host","chunk_hi":4096,"chunk_lo":0,"complete":true,"examples":[],"fn":"sigmoid","function":"sigmoid","hash_backend":"libcrypto SHA256 via --wrap=er_sha256","host_object_sha256":"e393383efeb444036afbc0244198c01a1684e2dcde825339cea508d7142bf42a","instrumented":"ASan and UBSan","mismatches":0,"range_complete":true,"reference_digest_sha256":"a62545e4b3067576aa72b26eca71d60f20f8db9774f58fadb45dd0c5a4d69e95","seconds":71.5,"sha256":"3ca88ea3b5a1ff4c015dd064f7fbc21d8a97c3be7527e600f921fd5e3504446c","verdict":"passed","words_checked":4294967296}
{"build":"host","chunk_hi":4096,"chunk_lo":0,"complete":true,"examples":[],"fn":"tanh","function":"tanh","hash_backend":"libcrypto SHA256 via --wrap=er_sha256","host_object_sha256":"e393383efeb444036afbc0244198c01a1684e2dcde825339cea508d7142bf42a","instrumented":"ASan and UBSan","mismatches":0,"range_complete":true,"reference_digest_sha256":"6596c8553a866cac76ac119eb05c832788d10d1e972ee32bbae35f513b21c34a","seconds":58.5,"sha256":"3ca88ea3b5a1ff4c015dd064f7fbc21d8a97c3be7527e600f921fd5e3504446c","verdict":"passed","words_checked":4294967296}
{"build":"host","chunk_hi":4096,"chunk_lo":0,"complete":true,"examples":[],"fn":"exp","function":"exp","hash_backend":"libcrypto SHA256 via --wrap=er_sha256","host_object_sha256":"e393383efeb444036afbc0244198c01a1684e2dcde825339cea508d7142bf42a","instrumented":"ASan and UBSan","mismatches":0,"range_complete":true,"reference_digest_sha256":"9d44e4100c4f0340f9b825393cc64bd64eae6ccdde8ece146df9464bd4a5c0c2","seconds":66.4,"sha256":"3ca88ea3b5a1ff4c015dd064f7fbc21d8a97c3be7527e600f921fd5e3504446c","verdict":"passed","words_checked":4294967296}
{"build":"forced","chunk_hi":4096,"chunk_lo":0,"complete":true,"examples":[],"fn":"sigmoid","function":"sigmoid","hash_backend":"libcrypto SHA256 via --wrap=er_sha256","host_object_sha256":"24c0ea764ff0e93c4ffa10abd3e3785ea4c4f7271965e7516c3c2aae4b06e32b","instrumented":"ASan and UBSan","mismatches":0,"range_complete":true,"reference_digest_sha256":"a62545e4b3067576aa72b26eca71d60f20f8db9774f58fadb45dd0c5a4d69e95","seconds":248.6,"sha256":"7a841bf948626cd94899d532075c16a83d26807bf5a936e57dc41698b10da17b","verdict":"passed","words_checked":4294967296}
{"build":"forced","chunk_hi":4096,"chunk_lo":0,"complete":true,"examples":[],"fn":"tanh","function":"tanh","hash_backend":"libcrypto SHA256 via --wrap=er_sha256","host_object_sha256":"24c0ea764ff0e93c4ffa10abd3e3785ea4c4f7271965e7516c3c2aae4b06e32b","instrumented":"ASan and UBSan","mismatches":0,"range_complete":true,"reference_digest_sha256":"6596c8553a866cac76ac119eb05c832788d10d1e972ee32bbae35f513b21c34a","seconds":41.9,"sha256":"7a841bf948626cd94899d532075c16a83d26807bf5a936e57dc41698b10da17b","verdict":"passed","words_checked":4294967296}
{"build":"forced","chunk_hi":4096,"chunk_lo":0,"complete":true,"examples":[],"fn":"exp","function":"exp","hash_backend":"libcrypto SHA256 via --wrap=er_sha256","host_object_sha256":"24c0ea764ff0e93c4ffa10abd3e3785ea4c4f7271965e7516c3c2aae4b06e32b","instrumented":"ASan and UBSan","mismatches":0,"range_complete":true,"reference_digest_sha256":"9d44e4100c4f0340f9b825393cc64bd64eae6ccdde8ece146df9464bd4a5c0c2","seconds":171.6,"sha256":"7a841bf948626cd94899d532075c16a83d26807bf5a936e57dc41698b10da17b","verdict":"passed","words_checked":4294967296}
{"budget_seconds":2404160,"build":"thumbv6m","chunk_hi":4096,"chunk_lo":0,"competition":"exact-integer-kernels","complete":true,"fingerprint":{"measurement":"2c8fd1f3a6711f0639685319fb25262b02bfecf4c6589c52cb58928270a46322","sandbox":"none","verifier":"ebbf9d5cac596a718532b34798dc452e4050d6940594005c44f9a729c699c5a8"},"function":"sigmoid","image_sha256":"8fe443b21f35b54cd12aa9d864be274d0be7838232896e8cf8656b81d0149e6b","jobs":3,"kind":"targetcheck","mismatches":0,"range_complete":true,"reasons":[],"schema":"eik-report-1","seconds":571.4,"sha256":"3ca88ea3b5a1ff4c015dd064f7fbc21d8a97c3be7527e600f921fd5e3504446c","stage":null,"target":"thumbv6m","verdict":"passed","words_checked":4294967296}
{"budget_seconds":2404160,"build":"thumbv6m","chunk_hi":4096,"chunk_lo":0,"competition":"exact-integer-kernels","complete":true,"fingerprint":{"measurement":"2c8fd1f3a6711f0639685319fb25262b02bfecf4c6589c52cb58928270a46322","sandbox":"none","verifier":"ebbf9d5cac596a718532b34798dc452e4050d6940594005c44f9a729c699c5a8"},"function":"tanh","image_sha256":"8fe443b21f35b54cd12aa9d864be274d0be7838232896e8cf8656b81d0149e6b","jobs":3,"kind":"targetcheck","mismatches":0,"range_complete":true,"reasons":[],"schema":"eik-report-1","seconds":250.8,"sha256":"3ca88ea3b5a1ff4c015dd064f7fbc21d8a97c3be7527e600f921fd5e3504446c","stage":null,"target":"thumbv6m","verdict":"passed","words_checked":4294967296}
{"budget_seconds":2404160,"build":"thumbv6m","chunk_hi":4096,"chunk_lo":0,"competition":"exact-integer-kernels","complete":true,"fingerprint":{"measurement":"2c8fd1f3a6711f0639685319fb25262b02bfecf4c6589c52cb58928270a46322","sandbox":"none","verifier":"ebbf9d5cac596a718532b34798dc452e4050d6940594005c44f9a729c699c5a8"},"function":"exp","image_sha256":"8fe443b21f35b54cd12aa9d864be274d0be7838232896e8cf8656b81d0149e6b","jobs":3,"kind":"targetcheck","mismatches":0,"range_complete":true,"reasons":[],"schema":"eik-report-1","seconds":254.8,"sha256":"3ca88ea3b5a1ff4c015dd064f7fbc21d8a97c3be7527e600f921fd5e3504446c","stage":null,"target":"thumbv6m","verdict":"passed","words_checked":4294967296}
```

## Item provenance

The 18 item results below were supplied as the goal's pinned handoff. Their hashes were checked against the assignment. The link paths refer to the handoff, which may be absent from a published checkout. The final diff and primary local integration records are reproduced above.

| Handoff item | SHA-256 |
|---|---|
| [codegen-m0][codegen-m0] | `78a49da4a880695a62bb9e0195fb3ea4e5a8a7496f0e40fbf8e4b8d07894e455` |
| [dispatch-order][dispatch-order] | `264a9825397a04403c05f6b499d99cf084aef6304ed26ee74d7619d3881c7d5f` |
| [exp-grid-tradeoff][exp-grid-tradeoff] | `5250811dffd2791b44ca215cb9198bbd22ba6ed3ec64b681829432e246c402d8` |
| [exp-guard][exp-guard] | `c68fd3bd106d8d52168671d8d541435e6d4327caa737133426fb6099bf6d9646` |
| [exp-neg-direct][exp-neg-direct] | `390b010a76edfdc23b91b7ca638045f9936df5ca02b3c4411abab96957b36a67` |
| [exp-neg-direct-b][exp-neg-direct-b] | `d8dd7061ae34ad55fae743ef5194e3fa7753bbe5f93a35a99189e9c92bb6fa1c` |
| [exp-reduction-m0][exp-reduction-m0] | `b237de3981ab01effe2511e285051fe7bb9a7b92e5d2a6f39c8d24002225d232` |
| [exp-wide-edges][exp-wide-edges] | `3ca0e3578273e8370de0d9e249f9c05a942060065793cd07660618e022b24b8a` |
| [sig-guard][sig-guard] | `d4b44064ee814da8b65e947f2d8a47c7ebfd869210072661e7f602bae192b505` |
| [sig-small-wide][sig-small-wide] | `41034ed018e703ec84566d0cab7d8b5519de75aee53470d6a5235373f8b5b135` |
| [sig-typ-cells][sig-typ-cells] | `bb77491b331129beb6a6ca60c6f0d3853b97351ff58ddd23320300a1106fed09` |
| [sig-via-shared][sig-via-shared] | `e9edb1034398d544d9e0777c1b81e5629dfa2545d2289b3e24a14415678e6a4c` |
| [size-code][size-code] | `b1cc4d99b2ece53d6bbd2999be00432723409e27507274ad2c4c8ca64ff040a6` |
| [size-cold-tables][size-cold-tables] | `1b8c98d34bf7f4ab1bab80e3bf5e9dbdb0e40621b94ee713a5086ce41aaddb48` |
| [size-pack][size-pack] | `93d66d1d114206298622a166c97c1009c762e44069e62a82376ccade7ca3bd16` |
| [tanh-cutoff-flags][tanh-cutoff-flags] | `ed15ce97dcdbcb4bad2d9ab39744fad38cdcf00ab113537b38ee8ec7570f5743` |
| [tanh-hard-wide][tanh-hard-wide] | `5a04a857d1e34762d0b0c8bc45427fb9cfa786077989654a34bcec2360b0012a` |
| [tanh-typ-cells][tanh-typ-cells] | `c0c7cb0f5eac0d7ae8394c5e5413affaaf2b0398d377377b2e68463c6600a75d` |

[base]: https://github.com/identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io/blob/c5e3f91274b1f0c409127e8cfc14aa5ac8f392da/eik-work/baselines/former-50/entry.c
[toolkit]: https://github.com/identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io/blob/c5e3f91274b1f0c409127e8cfc14aa5ac8f392da/eik-work/toolkit/dependencies.json
[rules]: https://github.com/conjectures-io/exact-integer-kernels-miner/blob/5a32428ad4aa23bce737d50a738ace24ddeeed2e/RULES.md
[score]: https://github.com/conjectures-io/exact-integer-kernels-miner/blob/5a32428ad4aa23bce737d50a738ace24ddeeed2e/eik/score.py
[stages]: https://github.com/conjectures-io/exact-integer-kernels-miner/blob/5a32428ad4aa23bce737d50a738ace24ddeeed2e/eik/stages.py
[digests]: https://github.com/conjectures-io/exact-integer-kernels-miner/blob/5a32428ad4aa23bce737d50a738ace24ddeeed2e/reference/digests.sha256
[codegen-m0]: ../../../.imd/reads/artifacts/item-codegen-m0
[dispatch-order]: ../../../.imd/reads/artifacts/item-dispatch-order
[exp-grid-tradeoff]: ../../../.imd/reads/artifacts/item-exp-grid-tradeoff
[exp-guard]: ../../../.imd/reads/artifacts/item-exp-guard
[exp-neg-direct]: ../../../.imd/reads/artifacts/item-exp-neg-direct
[exp-neg-direct-b]: ../../../.imd/reads/artifacts/item-exp-neg-direct-b
[exp-reduction-m0]: ../../../.imd/reads/artifacts/item-exp-reduction-m0
[exp-wide-edges]: ../../../.imd/reads/artifacts/item-exp-wide-edges
[sig-guard]: ../../../.imd/reads/artifacts/item-sig-guard
[sig-small-wide]: ../../../.imd/reads/artifacts/item-sig-small-wide
[sig-typ-cells]: ../../../.imd/reads/artifacts/item-sig-typ-cells
[sig-via-shared]: ../../../.imd/reads/artifacts/item-sig-via-shared
[size-code]: ../../../.imd/reads/artifacts/item-size-code
[size-cold-tables]: ../../../.imd/reads/artifacts/item-size-cold-tables
[size-pack]: ../../../.imd/reads/artifacts/item-size-pack
[tanh-cutoff-flags]: ../../../.imd/reads/artifacts/item-tanh-cutoff-flags
[tanh-hard-wide]: ../../../.imd/reads/artifacts/item-tanh-hard-wide
[tanh-typ-cells]: ../../../.imd/reads/artifacts/item-tanh-typ-cells
