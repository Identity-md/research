# Audit report

> go over the v6 folder

| | |
|---|---|
| Repository | https://github.com/DrTatum/MSFT95.git |
| Commit | `be86888e520165819ae09a4ae3e27f8473154b04` |
| Job | `7736b1b9-14c6-4b78-b72c-878233fad702` |
| Judged | 2026-10-24 15:09 UTC |
| Findings | 5 low · 4 info |

Four agents audited the code as it is at `be86888`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Low: Agent farm: OPEN-pool daily caps (cap0/cap1) still reset at UTC midnight, so 2x cap can be sold through the feed-less pool within seconds

`msft95-contracts-audit-v6/v4/MSFT95AgentFarm.sol:648`

```
        if (p.day != today) { p.day = today; p.used0 = 0; p.used1 = 0; }
```

Audit 7 I-2 moved the per-agent turnover window (_useTurnover, line 436) and the per-agent swap count (_swapDay, line 330) to a rolling 24 hours because a calendar-day reset let a keeper fit two days' budget into a few seconds. The third limit checked by swap(), the pool-wide cap0/cap1 that _useCap enforces for OPEN pools, was left keyed on block.timestamp / 1 days (lines 647-648), so used0/used1 are zeroed at 00:00:00 UTC whatever was spent at 23:59:59. OPEN pools are the ones with no feed and no floor (the MSFT95/USDG pool: deploy-farm.js sizes its cap at M95_DAY_CAP), where the only protections on a keeper swap are the keeper's own minOut (minOut = 1 passes the BadConfig check) and this cap. The per-agent turnover does not help because the cap is shared across all agents and a keeper spreads sales over many of them. The farm NatSpec (line 69) names cap0/cap1 as the bound to 'keep small', and the README's v6 bullet and MAINNET.md present the farm's limits as no longer resetting at midnight, but the aggregate bound is really 2x cap in any 24-hour span, with the two halves in adjacent blocks. Reported independently by four specialists (economics, permissions, math, flow); merged here. Fix: give Pool a window start (reset used0/used1 when block.timestamp >= start + 1 days, exactly as _useTurnover does) and update the NatSpec at line 114; or document cap0/cap1 as 'up to 2x per 24h' and halve the configured value.

**Reproduction**

Hardhat test run against this code (test-v4 harness: PoolManager, V4TestToken USDG 6 dec / MSFT95 18 dec, FarmMockAgents, farm delay 0). State: MSFT95/USDG v4 pool listed OPEN; setGuard(idx, true, 0, 0, 0, 0, cap on the USDG side = 1000e6, 1e30 on the other); agents 1 and 2 each deposited 2000e6 USDG; keeper has KEEPER_ROLE. Input: evm_setNextBlockTimestamp(midnightUTC - 3); swap(1, idx, usdIs0, 1000e6, 1) succeeds (used = cap). evm_setNextBlockTimestamp(midnightUTC - 2); swap(2, idx, usdIs0, 1e6, 1) reverts OverCap (cap holds within the day). evm_setNextBlockTimestamp(midnightUTC); swap(2, idx, usdIs0, 1000e6, 1). Expected under the rolling-window rule the rest of swap() follows: revert OverCap until midnightUTC - 3 + 86400. Actual: the call succeeds; pool(idx).used0/used1 reads 1000e6 again, agent 1 and agent 2 each hold 1000e6 USDG less, i.e. 2000e6 USDG (2x cap) was sold through the OPEN pool at minOut = 1 across one second. The existing suites never cross a day boundary on _useCap: farm.test.js 172-184 checks the cap inside one day and the midnight tests (farm.attack.test.js 85-88) cover only the per-agent turnover.

### 2. Low: Agent farm: setTreasury changes protocolBps with no delay, and _credit applies the new cut to fees earned under the old rate

`msft95-contracts-audit-v6/v4/MSFT95AgentFarm.sol:413`

```
        treasury = t; protocolBps = bps;
```

