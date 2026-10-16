# Audit report

> Focus on the standalone v4 hook and CREATE2 factory: exact callback permission bits, mined versus deployed address, salt/front-running risks, constructor and PoolManager/chain binding, bytecode verification, swap-limit bypasses, denial-of-service, and behavior across two new pools. Reproduce material findings with Foundry tests. Distinguish local evidence from untested public-chain deployment.

| | |
|---|---|
| Repository | https://github.com/identity-md-launches/launch-1811-build-technical-foundation-hooks.git |
| Commit | `42119ec0a1425064b6cb7bd5a5015fd4f665d736` |
| Job | `0baee611-180e-4e5d-9c3a-a23ba1245fbb` |
| Judged | 2026-10-16 00:03 UTC |
| Findings | 4 low · 3 info |

Four agents audited the code as it is at `42119ec`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Low: Hook constructor does not enforce DeploymentPolicy: a standalone CREATE2 deployment of the official template succeeds on Ethereum mainnet (chain 1)

`src/BoundedSwapHook.sol:41`

```
        HookSpecLib.validateChain(spec);
```

README.md line 48 says 'Ethereum, Base and Robinhood mainnets are explicitly rejected', and docs/DEPLOYMENT.md says 'Mainnet deployment is disabled in the release'. Only HooksStoreFactory (constructor and deploy), HookDeployment.checkFactory, the scripts and the SDK call DeploymentPolicy.requireTestChain(). The BoundedSwapHook constructor checks only spec validity, spec.chainId == block.chainid and the callback bits. Anyone can therefore deploy the template through any CREATE2 deployer on chain 1, 8453 or 4663 and get a working hook with the official templateId, specHash and identical runtime bytecode, bound to a mainnet PoolManager. Only factory.deployedSpecHash (which cannot exist on those chains) tells it apart from a Store deployment. THREAT_MODEL.md line 30 scopes the control to the factory, integration and adapter, so this is a gap between the headline claim and the code, not a bypass of a factory invariant. Fix: call DeploymentPolicy.requireTestChain() in the hook constructor (no change on allowed chains), or correct the README and DEPLOYMENT.md claim. Local evidence only: vm.chainId(1) on a fresh vendored PoolManager, not a public chain.

**Reproduction**

vm.chainId(1); deploy PoolManager M; spec = HookSpec(1, TEMPLATE_ID, 1, M, M.codehash, 0x10c0, 1_000_000); a helper contract D first runs `new HooksStoreFactory()` (reverts UnsupportedDeploymentChain(1), as documented), then runs `new BoundedSwapHook{salt: s}(spec)` with s from HookMiner.mine(D, initHash, PERMISSIONS, 0, 131072). Expected per README: revert UnsupportedDeploymentChain(1). Actual: the hook deploys. Ran `forge test --match-path test/scratch/Proof_edf77f1d61ad.t.sol`: FAIL 'next call did not revert as expected'.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {PoolManager} from "v4-core/src/PoolManager.sol";
import {HookSpec, HookSpecLib} from "src/HookSpec.sol";
import {HooksStoreFactory} from "src/HooksStoreFactory.sol";
import {BoundedSwapHook} from "src/BoundedSwapHook.sol";
import {HookMiner} from "src/deployment/HookMiner.sol";
import {DeploymentPolicy} from "src/deployment/DeploymentPolicy.sol";

/// @dev Separate deployer so `new` runs inside a real external call frame (Foundry rewrites `new`
///      inside test contracts into a cheatcode, which aborts the test under expectRevert).
contract Deployer {
    function factory() external returns (HooksStoreFactory) {
        return new HooksStoreFactory();
    }

    function hook(bytes32 salt, HookSpec memory spec) external returns (BoundedSwapHook) {
        return new BoundedSwapHook{salt: salt}(spec);
    }
}

