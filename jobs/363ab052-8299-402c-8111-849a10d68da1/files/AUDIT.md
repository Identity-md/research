# Audit report

> Final check for The Zero Person Billion Dollar Company ($COMPANY) on Robinhood Chain (4663), after IMD Swarm audit 78c00339 and re-check f1d5def3. AUDIT.md sections 4 and 5 map every finding to its fix and its test.
>
> What the contracts are for: CompanyToken is a fixed 1,000,000,000 supply ERC-20; its ownership is renounced in the constructor. CompanyHook owns the token's only Uniswap v4 pool, paired with IMD, with liquidity locked forever, and takes 4% of every swap: 1% to the protocol, 3% to holders. Holder fees are split 50% IMD and 10% each to NVDA, GOOGL, AAPL, GME and MSTR Robinhood stock tokens, bought IMD -> USDG -> stock at the start of every claim(). Only wallets holding at least 100,000 earn, and unclaimed rewards expire after 7 days.
>
> Changed since the re-check; review these hardest:
> 1. Chainlink check on the stock hop (fix for re-check finding 1): minStockOut(asset, usdIn) uses the stock/USD and USDG/USD feeds (8 decimals, max age 4 days, 3% tolerance) and is enforced in unlockCallback, which reverts PriceOff. _convertAll skips the stock on PriceOff or a stale feed, and falls back to IMD only on other failures. Can a caller force PriceOff or the fallback, or get a purchase through at a manipulated price? Are the decimals (USDG 6, stocks 18, read at deployment) and the stale-feed handling right?
> 2. GME (0x1b0E319c6A659F002271B69dB8A7df2F911c153E, the official Robinhood token) replaces AMC, which has no feed. Its v4 USDG pool (fee 1%, spacing 200, id 0x3d436b4f...063b) is thin (about $6k), so stockRoundLimit binds near 3.4 IMD per round.
> 3. A zero stockRoundLimit now credits the round as IMD without swapping (re-check finding 2).
> 4. Too little gas skips the stock instead of reverting (re-check finding 3).
>
> Please confirm these, check that nothing broke the solvency of the six reward assets, the flash-borrow guard, the 100,000 minimum, expiry or the scanner-relevant properties, and report anything new.
>
> Tests: cd contracts; git submodule update --init --recursive; forge test. Fork test (live feeds and pools): FORK_RPC=https://robinhood.drpc.org forge test --mc CompanyForkTest.

| | |
|---|---|
| Repository | https://github.com/imdmaxi/IMDINDEX.git |
| Commit | `d624407521951dcafa6aeb77a372e69226bb07fe` |
| Job | `363ab052-8299-402c-8111-849a10d68da1` |
| Judged | 2026-10-07 12:07 UTC |
| Findings | 2 high · 1 medium · 2 low · 2 info |

Four agents audited the code as it is at `d624407`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. High: Any send resets the expiry timer without forfeiting: an inactive wallet self-transfers 1 wei and claims its whole expired backlog

`contracts/src/CompanyToken.sol:373`

```
            if (!fromSystem) lastActive[from] = block.timestamp;
```

claim() is strict: it calls _recycle(msg.sender) before resetting lastActive, so a wallet inactive for more than 7 days hands everything but its last 7 days' earnings to feeRecipient (contract notice; test_expiry_claimIsStrict). _transfer is not: for any non-zero amount it sets lastActive[from] = block.timestamp (and lastActive[to] when the receiver pulled with transferFrom) without touching rewards that have already expired. expiredRewardsOf is gated on `block.timestamp <= last + INACTIVITY_PERIOD`, so once the timer is reset it returns 0 for every asset and the next claim pays the whole backlog in all six assets. The wallet needs nothing but 1 wei of its own tokens (transfer(self, 1)) or an accomplice to pull 1 wei from, and it can front-run any keeper's recycle() call. Net effect: expiry only ever applies to holders who do not know the trick, and feeRecipient loses every expired reward of everyone else; AUDIT.md guarantee 6 and the 'Expiry is strict' comment in claim() do not hold. This also undermines the fix for the flash-borrow finding below: returning borrowed tokens is itself a send. Fix (keeps the design): when a wallet becomes active again after more than 7 days, forfeit what has expired before resetting the timer, exactly as claim does. In _transfer, before the balances change (so weightOf is still the old weight): `if (!fromSystem && lastActive[from] != 0 && block.timestamp > lastActive[from] + INACTIVITY_PERIOD) _recycle(from);` and the same for `to` when msg.sender == to. Verified: with that change the attached proof passes and all 41 project tests still pass. (Reported by audit_economics; reproduced.)