The farm NatSpec (lines 70-72) says a re-tuned pool 'only becomes usable after delay, so holders see it coming and can freeze the keeper for their agent or leave'. setGuard and listV3/listV4 honour that through usableAt; setTreasury does not: the new treasury and protocolBps take effect in the same transaction. Fees are distributed into per-liquidity accumulators by _distribute at collection time but the protocol's cut is only computed in _credit (line 476, f0 * protocolBps / 10000) when the agent's fees are credited, lazily on add/remove/claimFees. Raising the cut (up to MAX_PROTOCOL_BPS = 20%) therefore reaches fees that were earned while a lower rate was advertised and are merely uncredited, which is the normal state between claims. The holder's only tool, setFrozen, does not prevent _credit from running when they later exit (holderRemove calls _credit), and there is no event ahead of the change to act on. The admin role is a trust assumption; the defect is that this one fee-affecting parameter skips the notice period the design promises. Impact is bounded to 20% of uncredited fees per agent. Reported by economics and permissions specialists; merged. Fix preserving the admin's power: queue the change (pendingBps/pendingTreasury, effectiveAt = now + delay) and apply it only after delay, or take the cut inside _distribute at collection time so a later change cannot touch fees already collected.

**Reproduction**

Hardhat test run against this code. State: farm deployed with protocolBps 500 (5%), delay 0 (the value does not matter: no delay path exists for setTreasury); agent 1 enters the AAPL/USDG ORACLE pool with $10,000; an outside trader churns the pool 4 times each way so the position earns fees; nothing has been credited. Measured by snapshot: claimFees(1, idx) at the advertised 5% credits USDG 179650 / AAPL 718609027594033 to the agent and USDG 9455 / AAPL 37821527768106 to treasuryOwed. Revert the snapshot. Input: admin calls setTreasury(treasury, 2000) then keeper calls claimFees(1, idx). Expected (per the stated design): the new rate cannot apply before delay, so the holder can claim at 5% first, and fees earned at 5% are credited at 5%. Actual: the same fee total (189105 USDG units) is split 151284 to the agent and 37821 to treasuryOwed, i.e. 20% is taken out of fees earned at 5%, in the very next block after the change, and pool(idx).usableAt is unchanged (no delay started).

### 3. Low: Agents NFT: the owner can repoint all three payees at itself at once via setPayees, taking 100% of mint proceeds despite the NatSpec 'nobody can take more than their share'

`msft95-contracts-audit-v6/contracts/MSFT95Agents.sol:156`

```
        if (vault_.code.length == 0 || team_ == address(0) || lp_ == address(0)) revert BadPayee();
```

The contract NatSpec (lines 17-19) states that 'Mint money follows the tokenomics and nobody can take more than their share: distribute() ... sends 70% into the casino vault's house bankroll, 10% to the team wallet and 20% to the liquidity wallet'. setPayees (line 153) has no delay and _setPayees only checks that vault_ has code and that team_ and lp_ are non-zero. It does not check that vault_ is the MSFT95Vault or that it credits a bankroll, and the three payees may be the same address. The owner (the Safe after handover, the deployer before it) can therefore point all three legs at addresses it controls and call distribute() (anyone may). This is an owner trust assumption, not a permission bypass, but the written guarantee is false as the code stands and players are told the 70% backs the casino bankroll. Fix options that keep the role: make casinoVault immutable or changeable only behind a delay with an event; require that vault_ has granted this contract BANKROLL_ROLE (IAccessControl(vault_).hasRole); or correct the NatSpec to say the owner can redirect proceeds.

**Reproduction**

