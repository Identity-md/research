# Audit report

> Audit only the msft95-contracts-audit-v5/ folder. These are MSFT95’s Robinhood Chain mainnet contracts after six automated review rounds; docs/AUDIT-6.md lists the latest fixes. Look hardest at:
> (1) scripts/mainnet/lib.js split, which records transfers by transaction hash. Find any stop-and-resume point where a part is paid twice or skipped, including when wallets are shared or kept by the deployer. Also check the vesting replacement and how much it carries over.
> (2) The overflow guard in MSFT95Staking.sync. Can sync or _accrue still overflow, or can the guard be used to hold back a legitimate reward?
> (3) The full-fill check in MSFT95RewardHook.afterSwap, for exact-in and exact-out swaps in both token orders. Can it refuse a legitimate full fill?
> (4) MSFT95AgentFarm.skim. Can it ever take tokens owed to agents or the treasury, including during callbacks, fee collection or removals?
> (5) The farm’s daily turnover limit (_useTurnover). Can the keeper get around it, or can it block a holder’s exit?
> (6) Re-check earlier fixes: the openTrading position gate, the vault’s separate house sweep window, MSFT being sweep-only in the vault, and that a compromised keeper can only cause bounded loss.
> Give concrete reproductions, and don’t modify or deploy anything.

| | |
|---|---|
| Repository | https://github.com/DrTatum/MSFT95.git |
| Commit | `10a7936a0778f4ed02bdfac99dda165e2d9c83f7` |
| Job | `2c8d4004-f484-4fd9-a842-f81f56f738eb` |
| Judged | 2026-10-24 14:02 UTC |
| Findings | 1 medium · 3 info |

Four agents audited the code as it is at `10a7936`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Medium: split(): a part's tx hash is saved only after the broadcast call returns, so a lost RPC answer or a lagging RPC node makes the resume pay the same part again with a new nonce (merges 4 specialist repo

`msft95-contracts-audit-v5/scripts/mainnet/lib.js:278`

```
        const tx = await fn();
        sent[key] = tx.hash; save();
```

AUDIT-6 M-1 says each split transfer is recorded by its hash 'the moment it is sent', so that 'nothing is paid twice'. In once(), the hash is written (line 279) only after fn() has resolved, which means after eth_sendRawTransaction has answered. Nothing is saved before the signed transaction leaves the key: no hash, no nonce, no raw tx. Two resume paths therefore pay a part again. (a) The node accepts the transaction but the call throws or never returns (RPC timeout or 5xx, connection reset, Ctrl-C or kill while it hangs). sent[key] stays empty, and the next run builds a new transfer. (b) The hash was saved, but on resume getTransactionReceipt(h) and getTransaction(h) both return null, for example on a load-balanced RPC whose node hasn't indexed the transaction yet. Lines 274-276 then log 'was dropped: sending again'. In both cases the new transaction gets the next nonce, so the first one can't stop it and both are mined. The post-split check (lines 289-290) runs only after the tokens have left. Also unverified: hardhat-ethers v3's sendTransaction keeps polling getTransaction(hash) until the node returns the transaction, and only then returns. That would make window (a) longer than a single RPC round trip. node_modules is not in the tree, so I could not confirm this. Impact with the defaults (TREASURY = LP_WALLET = SAFE): a duplicate treasury part sends 500,000,000 MSFT95 to the Safe. The 200,000,000 liquidity transfer then reverts, because the deployer holds 199,967,700. Every later resume stops at the same place, and the launch can't finish until the Safe signs 250,000,000 back by hand. A duplicate economy part puts a second 250,032,300 into the vault bankroll. The house can take MSFT95 back out only through sweep, at the 100,000 a day dailyCap, unless the Safe raises it with setToken. Shared and deployer-kept wallets otherwise behave correctly: mine() leaves out a part the deployer keeps, and `expected` counts it. The vesting step doesn't have gap (a), because it reads on-chain total() rather than a saved hash. It only has a narrow window where a fund() is still pending when the resume reads total(). Fix: sign before broadcasting. Use populateTransaction with an explicit nonce, then signer.signTransaction, then keccak256(raw), and save {hash, nonce, raw} before provider.broadcastTransaction(raw). On resume with no receipt, rebroadcast the same raw transaction. If getTransactionCount(me,'latest') is already past the saved nonce and there is still no receipt, stop for a manual check instead of sending a new transaction.

