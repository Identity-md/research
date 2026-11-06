# Goal write-up: merging the two newest rounds into the start file

Sources are the five results under `.imd/reads/artifacts/`: `item-m-all` (SHA-256 db22aff7167a4798251ed3d20432509f30e511e4958799aba5b17b41bb39b4b6), `item-m-plus-a` (149883fee797ad95a91e535b7a74453587a3eb19ca87ab95f7d8585db160a8f4), `item-m-plus-b` (6b40ef6fdf9512700501e6b92fb5c920955a97b29111faada6d411074173b7cd), `item-m-plus-c` (86a711e937d310d0ed3dc3583d97962ad1b53959bfb11b56e545070cb7407b32) and `item-m-safe` (aac61b519153db5193195c7fd184e57fff593ac2879211a25ac86997740a62e5). Every figure below is copied from those results; nothing is recomputed except where the text says so. The start file is 151e0b1b16f90a1384b823bc528d6d1407f7b4bbfcc7966c12119fe483bfd326 and its score is 108.63974289615767 on 600 seeds 1000..1599, reproduced by all five items as `base_mean_edge` except `item-m-plus-c`, which reports it as not measured.

## Blocks

| item | blocks and spreads | exact against the block files | by-spread runs, spreads 1/2/3/4 |
|---|---|---|---|
| `item-m-all` | c1-pairs on 1, c2-queue on 2, a3-ledger on 3, c4-all on 4 | 600 runs per spread, identical=true | 1016/980/958/1046 |
| `item-m-plus-a` | c1-pairs on 1, c2-queue on 2, a3-ledger on 3, c4-all on 4 | 600 runs per spread, identical=true | 752/742/718/788 |
| `item-m-plus-b` | c1-pairs on 1, c2-queue on 2, a3-ledger on 3, c4-all on 4 | 600 runs per spread, identical=true | 1016/980/958/1046 |
| `item-m-plus-c` | c1-pairs on 1, c2-queue on 2, a3-ledger on 3, c4-all on 4 (class dispatch) | 30 runs per spread, identical=true | 43/31/28/38 |
| `item-m-safe` | a3-ledger on 3 only; 1, 2, 4 keep the start file | 300 runs per spread, identical=true | 501/504/479/516 |

Every item reports all four spreads identical to their source files; the run count behind that claim is what separates `item-m-all` and `item-m-plus-b` (600 per spread, 2400 paired comparisons) from `item-m-safe` (300 per spread) and `item-m-plus-c` (30 per spread, 15 seeds from 100000 and 15 from 104000). `item-m-plus-c` also notes that its spreads 2-4 were checked before a later fix to the spread-1 top-level code.

## Fixes

| item | fix (spread) | measured gain | standard error | stayed |
|---|---|---|---|---|
| `item-m-plus-a` | a1-jumps (1) | 0.5009455722593997 | 0.3289621386809776 | yes |
| `item-m-plus-a` | a2-after (2) | 0.7478670929991998 | 0.14009787888594427 | yes |
| `item-m-plus-a` | a4-rich (4) | 0.22959375486119976 | 0.07775380466313571 | yes |
| `item-m-plus-a` | a4-free (4) | 0.052893605455300426 | 0.13495153349795513 | no |
| `item-m-plus-a` | a3-rich (3) | 0.7387592263152998 | 0.20043234577823205 | yes |
| `item-m-plus-a` | a1-free (1) | 0.29429490312559986 | 0.047839957990400236 | yes |
| `item-m-plus-a` | a3-free (3) | 0.2783257251334001 | 0.05424129829265064 | yes |
| `item-m-plus-a` | a4-stock (4) | 0.46915560943630036 | 0.05582351049007889 | yes |
| `item-m-plus-a` | a2-ledger (2) | 1.2108931310401003 | 0.1136786232236645 | yes |
| `item-m-plus-b` | a1-free (1) | 0.35149849538759986 | 0.1473650964688594 | yes |
| `item-m-plus-b` | a1-jumps (1) | -0.46009330345589977 | 0.5348458123513586 | no |
| `item-m-plus-b` | a2-ledger (2) | 1.0912132155852996 | 0.10001626498595995 | yes |
| `item-m-plus-b` | a2-after (2) | 0.8675470084540006 | 0.13694721873193286 | yes |
| `item-m-plus-b` | a3-free (3) | 0.2967595907355999 | 0.055760086084229464 | yes |
| `item-m-plus-b` | a3-rich (3) | 0.7203253607131 | 0.20022945125849764 | yes |
| `item-m-plus-b` | a4-stock (4) | 0.3884841414820999 | 0.04321751641266317 | yes |
| `item-m-plus-b` | a4-free (4) | 0.10763674876980042 | 0.14029986176237702 | no |
| `item-m-plus-b` | a4-rich (4) | 0.3102652228154002 | 0.0836897732963366 | yes |
| `item-m-plus-c` | a3-rich (3) | 0.8334181773983345 | 0.25588320751442933 | yes |
| `item-m-plus-c` | a3-free (3) | 0.17271267671833232 | 0.3251756280361294 | yes |
| `item-m-plus-c` | a4-rich (4) | 0.38517936668833586 | 0.14609271528377196 | yes |
| `item-m-plus-c` | a4-free (4) | 0.6258003894733333 | 0.3207823409434335 | yes |
| `item-m-plus-c` | a4-stock (4) | 0.4463098442333328 | 0.2447708962752243 | yes |
| `item-m-plus-c` | a1-jumps (1) | not tested | not tested | no |
| `item-m-plus-c` | a1-free (1) | not tested | not tested | no |
| `item-m-plus-c` | a2-after (2) | not tested | not tested | no |
| `item-m-plus-c` | a2-ledger (2) | not tested | not tested | no |
| `item-m-safe` | a1-jumps (1) | 0.8317693322811999 | 0.35873561884138366 | yes |
| `item-m-safe` | a1-free (1) | 0.1623564006363998 | 0.1415346551431088 | no |
| `item-m-safe` | a2-after (2) | 1.0651422830891997 | 0.17354929374259553 | yes |
| `item-m-safe` | a2-ledger (2) | 0.27792990249079996 | 0.10146617507217796 | yes |
| `item-m-safe` | a3-rich (3) | 1.0785609271135999 | 0.38144802285492224 | yes |
| `item-m-safe` | a3-free (3) | 0.26205756672299996 | 0.0884205488779404 | yes |
| `item-m-safe` | a4-rich (4) | 0.5250457714106009 | 0.10856922767315608 | yes |
| `item-m-safe` | a4-free (4) | 0.26696185971979836 | 0.3000436788195861 | yes |
| `item-m-safe` | a4-stock (4) | 0.2542907039806001 | 0.056770467549436286 | yes |

