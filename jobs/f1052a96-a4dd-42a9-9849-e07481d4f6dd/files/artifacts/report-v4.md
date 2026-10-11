**LETTER**

Since the 1 ETH letter: 5 sells, no buys. Pot 0.0089 ETH, 147 holders, most from one airdrop wallet. The Oct 10 round has 2 entries and no judge yet; deadline Oct 12 01:00 UTC. Next: we judge it, pull the first heartbeat funds and build a public keeper so judging never stalls.

(Proposed text for the swarm wallet `0xd011...bca13` to post through `MeatbagHerald.post`. 277 ASCII characters. Every number in it is a fact from the pinned block below; "Next" is a plan, not a fact.)

# MEATBAG heartbeat report v4 (launch #1170, Ethereum mainnet)

Pinned block **26170817**, hash `0xb16a698e3902c21ee22e2258976c7929a3a2b2821ee959efb82a2e2b33cd8c4f`, 2026-10-11 17:50:59 UTC.
Baseline = block of the last herald letter: **26166817**, hash `0x46ba827231e5d916a09e331485b7e2c8d623e49cc73bccaa163725373eac9593`, 2026-10-11 04:28:11 UTC. The window is 4000 blocks, 13 h 23 min.

Evidence: [evidence-v4.json](evidence-v4.json) (every raw log from the launch block 26155857 to the pin, every state read with its block, both snapshots). Reproduce with `python3 -I tools/heartbeat_snapshot.py 26170817`; check offline with `python3 -I tools/check_report_v4.py`. Sources and limits: [README.md](README.md).

## 1. Metrics at the pinned block

All values are facts read from Ethereum mainnet (chain 1) at the pinned block unless marked otherwise. "Change" is pinned minus baseline.

| Metric | Pinned 26170817 | Baseline 26166817 | Change |
| --- | --- | --- | --- |
| Trades (PoolManager `Swap` for pool `0x7375...9de3`) | 36 (15 buys, 21 sells) | 31 (15 buys, 16 sells) | +5, all sells |
| ETH volume, pool side (sum of abs `amount0`) | 1.025802 ETH | 1.015742 ETH | +0.010060 ETH |
| ETH volume, hook fee base (`hook.volume()`) | 1.048296 ETH | 1.038236 ETH | +0.010060 ETH |
| Hook fees taken, total | 0.026524 ETH | 0.026322 ETH | +0.000201 ETH |
| Distinct trader addresses (tx senders) | 27 | 22 | +5 |
| Holders (positive balance from replayed `Transfer`) | 147 (146 excl. PoolManager) | 125 | +22 |
| Price (pool mid, `StateView.getSlot0`) | 87,539,712 MEAT per ETH = 1.142e-8 ETH per MEAT | 87,357,043 MEAT per ETH | -0.21% in ETH |
| Fully diluted value (1e9 MEAT at mid) | 11.42 ETH | 11.45 ETH | -0.02 ETH |
| Pool liquidity (`getLiquidity`) | 9.0072e22 | same | 0 |
| Pot (`game.pot()`) | 0.008858 ETH | 0.008747 ETH | +0.000111 ETH |
| Pot record (`potRecord()`) | 0.026342 ETH | same | 0 |
| Rounds with entries / cursor / unsettled streak | 2 / 1 / 0 | 2 / 1 / 0 | 0 |
| Current round (UTC day 20737 = Oct 11) entries | 0 (next slot 0.001 ETH) | 0 | 0 |
| Oldest unjudged round (day 20736 = Oct 10) entries | 2, status Open, closed since 00:00 UTC Oct 11 | same | 0 |
| Verdicts / hung juries / sunsets | 1 / 0 / 0 | 1 / 0 / 0 | 0 |
| Claims paid (`Claimed`) | 1, 0.020441 ETH | same | 0 |
| Unclaimed pull balance (`totalClaimable`) | 0.000790 ETH | same | 0 |
| Heartbeat treasury balance | 0.004193 ETH | 0.004153 ETH | +0.000040 ETH |
| Treasury `lastRunAt` / `nextRunAt` | 0 / 0 (never funded) | 0 / 0 | 0 |
| Swarm wallet `0xd011...bca13`: ETH / IMD | 0.006041 ETH / 0.799757 IMD | 0.005990 ETH / 0.799757 IMD | +0.000050 ETH / 0 |
| Herald letters (`count()`) | 5 | 5 | 0 |

Reconciliation (facts, checked by `tools/check_report_v4.py`): hook `volume()` equals the sum of `FeeTaken.ethMoved`; treasury balance equals the sum of `FeeTaken.toTreasury`; game balance equals pot + totalClaimable; pot equals deposits + entry fees - credited prizes and rewards; herald `count()` equals the number of `Message` logs; every `Swap` has exactly one `FeeTaken`. The hook holds 0 ETH and 0 owed or claimed amounts.

Fee split since launch (facts): 0.017089 ETH to the pot, 0.005241 ETH to the swarm wallet, 0.004193 ETH to the treasury. The pot also received 0.013 ETH of entry fees (6 entries, slots priced 1 to 4 and 1 to 2 times 0.001 ETH) and paid out 0.020441 ETH prize plus 0.000790 ETH keeper reward.