Hardhat test run against this code (0.8.24 build). State: MSFT95Agents deployed with saleOpen = true, prices 0.1/0.05/0.02 ETH, casinoVault = a contract with a payable fundBankroll (stand-in for the vault), team and lp = separate EOAs; a buyer mints 10 Executive agents, so address(agents).balance = 1 ETH. Input: the owner deploys Sink { function fundBankroll(address,uint256) external payable {} function pull(address to) external { payable(to).transfer(address(this).balance); } } and calls setPayees(address(sink), owner, owner); the buyer calls distribute(); anyone calls sink.pull(owner). Expected per the NatSpec: setPayees rejects a payee set that does not pay 70% into the vault's bankroll (or the change waits behind a delay), and the vault receives 0.7 ETH. Actual: setPayees succeeds (sink has code, owner is non-zero), distribute() sends 0.7 ETH to the sink and 0.3 ETH to the owner, the original vault receives 0, and after pull the owner holds the full 1 ETH.

### 4. Low: MSFT95Token: 'never a wallet' exclusion rule relies on code.length, so the owner can exclude Safe/contract wallets and the staking contract from dividends

`msft95-contracts-audit-v6/v4/MSFT95Token.sol:128`

```
            if (account.code.length == 0) revert NotAContract(account);
```

The NatSpec (lines 14-17) promises that 'the owner can also exclude other contracts (a router, a presale) but never a wallet', and that the staking contract and the games vault 'stay eligible'. The only check in setExcluded is account.code.length != 0. Safe multisigs (including the project's own TREASURY/OPS Safes and any holder's Safe), ERC-4337 smart accounts and, on chains with Pectra, EOAs carrying an EIP-7702 delegation all have code, so the owner can stop any of them from earning future MSFT dividends; their share is then re-shared across the remaining eligible holders, the owner's own holdings included. Nothing stops excluding MSFT95Staking or the vault either, which cuts stakers off from the staked MSFT95's MSFT. What was already earned stays claimable (credit[]), so the loss covers future distributions only. This is an owner trust assumption, documented here because the NatSpec states a guarantee the code does not enforce. Fix: pin the excludable set at deployment (or an owner allowlist additions to which wait behind a delay), explicitly refuse the staking contract and vault, or reword the NatSpec to the real rule ('any address with code').

**Reproduction**

Hardhat test run against this code. State: MSFT95Token with 1,000,000,000 supply minted to the owner; 10,000,000 MSFT95 transferred to a contract-wallet stand-in (any address with code; a Safe behaves the same), 490,000,000 to Alice; eligibleSupply = 1e9 tokens. Input: owner calls setExcluded(contractWallet, true), then anyone calls distribute(1000 MSFT). Expected per the NatSpec ('never a wallet'): setExcluded reverts NotAContract for a wallet and the contract wallet earns 1000 * 10M / 1e9 = 10 MSFT, Alice 490 MSFT. Actual: setExcluded succeeds, excluded[contractWallet] = true, eligibleSupply drops to 990,000,000; after the distribution claimable(contractWallet) = 0 and claimable(alice) = 494.95 MSFT (the excluded wallet's share re-shared). Then setExcluded(MSFT95Staking, true) also succeeds and excluded[staking] = true, so stakers stop receiving MSFT from the staked supply.

### 5. Low: Launch split: the economy part's re-sign path first sends a fresh approve from the deployer, so a same-nonce re-sign either hangs or can never be mined

`msft95-contracts-audit-v6/scripts/mainnet/lib.js:349`

```
      await once("economy", async () => { await send(m.approve(A().vault, parts.economy[1])); return V.fundBankroll.populateTransaction(A().msft95, parts.economy[1]); });
```

once() handles a recorded transfer that has no receipt by calling build() and then signAndSend(key, req, s.nonce, true) (line 333): it re-signs the SAME nonce with higher fees so only one copy can ever land. For 'treasury' and 'liquidity' build() is a pure populateTransaction (line 348), so this works, and rehearse.js section 10 c exercises it only on 'liquidity' (faults.crash = 'liquidity:unsendable'). For 'economy' build() first runs send(m.approve(...)): a real transaction from the deployer account through the hardhat signer, with an automatically chosen (pending) nonce, awaited with tx.wait() (line 107) and no timeout. Both possible states of a stuck fundBankroll at nonce N break the same-nonce design. (1) N is still pending but underpriced: the approve takes nonce N+1 and wait() blocks until N is mined, which is exactly what is not happening; the launch hangs inside build() before reaching the re-sign, with no message, and re-running repeats the hang. (2) N was dropped by the node: the approve is mined as nonce N; signAndSend then signs fundBankroll with nonce N, broadcast fails ('nonce too low', only logged at line 315), receiptOf finds nothing and the run throws 'isn't mined yet: run again' (line 345); the next run sees used (N+1) > s.nonce and stops with 'no receipt ... although the deployer's nonce N is used' (line 329), and the explorer shows nonce N was the script's own approve, so the operator has to work out that the economy part was never paid and delete split.economy by hand. No double payment occurs in either state, but the resume that audit 7 M-1 introduced does not work for the first and largest part (250,032,300 MSFT95 to the vault's bankroll). The approve is also unnecessary on the re-sign path: the allowance set before the original fundBankroll is still in place because fundBankroll never executed. Fix: on the re-sign path do not send anything inside build(): check allowance first and approve only when allowance < amount, give that approve an explicit recorded nonce like the parts themselves, or make the approve its own recorded part before 'economy'.