`item-m-all` tried no fixes. `item-m-plus-c` lists the four spread-1 and spread-2 fixes as measured at all (`null` gain) because the c1-pairs and c2-queue blocks replace the start-file code they were written against; it dropped them untested. Its remaining five were tested on 60 runs of their spread, all-on against leave-one-out, and all passed.

## Difference from the start file

| item | mean | SE | retail | arbitrage | seconds, start | seconds, item |
|---|---|---|---|---|---|---|
| `item-m-all` | 1.445340121537375 | 0.15708671985275371 | 0.7685706656211752 | 0.676769455914275 | 179.17913917917758 | 179.33491440303624 |
| `item-m-plus-a` | 2.4314994365665337 | 0.21640274191625686 | 0.31911411444809995 | 2.1123853221140667 | 120.45409822463989 | 124.06083273887634 |
| `item-m-plus-b` | 2.2128427559408252 | 0.1728962114120029 | 0.3448020945050003 | 1.868040661433225 | 107.23521068086848 | 115.86656947713345 |
| `item-m-plus-c` | 2.1346696331885706 | 1.410839002179575 | 1.915353916744286 | 0.21931571645214276 | 241.93915333066667 | 251.27556937081474 |
| `item-m-safe` | 0.95685317308875 | 0.14141149083550503 | -0.2489319660061499 | 1.20578513908295 | 46.43412822112441 | 51.85971038695425 |

| item | spread | runs | mean | SE | retail | arbitrage |
|---|---|---|---|---|---|---|
| `item-m-all` | 1 | 1016 | 1.6356063570282477 | 0.33297078663721597 | 1.0300580291539372 | 0.6055483278707675 |
| `item-m-all` | 2 | 980 | 1.7287357789455104 | 0.47160501483821404 | 2.6768412316472454 | -0.9481054527019388 |
| `item-m-all` | 3 | 958 | 0.4883446301950943 | 0.04857877029821955 | -0.02987450130949868 | 0.5182191315026096 |
| `item-m-all` | 4 | 1046 | 1.8715001991542064 | 0.2413208423327588 | -0.5420085371849906 | 2.413508736337285 |
| `item-m-plus-a` | 1 | 752 | 2.7607500570893615 | 0.4681439732311693 | 0.5602578017253987 | 2.2004922553571804 |
| `item-m-plus-a` | 2 | 742 | 3.1191828508327495 | 0.6253819677133948 | 1.8774088114223721 | 1.2417740394117252 |
| `item-m-plus-a` | 3 | 718 | 1.177005828453065 | 0.17567191006929916 | -0.45932796508467955 | 1.636333793533844 |
| `item-m-plus-a` | 4 | 788 | 2.6128050845446706 | 0.3238672094824128 | -0.6690499780428937 | 3.2818550625796954 |
| `item-m-plus-b` | 1 | 1016 | 1.9515104762154525 | 0.3478722551131989 | 0.7234912613565947 | 1.2280192148513778 |
| `item-m-plus-b` | 2 | 980 | 3.005904837975102 | 0.51538162827511 | 1.7416755060861226 | 1.2642293318903062 |
| `item-m-plus-b` | 3 | 958 | 1.1897131414110653 | 0.1500223481925494 | -0.4360777386556363 | 1.6257908800641963 |
| `item-m-plus-b` | 4 | 1046 | 2.6607117105554496 | 0.26368738893498095 | -0.6165757799718925 | 3.277287490525717 |
| `item-m-plus-c` | 1 | 43 | 6.598859834299999 | 4.055074254964557 | 5.725346243925583 | 0.8735135903418605 |
| `item-m-plus-c` | 2 | 31 | -0.8770969421709667 | 1.686404881540754 | 1.1638107733387089 | -2.0409077154870965 |
| `item-m-plus-c` | 3 | 28 | 1.1220349091964241 | 0.8654988375657654 | -1.2141622702500008 | 2.336197179435714 |
| `item-m-plus-c` | 4 | 38 | 0.28620535582368517 | 1.7948490793683292 | 0.5231070907605265 | -0.2369017348815793 |
| `item-m-safe` | 1 | 501 | 0.8991263378299401 | 0.3261258436241331 | -0.26347085713692614 | 1.1625971949544909 |
| `item-m-safe` | 2 | 504 | 0.965591594697817 | 0.3381116020149563 | -0.4783680687543645 | 1.4439596634464285 |
| `item-m-safe` | 3 | 479 | 0.9424647366889358 | 0.2238444848266483 | -0.5412735746217119 | 1.4837383113045928 |
| `item-m-safe` | 4 | 516 | 1.017723407602713 | 0.21988715846672133 | 0.26066379129709283 | 0.757059616282558 |

