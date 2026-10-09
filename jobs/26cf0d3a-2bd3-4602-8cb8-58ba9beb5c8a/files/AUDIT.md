# Audit report

> Audit the SOVRN.ONE / SVO launch contracts in this repository (Solidity 0.8.26, Foundry, Uniswap v4 vendored in lib/). Scope: src/SovrnHook.sol, src/LifeForceVault.sol, src/SovrnToken.sol, src/HookFlags.sol, src/Interfaces.sol, script/PrepareLaunch.s.sol, launch.json, README.md. Tests in test/ (167 tests, run in both currency orders, plus test/Fork4663.t.sol which runs against the real chain when FORK_4663_RPC is set) are evidence to check, not the object of the audit. Intended deployment: Robinhood Chain (chain id 4663), a Uniswap v4 pool of {IMD, SVO} where IMD is the ERC-20 at 0x5F7Bb59365ce557C26dbcAa4EE9d39A4b95B7127 and SVO is a plain fixed-supply token; every trading fee is paid in IMD to an immutable LifeForceVault that only accounts for it; a fixed Safe (0xEb57c52272B90F989C41B739e2ccc5f00bF7697C) withdraws by hand. Write nothing to the repository; deliver report.md. Tone: factual and plain; no claims of safety beyond the evidence; do not call the contracts audited or secure; no investment language.
>
> CONTEXT. This code was adapted from an accepted ETH-paired version (the first commits of the branch, where the fee was native ETH): the fee currency became IMD, the hook now handles IMD as either currency0 or currency1 (decided by address order, `imdIsCurrency0`), and the vault now derives its reserves from IMD.balanceOf. Review that diff with particular care: the ETH-to-IMD generalisation is where new defects are most likely.
>
> HARD QUESTIONS (answer each with a verdict and evidence, and a reproducible Foundry test where possible):
> 1. Currency order. For both orders and for all four exact-input/exact-output modes, is `buy = (zeroForOne == imdIsCurrency0)` and `specifiedIMD = (buy == (amountSpecified < 0))` correct, are the IMD leg (amount0 vs amount1) and every sign in beforeSwap/afterSwap and their return deltas right, and does the fee always equal the stated percentage of the actual IMD leg? Can any price limit, tiny amount or rounding produce a fee that differs from the spec, a revert on a valid swap, or a fee larger than the amount?
> 2. Quote mechanism. The hook measures the real IMD delta with a self-call that always reverts, then requires the real swap to match (QuoteMismatch). Can that be broken or griefed (reentrancy, the busy flag, transient state, protocol fees, an LP-fee override, a hook-less path, concurrent unlocks)? Can the quote leave state behind?
> 3. ERC-20 fee path. Fees are taken with PoolManager.take(IMD, vault, fee), or minted as ERC-6909 claims (id uint160(IMD)) when the manager holds less IMD than the fee, then redeemed by the permissionless redeemFees(). Is the manager-balance check right, can claims be stranded or double-spent, can redeemFees be reentered, and what exactly happens if IMD reverts, returns false, takes a transfer fee, or calls back (ERC-777 style) during take or transfer?
> 4. Vault accounting. The vault has no receive hook for an ERC-20, so _reserves() derives reserves from IMD.balanceOf with a checkpoint model, floor(x*3000/10000) to buyback, a clamp so reserves never exceed the real balance (shortfall reduces buyback first), sync(), and Safe-only withdrawals paid with a low-level call. Can the Safe withdraw more than it should, can anyone grief or steal, can reserves ever exceed the balance or underflow, are rounding and dust handled, is nonReentrant correct, and is the low-level transfer return handling safe for non-standard ERC-20s? What does a malicious or upgraded IMD change?
> 5. Initialisation and addresses. beforeInitialize binds one pool: factory-only, exact currencies in address order, fee 12500, hooks == this, tickSpacing > 0. Is that complete? Hook flags 8396: does PrepareLaunch mine a valid address, can a hook with the wrong flags or a pre-initialised address slip through, does the constructor guard (block.chainid == 4663, IMD has code, token != IMD) hold, and is anything wrong with deploying the vault inside the hook constructor?
> 6. Opening-price and launch risks. What can an attacker do between pool initialisation and liquidity seeding (empty pool zero-delta swap, price manipulation, sandwiching the first-hour decaying buy fee, block.timestamp use)? Is anything in the README wrong or missing about this?
> 7. Trust and operational assumptions. IMD has an owner and unknown transfer rules; the pool manager has a protocol-fee controller; one Safe has custody of every withdrawal. State precisely what each can and cannot do to funds and trading, and whether the code or README understate any of it. In particular: what happens to trading if IMD blocks transfers to the vault?
> 8. Token. Confirm SovrnToken is plain (no owner, mint, tax, pause, blacklist), name() is exactly "SOVRN.ONE" and symbol() exactly "SVO", supply 10^27, and burn() on the vault sends only to DEAD and only SVO.
> 9. Tests and docs. Does the test suite genuinely cover the risks above in both orders (incl. mocks that misbehave), what is missing, and does every claim in README.md and launch.json match the code exactly (numbers, addresses, privileges, wording rules)?
>
> METHOD: use the Pashov methodology and specialties. Reproduce every finding against the code; discard unreproducible claims. Rate each finding by severity and likelihood, give a concrete fix, and separate real defects from documented design trade-offs. Do not claim this review substitutes for an independent human audit.

