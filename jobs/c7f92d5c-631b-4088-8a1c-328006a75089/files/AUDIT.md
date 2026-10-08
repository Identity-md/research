# Audit report

> Audit the three Ponzinomics contracts in src/pimd at this commit. PimdToken is a fixed-supply ERC-20: exactly 1,000,000,000 at 18 decimals, minted once in the constructor, no owner, no mint and no burn function (burning is a plain transfer to DEAD, so totalSupply never moves). PimdHook is a Uniswap V4 hook that taxes every trade in IMD, 2.4% on buys and 5.6% on sells with the pool's own 1.25% on top, split 75% to holders and 25% to the team, taking its fees as ERC-6909 claims on the quote currency. The IMD launch factory constructs the hook and opens the pool itself, so the team wallet, the engine address, the quote token and the opening tick (129,000, tolerance 300) are all source constants. PimdEngine pushes the holders' IMD into wallets weighted by balance times hold-streak, the tiers being zero under an hour and then 0.5x, 1x, 1.5x, 2x and 3x from fourteen days; tally weighs the whole set in one call and pay is paged. The holder-set logic is the part to look hardest at: it changed after your last audit of this repository and nobody outside has read it. Four things in particular. First, register probes an address with _isPool but can only see the code that is there at the time, so it now records a vettedCodeless bit and tally calls _shapeChanged, which takes all weight off an address once code arrives where there was none. Say whether that really closes the play of picking a CREATE2 address, funding it, registering it while it is still empty, letting the streak mature and only then deploying pair code into it, and whether it can be evaded from the other side by an address that carries code from the start. Second, _shapeChanged is blunt on purpose: any code arriving voids the verdict, a legitimate EIP-7702 delegation included, and prune drops a holder on that same test so the address can register again on what it now is. Confirm there is no reachable state in which a holder earns nothing and cannot be pruned, because the engine has no owner and that would be permanent. Third, prune now drops a holder on its shape as well as its size and is permissionless: confirm it cannot be aimed at a holder who should keep earning, and that the swap-and-pop is still right when the pruned holder is the last element. Fourth, the exclusion list at bind is the token, imd, the hook, the PoolManager, the engine, the team, address(0) and DEAD, plus whatever the binder names. Say whether anything else can hold PIMD, be registered, and then be unable to forward an IMD payout. Then the standing ones. Tally weighs the whole set in one call against min(bal, lastBal) so a single bag cannot be counted once per wallet it is moved through, which was the high you found last time: confirm it holds. The engine must never read holder weights while the PoolManager is unlocked, which is where a flash borrower would stand. One holder who cannot receive IMD must not be able to stall a batch. beforeRemoveLiquidity is the whole safety case for letting the launch factory hold the liquidity position: it must refuse every negative liquidityDelta for ever, from any caller including the position's owner and the hook itself, while allowing a zero delta so the pool's own fee collection still works. beforeAddLiquidity must allow exactly one add, the factory's seed, and refuse every later one, reentrancy and the hook calling itself included. beforeInitialize is the only gate on the pool's shape: confirm it cannot be bypassed and that every assumption the tax maths makes is enforced there, in particular that IMD is currency0. And the fee accounting: claims minted in beforeSwap and afterSwap must always equal holdersOwed plus teamOwed, with nothing double counted or stranded, and flush must not be able to pay out more than was taken. The engine pulls from the hook inside a try/catch, which has hidden one breakage from us already: say whether that pattern is safe here. Report findings rather than fixing them, and do not propose changes to the economics, the tax rates, the split or the tier ladder.

| | |
|---|---|
| Repository | https://github.com/JJ-ME55/Ponzinomics.git |
| Commit | `0fc1ff2556a8007f77b34fac39c83acaef957817` |
| Job | `c7f92d5c-631b-4088-8a1c-328006a75089` |
| Judged | 2026-10-08 14:50 UTC |
| Findings | 3 medium · 5 low · 3 info |

Four agents audited the code as it is at `0fc1ff2`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Medium: fire() pulls the hook through flush(), so the flush caller tip is paid to the engine and booked as holder income out of the team's 25%

`src/pimd/PimdEngine.sol:324`

```
            try hook.flush() {}
```

PimdHook.flush() (PimdHook.sol:436-443) carves a caller tip of min(callerTip = 0.01 IMD, 20% of teamOwed) out of the team's slice and pays it to msg.sender. On the engine's normal income path, PimdEngine.fire() is the caller (line 324, `try hook.flush() {}`), so msg.sender is the engine. The tip lands in the engine's IMD balance and the very next line's _book() (line 555-563) counts everything above pot + epochQuote as holder income. Every fire that finds holdersOwed != 0 therefore moves up to 20% of the team's accrued slice (capped at 0.01 IMD) from the team to the holders' pot. In a quiet market (under about 8.3 IMD of buys or 3.6 IMD of sells per epoch) the team receives exactly 80% of its 25%; in a busy one it loses a flat 0.01 IMD per fire, up to about 7.2 IMD a day at the 2-minute minInterval. The hook's totalToTeam still records the full slice as paid to the team and the Flushed event reports the tip as a keeper tip, so the lifetime stats disagree with the balances. The fire keeper is already paid fireTip from the engine's own tip budget, so nobody needed this payment. Claims stay consistent: holdersOwed + teamOwed is burned exactly, nothing is lost or double minted; only the recipient is wrong. Both contracts are ownerless, so this cannot be corrected after launch. Fix without touching the economics: have fire() pull through flushHolders() as its main path and leave flush() to outside callers (the team's slice then waits for an outside flush, which the hook already supports), or have flush() pay no tip (leave it in the team's share) when msg.sender == engine(). Merged from four specialists (math, flow, permissions, economics), who all reproduced the same numbers.

