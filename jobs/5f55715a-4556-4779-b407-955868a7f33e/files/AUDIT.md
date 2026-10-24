# Audit report

> Scope is the msft95-contracts-audit-v2/ folder only. Ignore msft95-casino/, msft95-vault/, msft95-github-upload/ and the older msft95-contracts-audit/ folder. README.md has the scope, roles and file hashes. docs/AUDIT-3.md lists the last review's findings and how each was fixed. Earlier reviews were automated, so treat every fix as unverified.
>
> Mainnet launch on Robinhood Chain (4663, Arbitrum Orbit L2). In scope: contracts/MSFT95Vault.sol, contracts/MSFT95Agents.sol (generated from tools/MSFT95Agents.sol.tpl), v4/MSFT95Token.sol, MSFT95RewardHook.sol, MSFT95Router.sol, MSFT95Staking.sol, MSFT95Vesting.sol, MSFT95AgentFarm.sol, MSFT95AgentStakes.sol (NEW), Create2Deployer.sol. Mocks, test-helpers, WETH9 and vendor/ are out of scope.
>
> LOOK HARDEST AT (new or changed since the last review):
>
> 1. MSFT95AgentStakes (NEW, holds 25% of supply). The core claim: the keeper can never take locked principal, only what has unlocked for agents it names. Try to break it:
>    - The principal() / liquid() / funded / registered / totalReleased accounting.
>    - release() pulling from the stake when liquid is short.
>    - claimRewards() treating MSFT95 above liquid() as a reward. Can the keeper stake/unstake/claim in an order that makes principal look like reward?
>    - Donations of MSFT95.
>    - register() for unminted ids, repeats, and a tier the NFT reports wrongly.
>    - returnUnallocated() racing register().
>    - A keeper who stakes everything and then calls release.
>    - Rounding in unlockedAt.
>    - Reentrancy through staking or the token.
>
> 2. MSFT95RewardHook trading gate (NEW). Can anything move the pool's price before openTrading()? Check direct PoolManager swaps, donate, adding liquidity in a narrow range, and other pools pointing at the hook. Is the NoLiquidity check (getLiquidity at the current tick) enough, or can 1 wei of out-of-range liquidity or a self-added position satisfy it in a harmful way?
>    Also check the new decimals-aware price floor in _fairOut (mulDiv scaling, feed decimals, stale feed).
>
> 3. MSFT95Staking stream change (CHANGED). Rounding leftovers now go to `dust` and join the running stream without moving its end; `idle` (streamed while nobody was staked) still restarts a stream. Check INV: owed + streaming <= held <= balance per token. Can dust/idle be double-counted, lost, or used to time a payout (a large idle landing in a stream with seconds left)? Can anyone still stretch or speed up a stream? Does flash staking still earn 0?
>
> 4. MSFT95AgentFarm hook-flag check (CHANGED). listV4 now rejects farm pools whose hook has add/remove-liquidity flags (0xF03). Is any flag combination still able to block holderRemove or take a cut? Holders must always be able to exit.
>
> 5. Launch script (scripts/mainnet/lib.js, rehearse.js). Order: token, hook, pool (trading closed), route, feed (now required), router, staking, vesting, vault (then excluded from dividends), split, agents, agentStakes (funded), handover. Is there any window where the deployer keeps power or tokens, or where something can be front-run between steps? Are the Safe actions (add liquidity, then openTrading, acceptOwnership) safe if done late or out of order?
>
> ALSO RE-CHECK (unchanged, high value):
> - Hook fee deltas in all four swap shapes.
> - Token dividend accounting with excluded addresses (the vault is now excluded).
> - Vault voucher replay and the daily caps.
> - What a stolen key can take: farm keeper, hook keeper, vault signer.
>
> Please give a PoC test for each High/Medium finding and say which invariant it breaks.

| | |
|---|---|
| Repository | https://github.com/DrTatum/MSFT95.git |
| Commit | `810a96b3fdfaab5710177882c09c5117b4d6d473` |
| Job | `5f55715a-4556-4779-b407-955868a7f33e` |
| Judged | 2026-10-24 06:18 UTC |
| Findings | 1 medium · 4 low · 4 info |

Four agents audited the code as it is at `810a96b`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Medium: openTrading() liquidity gate is satisfied by anyone's 1-wei in-range position, so the audit-3 H-1 fix only holds if the Safe signs 'add liquidity' before 'openTrading'

