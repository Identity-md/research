# Prediction Market challenge: write-up of this generation's 17 results

Goal: move this network from 3rd (106.55) to 1st (109.59) on Paradigm's Prediction Market challenge ([puzzle](https://www.paradigm.xyz/puzzles/prediction-market-challenge), [simulator and rules](https://github.com/danrobinson/prediction-market-challenge)), starting from seat 845 "crossing cover". On Paradigm that file scored 106.546791 mean edge (retail 129.252528, arbitrage -22.705737) ([base artifact](https://api.imd.fun/artifacts/40497298132dcc0ccc9f4c0672031c7eaae00ddcf8cf24983db989feeb3c5ca0)). The gap to first is 109.59 - 106.546791 = 3.043209.

**Every number below is a local simulator measurement taken from the item results. None is a Paradigm score.** No item entered a file on Paradigm or reports a hosted-sandbox run, so this report has no new leaderboard score (see "Paradigm entry status" at the end).

## How to get each file

Each item result is a public JSON file at `https://api.imd.fun/artifacts/<artifact SHA-256>`, the same place the six known files live. Its `code` field holds the frozen strategy, and the file also holds its evaluation records (`score`, `holdout`, `diff`, `seconds`, `tried`). On 2026-11-06 I downloaded all 17 from that address. Every download returned HTTP 200 and matched the artifact SHA-256 listed below. In every file, the SHA-256 of the `code` string matched its `code_sha256` field. Per the brief, the strategy code itself is left out of this report.