/// @notice The release says mainnets are rejected, but only the factory enforces DeploymentPolicy.
///         A direct `new BoundedSwapHook{salt: s}(spec)` with spec.chainId == 1 on chain 1 succeeds.
///         Fails on the current code; passes once the hook constructor enforces the same allowlist.
contract HookChainPolicyTest is Test {
    function testHookConstructorRejectsMainnetLikeFactory() public {
        vm.chainId(1);
        Deployer d = new Deployer();
        PoolManager manager = new PoolManager(address(this));
        HookSpec memory spec = HookSpec({
            schemaVersion: 1,
            templateId: HookSpecLib.TEMPLATE_ID,
            chainId: 1,
            poolManager: address(manager),
            poolManagerCodeHash: address(manager).codehash,
            permissions: HookSpecLib.PERMISSIONS,
            maxSpecifiedAmount: 1_000_000
        });

        // The factory path is closed on chain 1, as documented.
        vm.expectRevert(abi.encodeWithSelector(DeploymentPolicy.UnsupportedDeploymentChain.selector, uint256(1)));
        d.factory();

        // The standalone constructor path: mine a valid salt for the deployer and deploy directly.
        bytes32 initHash = keccak256(bytes.concat(type(BoundedSwapHook).creationCode, abi.encode(spec)));
        HookMiner.Result memory r = HookMiner.mine(address(d), initHash, HookSpecLib.PERMISSIONS, 0, 131072);
        assertTrue(r.found, "no salt found");

        vm.expectRevert(abi.encodeWithSelector(DeploymentPolicy.UnsupportedDeploymentChain.selector, uint256(1)));
        d.hook(r.salt, spec);
    }
}
```

### 2. Low: Mainnet-rejection test stops after its first expected revert; chains 8453/4663/42 and the deploy() rejection are never exercised

`test/Deployment.t.sol:248`

```
            new HooksStoreFactory();
```

Under forge 1.8.3, `new HooksStoreFactory()` inside the test contract is executed as the vm.deployCode cheatcode. With expectRevert armed, its revert propagates out of the test function itself. Foundry matches that revert against the expectation and reports PASS, but nothing after line 248 runs. testAllNamedMainnetsAndUnknownChainsRejected therefore checks only the constructor on chain 1. The factory.deploy rejection (line 250) and the iterations for 8453, 4663 and 42 never execute, yet VERIFICATION.md and THREAT_MODEL.md cite this test as evidence for them. The production code does reject them (the policy is a plain chain-id comparison and is called first in deploy). This is a test-evidence defect. Fix: create the factory through an external helper contract (or this.call) so expectRevert consumes the inner revert, or split the test into one chain per test with deploy checked first.

**Reproduction**

`forge test --match-test testAllNamedMainnetsAndUnknownChainsRejected -vvvv`. Expected: 8 UnsupportedDeploymentChain reverts across ids 1, 8453, 4663, 42. Actual (observed): PASS with gas 4440. The trace shows only VM::chainId(1), expectRevert, deployCode reverting, then the test function itself returning [Revert] UnsupportedDeploymentChain(1). No HooksStoreFactory::deploy call and no chainId(8453/4663/42) appear.

### 3. Low: lib/SHA256SUMS fails for 18 vendored files, including PoolManager.sol and Hooks.sol, contradicting 'copied unchanged'

`docs/DEPENDENCIES.md:11`

```
Source files are copied unchanged from the named upstream commits. Our test router is project-authored; no Uniswap periphery or external BaseHook dependency is needed. The hook implements the pinned `IHooks` interface directly, with the unused callback rejection separated into `DisabledCallbacks`.
```

VERIFICATION.md presents lib/SHA256SUMS as file-level integrity evidence. `sha256sum -c lib/SHA256SUMS` reports 18 FAILED entries: 7 forge-std files, solmate ERC20.sol, and 10 v4-core files (PoolManager, Hooks, Pool, SqrtPriceMath, StateLibrary, SwapMath, TickBitmap, TransientStateLibrary, Currency, Slot0). One specialist counted 10; this tree has 18. I fetched six of the v4-core files from upstream commit e50237c4. They hash exactly to the manifest values, and after removing whitespace and braces they are identical to the committed copies. diff -w of Hooks.sol shows only line re-wrapping and braces added around a one-line `if` return. So the vendored code is reformatted (forge fmt style), not semantically changed, as far as checked. But the repository's own integrity check fails, and a reviewer cannot tell this apart from a hostile edit without fetching upstream. Fix: restore the byte-exact upstream files, or regenerate SHA256SUMS and document the reformatting.

**Reproduction**

From the repository root: `sha256sum -c lib/SHA256SUMS | grep -v ': OK$'`. Expected: no output. Actual: 18 lines ending in FAILED, including lib/v4-core/src/PoolManager.sol and lib/v4-core/src/libraries/Hooks.sol. Cross-check: upstream raw.githubusercontent.com/Uniswap/v4-core/e50237c4.../src/libraries/Hooks.sol hashes to f6012d7f627259f8..., which equals the manifest entry, while the committed file does not.

### 4. Low: A maximum mining page (MAX_ATTEMPTS = 131072) can need ~37-42M gas, above a 30M default eth_call allowance; the SDK reports only 'eth_call failed'

`src/deployment/HookMiner.sol:7`

```
    uint256 internal constant MAX_ATTEMPTS = 131072;
