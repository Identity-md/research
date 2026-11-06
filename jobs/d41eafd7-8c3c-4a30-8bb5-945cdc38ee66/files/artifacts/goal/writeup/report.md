# Combined market blocks: candidates for operator pricing

Recommend **c1-pairs, c2-queue, c3-all and c4-all** for spreads 1, 2, 3 and 4 respectively, subject to the qualifications below. These are selections among the supplied local results, not newly measured improvements on Paradigm. Each has a confirming mean gain over its priced comparator larger than its reported paired standard error. There is no paired comparison between all competing files, and their different seed subsets prevent a conclusive ranking from absolute means alone. The exact files and results are obtainable through the source links below; the strategy is the JSON `code` string, not the JSON document itself.

## Goal and established reference

The requester reports a network score of **107.58**, first place **109.93**, and a base score of **106.804593** on Paradigm's 200 runs. The priced isolated improvements are spread 1 **+0.775951**, spread 2 **+0.065331**, spread 3 **+0.172915**, and spread 4 **+0.574129**; the requester gives their combined value as **108.392919**. These are task-brief figures, not measurements from this write-up. The brief also reports a candidate gaining **0.95** per run on **2,035** unseen runs but losing **0.73** on Paradigm's runs. Consequently none of the local improvements below should be added to the leaderboard score before operator pricing.