**Reproduction**

Unit setup as in Company.t.sol (mock IMD/USDG/stocks, real PoolManager). alice buys 20 IMD, bob buys 20 IMD: alice is credited 0.6 IMD. Warp 8 days; bob buys 10 IMD (one distribution inside the last 7 days): alice's recent share is 0.0794 IMD and expiredRewardsOf(alice, 0) == 0.6e18. Then vm.prank(alice); token.transfer(alice, 1); vm.prank(alice); token.claim(). Expected: paid[0] <= ~0.0794 IMD and 0.6 IMD reaches feeRecipient (or recycledHeld). Actual: expiredRewardsOf drops to 0 after the self-transfer, claim pays 679426250124817669 wei (0.679 IMD) to alice and feeRecipient receives 0. forge test --match-path test/scratch/ExpiryTransferRevive.t.sol fails with 'an inactive wallet is paid only its last 7 days: 679426250124817669 > 79426250124817672' and passes once _transfer forfeits expired rewards before resetting lastActive.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {PoolManager} from "v4-core/src/PoolManager.sol";
import {IPoolManager} from "v4-core/src/interfaces/IPoolManager.sol";
import {IHooks} from "v4-core/src/interfaces/IHooks.sol";
import {PoolModifyLiquidityTest} from "v4-core/src/test/PoolModifyLiquidityTest.sol";
import {TickMath} from "v4-core/src/libraries/TickMath.sol";
import {PoolKey} from "v4-core/src/types/PoolKey.sol";
import {Currency} from "v4-core/src/types/Currency.sol";
import {ModifyLiquidityParams} from "v4-core/src/types/PoolOperation.sol";

import {CompanyHook} from "src/CompanyHook.sol";
import {CompanyToken} from "src/CompanyToken.sol";
import {CompanyRouter} from "src/CompanyRouter.sol";
import {DeployLib} from "script/DeployLib.sol";

contract ScratchERC20 {
    uint8 public decimals = 18;
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    function mint(address to, uint256 amt) external {
        balanceOf[to] += amt;
    }

    function approve(address s, uint256 amt) external returns (bool) {
        allowance[msg.sender][s] = amt;
        return true;
    }

    function transfer(address to, uint256 amt) external returns (bool) {
        balanceOf[msg.sender] -= amt;
        balanceOf[to] += amt;
        return true;
    }

    function transferFrom(address f, address to, uint256 amt) external returns (bool) {
        if (allowance[f][msg.sender] != type(uint256).max) allowance[f][msg.sender] -= amt;
        balanceOf[f] -= amt;
        balanceOf[to] += amt;
        return true;
    }
}

contract ScratchFeed {
    function decimals() external pure returns (uint8) {
        return 8;
    }

    function latestRoundData() external view returns (uint80, int256, uint256, uint256, uint80) {
        return (1, 1e8, block.timestamp, block.timestamp, 1);
    }
}