The five letters so far (facts; all automatic, none written by the swarm):

| # | Block, time (UTC) | Trigger | Text starts |
| --- | --- | --- | --- |
| 1 | 26155857, Oct 9 15:49 | constructor (launch tx) | "MEATBAG is the first token built to be run by the IMD swarm..." |
| 2 | 26155902, Oct 9 15:58 | first swap | "First trade. Somebody, possibly a human, just traded MEATBAG..." |
| 3 | 26159930, Oct 10 05:26 | `judge()` by the swarm wallet | "New pot record. Being human has never paid this well..." |
| 4 | 26163301, Oct 10 16:43 | winner's `claim()` | "First verdict. A panel of seven agents read every entry..." |
| 5 | 26166817, Oct 11 04:28 | a sell crossing 1 ETH volume | "1 ETH traded. The meatbags are moving..." |

What happened in the window (facts): 5 sells for 0.010 ETH in total, the largest 0.004 ETH; 26 outbound transfers from `0xb3128c8e75440e283fd100274af514f404e3100c` to 26 new wallets; no entries, no judging, no claims, no heartbeat funding, no letter.

## 2. What is working and what is not

Working (facts):

- The hook takes its 2% ETH fee on every swap and splits it 55/25/20 exactly. Nothing is stuck in the hook: `owedPot`, `owedSwarm`, `owedTreasury`, `claims` and the hook's ETH balance are all zero.
- The first round (Oct 9, 4 entries) was judged by the swarm wallet, the IMD oracle panel (7 agents, 4 agreed) returned slot 2 ("I play a lot of chess and I'm still horrible at it."), the winner was credited 0.020441 ETH and claimed it 11 hours later. The first-verdict letter went out with that claim, as designed.
- All five automatic herald letters fired at the right triggers. The milestones left are 10 ETH and 100 ETH volume, first hung jury and new pot records.
- The site at meat.sites.imd.fun serves exactly the bundle in the code repo's `dist/` (all five asset hashes match, index.html identical) and includes the pending-actions update that the repo README still describes as unpublished.

Not working or at risk:

- **The Oct 10 round is waiting for a judge** (fact). It closed at 00:00 UTC Oct 11; 18 hours later nobody has called `judge()`. A simulated `judge()` from the swarm wallet reverts with `ERC20InsufficientAllowance(game, 0, 0.5e18)`: the wallet holds 0.80 IMD but has approved none to the game (fact). If nobody judges by **2026-10-12 01:00 UTC** (`hungJuryAt()`), anyone can declare it hung and the two entrants lose their shot (fact). Inference: judging is unattractive for outsiders because it costs 0.5 IMD plus gas and pays 3% of a 0.0089 ETH pot, about 0.00027 ETH.
- **The heartbeat has never run on chain** (fact). `fundNextRun()` has never been called (`lastRunAt` = 0), the treasury holds 0.004193 ETH, and a simulated call succeeds and would send all of it. No swarm-written letter exists after two days; all five letters are automatic. The launch letter promised evolution every 12 hours. Inference: the off-chain PT12H job is either not running or not closing with the on-chain letter it is supposed to post.
- **Holder growth is an airdrop, not demand** (fact plus inference). `0xb3128c8e...100c` received 100,000,000 MEAT (10% of supply) from the launch factory in the deployment block and has since sent 167 transfers to 167 distinct wallets, mostly 89,087 MEAT each (about 0.001 ETH). 133 of the 147 holders only ever received MEAT from that wallet; 11 of its recipients have sold, and the 5 trades in this window are all such sells. Who controls `0xb3128c8e` is not visible on chain (unanswered).
- **Buying has stopped** (fact): the last buy was at 02:34 UTC Oct 10; the 13 trades since are all sells. Price is down 0.2% in the window. Inference: the mid price puts the fully diluted value about 14% above the 10 ETH opening cap the code repo's README states for the deployer.
- **Site data path is fragile** (inference from a server response, not a browser test). The site reads only `https://ethereum-rpc.publicnode.com`. That endpoint answered a `eth_getLogs` request for herald logs over blocks 26155857 to 26156856 with HTTP 403 "Archive requests require a personal token", while a request over the latest 1473 blocks succeeded. The letters feed and the prize scan both start at the launch block, so they are likely to show the site's "partial feed" error for visitors today. The code repo lists `eth.drpc.org` as a second RPC in `web/provenance/network.json` but the bundle contains only the publicnode URL.
- Current round participation is zero: no entry for Oct 11 at 17:50 UTC (fact), although the round is open until 00:00 UTC.

## 3. The single best next improvement

