# Audit report

> Audit the contracts in 0xtenang/Runner as they are.

| | |
|---|---|
| Repository | https://github.com/0xtenang/Runner.git |
| Commit | `556c9205a52556d2e6da958ba1a9e225ad439083` |
| Job | `b58971f0-f89e-49cb-9d55-16b30b3f1237` |
| Judged | 2026-10-25 11:16 UTC |
| Findings | 2 low · 2 info |

Four agents audited the code as it is at `556c920`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Low: RunnerHook constructor accepts a feeRecipient that setFeeRecipient() rejects (the PoolManager or the hook itself); protocol IMD collected before the owner corrects it is lost

`contracts/RunnerHook.sol:176`

```
        if (address(poolManager_) == address(0) || imd == address(0) || owner_ == address(0) || feeRecipient_ == address(0)) {
```

setFeeRecipient() (contracts/RunnerHook.sol:429-434) refuses address(0), address(this) and address(poolManager) because IMD taken to the hook is stuck (the hook has no function that moves its own ERC-20 balance) and IMD taken to the PoolManager vanishes (a PoolManager->PoolManager transfer leaves no delta or claim). The constructor only checks feeRecipient_ != address(0), so the same two values are accepted at deployment. Both are plausible deploy-script mistakes: poolManager_ is the first constructor argument and the hook's own address is known before deployment because the CREATE2 salt is mined for it. collectProtocolFees() is permissionless, so once a swap has produced a protocol fee anyone can trigger the loss before the owner notices: _collect() zeroes pendingProtocolFees, burns the hook's ERC-6909 claims and take()s the IMD to the bad recipient. The owner can repair feeRecipient afterwards with setFeeRecipient(), but every IMD collected before that is unrecoverable. Reviewer note: the same constructor/setter asymmetry exists in RunnerToken (constructor sets protocolWallet = initialOwner at contracts/RunnerToken.sol:192 without the this/poolManager/hook checks of setProtocolWallet() at line 503), but there the mis-deployment also puts the owner role on a contract that can never call anything, so it is immediately visible and is noted here rather than reported separately. Fix: apply the setter's check in the constructor, e.g. `if (feeRecipient_ == address(this) || feeRecipient_ == address(poolManager_)) revert ZeroAddress();` (address(this) is available in a constructor). Reproduced by running the attached proof: the first test fails on the current code (deployment succeeds with feeRecipient == poolManager) and the second test demonstrates the stranded 20 IMD.

**Reproduction**

Deploy RunnerHook via CREATE2 with feeRecipient_ = address(poolManager), all other arguments valid (start tick 142_600, salt mined for HOOK_FLAGS). Expected: the deployment reverts, as setFeeRecipient(address(poolManager)) does with ZeroAddress(). Actual: it succeeds and feeRecipient() == address(poolManager). Then: owner calls openPool(runner); alice buys with 1,000 IMD through RunnerRouter, so pendingProtocolFees(IMD) == 20e18; anyone calls collectProtocolFees(IMD). Expected: 20 IMD reach a recipient. Actual: pendingProtocolFees becomes 0, the hook's IMD claims drop by 20e18, the PoolManager's IMD ERC-20 balance is unchanged (transfer to itself) and no address holds a claim or delta for those 20 IMD. Verified with `FOUNDRY_TEST=test/scratch forge test --match-path test/scratch/HookFeeRecipientCtor.t.sol` (foundry.toml points `test` at contracts/test, so the override is needed): test_constructor_rejectsPoolManagerAsFeeRecipient FAILS (deployed address != 0), test_harm_protocolFeesLostToPoolManager PASSES, confirming the loss.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {PoolManager} from "v4-core/src/PoolManager.sol";

import {RunnerHook} from "contracts/RunnerHook.sol";
import {RunnerRouter} from "contracts/RunnerRouter.sol";

contract CtorIMD {
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;
    function mint(address to, uint256 amt) external { balanceOf[to] += amt; }
    function approve(address s, uint256 amt) external returns (bool) { allowance[msg.sender][s] = amt; return true; }
    function transfer(address to, uint256 amt) external returns (bool) { balanceOf[msg.sender] -= amt; balanceOf[to] += amt; return true; }
    function transferFrom(address f, address to, uint256 amt) external returns (bool) {
        if (allowance[f][msg.sender] != type(uint256).max) allowance[f][msg.sender] -= amt;
        balanceOf[f] -= amt; balanceOf[to] += amt; return true;
    }
}