`msft95-contracts-audit-v2/v4/MSFT95RewardHook.sol:253`

```
        if (poolManager.getLiquidity(poolId) == 0) revert NoLiquidity();
```

The H-1 fix refuses every swap until openTrading(), and openTrading() is meant to make it impossible to open the pool 'while the pool is empty' so the 200M MSFT95 launch position is in before anyone can trade. The hook carries no add-liquidity permission bits, so anyone can call PoolManager.modifyLiquidity on the closed pool, and getLiquidity(poolId) reports only the liquidity active at the current tick: a stranger's position of liquidityDelta 1 around the launch tick makes the check pass. Out-of-range dust does not count (verified: getLiquidity is the active liquidity), so only in-range dust is needed, which costs about 1 wei of each token. The gate therefore enforces 'somebody added something in range', not 'the launch liquidity is in'. The Safe checklist (lib.js safeActions, docs/MAINNET.md lines 70-73) is two separate transactions. If openTrading() is executed first (out-of-order Safe actions, a failed or delayed add, or the deployer, who owns the hook until the Safe accepts, calling it), the pool opens with dust: one MSFT95 sold through the pool moves slot0 to the end of the range for nothing, and the 200M position added afterwards at 'the launch price' is minted at whatever tick the attacker left, which is exactly the H-1 scenario. Invariant broken: 'trading can only open once the launch liquidity is in' (README: 'openTrading(), which requires the pool to have liquidity'; AUDIT-3 H-1). Merged from four specialist reports (audit_flow, audit_economics, audit_permissions, and the economics duplicate). Fix that keeps the design: require getLiquidity(poolId) >= a minimum sized for the launch position (a constant or an openTrading(uint128 minLiquidity) argument), and/or check slot0 still equals the initialization price when opening; operationally, batch add-liquidity and openTrading in one Safe transaction.

**Reproduction**

