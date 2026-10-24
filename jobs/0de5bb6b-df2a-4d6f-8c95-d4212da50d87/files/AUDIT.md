# Audit report

> Scope is the msft95-contracts-audit-v3/ folder only. Ignore msft95-casino/, msft95-vault/, msft95-github-upload/ and the older msft95-contracts-audit/ and msft95-contracts-audit-v2/ folders. README.md has the scope, roles and file hashes. docs/AUDIT-4.md lists the last review's findings and how each was fixed. Earlier reviews were automated, so treat every fix as unverified.
>
> Mainnet launch on Robinhood Chain (4663, Arbitrum Orbit L2). In scope: contracts/MSFT95Vault.sol, contracts/MSFT95Agents.sol (generated from tools/MSFT95Agents.sol.tpl), v4/MSFT95Token.sol, MSFT95RewardHook.sol, MSFT95Router.sol, MSFT95Staking.sol, MSFT95Vesting.sol, MSFT95AgentFarm.sol, MSFT95AgentStakes.sol, Create2Deployer.sol. Mocks, test-helpers, WETH9 and vendor/ are out of scope.
>
> LOOK HARDEST AT (changed since the last review):
>
> 1. MSFT95RewardHook.openTrading(uint128 minLiquidity). Can trading open before the launch position is in? Can the price differ from launchSqrtPrice at that moment? Any way to move slot0 while trading is closed (donate, modifyLiquidity, initialize, another pool pointing at the hook)? Is half the launch liquidity (computed in scripts/mainnet/lib.js launchLiquidity) the right threshold, and is the maths right for both token orders?
>
> 2. MSFT95Staking.sync. An arrival smaller than what is still streaming now joins the running stream without moving its end; a bigger one restarts the hour. Check INV owed + streaming <= held <= balance per token across every path (fresh, idle, dust, setRewardOff on/off, MSFT95 as both stake and reward). Can any arrival size stretch a stream, speed one up, or let a just-in-time staker catch a payout? Does flash staking still earn 0? Also check claimToken now harvests like claim.
>
> 3. Hook price floor (_fairOut): the oraclePaused() check, the sequencer feed and grace period (setSequencer), a timestamp in the future, decimals scaling. Can the keeper or a stolen keeper key still convert below fair value?
>
> 4. Hook unlockCallback RouteTooShallow: a later hop must take exactly what the previous hop gave. Any route or hook shape where this wrongly reverts or lets a currency go unsettled?
>
> 5. MSFT95AgentStakes: claimRewards now also forwards the token's reward() asset (deduped), and the owner has rescue(token, to, amount) for anything but MSFT95. Can rescue or the forwarding loop ever reach principal or MSFT rewards owed to agents in a way the Safe shouldn't?
>
> 6. Launch script (scripts/mainnet/lib.js, rehearse.js): every setting is now checked in config() before the first transaction. Any remaining way for a run to stop half way with the deployer holding supply or ownership? Are the printed Safe actions safe if signed late or out of order?
>
> ALSO RE-CHECK (unchanged, high value):
> - Hook fee deltas in all four swap shapes.
> - Token dividend accounting with excluded addresses. The vault is eligible and MSFT is listed in it (deposits off) for buyback sweeps.
> - The Safe's one-batch setToken / sweep / setToken to sell up to 10% of supply out of the vault.
> - Vault voucher replay and daily caps.
> - What a stolen key can take: farm keeper, hook keeper, agent-stake keeper, vault signer.
>
> Please give a PoC test for each High/Medium finding and say which invariant it breaks.

| | |
|---|---|
| Repository | https://github.com/DrTatum/MSFT95.git |
| Commit | `3062412ab40266b1db749268ff6c83cdfcfca667` |
| Job | `0de5bb6b-df2a-4d6f-8c95-d4212da50d87` |
| Judged | 2026-10-24 07:23 UTC |
| Findings | 3 medium · 4 low · 3 info |

Four agents audited the code as it is at `3062412`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Medium: Vault: MSFT (the dividend asset, deposits off) is voucher-withdrawable, so a stolen SIGNER key alone can take the bankroll's MSFT dividends out at 20x the USDC dollar cap, although the design says onl

`msft95-contracts-audit-v3/scripts/mainnet/lib.js:29`

```
  MSFT: ["0", "50", "200", "10"] };   // MSFT is never deposited: only the Safe's buyback sweeps take it out (at most 200 a day)
```

