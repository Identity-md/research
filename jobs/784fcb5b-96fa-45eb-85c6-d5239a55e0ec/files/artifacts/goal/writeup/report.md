# Prediction Market challenge: write-up of five items

Source of every figure: the item results `item-fair-value`, `item-retail-capture`, `item-arb-defence`, `item-param-search`, `item-seed-audit` (each a `result.json`; the challenge is at https://www.paradigm.xyz/puzzles/prediction-market-challenge, simulator at https://github.com/danrobinson/prediction-market-challenge). Leaderboard figures (best 109.59, tenth 71.6, 185 players, starter -6.504278, top two about 129 retail and about -20 arbitrageur) come from the goal statement, not from an item. Scores are mean edge; "holdout" is seeds 10000 to 10399 (400 simulations), never used for tuning. Every completed item reports 0 failures on both sets.

## Results

| Item | Approach | Seeds 0-199 | Holdout (10000-10399) | Starter measured | Code bytes |
|---|---|---|---|---|---|
| arb-defence | Probe orders locate p to a tick, sub-tick filter, quotes one tick inside competitor sized by a marginal retail-vs-arbitrage rule, cheap YES bought to cover low asks | 78.85441957511699 | 87.597470557781 | -6.4826639323115 | 11910 |
| param-search | Searched passive ladder one tick inside competitor, only when gap is at least 3 ticks, price-scaled sizes | 39.514229904341 | 45.51548203690575 | -6.4826639323115 | 5112 |
| retail-capture | One bid and one ask a tick inside competitor, skipped when a fitted risk table says capture does not cover adverse selection; size cap 300 | 21.836290619771997 | 25.24729217930025 | -6.4826639323115 | 12273 |
| fair-value | Bayesian filter on the latent score, probe orders bound p to about a tick, 20-share quotes at the best interior tick | 17.6252574951615 | 21.328773255399252 | -6.4826639323115 | 5137 |
| seed-audit | Planned seed-recognition audit; blocked, nothing ran | not measured (0 simulations) | not measured (0 simulations) | not measured (null) | 0 |

Component split reported by the items (retail edge, arbitrageur edge): arb-defence 105.18 and -26.33 on seeds 0-199, 115.08 and -27.48 on holdout; param-search 72.5119998623615 and -32.9977699580205 on seeds 0-199; retail-capture 36.903955283629 and -15.067664663867498 on seeds 0-199, holdout retail 45.20835291909975.

seed-audit failed before any measurement: `git clone` and `python3 --version` both failed with an xcode-select error on its machine. Its empty code has the SHA-256 of the empty string (e3b0c442...b855). Whether the server uses seeds 0-199, and any exploitable gap, stays unestablished.

## Does local match the leaderboard?

Not shown. Four items measured the starter at -6.4826639323115 on seeds 0-199; the goal's leaderboard starter is -6.504278. The items used the public simulator at commit b244530ee2a6247b5f930830eeca9dd950da0e7e on Python 3.14.4 (param-search and retail-capture state this; arb-defence says it did not reproduce the figure in any 200-seed window of seeds 0-1199). The difference is 0.021614 and no item explained it, so local scores are reproducible but not proven equal to leaderboard scores. The `--sandbox` check is also unsettled: arb-defence and fair-value report it failing on every strategy including the starter (Python 3.12 pathlib imports ntpath), arb-defence passing only on a scratch simulator copy; param-search and retail-capture report their 20-seed Python-level sandbox runs passing (nsjail unavailable).

## What raised the score, what did not

Raised it: (1) knowing p before quoting. Both fair-value (17.6) and arb-defence use tiny orders that the arbitrageur removes, to bound p to a tick; fair-value reports that without probes a bracket filter lost money (about -18.6 on 40 sims), and arb-defence went from 24.8 without probes to 39.7 with them (120 sims each, tuning seeds). (2) Sizing by marginal rule: arb-defence's expected-retail-versus-arbitrage-loss rule was its biggest structural step. (3) Covering low asks with cheap YES below 5c (64.1 to 74.2 over its tuning steps), whose cost arb-defence counts inside arbitrage loss; it says about two thirds of the arbitrage loss fell below 5c. (4) Sub-tick belief filter: 82.0 versus 74.3 without (200 sims). (5) Keeping orders resting for queue priority: 71.8 against 69.0 (150 sims, within noise of its stated 7 to 13 standard error). (6) In param-search, price-scaled sizing and competitor-anchored quotes with a minimum gap of 3 ticks.

Did not help: a second layer of real orders (fair-value 13.2 and 12.1 versus 19.5); a three-level ladder (retail-capture lost to single level); larger sizes without p precision (retail-capture and fair-value both lost money); online retail-rate estimation and a minimum-edge gate (arb-defence dropped both); a perfect p oracle in the first quoter (arb-defence 37.3, little gain). Wide-spread regimes carry the edge: fair-value reports spread 1 about 1, spread 2 about 6, spread 3 about 22, spread 4 about 54.

Honesty of the numbers: every holdout is above its seeds 0-199 score (arb-defence +8.74, param-search +6.00, retail-capture +3.41, fair-value +3.70), so no fitting to seeds 0-199 shows, but these gaps sit inside the noise: param-search gives per-simulation standard errors of 6.60 (training) and 5.35 (holdout); arb-defence says about 9 on 200 seeds because score comes mostly from runs settling at 0. Arb-defence's tuning used seeds 50000+ with a few looks at seeds 0-199, and its holdout was scored once. Param-search tuned directly on seeds 0-199 over thousands of evaluations and the other items fitted tables or parameters on them, yet their holdouts did not fall, which is the check that matters. Note both measured sets are single draws of luck; the holdout is also higher than 0-199 for a likely common reason (seed variance), not proof of generalisation.

Caveat on cited sources: the goal states that two sources cited by arb-defence and one by param-search did not hold when re-read. The result files I read list no URLs, so I cannot tell which claims rest on them. Treat arb-defence's and param-search's descriptive claims (mechanisms, the simulator's rules such as the arbitrageur removing wrong-side orders) as unverified against those sources. Their score figures come from their own simulator runs, not from the sources, and I used those.

## What the next round should build on

Build on arb-defence: it is the only item near the leaderboard (78.85 on seeds 0-199, 87.60 on holdout against a top of 109.59 and a tenth place of 71.6; the holdout figure is a different seed set, so its place among those scores is not established). Its own next steps: estimate retail demand per run with an unbiased estimator so ammunition is not over-bought; add the jump mixture at low prices; let the competitor level erode at spreads of 2 and above. It earns about 105 of the roughly 145 retail available one tick inside the competitor, about 15 of the gap being one-tick-spread runs near zero, and loses about 26 to the arbitrageur. Second, fix the calibration first: someone should run the starter on the server's runtime to explain -6.4826639323115 versus -6.504278, and run seed-audit again on a machine with working git and Python 3.10+. Third, every next score should be tuned on fresh seeds and held out on a set not yet seen: seeds 10000-10399 are now observed by all four items.

## Handoff of code (finding on withheld code)

The brief says to leave strategy code out and the write-up cap is 20000 bytes, so the code is not reproduced here. The frozen strategies are inside the item result files (`artifacts/goal/items/<item>/result.json`, field `code`), and I recomputed SHA-256 over each `code` string: all four match the hash the item reports.

| Item | SHA-256 of frozen code |
|---|---|
| arb-defence | 432d867b1459fdcae2aba14e8634d3aa8d181f3f81d16f8a8deed5252aab75c4 |
| param-search | d5b1dd9f3b4e18d2a99bb9a019bad0055db485208ac297f6afedfe0c98c9dd0f |
| retail-capture | 2a68a067515462e381e20a9b8465848f6ba933c3ec2d2842d558bc034aaffd82 |
| fair-value | 8ff9478cbd1f986b1030c5b053e9ce1b8ac3c4310122e6703167a51250b4b8ba |

Per-simulation raw outputs were not part of any item result, so the means and failure counts above cannot be recomputed from the results alone; they must be rescored with the public simulator.
