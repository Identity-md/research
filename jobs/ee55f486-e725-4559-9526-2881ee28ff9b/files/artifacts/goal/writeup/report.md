# Where the base leaves points: ceilings for the Prediction Market strategy

Goal: measure where this network's Prediction Market strategy leaves points on the table, so the next rounds build only where there is room. Challenge: https://www.paradigm.xyz/puzzles/prediction-market-challenge; simulator and rules: https://github.com/danrobinson/prediction-market-challenge (docs/orderbook_prediction_market_challenge.md). Base: https://api.imd.fun/artifacts/ecbc9087b4f238fc1b5b0d52f55af073f676c038bfb6756172b1e51480ac1741. It scores 109.27254289017199 on seeds 1000-1599 and 98.28063388702982 on seeds 50000-53999. On 2026-11-06 the network is 3rd of 186 at 105.39 (127.13 retail, 21.74 lost to the arbitrageur). First place is 109.59 (130.77 and 21.18) and second is 109.43 (127.73 and 18.31). The gap to first is 4.2 points.

## Where the evidence comes from

Each figure below comes from one of the 12 seat results this write-up was given. A reviewer found that the earlier version linked to `../items/<seat>/result.json`, and those files were not shipped with the report. That finding held. This step may write only this file, so it cannot ship the seat files. Instead, every result is named here by its input id and SHA-256, and the provenance that matters (simulator commit, the exact rule edit, the seeds and the cleanliness checks) is copied from it below. Anyone holding the goal's inputs can check each number against the file with that hash.

| Input id | SHA-256 |
|---|---|
| item-edge-map | 67739daf82fc4f316bcc45627b4e9c11397bad4976819615d204299810f6227b |
| item-missed-retail | baeb4cd4c7e3984f601ce4d0c355ff3b99ef4333a40141e06534a4fa6fbfb99a |
| item-no-jump-loss | 748e4651884e819876c1d7b6484bc5395f4708a856d2b4951ba0671c5ed6c26d |
| item-no-drift-loss | 9185ecc575b4139ce7e3d2c832d82562a6273a41232aa54cc413d7272290c941 |
| item-free-stock | 64a9f0aadb4b04890bf9484bc304d35167ffd97c11a8b6101f0e8398c4398150 |
| item-unlimited-stock | 88ddb854baa53b061049a90a7df877232af4a7a990b514e2252920321e5a6dd0 |
| item-unlimited-cash | 9e02cd0bf8e19145f5fd010f70ddc71c726db3654c0b6fa6fbda4cac0f3595c9 |
| item-front-of-queue | 492af6f29535ab382bb54d7dcca15872c63125e946e7608cc67622937482c1f4 |
| item-retail-foresight | 1a82946dd3fc2a6d2822979711560709d038a8eaa307c0730dbd5a9f62d70140 |
| item-no-competitor | a129ee178233af5c5db46febbcb1a2df3e4caccc53e057f3610d192cd937d225 |
| item-rich-runs | c7c99d0696b28e0eb0c17bbe2604e0015deefde1417c7696feac5948ef9ade0c |
| item-leaders-path | edb08d1026c85ac831d0a8864efdef1a12e10040043528d6dfd0b6fc24f27ba8 |

All seats used simulator commit b244530ee2a6247b5f930830eeca9dd950da0e7e. Every seat that states the hash of the extracted base code gives SHA256 baef955ec10728839f7c3357016ec9eb0550e7ec689bbd5171b1cdd5c9e37273. Unless a row says otherwise, gains are paired differences (what-if minus base, run by run) over 4000 runs on seeds 50000-53999.