The launch lists MSFT in the vault with depositsEnabled=false so the Safe can sweep the bankroll's MSFT dividends for buybacks, and the comment and README say MSFT only ever leaves through sweep. But MSFT95Vault.withdraw() (contracts/MSFT95Vault.sol:238-253) validates a voucher against `listed`, maxWithdrawal, dailyCap and cosignAbove only; depositsEnabled is never consulted. LIMITS.MSFT is [minDeposit 0, maxWithdrawal 50 MSFT, dailyCap 200 MSFT, cosignAbove 10 MSFT], so a voucher for exactly cosignAbove (10 MSFT) needs only the SIGNER signature. Twenty such vouchers in one 24h window drain the 200 MSFT daily cap (~$100k at ~$500/MSFT), to any allowlisted address the signer names, with no cosigner and no server balance to represent it (the server never credits MSFT, since deposits are off). No legitimate player MSFT balance can exist, so every MSFT voucher is illegitimate by construction. The USDC limits the soft launch is otherwise built around are $250 single-sig / $5,000 a day, so this per-token limit is ~20x/40x larger in dollars. Invariant broken: MSFT only leaves the vault through Safe sweeps. Note this is also one of the launch settings that config() cannot catch: it is a per-token limit, not a missing env value.

**Reproduction**

State: the vault from lib.js with the mainnet LIMITS; the vault holds 200 MSFT funded via fundBankroll (in production the bankroll's MSFT dividends, settled with MSFT95Token.claimFor(vault)). Input: an attacker holding only the SIGNER private key signs Withdrawal{user: attacker, token: MSFT, amount: 10e18, nonce: 1..20, epoch: voucherEpoch, issuedAt: now, deadline: now+1h} and calls withdraw(w, [sig]). Expected: revert, because MSFT has no voucher path and deposits for it are disabled. Actual: all twenty succeed and 200e18 MSFT moves to the attacker. Foundry test Proof_40a29703e01d.t.sol run against this tree fails with 'a lone SIGNER key voucher-ed the vault's MSFT out: 200000000000000000000 != 0'. Fix (config only, no contract change): list MSFT with maxWithdrawal: 0 and cosignAbove: NO_COSIGN (withdraw then always reverts AboveMaxWithdrawal while sweep only checks dailyCap), or size MSFT's voucher limits in dollars. A sweep-only flag on TokenConfig would be the explicit fix.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.24;

// PoC: with the launch limits for MSFT (scripts/mainnet/lib.js LIMITS.MSFT = minDeposit 0, maxWithdrawal 50,
// dailyCap 200, cosignAbove 10, deposits off) the SIGNER key alone can voucher the vault's MSFT dividends out,
// 10 MSFT per voucher, 200 MSFT per window, although the design says MSFT only ever leaves through Safe sweeps.
// Fails on the shipped configuration (the withdrawals succeed). Passes once MSFT is made sweep-only
// (maxWithdrawal 0 + cosignAbove NO_COSIGN in LIMITS.MSFT, mirrored in MSFT_CFG below, or a sweep-only flag).
import "forge-std/Test.sol";
import {MSFT95Vault} from "contracts/MSFT95Vault.sol";
import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract MsftMock is ERC20 {
    constructor() ERC20("MSFT", "MSFT") { _mint(msg.sender, 1_000_000e18); }
}

contract VaultMsftVoucherTest is Test {
    MSFT95Vault vault;
    MsftMock msft;
    uint256 constant SIGNER_KEY = 0xA11CE;
    address signer = vm.addr(SIGNER_KEY);
    address cosigner = vm.addr(0xB0B);
    address guardian = vm.addr(0xC0C);
    address safe = address(0x5AFE);
    address attacker = address(0xBAD);

    function MSFT_CFG() internal pure returns (MSFT95Vault.TokenConfig memory) {
        // lib.js: MSFT: ["0", "50", "200", "10"], depositsEnabled: false, minDeposit: 0
        return MSFT95Vault.TokenConfig({listed: true, depositsEnabled: false, minDeposit: 0,
            maxWithdrawal: 50e18, dailyCap: 200e18, cosignAbove: 10e18});
    }

    function setUp() public {
        msft = new MsftMock();
        MSFT95Vault.TokenSetup[] memory toks = new MSFT95Vault.TokenSetup[](1);
        toks[0] = MSFT95Vault.TokenSetup({token: address(msft), config: MSFT_CFG()});
        MSFT95Vault.Setup memory s = MSFT95Vault.Setup({admin: safe, adminDelay: 0, signer: signer, cosigner: cosigner,
            guardian: guardian, bankroller: address(this), allowlistOnly: true, allowed: new address[](0), tokens: toks});
        vault = new MSFT95Vault(s);
        // the bankroll's MSFT dividends, settled into the vault (claimFor(vault) in production)
        msft.approve(address(vault), 200e18);
        vault.fundBankroll(address(msft), 200e18);
    }

    function _voucher(uint256 nonce) internal view returns (MSFT95Vault.Withdrawal memory w, bytes[] memory sigs) {
        w = MSFT95Vault.Withdrawal({user: attacker, token: address(msft), amount: 10e18, nonce: nonce,
            epoch: vault.voucherEpoch(), issuedAt: block.timestamp, deadline: block.timestamp + 1 hours});
        (uint8 v, bytes32 r, bytes32 s) = vm.sign(SIGNER_KEY, vault.hashWithdrawal(w));
        sigs = new bytes[](1);
        sigs[0] = abi.encodePacked(r, s, v);   // the SIGNER only: no cosigner
    }

    /// Invariant under test: MSFT (deposits off, dividend asset) never leaves the vault on a voucher.
    function test_signerAloneCannotVoucherMsftOut() public {
        vm.warp(1_700_000_000);
        for (uint256 n = 1; n <= 20; n++) {
            (MSFT95Vault.Withdrawal memory w, bytes[] memory sigs) = _voucher(n);
            // a sweep-only MSFT config makes every one of these revert (AboveMaxWithdrawal)
            try vault.withdraw(w, sigs) {} catch {}
        }
        assertEq(msft.balanceOf(attacker), 0, "a lone SIGNER key voucher-ed the vault's MSFT out");
        assertEq(msft.balanceOf(address(vault)), 200e18, "the vault's MSFT dividends should only leave through sweep");
        // and the Safe's sweep path must still work with the fixed config (sweep only checks the daily cap)
        vm.prank(safe);
        vault.sweep(address(msft), safe, 50e18);
        assertEq(msft.balanceOf(safe), 50e18);
    }
}
```

### 2. Medium: Vault: the runbook's one-batch 10%-of-supply sale leaves window.spent at the swept amount, so every player MSFT95 withdrawal reverts DailyCapExceeded for up to 24h

`msft95-contracts-audit-v3/contracts/MSFT95Vault.sol:289`

```
        uint256 spent = uint256(win.spent) + amount;
```

docs/MAINNET.md section 4 and rehearse.js 7b prescribe selling up to 10% of supply out of the bankroll as one Safe batch: setToken(MSFT95, {maxWithdrawal and dailyCap raised to the amount}), sweep(MSFT95, saleWallet, 100,000,000e18), setToken(MSFT95, original config). sweep() calls _spend(), which records window[MSFT95].spent = 100,000,000e18 in the current 24h window. The restoring setToken() rewrites tokenConfig only; _setToken never touches window[token]. Afterwards every player withdraw() (and every sweep) computes spent = 100,000,000e18 + amount > dailyCap 100,000e18 and reverts DailyCapExceeded until block.timestamp >= win.start + 1 day, and remainingToday() returns 0. The operation the runbook prescribes therefore freezes all player MSFT95 cash-outs (and any further house sweep) for up to a day, and the rehearsal never performs a player withdrawal after the batch, so the suite does not see it. Invariant broken: a house operation completed in its own batch does not change what players can withdraw afterwards.

**Reproduction**

State: vault with LIMITS.MSFT95 (maxWithdrawal 20,000e18, dailyCap 100,000e18, cosignAbove 5,000e18), bankroll funded 250,032,300e18, block.timestamp 1,700,000,000, one allowlisted player. Safe batch: setToken(MSFT95, raised), sweep(MSFT95, saleWallet, 100,000,000e18), setToken(MSFT95, original). Then a SIGNER-signed voucher for 20 MSFT95 to the player. Expected: paid, as 20e18 is far below maxWithdrawal and the 100,000e18 daily cap. Actual: remainingToday == 0 and withdraw reverts DailyCapExceeded(100,000,020e18, 100,000e18); it keeps reverting at now+86399 and only succeeds after the window rolls. Foundry test Proof_58947ff723a1.t.sol fails on this tree with "players' daily allowance is gone after the house sale: 0 <= 20000000000000000000". Fix (minimal, keeps the design): in _setToken, when a listed token's dailyCap changes, reset window[token] (delete), or give sweep() its own house window/cap so house moves do not consume the players' allowance.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.24;

// PoC: the documented one-batch sale (setToken raise / sweep 10% of supply / setToken restore, docs/MAINNET.md and
// rehearse.js 7b) leaves window[MSFT95].spent at 100,000,000e18 while dailyCap is back at 100,000e18, so every
// player voucher for MSFT95 reverts DailyCapExceeded until the 24h window rolls over.
// Fails on the current code (the player's 20 MSFT95 voucher reverts). Passes once _setToken resets or clamps the
// window when a token's dailyCap is lowered (or sweeps get their own allowance).
import "forge-std/Test.sol";
import {MSFT95Vault} from "contracts/MSFT95Vault.sol";
import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract M95Mock is ERC20 {
    constructor() ERC20("MSFT95", "MSFT95") { _mint(msg.sender, 1_000_000_000e18); }
}

contract VaultSaleBatchBlocksPlayersTest is Test {
    MSFT95Vault vault;
    M95Mock m95;
    uint256 constant SIGNER_KEY = 0xA11CE;
    address signer = vm.addr(SIGNER_KEY);
    address cosigner = vm.addr(0xB0B);
    address guardian = vm.addr(0xC0C);
    address safe = address(0x5AFE);
    address player = address(0x91A1E);
    address saleWallet = address(0x5A1E);

    function ORIGINAL() internal pure returns (MSFT95Vault.TokenConfig memory) {
        // lib.js LIMITS.MSFT95: ["20", "20000", "100000", "5000"]
        return MSFT95Vault.TokenConfig({listed: true, depositsEnabled: true, minDeposit: 20e18,
            maxWithdrawal: 20_000e18, dailyCap: 100_000e18, cosignAbove: 5_000e18});
    }

    function setUp() public {
        m95 = new M95Mock();
        MSFT95Vault.TokenSetup[] memory toks = new MSFT95Vault.TokenSetup[](1);
        toks[0] = MSFT95Vault.TokenSetup({token: address(m95), config: ORIGINAL()});
        address[] memory allowed = new address[](1); allowed[0] = player;
        MSFT95Vault.Setup memory s = MSFT95Vault.Setup({admin: safe, adminDelay: 0, signer: signer, cosigner: cosigner,
            guardian: guardian, bankroller: address(this), allowlistOnly: true, allowed: allowed, tokens: toks});
        vault = new MSFT95Vault(s);
        m95.approve(address(vault), 250_032_300e18);
        vault.fundBankroll(address(m95), 250_032_300e18);   // the Worker economy bankroll
    }

    function test_playerCanWithdrawAfterTheSafeSaleBatch() public {
        vm.warp(1_700_000_000);
        uint256 sale = 100_000_000e18;
        // the Safe's three-call batch from docs/MAINNET.md / rehearse.js 7b
        MSFT95Vault.TokenConfig memory raised = ORIGINAL();
        raised.maxWithdrawal = uint128(sale); raised.dailyCap = uint128(sale + 100_000e18);
        vm.startPrank(safe);
        vault.setToken(address(m95), raised);
        vault.sweep(address(m95), saleWallet, sale);
        vault.setToken(address(m95), ORIGINAL());
        vm.stopPrank();
        assertEq(m95.balanceOf(saleWallet), sale);

        // a player cashes out 20 MSFT95 of winnings right after: far below maxWithdrawal and the 100,000 daily cap
        MSFT95Vault.Withdrawal memory w = MSFT95Vault.Withdrawal({user: player, token: address(m95), amount: 20e18,
            nonce: 1, epoch: vault.voucherEpoch(), issuedAt: block.timestamp, deadline: block.timestamp + 1 hours});
        (uint8 v, bytes32 r, bytes32 s) = vm.sign(SIGNER_KEY, vault.hashWithdrawal(w));
        bytes[] memory sigs = new bytes[](1); sigs[0] = abi.encodePacked(r, s, v);
        assertGt(vault.remainingToday(address(m95)), 20e18, "players' daily allowance is gone after the house sale");
        vault.withdraw(w, sigs);   // reverts DailyCapExceeded(100_000_020e18, 100_000e18) on the current code
        assertEq(m95.balanceOf(player), 20e18);
    }
}
```

### 3. Medium: Hook: openTrading checks pool-wide active liquidity, not the launch position, so a stranger's narrow in-range position worth a fraction of the launch capital satisfies the 50%-of-launch-liquidity gate

`msft95-contracts-audit-v3/v4/MSFT95RewardHook.sol:276`

```
        if (minLiquidity == 0 || poolManager.getLiquidity(poolId) < minLiquidity) revert NoLiquidity();
```

Audit 4 M-1 was fixed by requiring getLiquidity(poolId) >= launchLiquidity().min, half the full-range L of the 200,000,000 MSFT95 launch position at PRICE. getLiquidity is the ACTIVE liquidity at the current tick and is not weighted by capital. The hook sets beforeAddLiquidity: false in its permission set (v4/MSFT95RewardHook.sol:313 is an unused hook), so anyone may add liquidity to the closed pool, and the hook never sees or checks the launch position. A position confined to a couple of tick spacings around the current tick has the same L as a full-range position at a much smaller capital cost, and it keeps slot0 at launchSqrtPrice, so the PriceMoved check passes too. The gate therefore does not establish that the launch position is in: if the Safe signs openTrading(min) before (or in a different batch from) the LP wallet's full-range add, a stranger's narrow position opens trading; the stranger then removes it, and the first swap on the now-empty open pool can move slot0 to a price limit at negligible cost, which is the audit-3 H-1 drain state the gate exists to prevent. The launch-liquidity arithmetic in scripts/mainnet/lib.js launchLiquidity() is itself consistent for both token orders; what is wrong is treating active L as evidence about a specific position. Invariant broken: tradingOpen => the launch full-range position is in the pool at launchSqrtPrice.

**Reproduction**

State: the MSFT95/USDG pool initialized at PRICE=0.05 (m95 as currency0, tick -306283, sqrtP 17715820206109101413394), trading closed, launchLiquidity().min = L/2 with L = 200e6*1e18*sp/Q96 = 44721017486476536568, so min = 22360508743238268284. Input: a stranger calls PoolManager.modifyLiquidity with tickLower = -306300, tickUpper = -306240 (two tick spacings around the current tick) and liquidityDelta = min. The band straddles the current tick, so getLiquidity(poolId) == min >= min, and it costs amount0 = 598682414469817754682177 raw (598,682 MSFT95, ~$29,934 at $0.05) and amount1 = 30062648228 raw (30,063 USDG): about $60k borrowed for two blocks, against a launch position of 200,000,000 MSFT95 (~$10M) plus its USDG side. slot0 is unchanged throughout, so sqrtP == launchSqrtPrice passes. Owner calls openTrading(min). Expected per docs/MAINNET.md ('only after the liquidity is in', 'refuses a smaller amount of liquidity'): NoLiquidity, because the launch full-range position is not in. Actual: trading opens on the stranger's position; the stranger removes it in the next transaction and the first swap on the now-open, near-empty pool moves slot0 to a price limit at negligible cost, the audit-3 H-1 state. Measured with src/Gate.t.sol run under forge with @uniswap/v4-core 1.0.2 (the amounts above are that run's logs). Fix: check the launch position itself, e.g. poolManager.getPosition(poolId, lpWallet, fullRangeLower, fullRangeUpper, salt).liquidity >= minLiquidity, or have the hook add the launch position and open trading in one owner-only call.