contract ExpiryTransferReviveTest is Test {
    address constant FEE_RECIPIENT = 0x8F5A29c82e8285Db3B2af8D0caF5404b0f9ce834;
    uint256 constant SUPPLY = 1_000_000_000e18;

    PoolManager pm;
    ScratchERC20 imd;
    ScratchERC20 usdg;
    CompanyHook hook;
    CompanyToken token;
    CompanyRouter router;
    address alice = makeAddr("alice");
    address bob = makeAddr("bob");
    address owner = makeAddr("owner");

    function _key(address a, address b, uint24 fee, int24 ts) internal pure returns (PoolKey memory) {
        (address c0, address c1) = a < b ? (a, b) : (b, a);
        return PoolKey(Currency.wrap(c0), Currency.wrap(c1), fee, ts, IHooks(address(0)));
    }

    function setUp() public {
        vm.warp(1_800_000_000);
        pm = new PoolManager(address(this));
        imd = new ScratchERC20();
        usdg = new ScratchERC20();
        PoolModifyLiquidityTest lp = new PoolModifyLiquidityTest(pm);
        imd.mint(address(this), 10_000_000e18);
        usdg.mint(address(this), 10_000_000e18);
        imd.approve(address(lp), type(uint256).max);
        usdg.approve(address(lp), type(uint256).max);

        PoolKey memory imdEth = PoolKey(Currency.wrap(address(0)), Currency.wrap(address(imd)), 10_000, 100, IHooks(address(0)));
        pm.initialize(imdEth, TickMath.getSqrtPriceAtTick(0));
        PoolKey memory imdUsd = _key(address(imd), address(usdg), 9000, 90);
        pm.initialize(imdUsd, TickMath.getSqrtPriceAtTick(0));
        lp.modifyLiquidity(imdUsd, ModifyLiquidityParams(-887220, 887220, 10_000e18, 0), "");

        address[5] memory stocks;
        CompanyToken.Pool[5] memory pools;
        address[5] memory feeds;
        for (uint256 i; i < 5; i++) {
            ScratchERC20 s = new ScratchERC20();
            s.mint(address(this), 10_000_000e18);
            s.approve(address(lp), type(uint256).max);
            PoolKey memory k = _key(address(usdg), address(s), 3000, 60);
            pm.initialize(k, TickMath.getSqrtPriceAtTick(0));
            lp.modifyLiquidity(k, ModifyLiquidityParams(-887220, 887220, 1_000_000e18, 0), "");
            stocks[i] = address(s);
            pools[i] = CompanyToken.Pool(3000, 60);
            feeds[i] = address(new ScratchFeed());
        }

        bytes memory initCode = abi.encodePacked(
            type(CompanyHook).creationCode,
            abi.encode(
                pm,
                address(imd),
                owner,
                FEE_RECIPIENT,
                DeployLib.startTickForMarketCap(306e18, SUPPLY),
                CompanyHook.ImdEthPool(10_000, 100, address(0))
            )
        );
        uint160 flags = uint160((1 << 13) | (1 << 11) | (1 << 7) | (1 << 6) | (1 << 3) | (1 << 2));
        (bytes32 salt, address expected) = DeployLib.mineSalt(address(this), flags, initCode, 0);
        address deployed;
        assembly {
            deployed := create2(0, add(initCode, 0x20), mload(initCode), salt)
        }
        require(deployed == expected, "hook address");
        hook = CompanyHook(payable(deployed));
        router = CompanyRouter(payable(hook.router()));
        token = new CompanyToken(
            address(hook), address(usdg), CompanyToken.Pool(9000, 90), stocks, pools, address(new ScratchFeed()), feeds
        );
        vm.prank(owner);
        hook.openPool(address(token));

        address[2] memory users = [alice, bob];
        for (uint256 i; i < 2; i++) {
            imd.mint(users[i], 1_000_000e18);
            vm.prank(users[i]);
            imd.approve(address(router), type(uint256).max);
        }
    }

    function _buy(address who, uint256 imdIn) internal returns (uint256) {
        vm.prank(who);
        return router.buy(address(token), imdIn, 0, block.timestamp);
    }

    /// @dev Expected (contract notice, test_expiry_claimIsStrict): once a wallet has been inactive for more than 7 days,
    ///      everything but its last 7 days' earnings has expired and goes to the protocol. Actual: `_transfer` resets
    ///      `lastActive[from]` without forfeiting anything, so a 1 wei self-transfer makes `expiredRewardsOf` 0 again
    ///      and the following claim pays the whole backlog to the wallet.
    function test_selfTransferRevivesExpiredRewards() public {
        _buy(alice, 20e18);
        _buy(bob, 20e18);
        uint256 old = token.withdrawableRewardOf(alice, 0);
        assertApproxEqAbs(old, 0.6e18, 10);

        vm.warp(block.timestamp + 8 days);
        _buy(bob, 10e18); // a distribution inside the last 7 days
        uint256 recent = token.withdrawableRewardOf(alice, 0) - old;
        uint256 expired = token.expiredRewardsOf(alice, 0);
        assertEq(expired, old, "the 0.6 IMD earned 8 days ago have expired");

        uint256 feeBefore = imd.balanceOf(FEE_RECIPIENT);
        vm.prank(alice);
        token.transfer(alice, 1); // "activity"
        vm.prank(alice);
        uint256[6] memory paid = token.claim();

        assertLe(paid[0], recent + 2, "an inactive wallet is paid only its last 7 days");
        assertEq(
            imd.balanceOf(FEE_RECIPIENT) - feeBefore + token.recycledHeld(0),
            expired,
            "the expired part belongs to the protocol"
        );
    }
}
```

### 2. High: claim() runs inside a foreign PoolManager unlock and expiredRewardsOf scales 'recent' by the live weight, so flash-borrowed pool tokens (or a round-trip gift) make nothing expire

`contracts/src/CompanyToken.sol:519`

```
        uint256 recent = FullMath.mulDivRoundingUp(magnifiedRewardPerShare[asset] - magCut, weightOf(holder), MAGNITUDE);