**Reproduction**

Ran the unmodified scripts/mainnet/lib.js (copied byte-identical, checked with cmp) outside the repo, with its split() driven against an in-memory chain. Start state: the deployer holds 950,000,000 MSFT95 after the vesting step, SAFE is set, and TREASURY and LP_WALLET are unset. Expected after split: Safe 450,000,000, vault 250,032,300, deployer 249,967,700. Scenario (a): the treasury transfer is applied by the node, but the send call throws 'timeout'. Output: `run 1: stopped: timeout ... | Safe 250,000,000 | vault 250,032,300 | deployer 449,967,700 | record.split [economy]`; `run 2 (resume): stopped: ERC20: transfer amount exceeds balance | Safe 500,000,000 | deployer 199,967,700 | record.split [economy,treasury]`; run 3 gives the same result as run 2. So the treasury part is paid twice and the step can't complete. Scenario (b): run 1 is killed while waiting for the treasury receipt, after its hash was saved. On resume, the RPC returns null for both getTransactionReceipt and getTransaction of that hash. Output: `run 2 (resume via lagging RPC node): stopped: ERC20: transfer amount exceeds balance | Safe 500,000,000 | vault 250,032,300 | deployer 199,967,700`. Actual: the Safe gets 500,000,000 and the deployer is 50,000,000 short of the agents' stake. Expected: each part is paid once.

### 2. Info: Farm turnover limit resets at 00:00 UTC and is kept per token: a sandwiching keeper fits about 4 x slipBps into a few seconds around midnight, and a PEG pool adds a leg per day, against the documented

`msft95-contracts-audit-v5/v4/MSFT95AgentFarm.sol:431`

```
        uint64 today = uint64(block.timestamp / 1 days);
        if (t.day != today) { t.day = today; t.base = balanceOf[agentId][token]; t.used = 0; }
```

_useTurnover is keyed per (agent, input token) and resets on the calendar-day number. The contract header (lines 60-64) and AUDIT-6 #7 say a keeper can now cost an agent 'at most about 2 x slipBps of its cash per day'. (1) Both turnover and the swap counter _swapDay (line 324) reset at block.timestamp / 1 days, not over a rolling 24h like the vault's _spend. So a round trip at 23:59:5x and another at 00:00:0x each pass, about 4 x slipBps within seconds. (2) Every token has its own budget, its balance at that token's first swap. So each extra listed token in a path adds a leg. deploy-farm.js lists PEG stable/stable pools (slipBps 30) next to the stock pools, so USDG -> USDC -> stock -> USDC is 3 legs a day. If the admin lists a stock against both stables, USDG -> A -> USDC -> B -> USDG is 4 legs. (3) The base is read when the keeper first swaps, and the keeper can call remove() just before that, so the budget covers the agent's LP position too, not just its cash. The limit doesn't block holders: withdraw, holderRemove, claimFees and setFrozen never touch turnover. So this is a loss bound looser than documented, not a way to move funds out. Fix: use a rolling 24h window, a start time plus 24h as in the vault's _spend, for both turnover and _swapDay. If 2 x slip is meant as a hard bound, count one budget per agent, not per token, for example the dollar value at the day's first swap. Otherwise document the real bound.

**Reproduction**

Traced by hand against the code. No farm test was executed: the tree has no node_modules or v4-core, so the farm can't be compiled here. Pool: AAPL/USDG ORACLE with slipBps 150 (as deploy-farm.js lists it), active and past usableAt. Agent 1 holds 10,000 USDG and isn't frozen. The keeper is the counterparty and sandwiches each leg down to the floor. At 23:59:50 UTC, swap(1, idx, USDG->AAPL, 10,000e6) sets turnover[1][USDG] to {day D, base 10,000e6, used 10,000e6}. Then swap(AAPL->USDG, all AAPL) sets turnover[1][AAPL] to used = base. A third USDG swap would revert OverCap here, as intended. At 00:00:05 UTC, t.day is D but today is D+1, so line 432 resets base to the remaining ~9,700e6 USDG with used 0, and _swapDay restarts its count at 1. The same two legs pass again. Expected per the doc: about 2 x 1.5% = 3% in a day. Actual: about 4 x 1.5%, roughly 5.9% of the agent's cash, within 15 seconds. With a PEG pool USDG/USDC (slipBps 30) and a TSLA/USDC pool, a day also allows USDG->USDC->TSLA->USDC: 3 legs, about 3.3%, and about 6.6% across midnight.