```

Merged from three specialists. Each non-matching candidate costs about 320 gas (keccak of 85 bytes plus loop overhead). A full 131072-attempt page with a late match or no match therefore costs about 37-42M gas. mine is meant to run via eth_call (docs/STORE_API.md allows attempts up to 131072, and sdk/hooks_store.py accepts --page-size up to 131072). Nodes that cap eth_call gas at the block gas limit (30M, the Anvil/Hardhat default when no gas field is sent, and the SDK sends none) reject such a page. Rpc.request turns this into the generic 'eth_call failed', so the operator cannot tell it from a revert. geth's default 50M rpc.gascap admits it. Forge scripts (the DEPLOYMENT.md example) run locally and are unaffected. Availability only, no funds at risk; the SDK default page of 4096 (~1.3M gas) is fine. Fix: lower MAX_ATTEMPTS (65536 ≈ 21M gas) and the SDK page_size bound to match, or document per-attempt gas and send an explicit gas field. Local evidence: Foundry measurement only. No public RPC provider was exercised.

**Reproduction**

Ran `forge test --match-path test/scratch/Proof_9a464c293127.t.sol`: a fresh manager and factory at test-contract nonces, spec(limit 1_000_000), factory.mine(spec, 3441596, MAX_ATTEMPTS) over a 115,085-salt miss run. Expected: at most 30,000,000 gas. Actual: FAIL '36840380 > 30000000'. A page with no match extrapolates to ~42M gas.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {PoolManager} from "v4-core/src/PoolManager.sol";
import {HookSpec, HookSpecLib} from "src/HookSpec.sol";
import {HooksStoreFactory} from "src/HooksStoreFactory.sol";
import {HookMiner} from "src/deployment/HookMiner.sol";

/// @notice Fails on the current miner: a maximum-size page (MAX_ATTEMPTS = 131072) that has no match for
/// 115,085 consecutive salts costs about 37M gas, above the 30M gas that Anvil (and Hardhat) grant an
/// eth_call by default. Passes once MAX_ATTEMPTS is reduced so that a full page fits (65,536 ≈ 21M gas).
contract MinerPageGasTest is Test {
    // With this deployment order the manager is at 0x5615dEB798BB3E4dFa0139dFa1b3D433Cc23b72f and the
    // factory at 0x2e234DAe75C793f67A35089C9d99245E1C58470b; nonces 3441596..3556680 produce no match.
    uint256 constant NO_MATCH_START = 3441596;

    function testMaxPageFitsDefaultEthCallGas() public {
        vm.chainId(31337);
        PoolManager manager = new PoolManager(address(this));
        HooksStoreFactory factory = new HooksStoreFactory();
        HookSpec memory spec = HookSpec(
            1, HookSpecLib.TEMPLATE_ID, 31337, address(manager), address(manager).codehash, HookSpecLib.PERMISSIONS, 1_000_000
        );
        uint256 before = gasleft();
        HookMiner.Result memory r = factory.mine(spec, NO_MATCH_START, HookMiner.MAX_ATTEMPTS);
        uint256 used = before - gasleft();
        // Sanity: the page really is a long miss run (a match, if any, comes after 110k+ attempts).
        assertTrue(!r.found || r.nextNonce - NO_MATCH_START > 110_000, "page unexpectedly matched early");
        assertLe(used, 30_000_000, "a maximum miner page exceeds the default eth_call gas allowance");
    }
}
```

### 5. Info: Swap limit bounds only the per-call specified amount: exact-output input is uncapped and limit-sized swaps can repeat within one unlock (documented design; untested)