```

expiredRewardsOf estimates the non-expiring 'recent' part as (per-share growth since the 7-day cutoff) x weightOf(holder), reading the holder's CURRENT weight; the comment assumes the weight can only have grown by tokens the holder legitimately earned on. claim() (line 478) is callable while the PoolManager is unlocked by someone else: hook.flush is a no-op for a non-router caller and _convertAll returns, but _recycle(msg.sender) still runs. A contract holder can pm.unlock(), pm.take() the pool's whole $COMPANY balance (~88% of supply at launch) for free, call claim(), then transfer the tokens back and settle(). A receipt from the PoolManager does not touch lastActive (the wallet is still 'inactive'), the borrowed weight does not change withdrawableRewardOf (corrections offset it), but it multiplies 'recent' by (pool balance + own) / own, so with any distribution in the window (the attacker can make a dust buy itself) recent exceeds the whole backlog, expiredRewardsOf returns 0, nothing is recycled, the timer is reset and the claim pays every expired reward in all six assets. The same inflation works without an unlock through a round-trip gift from an accomplice (receiving is not activity, the sender keeps its own rewards), which needs capital of about backlog / recent-growth tokens; the flash variant needs none. Independent of the self-transfer finding (the claim happens before any send). Victim: feeRecipient; AUDIT.md guarantee 6 is bypassed and section 6's 'a gift can only delay expiry, to nobody's gain' is wrong when combined with a claim. The existing FlashHolder mode-4 test only covers a wallet with no prior rewards. Fix: refuse claim() and recycle() while IPoolManager(poolManager).isUnlocked() (the routers never call them). `revert Reentrancy()` is the robust form (verified: the attached proof passes; test_flashBorrowedTokens_cannotCaptureRewards mode 4 then needs to expect the revert). A `return amounts` guard is only sufficient together with the forfeit-on-transfer fix of the previous finding, because returning the borrowed tokens is a send that resets the timer (verified both ways). To also close the gift variant, compute 'recent' from a weight that cannot be inflated at claim time, e.g. snapshot the weight whenever lastActive is set and use min(snapshot, current). (Reported by audit_math, audit_flow and audit_economics; merged, reproduced.)

**Reproduction**

Unit setup as in Company.t.sol. A contract wallet W buys 20 IMD of $COMPANY through CompanyRouter, bob buys 20 IMD: W is credited 0.6 IMD. Warp 8 days; bob buys 10 IMD: W's recent share is 0.0794 IMD, expiredRewardsOf(W, 0) == 0.6e18. W calls pm.unlock; in unlockCallback: pm.take(COMPANY, W, balanceOf(pm)); token.claim(); pm.sync; transfer the tokens back; pm.settle. Expected (test_expiry_claimIsStrict): W is paid at most ~0.0794 IMD and 0.6 IMD reaches feeRecipient. Actual: W is paid 679426250124817669 wei (0.679 IMD), feeRecipient receives nothing and W's timer is reset. forge test --match-path test/scratch/ExpiryFlashBypass.t.sol fails with 'an inactive wallet is paid only its last 7 days: 679426250124817669 > 79426250124817672'; it passes when claim() reverts mid-unlock, or with a return-early guard combined with forfeit-on-transfer.

### 3. Medium: A Chainlink feed that stops updating for good (or an empty IMD/USDG pool) locks that stock's 10% reserve forever: skipped every round, never falls back, no admin

`contracts/src/CompanyToken.sol:598`

```
            if (!_feedsFresh(a)) continue;