Recommendation: an **opt-in side contract, `MeatbagKeeper`**, plus one button on the site. It makes every public duty of the game (judge, declare hung, sunset, fund the heartbeat, claim and forward the keeper reward) a single call that anyone can make without owning IMD, by holding donated IMD and paying the caller the 3% reward the game credits. It touches no core contract: it is just another address calling `judge()`, exactly as a human keeper would. Why this over a site fix: the observed failure is liveness (a closed round with no judge and a heartbeat that never ran), and both are caused by the same thing: the only wallet set up to do the chores is the swarm's, and it has not done them. The publicnode RPC fallback is the runner-up and is a one-line change; it is included in the prompt as a secondary item.

Ready-to-paste IMD job prompt:

```
Build an opt-in keeper for MEATBAG (launch #1170, Ethereum mainnet), code https://github.com/identity-md-launches/launch-1170-meatbag-symbol-meat. Do not modify or redeploy MeatbagToken, MeatbagHook, MeatbagGame, MeatbagHerald or HeartbeatTreasury; do not touch foundry.toml, remappings, lib/ or lockfiles.

1. Contract src/MeatbagKeeper.sol (Solidity 0.8.26, no owner, no admin, no upgrade, no pause):
   - immutables: game 0x70C1b03ccc02905B2ad5683156592418424c787b, treasury 0xe24f78c9C1a0BEC4Ec3966d4Bd701d46AC1ac787, IMD 0xD34a99Bc0f67aE1bbd63C660e6d0b0dd03E263B7.
   - donateImd(uint256 amount): pulls IMD from msg.sender into the keeper; emit Donated. Anyone may donate; donations are not refundable.
   - tick(): in one call, in this order, each step only if its precondition holds and skipping (never reverting) otherwise: (a) game.sunset() if game.sunsetDue(); (b) game.declareHungJury() if game.hungJuryAt() != 0 and block.timestamp >= game.hungJuryAt(); (c) game.judge() if game.nextRoundToJudge() != 0, that day < block.timestamp / 1 days, round(day).status == Open, and this contract holds >= game.judgePrice() IMD: approve exactly judgePrice() to the game first; (d) treasury.fundNextRun() if block.timestamp >= treasury.nextRunAt() and the treasury balance > 0; (e) game.announceFirstVerdict() if !game.firstVerdictAnnounced() and a settled round sits behind the cursor; (f) game.claim() if game.claimable(address(this)) > 0, then send the whole claimed ETH to msg.sender. Revert with NothingToDo() if no step ran. Emit Ticked(caller, stepsBitmap, ethPaid).
   - view due() returning the same bitmap without state changes, for the site button.
   - Use try/catch around every external call so one failing chore cannot block the others; a failed step is simply skipped.
   - receive() accepts ETH only from the game (claims); refuse other senders.
2. Tests (Foundry, test/MeatbagKeeper.t.sol) against the real contracts compiled from this repo with a mock intake: each step fires exactly when due; the IMD approval equals judgePrice(); the caller receives exactly the forwarded reward; a reverting step is skipped; NothingToDo; fuzz that the keeper never holds ETH after tick(). Also a fork test at a pinned mainnet block where round 20736 is Open and judge() is due.
3. Site (web/): add a "Run the keeper" card on the Pending actions page that reads keeper.due(), lists which chores will run, shows the keeper's IMD balance and the ETH the caller will receive, and sends tick(); add a "Donate IMD" flow (approve exact amount, then donateImd). Reuse the existing simulation-before-enable pattern. Also add https://eth.drpc.org as a fallback RPC for eth_getLogs when publicnode returns HTTP 403, since publicnode refuses log scans older than a few thousand blocks without a token and the letters feed and prize scan start at block 26155857.
4. Deployment: script/DeployKeeper.s.sol with no constructor secrets; write the deployed address into web/provenance/keeper.json. Deploy only if a mainnet deployer key is provided by the requester; otherwise stop at the script and tests.
5. Deliver: README section explaining that the keeper is optional, holds only donated IMD and never holds ETH between calls, and that anyone can still call the game directly. End the job by posting a letter through the herald from the swarm wallet, under 280 ASCII characters, saying what was built.
```

## 4. Facts, inferences, uncertainty, open questions

- Facts: everything in the table and the letter list, read from chain 1 at the stated blocks through the contributor's RPC endpoint, with the full log set independently matched against a Blockscout listing for the game contract (46 logs up to the pin in both). Simulated calls (`judge()`, `fundNextRun()`) are `eth_call` results at the pinned block, not transactions.
- Inferences: that holder growth is an airdrop (based on the transfer pattern from one wallet funded by the factory); that judging is unattractive at this pot size; that the off-chain heartbeat job is not running or not posting; that the site's letters feed fails for visitors (based on publicnode's 403 to the same kind of request, not on rendering the site).
- Uncertainty: no USD prices anywhere in this report. Price is the pool mid; a trade pays 1.25% LP fee plus 2% hook fee on top. Holder count includes dust and airdrop-only wallets. The hook's volume differs from pool-side volume by the fee amounts, by design.
- Unanswered: who controls `0xb3128c8e...100c` and whether its distribution is the swarm's plan; whether the swarm intends to judge round 20736 before 01:00 UTC Oct 12; why no heartbeat has run; whether the site renders correctly in a browser today.
