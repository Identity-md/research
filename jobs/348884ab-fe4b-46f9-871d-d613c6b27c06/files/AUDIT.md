# Audit report

> Project: PepesFamily launchpad v4, final check after re-check b803125e
> Repo: github.com/0xtenang/PepesFamily (commit 2560653)
> Scope: contracts/src/PepesFamily.sol, contracts/src/PadToken.sol, contracts/src/PepesBuyback.sol, and contracts/src/PepesFamilyEthRouter.sol (now passes hookData)
> Tests: contracts/test/PepesFamily.t.sol, contracts/test/PepesBuyback.t.sol, contracts/test/Fork.t.sol
>
> Changes since b803125e
>
> Findings 1, 2 and 5: the reference follows only each buyback's own impact (ref × sqrtAfter / sqrtBefore). Otherwise poke() moves it toward spot by at most 2%/day (in price), at most 1 day counted per call. poke is permissionless and runs inside every buyback, and from PadToken.recycle via a low-level call. The guard is a flat 2% band. Minimum buyback is 0.1 IMD. Your proof scenarios are in test/PepesBuyback.t.sol: test_pacedPreBuysDoNotPay, test_idleTimeDoesNotLoosenTheGuard, test_dumpBracketDoesNotStall.
> Finding 3: receipts count as activity only when msg.sender == to or it's the first receipt.
> Finding 4: PepesFamilyEthRouter passes abi.encode(user) as hookData on the token-pool swaps. The hook decodes hookData when sender is router or ethRouter.
> Please check
>
> Can the ratchet be gamed: repeated pokes during a pump, poking around a dip, or the residual after a genuine crash (reference above market)?
> Is the low-level poke call from recycle safe? It should never block recycle.
> Do the ETH-router hookData changes affect anything else, for example the IMD/ETH pool or the Trade event?
> Any regression of earlier findings, or of v3 guarantees.

| | |
|---|---|
| Repository | https://github.com/0xtenang/PepesFamily.git |
| Commit | `25606530e1ef2f5f1b405e743067a6050a646808` |
| Job | `348884ab-fe4b-46f9-871d-d613c6b27c06` |
| Judged | 2026-10-06 15:45 UTC |
| Findings | 2 high · 3 low · 2 info |

Four agents audited the code as it is at `2560653`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. High: The reference keeps every buyback's own impact and comes down only 2%/day, so in ordinary operation (holders selling into the rises) or after any genuine fall it sits above the market and the pump-the

`contracts/src/PepesBuyback.sol:163`

```
        uint160 next = uint160(FullMath.mulDiv(refSqrtPrice, _sqrtPrice(), before));
```

Merged from audit_economics finding 1, audit_permissions finding 2 and audit_math finding 2; all three reproduced.

Root cause. Two rules combine. (1) Every buyback multiplies the reference by its own impact (line 163), about +1.9% in $Pepes price per buyback, up to 24 times a day, whether or not the market keeps that impact. (2) The only force that brings the reference back toward the market is poke(), at most 2% per day (lines 128-131). The guard (line 147) is one-sided: priceRiseBps() is 0 whenever the price is at or below the reference. So whenever the market ends up below the reference, the guard stops binding by the whole gap: a pump of up to (reference/market) x 1.02 passes, and every hourly buyback then buys into it, which is exactly the pump-then-series of audit ec4e3ea7 finding 1 that test_pumpThenSeriesStalls says is prevented.

Two ways to reach that state, neither needing the attacker.
(a) Ordinary operation, no crash (undocumented): a buyback lifts the price ~1.9%, a holder sells into the rise and the price gives the impact back, but the reference keeps it. With hourly buybacks the reference climbs up to ~45%/day in price against a 2%/day pull-down. Reproduced: after one day of 24 buybacks with a holder selling exactly the amount just burned after each (pool depth back at exactly 1,061.908 IMD), the reference sqrtPrice went from ~2.359e31 to 1.912e31, i.e. the reference price is ~52% above the market, and a 20%-of-depth pump still reads priceRiseBps() == 0.
(b) A genuine fall (the README line 85 'residual'): after bob sells 35% of his bag the $Pepes price is well under half the reference. Each buyback rescales the reference by its own impact, so the ratio reference/market is preserved and only poke() closes it, at 2%/day: after a deep fall the window stays open for weeks, and the series keeps running at the low the whole time (guard inert). The longer it is open the more the series spends into a pump: with 24, 72 or 120 hours of honest hourly pokes+buybacks between the fall and eve's half-depth pump, her profit is 53.8, 85.1 and 134.6 IMD. The poke-truncation finding lets an attacker stop the pull-down entirely, and case (a) keeps re-opening the gap without any fall.

