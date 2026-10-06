# Audit report

> Project: PepesFamily launchpad v4
> Repo: github.com/0xtenang/PepesFamily (commit 9a32f89)
> Scope: contracts/src/PepesFamily.sol, contracts/src/PadToken.sol, contracts/src/PepesBuyback.sol. The routers are unchanged from v3 (audited).
> Tests: contracts/test/PepesFamily.t.sol, contracts/test/Fork.t.sol, contracts/test/EthRouter.fork.t.sol
> Chain: Robinhood Chain (4663), Uniswap v4
>
> What changed from v3 (v3 audit: job a3e708e2)
>
> IMD-only launches.
> Reward expiry in PadToken. A wallet is active when it claims, sends, pulls tokens itself, receives ≥ ACTIVITY_MIN (10,000 tokens) or receives for the first time. After more than 7 days of inactivity, unclaimed rewards expire, except those earned in the last 7 days. This is computed with time checkpoints of magnifiedDividendPerShare, the same design as our audited $EARN token (jobs e6eda4d8, f6d3cd0e, a58eb2c6). Anyone can recycle(holder), which only moves expired rewards to PepesBuyback.
> PepesBuyback: one ownerless contract shared by all v4 tokens. Anyone, at most once an hour, at most 1% of the $PEPES pool's IMD depth per call, buys $PEPES via the PepesFamily v1 router and sends it all to 0x…dEaD.
> Please check
>
> Can recycle ever take rewards earned in the last 7 days, or more than a holder is owed? Is the token always solvent (IMD balance ≥ accountedBalance)?
> Can anyone reset another wallet's timer cheaply, or make an active wallet look inactive?
> Interaction with the v3 flash-borrow guard: can flash-held pool tokens affect expiry, recycling or distribution?
> Can the buyback be sandwiched profitably, including together with the $EARN buyback (2% cap, separate contract) in the same transaction?
> Can IMD leave PepesBuyback any way other than the burn swap? Can it be locked or griefed (e.g. maxBuyback returning 0, the v1 router reverting)?
> Gas and limits: checkpoints grow with every distribution. Is the binary search safe for long-lived tokens? Can recycleMany be abused?
> Anything in the IMD-only or constructor changes that breaks v3's guarantees: locked liquidity, the 4% fee on every router, routers compatible.

| | |
|---|---|
| Repository | https://github.com/0xtenang/PepesFamily.git |
| Commit | `9a32f8964a3e455bae7aee717cbe55de97186f4e` |
| Job | `ec4e3ea7-9b37-4113-ae4d-8cdd5ea19424` |
| Judged | 2026-10-06 11:18 UTC |
| Findings | 3 low · 4 info |

Four agents audited the code as it is at `9a32f89`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Low: Paced buyback is front-runnable for profit across hours: the per-call cap defeats an atomic sandwich, not a predictable series of hourly buys

`contracts/src/PepesBuyback.sol:85`

```
        if (block.timestamp < lastBuyback + BUYBACK_INTERVAL) revert TooSoon();
        uint256 imdIn = imd.balanceOf(address(this));
        uint256 cap = maxBuyback();
        if (imdIn > cap) imdIn = cap;
        if (imdIn == 0) revert BadAmount();
```

buybackAndBurnPepes is permissionless and, whenever the reserve holds more than one cap, always spends exactly min(reserve, 1% of the $Pepes pool's IMD depth) at the market price (minPepesOut is the caller's, usually 0). The only pacing is one call per hour (line 85), so the whole flow is public and predictable. The 4% quote-side fee each way does make a single-transaction sandwich lose (confirmed: with a 1% buy, or 1% plus a 2% $EARN-sized buy in the same transaction, the best front-run over a sweep of sizes loses; break-even is a single-transaction buy of roughly 4.0 to 4.5% of depth). But a trader who buys $Pepes once, triggers the buyback at every hour and sells at the end pays the 8% round trip once while the buyback moves the price ~1% per hour in their favour, and the cap itself grows with the depth their own buy added. The buyback therefore buys at a price the front-runner inflated and burns fewer $Pepes; the difference goes to the front-runner. This is inherent to any predictable on-chain buyer and the trader carries hours of price risk with capital of about 40% of depth, so it is rated low rather than medium, but it means the comment's claim (lines 44-46) and README ('a buyback sandwich that loses money') hold only for the atomic case. The requester asked this question directly. Merged from audit_math (medium). Fix options that keep the design: skip or shrink a buyback when the pool price has risen more than X% since the previous buyback (reference price = sqrtPrice recorded at the last call), or jitter the earliest allowed time so the series is not exactly predictable. At minimum, correct the comment and README.