### 4. Low: Staking: an arrival smaller than what is left joins the running stream over the seconds remaining, not over period, so a just-in-time staker catches it

`msft95-contracts-audit-v3/v4/MSFT95Staking.sol:159`

```
            uint256 rest = finish[token] - block.timestamp;
```

Audit 4 L-1 fixed stream stretching by folding an arrival with add < left into the running stream without moving its end. The consequence is the other direction: the arrival is streamed over rest = finish - now seconds, however short that is, instead of over `period` as the NatSpec promises ('Each arrival is paid out to stakers evenly over period ... nobody can catch a payout by staking for a moment around it'). Late in a stream rest is small, so an arrival of up to left is paid out almost immediately. Arrivals only start streaming when someone calls sync(), so anyone can choose the moment: leave the casino's transfer unsynced, stake a large amount just before finish (stake() calls _syncAll), unstake at finish and claim. The same compression applies to the dust/idle re-stream branch at line 149. Conservation (owed + streaming <= held <= balance) still holds, so no funds are lost to the contract; the loss is to stakers who were in for the full hour. Bounded by what is left of the stream and requires real stake, hence low. Invariant broken: each arrival is paid out evenly over period, so nobody can catch a payout by staking for a moment around it.

**Reproduction**

Honest staker stakes 1,000e18; 3,600e18 USDC arrives and sync() streams it at 1e18/s for 3,600s. At finish - 10s the remaining stream is 10e18 USDC and a 9e18 USDC arrival comes in (add < left), so sync() sets rate += 9e18/10s and finish stays. A just-in-time staker stakes 9,000e18 (90% of the pool) just before, waits to finish, unstakes and claims. Expected under the documented hour-long stream: its share of the 9e18 arrival over 10s is 9e18*0.9*10/3600 = 0.0225e18. Actual: 8.1e18 (it also takes 90% of the last 10e18 of the old stream). Foundry test Proof_96525acf4ed4.t.sol fails on this tree with 'the late arrival was paid out in 10 seconds: 8100000000000000000 > 23500000000000000'. Fix: when add < left, do not shorten the payout window: either extend finish so the combined amount still streams for close to period (newRest = max(rest, period*add/(add+left))), or keep the new arrival on its own rate ending at max(finish, now+period).

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import "forge-std/Test.sol";
import {MSFT95Staking} from "msft95-contracts-audit-v3/v4/MSFT95Staking.sol";
import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract Tok is ERC20 {
    constructor(string memory n) ERC20(n, n) { _mint(msg.sender, 1e30); }
    // MSFT95Staking._harvest() calls claim() on the stake token; a plain ERC-20 has none, so provide a no-op
    function claim() external pure returns (uint256) { return 0; }
}