Reference artifacts: [base](https://api.imd.fun/artifacts/41fa8829432f502a00c5302c0e2200b475c5c2e100a2a16b086aaab0ce62a395), [parent for scorer calibration](https://api.imd.fun/artifacts/40497298132dcc0ccc9f4c0672031c7eaae00ddcf8cf24983db989feeb3c5ca0), [priced spread 1](https://api.imd.fun/artifacts/08e3cde58c80ef5d44a5af6a896eeeef75abff9ff749e01d2ee329f1c68d2d60), [priced spread 2](https://api.imd.fun/artifacts/90459c5fffa37760b92c6a3ee93523240927484a7c8fa36b5d12b55a37c08733), [priced spread 3](https://api.imd.fun/artifacts/9acbf0cf247803e24c4e9e0ae987f830bc304be449b9981a837ed2d2ce7e62f2), [priced spread 4](https://api.imd.fun/artifacts/c80c33382f9c458ab6286dbc11fa761100a7e156dad7f3c12d74040b7c76578f). Simulator: [prediction-market-challenge](https://github.com/danrobinson/prediction-market-challenge). The priced mechanisms are, respectively: fivefold inside tick-2 asks under one cent with front asks retained; flow-scaled one-cent stock; per-run retail-rate/order-size adaptation; own-fill flow adapting ask sizes and stock (task brief and each item's `approach`).

## Confirming results

Every row cites its complete source JSON, including code, metrics and `tried` history. Numbers are transcribed without rounding. `ΔB ± SE` is candidate minus base; `ΔP ± SE` is candidate minus the priced block of the same spread. R/A are signed retail/arbitrage **differences against base**, not absolute edge or percentages. SE applies to total paired edge, not separately to R/A; component SEs were not supplied. Seconds are **base → candidate** on the item's timing sample, not full experiment duration. Identical means every reported SimulationResult field matched on the sampled other-spread runs; it is a reported finite check, not proof for all seeds. All items report zero candidate confirming failures (`holdout.failures`).

| Item / source | Spread | Pieces in delivered file (`contains`) | Confirming ΔB ± SE | Confirming ΔP ± SE | R / A versus base | Other spreads | Seconds, base → file |
|---|---|---|---|---|---|---|---|
| [c1-asks][c1-asks] | 1 | priced; s1-flow; q1-bids; q1-life | 2.3158657605373905 ± 0.33790506947116516 | 1.172168248613437 ± 0.2650408952050327 | 1.9363245830365143 / 0.37954117750847133 | true, 450 runs | 106.87160528847016 → 113.64596724743024 |
| [c2-all][c2-all] | 2 | priced spread-2 stock rule; s2-queue; s2-bids; q2-bids | 1.9979966456981875 ± 0.43704142763605786 | 1.237787021428701 ± 0.2532515879206801 | 2.4086684871730113 / -0.4106718414738167 | true, 450 runs | 59.249468920752406 → 59.32930721901357 |
| [c4-all][c4-all] | 4 | flow estimate; s4-bids; s4-asks; s4-queue; s4-middle; q4-ahead | 2.6078896352397063 ± 0.3826353790638878 | 1.5376988909949292 ± 0.15877897548684153 | -0.9020334121042604 / 3.5099230473390977 | true, 900 runs | 180.40632511256263 → 180.89650815119967 |
| [c3-all][c3-all] | 3 | s3-flow; s3-clock | 3.041444306678269 ± 0.9323195936655891 | 0.43899751404466797 ± 0.06254419195348541 | -1.423968732666096 / 4.465413039345876 | true, 450 runs | 146.9139512560796 → 148.38329777796753 |
| [c1-bids][c1-bids] | 1 | priced; q1-bids; q1-ahead | 1.7861548137700443 ± 0.3038745811145147 | 0.4797752608084268 ± 0.27459321069697257 | 1.991669698763176 / -0.20551488499035536 | true, 900 runs | 210.5617640367709 → 216.10719215264544 |
| [c1-all][c1-all] | 1 | s1-flow; priced spread-1 front rule (q1-ahead family); q1-bids; s1-bids | 3.951276983398 ± 1.512010620337482 | 1.0885710578066663 ± 0.7838365727203974 | 1.7511890804060009 / 2.2000879029686664 | true, 450 runs | 100.46663093566895 → 107.09078288078308 |
| [c1-pairs][c1-pairs] | 1 | priced spread-1 block; s1-flow; q1-ahead; q1-bids | 2.5414027248259132 ± 0.3917162243225099 | 1.235023171864296 ± 0.2813482609549018 | 2.4835917405638086 / 0.057810984265221715 | true, 900 runs | 63.8 → 66.3 |
| [c2-queue][c2-queue] | 2 | s2-queue; s2-stock; s2-bids; q2-bids | 2.0015597964197385 ± 0.43721099433183286 | 1.2413501721502518 ± 0.2535360118153212 | 2.4149221962356497 / -0.4133623998147029 | true, 450 runs | 280.492975549947 → 286.24650167889195 |
| [c4-pairs][c4-pairs] | 4 | priced; s4-bids; s4-asks; s4-middle | 2.163802854692901 ± 0.37363360350464353 | 1.093612110448124 ± 0.15242673594139847 | -1.5476680507807814 / 3.7114709054788033 | true, 900 runs | 137.76304837525822 → 139.73779390007257 |
| [c4-bids][c4-bids] | 4 | s4-flow; s4-bids; s4-asks; s4-queue | 2.3673774663976173 ± 0.39728777155944645 | 1.2971867221528401 ± 0.12661881993565946 | 0.5323073541067436 / 1.8350701122989859 | true, 900 runs | 127.7686242449563 → 126.65608088183217 |

### Sample sizes and comparability

Choosing uses eligible seeds in **20000–27999**, confirming in **80000–87999**, with spread selected by sampled competitor spread. Earlier-seat ranges **8000–15999** and **60000–67999** are excluded under the brief. Items report no constant tuning or seed recognition. They report simulator revision `b244530ee2a6247b5f930830eeca9dd950da0e7e`, default 2000-step simulations, and parent calibration **108.63974289615767** on 600 runs starting at seed 1000; this calibration is distinct from the base's private Paradigm score. These are the items' methodology claims, not simulations rerun for this report. [c1-asks][c1-asks] [c2-all][c2-all] [c3-all][c3-all] [c4-all][c4-all]

- **c1-pairs / c1-bids:** all 2016 choosing and 2053 confirming spread-1 seeds. c1-bids times 200 confirming runs; c1-pairs gives seconds without a sufficiently explicit timing sample/protocol, so its runtime comparison has weaker support. [c1-pairs][c1-pairs] [c1-bids][c1-bids]
- **c1-asks:** every second sorted eligible seed, 1008 choosing and 1027 confirming; timing on 100 confirming seeds. **c1-all:** first 150 eligible seeds in each window, timing on 150 confirming runs. Their absolute holdout means therefore do not rank them against full-window c1-pairs. [c1-asks][c1-asks] [c1-all][c1-all]
- **c2-all / c2-queue:** first 995 choosing and 993 confirming eligible spread-2 seeds; timing on 100 paired runs. c2-all times choosing seeds, c2-queue confirming seeds. c2-queue used checked heap-priority lookup indexes in its scoring harness, with original lookups for calibration and timing; it reports 32 full-run lookup comparisons and 30 confirming audit runs, plus extracted-code reproduction on one confirming seed per spread. These audits support but do not independently certify its optimization equivalence. [c2-all][c2-all] [c2-queue][c2-queue]
- **c3-all:** first 1020 choosing and 994 confirming eligible spread-3 seeds; timing on 100 confirming runs. Its initial half-window jobs were corrected to eligible-seed half-counts before confirming outcomes were available; supplementary 1061-seed figures did not select another file. [c3-all][c3-all]
- **All spread-4 items:** full 1953 choosing and 1972 confirming eligible seeds, timing on 200 spread-4 runs. c4-bids' final same-process timing ran base then candidate rather than alternating; do not treat the small speed differences between items as a controlled cross-file benchmark. [c4-all][c4-all] [c4-pairs][c4-pairs] [c4-bids][c4-bids]

## Spread decisions and interactions

### Spread 1: c1-pairs, with an ask-sizing overlap to price explicitly

Choose **c1-pairs** as the strongest full-window confirming candidate: **1.235023171864296 ± 0.2813482609549018** over priced. This exceeds one SE. Its full-window comparator c1-bids yields **0.4797752608084268 ± 0.27459321069697257**; the items do not supply the paired SE of c1-pairs minus c1-bids. c1-asks yields **1.172168248613437 ± 0.2650408952050327** on a different subset and is a credible alternative. c1-all's **1.0885710578066663 ± 0.7838365727203974** has much weaker precision. All four mean gains exceed their own SE, but this is not a formal selection-adjusted confidence claim. [c1-pairs][c1-pairs] [c1-bids][c1-bids] [c1-asks][c1-asks] [c1-all][c1-all]

The chosen file contains priced + s1-flow + q1-ahead + q1-bids. Flow adapts sizes and stock using partial front fills; q1-ahead preserves safer-price orders and enlarges tick-2 capacity; q1-bids banks ahead bids and tracks stock bids. On choosing runs, flow alone over priced gained **1.092327009775** (SE **0.29078471351826235**), adding ahead to flow gained **0.574983697047768** (SE **0.29465465747708547**), but adding q1-bids after those gained only **0.0006061611433031366** (SE **0.12345683271244572**). Thus q1-bids' standalone benefit overlaps heavily with q1-ahead. q1-life added only **0.0003517670411706367** (SE **0.0004889418420584428**) and was not retained; s1-bids was not tested on the final combination after its standalone pair lost. [c1-pairs][c1-pairs], `approach`, `tried`, `next`.

Do not describe the chosen file as deduplicated tick-2 sizing: its code retains both q1-ahead's 15000 cap in ask sizing and the priced fivefold multiplier. Its own `next` flags that overlap. This is the exact measured candidate, not a recommendation to remove either rule without testing. In contrast c1-asks explicitly avoids stacking overlapping tick-2 policies; q1-ahead as replacement lost **-0.13092642743234134** (SE **0.41367209627450097**), whereas its flow, bid and life additions were positive. c1-all found life negative and kept stock suppression; c1-asks and c1-bids rejected stock suppression. These differences are conditional interactions and sample differences, not additive gains. [c1-pairs][c1-pairs] [c1-asks][c1-asks] [c1-all][c1-all] [c1-bids][c1-bids]

c1-pairs supplies retail/arbitrage differences versus base in the table, but does **not** supply them versus priced; c1-all also lacks that decomposition. Do not manufacture them by combining differently rounded or sampled references. [c1-pairs][c1-pairs] [c1-all][c1-all]

### Spread 2: c2-queue, with c2-all essentially tied

Choose **c2-queue**, which reports **1.2413501721502518 ± 0.2535360118153212** over priced, larger than its SE. Its priced-relative retail gain is **2.070578441567271** and arbitrage change **-0.8292282694174219**: more retail offsets worse arbitrage. c2-all gives **1.237787021428701 ± 0.2532515879206801**, retail **2.0643247325046326**, arbitrage **-0.8265377110765357**. Their close means do not establish superiority; no paired cross-file SE was supplied. Retain c2-all as a near-tied alternative with a different implementation/harness history. [c2-queue][c2-queue] [c2-all][c2-all]

Both contain queue + flow-scaled stock + s2-bids + q2-bids. In c2-all, queue-first stock and priced-first queue matched every result on 995 choosing seeds: the route is overlapping implementation, not two gains to stack. Stock added **0.44913139023748744** (SE **0.26353360832830547**); s2-bids added **0.3464649139261305** (SE **0.07697208759753545**). The last bid-lead increment is noisy: c2-queue reports **0.03996440252572866** (SE **0.16145088231340582**), c2-all **0.045455215024723515** (SE **0.16184103654713325**). Their distinct full code hashes and outcomes mean the final files must not be treated as identical despite matching earlier route checks. [c2-all][c2-all] [c2-queue][c2-queue]

c2-queue's attempts to remove whole-order retention, keep only one side, alter the threshold or remove remainders all lost on its 125-run choosing diagnostics. Those paired deletions support retaining queue protection; direct oversized-order fill attribution alone is not a causal benefit estimate. The final q2-bids retention takes precedence for eligible ahead bids in c2-all, with queue logic handling remaining orders. [c2-queue][c2-queue], `tried`; [c2-all][c2-all], `approach`.

### Spread 3: c3-all, flow plus clock

Choose the sole supplied spread-3 combination **c3-all**: **0.43899751404466797 ± 0.06254419195348541** over priced, exceeding its SE. Priced-relative retail is **-0.0932503857858147**, arbitrage **0.5322478998288732**. The clock suppresses above-fair ammunition bids at ticks >=2 while H>500, before unchanged bridge logic. It adds risk control to priced flow. [c3-all][c3-all]

Adding s3-asks to flow fought the strategy: choosing total **-0.7963580444730389**, retail **1.1646048153936286**, arbitrage **-1.9609628598711766**, SE **0.8694739606602105**. Clock on flow alone gained **0.2643145625191177** (SE **0.11252652046932754**). Flow + asks + clock still lost to flow, so the ask rule was discarded. The supplied result supports that local interaction; its upstream source warning below limits independent provenance. [c3-all][c3-all], `tried`.

### Spread 4: c4-all, all supplied behavioral pieces

Choose **c4-all**: **1.5376988909949292 ± 0.15877897548684153** over priced, exceeding its SE. Its priced-relative retail change is **-0.5492577147797674**, arbitrage **2.086956605759584**: this candidate improves chiefly through reduced arbitrage losses. It has the highest reported confirming improvement on the shared full window among the three spread-4 files, but their paired cross-file errors were not supplied. c4-bids reports **1.2971867221528401 ± 0.12661881993565946** and c4-pairs **1.093612110448124 ± 0.15242673594139847**, also exceeding their own SE. [c4-all][c4-all] [c4-bids][c4-bids] [c4-pairs][c4-pairs]

The chosen file adds to priced flow: half-depth low-price regular bids, a 50-share ahead threshold for low-price asks, retention up to three times desired front-ask size, middle-ask loss scaled by 1.4, and split resting-ahead bids. Each sequential addition had positive choosing mean; middle sacrifices retail for arbitrage protection, while ahead added **0.18278774083492066** (SE **0.04061513422078071**) after middle. Arithmetic optimizations and flow estimation are retained once. [c4-all][c4-all], `approach`, `tried`.

c4-bids isolates bid + ask + queue. Its choosing ask/queue interaction is **0.040161479966052564** (SE **0.037092136572651355**); it characterizes them as approximately additive, without precise evidence of positive synergy. c4-pairs' different greedy path retained bid + ask + middle; queue and ahead gave positive increments on an earlier triple but were not in its returned file. That is not evidence they add the same amount on every later block. c4-all supplies the actual tested all-piece alternative; same-spread gains from these files must not be summed. c4-pairs does not supply confirming retail/arbitrage differences versus priced. [c4-bids][c4-bids] [c4-pairs][c4-pairs] [c4-all][c4-all]

## Evidence limits and pricing handoff

The task flags upstream source reread failures for **c4-all (3 sources), c3-all (1 source), c4-pairs (4 sources), c4-bids (4 sources)**. The failed passages and exact source identities are not present in the supplied result JSONs, so this report cannot determine which specific upstream claims failed or repair their provenance. Treat descriptions of inherited mechanisms and original claimed gains in these items as contributor assertions. Their code and locally reported combined measurements remain inspectable in the linked results, but successful retrieval of those results does not independently validate the failed upstream citations or reproduce their simulations. Spread-3 and spread-4 recommendations are therefore provisional on operator pricing, with this additional provenance qualification. Warning counts come from the task brief; the linked results supply the claims being qualified.

Across spreads the brief says isolated gains on the same fixed scored runs add exactly, because a run has one fixed spread. That does not justify summing conditional local means from unequal spread subsets, and this report provides no invented combined leaderboard forecast. Nor do finite unchanged-other-spread checks prove universal isolation. Price each exact selected file against its corresponding priced block on Paradigm before composing a new four-spread submission; no new merged strategy has been measured or delivered here. The selected items themselves request operator pricing in `next`. [c1-pairs][c1-pairs] [c2-queue][c2-queue] [c3-all][c3-all] [c4-all][c4-all]

## Retrievable strategy and result artifacts

Each link below is a complete content-addressed JSON result, with the **full JSON SHA-256 in its URL**. It contains the exact Python strategy in `code`, its separate `code_sha256`, and all result fields cited above. Download the linked JSON, verify the raw response against the URL hash, decode `code` as a JSON string, and save its UTF-8 bytes without adding a newline. Verify those bytes against the complete code hash below before entering the Python file. No code is included in this prose. The JSON artifact hash and Python code hash are different objects and are not interchangeable.

During this revision all ten URLs returned HTTP 200 with bytes exactly matching the corresponding supplied input SHA-256; every decoded strategy matched its declared code SHA-256 and parsed as Python. These are retrieval/integrity checks, not simulation reruns. Public URLs provide the underlying results even when the local `artifacts/goal/items/` and `.imd/reads/artifacts/` inputs are absent from the reader's delivered bundle.

| Item | Complete JSON result and exact strategy | SHA-256 of decoded Python `code` |
|---|---|---|
| c1-asks | [Retrieve JSON + code][c1-asks] | `cc19ea1c12c8b318e99bd933ebe147d51e207a388f5e1ba5c7bdd3f562f9d73d` |
| c2-all | [Retrieve JSON + code][c2-all] | `c830dd0245a9a64248ede6f93e8879986b7f018fb156b218882e0fd029cbcfd3` |
| c4-all **recommended** | [Retrieve JSON + code][c4-all] | `d96399a0cd50e3e4f9e5121656b227f9f4d61e088500919b18073dfdd91bc864` |
| c3-all **recommended** | [Retrieve JSON + code][c3-all] | `2d763767160f2791f9e92e18300f49a5fce7ce7e99a717c463c3e8c081920550` |
| c1-bids | [Retrieve JSON + code][c1-bids] | `6e96989063548d73f4b791241e4c57be6c964243a3e64e88f9a560734a208fee` |
| c1-all | [Retrieve JSON + code][c1-all] | `b1fad1bd6fc156564de5a17ffd616791b9b7123814c94488cb6d0f7babc0ce73` |
| c1-pairs **recommended** | [Retrieve JSON + code][c1-pairs] | `f627ba06a2fe47399e5170ab1885ddec5fd6c06e8a27f8293005b93daaaa32f7` |
| c2-queue **recommended** | [Retrieve JSON + code][c2-queue] | `5948bf6227f4224bb2358dd267a562f6459693eb32f134ba30eeb6771f9a7f0a` |
| c4-pairs | [Retrieve JSON + code][c4-pairs] | `2314723a8e7644db204d39a7b4d53aa8c59a90bc3edf46b53dbf4978ab52cef0` |
| c4-bids | [Retrieve JSON + code][c4-bids] | `50be0e64e1c1a8e123c933da5d8d053df26a496993f6df0134d940fe0331691a` |

Source references resolve directly to the public artifacts rather than ephemeral local input paths. For the numeric table, field paths are `spread`, `contains`, `diff`, `vs_priced`, `others_identical`, and `seconds`; sample sizes, component differences versus priced and interaction results come from `approach` and `tried`. No seed-level result arrays or independently rerunnable scoring harness are supplied in these JSONs; recomputing SEs requires rerunning the referenced simulator and the supplied strategies with the stated sampling protocols.

[c1-asks]: https://api.imd.fun/artifacts/de522a500fedf4a446fa3ef2f2f9fb67de2d73b8055791ed305cb2b7af6b9e91
[c2-all]: https://api.imd.fun/artifacts/37b6dccc9781fa12cb46570e5c0cbda865dc673ea687aabe022cef3cba3d8518
[c4-all]: https://api.imd.fun/artifacts/46b20a51dbb98abf4c9f7832f362dc8320c2c3288dae986a8863a7455bd57402
[c3-all]: https://api.imd.fun/artifacts/bc97804003250f22e8b605ca973dcd8525620e1feac81000149d17cb6af1c08f
[c1-bids]: https://api.imd.fun/artifacts/6931c7d9c4f5a595b7da90da1651027f2a976de03ad1757d3c5f37b2bbc8bcd8
[c1-all]: https://api.imd.fun/artifacts/7ef8d7351e6d049c5dddce5a84b0f0fda724156fa58bb057db3143a9679b32d0
[c1-pairs]: https://api.imd.fun/artifacts/f7304b601a970104247074052cd75db749edc8d9e989fcce2a67c98bdcdc44bd
[c2-queue]: https://api.imd.fun/artifacts/fbaba62304b28380cd79b2de69f597deba95429638ed18a2bf5391077d025558
[c4-pairs]: https://api.imd.fun/artifacts/4b7801cabe5516bfab4948a8a96285db64e6da008377006f5f03852a019a0ce3
[c4-bids]: https://api.imd.fun/artifacts/e6482970a6b03e462c163c97d382b5b94f13a3451ad18bf4dfcfffae7f763829
