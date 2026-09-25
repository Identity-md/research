# Report: Uniswap v4 hook permissions for IMD factory launches (Sepolia)

Date: 2026-09-25. Full details are in `HOOK_PERMISSIONS.md` and `HOOK_PERMISSIONS.json` at the repo root.

## Answer

| Set | Permissions | Address flag bits |
|---|---|---|
| A: no-op smoke | `afterSwap` | `0x0040` |
| B: fixed fee skim | `afterSwap`, `afterSwapReturnDelta` | `0x0044` |
| C: burn-share | `afterSwap`, `afterSwapReturnDelta` | `0x0044` |

- Do not use `beforeInitialize` or `afterInitialize` for IMD factory launches.
- Constructor args must contain only PoolManager literals. On chainId 11155111 that is `0xE03A1074c86CFeDd5C142C4F04F1a1536e203543`.

## Evidence (facts)

- **Permission layout.** `Hooks.Permissions` has 14 bools. Their flags are bits 13..0 of the hook address, from `BEFORE_INITIALIZE_FLAG = 1<<13` down to `AFTER_REMOVE_LIQUIDITY_RETURNS_DELTA_FLAG = 1<<0`. Source: [v4-core Hooks.sol @46c6834](https://github.com/Uniswap/v4-core/blob/46c6834698c48bc4a463a86d8420f4eb1d7f3b75/src/libraries/Hooks.sol).
- **Who `sender` is.** `PoolManager.initialize` calls `key.hooks.beforeInitialize(...)`, which passes `msg.sender`, the caller of `initialize`, as `sender`. Source: [PoolManager.sol L117-142 @46c6834](https://github.com/Uniswap/v4-core/blob/46c6834698c48bc4a463a86d8420f4eb1d7f3b75/src/PoolManager.sol#L117-L142).
- **How hook failures surface.** A hook that fails is re-thrown by `CustomRevert.bubbleUpAndRevertWith` as `WrappedError(target, selector, reason, details)`, with `details = HookCallFailed`. Source: [CustomRevert.sol](https://github.com/Uniswap/v4-core/blob/46c6834698c48bc4a463a86d8420f4eb1d7f3b75/src/libraries/CustomRevert.sol).
  - The selectors, computed with `cast sig`, are: WrappedError `0x90bfb865`, beforeInitialize `0xdc98354e`, HookCallFailed `0xa9e35b2f`.
- **Flag validity rules.**
  - `isValidHookAddress` requires each `*ReturnDelta` flag to have its base flag.
  - A hook with no flags is valid only for dynamic-fee pools.
  - `validateHookPermissions` requires an exact match on all 14 bits.
- **OZ fee hook permissions.** OZ `BaseHookFee` uses exactly `afterSwap` + `afterSwapReturnDelta`. Source: [BaseHookFee.sol @80bd724](https://github.com/OpenZeppelin/uniswap-hooks/blob/80bd72492bb373c67d1e37d179f42a19b89e2440/src/fee/BaseHookFee.sol).
- **Constructor and caller checks.** OZ `BaseHook`'s constructor takes only `IPoolManager` and validates the hook address. Its callbacks are `onlyPoolManager`.
- **Sepolia PoolManager.** The PoolManager for Sepolia (11155111) is `0xE03A1074c86CFeDd5C142C4F04F1a1536e203543`, per [docs.uniswap.org/contracts/v4/deployments](https://docs.uniswap.org/contracts/v4/deployments). `eth_getCode` via a public Sepolia RPC returned non-empty code.

## Inferences

- A `beforeInitialize` that gates on the pad, or on a stored launcher, sees `sender = factory` and reverts. The whole factory launch then fails with `WrappedError`, and the real reason is nested inside `reason`.
- Hooks whose logic is only on the swap path ("BurnShareHook-style") are never called during `initialize`, so they cannot block pool creation.
- Constructor placeholders (`$pad`, `$token`) change the CREATE2 init code. That changes the hook address and its flag bits, which breaks the mined salt and the attestation.

## Uncertainty / unanswered

- I did not locate a public BurnShareHook deployment, so no hook address is cited.
- The factory's liquidity-seeding path is unknown. It affects whether liquidity flags could ever be safe.
- Whether burn-share should be one-sided or two-sided, and what the burn target should be, is an open design choice.
- The failure mode was derived from source code. It was not reproduced on-chain, and nothing was deployed.
- The consistency checks (JSON parses, all names are real `Hooks.Permissions` fields, bitmasks correct, MD matches JSON) passed locally. No independent review has been done.