**Reproduction**

Unit test on a PepesFamily pool standing in for the v1 $Pepes pool (same 4% hook fee, same single-sided curve): pool depth ~1,060 IMD after a 1,000 IMD buy; PepesBuyback holds 212 IMD (20% of depth) of recycled rewards. Eve: routerA.buy(pepes, 424 IMD) (40% of depth); eight times {warp +1 hour; buyback.buybackAndBurnPepes(0, now)}; routerA.sell(pepes, all). Expected (per the contract comment and README): Eve ends with less IMD than she started with. Actual: Eve starts with 10,000 IMD and ends with 10,021.48 IMD (+21.48 IMD, about 18% of the 121.37 IMD the buyback spent). The same sequence with one call and no waiting loses, so the per-call cap is not the binding constraint. Run: forge test --match-path test/scratch/Proof_431d.t.sol (fails on this code with 'front-running the paced buyback must not be profitable').

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {PoolManager} from "v4-core/src/PoolManager.sol";

import {PepesFamily} from "src/PepesFamily.sol";
import {PepesFamilyRouter} from "src/PepesFamilyRouter.sol";
import {PepesBuyback} from "src/PepesBuyback.sol";
import {PadToken} from "src/PadToken.sol";

contract MockIMD {
    string public name = "IMD";
    string public symbol = "IMD";
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

/// @notice The $Pepes pool is modelled by a PepesFamily launch (same 4% quote-side hook fee and single-sided
///         curve as the v1 pad, whose FEE_BPS is 400 on chain). A second PepesFamily instance points its
///         PepesBuyback at that token and that router, exactly as production points at the v1 router.
contract BuybackFrontrunTest is Test {
    uint160 constant FLAGS = uint160((1 << 13) | (1 << 11) | (1 << 7) | (1 << 6) | (1 << 3) | (1 << 2));

    PoolManager pm;
    MockIMD imd;
    PepesFamily padA; // stands in for v1: hosts the $Pepes pool
    PepesFamilyRouter routerA;
    PadToken pepes;
    PepesFamily padB; // v4: its PepesBuyback buys `pepes` through routerA
    PepesBuyback buyback;

    address eve = makeAddr("eve");
    address bob = makeAddr("bob");

    function setUp() public {
        vm.warp(1_800_000_000);
        pm = new PoolManager(address(this));
        imd = new MockIMD();
        padA = _deployPad(address(1), address(2));
        routerA = PepesFamilyRouter(payable(padA.router()));
        pepes = PadToken(payable(padA.launch("Pepes", "PEPES", "", address(imd))));
        padB = _deployPad(address(pepes), address(routerA));
        buyback = PepesBuyback(padB.buyback());

        // a $Pepes pool with some depth: bob bought in earlier (virtual IMD depth ~1,060 IMD)
        imd.mint(bob, 10_000e18);
        vm.startPrank(bob);
        imd.approve(address(routerA), type(uint256).max);
        routerA.buy(address(pepes), 1_000e18, 0, block.timestamp);
        vm.stopPrank();

        imd.mint(eve, 10_000e18);
        vm.startPrank(eve);
        imd.approve(address(routerA), type(uint256).max);
        pepes.approve(address(routerA), type(uint256).max);
        vm.stopPrank();
    }

    function _deployPad(address pepes_, address pepesRouter_) internal returns (PepesFamily) {
        int24 tick = 161200; // ~100 IMD launch market cap (1e7 tokens per IMD)
        bytes memory initCode = abi.encodePacked(
            type(PepesFamily).creationCode,
            abi.encode(
                pm,
                address(imd),
                address(this),
                address(this),
                tick,
                PepesFamily.ImdEthPool(10_000, 100, address(0)),
                pepes_,
                pepesRouter_
            )
        );
        bytes32 salt;
        address predicted;
        for (uint256 i;; i++) {
            salt = bytes32(i);
            predicted = address(
                uint160(uint256(keccak256(abi.encodePacked(bytes1(0xff), address(this), salt, keccak256(initCode)))))
            );
            if (uint160(predicted) & 0x3FFF == FLAGS) break;
        }
        address deployed;
        assembly {
            deployed := create2(0, add(initCode, 0x20), mload(initCode), salt)
        }
        require(deployed == predicted, "hook address");
        return PepesFamily(deployed);
    }

    /// Eve buys 40% of the pool's IMD depth, calls the capped buyback at every hour for 8 hours (anyone may),
    /// then sells. Each call is capped at 1% of depth and loses money if sandwiched atomically, but the hourly
    /// pace makes the flow predictable: the price moves ~1%/hour in her favour while her round trip costs 8%.
    /// With a reserve of 20% of depth she exits with more IMD than she started with.
    function test_pacedBuybackCannotBeFrontRunForProfit() public {
        uint256 depth = buyback.maxBuyback() * 100;
        imd.mint(address(buyback), depth / 5);
        uint256 start = imd.balanceOf(eve);

        vm.startPrank(eve);
        uint256 got = routerA.buy(address(pepes), depth * 40 / 100, 0, block.timestamp);
        for (uint256 h; h < 8; h++) {
            vm.warp(block.timestamp + 1 hours);
            buyback.buybackAndBurnPepes(0, block.timestamp);
        }
        routerA.sell(address(pepes), got, 0, block.timestamp);
        vm.stopPrank();

        uint256 end = imd.balanceOf(eve);
        emit log_named_decimal_uint("pool virtual IMD depth", depth, 18);
        emit log_named_decimal_uint("eve start IMD", start, 18);
        emit log_named_decimal_uint("eve end IMD", end, 18);
        emit log_named_decimal_uint("IMD spent by the buyback", buyback.totalImdSpent(), 18);
        assertLe(end, start, "front-running the paced buyback must not be profitable");
    }
}
```

### 2. Low: PepesBuyback burns only the swap delta: $Pepes sent to it directly is locked forever and accrues v1 holder dividends nobody can claim

`contracts/src/PepesBuyback.sol:95`

```
        burned = pepes.balanceOf(address(this)) - before;
        pepes.transferOut(DEAD, burned);
```

buybackAndBurnPepes snapshots the $Pepes balance before the swap and sends only `after - before` to 0x...dEaD. The contract has no owner and no other function that moves $Pepes, so any $Pepes that reaches it by a plain transfer (a user assuming 'send $Pepes here to burn it', an airdrop, griefing dust) stays in `before` on every later call and never leaves, contrary to the NatSpec 'sends all of it to the burn address'. Because PepesBuyback is not in PadTokenV1's immutable exclusion list (PoolManager, pad, router, token, 0x0, dEaD), a stranded balance keeps earning its pro-rata share of every future 3% $Pepes holder fee inside the $Pepes token contract, and PadTokenV1.claim() pays only msg.sender, which PepesBuyback can never be; that IMD is lost to all other $Pepes holders. The IMD side spends the whole balance (`imdIn = imd.balanceOf(address(this))`) while the $Pepes side spends only the delta, an asymmetry with no reason behind it. Merged from four specialists (audit_math, audit_flow, audit_economics, audit_permissions), identical mechanism and fix. Fix: after the swap, `burned = pepes.balanceOf(address(this)); pepes.transferOut(DEAD, burned);` so direct sends are burned on the next call (totalPepesBurned then also counts donations, which is the desired accounting).

**Reproduction**

pepes.mint(buyback, 5e18) (any direct transfer of 5 $Pepes to the buyback); imd.mint(buyback, 1e18); buyback.buybackAndBurnPepes(0, now). Expected: pepes.balanceOf(buyback) == 0 and the burn address received the 5 $Pepes with the bought ones. Actual: burned equals only the swap output and pepes.balanceOf(buyback) == 5e18 afterwards, permanently. Run: forge test --match-path test/scratch/Proof_4a52.t.sol (fails on this code with 'stray $Pepes stay locked in the buyback forever: 5000000000000000000 != 0'). The v1 dividend part follows from reading src/v1/PadTokenV1.sol: isExcluded (lines 140-143) does not cover the buyback and claim() (line 173) pays msg.sender only.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {PoolManager} from "v4-core/src/PoolManager.sol";
import {PoolModifyLiquidityTest} from "v4-core/src/test/PoolModifyLiquidityTest.sol";
import {TickMath} from "v4-core/src/libraries/TickMath.sol";
import {PoolKey} from "v4-core/src/types/PoolKey.sol";
import {Currency} from "v4-core/src/types/Currency.sol";
import {IHooks} from "v4-core/src/interfaces/IHooks.sol";
import {ModifyLiquidityParams} from "v4-core/src/types/PoolOperation.sol";

import {PepesBuyback} from "src/PepesBuyback.sol";

contract MockToken {
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

contract MockRouter {
    MockToken imd;
    MockToken pepes;
    PoolKey key;

    constructor(MockToken i, MockToken p) {
        imd = i;
        pepes = p;
    }

    function setKey(PoolKey memory k) external {
        key = k;
    }

    function pad() external view returns (address) {
        return address(this);
    }

    function poolKey(address) external view returns (PoolKey memory) {
        return key;
    }

    function buy(address, uint256 amountIn, uint256, uint256) external payable returns (uint256 out) {
        imd.transferFrom(msg.sender, address(this), amountIn);
        out = amountIn * 1000;
        pepes.mint(msg.sender, out);
    }
}

contract StrayPepesTest is Test {
    address constant DEAD = 0x000000000000000000000000000000000000dEaD;

    function test_pepesSentDirectlyIsNeverBurned() public {
        vm.warp(1_800_000_000);
        PoolManager pm = new PoolManager(address(this));
        MockToken imd = new MockToken();
        MockToken pepes = new MockToken();
        MockRouter r = new MockRouter(imd, pepes);
        PoolModifyLiquidityTest lp = new PoolModifyLiquidityTest(pm);
        pepes.mint(address(this), 100_000e18);
        imd.mint(address(this), 100_000e18);
        pepes.approve(address(lp), type(uint256).max);
        imd.approve(address(lp), type(uint256).max);
        (address c0, address c1) =
            address(pepes) < address(imd) ? (address(pepes), address(imd)) : (address(imd), address(pepes));
        PoolKey memory k = PoolKey(Currency.wrap(c0), Currency.wrap(c1), 3000, 60, IHooks(address(0)));
        pm.initialize(k, TickMath.getSqrtPriceAtTick(0));
        lp.modifyLiquidity(k, ModifyLiquidityParams(-887220, 887220, 1_000e18, 0), "");
        r.setKey(k);
        PepesBuyback b = new PepesBuyback(address(imd), address(pepes), address(r), address(pm));

        pepes.mint(address(b), 5e18); // $Pepes sent straight to the buyback (a donation to the burn)
        imd.mint(address(b), 1e18);
        b.buybackAndBurnPepes(0, block.timestamp);
        assertEq(pepes.balanceOf(address(b)), 0, "stray $Pepes stay locked in the buyback forever");
    }
}
```

### 3. Low: ACTIVITY_MIN is a fixed token count, not a value: genuine small buys at higher market caps are not activity (an actively buying wallet gets recycled) while strangers reset any timer for ~0.001 IMD

`contracts/src/PadToken.sol:229`

```
            if (!toExcluded && (msg.sender == to || amount >= ACTIVITY_MIN || lastActive[to] == 0)) {
                lastActive[to] = block.timestamp;
            }
```

A buy through PepesFamilyRouter, PepesFamilyEthRouter or any v4 router delivers tokens with PoolManager.take, so in _transfer msg.sender is the PoolManager, not the buyer, and the receipt counts as activity only when amount >= ACTIVITY_MIN (10,000 tokens, 0.001% of supply) or it is the wallet's first receipt. The threshold is denominated in tokens, so its IMD value is 1e-5 of the market cap. Two consequences of the one rule. (1) Holder's disfavour: once the market cap passes ~100,000 IMD, a 1 IMD buy yields fewer than 10,000 tokens, so a holder who keeps buying with their own IMD but never claims is 'inactive' from their first buy and anyone can recycle everything older than 7 days, although the wallet traded a day earlier. README and the contract notice equate the threshold with 'any real buy', which holds only at small caps; the suite only tests a 1 IMD buy at a ~100 IMD cap (millions of tokens). (2) Burn's disfavour: a third party can push lastActive[victim] forward at will by sending 10,000 tokens, which costs ~0.0013 IMD at the harness's 120 IMD cap and ~0.0064 IMD at the production 635 IMD start cap; one wallet holding a bag of a cheap token can keep every other holder's rewards perpetually unexpired, defeating the expiry for that token (the NatSpec says the constant 'keeps dust gifts from holding off someone else's expiry for free'). Neither direction harms a holder's claimable balance (lastActive only ever moves forward, see test_lastActiveNeverDecreases) and the holder can always claim or self-transfer, so low. Merged from audit_math, audit_flow, audit_economics and audit_permissions (six findings, two impacts, one root cause). Fix options that keep the gift rule: let the two immutable project routers record the buyer's own buy as activity regardless of size (e.g. a `markActive(buyer)` restricted to router/ethRouter, or treat a receipt from the PoolManager as activity when the trade came through the pad's own routers), and make the third-party receipt threshold value-based (a share of the recipient's balance, or an IMD-equivalent read from the pool price) rather than a fixed count. At minimum document the threshold in IMD terms.