**Reproduction**

Code trace (script, no chain state needed). State: deployments/<network>Launch.json has steps.vault done and split.economy = {hash: H, nonce: N, raw: R} where R was broadcast with a maxFeePerGas below what the chain now needs (or the node dropped it); the deployer's latest nonce == N. Run launch.js (resume). Expected (per the comments at lines 277-286, MAINNET.md section 3 and AUDIT-7 M-1): the economy transfer is re-signed with nonce N and higher fees and pays once. Actual path: once('economy') -> receiptOf -> null -> rebroadcast R (line 323) -> still no receipt -> used (N) > N is false -> line 333 evaluates build() -> line 349 runs send(m.approve(vault, 250032300e18)) = (await tx).wait() with the signer's pending nonce. If R is still pending in the node: the approve queues at nonce N+1 and wait() never returns; the launch hangs with no message. If R was dropped: the approve mines as nonce N; the fundBankroll re-signed with nonce N is rejected by every node; the run ends with 'economy: ... isn't mined yet: run again'; the next run ends with 'no receipt for H, ... although the deployer's nonce N is used', and the vault's bankroll stays unpaid until the operator deletes split.economy by hand. Compare rehearse.js lines 260-263, where the identical fault on 'liquidity' passes because that build() sends nothing; no rehearsal check faults 'economy'.

### 6. Info: Agent farm NatSpec understates the keeper loss bound: 2x turnover fits inside any 24h at a window edge, and per-token windows allow four stock legs per window

`msft95-contracts-audit-v6/v4/MSFT95AgentFarm.sol:65`

```
///     A round trip USDG -> stock -> USDG costs at most about 2 x the stock pool's slipBps of the agent's cash per 24
```

Two claims in the keeper-loss documentation (which the README asks reviewers to check: 'whether anything still compounds across windows faster than the documented bound') do not hold. (1) 'within any 24 hours ... at most what the agent held' (line 60): the window opens at the first swap and resets 86400 s later, so used can reach base in the last second of window 1 and again in the first second of window 2; any 24h span straddling the boundary sees 2x base per token and 16 swaps, the same 2x the vault NatSpec documents for dailyCap (MSFT95Vault.sol line 26) but omitted here. (2) 'A round trip USDG -> stock -> USDG costs at most about 2 x the stock pool's slipBps ... USDG -> USDC -> stock -> USDC is 2 x stock slip + 1 x peg slip': turnover is tracked per (agent, input token) and the base of each token's window is read when that token is first sold, including what just arrived from a previous leg. With two listed dollar tokens and stock pools quoted in each, the path USDG -> S1 -> USDC -> S2 -> USDG uses each input token once and crosses four stock pools: about 4 x stock slip per window (about 6% at slipBps 150 instead of the stated about 3%), and about 12% in a two-second span at a window edge, each leg taken by a keeper that is also the counterparty. No code change is strictly required; the bound should be stated correctly so operators size slipBps and agents size their deposits against the real number, or the window should cap total swapped value per agent per rolling 24h across tokens. Documentation-only, so informational.