Holdout, on seeds the strategies never saw: `item-m-all` mean 101.34648773350678, retail 126.12749112223977, arbitrage -24.781003388749372; `item-m-plus-a` 100.35329357035293 / 123.56234597949526 / -23.20905240914923; `item-m-plus-b` 102.11399036791022 / 125.7037225511236 / -23.589732183230424; `item-m-plus-c` 89.19867549086285 / 120.57814024763785 / -31.37946475679786; `item-m-safe` 94.4769774633412 / 118.4531573609182 / -23.97617989758095. All five report zero failures. These holdout means are not comparable to the 108.63974289615767 start score, which was measured on seeds 1000..1599.

## Fixes that held everywhere they were tried

a2-after, a2-ledger, a3-rich, a3-free, a4-rich and a4-stock were kept in every file that measured them. a1-jumps was kept by `item-m-plus-a` (+0.5009455722593997) and `item-m-safe` (+0.8317693322811999) but lost in `item-m-plus-b` (-0.46009330345589977, SE 0.5348458123513586) and untested in `item-m-plus-c`. a1-free was kept by plus-a and plus-b and dropped by m-safe. a4-free was dropped by plus-a and plus-b and kept by plus-c and m-safe. The disagreement on a1-jumps and a4-free is inside the noise for a1-jumps and one-sided for a4-free.

## Which file to enter first

`item-m-plus-b`. It uses all four blocks, passed the widest exactness check (600 runs per spread), measured every fix on 1000 paired runs, ran the full 4000-run holdout, and has the highest holdout mean of the five (102.11399036791022) with zero failures. Second choice is `item-m-plus-a` (holdout 100.35329357035293), which additionally recovered a1-jumps but ran 3000 of the 4000 holdout seeds and timed its two strategies concurrently, so its seconds are not a clean serial comparison.

The strategy code is not reproduced here, as the brief requires ("Leave the code out"); it is the `code` field of each item result, and `item-m-plus-b`'s is 40014 characters with SHA-256 4f9167dddd457f394e988bf9c9e2576dd6120834bfb8d93573ce9451fd587598, `item-m-plus-a`'s 37922 characters with 5d1bd5272884f513b19f0e66a7c235f6c188a08e4f7787ac9346f1614dda3ed3. Those files live in the repository at `artifacts/goal/items/m-plus-b/result.json` and `artifacts/goal/items/m-plus-a/result.json`. This report alone cannot carry either entry: the code is roughly 40 kB and this file is capped at 16000 bytes.

## Files that are unsafe to enter

`item-m-plus-c` is the least safe. Its exactness rests on 30 runs per spread, its by-spread differences come from 28-43 runs with standard errors up to 4.055074254964557, its holdout covers only seeds 130000-130139 (140 runs, stated in its `tried` field), its `base_mean_edge` was never measured, its spreads 1 and 2 carry untested fixes, and it was built on a machine with one CPU where the reference CLI did not finish 600 runs in ten minutes. It reports mean edge 89.19867549086285 on holdout, far below the other files. `item-m-safe` was measured under PyPy 3.12.15, not the reference CPython 3.12.3, and its own note says exactness therefore holds within PyPy and does not establish CPython bit parity; its run counts were also halved. Its gain (+0.95685317308875) is the smallest of the five. `item-m-all` is safe to enter but is the block-only build with no fixes, so it gives up the fix gains.

Two smaller cautions: `item-m-plus-a` placed the a1-jumps split before the spread-1 flow-tracking block, a placement the brief did not specify, and its arithmetic is the one part of its merge not covered by an exactness check against a source file. `item-m-plus-b` dropped a1-jumps and a4-free, so it is not the union of every fix.