**Reproduction**

test/scratch/Judge.t.sol, JudgeActivityTest (both pass on the current code, showing the behaviour). test_smallRealBuyIsNotActivity: launch at the 100 IMD start cap; bob buys 10 IMD (lastActive = T0); carol buys 5,000 IMD (market cap 241,296 IMD); warp 6 days; bob buys 1 IMD through PepesFamilyRouter and receives 3,977.7 tokens (< 10,000) -> lastActive[bob] == T0 unchanged (expected: now, he just bought); warp 1 day + 1 s; recycle(bob) moves 150.30 IMD of bob's 150.30 IMD owed to the buyback (expected 0: bob traded 25 hours earlier). test_thirdPartyResetsTimerCheaply: carol buys 0.01 IMD and receives 79,984 tokens; warp 6 days; carol.transfer(bob, 10,000e18) -> lastActive[bob] == block.timestamp; cost 0.00125 IMD per reset at a 120 IMD market cap.

### 4. Info: Sandwich-bound comment is wrong: the v4 and $EARN buybacks together expose 3% of depth, not 2%; measured break-even is about 4.0 to 4.5%, and a v1 fee self-rebate narrows that margin as the pool's sha

`contracts/src/PepesBuyback.sol:44`

```
    /// @notice IMD spent per buyback: at most 1% of the $Pepes pool's IMD depth, at most once an hour. Half of the
    ///         $EARN buyback's 2%, so both together stay within the 2%-of-depth bound under which a sandwich costs
    ///         more in the $Pepes pool's 4% fees (each way) than it can move the price.
    uint256 public constant MAX_BUYBACK_BPS = 100;
```