**Reproduction**

Hardhat test run against this code (two tokens suffice to show the per-token accounting). State: ORACLE AAPL/USDG pool, slipBps 150, fresh feed at $250; agent 1 holds 1000e6 USDG and 10e18 AAPL. Input, in one block: swap(1, idx, sell USDG, 1000e6, 0) then swap(1, idx, sell AAPL, <entire AAPL balance including what the first leg returned>, 0). Expected from the NatSpec: one turnover of 'what the agent held' per 24h. Actual: both legs pass _useTurnover; turnover(1, USDG) = used 1000000000 / base 1000000000 and turnover(1, AAPL) = used 13987748549259055285 / base 13987748549259055285, i.e. the AAPL leg's base includes the USDG just converted, so the same dollars cross a stock pool twice in one window (two legs, 2 x slip) and, with a second dollar token and a second stock, four times. Arithmetic for the 4-leg path at slipBps 150: 1000 x 0.985^4 = 941 USDG (5.9% per window); repeating at window.start + 86400 gives about 11.5% inside one 24-hour span.

### 7. Info: Agent farm: _credit withholds 1 wei per token but advances the agent's debt to the full share, so owed[token] drifts up and the wei is unclaimable and unskimmable

`msft95-contracts-audit-v6/v4/MSFT95AgentFarm.sol:470`

```
        if (f0 > 0) f0 -= 1;
        if (f1 > 0) f1 -= 1;
```

_distribute adds the full collected fee to owed[token] and grows acc by mulDiv(f, Q128, liquidity) (floor). _credit then credits the agent floor(s*acc/Q128) - debt minus a further 1 wei, but sets debt to the un-reduced floor(s*acc/Q128) (lines 473-474). The subtracted wei is neither credited to the agent nor to treasuryOwed nor to any later credit; it stays counted in owed[token], which skim() treats as agents' money (line 279). The guard is also unnecessary for its stated purpose ('per-agent rounding can never add up to more than the pool actually paid'): with both roundings already floors, the sum over agents of floor(s_i*acc/Q128) <= floor(L*acc/Q128) <= f. The effect is that owed[token] exceeds sum(balanceOf) + treasuryOwed + sum(pendingFees) by one wei per credit with non-zero pending fees, per token, forever; after every agent has left, that residue can never leave the farm because skim computes bal - owed. Amounts are dust (1e-6 USDG per credit) and do not compound, so informational. farm.test.js only asserts balanceOf(farm) >= owed (its solvent() helper), which this drift satisfies. Reported by economics and math specialists; merged. Fix: delete the two -= 1 lines, or add the withheld wei to treasuryOwed[token] so owed stays claimable, or set debt to the reduced value so the wei stays pending.

**Reproduction**

Hardhat test run against this code. State: farm with protocolBps 0; agent 1 is the only liquidity holder in the AAPL/USDG v4 pool; fees have been collected into the accumulators by a claim for agent 2 (which holds nothing), so pendingFees(1, idx) = USDG 94553 / AAPL 378215277681070 and nothing new is collected on the next call. Input: keeper calls claimFees(1, idx). Expected: the agent is credited 94553 / 378215277681070 (or the remainder goes to the treasury) and owed[token] stays equal to what is claimable. Actual: balanceOf(1) grows by 94552 / 378215277681069, pendingFees(1, idx) becomes 0 / 0, treasuryOwed stays 0, and owed[USDG] is unchanged, so 1 wei of each token is now counted as owed to nobody. The holder then calls holderRemove(1, idx, all shares) and withdraw(1, token, max) for both tokens: the farm still holds 3 USDG units, owed[USDG] says 3, no agent has a balance or pending fees, and skim.staticCall(USDG) returns 0 (bal - owed = 0). The 3 units can never leave the contract; every further credit strands another.

### 8. Info: Agent farm: the ORACLE swap floor truncates to zero for dust amountIn, so the slipBps guarantee lapses and a swap may return nothing