| | |
|---|---|
| Repository | https://github.com/SovrnOne/sovrn-contracts.git |
| Commit | `a939314fbfb34c9a6fc91c037145158e7bbc08b5` |
| Job | `26cf0d3a-2bd3-4602-8cb8-58ba9beb5c8a` |
| Judged | 2026-10-09 03:29 UTC |
| Findings | 6 low · 3 info |

Four agents audited the code as it is at `a939314`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Low: Vault persists a shortfall write-down on sync()/withdraw, so the 70/30 split of IMD that later returns is path dependent and permissionless sync() can move buyback into inference

`src/LifeForceVault.sol:67`

```
        inference = newInference;
        buyback = newBuyback;
```

_reserves() clamps the views to the real IMD balance without touching storage, so a transient shortfall (IMD leaving the vault by a route the vault does not control: a seizure, a negative rebase, a transfer fee on an inbound transfer that is later compensated) is reversible as long as nothing is checkpointed. But sync() (permissionless) and both withdraw functions (LifeForceVault.sol:77 and :85) write the clamped values back into storage. Once that happens the buyback checkpoint that was only temporarily unbacked is deleted; any IMD that then returns is treated as new income and split 70/30 on top of the already-full inference checkpoint. The final inference/buyback allocation of identical cash flows therefore depends on whether a third party called sync() while the balance was short, and the drift is one way (buyback never recovers its share). README line 65 documents that a shortfall reduces buyback first but not that the reduction becomes permanent on the next checkpoint, nor that the outcome depends on who calls sync() when. Preconditions are IMD level (the deployed IMD shows no fee or seizure function today, but it has an owner and a blocklist), both reserves pay the same Safe and the README calls the split accounting only, so no value leaves the system: this is a design seam, not a theft path. Merged from four specialist reports (permissions, math, economics, flow). Fix (preserves the design): in sync() and the withdraw functions only raise the checkpoints when balance >= inference + buyback; when the balance is short leave the stored checkpoints as they are and bound the withdrawal by the clamped view (withdrawals still debit the stored reserve and can never exceed the live balance). Alternatively track the shortfall as an explicit deficit that returning IMD repays before any new split. Then state the chosen rule in README 'Vault accounting and callers'.

**Reproduction**

Plain ERC-20 at 0x5F7Bb59365ce557C26dbcAa4EE9d39A4b95B7127, chain id 4663, LifeForceVault deployed directly. (1) transfer 100e18 IMD to the vault, call sync(): inferenceReserve() 70e18, buybackReserve() 30e18. (2) move 30e18 out of the vault by a route the vault does not control (vm.prank(vault); imd.transfer(BOB, 30e18)): views 70e18 / 0. (3) BOB calls vault.sync(). (4) BOB transfers the same 30e18 back. Expected: balance equals the original checkpoint again, views 70e18 / 30e18 (which is what the views return if step 3 is skipped). Actual: inferenceReserve() 91e18, buybackReserve() 9e18. Reproduced: forge test --match-path test/scratch/VaultSyncShortfall.t.sol fails with '9000000000000000000 != 30000000000000000000'. The two withdraw functions write the same clamped values (line 77 and 85), so a Safe withdrawal during the shortfall has the same one-way effect.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;
import {Test} from "forge-std/Test.sol";
import {PoolManager} from "v4-core/src/PoolManager.sol";
import {IPoolManager} from "v4-core/src/interfaces/IPoolManager.sol";
import {SovrnToken} from "src/SovrnToken.sol";
import {LifeForceVault} from "src/LifeForceVault.sol";
import {ERC20} from "solmate/src/tokens/ERC20.sol";