The NatSpec says the 1% cap is 'half of the $EARN buyback's 2%, so both together stay within the 2%-of-depth bound'. 1% + 2% = 3%, and both calls are permissionless with minOut = 0, so an atomic bundle of PepesBuyback.buybackAndBurnPepes followed by PepesEarnToken.buybackAndBurnPepes on the same $Pepes pool buys 3% of depth in one transaction. Measured with the real hook on a PepesFamily pool (same 4% quote-side fee as the live v1 $Pepes pool, FEE_BPS 400 confirmed on chain): a naive attacker paying the full 4% each way loses for every front-run size when the victim buy is up to 4.0% of depth and first profits at 4.5% (+1.04 IMD on a 19,300 IMD pool), so today's 3% bundle is safe with a margin of roughly 1 to 1.5% of depth, and any further anyone-callable buyer on the $Pepes pool above that would cross the line. Lead not reproduced here (needs the v1 PepesFamily pad source, not in this repository): the v1 pad distributes mid-unlock for any caller and PadTokenV1.distribute has no unlock guard (AUDIT.md), so an attacker trading inside its own unlock can flash-take the PoolManager's $Pepes, flush, and claim back (pool share of supply) x 3% of its own fee each way; audit_flow's model puts the 3% bundle at profitable once the PoolManager holds ~40% of supply. Live today the PoolManager holds 1.979e26 of 1e27 $Pepes (~20%), where the specialist's fork test lost money in every configuration, so this is state-dependent and informational. Merged from audit_economics (info) and audit_flow (low, demoted: not reproducible against this tree and unprofitable at the live state). Suggested: fix the comment (3% combined, ~4% break-even), add a unit test that bundles both buybacks, and if the margin matters, make the two contracts refuse to run in the same block (e.g. PepesBuyback checks the $EARN token's lastBuyback != block.timestamp) or lower MAX_BUYBACK_BPS.