Who loses: $Pepes holders. The buyback spends IMD from expired rewards at pumped prices and burns fewer $Pepes (18% fewer per IMD in the economics specialist's crash run); the attacker keeps 11% to 43% of what the series spends, after both 4% fees. The README calls the post-fall state a residual lasting 'until the reference has caught up (2% a day)'; that catch-up takes weeks after a deep fall and the window is profitable the whole time, and in case (a) the reference never catches up while buybacks run.

Fix (design decision, preserves the guard's intent): the reference must not stay above the market. Options verified locally: (1) in poke(), follow a fall in $Pepes price at once and keep the 2%/day only on the way up (orientation: when imdIsCurrency0 a lower $Pepes price is a higher sqrtPrice: `if (imdIsCurrency0 ? cur > ref : cur < ref) next = cur;`). With that one line both proof tests pass (0 buybacks run, eve -16.7 and -12.2 IMD) and all 9 tests in test/PepesBuyback.t.sol still pass; trade-off: a single-transaction dump-poke-rebuy can then pull the reference down by the dump depth and stall the buyback for gap/2% days at the cost of 8% fees on the dumped amount (griefing, no gain; audit b803125e finding 5 class). (2) A bounded faster downward step (e.g. 24x the upward one) fixes case (a) but not a one-day-old deep fall (proof test 2 still fails). (3) Cap what the series may spend per rolling day (e.g. 3% of depth) so that holding a pump across the series costs more in fees than it captures, whatever the reference. (1) or (3), or both, resolve the finding.

**Reproduction**

Setup as test/PepesBuyback.t.sol (launchpad A hosts '$Pepes', bob bought with 1,000 IMD, pool depth ~1,062 IMD, launchpad B's PepesBuyback buys through A's router).
(a) No crash: mint one depth (1,062 IMD) to the buyback; for 24 hours: buybackAndBurnPepes, then bob sells exactly totalPepesBurned delta, warp 1 hour, poke(). Then eve buys 20% of depth, calls buybackAndBurnPepes every hour for 12 hours, sells everything. Expected (test_pumpThenSeriesStalls property): priceRiseBps() > 200 after the pump, 0 buybacks run, eve ends at or below her start. Actual: priceRiseBps() == 0 after the pump, 12 of 12 buybacks run spending 160.18 IMD, eve ends +29.07 IMD.
(b) Crash: mint one depth to the buyback, one buyback (fresh reference), bob sells 35% of his bag, then 24 hours of hourly poke()+buybackAndBurnPepes by honest keepers. eve buys with depth/2, calls the buyback every hour for 24 hours, sells. Expected: stalled, eve loses. Actual: priceRiseBps() == 0 after the half-depth pump, 24 of 24 run spending 123.77 IMD, eve ends +53.79 IMD.
Run: forge test --match-path test/scratch/ReferenceAboveMarketProof.t.sol -vv (both tests fail on commit 2560653; both pass with fix option 1).

### 2. High: poke() truncates its step to whole half-basis-points but always restarts the clock: pokes less than 864 s apart freeze the reference, so anyone (or a busy recycle bot) can stall the buyback indefinite

`contracts/src/PepesBuyback.sol:128`

```
        uint256 h = (REF_STEP_PER_DAY_BPS * dt) / (2 * 1 days);
```

Merged from audit_economics finding 2, audit_flow finding 1, audit_permissions finding 1 and audit_math finding 1; all four reproduced (their four proofs all fail on this code for the stated reason).

Root cause. Line 124 sets refTime = block.timestamp unconditionally, then line 128 computes h = 200 * dt / 172800 = dt / 864 in integer half-basis-points of sqrtPrice. For dt < 864 s, h == 0, lo == hi == ref and the reference does not move, yet the elapsed time has been consumed. Every poke discards dt mod 864 s: pokes every 10 minutes move nothing at all, pokes every 1,727 s follow at half speed, and even the hourly cadence the buyback itself uses gives h = 4 instead of 4.17 (1.92%/day, not 2%). poke() is permissionless and is also run by every PadToken.recycle of every v4 token (PadToken.sol line 329), so the state arises without an attacker whenever recycles land every few minutes, and can be forced by anyone for about 100 cheap transactions a day.

Impact. Once the $Pepes price is more than 2% above the frozen reference (any organic rise, or a pump), buybackAndBurnPepes reverts PriceRisen on every call for as long as the pokes continue; the contract's promise that 'an organic rise or fall is followed at 2% a day' does not hold, and the recycled IMD, which can only leave through the burn swap, accumulates unspent. After a fall the same cadence keeps the reference above the market forever, which holds open the farmable window of the reference-above-market finding. Honest pokes cannot help: they also reset refTime with h == 0.

Fix: do not discard the remainder. Compute the step at full precision, e.g. `uint256 step = (ref * REF_STEP_PER_DAY_BPS * dt) / (2 * 1 days * 10_000); uint256 lo = ref - step; uint256 hi = ref + step;` (ref < 2^160 so the product fits in 256 bits); verified locally: the proof passes and the 9 tests in test/PepesBuyback.t.sol still pass. Alternatively advance refTime only by the time actually credited (refTime += h * 864) or return before writing refTime when h == 0.

**Reproduction**

Setup as test/PepesBuyback.t.sol; the buyback holds 100 IMD. eve buys 100 IMD of $Pepes and holds (priceRiseBps() = 1889). Then anyone calls poke() every 10 minutes for 30 days (4,320 calls, no trades). Expected (contract notice lines 36-40, test_organicRiseOnlyDelays which pokes daily and resumes in 8 days): the reference follows at 2%/day and the buyback resumes within about 10 days. Actual: refSqrtPrice is bit-identical before and after (23817539250915624842179591654741), priceRiseBps() is still 1889 and buybackAndBurnPepes reverts PriceRisen. Single step: with the price above the reference, warp 863 s and poke(): refTime == block.timestamp but refSqrtPrice is unchanged (reproduced in a scratch test).
Run: forge test --match-path test/scratch/PokeTruncationProof.t.sol (fails on commit 2560653 with '30 days of pokes never moved the reference'; passes with the full-precision step).

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

contract ProofIMD {
    string public name = "Identity.md";
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

/// @dev Only there so launchpad A (which hosts the "$Pepes" pool) can be deployed: its own buyback is never used.
contract ProofWiring {
    PoolKey key;

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

/// @dev "$Pepes" is a token launched on launchpad A (same 4% hook fee and single-sided curve as the live v1 pool);
///      launchpad B's PepesBuyback buys it through A's router, as production buys $Pepes through the v1 router.
abstract contract ProofBase is Test {
    uint160 constant FLAGS = uint160((1 << 13) | (1 << 11) | (1 << 7) | (1 << 6) | (1 << 3) | (1 << 2));
    int24 constant START_TICK = 161000; // ~100 IMD starting market cap

    PoolManager pm;
    ProofIMD imd;
    PepesFamilyRouter routerA;
    PadToken pepes;
    PepesBuyback buyback;

    address eve = makeAddr("eve");
    address bob = makeAddr("bob");

    function setUp() public {
        vm.warp(1_800_000_000);
        pm = new PoolManager(address(this));
        imd = new ProofIMD();

        ProofIMD other = new ProofIMD();
        ProofWiring w = new ProofWiring();
        (address c0, address c1) =
            address(other) < address(imd) ? (address(other), address(imd)) : (address(imd), address(other));
        PoolKey memory k = PoolKey(Currency.wrap(c0), Currency.wrap(c1), 3000, 60, IHooks(address(0)));
        pm.initialize(k, TickMath.getSqrtPriceAtTick(0));
        w.setKey(k);

        PepesFamily padA = _deployPad(address(other), address(w));
        routerA = PepesFamilyRouter(payable(padA.router()));
        pepes = PadToken(payable(padA.launch("Pepes", "PEPES", "", address(imd))));
        imd.mint(bob, 10_000e18);
        vm.startPrank(bob);
        imd.approve(address(routerA), type(uint256).max);
        pepes.approve(address(routerA), type(uint256).max);
        routerA.buy(address(pepes), 1_000e18, 0, block.timestamp); // gives the $Pepes pool some depth
        vm.stopPrank();

        buyback = PepesBuyback(_deployPad(address(pepes), address(routerA)).buyback());

        imd.mint(eve, 10_000e18);
        vm.startPrank(eve);
        imd.approve(address(routerA), type(uint256).max);
        pepes.approve(address(routerA), type(uint256).max);
        vm.stopPrank();
    }

    function _deployPad(address pepes_, address pepesRouter_) internal returns (PepesFamily) {
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
        bytes32 h = keccak256(initCode);
        for (uint256 i; i < 500_000; i++) {
            address a = address(uint160(uint256(keccak256(abi.encodePacked(bytes1(0xff), address(this), bytes32(i), h)))));
            if (uint160(a) & 0x3FFF != FLAGS) continue;
            address deployed;
            assembly {
                deployed := create2(0, add(initCode, 0x20), mload(initCode), i)
            }
            require(deployed == a, "hook address");
            return PepesFamily(deployed);
        }
        revert("no salt");
    }

    function _tryBuyback() internal returns (bool ok) {
        try buyback.buybackAndBurnPepes(0, block.timestamp) {
            ok = true;
        } catch {}
    }

    function _depth() internal view returns (uint256) {
        return buyback.maxBuyback() * 100;
    }
}

contract PokeTruncationProof is ProofBase {
    /// The price sits ~19% above the reference. poke() is documented to follow at 2% a day, so 30 days are plenty.
    /// Here someone (anyone: poke is permissionless and every PadToken.recycle calls it) pokes every 10 minutes.
    function test_frequentPokesStillFollowTheMarket() public {
        imd.mint(address(buyback), 100e18);
        vm.prank(eve);
        routerA.buy(address(pepes), 100e18, 0, block.timestamp);
        assertGt(buyback.priceRiseBps(), 1_000, "price is well above the reference");
        uint160 ref0 = buyback.refSqrtPrice();

        for (uint256 i; i < 30 days / 10 minutes; i++) {
            vm.warp(block.timestamp + 10 minutes);
            buyback.poke();
        }

        assertTrue(buyback.refSqrtPrice() != ref0, "30 days of pokes never moved the reference");
        assertLe(buyback.priceRiseBps(), buyback.MAX_PRICE_RISE_BPS(), "2% a day for 30 days covers a 19% rise");
        buyback.buybackAndBurnPepes(0, block.timestamp);
        assertGt(buyback.totalImdSpent(), 0, "the buyback resumed");
    }
}
```

### 3. Low: A buyback attempt that fails the guard reverts its own poke, so 'poke runs inside every buyback' never holds when it matters: hourly attempts alone never un-stall the buyback

`contracts/src/PepesBuyback.sol:147`

```
        if (priceRiseBps() > MAX_PRICE_RISE_BPS) revert PriceRisen();
```

Merged from audit_economics finding 3, audit_flow finding 2 and audit_math finding 3; reproduced.

buybackAndBurnPepes calls poke() at line 146 and reverts PriceRisen at line 147 when the price is still more than 2% above the reference; the revert undoes the poke's writes to refSqrtPrice and refTime (the same holds for the TooSoon and BadAmount reverts). So the notice ('poke, also run by every recycle and buyback'), README line 85 and the comment on test_organicRiseOnlyDelays ('every recycle and buyback attempt') overstate what happens: a stalled buyback never advances the reference from its own attempts, and the natural integration (a keeper retrying buybackAndBurnPepes hourly) makes no progress ever. Only an explicit poke() or a PadToken.recycle that actually moves expired rewards moves the reference, and because one update counts at most one day, someone has to do that at least daily. test_organicRiseOnlyDelays passes only because its loop calls buyback.poke() explicitly.

Fix: keep the poke when the guard fails, e.g. `if (priceRiseBps() > MAX_PRICE_RISE_BPS) { _locked = 1; return 0; }` (callers already treat 0 burned as nothing done; verified locally: the proof passes and the existing 9 tests pass), or document that upkeep must call poke() at least daily and have the website/keeper do it.

**Reproduction**

Setup as test/PepesBuyback.t.sol; the buyback holds 100 IMD. eve buys 100 IMD of $Pepes (priceRiseBps() = 1889). A keeper calls buybackAndBurnPepes(0, block.timestamp) once an hour for 30 days and nothing else is called. Expected per the notice: the reference follows at 2%/day and the buyback resumes after about 8 days. Actual: 720 attempts all revert PriceRisen, refSqrtPrice never changes, totalImdSpent stays 0. Single step: warp 3 days, call buybackAndBurnPepes: it reverts and afterwards refTime and refSqrtPrice equal their values from before the call (refTime still 1800000000).
Run: forge test --match-path test/scratch/FailedAttemptPokeProof.t.sol (fails on commit 2560653 with '720 hourly attempts never moved the reference').

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

contract ProofIMD {
    string public name = "Identity.md";
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

/// @dev Only there so launchpad A (which hosts the "$Pepes" pool) can be deployed: its own buyback is never used.
contract ProofWiring {
    PoolKey key;

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

/// @dev "$Pepes" is a token launched on launchpad A (same 4% hook fee and single-sided curve as the live v1 pool);
///      launchpad B's PepesBuyback buys it through A's router, as production buys $Pepes through the v1 router.
abstract contract ProofBase is Test {
    uint160 constant FLAGS = uint160((1 << 13) | (1 << 11) | (1 << 7) | (1 << 6) | (1 << 3) | (1 << 2));
    int24 constant START_TICK = 161000; // ~100 IMD starting market cap

    PoolManager pm;
    ProofIMD imd;
    PepesFamilyRouter routerA;
    PadToken pepes;
    PepesBuyback buyback;

    address eve = makeAddr("eve");
    address bob = makeAddr("bob");

    function setUp() public {
        vm.warp(1_800_000_000);
        pm = new PoolManager(address(this));
        imd = new ProofIMD();

        ProofIMD other = new ProofIMD();
        ProofWiring w = new ProofWiring();
        (address c0, address c1) =
            address(other) < address(imd) ? (address(other), address(imd)) : (address(imd), address(other));
        PoolKey memory k = PoolKey(Currency.wrap(c0), Currency.wrap(c1), 3000, 60, IHooks(address(0)));
        pm.initialize(k, TickMath.getSqrtPriceAtTick(0));
        w.setKey(k);

        PepesFamily padA = _deployPad(address(other), address(w));
        routerA = PepesFamilyRouter(payable(padA.router()));
        pepes = PadToken(payable(padA.launch("Pepes", "PEPES", "", address(imd))));
        imd.mint(bob, 10_000e18);
        vm.startPrank(bob);
        imd.approve(address(routerA), type(uint256).max);
        pepes.approve(address(routerA), type(uint256).max);
        routerA.buy(address(pepes), 1_000e18, 0, block.timestamp); // gives the $Pepes pool some depth
        vm.stopPrank();

        buyback = PepesBuyback(_deployPad(address(pepes), address(routerA)).buyback());

        imd.mint(eve, 10_000e18);
        vm.startPrank(eve);
        imd.approve(address(routerA), type(uint256).max);
        pepes.approve(address(routerA), type(uint256).max);
        vm.stopPrank();
    }

    function _deployPad(address pepes_, address pepesRouter_) internal returns (PepesFamily) {
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
        bytes32 h = keccak256(initCode);
        for (uint256 i; i < 500_000; i++) {
            address a = address(uint160(uint256(keccak256(abi.encodePacked(bytes1(0xff), address(this), bytes32(i), h)))));
            if (uint160(a) & 0x3FFF != FLAGS) continue;
            address deployed;
            assembly {
                deployed := create2(0, add(initCode, 0x20), mload(initCode), i)
            }
            require(deployed == a, "hook address");
            return PepesFamily(deployed);
        }
        revert("no salt");
    }

    function _tryBuyback() internal returns (bool ok) {
        try buyback.buybackAndBurnPepes(0, block.timestamp) {
            ok = true;
        } catch {}
    }

    function _depth() internal view returns (uint256) {
        return buyback.maxBuyback() * 100;
    }
}

contract FailedAttemptPokeProof is ProofBase {
    /// The price sits ~19% above the reference and a keeper calls the buyback every hour for 30 days, nothing else.
    /// "poke runs inside every buyback", so the reference should follow at 2% a day and the buyback resume.
    function test_hourlyAttemptsAloneEventuallyResume() public {
        imd.mint(address(buyback), 100e18);
        vm.prank(eve);
        routerA.buy(address(pepes), 100e18, 0, block.timestamp);
        assertGt(buyback.priceRiseBps(), 1_000, "price is well above the reference");
        uint160 ref0 = buyback.refSqrtPrice();

        for (uint256 i; i < 30 * 24; i++) {
            vm.warp(block.timestamp + 1 hours);
            _tryBuyback();
        }

        assertTrue(buyback.refSqrtPrice() != ref0, "720 hourly attempts never moved the reference");
        assertGt(buyback.totalImdSpent(), 0, "the buyback resumed within 30 days");
    }
}
```

### 4. Low: Dip-poking: after a day without pokes, one sell-poke-rebuy transaction takes the whole 2% step downward and stalls the buyback for a day at ~0.16% of depth in fees (documented trade-off, quantified; n

`contracts/src/PepesBuyback.sol:125`

```
        uint256 cur = _sqrtPrice();
```

Merged from audit_flow finding 3 and audit_permissions finding 4; reproduced. Answers the re-check question 'poking around a dip'.

poke() moves the reference toward whatever the pool's spot sqrtPrice is in the poking transaction, by up to 2% (price) for one day of elapsed time; nothing requires the price to persist, and poke() is not blocked while the PoolManager is unlocked, so the bracket can also run inside an unlock with flash-accounted funds. Whoever pokes first after a day of silence takes the whole day's budget in their direction: sell about 2% of depth (price -3.6%), poke (reference -2%), rebuy to the previous price. priceRiseBps() is then just above 200 and the next buyback reverts PriceRisen until a later poke, a day on, moves the reference back. The cost is the two 4% hook fees on the dumped amount (1.76 IMD here, ~0.16% of depth), no position held, no gain: it is griefing of the burn. It is not cumulative: the reference can never be pushed below the dipped spot, and honest pokes (hourly) compete for the same elapsed-time budget, limiting the attack to dips at least as deep as the gap wanted (the flow specialist measured 60 of 72 hourly buybacks still running with hourly honest pokes and hourly 0.2% dips).

test_dumpBracketDoesNotStall only covers a bracket one hour after the last update (step 0.08%), which is why it passes. The notice and README already accept that a bracketed dip moves the reference 'by at most 2% a day'; this is reported so the consequence (a repeatable, nearly free one-day stall whenever upkeep is sparse) is a conscious choice, and because the fix for the reference-above-market finding (following a fall at once) widens it to the dump depth.

Mitigations if wanted: run poke() hourly from the keeper (bounds the step a bracketer can take to 0.08%); apply the price observed at the previous poke rather than the current one (store a candidate sqrtPrice on each poke and move toward the previous candidate), so moving the reference requires the manipulated price to persist until a later poke; skip the observation while poolManager.isUnlocked(), as PadToken.distribute does.

**Reproduction**

Setup as test/PepesBuyback.t.sol; the buyback holds 100 IMD. eve buys 2% of depth (21 IMD) and holds; five daily pokes bring the reference to the market (priceRiseBps() == 0). One day later, in one transaction: eve sells her bag, calls poke(), buys back with 109% of the proceeds (restoring the price). Expected if dips were harmless: the next buyback runs. Actual: priceRiseBps() == 202 > 200, buybackAndBurnPepes reverts PriceRisen; eve's cost is 1.76 IMD (round-trip fees, ~0.16% of the 1,082 IMD depth) and she holds the same bag; a day later, after a poke, the buyback runs again. (Scratch test test_dipBracketAroundPoke, log output.)

### 5. Low: Poke-then-guard ordering makes the effective band ~4% after an idle day, and any pre-buy inside the band held across the hourly series pays (bounded leak, ~1-3% of what the series spends)

`contracts/src/PepesBuyback.sol:146`

```
        poke();
```

Merged from audit_economics finding 4 and audit_permissions finding 3; reproduced.

(a) buybackAndBurnPepes pokes first (line 146) and checks the guard second (line 147). When a day has passed since the last update, the poke moves the reference up to 2% toward a price pumped in the same transaction, and the guard then allows another 2%, so a pre-buy of about 2% of depth (+3.9% in price, priceRiseBps() 387) passes although the documented band is 2%. (b) From then on the reference follows each buyback's own impact, so every later buyback passes as well while the buyer simply holds: 24 buybacks of ~1.9% each appreciate the bag. test_pacedPreBuysDoNotPay only tests re-buying before every buyback, which stalls after the first; buying once and holding does pay.

This is bounded (the buyback overpays by at most the band) and partly inherent to a public hourly schedule; it is reported so the bound is a conscious choice. If wanted: check the guard against the reference as it stood before this call's poke (keeps the band at the documented 2% after idle days); a smaller band with a correspondingly slower drift; or a daily cap on what the series spends, which also helps the reference-above-market finding.

**Reproduction**

Setup as test/PepesBuyback.t.sol; the buyback holds one pool depth (1,061.9 IMD).
(a) Warp 1 day. eve buys 2% of depth (21.24 IMD): priceRiseBps() == 387. 24 hourly buybacks follow, then she sells. Expected per the test suite's stated property ('riding the hourly series must not pay'): no profit. Actual: all 24 buybacks run (290.55 IMD spent) and eve ends +9.57 IMD (45% on her position).
(b) Fresh reference (one buyback run), eve buys 0.5% of depth (5.31 IMD): priceRiseBps() == 95; 24 hourly buybacks run; she sells: +2.42 IMD on a 5.3 IMD stake after both 4% fees. (Scratch tests test_idleDayPreBuyRidesSeries and test_inBandPreBuy, log output.)

### 6. Info: Trust assumption (verified, not a defect): buys through third-party routers credit tx.origin, so an ERC-4337 smart account's buys mark its bundler active; the ETH-router hookData change is otherwise c

`contracts/src/PepesFamily.sol:356`

```
            : tx.origin;
```

From audit_permissions finding 5; confirmed by reading the code and the hookData paths. Answers the re-check question on the ETH router.

Verified in this commit: PepesFamilyEthRouter passes abi.encode(user) only on the token-pool swaps (lines 135 and 149) and empty hookData on the IMD/ETH legs (lines 131 and 160), so a hook on the IMD/ETH pool sees no change; the PepesFamily hook decodes hookData only when sender is router or ethRouter and hookData.length == 32, and both are immutables set in the constructor; a third-party router cannot impersonate either because sender is the PoolManager's msg.sender; Trade.trader and markActive now receive the ETH-router user instead of tx.origin, matching the IMD router; PadToken.recycle's low-level call to poke() cannot block a recycle (poke makes no external calls besides PoolManager reads, cannot overflow since next is always below a uint160 value, and a failing or codeless target just yields ok == false).

Remaining asymmetry: for swaps not sent by the two PepesFamily routers the hook records tx.origin. A smart-contract wallet trading through an aggregator via an ERC-4337 bundler has tx.origin == the bundler EOA, so markActive never touches the wallet and its rewards expire after 7 days of not claiming or sending even while it keeps buying. The NatSpec and README line 82 document this ('should claim (or send) at least weekly'); surface it in the UI.

**Reproduction**

State: a token launched on the v4 pad; a smart account S buys through PoolSwapTest (any non-PepesFamily router) in a transaction whose tx.origin is bundler B. Expected by a user of S: S is active. Actual: lastActive[S] is unchanged (only its first-ever receipt set it); lastActive[B] is set. After 7 days recycle(S) moves S's older rewards to the buyback. (Read from PepesFamily.sol lines 354-358 and PadToken.markActive; the existing PepesFamily.t.sol router tests show the router path crediting the user.)

### 7. Info: Guard tests never poke at sub-864 s cadence, never start from a reference above the market, and never hold a single in-band pre-buy across the series, so the defects above are outside the suite

`contracts/test/PepesBuyback.t.sol:211`

```
            buyback.poke();
```

From audit_math finding 4; confirmed. test_organicRiseOnlyDelays pokes once a day (and un-stalls only because of this explicit poke, not through the buyback attempts the comment on line 200 credits); test_dumpBracketDoesNotStall brackets one hour after the last update; the hourly-series tests update at exactly one hour; every scenario starts with the reference at or above the market and immediately runs a buyback. Suggested additions: (a) poke every N seconds for N in {1, 60, 800} over 10 days after a 10-20% rise and assert the buyback resumes within the documented window; (b) the pump-then-series scenario after a day of buybacks with holders selling the burned amount, and after a 35% bag sale plus a day of hourly pokes, asserting runs == 0 and no attacker profit; (c) one 2%-of-depth pre-buy after an idle day held across 24 buybacks; (d) a sell-poke-rebuy bracket a day after the last update.

**Reproduction**

forge test --match-path test/PepesBuyback.t.sol on commit 2560653: 9 passed. The scratch tests test/scratch/PokeTruncationProof.t.sol, test/scratch/ReferenceAboveMarketProof.t.sol and test/scratch/FailedAttemptPokeProof.t.sol exercise those inputs and fail. The full non-fork suite (125 tests) passes, so no regression of earlier fixed findings was observed.

---

Judge's submission `042ae79d6377b3919646e9f0ac77b3a512d8953143f58619c628d538041d46c4`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