/// @dev Plain ERC-20 whose runtime code is placed at IMD's real address (no artifact lookup by file name).
contract PlainIMD is ERC20 {
    constructor() ERC20("Identity.md", "IMD", 18) {}

    function mint(address to, uint256 amount) external {
        _mint(to, amount);
    }
}

/// @dev A temporary shortfall (IMD leaves the vault by a route the vault does not control, then the same
///      amount comes back) must not change the 70/30 split. Today anyone can call sync() during the
///      shortfall and permanently move the buyback reserve into inference.
contract VaultSyncShortfallTest is Test {
    address constant IMD_ADDR = 0x5F7Bb59365ce557C26dbcAa4EE9d39A4b95B7127;
    address constant BOB = address(0xB0B);
    PlainIMD imd;
    LifeForceVault vault;

    function setUp() public {
        vm.chainId(4663);
        PoolManager manager = new PoolManager(address(this));
        vm.etch(IMD_ADDR, address(new PlainIMD()).code);
        imd = PlainIMD(IMD_ADDR);
        imd.mint(address(this), 1e30);
        SovrnToken token = new SovrnToken();
        vault = new LifeForceVault(IPoolManager(address(manager)), token, address(0xBEEF));
    }

    function test_permissionlessSyncDuringShortfallRewritesSplit() public {
        imd.transfer(address(vault), 100 ether);
        vault.sync();
        assertEq(vault.inferenceReserve(), 70 ether);
        assertEq(vault.buybackReserve(), 30 ether);

        // 30 IMD leave the vault by a route the vault does not control (modelled with a prank).
        vm.prank(address(vault));
        imd.transfer(BOB, 30 ether);
        assertEq(vault.inferenceReserve(), 70 ether);
        assertEq(vault.buybackReserve(), 0);

        // Anyone checkpoints while the balance is short.
        vm.prank(BOB);
        vault.sync();

        // The same 30 IMD come back.
        vm.prank(BOB);
        imd.transfer(address(vault), 30 ether);

        // Expected: the original 70 / 30 is restored (the balance equals the original checkpoint again).
        // Actual: 91 / 9, because the sync() during the shortfall deleted the buyback checkpoint and
        // the returned 30 IMD is re-split 70/30 on top of inference.
        assertEq(vault.buybackReserve(), 30 ether, "buyback reserve permanently reduced by a permissionless sync");
        assertEq(vault.inferenceReserve(), 70 ether);
    }
}
```

### 2. Low: IMD owner powers understated: the deployed IMD has an owner-only v4 transfer gate (plus blocklist and OFT bridge) controlled by one EOA; switching the gate on halts both swaps and LP IMD withdrawals o

`README.md:34`

```
- If IMD refuses a transfer to the vault (a blacklist, a pause, a transfer hook), a swap whose fee is taken directly reverts. The claims fallback only runs when the manager holds less IMD than the fee, and its redemption would revert for the same reason until the vault can receive IMD. Trading on the hooked pool stops while that lasts.
```

README lines 30-36 and the launch.json notes describe IMD's rules hypothetically. The IMD contract at 0x5F7Bb59365ce557C26dbcAa4EE9d39A4b95B7127 on chain 4663 is a non-proxy (EIP-1967 implementation slot empty) with verifiable owner powers: owner() = 0x047F606fD5b2BaA5f5C6c4aB8958E45CB6B054B7, an address with no code (a single externally owned key); an owner-only setV4Config(address poolManager, address gate, bool) that today is unset (poolManager() = 0x0) and, when set, makes every IMD transfer out of the configured PoolManager revert ('BridgedFP: v4 transfer not approved') unless the gate contract approves it; a blocklist view blocked(address) (false for the PoolManager and the Safe today); a one-way transfersEnabled switch (already true, enableTransfers() reverts 'already enabled'); and a LayerZero OFT bridge (peers(30101) is set), so the owner can re-point a peer and credit IMD on this chain through the bridge path. The README only says that a refused transfer to the vault reverts fee-taking swaps and that 'trading stops'. With the gate on and this pool not approved, every IMD transfer out of the manager reverts: buys (the hook's take of the fee to the vault at SovrnHook.sol:224), sells (the trader's IMD output take), LP removals (the LP's IMD take), and redeemFees(). Liquidity providers therefore cannot exit their IMD either, which the README does not state, and the switch is held by one key. The vault's own withdrawals to the Safe are not manager transfers and keep working unless the vault or the Safe is blocklisted. This is a trust assumption of the agreed design (IMD is an external token), not a code defect. Fix (documentation and launch process): name the gate, the blocklist, the bridge and the single-key owner in README 'IMD assumptions and risks' and in launch.json notes; state that the gate also freezes LP exits; before launch confirm with the IMD owner whether the gate will be enabled and, if so, that this pool's manager transfers are approved; record blocked() for the hook, vault and Safe after deployment.

**Reproduction**

Live reads against https://rpc.mainnet.chain.robinhood.com (chain id 4663): cast call IMD 'owner()(address)' -> 0x047F606fD5b2BaA5f5C6c4aB8958E45CB6B054B7; cast code of that address -> 0x; cast call IMD 'poolManager()(address)' -> 0x0; 'transfersEnabled()(bool)' -> true; 'blocked(address)(bool)' for the Safe and the real manager -> false; cast call --from <owner> IMD 'setV4Config(address,address,bool)' 0x8366a39CC670B4001A1121B8F6A443A643e40951 0xdEaD true -> succeeds (eth_call), the same from 0x1111...1111 -> OwnableUnauthorizedAccount. Fork reproduction (test/scratch/ForkGate.t.sol, run with FORK_4663_RPC set, passes): deploy token, hook and vault on a fork with the real manager and real IMD, initialize the pool, seed full-range liquidity 1e22, warp past the decay; a 1e18 IMD buy pays its fee into the vault. Then vm.prank(IMD.owner()); IMD.setV4Config(realManager, 0xdead01, true). Afterwards the same buy reverts, an exact-input sell of 1000e18 SVO reverts, and router.liquidity(key, ModifyLiquidityParams(-887220, 887220, -1e21, 0)) reverts (all three are IMD transfers out of the manager), while vault.withdrawInference(1) from the Safe still succeeds. Expected per README: only 'a swap whose fee is taken directly reverts'. Actual: every IMD-moving operation on the manager halts, switchable by one EOA.

### 3. Low: REFUEL_SAFE on chain 4663 is a 1-of-3 Safe today: any single owner key can withdraw every fee IMD (operational trust assumption the README leaves unverified)

`README.md:97`

```
After launch, no setters or setup transactions exist. The Safe operators monitor both reserves and any claim backing, arrange permissionless redemption when needed, withdraw inference funds in IMD (and sell it for the USD that the voice provider requires), and withdraw buyback funds to acquire SVO by hand with appropriate trade limits. They transfer acquired SVO to the vault and anyone calls `burn()`. The contracts enforce the withdrawal destination and reserve bounds; they cannot enforce what the Safe does with withdrawn IMD or schedule its purchases. Operators must confirm control of the specified Safe on chain 4663, including its signing threshold, before launch. The supplied Safe identity is a requester parameter, not independently verified here.
```

withdrawInference and withdrawBuyback (LifeForceVault.sol:76-90) pay only REFUEL_SAFE, and the two reserves together always equal the vault's whole IMD balance, so the Safe's signing policy is the only control over 100% of collected fees. The README and launch.json say the threshold is unverified. It is verifiable on chain: 0xEb57c52272B90F989C41B739e2ccc5f00bF7697C holds a Safe proxy (VERSION 1.5.0) with three owners, all without code, and getThreshold() = 1. One compromised or rogue key among three is enough to drain the vault to the Safe and onward; the contracts have no delay, rate limit or alternative recipient. The single-recipient design is intended, so this is not a code defect. Fix (operational, before launch): raise the threshold to at least 2-of-3, or state in README 'Preparation and operation' and in launch.json that custody is effectively single-key today.

**Reproduction**

cast call 0xEb57c52272B90F989C41B739e2ccc5f00bF7697C 'getThreshold()(uint256)' --rpc-url https://rpc.mainnet.chain.robinhood.com -> 1; 'getOwners()(address[])' -> [0x217C05f5D1D1E595BBae94534540B803bfC4563B, 0xb1eC9d1C36974d05eb9889eBf8A150b05791E559, 0x7fFA8901be4777D9fD78F9A00D98DFCDBD833671]; 'VERSION()(string)' -> "1.5.0" (read on 2026-10-09). With any one of those keys a Safe execTransaction to vault.withdrawInference(inferenceReserve()) and vault.withdrawBuyback(buybackReserve()) moves the entire vault balance to the Safe; the vault checks only msg.sender == REFUEL_SAFE (LifeForceVault.sol:41-44). Expected per README: a threshold confirmed before launch; actual on-chain state: threshold 1.

### 4. Low: ETH-to-IMD change: taking the fee as IMD inside afterSwap breaks any v4 router that pays the input before swapping (sync -> transfer -> swap -> settle); undocumented integration constraint new to this

`src/SovrnHook.sol:224`

```
                poolManager.take(Currency.wrap(IMD), address(vault), fee);