**Reproduction**

test/scratch/Judge.t.sol, JudgeSandwichTest. test_stackedAtomicSandwichLoses: pool depth 19,300 IMD; buyback reserve 19,300 IMD; for front-run sizes 0.1% to 50% of depth: eve buys, buyback (1% of post-front-run depth), an unrelated buy of 2% of post-front-run depth in the same transaction (the $EARN stand-in), eve sells; best eve P&L = -0.47 IMD (loss). test_breakEvenSweep: victim buy of 1.0/1.5/.../4.0% of depth -> best attacker P&L -1.17/-1.00/-0.82/-0.65/-0.47/-0.30/-0.12 IMD (all losses); 4.5% -> +1.04 IMD at a 4% front-run; 5% -> +17.8 IMD; 6% -> +115 IMD. Expected per the comment: safe bound at 2%; actual: safe up to ~4%, with the live combined exposure at 3%.

### 5. Info: Buyback wiring (pepes, pepesRouter) is only zero-checked at construction; a mis-wired deployment makes buybackAndBurnPepes revert forever while recycle keeps sending IMD there with no way out

`contracts/src/PepesBuyback.sol:65`

```
        if (imd_ == address(0) || pepes_ == address(0) || pepesRouter_ == address(0) || poolManager_ == address(0)) {
            revert ZeroAddress();
        }
```