/// sync(): an arrival smaller than what is still streaming is spread over the SECONDS LEFT in the running stream, not over
/// `period`. Late in a stream that is a few seconds, so a staker who steps in just before the sync and out right after the
/// stream ends takes its share of the new arrival almost at once. Expected: every arrival streams for about an hour, so a
/// 10-second stake earns at most ~10/3600 of it.
contract StakingJoinSpeedsUp is Test {
    MSFT95Staking staking;
    Tok msft95; Tok usdc;
    address honest = address(0xA0);
    address jit = address(0x717);

    function setUp() public {
        vm.warp(1_000_000);
        msft95 = new Tok("MSFT95"); usdc = new Tok("USDC");
        address[] memory rewards = new address[](1); rewards[0] = address(usdc);
        staking = new MSFT95Staking(msft95, address(this), rewards);
        msft95.transfer(honest, 1_000e18); msft95.transfer(jit, 9_000e18);
        vm.prank(honest); msft95.approve(address(staking), type(uint256).max);
        vm.prank(jit); msft95.approve(address(staking), type(uint256).max);
    }

    function test_jitStakerCatchesLateArrival() public {
        vm.prank(honest); staking.stake(1_000e18);
        usdc.transfer(address(staking), 3_600e18);                      // the casino's hourly house edge arrives...
        staking.sync(address(usdc));                                     // ...and streams at 1 USDC/s for an hour
        uint256 finish = staking.finish(address(usdc));

        vm.warp(finish - 10);                                            // 10 seconds before the stream ends: 10 USDC left
        usdc.transfer(address(staking), 9e18);                           // a smaller arrival of 9 USDC
        vm.prank(jit); staking.stake(9_000e18);                          // the JIT staker takes 90% of the pool and syncs the arrival
        (uint256 remaining, uint256 endsAt) = staking.streaming(address(usdc));
        assertEq(endsAt, finish);                                        // the end did not move: the 9 USDC go out over 10 s
        assertEq(remaining, 19e18);

        vm.warp(finish);
        vm.prank(jit); staking.unstake(9_000e18);
        vm.prank(jit); staking.claim();
        uint256 got = usdc.balanceOf(jit);
        // 10 seconds of an hour-long stream of 9 USDC at a 90% share is 0.0225 USDC; the JIT staker gets 8.1 USDC of the
        // arrival (plus 9 of the old stream's last 10 USDC): 17.1 in total
        assertLe(got - 9e18, 9e18 * 90 / 100 * 10 / 3600 + 1e15, "the late arrival was paid out in 10 seconds");
    }
}
```

### 5. Low: Launch: findRoute picks whichever hookless USDG/MSFT pool has the most active liquidity, so a pool anyone can create becomes the hook's conversion route with no operator review

`msft95-contracts-audit-v3/scripts/mainnet/lib.js:323`

```
  const direct = await live(a.usdg, a.msft); if (direct) return [direct.k];