```

In the ETH-paired baseline the fee left the manager as native value and native settlement uses msg.value, so a router's settle() never depended on the manager's token balance. With IMD the manager settles ERC-20 input as balanceNow - balanceRecordedBySync. The hook now moves `fee` IMD out of the manager during afterSwap. A router that calls sync(IMD), transfers the input, then swaps and only then settle() (a valid v4 ordering used by pay-first integrations) is credited input - fee by settle() and ends the unlock with an unsettled -fee delta: the swap reverts with CurrencyNotSettled on the hooked pool while the identical call succeeds on a hookless pool. Sells are unaffected (IMD is the output side), and routers that sync immediately before transfer+settle after the swap (Uniswap V4Router, Universal Router) are unaffected. No funds are lost; a class of otherwise valid integrations cannot buy on the hooked pool, and README 'Fees and settlement' does not mention it. Merged from two specialist reports (permissions, economics). Fix: document in README that the hook takes IMD out of the manager during afterSwap, so integrators must settle IMD input after the swap with sync() immediately before settle(), or overpay by the fee; or, if full compatibility is wanted, always mint the fee as ERC-6909 claims and redeem them permissionlessly (a design change that moves every fee through redeemFees()).

**Reproduction**

test/scratch/Judge.t.sol::test_payFirstRouter_hookedVsHookless (passes in both currency orders). Fixture: SystemBase (mock plain ERC-20 at IMD's address, chain id 4663, real vendored PoolManager), hooked pool and an identical hookless pool each seeded with full-range liquidity 1e22, 1 hour after opening. PayFirstRouter.unlockCallback: sync(IMD); IMD.transferFrom(payer, manager, 1e18); swap(key, SwapParams(buy, -1e18, limit)); settle(); take(SVO). Hookless pool: succeeds. Hooked pool, same call: reverts IPoolManager.CurrencyNotSettled (settle credits 1e18 - 0.035e18 while the trader's delta is -1e18). Hooked pool with 1e18 + 0.035e18 pre-paid: succeeds (the router absorbs the fee). Exact-input sell of 1000e18 SVO with the same pay-first ordering on the hooked pool: succeeds. Expected: a v4-valid pay-first buy settles; actual: reverts only on the hooked pool.

### 5. Low: README states that live forks were not run while the same README reports fork-rehearsal and live-RPC results

`README.md:111`

```
This deliverable includes no deployment transactions. Local tests and source review do not establish live-chain readiness. A separate independent adversarial review and a chain-specific deployment rehearsal remain with the launch process; no external security certification is asserted. Static analyzers, formal verification and live forks were not run. `test/REVIEW.md` and `test/README.md` are historical records of the ETH-paired review.
```

Line 111 says 'live forks were not run'. Line 109 reports a result that only a fork run can produce ('The real manager's protocol-fee controller assigned this pool a protocol fee of 0 at the time of the rehearsal'), line 107 reports eth_estimateGas measurements taken against Robinhood Chain on 2026-10-08, and the HEAD commit is titled 'Fork rehearsal on real Robinhood Chain'. One of the two statements is wrong, and the task's wording rule is that every README claim matches exactly. Offline the fork suite is skipped (165 passed, 2 skipped), so a reader cannot resolve the contradiction from the tree alone. Fix: replace the sentence on line 111 with an exact statement, e.g. 'Static analyzers and formal verification were not run. test/Fork4663.t.sol was run on 2026-10-08 against https://rpc.mainnet.chain.robinhood.com; it is skipped in a default forge test and must be re-run before launch.'

**Reproduction**

Read README.md lines 107, 109 and 111 together. Expected: one consistent statement of what was and was not run against a live fork. Actual: line 111 denies any live fork run; lines 107 and 109 report results obtained from a live RPC and a fork. forge test (no FORK_4663_RPC) prints Fork4663ImdLowTest and Fork4663ImdHighTest as skipped; with FORK_4663_RPC set the fork suites and the scratch fork test in this review do run against the real chain, confirming the line-109 kind of result is obtainable.

### 6. Low: Liquidity operations on the hooked pool pay no hook fee: an IMD-only range order converts IMD to SVO during the 50% launch window without the buy fee (design trade-off, undocumented)

`README.md:40`

```
The hook fee applies only to the single pool identified by `hook.poolKey()`. Anyone can create and fund another SVO/IMD pool without this hook; trades there pay no fee to this vault and do not use the launch buy-fee decay. A **buy** pays IMD in and receives SVO; a **sell** pays SVO in and receives IMD. Every fee is paid in IMD.
```

The hook enables only beforeInitialize, beforeSwap and afterSwap; modifyLiquidity on the hooked pool is unrestricted and carries no hook fee. A participant who wants SVO for IMD can mint an IMD-only position just beyond the current tick and let sellers (who pay 3.5%) push the price through it; burning the position returns SVO acquired with no hook fee while also collecting the 1.25% LP fee. The mirror (SVO-only range on the other side) sells SVO for IMD with no 3.5% fee. This is inherent to a swap-only fee hook and is a design trade-off, not a code error, but it depends on counter-flow and the README's only statement on fee avoidance is about other pools; it says nothing about liquidity on this pool, and the first-hour 50% buy fee is presented as protection of the opening price. Fix: document it in 'Fees and settlement' and in launch.json notes; if the launch policy requires that no path on this pool bypass the buy fee, add beforeAddLiquidity/beforeRemoveLiquidity restrictions (which changes the agreed hook flags and manifest: a scope decision for the requester).

**Reproduction**

test/scratch/Judge.t.sol::test_rangeOrderPaysNoHookFee (passes in both currency orders). Pool seeded with 1e21 full-range liquidity at LAUNCH_PRICE, elapsed 0 so launchFeeNow() == 0.5e18. ALICE mints liquidity 1e20 in the 1200-tick range just beyond the current tick on the IMD side: she pays 581047279124406 wei IMD and zero SVO; the vault's IMD is unchanged. BOB sells 1e24 SVO through the hooked pool (the vault's IMD rises by his 3.5%). ALICE burns her position: she receives 62753906800716440802742 wei SVO, and the vault's IMD is unchanged by her mint or burn. A 50% buy of the same IMD at that moment would have paid 290523639562203 wei to the vault; she paid 0.

### 7. Info: IMD.balanceOf is a hard dependency of every swap, including zero-fee swaps, and of every vault view and withdrawal; not in the README risk list and not covered by a test

`src/SovrnHook.sol:218`

```
        bool asClaim = _imdBalanceOf(address(poolManager)) < fee;