PepesFamily's constructor deploys the shared PepesBuyback from two arguments that are checked only for zero. The buyback address is immutable in PepesFamily and in every PadToken it launches; PadToken.recycle transfers IMD to it unconditionally and PepesBuyback has no owner and no path for IMD other than IPepesRouterV1(pepesRouter).buy. If pepesRouter is not a v1-compatible router, pepes is not launched on pepesRouter.pad() (poolKey reverts UnknownToken), the pool is ETH-paired (the v1 router's buy then reverts BadAmount for an IMD-approved call), or imd is neither pool currency (cap computed from the wrong side), buybackAndBurnPepes can never succeed and every v4 token's expired rewards accumulate unrecoverably. PepesEarnIMD.openPool validates the analogous targets; PepesFamily v4 has no equivalent check. Deploy.s.sol hard-codes the live $Pepes 0xE2C4...5644 and v1 router 0xA736...83dC, and the wiring verifies on chain (router.pad() = 0x2d76...68CC, poolKey($Pepes) = (IMD, PEPES, 0, 200, pad), FEE_BPS 400) and in Fork.t.sol, so this is deployment hygiene, not a live defect. Merged from audit_math, audit_flow, audit_economics and audit_permissions. Fix: in PepesBuyback's constructor resolve `IPepesPadV1(IPepesRouterV1(pepesRouter_).pad()).poolKey(pepes_)`, require that one currency is imd_ and that the pool is initialised (sqrtP != 0), so a mis-wired PepesFamily deployment reverts instead of creating a permanent sink.

**Reproduction**

test/scratch/Judge.t.sol, JudgeWiringTest.test_eoaRouterAccepted_thenBuybackBricked (passes, showing the behaviour): deploy PepesFamily with pepes = 0xCAFE and pepesRouter = 0xBEEF (both EOAs). Expected: deployment refused. Actual: it succeeds; launch a token, bob and carol buy 10 IMD each, warp 8 days, recycle(bob) moves bob's IMD into the buyback; buyback.maxBuyback() and buyback.buybackAndBurnPepes(0, now) revert on every call, and the IMD has no other exit.

### 6. Info: maxBuyback() is 0 while the $Pepes pool sits exactly at its launch tick (single-sided position inactive), so the buyback reverts BadAmount until someone buys; IMD waits, nothing is lost

`contracts/src/PepesBuyback.sol:110`

```
        uint256 liquidity = IPoolManager(poolManager).getLiquidity(id);
        uint256 imdDepth = Currency.unwrap(key.currency0) == imd
            ? FullMath.mulDiv(liquidity, Q96, sqrtP) // IMD is currency0: x = L / sqrtP
            : FullMath.mulDiv(liquidity, sqrtP, Q96); // IMD is currency1: y = L * sqrtP
        return (imdDepth * MAX_BUYBACK_BPS) / 10_000;
```