### 3. Info: Vesting step can never finish with VEST_DELAY=0 (or any delay shorter than deploy+approve+fund): every resume marks the empty schedule stale and deploys another whose fund() reverts AfterStart (merges

`msft95-contracts-audit-v5/scripts/mainnet/lib.js:217`

```
        const start = (await now()) + cfg.VEST_DELAY;
```

config() takes VEST_DELAY as Number(env.VEST_DELAY || 3600), so '0' gives 0 and isn't rejected. start is the latest block's timestamp plus that delay. MSFT95Vesting.fund reverts when block.timestamp >= start (MSFT95Vesting.sol line 60). The fund transaction mines in a later block than `latest`, so its timestamp is >= start and it always reverts. On each resume, the audit-6 L-2 branch (lines 210-214) sees total 0 with now >= start. It pushes the contract to vestingStale and deploys another one, which fails the same way. Nothing is lost: have counts the stale totals, which are 0. But the launch can't pass the vesting step, and each attempt leaves another empty vesting contract on chain. Fix: in config(), reject a VEST_DELAY below a safe minimum (for example 600 s). Before approve and fund, check that start is still at least a margin ahead of the latest block timestamp.

**Reproduction**

Traced against the code. With env VEST_DELAY=0 and the launch at step vesting: deploy(MSFT95Vesting, ..., start = T) mines at T' >= T, approve mines, and fund(50,000,000e18) mines at T'' >= T, so it reverts AfterStart and the step throws. Next run: A().vesting total() = 0 and now >= start, so the address goes into vestingStale and a new schedule is deployed with start = now, and fund reverts again. Expected: one schedule funded with 50,000,000. Actual: vestingStale grows by one address per run, and the step is never recorded.

### 4. Info: Launch pre-flight doesn't validate OPS, TREASURY, LP_WALLET or TEAM, so a malformed value stops the launch half way, after token, hook, pool, staking and part of the split, which audit-4 L-4 was meant

`msft95-contracts-audit-v5/scripts/mainnet/lib.js:57`

```
    OPS: env.OPS || SAFE, TREASURY: env.TREASURY || SAFE, LP_WALLET: env.LP_WALLET || SAFE, TEAM: env.TEAM || SAFE,
```

config() runs addr() (isAddress plus checksum) on SAFE, HOOK_KEEPER, STAKE_KEEPER, SIGNER, COSIGNER, GUARDIAN and MSFT_FEED before any transaction (comment at line 46: 'everything the launch needs is checked before the first transaction'). The four wallets that receive supply or roles are copied as given. A typo is only caught when ethers uses the value. OPS fails at the vesting constructor. TREASURY and LP_WALLET fail in split, after economy has already moved 250,032,300 into the vault. TEAM fails at the agents step. By then the deployer key still holds the rest of the supply and owns the token and the hook. The launch can be recovered by fixing the env and resuming, and no funds are lost. Fix: when not dry, call addr(k, SAFE) for OPS, TREASURY, LP_WALLET and TEAM inside config().

**Reproduction**

Traced against the code. Set TREASURY=0x5fc5360D0400a0Fd4f2af552ADD042D716F1d16 (one hex digit short) with every other setting valid. Expected per the audit-4 L-4 comment: config() throws before the first transaction. Actual: config() returns, because it never calls isAddress on TREASURY. Steps token through vault run. In split, once('economy') pays 250,032,300 to the vault, and then m.transfer(parts.treasury[0], ...) throws from ethers ('invalid address' or an ENS lookup error). mine() compares lower-cased strings and doesn't validate either.

---

Judge's submission `80d8246c5a7c94f0f6dcd1ba26ca71df91dc827a63bd9f109fd495aa077b3acb`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