State: pool initialised by the hook owner at the launch price (tick 0), trading closed, no launch liquidity. 1) Any address calls PoolManager.modifyLiquidity on the pool with tickLower=-60, tickUpper=60, liquidityDelta=1 and settles the two 1-wei deltas; getLiquidity(poolId) == 1. 2) The owner calls openTrading(). Expected: revert NoLiquidity (the launch position is not in). Actual: tradingOpen becomes true, TradingOpened emitted. 3) The stranger sells 1e18 MSFT95 with sqrtPriceLimit at the range edge: slot0.sqrtPriceX96 moves from the launch price to TickMath.MIN/MAX_SQRT_PRICE+-1 for ~0 USDG. Run: forge test --match-path test/scratch/HookGateDust.t.sol: both tests fail on this code ('next call did not revert as expected' and '1 MSFT95 moved the opened pool's price to the end of the range') and pass once openTrading requires a minimum liquidity.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import "forge-std/Test.sol";
import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {PoolManager} from "@uniswap/v4-core/src/PoolManager.sol";
import {IPoolManager} from "@uniswap/v4-core/src/interfaces/IPoolManager.sol";
import {IHooks} from "@uniswap/v4-core/src/interfaces/IHooks.sol";
import {PoolKey} from "@uniswap/v4-core/src/types/PoolKey.sol";
import {PoolId, PoolIdLibrary} from "@uniswap/v4-core/src/types/PoolId.sol";
import {Currency} from "@uniswap/v4-core/src/types/Currency.sol";
import {TickMath} from "@uniswap/v4-core/src/libraries/TickMath.sol";
import {StateLibrary} from "@uniswap/v4-core/src/libraries/StateLibrary.sol";
import {ModifyLiquidityParams, SwapParams} from "@uniswap/v4-core/src/types/PoolOperation.sol";
import {PoolModifyLiquidityTest} from "@uniswap/v4-core/src/test/PoolModifyLiquidityTest.sol";
import {PoolSwapTest} from "@uniswap/v4-core/src/test/PoolSwapTest.sol";
import {MSFT95RewardHook} from "msft95-contracts-audit-v2/v4/MSFT95RewardHook.sol";
import {Create2Deployer} from "msft95-contracts-audit-v2/v4/Create2Deployer.sol";

contract PlainToken is ERC20 {
    uint8 private immutable _d;
    constructor(string memory n, uint8 d) ERC20(n, n) { _d = d; }
    function decimals() public view override returns (uint8) { return _d; }
    function mint(address to, uint256 a) external { _mint(to, a); }
}

/// Audit 3 H-1 fix: openTrading() "reverts while the pool has no liquidity", so the Safe can't open an empty pool
/// whose price anyone can then move for free. But anyone may add liquidity to the closed pool, and 1 wei of it in
/// range satisfies the check. If the Safe signs openTrading() before (or without) its 200M launch position, the gate
/// passes on a stranger's dust and the pool opens as good as empty: the attack H-1 describes is back.
contract HookGateDustTest is Test {
    using PoolIdLibrary for PoolKey;
    using StateLibrary for IPoolManager;

    uint160 constant FLAGS = (1 << 13) | (1 << 7) | (1 << 6) | (1 << 3) | (1 << 2);
    uint160 constant MASK = (1 << 14) - 1;

    PoolManager pm;
    PlainToken msft95;
    PlainToken usdg;
    PlainToken msft;
    MSFT95RewardHook hook;
    PoolKey key;
    PoolModifyLiquidityTest lp;
    PoolSwapTest swapper;
    address stranger = address(0x5714);

    function setUp() public {
        pm = new PoolManager(address(this));
        // deploy at fixed-ish order so currency0/currency1 are whatever they are; the hook accepts either order
        msft95 = new PlainToken("MSFT95", 18);
        usdg = new PlainToken("USDG", 6);
        msft = new PlainToken("MSFT", 18);
        Create2Deployer dep = new Create2Deployer();
        bytes memory init = abi.encodePacked(type(MSFT95RewardHook).creationCode,
            abi.encode(IPoolManager(address(pm)), Currency.wrap(address(msft95)), Currency.wrap(address(usdg)), IERC20(address(msft)), address(this), address(0xBEEF)));
        bytes32 h = keccak256(init);
        bytes32 salt; address addr;
        for (uint256 i; i < 200000; i++) {
            salt = bytes32(i);
            addr = address(uint160(uint256(keccak256(abi.encodePacked(bytes1(0xff), address(dep), salt, h)))));
            if (uint160(addr) & MASK == FLAGS && addr.code.length == 0) break;
        }
        hook = MSFT95RewardHook(dep.deploy(salt, init));
        (Currency c0, Currency c1) = address(msft95) < address(usdg)
            ? (Currency.wrap(address(msft95)), Currency.wrap(address(usdg)))
            : (Currency.wrap(address(usdg)), Currency.wrap(address(msft95)));
        key = PoolKey({currency0: c0, currency1: c1, fee: 3000, tickSpacing: 60, hooks: IHooks(address(hook))});
        pm.initialize(key, TickMath.getSqrtPriceAtTick(0));   // the launch price; trading closed
        lp = new PoolModifyLiquidityTest(pm);
        swapper = new PoolSwapTest(pm);
        msft95.mint(stranger, 1e24); usdg.mint(stranger, 1e12);
        vm.startPrank(stranger);
        msft95.approve(address(lp), type(uint256).max); usdg.approve(address(lp), type(uint256).max);
        msft95.approve(address(swapper), type(uint256).max); usdg.approve(address(swapper), type(uint256).max);
        vm.stopPrank();
    }

    function test_strangerDustSatisfiesNoLiquidityGate() public {
        // an empty pool can't be opened: this is the audit 3 H-1 guarantee
        vm.expectRevert(MSFT95RewardHook.NoLiquidity.selector);
        hook.openTrading();

        // a stranger puts 1 wei of liquidity around the current tick, before the Safe has added anything
        vm.prank(stranger);
        lp.modifyLiquidity(key, ModifyLiquidityParams({tickLower: -60, tickUpper: 60, liquidityDelta: 1, salt: 0}), "");
        assertEq(IPoolManager(address(pm)).getLiquidity(key.toId()), 1);

        // INV: the launch liquidity, not a stranger's dust, is what lets trading open. Expected: still NoLiquidity.
        // Actual: openTrading() succeeds on 1 wei, and the first swap moves the price to the end of the range for free.
        vm.expectRevert(MSFT95RewardHook.NoLiquidity.selector);
        hook.openTrading();
    }

    /// the same state, shown from the other side: once opened on dust the price is anyone's
    function test_openedOnDustThePriceMovesForNothing() public {
        vm.prank(stranger);
        lp.modifyLiquidity(key, ModifyLiquidityParams({tickLower: -60, tickUpper: 60, liquidityDelta: 1, salt: 0}), "");
        bool opened;
        try hook.openTrading() { opened = true; } catch {}
        if (!opened) return;   // the fix holds: nothing more to show
        (uint160 before,,,) = IPoolManager(address(pm)).getSlot0(key.toId());
        bool z = Currency.unwrap(key.currency0) == address(msft95);   // sell MSFT95 for USDG
        vm.prank(stranger);
        swapper.swap(key, SwapParams({zeroForOne: z, amountSpecified: -int256(1e18), sqrtPriceLimitX96: z ? TickMath.MIN_SQRT_PRICE + 1 : TickMath.MAX_SQRT_PRICE - 1}),
            PoolSwapTest.TestSettings({takeClaims: false, settleUsingBurn: false}), "");
        (uint160 after_,,,) = IPoolManager(address(pm)).getSlot0(key.toId());
        // one MSFT95 sold into the opened pool moved it from the launch price to the edge of the range
        assertTrue(after_ == before, "1 MSFT95 moved the opened pool's price to the end of the range");
    }
}
```

### 2. Low: Anyone can still stretch a reward stream: a 1-wei transfer of a listed reward token plus sync() restarts the hour with the whole unstreamed remainder, contrary to the audit-3 L-1 claim

`msft95-contracts-audit-v2/v4/MSFT95Staking.sol:151`

```
        rate[token] = (fresh * ACC + back + d + left) / period;
        finish[token] = block.timestamp + period;
```

The v3 change stops rounding dust from moving a stream's end (lines 141-148), and the NatSpec at line 142-143 says a sync 'never stretches a stream past its hour'. That holds only when nothing arrives. Any fresh > 0 takes the full-restart path: `left` (everything still unstreamed) is folded into a new rate and finish = now + period. `fresh` is just balance minus held (minus totalStaked for MSFT95), with no minimum, so any third party can create it by transferring 1 wei of USDC, WETH, MSFT or MSFT95 to the staking contract and calling the public sync()/syncAll(). Repeated every block, the tail of every stream is pushed back each time: with T seconds left and R remaining, one wei plus a sync spreads R over a fresh 3600 s, so payout decays geometrically instead of finishing. Nothing is lost (INV owed + streaming <= held <= balance holds: held only grows by fresh and rate*(finish-now) always equals what was folded in, less the period remainder), flash staking still earns 0 and no path speeds a stream up. Stakers who leave during a stretched stream forfeit what has not streamed to those who stay, so a staker can also grief in their own favour, and a whale that stakes during the stretch earns a share of rewards that had arrived before it staked. Merged from audit_flow, audit_math and audit_permissions. Fix options that keep the design: fold arrivals below a per-token minimum into the running stream the way dust is (rate += fresh*ACC/rest without moving finish), or only move finish when fresh is at least some fraction of left, or blend the end as a weighted average.

**Reproduction**

alice stakes 10e18 MSFT95. 3600e6 USDC arrives and sync(usdc) sets rate = 1e6*1e36/s, finish = t0+3600. At t0+1800 a griefer transfers 1 wei USDC to the staking contract and calls sync(usdc). Expected (per the line-143 comment and AUDIT-3 L-1): finish still t0+3600 and alice's claimable at t0+3600 is ~3600e6. Actual: left = 1800e6*1e36, rate = (1e36 + left)/3600, finish = t0+5400; at t0+3600 alice's claimable is ~2700e6 and the rest streams until t0+5400. Run: forge test --match-path test/scratch/StakingStreamStretch.t.sol: fails with '1 wei moved the end of the stream by half an hour: 5401 != 3601'.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import "forge-std/Test.sol";
import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {MSFT95Staking} from "msft95-contracts-audit-v2/v4/MSFT95Staking.sol";

contract PlainToken is ERC20 {
    uint8 private immutable _d;
    constructor(string memory n, uint8 d) ERC20(n, n) { _d = d; }
    function decimals() public view override returns (uint8) { return _d; }
    function mint(address to, uint256 a) external { _mint(to, a); }
}

/// Audit 3 L-1 claims "a sync never stretches a stream past its hour". Anyone can still do it: a 1 wei transfer of a
/// listed reward token to the staking contract is a "fresh" arrival, and every arrival restarts the one-hour stream
/// with everything still unstreamed folded in. The griefer pays 1 wei per restart.
contract StakingStreamStretchTest is Test {
    PlainToken stakeToken;
    PlainToken usdc;
    MSFT95Staking staking;
    address alice = address(0xA11CE);
    address griefer = address(0x6B1E);

    function setUp() public {
        stakeToken = new PlainToken("MSFT95", 18);
        usdc = new PlainToken("USDC", 6);
        address[] memory rewards = new address[](1);
        rewards[0] = address(usdc);
        staking = new MSFT95Staking(stakeToken, address(this), rewards);
        stakeToken.mint(alice, 10e18);
        vm.startPrank(alice);
        stakeToken.approve(address(staking), type(uint256).max);
        staking.stake(10e18);
        vm.stopPrank();
    }

    function test_oneWeiArrivalDoesNotMoveStreamEnd() public {
        uint256 t0 = block.timestamp;
        // the casino pays 3600 USDC: it should stream out by t0 + 1 hour
        usdc.mint(address(staking), 3600e6);
        staking.sync(address(usdc));
        assertEq(staking.finish(address(usdc)), t0 + 1 hours);

        // half way through, a griefer drops 1 wei of USDC on the contract and syncs
        vm.warp(t0 + 30 minutes);
        usdc.mint(griefer, 1);
        vm.prank(griefer);
        usdc.transfer(address(staking), 1);
        staking.sync(address(usdc));

        // INV (audit 3 L-1): the stream's end does not move for anything but a real arrival of rewards
        assertEq(staking.finish(address(usdc)), t0 + 1 hours, "1 wei moved the end of the stream by half an hour");

        // and at the original end alice should have essentially all 3600 USDC
        vm.warp(t0 + 1 hours);
        (, uint256[] memory amounts) = staking.claimable(alice);
        assertGe(amounts[0], 3599e6, "alice got only ~2700 USDC by the hour: the rest was pushed into a new hour");
    }
}
```

### 3. Low: claimToken() skips the holder-MSFT harvest that stake(), unstake() and claim() perform, so a per-token MSFT claim can pay less than claim() at the same moment

`msft95-contracts-audit-v2/v4/MSFT95Staking.sol:108`

```
    function claimToken(address token) external nonReentrant {
        _syncAll();
```

stake(), unstake() and claim() call _harvest() first, which pulls the MSFT the staked MSFT95 has earned as an MSFT95 holder into the contract so sync(msft) can start streaming it. claimToken() calls only _syncAll(), so MSFT distributed since the last harvest is still sitting in MSFT95Token.claimable(staking) when the caller is settled: no stream starts and claimToken(msft) pays less than claim() would from that second on. Nothing is lost: the next stake/unstake/claim/harvestHolderRewards pulls it and streams it to whoever is staked then, which favours later stakers over the one who used claimToken. Reported by audit_permissions; reproduced with a test. Fix: call _harvest() at the start of claimToken() as well (one try/catch call).

**Reproduction**

alice holds the whole 1e9 MSFT95 supply and stakes 5e8 (so the staking contract is an eligible holder of half the supply; MSFT is the only listed reward). Someone calls MSFT95Token.distribute(100e18 MSFT): msft95.claimable(staking) == ~50e18. alice calls staking.claimToken(msft). Expected: the 50 MSFT is harvested and starts streaming (streaming(msft).remaining > 0), as it would after claim(). Actual: msft.balanceOf(staking) == 0 and streaming(msft).remaining == 0; a later claim() harvests and starts the stream. Run: forge test --match-path test/scratch/ClaimTokenHarvest.t.sol: fails with 'claimToken did not harvest the holder MSFT: no stream started'.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import "forge-std/Test.sol";
import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {MSFT95Staking} from "msft95-contracts-audit-v2/v4/MSFT95Staking.sol";
import {MSFT95Token} from "msft95-contracts-audit-v2/v4/MSFT95Token.sol";

contract PlainToken is ERC20 {
    constructor() ERC20("MSFT", "MSFT") {}
    function mint(address to, uint256 a) external { _mint(to, a); }
}

/// stake(), unstake() and claim() harvest the MSFT the staked MSFT95 has earned as a holder before settling, so the
/// stream of that MSFT starts at once. claimToken() skips the harvest: the MSFT distributed since the last harvest is
/// not in the contract when the caller is settled, and its stream does not start until some other path harvests.
/// Fails on the current code (no stream after claimToken), passes once claimToken() calls _harvest() like claim() does.
contract ClaimTokenHarvestTest is Test {
    PlainToken msft;
    MSFT95Token msft95;
    MSFT95Staking staking;
    address alice = address(0xA11CE);

    function setUp() public {
        msft = new PlainToken();
        address[] memory none;
        msft95 = new MSFT95Token("MSFT95", "MSFT95", 1_000_000_000e18, alice, IERC20(address(msft)), address(this), none);
        address[] memory rewards = new address[](1);
        rewards[0] = address(msft);
        staking = new MSFT95Staking(IERC20(address(msft95)), address(this), rewards);
        vm.startPrank(alice);
        msft95.approve(address(staking), type(uint256).max);
        staking.stake(500_000_000e18);   // half the supply staked: the staking contract earns half of every MSFT distribution
        vm.stopPrank();
    }

    function test_claimTokenHarvestsLikeClaim() public {
        msft.mint(address(this), 100e18);
        msft.approve(address(msft95), 100e18);
        msft95.distribute(100e18);
        assertApproxEqAbs(msft95.claimable(address(staking)), 50e18, 1);

        vm.prank(alice);
        staking.claimToken(address(msft));

        // INV: any claim path brings the holder MSFT in and starts its stream (claim() does exactly this)
        (uint256 remaining, ) = staking.streaming(address(msft));
        assertGt(remaining, 0, "claimToken did not harvest the holder MSFT: no stream started");
        assertApproxEqAbs(msft.balanceOf(address(staking)), 50e18, 1, "holder MSFT still sits unclaimed in the token");
    }
}
```

### 4. Low: Hook price floor ignores the Robinhood stock feed's oraclePaused() flag (and the sequencer feed), unlike the farm's feedPrice

`msft95-contracts-audit-v2/v4/MSFT95RewardHook.sol:235`

```
        if (px <= 0 || block.timestamp - at > feedMaxAge) revert FeedStale();   // markets closed: the fees wait
```

MSFT95AgentFarm.feedPrice (v4/MSFT95AgentFarm.sol lines 189-196) treats an answer as not fresh when the Robinhood stock feed reports oraclePaused() == true (the pauses around splits, dividends, halts) and when the L2 sequencer uptime feed says the chain is down or just back. MSFT95RewardHook._fairOut, which exists to bound what a stolen keeper key can lose on convert, only checks the sign and the updatedAt age (3 h default). During a pause the feed's last answer stays within feedMaxAge, so for up to 3 h the keeper (or a stolen keeper key) can convert at a floor derived from a pre-event price: around a 2:1 split the floor is ~2x too lenient (half the MSFT the fees are worth), or in the other direction honest conversions are blocked. Bounded by maxSlipBps plus the price move during the pause, and it needs a keeper acting inside the window, so low. Reported by audit_math; reproduced by code comparison of the two feed readers. Fix: in _fairOut staticcall oraclePaused() as the farm does and treat true as FeedStale; optionally share the farm's sequencer check.

**Reproduction**

State: hook with msftFeed set, feedMaxAge = 3 h. The feed returns answer = 500e8, updatedAt = now - 1 h, and oraclePaused() == true because the stock is halted; the real market price has moved to 450 (or the stock has split to 250). Keeper calls convert(amountIn, 0). Expected (same policy as the farm, line 190-191): revert FeedStale, the fees wait. Actual: _fairOut returns amountIn/500 * 0.97 and the swap goes through against a route pool at whatever price it shows, down to that floor; the farm would have refused the same feed state.

### 5. Low: Launch script validates HOOK_KEEPER, SIGNER/COSIGNER/GUARDIAN, MSFT_FEED and STAKE_KEEPER only inside the step that uses them, after earlier steps have already moved supply and left the deployer as ow

`msft95-contracts-audit-v2/scripts/mainnet/lib.js:47`

```
    HOOK_KEEPER: env.HOOK_KEEPER, STAKE_KEEPER: env.STAKE_KEEPER,
```

config() reads HOOK_KEEPER, STAKE_KEEPER, SIGNER, COSIGNER and GUARDIAN without checking them (line 47-48); only SAFE is validated up front. Each is checked inside the step that needs it: HOOK_KEEPER in hook (line 120, after the token has been minted to the deployer), MSFT_FEED in feed (line 146, after token, hook, pool and route), SIGNER/COSIGNER/GUARDIAN in vault (line 178, after staking and vesting are deployed and 50M MSFT95 staked), STAKE_KEEPER in agentStakes (line 230, after split has funded the vault with 250,032,300 MSFT95 and paid treasury and LP). Steps before the failing one are recorded as done and the run aborts. For a missing STAKE_KEEPER that leaves the agents' 249,967,700 MSFT95 (25% of supply) in the deployer EOA (split deliberately leaves it there for agentStakes to pick up) with the deployer still owner of the token and hook, because handover never runs, until an operator fixes the env and re-runs. This is the window the brief asks about: a hot deployer key holding 25% of supply and both Ownable2Step owners for an unbounded time. Reported by audit_economics; reproduced by tracing config() and the step order. Fix: validate every required address (SAFE, HOOK_KEEPER, STAKE_KEEPER, SIGNER, COSIGNER, GUARDIAN, and MSFT_FEED unless ALLOW_NO_FEED) in config() before the first transaction, and check AGENT_STAKE_TIERS there too.

**Reproduction**

Run launch.js on chain 4663 with SAFE, HOOK_KEEPER, SIGNER, COSIGNER, GUARDIAN and MSFT_FEED set and STAKE_KEEPER unset. Expected: the script refuses to start. Actual (by the step order in makeLaunch: chain, token, hook, pool, route, feed, router, staking, vesting, vault, split, agents, agentStakes, handover): every step through agents succeeds and is written to deployments/<net>Launch.json; agentStakes throws 'Set STAKE_KEEPER (the server's agent-stake keeper address)'; afterwards msft95.balanceOf(deployer) == 249,967,700e18, MSFT95Token.owner() == deployer and MSFT95RewardHook.owner() == deployer with no pending transfer to the Safe. The same shape applies to a missing MSFT_FEED (fails after pool and route) and missing SIGNER/COSIGNER/GUARDIAN (fails after vesting has staked 50M).

### 6. Info: Hook convert: a partial fill on a later route hop leaves the intermediate currency unsettled, so the whole conversion reverts with CurrencyNotSettled

`msft95-contracts-audit-v2/v4/MSFT95RewardHook.sol:218`

```
            amount = uint256(uint128(recv));
```

unlockCallback chains exact-input swaps hop by hop and settles only the first-hop input (`spent`) and the last-hop output (`amount`). Each swap runs to the pool's price limit, so a hop whose pool lacks depth fills partially. For hop 0 that is handled (spent is what was actually paid). For hop i >= 1 the hook keeps a positive delta in the intermediate currency equal to recv(i-1) - paid(i) that is never taken, so PoolManager.unlock reverts with CurrencyNotSettled and convert fails until the keeper lowers amountIn or the owner resets the route. No funds are lost (atomic revert), and the single-hop USDG/MSFT route planned for mainnet is unaffected. Reported by audit_math; reproduced by tracing the delta accounting. Fix: track paid per hop and, when paid < amount for i >= 1, take the leftover intermediate currency to the hook or revert with a descriptive error.

**Reproduction**

State: route = [USDG/WETH, WETH/MSFT], the WETH/MSFT pool holds liquidity worth 1 WETH. convert(10_000e6 USDG, 0): hop 0 pays 10,000 USDG and receives 4 WETH; hop 1 can only sell 1 WETH before reaching MIN_SQRT_PRICE+1 (paid = 1 WETH), so 3 WETH remain as a positive delta owed to the hook. Expected: either the leftover is taken into the hook or a descriptive revert. Actual: unlock reverts with CurrencyNotSettled, and the keeper has to guess a smaller amountIn.

### 7. Info: AgentStakes can only forward tokens that Staking lists as rewards; MSFT (if ever unlisted) or any other token that lands there is unrecoverable

`msft95-contracts-audit-v2/v4/MSFT95AgentStakes.sol:162`

```
        address[] memory ts = staking.rewardTokenList();
```

claimRewards() pulls the MSFT95 holder dividend with IHolder(token).claim() and then forwards only the tokens in staking.rewardTokenList(). The launch lists MSFT in Staking, so today this works, but the dependency is implicit: if MSFT is ever not in that list (a Staking redeploy with a different list, or MAX_REWARD_TOKENS reached first), the MSFT dividend on the agents' 25% accumulates here with no function able to move it; the same holds for any other token sent here by mistake (there is no rescue, and returnUnallocated only moves MSFT95). Not a loss of principal. Reported by audit_permissions; reproduced by code reading. Fix: forward the token's own reward() asset explicitly in claimRewards(), and/or add an owner rescue for tokens other than MSFT95.

**Reproduction**

Deploy Staking with rewards=[USDC] only, AgentStakes pointing at it, fund it. Call MSFT95Token.distribute(1000e18 MSFT). Keeper calls claimRewards(): IHolder.claim() moves AgentStakes' MSFT share into the contract, the loop over rewardTokenList never sees MSFT, and msft.balanceOf(agentStakes) stays > 0 with no function able to move it.

### 8. Info: returnUnallocated() can be front-run by a permissionless register(), making the Safe's precomputed amount revert with TooMuch

`msft95-contracts-audit-v2/v4/MSFT95AgentStakes.sol:188`

```
        if (amount > funded - registered || amount > liquid()) revert TooMuch();
```

register() is permissionless and increases `registered` for any minted agent, while the owner's returnUnallocated() is bounded by funded - registered at execution time. Anyone who sees the Safe's transaction can register minted-but-unregistered agents first so that funded - registered < amount and the return reverts. The outcome is correct in substance (a minted agent is owed its allocation), so this is a runbook note: compute the amount from on-chain state at execution, or expect to resend. The rest of the accounting (principal = funded - totalReleased, liquid = principal - staked, register bounded by funded, release pulling the shortfall from the stake, claimRewards counting only balance above liquid as reward, unlockedAt flooring with the full amount at the last step, duplicate and unminted ids, nonReentrant on every keeper path) was traced through stake/unstake/release/claim/donate/return sequences and no path lets the keeper or owner take locked principal. Reported by audit_math; reproduced by code reading. Additionally checked with a 400-run Foundry fuzz (test/scratch/AgentStakesInvariant.t.sol: random 24-step sequences of register/stake/unstake/release/claimRewards/donate/returnUnallocated/fund/reward arrivals/MSFT distributions) asserting staked <= principal, balance >= liquid and balance + staked >= registered - totalReleased after every step: no violation.

**Reproduction**

State: funded = 100, agents A and B minted, only A registered (registered = 50). The Safe submits returnUnallocated(to, 50). Before it executes, anyone calls register([B]): registered = 100. Expected by the Safe: 50 returned. Actual: amount > funded - registered (50 > 0) reverts TooMuch; the tokens stay allocated to B and the Safe must recompute.

### 9. Info: MSFT95 sent to MSFT95AgentStakes outside fund() is treated as reward and forwarded to the hot keeper key; MSFT95 rewards cannot be re-staked

`msft95-contracts-audit-v2/v4/MSFT95AgentStakes.sol:169`

```
                uint256 held = liquid();                // the MSFT95 here that is principal stays
                b = b > held ? b - held : 0;
```

claimRewards defines the MSFT95 reward as balance minus liquid(). liquid() = funded - totalReleased - staked, so principal is protected (after any sequence of fund/stake/unstake/release/returnUnallocated/claimRewards, balance >= liquid() and staked <= principal), but every other MSFT95 that lands here, including a donation or a transfer sent to the wrong address, becomes the keeper's to take, and it cannot be staked because stake() caps amount at liquid(). This matches the documented design (the keeper shares rewards) and does not break the custody claim. Trust note on the keeper, verified: a stolen keeper key can release every unlocked amount to itself, claim every reward in flight, unstake the whole stake (stopping the agents' yield until the Safe rotates the keeper) and stake everything so liquid() == 0, which makes returnUnallocated revert until the Safe calls setKeeper and the new keeper unstakes. None of these reach locked principal. Merged from audit_economics and audit_permissions.

**Reproduction**

fund(100e18); register one agent of allocation 100e18; a third party transfers 5e18 MSFT95 directly to the contract. keeper calls claimRewards(). Expected by a strict 'rewards only' reading: only staking rewards leave. Actual: 5e18 MSFT95 is sent to the keeper (balance 105e18, liquid 100e18, b = 5e18); principal() == 100e18 and balance >= liquid() still hold. Keeper powers: keeper calls stake(funded) so liquid() == 0; owner's returnUnallocated(to, 1) reverts TooMuch although funded - registered > 0, until setKeeper(K2) and K2.unstake(x).

---

Judge's submission `5a39d1c899d7db494dc224e655e8576fb10f4cb34728f3b01505ad7589a1482d`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