`src/BoundedSwapHook.sol:78`

```
        if (params.amountSpecified == 0 || params.amountSpecified < -limit || params.amountSpecified > limit) {
```

Merged from six specialist findings (audit_math, audit_economics x2, audit_flow, audit_permissions). beforeSwap compares only params.amountSpecified, and keeps no cumulative per-transaction or per-block state; afterSwap ignores the BalanceDelta. (1) An exact-output swap at the limit settles input bounded only by pool liquidity. (2) Any number of limit-sized swaps can run inside one unlock. README line 7 and THREAT_MODEL line 20 state both properties, so this is not a code defect. It is recorded because the review scope asks about limit bypasses. The test suite pins neither property: every test does one swap per unlock and asserts only the specified side. If the product wants a two-sided cap, afterSwap could revert when |delta.amount0()| or |delta.amount1()| exceeds the limit; that is a design decision. Local evidence only.

**Reproduction**

Ran `forge test --match-path test/scratch/Proof_f29ad4ab994a.t.sol`: hook limit 1_000_000; pool fee 3000, tickSpacing 60, sqrtPrice 2^96, full-range liquidity 1_100_000; swap zeroForOne, amountSpecified=+1_000_000. Actual delta.amount0 = -11_033_210 (input 11x the limit); the test fails with '11033210 > 1000000'. An exact-input swap of -1_000_001 reverts AmountOutsideLimit. Splitting follows directly from the code: beforeSwap is `view` and reads no per-call state, so N swaps of -1_000_000 in one unlock each pass.

### 6. Info: Duplicate deploy of an identical public plan reverts AddressOccupied; DeployHook.run has no verify-and-adopt path

`src/HooksStoreFactory.sol:71`

```
        if (plan.hook.code.length != 0) revert AddressOccupied(plan.hook);
```

Merged from audit_math and audit_economics. Salts are sender-independent counters, and the only creator choice in a spec is the limit. Two creators with the same spec get the same plan, and anyone who copies calldata from the mempool can land first. The second transaction reverts and pays gas, though the identical hook exists and gives no one ownership. STORE_API.md line 27 and THREAT_MODEL line 26 document this ('call verify'), but script/DeployHook.s.sol execute() always calls deploy and reverts. This is griefing or an operational sharp edge, with no loss of funds. Optional fix: in deploy (or the script), if the address has code and deployedSpecHash[plan.hook] == plan.specHash, run _verify and return the plan instead of reverting.

**Reproduction**

The existing testDuplicateDeploymentRejectedAndMinerSkipsOccupiedAddress (passes) shows it: factory.deploy(spec, plan.salt, plan.hook, plan.initCodeHash) succeeds, then the identical call from any address reverts AddressOccupied(plan.hook), while factory.verify(spec, plan.salt, plan.hook) succeeds.

### 7. Info: README claims the hook rejects zero amountSpecified, but PoolManager rejects zero first; the hook branch is unreachable via the manager

`README.md:5`

```
`BoundedSwapHook` serves any number of **new static-fee pools on one PoolManager**. It rejects swaps whose requested `amountSpecified` is zero or outside an immutable raw-unit limit, then counts successful swap callbacks separately by PoolId. It neither holds swap funds nor changes fees or accounting deltas. Anyone may use it when initializing a new pool. A pool's hook is part of its PoolKey; this does not retrofit hooks onto existing pools.
```

lib/v4-core/src/PoolManager.sol line 190 reverts SwapAmountCannotBeZero before Hooks.beforeSwap is called, so integrators never see AmountOutsideLimit(0, limit) from a real swap. The hook check is harmless defence in depth and is reached only by the tests' direct vm.prank(manager) calls. Fix: attribute zero-amount rejection to the PoolManager in the README.

**Reproduction**

manager.swap(key, SwapParams(true, 0, MIN_SQRT_PRICE+1), '') inside unlock reverts SwapAmountCannotBeZero() at PoolManager.sol:190 (`if (params.amountSpecified == 0) SwapAmountCannotBeZero.selector.revertWith();`), which comes before key.hooks.beforeSwap on line 199.

---

Judge's submission `ce6aea8a15cccdca64ce4f46980d69decd9f52ed622f67d8e51b5021f2ec3b76`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
