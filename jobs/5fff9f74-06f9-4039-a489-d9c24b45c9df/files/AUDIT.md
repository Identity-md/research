# Audit report

> Audit the OverflowKeeper contract in this repository (Solidity 0.8.26, Foundry). Primary target: src/OverflowKeeper.sol, a Gnosis Safe MODULE. Also in scope: script/DeployKeeper.s.sol (pinned deploy). Read for context: src/LifeForceVault.sol and src/SvoStaking.sol (both immutable, deployed, separately audited: treat as fixed external contracts the keeper drives), src/Interfaces.sol (the reentrancy Guard mixin; 'Guard' here is NOT a Safe guard), KEEPER.md (design, authority limits, runbooks, prior review notes), STAKING.md, test/OverflowKeeper.t.sol, test/AdversarialKeeperA.t.sol, test/AdversarialKeeperB.t.sol (the last two were written by adversarial reviewers; their MockSafe models Safe 1.5.0 module semantics: GS104 revert when not enabled, inner failure returned as success=false with return data, optional module guard pre/post hooks). Out of scope: the hook, the token and the vault's own logic. Build/test: forge build && forge test --match-path 'test/*Keeper*'. Write nothing to the repository; deliver report.md with a machine-readable JSON appendix. Tone: factual; no claims of safety beyond the evidence; no investment language.
>
> DEPLOYMENT CONTEXT. Robinhood Chain, id 4663. The LifeForceVault 0x2001318118e1B3DF1e653E0999926bdAa48A5A52 holds IMD (0x5F7Bb59365ce557C26dbcAa4EE9d39A4b95B7127, an ERC-20 with a single-key owner, a blocked(address) blocklist and a transfer gate: treat as untrusted) split 70/30 into an inference reserve (pays for an AI voice service) and a buyback reserve; only the hard-coded REFUEL_SAFE 0xEb57c52272B90F989C41B739e2ccc5f00bF7697C (Safe v1.5.0 proxy, 2-of-3, no modules, no guards today) can call withdrawInference(amount), which sends IMD to that Safe. SvoStaking 0xe8ebB026Ff49f139aBc50C3Af64bdFebbF28f533 streams IMD it receives to SVO stakers over 7 days when anyone calls notify(); while a stream runs notify() reverts unless the new IMD is at least a tenth of what is left, and also reverts when the total is below 7 days of wei or above MAX_STREAM (1e40). Until now the Safe's owners had to sign a batch (withdraw, transfer, notify) to move the overflow, and twice it got stuck in the Safe queue.
>
> WHAT IT DOES. Once the Safe's owners enable the keeper as a module (enableModule, one 2-of-3 tx), sweep() is permissionless: amount = vault.inferenceReserve() - full (full = 25 IMD at deploy; setFull and setMinSweep are callable only by the Safe); it reverts NothingToSweep below minSweep (1 IMD) and Blocked when IMD's blocked() is non-zero for the vault, the Safe or the staking contract. Through execTransactionFromModuleReturnData (operation 0 only) it makes the Safe call vault.withdrawInference(amount), checks the Safe's IMD balance rose by exactly amount (else SafeBalanceMismatch), makes the Safe transfer FEE_BPS = 50 (0.5%) of it to msg.sender and the rest to the staking contract, checks the Safe's balance is back to where it started, then calls staking.notify() itself only if a mirror of notify()'s checks (including the fold of emission that ran while nobody was staked) says it will pass; otherwise the IMD waits in the staking contract for a later sweep or a direct notify(). preview() predicts all of this. No owner, no upgrade, holds no tokens, nonReentrant. MIN_SWEEP_FLOOR = 7 days * 10000 / 9950 + 1 wei. The constructor checks vault.REFUEL_SAFE(), vault.IMD(), staking.rewardToken() == IMD and staking.token() == vault.token().
>
> AUDIT SCOPE. (1) SECURITY: every path by which the module could make the Safe move more than the computed overflow, touch the Safe's own IMD, ETH or other tokens, delegatecall, or change the Safe's configuration; the balance-check invariant against a fee-on-transfer, false-returning, callback-making, rebasing or blocklisting IMD and against a Safe or module guard that reports success for a failed inner call; the view-vs-execution reserve math (the vault's checkpoint and shortfall clamp) and whether withdrawInference can ever revert or leave the reserve different from full; the notify() mirror (every revert branch of SvoStaking.notify(), including undistributed, lastUpdate before the first stream, periodFinish == now, the leftover/10 boundary, dust and MAX_STREAM): can the keeper call a notify() that reverts, or park IMD that would have streamed, and can parked IMD be stranded; fee economics (fee farming, timing, sandwiching around fee arrivals, repeated minimal sweeps, stretching the staking stream horizon); griefing or DoS of sweep() and of the Safe; reentrancy via the fee transfer, IMD callbacks or notify(); front-running of the Safe's own setFull/disableModule; the moment enableModule executes (any overflow present is sweepable at once); Safe 1.5.0 ModuleManager semantics (GS104, return data, module guard checkModuleTransaction/checkAfterModuleExecution, SafeL2 events) and whether the MockSafe in the tests hides anything; the deploy script (chain pin, constants, exact-value overrides ALLOW_OTHER_FULL/ALLOW_OTHER_MIN_SWEEP, wei floors, read-back). (2) COMPLIANCE: do code, NatSpec, KEEPER.md and STAKING.md match behaviour; list every claim the code does not enforce; centralisation powers (the Safe's setFull, setMinSweep, disableModule; IMD owner's blocklist). (3) CODE QUALITY: NatSpec and event accuracy, low-level calls, gas, test gaps, anything the three prior reviews missed.
>
> STANDARDS. Safe module security guidance (modules bypass the owner threshold; least authority); SWC Registry; Consensys Smart Contract Best Practices; OWASP Smart Contract Top 10; ERC-20 non-standard behaviour (compare OpenZeppelin SafeERC20).
>
> ALREADY REVIEWED (2026-10-20, three independent AI adversarial reviews, no critical or high findings; fixes applied, see KEEPER.md 'Review notes'). Verify each fix and try to break it: (1) SafeBalanceMismatch invariant (exactly amount arrives; the Safe ends where it started); (2) constructor refuses a staking contract for another token; (3) blocked() read tolerates non-bool answers (any non-zero word = blocked, missing function = not blocked); (4) MIN_SWEEP_FLOOR grossed up for the fee; (5) the notify() mirror folds emission with nobody staked exactly as _updateGlobal does; (6) preview().ready covers the vault, the Safe and the staking contract.
>
> KNOWN AND ACCEPTED (do not report as new, but dispute them if you disagree). The 0.5% fee on a 1 IMD sweep is dust, so the team or a cron is the realistic caller. Each sweep that meets the tenth rule re-spreads the remainder over a fresh week (the staking contract's design); stakers lose nothing in total. A sweep under the tenth rule parks IMD in the staking contract until a later sweep or the stream's end; anyone may call notify() directly. The Safe's owners can set full to 0 (sweep everything) or huge (pause); that is Safe policy, no worse than the Safe's existing power to withdraw everything by hand. setFull/disableModule are visible before execution and a sweep can land first at the old level. A look-alike vault or staking contract can satisfy the constructor's identity checks; the deploy script pins the real addresses and the enable runbook requires each signer to read vault()/staking()/full() back before signing. IMD blocking the Safe or the vault makes every withdrawal fail, keeper or not.
>
> REPORT FORMAT. Summary with overall risk rating and counts by severity; findings table (ID, severity, category, file:line, title) most severe first; per finding a concrete exploit or failing Foundry test, impact, fix and confidence; what was checked and found fine; assumptions; JSON appendix [{id, severity, category, file, line, title, status}]. No generic advice.

| | |
|---|---|
| Repository | https://github.com/SovrnOne/sovrn-contracts.git |
| Commit | `90746ea5aa7aea70ad73eb0d6630ed96303af955` |
| Job | `5fff9f74-06f9-4039-a489-d9c24b45c9df` |
| Judged | 2026-10-20 23:57 UTC |
| Findings | 3 low · 3 info |

Four agents audited the code as it is at `90746ea`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Low: sweep() always reverts SafeBalanceMismatch when the refuel Safe itself is the caller (fee is a Safe-to-Safe self-transfer)

`src/OverflowKeeper.sol:149`

```
        if (end != start) revert SafeBalanceMismatch(start, end);
```

sweep() pays FEE_BPS of the withdrawn amount to msg.sender (line 146) and then requires the Safe's IMD balance to equal its starting balance (line 149). When msg.sender is SAFE (an owner-signed Safe transaction calling sweep(), e.g. enableModule + first supervised sweep in one batch, or the admin page used inside the Safe app), the fee leg moves IMD from the Safe to the Safe, so the Safe ends with start + fee and the whole sweep reverts. Nothing is lost (atomic revert), but the one party that owns the module can never sweep through it. This is not mentioned in the NatSpec ('permissionless', 'anyone') or KEEPER.md Runbook C step 5 ('sweep() from any wallet'). Merged from four specialist reports (audit_math, audit_flow, audit_economics, audit_permissions). Fix: `fee = msg.sender == SAFE ? 0 : amount * FEE_BPS / BPS;` (the existing `if (fee != 0)` then skips the self-transfer and the end == start invariant holds unchanged), or document the exclusion. Verified: with that one-line change the proof passes and the existing 46 keeper tests still pass.

**Reproduction**

State: keeper enabled as a module, vault holds 100 IMD synced (inference 70, full 25, overflow 45), Safe IMD balance 0. Input: the Safe calls keeper.sweep() as an ordinary call. Expected: sweep succeeds, reserve back at 25 IMD, staking receives >= 44.775 IMD. Actual: revert SafeBalanceMismatch(0, 225000000000000000). The same call from any other address succeeds. `forge test --match-path test/scratch/KeeperSafeCaller.t.sol` fails with exactly that error on the current code.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {LifeForceVault} from "src/LifeForceVault.sol";
import {SvoStaking} from "src/SvoStaking.sol";
import {SovrnToken} from "src/SovrnToken.sol";
import {OverflowKeeper} from "src/OverflowKeeper.sol";

/// @dev Plain ERC-20 stand-in for IMD, etched at IMD's real address. Exact transfers, returns true, no fee, no hooks.
contract PlainIMD {
    mapping(address => uint256) public balanceOf;
    uint256 public totalSupply;

    function mint(address to, uint256 amount) external {
        balanceOf[to] += amount;
        totalSupply += amount;
    }

    function transfer(address to, uint256 amount) external returns (bool) {
        balanceOf[msg.sender] -= amount;
        balanceOf[to] += amount;
        return true;
    }
}

/// @dev The slice of Safe 1.5.0 a module uses: GS104 when not enabled, inner failure returned as success=false.
contract MiniSafe {
    mapping(address => bool) public enabled;

    function enableModule(address m) external {
        enabled[m] = true;
    }

    function disableModule(address m) external {
        enabled[m] = false;
    }

    function isModuleEnabled(address m) external view returns (bool) {
        return enabled[m];
    }

    function execTransactionFromModuleReturnData(address to, uint256 value, bytes calldata data, uint8 operation)
        external
        returns (bool success, bytes memory returnData)
    {
        require(enabled[msg.sender], "GS104");
        require(operation == 0, "call only");
        (success, returnData) = to.call{value: value}(data);
    }

    /// @dev The Safe executing an ordinary (owner-signed) transaction: a plain call from the Safe's address.
    function exec(address to, bytes calldata data) external returns (bytes memory) {
        (bool ok, bytes memory ret) = to.call(data);
        if (!ok) {
            assembly {
                revert(add(ret, 0x20), mload(ret))
            }
        }
        return ret;
    }
}

contract KeeperSafeCallerTest is Test {
    address internal constant SAFE = 0xEb57c52272B90F989C41B739e2ccc5f00bF7697C;
    address internal constant IMD = 0x5F7Bb59365ce557C26dbcAa4EE9d39A4b95B7127;
    uint256 internal constant FULL = 25 ether;
    uint256 internal constant MIN_SWEEP = 1 ether;

    SovrnToken internal token;
    LifeForceVault internal vault;
    SvoStaking internal staking;
    OverflowKeeper internal keeper;
    PlainIMD internal imd;
    MiniSafe internal safe;

    function setUp() public {
        vm.chainId(4663);
        vm.etch(IMD, address(new PlainIMD()).code);
        imd = PlainIMD(IMD);
        vm.etch(SAFE, address(new MiniSafe()).code);
        safe = MiniSafe(SAFE);
        token = new SovrnToken();
        // The vault's constructor only needs code at the manager address and a non-zero hook address.
        bytes memory creation =
            abi.encodePacked(type(LifeForceVault).creationCode, abi.encode(address(token), address(token), address(0xbeef)));
        address v;
        assembly {
            v := create(0, add(creation, 0x20), mload(creation))
        }
        require(v != address(0), "vault deploy");
        vault = LifeForceVault(v);
        staking = new SvoStaking(token, IMD, address(this));
        keeper = new OverflowKeeper(vault, staking, FULL, MIN_SWEEP);
        safe.enableModule(address(keeper));
        // One staker so streamed IMD has somewhere to go.
        token.approve(address(staking), type(uint256).max);
        staking.stake(1_000_000 ether);
        // 100 IMD arrives at the vault: inference 70, overflow 45 over full = 25.
        imd.mint(address(vault), 100 ether);
        vault.sync();
        assertEq(keeper.overflow(), 45 ether);
    }

    /// The refuel Safe itself (an owner-signed Safe transaction, e.g. enableModule + sweep in one batch, or the
    /// admin page button used inside the Safe app) calls sweep(). The fee leg is a Safe-to-Safe self transfer, so the
    /// Safe ends the sweep holding the fee, and the "Safe ends where it started" check reverts the whole sweep with
    /// SafeBalanceMismatch(start, start + fee). Expected: the Safe can run a sweep like any other caller.
    function test_safeItselfCanSweep() public {
        (,,,, bool ready) = keeper.preview();
        assertTrue(ready, "preview says the sweep is ready");
        uint256 safeBefore = imd.balanceOf(SAFE);
        // Currently reverts: SafeBalanceMismatch(0, 0.225 ether).
        safe.exec(address(keeper), abi.encodeCall(OverflowKeeper.sweep, ()));
        assertEq(vault.inferenceReserve(), FULL, "reserve back at full");
        assertGe(imd.balanceOf(address(staking)), 44.775 ether, "stakers got at least the rest");
        assertGe(imd.balanceOf(SAFE), safeBefore, "the Safe did not pay anything of its own");
    }
}
```

### 2. Low: preview().ready is true while the keeper is not an enabled module, although sweep() then reverts GS104

`src/OverflowKeeper.sol:124`

```
        ready = amount >= minSweep && !_anyBlocked();
```

The preview() NatSpec (lines 113-115) says `ready` is false when sweep() would revert, and KEEPER.md review note (6) presents ready as covering the parties. `ready` checks only minSweep and the three blocked() reads; it never reads Safe.isModuleEnabled(address(this)). Before enableModule executes, and after disableModule (the documented off switch), preview() returns ready=true and willNotify=true while every sweep() reverts with the Safe's GS104. A cron or the admin page polling preview() keeps sending reverting transactions, and an operator cannot tell from preview() that the module is off. The same gap applies to an IMD transfer gate that does not flag addresses in blocked() (already shown by AdversarialKeeperB test_F5; not fixed). Merged from audit_math, audit_flow and audit_permissions. Fix: add `isModuleEnabled(address) external view returns (bool)` to ISafeModuleManager (present on Safe 1.5.0) and AND it into `ready`, ideally via a tolerant staticcall: the MockSafes in test/OverflowKeeper.t.sol and test/AdversarialKeeper{A,B}.t.sol do not implement isModuleEnabled, so a plain interface call makes preview() revert in 16 existing tests (checked); either read it tolerantly or add the function to those mocks. Otherwise narrow the NatSpec.

**Reproduction**

State: vault inference 70 IMD, full 25, overflow 45, nothing blocked, keeper NOT enabled (or disabled again) on the Safe. Call keeper.preview(): returns ready=true. Call keeper.sweep(): reverts Error("GS104"). Expected per NatSpec: ready=false. `forge test --match-path test/scratch/KeeperPreviewModule.t.sol` fails with 'ready should be false when sweep() would revert'; with the fix it passes (it also checks ready=true and a working sweep once re-enabled).

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {LifeForceVault} from "src/LifeForceVault.sol";
import {SvoStaking} from "src/SvoStaking.sol";
import {SovrnToken} from "src/SovrnToken.sol";
import {OverflowKeeper} from "src/OverflowKeeper.sol";

/// @dev Plain ERC-20 stand-in for IMD, etched at IMD's real address. Exact transfers, returns true, no fee, no hooks.
contract PlainIMD {
    mapping(address => uint256) public balanceOf;
    uint256 public totalSupply;

    function mint(address to, uint256 amount) external {
        balanceOf[to] += amount;
        totalSupply += amount;
    }

    function transfer(address to, uint256 amount) external returns (bool) {
        balanceOf[msg.sender] -= amount;
        balanceOf[to] += amount;
        return true;
    }
}

/// @dev The slice of Safe 1.5.0 a module uses: GS104 when not enabled, inner failure returned as success=false.
contract MiniSafe {
    mapping(address => bool) public enabled;

    function enableModule(address m) external {
        enabled[m] = true;
    }

    function disableModule(address m) external {
        enabled[m] = false;
    }

    function isModuleEnabled(address m) external view returns (bool) {
        return enabled[m];
    }

    function execTransactionFromModuleReturnData(address to, uint256 value, bytes calldata data, uint8 operation)
        external
        returns (bool success, bytes memory returnData)
    {
        require(enabled[msg.sender], "GS104");
        require(operation == 0, "call only");
        (success, returnData) = to.call{value: value}(data);
    }

    /// @dev The Safe executing an ordinary (owner-signed) transaction: a plain call from the Safe's address.
    function exec(address to, bytes calldata data) external returns (bytes memory) {
        (bool ok, bytes memory ret) = to.call(data);
        if (!ok) {
            assembly {
                revert(add(ret, 0x20), mload(ret))
            }
        }
        return ret;
    }
}

contract KeeperPreviewModuleTest is Test {
    address internal constant SAFE = 0xEb57c52272B90F989C41B739e2ccc5f00bF7697C;
    address internal constant IMD = 0x5F7Bb59365ce557C26dbcAa4EE9d39A4b95B7127;
    uint256 internal constant FULL = 25 ether;
    uint256 internal constant MIN_SWEEP = 1 ether;

    SovrnToken internal token;
    LifeForceVault internal vault;
    SvoStaking internal staking;
    OverflowKeeper internal keeper;
    PlainIMD internal imd;
    MiniSafe internal safe;

    function setUp() public {
        vm.chainId(4663);
        vm.etch(IMD, address(new PlainIMD()).code);
        imd = PlainIMD(IMD);
        vm.etch(SAFE, address(new MiniSafe()).code);
        safe = MiniSafe(SAFE);
        token = new SovrnToken();
        // The vault's constructor only needs code at the manager address and a non-zero hook address.
        bytes memory creation =
            abi.encodePacked(type(LifeForceVault).creationCode, abi.encode(address(token), address(token), address(0xbeef)));
        address v;
        assembly {
            v := create(0, add(creation, 0x20), mload(creation))
        }
        require(v != address(0), "vault deploy");
        vault = LifeForceVault(v);
        staking = new SvoStaking(token, IMD, address(this));
        keeper = new OverflowKeeper(vault, staking, FULL, MIN_SWEEP);
        safe.enableModule(address(keeper));
        // One staker so streamed IMD has somewhere to go.
        token.approve(address(staking), type(uint256).max);
        staking.stake(1_000_000 ether);
        // 100 IMD arrives at the vault: inference 70, overflow 45 over full = 25.
        imd.mint(address(vault), 100 ether);
        vault.sync();
        assertEq(keeper.overflow(), 45 ether);
    }

    /// preview().ready is true while the module is not enabled, although sweep() reverts GS104.
    function test_previewReadyWhileModuleDisabled() public {
        safe.disableModule(address(keeper));
        (,,,, bool ready) = keeper.preview();
        vm.expectRevert("GS104");
        keeper.sweep();
        assertFalse(ready, "ready should be false when sweep() would revert");
        // Once enabled again, preview() must report ready and the sweep must work.
        safe.enableModule(address(keeper));
        (,,,, ready) = keeper.preview();
        assertTrue(ready, "ready once enabled");
        keeper.sweep();
    }
}
```

### 3. Low: DeployKeeper's ALLOW_OTHER_FULL / ALLOW_OTHER_MIN_SWEEP are plain overrides, not the exact-value confirmation the comment claims

`script/DeployKeeper.s.sol:38`

```
        uint256 full = vm.envOr("ALLOW_OTHER_FULL", DEFAULT_FULL);
```

The header (lines 16-18) says a different value 'is taken only when ALLOW_OTHER_FULL / ALLOW_OTHER_MIN_SWEEP names that exact wei value, so a leftover rehearsal variable cannot apply by accident', citing the DeployStaking pattern. In DeployStaking the value comes from one variable and the override must repeat it (`vm.envOr("ALLOW_OTHER_FUNDER", address(0)) == funder`). Here the override variable is itself the value: whatever ALLOW_OTHER_FULL holds is deployed, with no second variable to match. So a leftover rehearsal value (e.g. ALLOW_OTHER_FULL=1000000000000000000 from a test run) does apply, exactly the case the comment says is impossible. The only remaining guards are the console WARNING line, the >= 1 IMD / >= 0.1 IMD unit floors and full > minSweep, plus the KEEPER.md runbook step `env | grep ALLOW_OTHER` must be empty. Impact is limited: the keeper is harmless until enabled and signers must read full() back before enabling, but a full that is set too low makes the first sweep after enableModule move IMD above that level at once (KEEPER.md 'any overflow present is sweepable at once'). Fix: read the setting from FULL / MIN_SWEEP, and accept a non-default value only when `vm.envOr("ALLOW_OTHER_FULL", uint256(0)) == full` (likewise for minSweep), or correct the comment.

**Reproduction**

With a leftover `export ALLOW_OTHER_FULL=1000000000000000000` (1 IMD) in the shell, run the script on chain 4663: line 38 sets full = 1e18, the checks at lines 40-42 pass (1e18 >= 1 ether; 1e18 > 1e18 fails only if minSweep is also 1e18, so with ALLOW_OTHER_MIN_SWEEP=1e17 both pass), and the keeper is deployed with full = 1 IMD after only a console WARNING. Expected per lines 17-18: the leftover variable is refused unless a second value names it. Actual: it is applied. Verified by reading the code against DeployStaking.s.sol lines 46-49.

### 4. Info: IMD above MAX_STREAM is forwarded and 'parked' but can never be notified again: stranded in SvoStaking, contradicting 'Never stuck'

`src/OverflowKeeper.sol:147`

```
        _safeTransfer(address(staking), toStakers);
```

sweep() forwards toStakers unconditionally, then calls notify() only if the mirror passes. notify() reverts when added + leftover + undistributed > MAX_STREAM (1e40). None of those terms can fall without a successful notify(): `added` = balance - rewardsReserved (claims lower both), and undistributed only changes inside notify(). Once the total exceeds 1e40, every notify() reverts InvalidAmount forever and the IMD has no exit (claim pays only streamed rewards). The keeper computes that total in its mirror and still forwards. Requires about 1e22 IMD at the staking contract, so there is no practical impact at real supply; recorded because the NatSpec 'Never stuck ... the next sweep that meets the threshold streams it' and KEEPER.md's 'never stranded' are not enforced at this bound. Fix (optional): revert in sweep() when the mirror's total would exceed MAX_STREAM, and name the bound in the docs.

**Reproduction**

Scratch test test/scratch/KeeperStranded.t.sol::test_parkedAboveMaxStreamIsStranded (passes on current code, demonstrating the behaviour): nobody staked; 0.95e40 IMD minted to SvoStaking and notify(); warp 7 days + 1 s (whole stream folds into undistributed); mint 0.1e40 IMD to the vault. preview() -> ready=true, willNotify=false; sweep() succeeds and parks toStakers (unnotified == toStakers). Then stake 1,000,000 SVO, warp 70 days: staking.notify() still reverts InvalidAmount.

### 5. Info: KEEPER.md test count and gas figures do not match the repository (46 tests, ~354k / ~187k gas)

`KEEPER.md:114`

```
no delegatecall path, gas (~295k with notify, ~97k parked).
```

KEEPER.md lines 5 and 44 say 47 Foundry tests; `forge test --match-path 'test/*Keeper*'` runs 46 (14 + 13 + 17 + 2). Line 114 quotes ~295k gas with notify and ~97k parked; the suite's own measurement (AdversarialKeeperA test_sound_sweepGas) logs 353,947 and 187,012. The fee-economics reasoning is unaffected in direction, but the operators' reference is stale. Merged from audit_math and audit_flow. Fix: update the figures after the final code.

**Reproduction**

Run `forge test --match-path 'test/*Keeper*' -vv` (without test/scratch): 4 suites, 46 tests passed; logs 'sweep gas (notify path): 353947' and 'sweep gas (park path): 187012'. Expected per KEEPER.md: 47 tests, ~295k / ~97k.

### 6. Info: Deploy script says a not-yet-enabled keeper reverts SafeCallFailed; it reverts with the Safe's GS104 string

`script/DeployKeeper.s.sol:14`

```
///   SafeCallFailed (the Safe answers GS104) and nothing can move. The Safe can disableModule() at any time.
```

When the module is not enabled, Safe 1.5.0 reverts inside execTransactionFromModuleReturnData with Error("GS104"); that revert bubbles out of the keeper unchanged. SafeCallFailed is only raised when the Safe returns success=false. The keeper's own NatSpec (line 206), KEEPER.md Runbook D and test/OverflowKeeper.t.sol (vm.expectRevert("GS104")) say GS104. Tooling that matches the SafeCallFailed selector to detect 'not enabled' will never match. Fix: reword the comment.

**Reproduction**

Keeper deployed, not enabled, overflow 45 IMD; keeper.sweep() reverts Error("GS104"), not SafeCallFailed(bytes) (asserted by test_sweepRefusesWhenNotEnabledAndWorksOnceEnabled in test/OverflowKeeper.t.sol and by test/scratch/KeeperPreviewModule.t.sol).

---

Judge's submission `fc315fb2a2bad1fff100c18720781c265a7348c8541365934a53bf243cce511d`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