```

On mainnet the route step calls findRoute(), which scans the four standard fee tiers for USDG/MSFT (then USDG/WETH + WETH/MSFT, then USDG/ETH + ETH/MSFT) and picks the pool with the largest getLiquidity(), requiring only L > 0 and a nonzero price. Pool creation on Uniswap v4 is permissionless, so anyone who sees the launch coming can initialize a USDG/MSFT pool (or either two-hop pair) at an arbitrary price with 1 wei of liquidity. If no deeper legitimate pool exists at that moment, setRoute() is signed for the attacker's pool with no operator review: the script never prints the chosen pool key, never checks its liquidity against a floor, and never compares its price to the Chainlink feed it just configured. With the floor on, every convert() then reverts TooLittle (fees wait until the Safe calls setRoute, a timelocked action); with ALLOW_NO_FEED=1 the keeper sells the fees into the attacker's pool at its price. Invariant broken: the conversion route is a pool the operator approved / deep enough to price a week of fees.

**Reproduction**

State: Robinhood Chain with no USDG/MSFT pool deeper than the attacker's, or none at all. Attacker: PoolManager.initialize({USDG, MSFT, fee 100, tickSpacing 1, hooks 0}, sqrtPrice for 1 MSFT = 1 USDG) and adds liquidityDelta 1 in a one-tick range. Launch: the route step runs findRoute(); live(usdg, msft) returns that key (L = 1 > 0, p > 0), so hook.setRoute([attackerKey]) is sent. Expected: setRoute only for a pool the operator approved or with liquidity above a minimum, and a printed key. Actual: convert() routes through the attacker's pool; with a feed set every conversion reverts TooLittle until the Safe resets the route, and without one the fees are sold at the attacker's price. Fix: require a minimum active liquidity (e.g. the USDG value of a week of expected fees) and a spot price within maxSlipBps of the feed before setRoute; print the chosen key and require ROUTE=<keys> to be set explicitly on mainnet.

### 6. Low: Launch: the 0.8.24 build artifacts are only checked in the vault step, after the token, hook, pool, route, feed, router, staking and vesting have already been sent

`msft95-contracts-audit-v3/scripts/mainnet/lib.js:216`

```
      const V = await v1Factory(ethers, "MSFT95Vault", signer).deploy(setup);