/// @dev RunnerHook's constructor accepts a feeRecipient that setFeeRecipient() refuses (the PoolManager or the hook
///      itself). With feeRecipient == poolManager, collectProtocolFees() `take`s IMD to the PoolManager, where it is
///      unaccounted and lost. The constructor should apply the same check as the setter.
contract HookFeeRecipientCtorTest is Test {
    uint256 constant DAY = 1 days;
    address owner = makeAddr("owner");
    address team = makeAddr("team");
    address alice = makeAddr("alice");

    PoolManager pm;
    CtorIMD imd;

    function setUp() public {
        vm.warp(20_500 * DAY + 3600);
        pm = new PoolManager(address(this));
        imd = new CtorIMD();
    }

    function _flags() internal pure returns (uint160) {
        return uint160((1 << 13) | (1 << 11) | (1 << 7) | (1 << 6) | (1 << 5) | (1 << 3) | (1 << 2));
    }

    function _mine(bytes memory initCode) internal view returns (bytes32 salt, address hook) {
        bytes32 h = keccak256(initCode);
        for (uint256 i = 0; i < 2_000_000; i++) {
            hook = address(uint160(uint256(keccak256(abi.encodePacked(bytes1(0xff), address(this), bytes32(i), h)))));
            if (uint160(hook) & 0x3FFF == _flags()) return (bytes32(i), hook);
        }
        revert("no salt");
    }

    function _deploy(address feeRecipient_) internal returns (address deployed) {
        bytes memory initCode = abi.encodePacked(
            type(RunnerHook).creationCode,
            abi.encode(pm, address(imd), owner, feeRecipient_, int24(142_600), RunnerHook.ImdEthPool(10_000, 100, address(0)))
        );
        (bytes32 salt,) = _mine(initCode);
        assembly {
            deployed := create2(0, add(initCode, 0x20), mload(initCode), salt)
        }
    }

    /// Fails on the current code: the constructor accepts feeRecipient == poolManager, which setFeeRecipient rejects
    /// with ZeroAddress(). Passes once the constructor applies the same check (create2 then returns address(0)).
    function test_constructor_rejectsPoolManagerAsFeeRecipient() public {
        address deployed = _deploy(address(pm));
        assertEq(deployed, address(0), "constructor must refuse feeRecipient == poolManager like setFeeRecipient does");
    }

    /// Shows the harm on the current code: with feeRecipient == poolManager, protocol IMD is sent to the PoolManager
    /// and is unreachable by anyone (no delta, no claims), while pendingProtocolFees is zeroed. Once the constructor
    /// is fixed the deploy reverts and there is nothing to demonstrate, so the test returns early.
    function test_harm_protocolFeesLostToPoolManager() public {
        address deployed = _deploy(address(pm));
        if (deployed == address(0)) return;
        RunnerHook hook = RunnerHook(deployed);
        RunnerRouter router = RunnerRouter(hook.router());
        address runner = deployCode("RunnerToken.sol:RunnerToken", abi.encode(owner, address(hook), team, address(imd), address(pm)));
        vm.prank(owner);
        hook.openPool(runner);

        imd.mint(alice, 10_000e18);
        vm.startPrank(alice);
        imd.approve(address(router), type(uint256).max);
        router.buy(runner, 1_000e18, 0, block.timestamp);
        vm.stopPrank();
        assertEq(hook.pendingProtocolFees(address(imd)), 20e18);

        uint256 pmBefore = imd.balanceOf(address(pm));
        uint256 claimsBefore = pm.balanceOf(address(hook), uint256(uint160(address(imd))));
        hook.collectProtocolFees(address(imd));
        assertEq(hook.pendingProtocolFees(address(imd)), 0, "fees marked as paid");
        assertEq(imd.balanceOf(address(pm)), pmBefore, "IMD never left the PoolManager");
        assertEq(pm.balanceOf(address(hook), uint256(uint160(address(imd)))), claimsBefore - 20e18, "hook's claims burned");
        assertEq(pm.balanceOf(address(pm), uint256(uint160(address(imd)))), 0, "nobody holds a claim on the 20 IMD");
    }
}
```

### 2. Low: claimable() promises "what claim() would pay" but ignores the 20% instant burn and the TooManyLocks revert

`contracts/RunnerToken.sol:347`

```
    function claimable(address account, uint256 totalEarned) external view returns (uint256 amount) {
```

The NatSpec at contracts/RunnerToken.sol:343-346 says claimable() returns what claim() would pay right now and lists the conditions under which it returns 0 (paused, no emission, no signer, daily cap, empty pool). Two divergences remain: (1) an instant claim (claim(..., instant=true)) moves amount - amount*INSTANT_BURN_BPS/BPS = 80% to the runner and burns 20% (lines 388-391), while claimable() returns 100%; (2) a locked claim reverts TooManyLocks when the account already has MAX_ACTIVE_LOCKS (30) unfinished locks (line 394), while claimable() still returns the full amount. The in-app Earn tab computes its figure server-side, so the impact is limited to wallets, explorers and integrators that read claimable() on chain and show it as the amount that will arrive. Fix: give claimable() an `instant` parameter and apply the same burn (and return 0 when the account's active locks are at MAX_ACTIVE_LOCKS for the locked path), or reword the NatSpec to say it returns the gross difference before the instant burn and before the lock-slot check.

**Reproduction**

State: emission started, signer set, claimed[runner] = 0, run-reward pool full. Input: totalEarned = 1000e18 with a valid signer signature for instant = true, msg.sender = runner. Expected (per NatSpec): claimable(runner, 1000e18) equals what claim() pays. Actual: claimable() returns 1000e18; claim(runner, 1000e18, deadline, v, r, s, true) moves 800e18 to the runner and burns 200e18 (RewardsBurned). Verified with the attached proof: `FOUNDRY_TEST=test/scratch forge test --match-path test/scratch/ClaimableInstant.t.sol` fails with `800000000000000000000 != 1000000000000000000000`. Second input: submit 30 locked claims for alice (totalEarned 1e18, 2e18, ... 30e18), so locksOf(alice).activeLocks == 30; then claimable(alice, 31e18) returns 1e18 while claim(alice, 31e18, ..., false) reverts TooManyLocks(). Verified in test/scratch/Repro.t.sol::test_claimable_ignoresTooManyLocks (passes, i.e. the divergence is observed).

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";

/// @dev RunnerToken is compiled with solc 0.8.24, so it is reached through this interface and deployCode.
interface IRunnerToken {
    function balanceOf(address) external view returns (uint256);
    function totalSupply() external view returns (uint256);
    function setSigner(address) external;
    function startEmission() external;
    function domainSeparator() external view returns (bytes32);
    function CLAIM_TYPEHASH() external view returns (bytes32);
    function claimable(address account, uint256 totalEarned) external view returns (uint256);
    function claim(address account, uint256 totalEarned, uint256 deadline, uint8 v, bytes32 r, bytes32 s, bool instant) external;
}

/// @notice claimable() promises "what claim() would pay right now", but an instant claim pays only 80%
///         (20% is burned). Fails on the current code; passes once claimable() accounts for the instant burn
///         (e.g. takes the `instant` flag, or documents/returns the gross and net separately).
contract ClaimableInstantTest is Test {
    IRunnerToken token;
    uint256 signerKey = 0xA11CE;
    address owner = makeAddr("owner");
    address runner = makeAddr("runner");

    function setUp() public {
        vm.warp(20_500 days + 3600);
        token = IRunnerToken(deployCode(
            "RunnerToken.sol:RunnerToken",
            abi.encode(owner, makeAddr("hook"), makeAddr("team"), makeAddr("imd"), makeAddr("poolManager"))
        ));
        vm.startPrank(owner);
        token.setSigner(vm.addr(signerKey));
        token.startEmission();
        vm.stopPrank();
    }

    function test_claimable_matchesInstantClaimPayout() public {
        uint256 totalEarned = 1_000e18;
        uint256 deadline = block.timestamp + 3600;
        bytes32 digest = keccak256(abi.encodePacked(
            "\x19\x01", token.domainSeparator(),
            keccak256(abi.encode(token.CLAIM_TYPEHASH(), runner, totalEarned, deadline, true))
        ));
        (uint8 v, bytes32 r, bytes32 s) = vm.sign(signerKey, digest);

        uint256 promised = token.claimable(runner, totalEarned);
        assertEq(promised, totalEarned, "view reports the full difference");

        uint256 before = token.balanceOf(runner);
        vm.prank(runner);
        token.claim(runner, totalEarned, deadline, v, r, s, true);
        uint256 paid = token.balanceOf(runner) - before;

        // 800 RUNNER arrive, 200 are burned: the view over-promised by 25%.
        assertEq(paid, promised, "claimable() must equal what the instant claim pays");
    }
}
```

### 3. Info: Odd-wei fees split protocol 0 / holders 1 instead of 2%/2%: the protocol share floors to zero on dust-sized IMD legs

`contracts/RunnerHook.sol:358`

```
        uint256 protocolFee = (fee * PROTOCOL_FEE_BPS) / FEE_BPS;
```

_feeOf rounds the 4% fee up, so every swap with an IMD leg of 2..25 wei pays a fee of exactly 1 wei. _chargeFee then splits it as protocolFee = fee * 200 / 400, which floors 1/2 to 0, and credits fee - protocolFee = 1 wei to holders. For every odd fee the extra wei goes to holders; for fee == 1 the protocol receives nothing, so the documented 2% protocol / 2% holder split is 0% / 4% for that trade. The total fee is conserved (pendingProtocolFees + pendingHolderFees == minted claims), the deviation is bounded by 1 wei per swap, and a 1-wei exact-in buy cannot execute (fee == input, the pool swaps 0, afterSwap reverts EmptySwap). Economic impact is nil: spamming 25-wei swaps through a third-party router only burns gas to move 1 wei per swap from the protocol to holders. Reported as a concrete mismatch between the stated split and the arithmetic. Fix if exact parity matters: round the protocol half up on alternate swaps, or document that holders receive the rounding wei.

**Reproduction**

Setup as in contracts/test/RunnerHook.t.sol (hook at startTick 142,600, pool opened, local v4 PoolManager). Through PoolSwapTest, perform an exact-in buy with amountSpecified = -24 (24 wei IMD) and zeroForOne = launches(runner).quoteIsCurrency0. Expected per the NatSpec: fee = 1 wei split 2%/2% between protocol and holders (or a documented rounding direction). Actual: hook.pendingProtocolFees(IMD) increases by 0 and hook.pendingHolderFees(RUNNER) increases by 1. Observed in test/scratch/Repro.t.sol::test_oddWeiFee_splitGoesEntirelyToHolders: amount 24 -> protocol 0 / holders 1; 25 -> 0 / 1; 26 -> 1 / 1; 51 -> 1 / 2. amountSpecified = -1 reverts (test_oneWeiBuy_revertsEmptySwap). The afterSwap path (exact-in sell / exact-out buy) calls the same _chargeFee.

### 4. Info: buyWithEth refunds the router's whole ETH balance, not only the caller's unspent msg.value

`contracts/RunnerEthRouter.sol:83`

```
        if (address(this).balance > 0) address(0).transferOut(msg.sender, address(this).balance);
```

The refund after the unlock sends address(this).balance to msg.sender instead of msg.value - ethIn. The router has no receive() function, so in normal operation the two are equal and nothing is lost; but any ETH that reaches the router by other means (SELFDESTRUCT beneficiary, coinbase reward, or a future change that lets the router hold ETH) is handed to whichever buyer calls next. Not exploitable for profit beyond that windfall and no loss to protocol users; hygiene note. Fix: return ethIn from the callback alongside tokensOut (or snapshot address(this).balance - msg.value before the unlock) and refund only msg.value - ethIn.

**Reproduction**

State: 1 wei credited to the RunnerEthRouter outside buyWithEth (vm.deal(address(ethRouter), 1 wei) in the test; on chain, a contract self-destructing with the router as beneficiary). Input: alice calls buyWithEth{value: 1 ether}(RUNNER, 0, deadline) against an IMD/ETH pool deep enough to fill the full 1 ether. Expected: alice's refund is 0 (msg.value - ethIn) and her ETH balance drops by exactly 1 ether. Actual: the `if (address(this).balance > 0)` branch sends her the stray wei, so her balance drops by 1 ether - 1 wei and the router ends at 0. Verified in test/scratch/Repro.t.sol::test_buyWithEth_refundsStrayBalanceToCaller.

---

Judge's submission `63c0dd433e27aca96a32bcc5bbf4f540f77c7a0f9bc299ce2346e70116758d2c`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