Six results cite sources that did not hold when their machines read them again: no-jump-loss (3 sources), no-drift-loss (2), free-stock (1), unlimited-stock (2), front-of-queue (1) and retail-foresight (1). The results as given here do not show which statement each failing source supported. So read any claim in those six that rests on an outside page (as opposed to the seat's own simulator runs) as unverified. Their measured diffs come from their own runs and are reported as such.

## Ceilings, largest first

Gain = ceiling (SE). R / A = retail and arbitrage parts. By spread = gain in runs with competitor spread 1 / 2 / 3 / 4 (SE).

| What-if (input) | Gain (SE) | R / A | By spread | Clean? |
|---|---|---|---|---|
| Participant first in queue at equal price, and quotes at the competitor price instead of one tick inside (item-front-of-queue) | 47.859869056410425 (1.0281727297941858) | 56.70016212783635 / -8.84029307142165 | 47.81785765661555 (2.6594672731265394) / 48.32466608308256 (2.001400493789408) / 49.026854450867944 (1.825312511198579) / 46.20041807953684 (1.525828180258) | Clean by its own account, but the seat calls it a joint change (priority plus repricing). Priority alone is 1.9795897512764 (SE 0.11741239655341132; retail 1.681778585250425, arb 0.2978111660273251). One source did not hold. |
| No competitor in retail matching; the competitor's quote signal is replayed from the baseline (item-no-competitor) | 15.654209962010375 (0.4816910156520244) | 15.323160906893499 / 0.3310490551177251 | 18.887432062729626 (1.1434272178383673) / 15.133287683067834 (0.9113268051278619) / 16.547512201622816 (0.9387478713801712) / 11.863124721936119 (0.8002261562593375) | Clean on information. It includes monopoly price and FIFO advantages, which the seat says are intrinsic to removing the competitor. |
| Free stock: negative edge forgiven on YES bid fills at 5 cents or below (item-free-stock) | 10.600204159728674 (0.47489436001810703) | 0.0 / 10.600204159729392 | 16.15857656548119 (1.4810119967139241) / 11.223948532129667 (0.9254338233516672) / 8.328110261261065 (0.527909940587626) / 6.514462412402368 (0.40289349071506947) | Clean: only the recorded edge changes, and all 4000 pairs match on every non-edge field. One source did not hold. |
| Arbitrageur skips base orders on jump steps (item-no-jump-loss) | 7.464602365007875 (1.0123114988310487) | 0.12548197081745016 / 7.3391203941951755 | 3.9469318800400583 (2.8730032164619916) / 4.736768314097796 (1.33308470376203) / 10.402776816158703 (2.043570402172372) / 10.878645893093704 (1.3685704575145148) | "Mostly clean", with side effects against the base. A cancel variant gives 11.776567126023199 (SE 1.0360469378961532). Three sources did not hold. |
| Phantom depth at the base's best price for retail while p<0.05 (item-rich-runs) | 6.1430107364775814 (0.35304196679864086) | 6.1430107364775814 / 0.0 | 10.890405256355507 (1.0733858286874989) / 6.081996359305553 (0.5865846879239448) / 3.82928115306932 (0.4386795601474673) / 3.6565324109336315 (0.49520920325999784) | Clean but generous: the phantom size never pays the arbitrageur. |
| Unlimited YES stock and collateral for asks at 5 cents or below (item-unlimited-stock) | 2.6866056031100016 (2.686619389560256), **30 runs only**, seeds 50000-50029 | 1.4797508542466669 / 1.2068547488666668 | 0.0 (0.0, 8 runs) / 0.0 (0.0, 5) / 11.514081128485714 (11.514081128485714, 7) / -3.9980609994927366e-05 (3.998060999492736e-05, 10) | Not shown. The 4000-run check was not completed and the base reference was not reproduced (114.00474655356668 on 30 seeds). Two sources did not hold. |
| Cash never binds (starting cash 1,000,000) (item-unlimited-cash) | 2.022563212233975 (0.22571927384829718) | 1.347462757816975 / 0.675100454419975 | 3.101001309556988 (0.6685558885373565) / 1.821206074168537 (0.37935795336104466) / 1.846252291432252 (0.346600360479387) / 1.2842448668928794 (0.30093888093689947) | Clean: 3321 of 4000 runs are bit-identical. The base's xu rule still binds. |
| Retail foresight: the next retail order is known before quoting (item-retail-foresight) | -4.753894308260601 (0.8121182463231497), 500 runs | -3.2077414973899994 / -1.5461528108862 | -5.892633269170992 (1.994971931944536) / -4.734437326549242 (1.1552528634060448) / -5.215723871564168 (1.9797479044258128) / -3.0271761040743614 (1.1252549330295871) | **Not clean**: the engine override breaks the base's own order bookkeeping. One source did not hold. |
| No arbitrage on no-jump steps, except bids at 5 cents and below (item-no-drift-loss) | -28.3573790154357 (0.8875141718092743) | -23.892162488129298 / -4.46521652731325 | -1.0846146521940945 (2.1757687143676554) / -21.205793930662526 (1.1057742786037525) / -42.181926661469916 (1.5211330385911017) / -49.80923200990454 (1.6850725750615099) | **Not clean**: removing these fills starves the base's fill-based inference. Two sources did not hold. |

Two what-ifs could not be made cleanly: retail-foresight and no-drift-loss. Their negative numbers are not ceilings and close nothing. Unlimited-stock is not established either: its standard error equals its mean, and it rests on 30 runs.

## Ceilings over one point

**Front of queue (47.859869056410425).** Under the published FIFO rule a new order cannot jump an older competitor order. A real strategy can only gain priority by already resting at a tick before the competitor replenishes there; the base already does this through `self.ahead`. The honest priority-only ceiling is 1.9795897512764, not 47.86. Joining at the competitor price under ordinary FIFO costs a great deal: that control measured -118.52891369932563 (SE 2.3307002606258416). The legal retention attempt ("keep3", tuned on seeds 4000-7999, then a single holdout run) measured +0.25266284248429993 (SE 0.10793883644096303). The missed-retail count puts the FIFO-only gross opportunity at 1.336786728499442 per run.

**No competitor (15.654209962010375).** A live strategy wins competitor flow only by quoting a better legal price, acquiring time priority, or supplying more inventory and collateral at a competitive quote. Beating a tick-1 competitor bid means paying tick 2, which erases the edge when p is between 0.01 and 0.02, and it also ties up cash and adds arbitrage risk. The real attempt "front_stock_100" measured 0.017521660387624715 (SE 0.059655014715235634), and the queue-priority control measured 0.0029731102192500193 (SE 0.0019616558127204193). The seat says not to build a simple retention or bid-size change from this ceiling.

**Free stock (10.600204159728674).** A real strategy could avoid low-price replenishment bids when the YES it already holds covers the retail sales it can foresee, and could acquire stock on small crossings below its estimate instead of paying above fair value. Cutting those bids loses profitable retail bid fills and fill information, and less stock means fewer covered asks or nearly $1 of collateral per uncovered YES. The tested cap on cheap bids, set by projected cover demand (horizon 1000, chosen on seeds 4000-4599), lost -7.335753105350152 (SE 0.5921357294213615) on unseen seeds, and all three caps lost on training. The seat says to open the direction as joint stock and collateral valuation, not as a plain inventory cut.

**No jump loss (7.464602365007875).** The seat finds almost none of it realizable: jumps are i.i.d. Poisson draws made after the strategy quotes, so nothing can dodge the jump step itself. Shrinking size at risk trades retail one for one. The jump-charge ×0.5 setting gave -1.5528310372969991 and ×2 gave -0.6446750789249999 on tuning seeds 4000-4999. Per-run jump-rate learning measured -0.13092513432870032 (SE 0.41662564774833855) on unseen seeds. What is left is recovery after a jump, which the skip-vs-cancel gap of about 4.3 bounds. Three of this result's sources did not hold.

**Phantom depth (6.1430107364775814).** The seat says very little of this is realizable: most of it is the base's size rule deliberately trading retail against up-jump arbitrage, and the phantom size never pays that cost. Larger size pays the arbitrageur. The one attempt, qmax 3000 to 6000, measured 0.17881432068125003 (SE 0.07912630296231266) on the holdout, and the seat calls it safe to fold in.

**Unlimited stock (2.6866056031100016, 30 runs).** It could be approximated by buying YES before posting low asks, through the cheap bid bank or a complete-set mint if the venue had one. Either costs cash, collateral and settlement exposure, and the API has no free-stock operation. No attempt was made. The figure is not significant, and two sources did not hold.

**Unlimited cash (2.022563212233975).** A real run can only spend its spare cash sooner. Collecting this needs about 3.7 times the starting cash and earns about 1.2 cents per dollar of collateral. The attempt (Hu 500 to 800, xu 0.10 to 0.05) measured -0.12430093107790009 (SE 0.15238069514380506). The seat says not to build more cash rules.

## What the three counting seats found

- **Edge map (item-edge-map)** is a no-cheat log; its diff is 0.0 over 4000 runs. 103.05 of the base's 126.02 retail edge comes from asks, and 83.32 from asks filled while p<5c (11.9% of steps). It loses 27.74 to the arbitrageur, 14.56 of that on the 3.8 steps per run that contain a jump. In the 5-80c middle the base earns 34.97 retail and pays 12.10. The seat's arithmetic bound of 6.36 for queue priority at p<2c is a sum over the map, not a simulated ceiling. Its attempt measured 0.12006114750162496 (SE 0.17157513684656325).
- **Missed retail (item-missed-retail)** is a frozen-path gross count, not a counterfactual: 67.29920187181038 (SE 0.9882898009129557) per run. The largest category is size_ran_out at 48.75928917839752, and the largest zone is [0.2,0.8) at 29.721029361435146. The tested covered second ask lost -4.741292586289525 (SE 0.21334474576811202).
- **Leaders' path (item-leaders-path)** is the public submissions record (https://www.paradigm.xyz/puzzles/api/v1/prediction-market/submissions); its diff is 0.0. No leader code is public. Compared with IMD, Littoral v16 saves 3.432385 of arbitrage loss and adds 0.606881 retail; KING adds 3.643624 retail with 0.560570 less arbitrage loss. The seat calls these descriptive gaps, not mechanisms. Its cash-reservation attempt measured -0.0022317855786250116 (SE 0.0017917106041472873).

## Next goal: build, in order

1. **Valuing stock and collateral jointly at low probability.** The free-stock ceiling is 10.600204159728674, and 16.15857656548119 at spread 1. The no-competitor result (15.654209962010375) points the same way: the next seat should price a marginal YES by the covered asks it enables later, then choose bid price and size from that value. Plain caps and size bumps already lost.
2. **Recovery after a jump.** This is bounded by the skip-vs-cancel gap of about 4.3 within the no-jump-loss result. Measure first, because three of that result's sources did not hold.
3. **Acquiring queue position without dropping price improvement.** Only priority-only (1.9795897512764) and the retention gain (0.25266284248429993) are real here. Reproduce keep3 and fold it in only if it holds.

**Drop:** dodging jumps, drift buffers (0.06769675810909985, SE 0.06596692953580126), retail foresight, more cash rules, deeper low-price size, and the 5-80c and above-80c zones. Unlimited stock stays unmeasured until a full 4000-run paired rerun exists.