| Item | Artifact (result JSON incl. code) | `code_sha256` |
|---|---|---|
| demand-floor | [db492ed5…](https://api.imd.fun/artifacts/db492ed5ea693781491dd7ef27a59d076aa1860b94bea08bd0e134b608e0d93b) | 6aabf8e9f61ee7ea673b35c1c17a2ef49a2a08c750d6bfe147f2042e1acaa436 |
| cash-fix | [a261c9de…](https://api.imd.fun/artifacts/a261c9ded9200dd29189d624562aff18826e59e8fa7220b4cebcd9e7ea1aa330) | a5563563a0e78d64fd50637ac4972e9950046e8469152a57b3d1affb1b87c81d |
| retail-mid | [2adaa7a6…](https://api.imd.fun/artifacts/2adaa7a6f614b6b94f3c82f0c06e328c4ff40fb4dde18e078d9ebbd1b0fdaea6) | 4d34c482983b88e18053535d96c3fc256d0fb8baf8c5ec607e3097098276b297 |
| wildcard-pattern | [219817b7…](https://api.imd.fun/artifacts/219817b76f78d7d900d71abffa2e78294574443bb5281668907836a44ac2942e) | 0f4d34f0f93c32455d06cb4b0db73682ff9c54805952167870a6dcb2960dcebd |
| retail-missed | [a542e2f8…](https://api.imd.fun/artifacts/a542e2f89cf2236641fb9e3023304b287f03bb066e28983972f2c6af6fc50a07) | 65d8a3994876e19a8846378008dd456cbe1acb10dea90448bba2b1e2b2bc63c6 |
| speed | [4435181e…](https://api.imd.fun/artifacts/4435181e4d916cfb6bd345fae3d88025d37032eae02221025d39a98496a66553) | 0351b7a677600ba8070e0f65bf1f160b20687fe3547c770eaa0cf04fc94fcb8f |
| graft-spreads | [41fa8829…](https://api.imd.fun/artifacts/41fa8829432f502a00c5302c0e2200b475c5c2e100a2a16b086aaab0ce62a395) | dcf68e0c9a7b06f90cf70a833357b60e2208b5b3e2971e7dddf02986d4747076 |
| cross-deeper | [bd9a1b26…](https://api.imd.fun/artifacts/bd9a1b26a7a53c2adae4dbbbdf84ee809c782a2806c96919839ecdbbd8c2c080) | 2c0acfc867ad2feeaf07d14822d1f631d64db14e8d8c6cb1ca7f49017bbd0d5d |
| graft-demand | [8b4ad631…](https://api.imd.fun/artifacts/8b4ad631c15180565229a8ef483520e09c238374bbfe3254fa1e9e0d8bdfb3a0) | 8ceaba9565a9d9824c39c3f8cf3d18e44c41ebf3ccafb4dd696d2eced5979afe |
| stack-all | [a884acfd…](https://api.imd.fun/artifacts/a884acfde24db7282875fc52bb53dc4456670ed84cf8d2f59297317081e555d8) | 2f568c5997204668f46871f2a89c9709412f1d866894a3e869d200e746638781 |
| late-fix | [fee58554…](https://api.imd.fun/artifacts/fee585548f47dd8b88d1791f44566f1880b7cc7f9357e8522f6c3f6fc962c61e) | 08fdb3c2412a8a1f49f85150468f3864dc077532a8e702a18d33fd83cddc1aa6 |
| retail-second-level | [f11f1976…](https://api.imd.fun/artifacts/f11f19768248d59bdee6bf1fb47e12b0512ac22dcb7b579713861e78931b839f) | 27978c8bfb52db9d0915dd326c1138d00fcd39fb71131fbb02383ce4adb27f88 |
| cross-ask | [e7d76b2c…](https://api.imd.fun/artifacts/e7d76b2cbef19657a842cf0561ea0a4e7e5ba22f4fc83f97fde9ce42e4856238) | 4b641935ac05cf2318c547fe2a6f89fc593f3085f631e848bbe56e2cd43d0803 |
| jump-exposure | [3233cdc8…](https://api.imd.fun/artifacts/3233cdc8945dc78a0dd4c7174a9808d020279e30968b7e31034fcbf6e1cbeabb) | 71d04d586f29… (base code, unchanged) |
| proxy-weights | [04efaa94…](https://api.imd.fun/artifacts/04efaa945d7e571d4bbd35e77376d67d78f36908c39ae301448dc4f682fd33c5) | 71d04d586f29… (base code, unchanged) |
| proxy-mix | [d67ebf41…](https://api.imd.fun/artifacts/d67ebf4151551c221c97a255c35dcb288a2a62f834f46ecdeaac464c596b2aa9) | 71d04d586f29… (base code, unchanged) |
| wildcard-retail | [010f7ced…](https://api.imd.fun/artifacts/010f7ced96dc9eedab4d6e599583e4224c262122d09213129833f1f880996646) | 71d04d586f29… (base code, unchanged) |

The base's code SHA-256 is 71d04d586f29bb44ebf387156da6553da332111bdfafb9548c0a1530f52f6594.

## Results table

Rows are sorted by the mean-edge difference from the base on unseen seeds (the `diff` block: candidate minus base, paired per run). Retail and arbitrage are the two parts of that difference; a positive arbitrage figure means less arbitrage loss. Seconds are wall time for 200 runs, measured by each item on its own machine, so they can only be compared within a row. Code size is the length of the `code` string. "Unseen runs" is the holdout count, from seed 50000. **Candidate** means all three rules hold: unseen retail difference ≥ 0, zero failures, and seconds no greater than the base's.

| # | Item | Δ mean (SE) | Δ retail | Δ arb | s/200 runs: item vs base | Code size | Unseen runs | Candidate? |
|---|---|---|---|---|---|---|---|---|
| 1 | stack-all | 1.2441070518834279 (0.8468937659959795) | 0.33774727491485684 | 0.9063597769642855 | 150.28571428571428 vs 140.0 | 37976 | 350 | No: slower; only 350 runs |
| 2 | graft-demand | 0.9268457367855253 (0.4025218703783972) | -0.9557892549512501 | 1.882634991743025 | 169.42 vs 155.72 | 37936 | 4000 | No: retail lower, slower |
| 3 | demand-floor | 0.5484719976832001 (0.11612940188936807) | 0.34782875931662516 | 0.20064323837089992 | 113.57789771584794 vs 115.75908906990662 | 38142 | 4000 | **Yes** |
| 4 | cash-fix | 0.5122042913809504 (0.24659084956319965) | 0.14871560857800026 | 0.36348868279917496 | 105.08536023297347 vs 107.24866369995289 | 14483 | 4000 | **Yes** |
| 5 | graft-spreads | 0.50242183186265 (0.07846090435735968) | 0.06887844159805004 | 0.43354339026462496 | 111.53628118382767 vs 111.41148243751377 | 15393 | 4000 | No: 0.12479874631389976 s slower |
| 6 | cross-deeper | 0.23374616781452492 (0.07730470236432167) | 0.13688402687157483 | 0.09686214094437494 | 82.86836009519175 vs 82.27741253585555 | 14895 | 4000 | No: slower (+0.7%, which the item calls noise) |
| 7 | retail-mid | 0.22570523626440003 (0.03437928452040865) | 0.4910117788789 | -0.265306542615425 | 189.05823257332668 vs 206.40725212194957 | 15826 | 4000 | **Yes** |
| 8 | wildcard-pattern | 0.209404062670175 (0.0669494819952478) | 0.37421341827392507 | -0.16480935560390003 | 243.92939586169086 vs 254.04184297309257 | 12907 | 4000 | **Yes** |
| 9 | late-fix | 0.1658806724636503 (0.03145024960903636) | -0.05671240280027499 | 0.2225930752644 | 1092.748664598912 vs 1121.0166670444887 | 13421 | 4000 | No: retail lower |
| 10 | retail-second-level | 0.035220997439274926 (0.0640336497981795) | 0.04513479143878385 | -0.009913793999924536 | 60.663953667040914 vs 54.44736991589889 | 20372 | 4000 | No: about 11% slower |
| 11 | retail-missed | 0.011480842793549996 (0.009533915369918038) | 0.011155944659200025 | 0.000324898134375022 | 167.29498300235718 vs 173.78885432262905 | 13902 | 4000 | Yes, but the gain is within noise |
| 12 | speed | 0.0 (0.0) | 0.0 | 0.0 | 257.17929600796197 vs 265.82176911085844 | 13500 | 4000 | Yes (same policy as the base, faster) |
| 13 | proxy-weights | 0.0 (0.0) | 0.0 | 0.0 | 513.9856903129257 vs 504.6526717925444 | 14239 | 4000 | n/a: base code unchanged |
| 14 | jump-exposure | 0.0 (0.0) | 0.0 | 0.0 | 182.68 vs 184.98 | 14239 | 4000 | n/a: base code unchanged |
| 15 | wildcard-retail | 0.0 (0.0) | 0.0 | 0.0 | 910.2666666666667 vs 910.2666666666667 | 14239 | 30 | n/a: not completed, base code |
| 16 | cross-ask | -0.2401943067644998 (0.07244571115698904) | 0.04845515125424983 | -0.28864945801825004 | 577.0 vs 576.25 | 15366 | 400 | No: loses, slower |
| 17 | proxy-mix | null (null) | null | null | null vs null | 14239 | not finished | n/a: no full scores |

Notes on the table:
- **stack-all and graft-demand:** their large Δ values come with large standard errors. stack-all used only 350 unseen runs, and its base reference there is 99.45323934378943, not the 97.54703502577897 that most items measured. Both trade retail for arbitrage savings, either outright (graft-demand) or on tuning seeds (stack-all lost 1.70 retail there).
- **cross-ask:** 400 unseen runs on a heavily loaded machine.
- **wildcard-retail:** 30 runs; the item says its `score` block is placeholders.
- **speed:** its long sweeps ran on PyPy, so its absolute scores are PyPy-specific (calibration mean 108.62320549194204 versus CPython 108.63974289615767). That is why its base reference (97.54400381637852) differs from the other items'.

## Which grafts held

- **Demand fit graft.** Grafted verbatim (graft-demand), it did not hold: +0.9268457367855253 mean, but -0.9557892549512501 retail and slower, the trade that has lost on Paradigm. Grafting it again with its retail suppression removed (demand-floor) did hold. demand-floor keeps the base's ordinary quote sizing, uses the fitted flow only for stock, sets bulk/near-stock floors of 0.45/0.5, and replaces the 9x9 prior with weighted 5x5 quadrature. It gained 0.5484719976832001 (SE 0.11612940188936807) with +0.34782875931662516 retail and ran faster than the base. Its retail on the richest tenth of unseen runs went from 192.918195187389 to 196.18402107417975.
- **Per-spread constants.** These held on net but not on speed (graft-spreads: +0.50242183186265 net, +0.06887844159805004 retail, 0.12479874631389976 s slower over 200 runs). Only the spread 1 and spread 3 overrides were kept; spread 4 was rejected.
- **Stacking demand fit with crossing cover** (stack-all) was not shown to help: 350 runs, not significant, slower.
- **Cash plan, recut as cash-fix, held:** +0.5122042913809504 with +0.14871560857800026 retail and faster than the base. It uses a 25% allowance for uncovered asks, a $200 reserve that fades over the last 50 steps, and a scarcity charge below p=0.1. The item notes that the listed parent artifact returned HTTP 404 to it.
- **Late-game, recut as late-fix,** still cost retail (-0.05671240280027499), so it is not a candidate.
- **speed** is an exact-behaviour refactor of the base: 257.17929600796197 s against 265.82176911085844 s per 200 runs.

## Where new retail was found

- **retail-mid** found the largest retail gain, +0.4910117788789. It refills inside the competitor at estimated p ≥ 0.20 whenever depth is below 95% of target (instead of 70%), multiplies the bid target by 1.5 at p ≥ 0.95, and adds an upper-tail duration estimate. Its unseen change at execution prices ≥ 20 cents was retail buy 0.3420015210557006, retail sell 0.14562813455592494 and arbitrage -0.2975848318374279. Net +0.22570523626440003.
- **wildcard-pattern** gained +0.37421341827392507 retail by raising the ask-size ceiling to max(3000, min(10000, YES inventory)) only when p < 0.002, so the extra asks are backed by cheap stock already held. Net +0.209404062670175.
- **demand-floor** (+0.34782875931662516) and **cross-deeper** (+0.13688402687157483) found retail in low-price stock and cover. cross-deeper is held back only by timing.
- **Small or nil retail:**
  - retail-missed: +0.011155944659200025 (within noise).
  - retail-second-level: +0.04513479143878385, within noise and about 11% slower.
  - cross-ask: +0.04845515125424983 retail, but -0.2401943067644998 net.
- **Retail versus arbitrage overall:** jump-exposure found that reweighting the jump-loss term is a straight retail-for-arbitrage trade, with the base already at the optimum. cross-deeper's zone audit puts most retail below 2c: 73.689 base versus 73.733 for the variant.
- **Source caveat:** retail-mid, retail-second-level, cross-deeper, cross-ask, demand-floor and wildcard-pattern each cite at least one source that did not hold on re-read. What they say about the simulator or about Paradigm from those sources is unconfirmed. Their numbers are their own local measurements, and that caveat does not apply to them.

## What the two fitting seats say about Paradigm's runs

Both fitting seats cite sources that did not hold on re-read (proxy-weights 1, proxy-mix 2), so treat their conclusions as provisional.

**proxy-mix** did not finish. Its 4000-run blocks are null. On one paired 200-run block (seeds 50000–50199) it ranks the files:

1. cash plan 104.174949
2. late-game 103.078766
3. demand fit 102.996949
4. parent 102.326223
5. first entry 89.863985

It did not rank the base on that block. It suggests that retail richness and runs settling NO may matter, and calls broader spreads and calmer paths unverified hypotheses.

**proxy-weights** found that uniform weights won. None of its 15 feature tilts passed validation (RMSE plus ESS ≥ 250) on two disjoint 500-run halves. Under uniform weights the unseen 4000-run ranking is cash, late, demand, base, parent, first, with RMSE 5.5141969916820655 against Paradigm's 18 numbers. The local mean edge runs about 5.45 to 9.00 below Paradigm's.

Its predeclared 18-feature diagnostic, fitted in-sample to all of seeds 50000–53999 with ESS held at 1000, reproduces Paradigm's order exactly: base, demand, cash, parent, late, first. Its RMSE is 0.37720518811906967. The weights it fits:

- Heaviest on jump intensity (1.4348849236124452) and YES×p0 (1.0968145466988934).
- Against p0 squared (-1.0412425010641355), largest absolute jump (-1.2735834901575025) and realized jump sum (-0.896670696535314).
- Up on YES settlement (0.6283585512739394) and down on spread 3 (-0.7802546391631922).

Read loosely, Paradigm's runs look as though they hold more jump-intensive regimes, starting probabilities nearer 0.5, more YES settlement and fewer spread-3 markets. The item stresses that this is calibration, not evidence of predictive success. It needs a fresh test on seeds 60000–63999 before anyone uses it to select files.

## What the next generation should start from

- **Starting files.** Start from **demand-floor** (best eligible: +0.5484719976832001, SE 0.11612940188936807, retail +0.34782875931662516). Use **speed** as the base reference, since its policy is identical and it is faster.
- **Grafts to stack onto it, each tested separately:**
  - cash-fix's reserve and scarcity charge.
  - retail-mid's ≥ 20-cent refill rule.
  - wildcard-pattern's inventory-backed ceiling below p = 0.002.
  - cross-deeper's 1.5x/offset cover, once its runtime is trimmed.
  - graft-spreads' spread 1 and 3 overrides, once their overhead is removed.
- **Fresh seeds.** Seeds 50000–53999 are now used and must not be reused as a holdout.
- **Prototype to test.** demand-floor's untested `tiny_regime` prototype has a 1000-run validation gain of 1.0845625551113998 (SE 0.7033181182750896) and should be tested on fresh seeds.
- **Selection.** Test the proxy-weights diagnostic recipe on fresh seeds before using it to select.

The eligible files' gains (0.0115 to 0.548 locally) are each far below the 3.043209 gap. Whether they stack, and whether they transfer to Paradigm, has not been measured.

## Paradigm entry status

No item entered a file on Paradigm, so this report has no entry identifier and no official 200-run result. Entry is an outward-facing submission from the requester's account, and none of these workers had that account or that step. The submission-ready set is the four eligible files with local gains:

| File | Artifact |
|---|---|
| demand-floor | db492ed5ea693781491dd7ef27a59d076aa1860b94bea08bd0e134b608e0d93b |
| cash-fix | a261c9ded9200dd29189d624562aff18826e59e8fa7220b4cebcd9e7ea1aa330 |
| retail-mid | 2adaa7a6f614b6b94f3c82f0c06e328c4ff40fb4dde18e078d9ebbd1b0fdaea6 |
| wildcard-pattern | 219817b76f78d7d900d71abffa2e78294574443bb5281668907836a44ac2942e |

Each one's `code` field is the file to submit. No item checked success in Paradigm's hosted sandbox, and two earlier files failed there about five minutes in. The local timings above are the only evidence on speed.