`msft95-contracts-audit-v6/v4/MSFT95AgentFarm.sol:338`

```
            floor_ = _fairOut(p, zeroForOne, amountIn) * (10000 - p.slipBps) / 10000;
```

_fairOut for a sale of the stock side computes mulDiv(amountIn, f * 10**dOut, 1e18 * 10**dIn) (line 638). With an 18-decimal stock, a 6-decimal dollar token and a feed price f the result is amountIn * f / 1e30, which rounds to 0 for every amountIn below 1e30 / f (4e9 wei of stock at $250, about $1e-6). The floor then becomes 0, and because minOut = 0 is accepted on ORACLE pools (only OPEN pools require minOut > 0, line 343), the check out < floor_ can never trigger, so the swap may complete with out = 0. The NatSpec promise that 'every swap must return at least the feed's value less slipBps' (line 57) therefore holds only above the truncation threshold. The value at stake per swap is below $1e-6 and the keeper's swap count is capped at 8 per rolling day per agent, so the economic impact is negligible; recorded as a precision boundary where the stated invariant lapses. Fix: compute the floor with FullMath.mulDivRoundingUp, and/or revert when floor_ == 0 on ORACLE and PEG pools unless minOut > 0.

**Reproduction**

Hardhat test run against this code. State: ORACLE AAPL(18 dec)/USDG(6 dec) v4 pool, fresh FarmMockFeed at 250e8 with 8 decimals (f = 250e18), slipBps 150; agent 1 holds 1e9 wei of AAPL. Input: keeper calls swap(1, idx, sellAAPL, 1_000_000_000, 0). Arithmetic: _fairOut = mulDiv(1e9, 250e18 * 1e6, 1e18 * 1e18) = floor(2.5e35 / 1e36) = 0; floor_ = 0 * 9850 / 10000 = 0; minOut 0 leaves floor_ = 0. Expected: the swap returns at least 0.985 x fair value (0.246 USDG units, i.e. at least 1 unit with round-up) or reverts TooLittle. Actual: the call succeeds, the agent's USDG balance grows by 0 and its AAPL balance is reduced: the swap returned nothing and no TooLittle was raised.

### 9. Info: Reward hook: _fee rounds down in the swapper's favour and is zero for USDG legs below 34 units

`msft95-contracts-audit-v6/v4/MSFT95RewardHook.sol:147`

```
        return gross ? amount * b / 10_000 : amount * b / (10_000 - b);
```

Both branches of _fee truncate toward the swapper, so the protocol fee is below the nominal 3% of gross USDG by up to one unit per swap, and a swap whose USDG leg is below 34 units (6-decimal USDG: $0.000034) pays no fee at all (fee == 0 returns ZERO_DELTA at line 160 and 0 at line 186). The fee is not compoundable and gas on Robinhood Chain far exceeds the 1-unit saving, so there is no profitable farming path; recorded because fees are conventionally rounded in the protocol's favour and rewards.distribute ultimately pays this USDG to MSFT95 holders. Fix: Math.mulDiv(amount, b, 10_000, Math.Rounding.Ceil) and Math.mulDiv(amount, b, 10_000 - b, Math.Rounding.Ceil), or accept and document that fees round in the swapper's favour.

**Reproduction**

Arithmetic on the code as written with feeBps = 300. Input: a sell of exact MSFT95 that moves 33 USDG units out of the pool (afterSwap, USDG not the specified currency, amountSpecified < 0): _fee(33, true) = 33 * 300 / 10000 = 0, so the hook returns 0 and the swapper keeps all 33 units; expected under round-up: 1 unit to the hook. Input: an exact-output buy where the pool takes 9701 USDG units: _fee(9701, false) = 9701 * 300 / 9700 = 300 (exact value 300.03); the swapper pays 10001 units of which the hook keeps 300, i.e. 2.9997% instead of 3%.

---

Judge's submission `6760a00ab9fe18e017ad303ea75fc7b4eeb04007209c26c381a99aaf57902b57`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