```

Audit 4 L-4 moved every env setting into config() so a missing one cannot stop the run half way with the deployer holding supply and ownership. One precondition is still checked late: v1Factory() (lib.js:34-39) throws 'Build the vault contracts first (npx hardhat compile)' when artifacts/contracts/MSFT95Vault.sol/MSFT95Vault.json is missing, and it is first called at line 216 inside the vault step and again at line 247 inside the agents step. launch.js runs with hardhat.v4.config.js, whose artifacts path is ./artifacts-v4, so the 0.8.24 artifacts are only produced by a separate `npx hardhat compile`. A fresh machine (the runbook asks for a fresh server) that runs the launch without that separate compile reaches the vault step with the deployer holding 1,000,000,000 MSFT95 and owning the token and the hook, the pool initialized, and staking, vesting and the router deployed, then stops: exactly the state L-4 set out to prevent. The README's launch command does not include the compile. The run is resumable, so this is a low, not a medium.

**Reproduction**

Input: a checkout with no ./artifacts directory (only `npx hardhat --config hardhat.v4.config.js compile` was run) and every env setting valid. Run `npx hardhat --config hardhat.v4.config.js run scripts/mainnet/launch.js --network rhMainnet`. Expected: it refuses before the first transaction. Actual: the chain, token, hook, pool, route, feed, router, staking and vesting steps all succeed (about 14 transactions), then 'Build the vault contracts first ... is missing' is thrown at the vault step, with the deployer still holding the supply and ownership of the token and hook. Fix: call v1Factory for MSFT95Vault and MSFT95Agents in config() (or at the start of chain()) and fail if either artifact is missing.

### 7. Low: Launch: resuming after a failure inside the 'split' step funds the vault a second time and leaves the deployer unable to fund the LP wallet or the agent stakes

`msft95-contracts-audit-v3/scripts/mainnet/lib.js:235`

```
      await send(m.approve(A().vault, parts.economy[1])); await send(V.fundBankroll(A().msft95, parts.economy[1]));