getLiquidity returns the liquidity active at the current tick. The live $Pepes pool has IMD as currency0 and $Pepes as currency1 (confirmed on chain), so its single position runs from MIN_TICK to the launch tick and is inactive when the price is exactly at the launch tick (lower <= tick < upper fails at tick == upper). In that state, which is reached only when every $Pepes has been sold back into the pool, liquidity is 0, maxBuyback() returns 0 and buybackAndBurnPepes reverts BadAmount (line 89) even with a funded reserve. recycle keeps working and the IMD stays in the contract, so this is a liveness corner case rather than a lock: the one state in which the burn cannot run is the one in which nobody holds $Pepes. Today the PoolManager holds ~20% of supply, far from that state. Merged from audit_flow (info). No change required; optionally return early with a clearer error or fall back to the position's liquidity.

**Reproduction**

test/scratch/Judge.t.sol, JudgeWiringTest.test_maxBuybackZeroAtLaunchTick (passes, showing the behaviour): launch a PepesFamily token whose pool has IMD as currency0 (the live $Pepes ordering) and point a PepesBuyback at it before any buy. maxBuyback() == 0; with 1 IMD in the buyback, buybackAndBurnPepes(0, now) reverts BadAmount. After one 1 IMD buy moves the price into range, maxBuyback() > 0. With the opposite ordering (token as currency0) the cap is positive at the launch tick.

### 7. Info: Expiry test coverage: the suite never asserts that recent rewards survive repeated recycles, the all-expires case for a zero-balance holder, un-flushed fees, or sub-threshold receipts; the properties

`contracts/test/PepesFamily.t.sol:840`

```
    function testFuzz_expirySolvent(uint96 a, uint96 b, uint32 gap1, uint32 gap2) public {
        PadToken t = _launch();
        _buy(bob, t, bound(a, 1e15, 500e18));
        vm.warp(block.timestamp + bound(gap1, 0, 20 days));
        _buy(carol, t, bound(b, 1e15, 500e18));
        vm.warp(block.timestamp + bound(gap2, 0, 20 days));
```

The repository's expiry fuzz drives three router buys with two gaps and one recycle. It never (1) recycles the same wallet twice so that rewards cross the 7-day line between calls, (2) recycles a holder whose balance is 0 (sold everything 7+ days ago, so `recent` is 0 and everything older expires), (3) leaves fees pending in the pad from third-party-router swaps and flushes after a recycle, (4) mixes dust gifts (<ACTIVITY_MIN, balance grows without activity) and real gifts with distributions, (5) checks activity through PepesFamilyEthRouter, or (6) checks the buyback against a pool whose active liquidity is 0. The brief's first question (can recycle take rewards earned in the last 7 days, or more than owed; is the token solvent) is therefore not regression-tested. A judge fuzz over 1,500 random sequences of up to 40 actions (buys, half-sells, dust and real gifts, un-flushed external swaps, flushes, claims, self-transfers, warps, recycles), tracking the holder's accumulative dividend after every action to compute the true amount earned in the last 7 days, found no violation: expired <= owed, withdrawable after recycle >= rewards distributed in the last 7 days, IMD balance >= accountedBalance, and recycles only when now > lastActive + 7 days. Across 60 fixed seeds of 40 actions each, 325 recycle calls were made and 39 of the 60 sequences recycled a positive amount, so the path is exercised rather than trivially passing. Not a code defect; recommend adding these properties to test/PepesFamily.t.sol. Merged from audit_permissions (info).

**Reproduction**

test/scratch/ExpiryInvariants.t.sol (all pass): testFuzz_recycleNeverTakesRecentOrMoreThanOwed (1,500 runs; test/scratch/ExpiryStats.t.sol counts the coverage over 60 fixed seeds); test_secondRecycleOnlyTakesAgedRewards: R1 day 0, R2 day 5, recycle day 8 takes R1 only; recycle day 10 takes 0 (R2 is 5 days old); R3 day 10; recycle day 13 takes R2 only and leaves R3. test_zeroBalanceHolderLosesEverythingOld: bob buys day 0, earns, sells all day 1, alice buys day 3 (bob earns nothing), day 8+1s recycle(bob) returns his whole day-0 reward and withdrawableDividendOf(bob) == 0. test_flashHeldTokensDoNotChangeExpiryOrDistribution: inside an attacker's unlock holding the pool's whole token balance, expiredRewardsOf(bob) equals its value outside the unlock, distribute() returns 0, pending fees stay pending, and the flash holder's claim pays 0. Uncovered-case example currently not asserted by the suite: the zero-balance all-expires sequence above.

---

Judge's submission `51451fee74048e31b8ab1cf9718275cd09160e371bc9fea0d3ad491c86c6c3ba`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