```

_convertAll treats a stale or unusable feed (answer <= 0, call reverting, or updatedAt older than MAX_ORACLE_AGE = 4 days) as 'hold the stock': continue, no lastConvert update, no _fallBackToImd. That is right for a weekend or a holiday, but the hold has no end. If a stock's /USD feed is deprecated by Chainlink, repointed, or simply stops updating (the five feeds are new, on a new L2, and the NVDA one is already a differently named generation, 'RHNVDA / USD', than the four 'Robinhood X / USD' feeds), _feedsFresh(a) is false on every call for the rest of the contract's life. distribute() keeps moving 10% of every holder-fee arrival into pendingConvert[a] (50% for all five stocks if the shared USDG/USD feed dies), the IMD stays counted in _pendingTotal() so distribute() never re-credits it, and nothing can release it: convert/claim skip it, there is no owner, no setter for priceFeeds/usdFeed, and the only path to _fallBackToImd for that stock is the exact-zero stockRoundLimit branch, which needs the stock pool to be empty at its price. The same no-exit behaviour exists when the IMD/USDG pool has no in-range liquidity (maxConvert() == 0 at line 583: cap = 0, every stock skipped, no fallback). Compare: a stock whose token blocks this contract or whose pool is empty is paid to holders as IMD one capped round at a time; a dead feed strands the same money. Minimal fix preserving the design: keep the 4-day hold, but after an extended outage (e.g. updatedAt older than 30 days, far beyond any market closure, or no successful conversion for that long while a reserve waits) treat the stock like one that cannot be bought and _fallBackToImd(a, imdIn) one capped round at a time; do the same when maxConvert() has been 0 that long. (Reported by audit_permissions, audit_flow and audit_economics; merged, reproduced.)

**Reproduction**

Unit setup as in Company.t.sol. alice and bob buy 1,000 IMD each (pendingConvert(1) == 6e18). Set the NVDA feed's updatedAt to now - 5 days and never update it again; keep USDG and the other four feeds fresh. For 365 days: warp +1 day, refresh the other feeds, call convert() and have alice claim(). Expected: the 6 IMD reserved for NVDA reach holders within a bounded time, as NVDA or as IMD. Actual: owed(1) == 0, pendingConvert(1) is still exactly 6e18 after a year while pendingConvert(2) == 0 (the other stocks converted), stockRoundLimit(1) > 0 (the pool is fine), and one more 1,000 IMD buy makes it 9e18. Second input: remove all in-range liquidity from the IMD/USDG pool so maxConvert() == 0; after 30 daily convert() calls all five pendingConvert stay at 6e18. Both are demonstrated by forge test --match-path test/scratch/StaleFeedLock.t.sol (passes on this code: it asserts the frozen state).

### 4. Low: Re-check fix 2 (zero stockRoundLimit pays the round as IMD) is defeated by a dust in-range position: the reserve is held instead of paid

`contracts/src/CompanyToken.sol:592`

```
            if (poolLimit == 0) {
```

The 'no liquidity at the stock pool's price' branch tests stockRoundLimit(a) for exactly zero. stockRoundLimit is fee/2 x the virtual USDG depth of whatever liquidity is in range, so one dust position (2e9 liquidity, a few wei of each token, full range) makes it a few wei instead of zero. The round then becomes imdIn = that handful of wei: convertStock swaps it, minStockOut rounds to 0 so the price check passes (or Slippage falls back the same few wei), lastConvert is set, and the 4 IMD the round was meant to hand to holders as IMD stays in pendingConvert. Anyone can place that position in the hookless stock pools today for the cost of one LP transaction (it does nothing while real liquidity covers the price), and whenever the real liquidity is gone or the price has left its range (GME's pool is ~$6k, most likely one concentrated position) it keeps the stock's whole 10% share frozen instead of paid as IMD, for as long as nobody provides real liquidity. Pure griefing (no profit), reversible when real liquidity returns, hence low. Fix: treat a limit too small to buy anything as empty, e.g. `if (poolLimit < MIN_ROUND_IMD) { _fallBackToImd(a, imdIn); continue; }` with a floor such as 1e15 wei (0.001 IMD) or cap / 1000. (Reported by audit_permissions, audit_flow and audit_economics; merged, reproduced.)

**Reproduction**

Same setup as test_recheck2_zeroLiquidityRoundPaidAsImd_noSwap: alice and bob buy 1,000 IMD each (pendingConvert(1) == 6e18), the NVDA pool's LP removes all 1,000,000e18 of liquidity, stockRoundLimit(1) == 0. A griefer adds a full-range position of 2e9 liquidity: stockRoundLimit(1) is now > 0 but < 1e10 wei. Run 100 rounds of convert() one minute apart. Expected (re-check fix 2): each round credits maxConvert()/5 = 4 IMD of the reserve to holders as IMD, so the 6 IMD are paid within two rounds. Actual: the reserve moves less than 1e12 wei in total, owed(0) grows by less than 1e12 wei, pendingConvert(1) stays above 6e18 - 1e12, lastConvert(1) is set every round. forge test --match-path test/scratch/DustLiquidity.t.sol (passes on this code: it asserts the frozen state).

### 5. Low: Inside the 3% oracle tolerance a JIT sandwich of the stock hop is still profitable when a stock pool's in-range depth x fee is below one 4 IMD round

`contracts/src/CompanyToken.sol:646`

```
        if (stockOut < minStockOut(asset, usdOut)) revert PriceOff();
```

The PriceOff check bounds how far from Chainlink a purchase may execute (ORACLE_TOLERANCE_BPS = 300) but does not make the round sandwich-proof; it caps the skim at 3% of each round's stock share. The attack is atomic and self-triggered (convert() is permissionless, once per minute per stock): (1) push the stock's USDG price up by p < tolerance - pool fee; (2) add a narrow JIT position at the pushed tick, which lifts stockRoundLimit (same-transaction depth read) from fee/2 x real depth to the full MAX_ROUND_IMD/5 = 4 IMD; (3) call convert(): the round pays ~4 IMD of USDG into the JIT position at the pushed price and still clears minStockOut; (4) remove the position and swap back. Net gain is about p x (V - fee x D_real) with V = 4 IMD: positive whenever fee x D_real < V, i.e. live in-range USDG depth below ~$390k for the 0.01% NVDA pool, ~$13k for the 0.3% GOOGL/AAPL pools, ~$16k for MSTR (0.25%), ~$3.9k for the 1% GME pool. Live today (fork of Robinhood Chain, 2026-10-07): NVDA limit 474 IMD => ~$93M virtual depth, GME 3.6 IMD => ~$7k, so no pool is exploitable right now, but NVDA's depth comes from concentrated positions whose virtual depth collapses when the price leaves their range, and GME's margin is under 2x. It contradicts AUDIT.md guarantee 4 ('conversion can't be profitably sandwiched') rather than a stated loss bound, and the loss per round is at most 3% of 4 IMD per stock. Lowering the tolerance only scales the skim down and cannot go below the GME pool's 1% fee plus impact. Options: size the per-stock round from the pool's fee tier against a fixed conservative depth floor rather than its same-transaction depth, route NVDA through a higher-fee USDG pool, or document the 3% as the accepted per-round loss bound in AUDIT.md section 6. (Reported by audit_permissions; reproduced.)

**Reproduction**

Mock environment, IMD/USDG 1:1 (4 IMD = 4 USDG), NVDA pool with the mainnet tier (fee 100 = 0.01%, spacing 1) and 20,000 USDG of full-range depth, all feeds $1. alice and bob buy 1,000 IMD each: pendingConvert(1) == 6e18, stockRoundLimit(1) ~ 1 IMD. Warp +1 minute. Attacker (holding 100,000 USDG and 100,000 NVDA, both $1 at the oracle): swap 250 USDG for NVDA (price +2.5%); add liquidity 5,000,000e18 in [tick-1, tick+2] (stockRoundLimit(1) > 4 IMD); call convert(): the full 4 IMD round converts at the pushed price and passes the 97% check; remove the JIT position; swap the pushed NVDA back. Expected (guarantee 4): attacker's USDG + NVDA does not exceed 200,000e18. Actual: 200000047551847129067383, a profit of 0.0476 USDG (1.2% of the round) taken from the NVDA credited to holders. forge test --match-path test/scratch/ToleranceSandwich.t.sol fails with 'sandwich not profitable: 200000047551847129067383 > 200000000000000000000000'.

### 6. Info: GME's 1%-fee pool leaves under 1 point of the 3% oracle tolerance as live margin, so its rounds will often be skipped and its reserve grows without a ceiling

`contracts/src/CompanyToken.sol:135`

```
    uint256 public constant ORACLE_TOLERANCE_BPS = 300;
```

minStockOut() requires stockOut >= 97% of the Chainlink-implied amount, and stockOut is net of the stock pool's own fee. For GME the pool fee is 1% (fee 10_000, spacing 200) and the pool is thin (~$6k), so the pool's effective price sits structurally above the feed. On the live fork today the GME round received 1.198164 GME for 30.144726 USDG against a feed-implied 1.225078 GME (Robinhood GME/USD 24.60735, USDG/USD 1.00004): 97.80% of fair, i.e. 0.80 points above the PriceOff floor (the previous specialist measurement a few hours earlier was 98.31%; the feed moved 0.5%). NVDA/GOOGL/AAPL/MSTR cleared it by 2.4-3.3 points (ratios 1.0028, 0.9935, 0.9996, 0.9959). Any further 0.8% gap between the GME pool and the feed (an after-hours move, a feed heartbeat lag, or a ~$50 trade in a $6k pool) makes every GME round revert PriceOff and skip. A skipped round neither converts nor falls back, so pendingConvert[4] keeps receiving 10% of every holder fee with no ceiling, and when the gap closes it drains at most stockRoundLimit (~3.6 IMD) per minute, credited to whoever holds then (accepted limit 6 of audit 78c00339), not to the holders who earned it. This is the documented 'value waits' behaviour, reported with the measured margin so the requester can decide whether 3% is the intended tolerance for a 1%-fee pool (e.g. apply the tolerance to the pre-fee amount, use a per-stock tolerance of fee + 2%, or pick a deeper GME venue). (Reported by audit_math; re-measured.)

**Reproduction**

FORK_RPC=https://robinhood.drpc.org forge test --mc CompanyForkTest -vvvv (run 2026-10-07, ~1791374022): Converted(asset 4, imdIn 3616432188786722807, usdOut 30144726, stockOut 1198164319145473944); feeds at that block: USDG/USD 100004000, Robinhood GME/USD 2460735000. fair = 30144726 * 100004000 * 1e18 / (2460735000 * 1e6) = 1225078352160634932; minStockOut = 0.97 * fair = 1188326001595815884; stockOut / fair = 0.9780. Unit analogue: in the Company.t.sol setup (1:1 pools, 0.3% fee) set feeds[3] to 0.972e8 and call convert() after 1 minute: out[4] == 0 and pendingConvert(4) stays at 6e18 every round while the gap persists.

### 7. Info: Nothing prevents a second, hookless $COMPANY pool: trades there pay no 4% fee, so 'every swap' and 'blocks other pools' in AUDIT.md overstate the hook

`contracts/src/CompanyHook.sol:489`

```
    function beforeInitialize(address, PoolKey calldata, uint160) external pure returns (bytes4) {
```

AUDIT.md describes the hook as owning 'the token's only Uniswap v4 pool' that 'blocks other pools and outside liquidity', and the brief says it 'takes 4% of every swap'. The hook can only refuse pools whose key names this hook (beforeInitialize / beforeAddLiquidity revert HookNotAllowed, skipped for its own calls). The token has no transfer restriction (the scanner tests require that), so any holder can initialize a $COMPANY/IMD pool with hooks = address(0) (or list the token anywhere else) and provide liquidity; swaps there pay no protocol or holder fee and the routers are not involved. Inherent to fee-by-hook with an unrestricted token; it cannot be fixed without a transfer restriction, which would break the scanner properties. Reported so the documentation and fee-revenue assumptions say what is true: fees are charged on the hook's pool, which holds the locked supply and is therefore the deepest venue, not on every swap of the token. (Reported by audit_flow; reproduced.)

**Reproduction**

Unit setup as in Company.t.sol. alice buys 1,000 IMD of $COMPANY through CompanyRouter; initialize PoolKey(IMD, COMPANY, fee 3000, spacing 60, hooks 0) at the hook pool's current tick and have alice add 1e15 liquidity full range (no revert). bob swaps 100 IMD exact-in through PoolSwapTest on that key. Expected per the brief: 4 IMD of fees (1 protocol, 3 holders). Actual: bob receives $COMPANY and hook.pendingHolderFees(token) and hook.pendingProtocolFees(IMD) are unchanged. forge test --match-path test/scratch/HooklessPool.t.sol (passes on this code: it asserts the behaviour).

---

Judge's submission `bbea7c9424be7558f48f18c6cd2071a87b7e113d736928d39abb7b3bb4b3551e`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