```

step() records a step only after its whole function returns (lib.js:96-99), and the split step sends up to four transactions with no per-transaction record and no on-chain state check. If any transaction after fundBankroll fails (an RPC timeout in .wait() after the tx was mined, a gas or nonce error, the operator pressing Ctrl-C), the resume re-runs the whole step and calls fundBankroll(MSFT95, 250,032,300e18) again. The config() pre-checks do not cover this path. Invariant broken: the supply split vault 250,032,300 / treasury 250,000,000 / LP 200,000,000 / agent stakes 249,967,700 / vesting 50,000,000. The run then stops with the deployer still owning the token and hook, and the extra 250M needs the Safe to raise dailyCap with setToken (100k/day as configured) to get back out.

**Reproduction**

Run launch.js on a fork. Let split's fundBankroll be mined, then make the treasury transfer's wait() throw (kill the RPC). Re-run launch.js. Expected: split resumes without re-funding. Actual: fundBankroll is sent again, so the vault holds 500,064,600 MSFT95. The deployer has 1e9 - 50M - 500,064,600 = 449,935,400; the treasury takes 250M, then the 200M LP transfer reverts (199,935,400 left), so the run stops before agentStakes and handover. Fix: make each sub-transfer idempotent, either by recording each sub-transaction or by checking on-chain balances (vault MSFT95 balance, treasury balance) before sending.

### 8. Info: AgentStakes: rescue() can take the agents' MSFT dividends and staking reward tokens between keeper collections

`msft95-contracts-audit-v3/v4/MSFT95AgentStakes.sol:197`

```
    function rescue(IERC20 t, address to, uint256 amount) external onlyOwner nonReentrant {
```

rescue() excludes only MSFT95 (and to == 0). Everything else the contract holds is, by its own accounting, a reward owed to the agents: the MSFT that the liquid MSFT95 earns as a holder (forwarded by claimRewards since audit 4 I-2) and the USDC/wsNET/IMD/WETH/MSFT that staking.claim() pays. Until the keeper's claimRewards() runs, the owner (the Safe) can rescue() any of it to any address. This is an owner trust assumption rather than a bypass, and principal is not reachable (rescue refuses MSFT95, and the forwarding loop subtracts liquid()), but the NatSpec ('Return a token other than MSFT95 that is stuck here (sent by mistake)') and README ('it can't touch a registered agent's allocation') undersell it. Fix: also refuse IHolder(token).reward() and every address in staking.rewardTokenList(), or document the power in README's trust section.

**Reproduction**

AgentStakes holds liquid MSFT95. After MSFT95Token.distribute() and anyone calling MSFT95Token.claimFor(agentStakes), MSFT.balanceOf(agentStakes) > 0. The Safe calls agentStakes.rescue(MSFT, safe, X). Expected per NatSpec: only a stray token can be moved. Actual: X MSFT goes to the Safe, and the next claimRewards forwards 0 MSFT to the keeper. Same for any listed staking reward token paid in by claimRewards' staking.claim().

### 9. Info: Vault: setToken / sweep / setToken in one Safe batch moves any amount at once, so the daily cap bounds only the SIGNER key, not the admin

`msft95-contracts-audit-v3/contracts/MSFT95Vault.sol:346`

```
    function sweep(address token, address to, uint256 amount) external onlyRole(DEFAULT_ADMIN_ROLE) nonReentrant {
```

sweep is documented as counting against the same daily cap as players, and it does, but setToken is not timelocked (AccessControlDefaultAdminRules delays only admin handover). The admin can raise dailyCap/maxWithdrawal, sweep any amount, and restore the config within one transaction, as docs/MAINNET.md itself prescribes for the 10% sale. So the cap protects only against a stolen SIGNER key, and the NatSpec should say the Safe is unbounded. Stolen-key bounds otherwise hold: a SIGNER alone gets at most cosignAbove per voucher and 2x dailyCap per token per 24h, and vouchers are bound by chainId/contract (EIP-712), per-user nonce, epoch, a 1-day lifetime and a 5-minute clock skew.

**Reproduction**

With LIMITS.MSFT95 (dailyCap 100,000e18), a Safe batch of setToken(MSFT95, {listed:true, depositsEnabled:true, minDeposit:20e18, maxWithdrawal:1e26, dailyCap:1e26, cosignAbove:NO_COSIGN}), sweep(MSFT95, buyback, 1e26), setToken(MSFT95, original) succeeds and moves 100,000,000e18 MSFT95 in one transaction. Expected per the NatSpec on sweep ('Counts against the same daily cap as players'): DailyCapExceeded. Actual: the transfer succeeds. Document as an admin power; no code change needed if the Safe is trusted.

### 10. Info: Staking: per-user floor rounding lets the sum of owed exceed held by a few wei; _pay caps it so the last claimer is short by dust

`msft95-contracts-audit-v3/v4/MSFT95Staking.sol:121`

```
        if (a > held[t]) a = held[t];   // rounding never lets claims run past what was shared
```

_settle credits floor(accPerShare*s/ACC) - floor(accPerShare_old*s/ACC) on every settle, which can exceed the exact share by up to 1 wei per user per settle; the dust mapping catches only the accPerShare division remainder, not this one. Over many settles the sum of owed drifts above held by wei. The cap at line 121 prevents over-payment, so the only effect is that whoever claims last may receive a few wei less than owed and owed keeps a dust balance that can never be paid. No staker funds are lost.

**Reproduction**

Randomized sequence (three users, stake 1..1000e18, USDC and MSFT95 arrivals, warps, claims, setRewardOff on/off): after ~50 steps the sum over users of claimable(t) + streaming + dust + idle exceeds held(t) by a few hundred wei. Expected: sum(owed) <= held exactly. Actual: exceeded by 893 wei in one observed run; _pay caps each payment at held, so the totals still balance in token terms.

---

Judge's submission `7d961646ba6a33ae5bf0cb731eba366b285e7c04f096e398d8bbb6d791a70cb3`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