**Reproduction**

Full stack (PoolManager, real hook with constants pointed at local doubles, real engine, test config minBalance 100,000e18). Register carol with 1,000,000 PIMD. Past the launch cap, alice does an exact-in buy of 1 IMD: hook.holdersOwed() == 0.018e18, hook.teamOwed() == 0.006e18. Warp 2 hours, keeper calls engine.fire(). Expected: team receives 0.006e18 IMD and engine.totalIncome() == 0.018e18. Actual (forge run of test/scratch/ProofFlushTip.t.sol): team receives 0.0048e18, engine.totalIncome() == 0.0192e18, hook.totalToTeam() == 0.006e18. The 0.0012e18 tip (20% of the team's slice) went from the team to the holders' pot. The attached proof fails on this code with `the team did not receive its whole slice: 4800000000000000 != 6000000000000000`.

### 2. Medium: One minimum bag walked through fresh addresses fills the bounded holder set and locks every honest holder out of register()

`src/pimd/PimdEngine.sol:266`

```
            if (holders.length >= maxHolders) revert HolderSetFull(maxHolders);
```

register() admits an address on nothing but its PIMD balance at the instant of the call (line 261-262) and then counts it against maxHolders for as long as it stays in the set (line 266). Nothing remembers where a bag came from or requires it to survive a tally before it occupies a slot. Registration is permissionless and works for any address, so an attacker holding exactly minBalance moves the bag to a fresh address, registers it, moves it on, registers the next, and so on until holders.length == maxHolders. From then on every register() call reverts HolderSetFull for everybody, however large or old their bag, and a keeper batch that crosses the cap reverts as a whole. The deploy script (script/DeployPimd.s.sol:62-63) sizes the bound on the premise that 'the minimum bag is a tenth of a percent of supply, so at most 1,000 addresses can qualify at once and this cap is never the thing that binds'; that premise is false because qualifying is only tested at registration. Measured with the live config (maxHolders 1,200, minBalance 1,000,000e18, which the engine named by the hook, 0x8974d07239e6D8B843eE70725823E7e95CbB6924, reports on chain): filling 1,200 slots costs about 178M gas (about six transactions at Robinhood's 32M per-tx cap, gas only, the attacker's capital is one 0.1% bag). The ghosts are prunable, but only in Phase.Idle, one paid call at a time (22.7M gas for all 1,199), and register() works in every phase, so the attacker refills as soon as slots open: a standing gas race, with no owner to end it. Two aggravators measured on this code: (1) the ghosts do not wedge the engine (a tally over 1,199 empties plus one weighted holder costs 16.1M gas) but tally and pay each pay tipPerHolder per entry, so one epoch over the padded set paid the keeper 7.25 IMD (bounded by the 5% tip budget) against 0.056 IMD for an honest set of one; (2) the streak clock starts at registration, so an honest buyer locked out during the launch window loses hold time that cannot be recovered. Who loses: every holder who cannot register, and the pot through inflated tips; who gains: already-registered holders and whoever runs tally/pay on the padded set. Fix without changing the economics: make a slot cost a bag that stays, e.g. let register() evict (or skip rather than revert on) an entry whose live balance is below minBalance or whose shape changed when the set is full, or only count a registration against the bound once a tally has seen its bag (lastBal is already written at line 273). Merged from three specialists (flow, permissions, economics) with matching measurements.

**Reproduction**

Engine bound with maxHolders 1,200 and minBalance 1,000,000e18 (the live values). Attacker holds 1,000,000e18 PIMD. For i in 0..1199: transfer the bag to sybil_i, call register([sybil_i]). holderCount() == 1200 and only the last sybil holds any PIMD. An honest wallet holding 10,000,000e18 PIMD calls register([honest]). Expected: an address holding ten times the minimum, not excluded and not a pool, is registered. Actual: revert HolderSetFull(1200). The attached proof (mock hook and pool manager, real token and engine) fails on this code with exactly that error; the specialists' full-stack version (test/scratch/HolderSetFill.t.sol) fails the same way. Gas measured on this code: fill 178M, tally over the padded set 16.1M, prune of 1,199 ghosts 22.7M, keeper tips for the padded epoch 7.25 IMD.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {ERC20} from "solmate/src/tokens/ERC20.sol";
import {PimdToken} from "src/pimd/PimdToken.sol";
import {PimdEngine} from "src/pimd/PimdEngine.sol";

/// A plain 18-decimal stand-in for IMD.
contract MockIMD is ERC20("Identity.md", "IMD", 18) {
    function mint(address to, uint256 amount) external {
        _mint(to, amount);
    }
}

/// The only thing the engine reads from the PoolManager is the transient unlock flag.
contract MockPoolManager {
    function exttload(bytes32) external pure returns (bytes32) {
        return bytes32(0);
    }
}

/// Just enough hook for `bind` to accept it and for `fire` to find nothing owed.
contract MockHook {
    address public engine;
    address public quote;
    address public token;
    address public poolManager;

    constructor(address quote_, address token_, address pm_) {
        quote = quote_;
        token = token_;
        poolManager = pm_;
    }

    function setEngine(address e) external {
        engine = e;
    }

    function holdersOwed() external pure returns (uint256) {
        return 0;
    }

    function flush() external pure returns (uint256, uint256) {
        return (0, 0);
    }

    function flushHolders() external pure returns (uint256) {
        return 0;
    }
}

/// Finding: `register` is permissionless and bounded, but the bound is filled by one bag.
/// Registration reads `balanceOf` at call time and nothing else, so a single bag of exactly `minBalance`
/// moved through `maxHolders` fresh addresses, each registered as it passes, fills the set in one
/// transaction. Every honest holder after that is refused with `HolderSetFull`, however big their bag.
/// Live Robinhood config: maxHolders 1,200, minBalance 1,000,000 PIMD (0.1% of supply).
contract HolderSetFillTest is Test {
    uint256 constant MIN = 1_000_000e18;
    uint256 constant MAX_HOLDERS = 1_200;

    MockIMD imd;
    MockPoolManager pm;
    PimdToken token;
    MockHook hook;
    PimdEngine engine;
    address team = makeAddr("team");

    function setUp() public {
        imd = new MockIMD();
        pm = new MockPoolManager();
        token = new PimdToken(); // this contract holds the whole supply
        hook = new MockHook(address(imd), address(token), address(pm));
        engine = new PimdEngine(
            PimdEngine.Config({
                poolManager: address(pm),
                imd: address(imd),
                team: team,
                binder: address(this),
                dripBpsPerPeriod: 150,
                minInterval: 2 minutes,
                minBalance: MIN,
                fireTip: 0.05e18,
                tipPerHolder: 0.003e18,
                maxCatchup: 6 hours,
                maxHolders: MAX_HOLDERS
            })
        );
        hook.setEngine(address(engine));
        engine.bind(address(token), address(hook), new address[](0));
    }

    function test_one_minimum_bag_fills_the_whole_holder_set_and_locks_everyone_else_out() public {
        // The attacker owns exactly one minimum bag: 0.1% of supply.
        address attacker = makeAddr("attacker");
        token.transfer(attacker, MIN);

        // One transaction: move the bag to a fresh address, register it, move on. Each registration sees a
        // full bag at the address being registered. Nothing in `register` remembers where the bag came from.
        address[] memory one = new address[](1);
        address prev = attacker;
        for (uint256 i; i < MAX_HOLDERS; ++i) {
            address sybil = address(uint160(0xA11CE0000 + i));
            vm.prank(prev);
            token.transfer(sybil, MIN);
            one[0] = sybil;
            engine.register(one);
            prev = sybil;
        }
        assertEq(engine.holderCount(), MAX_HOLDERS, "the set is full on the strength of one bag");
        assertEq(token.balanceOf(prev), MIN, "and the attacker still holds that one bag, in the last sybil");

        // An honest holder with ten minimum bags, bought the ordinary way, now tries to register.
        address honest = makeAddr("honest");
        token.transfer(honest, 10 * MIN);
        one[0] = honest;
        // Expected: an address holding far more than the minimum, that is not a pool and not excluded, can
        // register. Actual on this code: `HolderSetFull(1200)`.
        engine.register(one);
        (bool registered,,,,) = engine.holderInfo(honest);
        assertTrue(registered, "an honest holder could not register because one bag occupies every slot");
    }
}
```

### 3. Medium: bind's fixed exclusion list omits the launch factory, and any other non-forwarding PIMD holder (lockers, precompiles, burn sinks) can be registered by a stranger and strands its share of every drip fo

`src/pimd/PimdEngine.sol:228`

```
            [token_, address(imd), hook_, address(poolManager), address(this), team, address(0), DEAD];
```

Answer to the brief's fourth question: yes. Exclusion happens once, at bind, as a fixed list (token, imd, hook, PoolManager, engine, team, address(0), DEAD) plus whatever the binder names. register() is permissionless for any address, its only shape filter is _isPool (which recognises a contract only if token0() or token1() returns PIMD), and after bind nothing can add an exclusion: the engine has no owner. So anyone can enrol, at any time, any address that holds >= minBalance, is not V2/V3-shaped and cannot move IMD; once enrolled it earns its weight every epoch, pay's _send succeeds (an ERC-20 transfer to a keyless or inert address does not fail), so the IMD does not even return to the pot, and prune() never drops it because its bag does not fall, it was not codeless-then-coded, and _isPool still says no. The concrete case the protocol itself can see: the launch factory. The hook pins it as a source constant (PimdHook.LAUNCH_FACTORY / launchFactory(), PimdHook.sol:100,134) and it owns the only liquidity position. Every sell pays the pool's 1.25% fee in PIMD to that position, and a zero-delta modifyLiquidity (which beforeRemoveLiquidity deliberately allows as fee collection) lands it in the factory's balance. Reproduced on this code: one 300 IMD buy and a half-bag sell leave 648,006 PIMD in the mock factory after one collection, above the 100,000 test minimum; register([factory]) then succeeds (it has code, so vettedCodeless is false and _shapeChanged never fires; it has no token0/token1, so _isPool is false), the next epoch pays it IMD, and prune([factory]) leaves it registered. Whether the real factory ever retains PIMD above the production minimum, or can forward IMD, depends on code outside this repository, so the factory case is conditional on that state; the deploy instructions (DeployPimd.s.sol:94-95) tell the binder to exclude only the airdrop distributor. IPimdHookLike does not even declare launchFactory(), so the engine cannot read the address the hook already knows. Unconditional cases reproduced on this code: a precompile (address(1)) funded with minBalance registers, is paid, and cannot be pruned (IMD stranded at a keyless address); the same holds for burn sinks other than DEAD and zero, and for any locker, vesting, escrow or non-V2/V3 venue (Curve-style coins(i), Balancer vault, ERC-4626 wrapper) that holds PIMD after bind, which anyone can register on its behalf. The NatSpec on bind (lines 199-203, 221-226) treats exactly this outcome as the reason the distributor and token are excluded. Fix within the design: add launchFactory() to IPimdHookLike and h.launchFactory() to the fixed list at bind (and document that the binder must name any other known non-forwarding holder); for the general case the only robust answer is a scope decision, e.g. self-registration only (msg.sender == a, or a signature from a) so a contract is enrolled only if it chooses to be. Merged from four specialists (math: precompiles; flow: factory; permissions: lockers; economics: factory fee collection).

**Reproduction**

Factory case (full stack, test config minBalance 100,000e18, binder passes no alsoExclude): past the launch cap, alice buys with 300 IMD and sells half her PIMD; the factory runs a zero-delta modifyLiquidity on its position (fee collection) and now holds 648,006 PIMD; a stranger calls engine.register([factory]). Expected: the launch factory, an address the hook itself names and that cannot forward IMD, is excluded like every other launch contract. Actual: holderInfo(factory).registered_ == true; after 2 days fire/tally/pay sends it IMD, and prune([factory]) leaves it registered. The attached proof (test/scratch/ProofFactoryRegistered.t.sol) fails on this code at the registration assertion. Precompile case (mock-based, minBalance 1,000,000e18): transfer 1,000,000e18 PIMD to address(1), register([address(1), alice]), mint 1,000 IMD to the engine, warp 2 days, fire, tally(10), pay(10). Expected: no IMD is sent to an address that cannot forward it, or it is prunable. Actual: imd.balanceOf(address(1)) > 0 and prune([address(1)]) leaves holderCount at 2.

### 4. Low: _isPool is a selector probe the probed contract answers, so a pool that carries code from the start is registered, paid and never prunable; the codeless CREATE2 play is closed

`src/pimd/PimdEngine.sol:631`

```
        return _probe(a, IPairLike.token0.selector) == t || _probe(a, IPairLike.token1.selector) == t;
```

Answer to the brief's first question, both sides. The codeless side is closed: an address registered empty gets vettedCodeless = true (line 272); when any code arrives, tally gives it weight 0 the same epoch (line 411), prune drops it on the same test (line 300), and re-registration is refused by _isPool if the code is a pair. After Cancun (EIP-6780) deployed code cannot be removed again outside its creating transaction, so a pair that lands stays caught; registering from inside the pair's own constructor does not help because the code lands after the constructor returns. The other side is open, and nothing ever catches it, because _shapeChanged only watches addresses that were codeless at registration and tally deliberately never re-probes. (a) A pair whose token0()/token1() depend on the caller: _probe is a staticcall from the engine's own address, so a pair that answers address(0) when msg.sender == engine and PIMD to everyone else passes register and every later prune, and collects drips on pooled PIMD indefinitely. (b) A proxy or a contract with mutable token0/token1: register with a non-matching answer, flip afterwards; prune would catch it, but only if someone calls prune between flips. (c) Any pool shape that does not expose token0/token1 at all (a Curve-style pool, a Balancer vault, an ERC-4626 wrapper, a V4 singleton other than the excluded PoolManager) is never seen. Two smaller gaps in the codeless defence, both bounded to one epoch: pay() does not re-check shape, so pair code deployed between tally and pay is still paid that epoch's full share (reproduced: a codeless registration given pair code after tally and before pay received its drip, and was prunable afterwards); and on an EIP-7702 chain an EOA registered codeless can carry pair-shaped delegated code between tallies and clear it (code length back to 0) before the next tally, so _shapeChanged reads false. The harm is bounded: a pool earns in proportion to the PIMD it holds, the same as a wallet with that bag, and the NatSpec at line 623-627 already scopes the probe to 'V2/V3-style' pools. Fixing (a) and (c) is a scope decision rather than a patch: a probe the target can detect cannot be made reliable, so either document _isPool as a convenience filter and a trust limit, or exclude pools by allow-list/self-registration. For (b) and the 7702 case, recording EXTCODEHASH at registration and treating any change (including back to empty) as a shape change would help. Also confirmed for the brief's third question: prune's swap-and-pop is correct when the pruned holder is last (the slot is rewritten to itself, popped, then deleted) and a duplicated address in the accounts list is skipped on its second visit. Merged from four specialists (math, flow, permissions, economics).

**Reproduction**

Mock hook and pool manager, real token and engine, minBalance 1,000,000e18. Deploy a contract whose token0() returns msg.sender == engine ? address(0) : PIMD, and token1() likewise for IMD. Transfer 5,000,000e18 PIMD to it. register([pair]) succeeds (holderInfo shows registered). Mint 1,000e18 IMD to the engine, warp 2 days, fire(), tally(10), pay(10). Expected: a pair reporting PIMD as token0 collects nothing. Actual: imd.balanceOf(pair) is about 304e18 and prune([pair]) leaves it registered. The attached proof fails on this code with `a PIMD pair collected the holders' drip: 304223859391774029000 != 0`. Pay-after-tally window (full stack): register a codeless address L holding a full bag and alice; warp 2 days; fire; tally(500); etch pair code reporting PIMD as token0 at L; pay(500). Actual: imd.balanceOf(L) > 0; prune([L]) then removes it.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {ERC20} from "solmate/src/tokens/ERC20.sol";
import {PimdToken} from "src/pimd/PimdToken.sol";
import {PimdEngine} from "src/pimd/PimdEngine.sol";

contract MockIMD is ERC20("Identity.md", "IMD", 18) {
    function mint(address to, uint256 amount) external {
        _mint(to, amount);
    }
}

contract MockPoolManager {
    function exttload(bytes32) external pure returns (bytes32) {
        return bytes32(0);
    }
}

contract MockHook {
    address public engine;
    address public quote;
    address public token;
    address public poolManager;

    constructor(address quote_, address token_, address pm_) {
        quote = quote_;
        token = token_;
        poolManager = pm_;
    }

    function setEngine(address e) external {
        engine = e;
    }

    function holdersOwed() external pure returns (uint256) {
        return 0;
    }

    function flush() external pure returns (uint256, uint256) {
        return (0, 0);
    }

    function flushHolders() external pure returns (uint256) {
        return 0;
    }
}

/// A V2-shaped pair for PIMD/IMD that carries code from the moment it is registered. It reports PIMD as
/// `token0` to every caller except the engine, whose probe is a staticcall from a known address. Routers,
/// explorers and LPs see an ordinary pair; `_isPool` sees nothing. Nothing in it ever changes shape, so
/// `_shapeChanged` never fires either, and it is never prunable.
contract PairThatHidesFromTheEngine {
    address immutable pimd;
    address immutable imd;
    address immutable engine;

    constructor(address pimd_, address imd_, address engine_) {
        pimd = pimd_;
        imd = imd_;
        engine = engine_;
    }

    function token0() external view returns (address) {
        return msg.sender == engine ? address(0) : pimd;
    }

    function token1() external view returns (address) {
        return msg.sender == engine ? address(0) : imd;
    }
}

/// Finding: `_isPool` is a selector probe the probed contract answers, so a pool that carries code from the
/// start evades it by answering the engine differently, by starting with a non-matching `token0` and
/// changing it later, or by not exposing `token0`/`token1` at all. `_shapeChanged` only watches codeless
/// registrations, so none of these ever lose weight or become prunable.
contract PoolProbeEvasionTest is Test {
    uint256 constant MIN = 1_000_000e18;

    MockIMD imd;
    MockPoolManager pm;
    PimdToken token;
    MockHook hook;
    PimdEngine engine;
    address team = makeAddr("team");
    address keeper = makeAddr("keeper");

    function setUp() public {
        imd = new MockIMD();
        pm = new MockPoolManager();
        token = new PimdToken();
        hook = new MockHook(address(imd), address(token), address(pm));
        engine = new PimdEngine(
            PimdEngine.Config({
                poolManager: address(pm),
                imd: address(imd),
                team: team,
                binder: address(this),
                dripBpsPerPeriod: 150,
                minInterval: 2 minutes,
                minBalance: MIN,
                fireTip: 0.05e18,
                tipPerHolder: 0.003e18,
                maxCatchup: 6 hours,
                maxHolders: 1_200
            })
        );
        hook.setEngine(address(engine));
        engine.bind(address(token), address(hook), new address[](0));
    }

    function test_a_pair_that_answers_the_engine_differently_is_registered_paid_and_unprunable() public {
        PairThatHidesFromTheEngine pair = new PairThatHidesFromTheEngine(address(token), address(imd), address(engine));
        // To everyone else it is a PIMD pair.
        vm.prank(makeAddr("anyRouter"));
        assertEq(pair.token0(), address(token), "every other caller sees a PIMD pair");

        // The pair holds pooled PIMD, exactly the bag `_isPool` exists to keep out of the drip.
        token.transfer(address(pair), 5 * MIN);
        address[] memory one = new address[](1);
        one[0] = address(pair);
        engine.register(one);
        (bool registered,,,,) = engine.holderInfo(address(pair));
        assertTrue(registered, "the probe passed a pair that carries pair code from the start");

        // Income arrives and the streak matures.
        imd.mint(address(engine), 1_000e18);
        vm.warp(vm.getBlockTimestamp() + 2 days);
        vm.startPrank(keeper);
        engine.fire();
        engine.tally(10);
        engine.pay(10);
        vm.stopPrank();

        // And nobody can take it back out: it never changed shape, and the probe still says it is not a pool.
        engine.prune(one);
        (registered,,,,) = engine.holderInfo(address(pair));
        assertTrue(registered, "prune cannot remove it either");

        // Expected per the design: "a rogue V2/V3-style pool must not collect drips". Actual: it was paid.
        assertEq(imd.balanceOf(address(pair)), 0, "a PIMD pair collected the holders' drip");
    }
}
```

### 5. Low: An epoch in which every holder weighs zero still pays the fire and tally keeper tips out of the pot

`src/pimd/PimdEngine.sol:354`

```
        _tip(fireTip);
```

fire() refuses to open an epoch and pays nothing when the set is empty (line 342, the fix for the previous review's M4), but it still opens one and pays fireTip (line 354) whenever holders.length > 0, even if no holder can carry weight: every holder in its first hour (tier 0), below minBalance on min(bal, lastBal), or caught by _shapeChanged. tally then finds tw == 0, returns epochQuote to the pot (lines 419-423) and still pays tipPerHolder * n (line 428). Both tips come out of the pot, bounded by the 5% tip budget of the drip, and no holder is paid in exchange. This is the natural state of the first hour after launch, when income is highest and every registered wallet is at tier 0: any keeper can call fire() + tally() every minInterval (2 minutes) and take min(fireTip + tipPerHolder * n, 5% of the drip) each time. It can also be forced later by a set whose only registered wallet is kept at tier 0 (moving 1 wei out before each tally restarts its streak). The loss is bounded to what a normal epoch would pay in tips, so this is low. Fix without touching the economics: pay the fire tip only once tally finds tw > 0 (e.g. defer it to the Pay phase), or skip both tips when tw == 0, so a keeper is paid for an epoch only when the epoch pays somebody.

**Reproduction**

Full stack, test config (fireTip 0.02e18, tipPerHolder 0.0005e18, drip 400 bps per 15 min). Past the launch cap, alice buys 200 IMD of PIMD, register([alice]), bob calls hook.flush() so the IMD is at the engine. Warp 10 minutes (alice is under 1 hour, tier 0). Keeper calls fire() then tally(500). Expected: phase returns to Idle with nothing paid and the pot unchanged. Actual (forge run): phase is Idle, alice holds no IMD, and the keeper received 9.5117e15 IMD from the pot (fireTip + tipPerHolder, under the 5% budget). Two minutes later the same pair of calls pays the keeper again.

### 6. Low: A stranger can trigger _shapeChanged on a counterfactual smart-wallet holder: zero weight, then prune and a streak reset

`src/pimd/PimdEngine.sol:620`

```
        return h.vettedCodeless && a.code.length != 0;
```

Answer to the brief's third question (can prune be aimed at a holder who should keep earning): yes, through code the holder did not deploy. Counterfactual smart accounts (ERC-4337 account factories, Safe via its proxy factory) have an address before deployment, receive PIMD while codeless, and can be deployed by anyone through the public factory with the owner's own parameters. A rival (1) registers the victim's undeployed address, which register() permits for any address and which sets vettedCodeless = true, then (2) once the victim's streak has matured, calls the factory to deploy the victim's own wallet. From the next tally the victim's weight is 0 (line 411 via line 620) and the rival's relative share rises; in the next Idle window anyone can prune the victim (line 300), which deletes streakStart. Re-registering restarts the clock at 0x for an hour and 0.5x for a day, so a 3x holder loses about 14 days of tier. Cost: one account deployment plus a prune. Nothing is permanently stuck (the holder can be pruned and re-registered, which also answers the brief's second question: every _shapeChanged state is prunable), which is why this is low. Mitigations that keep the pair defence: only allow self-registration of a codeless address, so a stranger cannot set vettedCodeless on someone else's counterfactual wallet; or let prune followed by re-register keep streakStart when the only change is code arriving and the new code passes _isPool. (Specialist: permissions.)

**Reproduction**

Full stack. A CREATE2 account factory with permissionless createAccount(owner). victim = factory.getAddress(victimOwner), undeployed, holds bob's full bag (about 80M PIMD); alice holds a similar bag. register([alice]); register([victim]). Warp 15 days (both at 3x); run an epoch: the victim is paid and holderInfo shows tier 30,000. A rival calls factory.createAccount(victimOwner), which deploys exactly the victim's wallet (owner() == victimOwner). Warp 1 hour, run another epoch. Expected: the victim keeps earning. Actual (forge run): the victim's IMD balance does not change (weight 0), and engine.prune([victim]) by anyone removes it, erasing the 15-day streak.

### 7. Low: The launch value of maxHolders (1,200) exceeds what a whole-set tally can execute inside Robinhood's 32M per-transaction gas cap

`script/DeployPimd.s.sol:64`

```
            maxHolders: vm.envOr("MAX_HOLDERS", uint256(1_200))
```

maxHolders exists so the atomic tally always fits in one transaction (PimdEngine.sol:85-90). The constructor only caps it at 5,000 (line 182), and the deploy script chooses 1,200 on the stated basis that 'Robinhood Chain takes [42M] without noticing (its block limit is 2^50)' (lines 59-63). That 2^50 is the placeholder gasLimit Arbitrum-family nodes put in the block header (confirmed: `cast block latest` on Robinhood reports 1125899906842624); the executable budget is ArbOS's maxTxGasLimit, which Robinhood's ArbGasInfo precompile (0x6C, getGasAccountingParams) reports as 32,000,000 (speed limit 7M/s, gasPoolMax 32M). The engine the hook names on chain (0x8974d07239e6D8B843eE70725823E7e95CbB6924) reports maxHolders 1,200 and minBalance 1,000,000e18. Measured on this code, tally costs about 33.5k gas per weighted holder (the zero-to-nonzero weight SSTORE dominates and recurs every epoch because pay zeroes it), so a tally of 1,000 weighted holders needs 33,529,657 gas and cannot execute on Robinhood; the ceiling is about 950 weighted holders. Past it the epoch sits in Tally, pay refuses (WrongPhase), after a day abortEpoch returns the IMD, the next fire opens an epoch stuck the same way, and prune cannot shrink the set because every holder keeps a bag at or above the minimum. There is no owner. Reachability is the caveat: at minBalance 1,000,000 PIMD, 950 weighted holders means 95% of the supply in qualifying wallets at once, an end state a fully bought-out pool can reach but not one an attacker can force (empty entries cost only 13.4k each: 1,199 empties plus one weighted holder tallied in 16.1M), so this is low. The fix is a number, not code: a maxHolders that leaves headroom under 32M at the measured per-holder cost (about 900 with margin), or a constructor check tying the bound to a measured gas budget, and the script comment corrected. The engine's NatSpec also refers to a GAS.md that is not in the tree. (Specialist: flow.)

**Reproduction**

Mock hook and pool manager, real token and engine with maxHolders 1,200 and minBalance 1,000,000e18 (the live values). 1,000 addresses each holding exactly 1,000,000e18 PIMD (the whole supply), all registered; 10,000e18 IMD at the engine; warp 2 days so every holder is at 1x. fire(), then measure gas around tally(1000). Expected: a set the bound permits is weighable in one Robinhood transaction (<= 32,000,000 gas). Actual (forge run of test/scratch/TallyGas.t.sol): 33,529,657 gas. On chain: `cast call 0x6C "getGasAccountingParams()(uint256,uint256,uint256)"` on Robinhood returns (7000000, 32000000, 32000000).

### 8. Low: Constructor accepts minBalance == 0, under which empty addresses register, earn nothing and can never be pruned

`src/pimd/PimdEngine.sol:189`

```
        minBalance = c.minBalance;
```

The constructor bounds dripBpsPerPeriod, maxCatchup and maxHolders but not minBalance. With minBalance = 0, register() accepts any address with a zero balance (bal < 0 is never true), tally computes eff = 0 and weight 0, and prune keeps the address because balanceOf(a) >= 0 is always true, _shapeChanged is false for a codeless address and _isPool is false. That is exactly the state the brief asks to rule out: a holder that earns nothing and cannot be pruned, in an engine with no owner; and since register is permissionless, anyone can fill the bounded set with such addresses and registration is dead for the life of the contract. Both deploy configurations set a positive minimum, but the script reads MIN_BALANCE from the environment (DeployPimd.s.sol:55) so a mis-set variable would ship it; the engine's own invariants ('a pooled bag does not fall below the minimum on its own', 'prune can take out anything that earns nothing') silently depend on minBalance >= 1. Fix: revert BadConfig when c.minBalance == 0. (Specialist: economics.)

**Reproduction**

Mock hook and pool manager, real token and engine constructed with minBalance = 0 and maxHolders = 2, bound. register([0x1111, 0x2222]) with both addresses holding no PIMD; then prune([0x1111, 0x2222]); then register([alice]) with alice holding 10,000,000e18 PIMD. Expected: BadConfig at construction, or the empty addresses are prunable. Actual (forge run): construction succeeds, holderCount is 2 after register, still 2 after prune, and alice's registration reverts HolderSetFull(2) permanently.

### 9. Info: The hold streak is enforced only at tally instants: a bag sent out and back (or sold and re-bought) between two tallies keeps its tier, contrary to the documented rule

`src/pimd/PimdEngine.sol:399`

```
            if (bal < last) {
```

The contract NatSpec (line 36) and the README (line 10) state that selling or sending PIMD out restarts the hold clock. tally only compares the balance at this tally with the balance recorded at the previous one, so anything that happens in between and is undone before the next tally is invisible: bal == last, the branch at line 399 is not taken, streakStart is unchanged, and min(bal, lastBal) is satisfied because the bag is back. With the keeper's intended 15-minute cadence the window is short, but the cadence is a keeper policy (the only floor is minInterval = 2 minutes and nothing forces a fire), so the window is however long the keeper is quiet. No profit path was found: a sell/re-buy round trip costs the 5.6% + 2.4% taxes plus the pool's 1.25% twice, a transfer out and back costs only gas but a borrowed bag carries no weight for the borrower under min(bal, lastBal), so this is a behaviour/documentation mismatch rather than an exploit. Either the documents should say the rule is evaluated at epoch boundaries, or the design would need per-transfer bookkeeping, which the token deliberately avoids. Merged from two specialists (flow, economics).

**Reproduction**

Full stack. alice registered, warp 15 days, run an epoch: holderInfo(alice).tierBps_ == 30,000. alice transfers her entire bag to bob (balance 0), bob transfers it back; 15 minutes later run another epoch. Expected per the documented rule: sending out restarts the clock, tier 0. Actual (forge run): tierBps_ is still 30,000 and she is weighed at 3x.

### 10. Info: The try/catch around the hook pull is safe against gas and return-data games, but both catch arms are silent, so IMD refusing the engine looks like a quiet market forever

`src/pimd/PimdEngine.sol:329`

```
                try hook.flushHolders() {} catch {}
```

Assessment the brief asked for. The pattern is sound for what it is meant to survive: hook.holdersOwed() is a plain getter on a contract bind verified has code, so the call outside the try cannot revert; both calls in the try are to the hook, which exists, so the no-code case that try/catch does not catch cannot occur; flush() and flushHolders() run no holder-controlled code (burn, take and an IMD transfer with no recipient callback), so neither can be made to exhaust gas; the 63/64 trick (giving fire just enough gas that the inner call runs out while the outer continues) is out of reach at Robinhood's 32M per-transaction cap; and the PoolManager is locked again before _book runs. The ordinary revert in flush (a refused team transfer) falls through to flushHolders as designed, and that path is now wired (the previous review's M2). What the pattern hides is a failure of the one address it cannot route around: if IMD ever refuses transfers to the engine itself (a blacklist, a pause, an upgrade that rejects contracts), both flush paths revert at PoolManager.take, fire swallows both, books nothing, drips the existing pot to zero and then returns early for ever while holdersOwed grows at the hook without bound. No function in the hook can move those claims anywhere but engine() and team(), and engine() is a source constant. That is a trust assumption on IMD's owner rather than a defect in this code, but it should be written down as one, and the catch arms could emit an event (carrying the revert data) so the condition is visible off-chain instead of looking like a quiet market, which is the kind of silent breakage the brief says has hidden one problem already. Merged from two specialists (flow, economics).

**Reproduction**

Full stack. alice registered, holdersOwed > 0 at the hook. vm.mockCallRevert on IMD transfer(engine, *). Warp 2 hours, keeper calls fire(). Expected: a hook-side problem delays income but is observable. Actual (forge run): fire() succeeds, hook.holdersOwed() is unchanged, engine.totalIncome() == 0, no epoch opens, and nothing records that both pulls failed.

### 11. Info: README describes the previous economics (3%/7% tax, 60/20/20 split, hook-side burn, launcher role, 100,000 PIMD minimum on Robinhood), which the code no longer has

`README.md:6`

```
- **3% on buys, 7% on sells**, taken in IMD by the hook
```

The README still states a 3% buy / 7% sell tax split 60% holders / 20% buy-and-burn / 20% team (lines 6-7, 27), a PimdHook.launcher one-shot role and hook.launch() (lines 28, 90), a hook that 'buys PIMD back and burns it' (line 19), the supply minting to the hook and the hook holding the position (lines 36-37), and a 100,000 PIMD minimum on Robinhood (line 104). The code at this commit taxes 2.4% / 5.6% split 75/25 (PimdHook.sol:63-65) with the burn funded by the pool fee outside the hook, has no launcher (the factory opens and seeds the pool), and DeployPimd.s.sol:55 sets the production minimum to 1,000,000 PIMD on Robinhood mainnet. Auditors and integrators reading the README check the wrong numbers. (Specialist: economics.)

**Reproduction**

Compare README.md lines 6-7, 27-28, 36-37, 90 and 104 with PimdHook.sol BUY_TAX_BPS = 240, SELL_TAX_BPS = 560, HOLDERS_BPS = 7_500, the absence of any launcher or launch() in PimdHook.sol, and DeployPimd.s.sol line 55. Expected: they agree. Actual: they do not.

---

Judge's submission `51b6aa4fa89fc80bddd2070758bf17bb1550d4a0ed4f85fc893af9e3819a3779`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