```

afterSwap evaluates _imdBalanceOf(poolManager) unconditionally, before the `if (fee != 0)` branch, so a swap whose IMD leg rounds to a zero fee still reverts (HookCallFailed wrapping InvalidAmount) when IMD's balanceOf reverts or returns fewer than 32 bytes. LifeForceVault._imdBalance() has the same dependency: inferenceReserve(), buybackReserve(), sync(), withdrawInference() and withdrawBuyback() all revert with TransferFailed while balanceOf is unavailable, so the Safe cannot withdraw IMD already held even though the transfer itself might succeed. README 'IMD assumptions and risks' covers a refusing transfer, a false return, a transfer fee and confiscation, but not a reverting or non-standard balanceOf, and MockIMD has no switch for it. A reverting balanceOf would also break the manager's own sync/settle for IMD, so this is a robustness note, not an exploit. Suggested fix: compute asClaim inside `if (fee != 0)` (a zero-fee swap then needs no balance read), add a MockIMD mode whose balanceOf reverts with a test documenting the vault's behaviour, and add the dependency to the README risk list.

**Reproduction**

test/scratch/Judge.t.sol::test_zeroFeeSwapNeedsBalanceOf (passes in both currency orders): SystemBase fixture, seeded pool, 1 hour after opening; vm.mockCallRevert(IMD, abi.encodeWithSignature('balanceOf(address)', manager), 'paused'); then an exact-input sell of 1 wei SVO (IMD output 0, fee 0, nothing to take). Expected: the swap succeeds with a zero IMD delta. Actual: the unlock reverts from afterSwap. Vault side: after sync() of 10e18, mocking balanceOf(vault) to revert makes inferenceReserve() and a Safe call to withdrawInference(1) revert with TransferFailed (LifeForceVault.sol:122).

### 8. Info: ETH-era dead code (_sendETH, ETHSendFailed) remains in Guard and is compiled into the IMD-only vault

`src/Interfaces.sol:15`

```
    function _sendETH(address to, uint256 amount) internal {
```

Guard still declares error ETHSendFailed and the internal _sendETH low-level value call from the ETH-paired baseline. LifeForceVault, the only contract inheriting Guard, no longer calls it (it uses _sendIMD) and has no receive(); the function is unreachable. It is leftover surface from the fee-currency change this review was asked to scrutinise, it reads as if the vault might still move native ETH (the README says it pays in IMD only), and it costs bytecode in an immutable contract. Merged from three specialist reports. Fix: delete _sendETH and ETHSendFailed from Guard, or reduce Guard to the nonReentrant modifier. No behaviour change.

**Reproduction**

grep -rn '_sendETH\|ETHSendFailed' src test script (excluding test/scratch) returns only src/Interfaces.sol lines 13, 15 and 18: no call site in src/LifeForceVault.sol, src/SovrnHook.sol, the script or any delivered test. The vault uses only nonReentrant from Guard.

### 9. Info: Shortfall clamp on buybackOut is unreachable; reserves always sum exactly to the IMD balance, which the README understates

`src/LifeForceVault.sol:112`

```
        if (buybackOut > buyback) buybackOut = buyback;
```

In the balance < tracked branch, inferenceOut = min(inference, balance) and buybackOut = balance - inferenceOut. If inference <= balance then buybackOut = balance - inference < buyback (because balance < inference + buyback); otherwise buybackOut = 0 <= buyback. The clamp on line 112 can never fire, and in both branches inferenceOut + buybackOut == balance. README line 65 says the sum 'never exceeds the vault's IMD balance and equals it whenever the balance is at least the recorded checkpoints', a weaker property than the code guarantees (always equal). Not a defect. Fix: remove the dead line and state the exact invariant in README so future invariant tests check equality.

**Reproduction**

Any state: tracked (7e18, 3e18) with balance 9e18 gives views (7e18, 2e18), sum 9e18; with balance 5e18 gives (5e18, 0), sum 5e18. The delivered testFuzz_clampNeverExceedsBalance already asserts inference + buyback == balance for every fuzzed state (forge test --match-test testFuzz_clampNeverExceedsBalance passes), confirming equality rather than only the upper bound the README states.

---

Judge's submission `2da711c16a8b1432d5d6a2a1dc5ef02388313272f4b4ce72c11f5d50c81c7b12`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
