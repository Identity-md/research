# Audit report

> Audit the contracts in 0xtenang/PepesFamily as they are.

| | |
|---|---|
| Repository | https://github.com/0xtenang/PepesFamily.git |
| Commit | `7379f646769eb979a88dac9978c0d8a6b4429e72` |
| Job | `964f33f1-8840-4eec-9489-b908591ddbeb` |
| Judged | 2026-10-30 11:40 UTC |
| Findings | 1 high · 2 medium · 2 low |

Four agents audited the code as it is at `7379f64`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. High: PepesFamilyRemote: anyone can strand a remote-launched token's creator fees by calling the launchpad's public collectCreatorFees first

`contracts/src/PepesFamilyRemote.sol:157`

```
        uint256 before = IRemoteToken(quote).balanceOf(address(this));
```

A token launched through PepesFamilyRemote.launchFor has the remote contract as its creator on the launchpad, so PepesFamily.creatorPayout[token] == address(remote) (contracts/src/PepesFamily.sol:301). PepesFamily.collectCreatorFees(token) (contracts/src/PepesFamily.sol:497) is callable by anyone and takes the pending quote to creatorPayout, i.e. into the remote. PepesFamilyRemote.collectCreatorFees, the only path that pays the real creator (creatorOf[token]), forwards only the quote-balance delta of its own call (lines 157-160). Quote that reached the remote through a direct launchpad call is never forwarded: the remote has no sweep and no owner withdrawal, and later calls measure a zero delta. Because every token on a pad shares one quote, a stranded balance cannot be attributed to a token afterwards. A griefer can front-run every remote.collectCreatorFees(token) with pad.collectCreatorFees(token) and lock 100% of that creator's fees until the creator completes handOver + acceptCreatorPayout; everything collected before that is lost for good. An ordinary keeper or explorer user calling the public launchpad function causes the same loss by accident. Verified: the remote's only state-changing functions are launchFor, buyFor, collectCreatorFees, handOver, transferCreator, setPad and the ownership pair; none moves an existing ERC20 balance. Fix: do not let the remote be a payout address that direct collections pay into without attribution. Options: deploy a minimal per-token payout escrow (CREATE2 clone) as the launchpad creatorPayout for remote launches whose only function forwards its whole quote balance to creatorOf[token]; or read pad.pendingCreatorFees(token) before the call and forward that amount, combined with proposing the creator as payout at launch so direct collections cannot land in the remote. At minimum add a creator-callable sweep so already-stranded fees are recoverable.

**Reproduction**

State: remote.launchFor(pad, alice, 'Remote', 'RMT', '{}', FeeSplit(100,100,100), 0, 0, 0) so pad.creatorPayout(token) == address(remote). Bob buys with 10 WETH through PepesFamilyRouter.buy: pad.pendingCreatorFees(token) == 0.1e18. Input: griefer (any address) calls pad.collectCreatorFees(token); then anyone calls remote.collectCreatorFees(token). Expected: alice receives 0.1e18 quote. Actual: pad.collectCreatorFees takes 0.1e18 to the remote; remote.collectCreatorFees returns 0 and forwards nothing; weth.balanceOf(remote) stays 0.1e18 and no function can move it. Reproduced: contracts/test/scratch/RemoteStrandedCreatorFees.t.sol, run with `cd contracts && forge test --match-path test/scratch/RemoteStrandedCreatorFees.t.sol`, fails on this code with 'forwarded amount: 0 != 100000000000000000'.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {PoolManager} from "v4-core/src/PoolManager.sol";
import {PepesFamily} from "src/PepesFamily.sol";
import {PepesFamilyRouter} from "src/PepesFamilyRouter.sol";
import {PepesFamilyRemote, IRemotePad} from "src/PepesFamilyRemote.sol";
import {PadToken} from "src/PadToken.sol";
import {DeployLib} from "script/DeployLib.sol";

contract ScratchWETH {
    string public name = "Wrapped Ether";
    string public symbol = "WETH";
    uint8 public decimals = 18;
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    receive() external payable {
        deposit();
    }

    function deposit() public payable {
        balanceOf[msg.sender] += msg.value;
    }

    function withdraw(uint256 wad) external {
        balanceOf[msg.sender] -= wad;
        (bool ok,) = msg.sender.call{value: wad}("");
        require(ok, "withdraw");
    }

    function approve(address s, uint256 a) external returns (bool) {
        allowance[msg.sender][s] = a;
        return true;
    }

    function transfer(address to, uint256 a) external returns (bool) {
        return transferFrom(msg.sender, to, a);
    }

    function transferFrom(address f, address to, uint256 a) public returns (bool) {
        if (f != msg.sender && allowance[f][msg.sender] != type(uint256).max) allowance[f][msg.sender] -= a;
        balanceOf[f] -= a;
        balanceOf[to] += a;
        return true;
    }
}

/// @notice A token launched through PepesFamilyRemote has the remote contract as its `creatorPayout` on the
///         launchpad. The launchpad's `collectCreatorFees(token)` is callable by anyone and pays `creatorPayout`,
///         so anyone can make the creator fees land in the remote contract outside `PepesFamilyRemote.collectCreatorFees`,
///         which only forwards the balance delta of its own call. The fees are then stuck in the remote forever.
contract RemoteStrandedCreatorFeesTest is Test {
    PoolManager pm;
    ScratchWETH weth;
    PepesFamily pad;
    PepesFamilyRouter router;
    PepesFamilyRemote remote;
    address owner = makeAddr("owner");
    address filler = makeAddr("filler");
    address alice = makeAddr("alice"); // the real creator, who paid on another chain
    address bob = makeAddr("bob"); // a trader
    address griefer = makeAddr("griefer");

    function setUp() public {
        vm.warp(1_800_000_000);
        pm = new PoolManager(address(this));
        weth = new ScratchWETH();
        bytes memory initCode = abi.encodePacked(
            type(PepesFamily).creationCode,
            abi.encode(
                pm,
                address(weth),
                owner,
                makeAddr("fees"),
                DeployLib.startTickForMarketCap(1.5e18),
                PepesFamily.ImdEthPool(0, 0, address(0))
            )
        );
        (bytes32 salt,) = DeployLib.mineSalt(address(this), uint160(0x28CC), initCode, 0);
        address deployed;
        assembly {
            deployed := create2(0, add(initCode, 0x20), mload(initCode), salt)
        }
        pad = PepesFamily(deployed);
        router = PepesFamilyRouter(payable(pad.router()));
        address[] memory pads = new address[](1);
        pads[0] = address(pad);
        remote = new PepesFamilyRemote(owner, pads);
        vm.deal(filler, 100 ether);
        vm.deal(bob, 100 ether);
        vm.prank(bob);
        weth.deposit{value: 50 ether}();
        vm.prank(bob);
        weth.approve(address(router), type(uint256).max);
    }

    function test_anyoneCanStrandRemoteCreatorFees() public {
        // Alice launches cross-chain: the remote contract is the creator payout on the launchpad.
        vm.prank(filler);
        (address token,) = remote.launchFor(
            address(pad), alice, "Remote", "RMT", "{}", IRemotePad.FeeSplit(100, 100, 100), 0, 0, 0
        );
        assertEq(pad.creatorPayout(token), address(remote));

        // A trade accrues 1% creator fee: 0.1 WETH on a 10 WETH buy.
        vm.prank(bob);
        router.buy(token, 10 ether, 1, block.timestamp);
        assertEq(pad.pendingCreatorFees(token), 0.1 ether);

        // Anyone calls the launchpad's public collector directly: the fee lands in the remote contract.
        vm.prank(griefer);
        pad.collectCreatorFees(token);
        assertEq(pad.pendingCreatorFees(token), 0);
        assertEq(weth.balanceOf(address(remote)), 0.1 ether, "fee sits in the remote contract");

        // The remote's forwarder measures only the delta of its own call, so it forwards nothing.
        uint256 a0 = weth.balanceOf(alice);
        uint256 fwd = remote.collectCreatorFees(token);

        // Expected: the creator receives her 0.1 WETH. Actual: zero is forwarded and the WETH stays in the remote,
        // which has no function that can move it.
        assertEq(fwd, 0.1 ether, "forwarded amount");
        assertEq(weth.balanceOf(alice) - a0, 0.1 ether, "creator paid");
        assertEq(weth.balanceOf(address(remote)), 0, "remote keeps nothing");
    }
}
```

### 2. Medium: Buys through PepesFamilyRemote mark the Remote contract active, not the buyer: a repeat cross-chain buyer's rewards expire and anyone can recycle them to feeRecipient

`contracts/src/PepesFamilyRemote.sol:207`

```
        tokens = IRemoteEthRouter(IRemotePad(pad).ethRouter()).buyWithEth{value: value}(token, minTokens, block.timestamp);
```

Merged from two specialists (audit_flow and audit_permissions) reporting the same mechanism. PadToken's rule (contracts/src/PadToken.sol:18-25 and 239-245) is that a buy of any size through any router is the buyer's own activity: PepesFamily.afterSwap calls markActive(trader) on every buy (contracts/src/PepesFamily.sol:430-434), where trader is the address in hookData for the pad's own routers. PepesFamilyEthRouter and PepesFamilyNativeRouter put their msg.sender there (Route.user, contracts/src/PepesFamilyNativeRouter.sol:77 and :141). PepesFamilyRemote._buy calls ethRouter.buyWithEth itself (line 207), so hookData carries the Remote's address and markActive is applied to the Remote contract, never to the end buyer. The Remote then forwards the tokens with transfer (line 208); PadToken._update only records the recipient's activity when msg.sender == to or on a first receipt (contracts/src/PadToken.sol:233). A user who already holds the token and buys again only through the cross-chain path therefore never refreshes lastActive. After 7 days without a claim or send, expiredRewardsOf returns their rewards older than 7 days and anyone can call recycle(holder) to move them to the pad's feeRecipient, contradicting the documented rule and the Remote's own notice ('Tokens bought go straight to the user'). The victim loses funds they would keep had they bought through the router directly. Fix: let the Remote report the end user to the hook. Add buyWithEthFor(address user, ...) to PepesFamilyEthRouter and PepesFamilyNativeRouter that puts `user` in Route.user/hookData (keeping payout and refunds to msg.sender, the Remote, so its forwarding logic is unchanged), and have PepesFamilyRemote._buy call it with `to`.

**Reproduction**

Pad paired with a WETH9-like asset (ImdEthPool tickSpacing 0, so ethRouter is PepesFamilyNativeRouter), PepesFamilyRemote allowlisting the pad. t0: filler calls remote.launchFor{value: 1 ether}(pad, alice, ..., FeeSplit(0,300,0), buyValue=1 ether, minTokens=1, gasDrop=0): alice's first receipt sets lastActive[alice]=t0. t0: bob calls router.buy(token, 5 ether, 1, deadline): his 3% holder fee is distributed to alice (withdrawableDividendOf(alice) > 0). t0+6 days: filler calls remote.buyFor{value: 1 ether}(pad, token, alice, 1, 0). Expected: lastActive[alice] == t0+6 days. Actual: lastActive[alice] == t0 (1800000000 != 1800518400); the hook called markActive(address(remote)). t0+7 days+1 hour: expected expiredRewardsOf(alice) == 0 and recycle(alice) moves nothing. Actual: expiredRewardsOf(alice) == 194644400168944778 wei and recycle(alice) sends that WETH to feeRecipient although alice bought 25 hours earlier. Reproduced: contracts/test/scratch/RemoteActivity.t.sol, run with `cd contracts && forge test --match-path test/scratch/RemoteActivity.t.sol`; fails on this code at the lastActive assertion.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {PoolManager} from "v4-core/src/PoolManager.sol";
import {PepesFamily} from "src/PepesFamily.sol";
import {PepesFamilyRouter} from "src/PepesFamilyRouter.sol";
import {PepesFamilyRemote, IRemotePad} from "src/PepesFamilyRemote.sol";
import {PadToken} from "src/PadToken.sol";
import {DeployLib} from "script/DeployLib.sol";

/// @dev WETH9-like wrapped native coin, used as the pad's pair asset so the pad deploys a PepesFamilyNativeRouter.
contract ScratchWETH {
    string public name = "Wrapped Ether";
    string public symbol = "WETH";
    uint8 public decimals = 18;
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    receive() external payable {
        deposit();
    }

    function deposit() public payable {
        balanceOf[msg.sender] += msg.value;
    }

    function withdraw(uint256 wad) external {
        balanceOf[msg.sender] -= wad;
        (bool ok,) = msg.sender.call{value: wad}("");
        require(ok, "withdraw");
    }

    function approve(address s, uint256 a) external returns (bool) {
        allowance[msg.sender][s] = a;
        return true;
    }

    function transfer(address to, uint256 a) external returns (bool) {
        return transferFrom(msg.sender, to, a);
    }

    function transferFrom(address f, address to, uint256 a) public returns (bool) {
        if (f != msg.sender && allowance[f][msg.sender] != type(uint256).max) allowance[f][msg.sender] -= a;
        balanceOf[f] -= a;
        balanceOf[to] += a;
        return true;
    }
}

/// @notice A buy through PepesFamilyRemote must count as the end buyer's activity (PadToken: "a buy of any size,
///         through any router, is the buyer's own activity"). Today the hook marks the Remote contract instead, so
///         a repeat cross-chain buyer stays "inactive" and anyone can recycle their older rewards to feeRecipient.
contract RemoteActivityTest is Test {
    PoolManager pm;
    ScratchWETH weth;
    PepesFamily pad;
    PepesFamilyRouter router;
    PepesFamilyRemote remote;
    address owner = makeAddr("owner");
    address fees = makeAddr("fees");
    address filler = makeAddr("filler");
    address alice = makeAddr("alice"); // pays on another chain; the filler calls the Remote for her
    address bob = makeAddr("bob");

    function setUp() public {
        vm.warp(1_800_000_000);
        pm = new PoolManager(address(this));
        weth = new ScratchWETH();
        bytes memory initCode = abi.encodePacked(
            type(PepesFamily).creationCode,
            abi.encode(
                pm,
                address(weth),
                owner,
                fees,
                DeployLib.startTickForMarketCap(1.5e18),
                PepesFamily.ImdEthPool(0, 0, address(0))
            )
        );
        (bytes32 salt,) = DeployLib.mineSalt(address(this), uint160(0x28CC), initCode, 0);
        address deployed;
        assembly {
            deployed := create2(0, add(initCode, 0x20), mload(initCode), salt)
        }
        pad = PepesFamily(deployed);
        router = PepesFamilyRouter(payable(pad.router()));
        address[] memory pads = new address[](1);
        pads[0] = address(pad);
        remote = new PepesFamilyRemote(owner, pads);
        vm.deal(filler, 100 ether);
        vm.deal(bob, 100 ether);
        vm.prank(bob);
        weth.deposit{value: 50 ether}();
        vm.prank(bob);
        weth.approve(address(router), type(uint256).max);
    }

    function test_remoteBuyIsTheBuyersActivity() public {
        uint256 t0 = block.timestamp;
        // Alice launches with a buy from another chain: her first receipt records activity at t0.
        vm.prank(filler);
        (address token,) = remote.launchFor{value: 1 ether}(
            address(pad), alice, "Remote", "RMT", "{}", IRemotePad.FeeSplit(0, 300, 0), 1 ether, 1, 0
        );
        PadToken t = PadToken(payable(token));
        assertEq(t.lastActive(alice), t0, "first receipt counts");

        // Bob buys directly: his 3% holder fee is distributed to Alice, the only holder, at t0.
        vm.prank(bob);
        router.buy(token, 5 ether, 1, block.timestamp);
        assertGt(t.withdrawableDividendOf(alice), 0, "alice earned rewards at t0");

        // Six days later Alice buys again, through the Remote. A buy is the buyer's own activity.
        vm.warp(t0 + 6 days);
        vm.prank(filler);
        remote.buyFor{value: 1 ether}(address(pad), token, alice, 1, 0);
        assertEq(t.lastActive(alice), block.timestamp, "a buy through the Remote must mark the buyer active");

        // Seven days and an hour after t0 she has been active for just over a day: nothing of hers may expire.
        vm.warp(t0 + 7 days + 1 hours);
        assertEq(t.expiredRewardsOf(alice), 0, "an active holder's rewards don't expire");
        uint256 feesBefore = weth.balanceOf(fees);
        t.recycle(alice);
        assertEq(weth.balanceOf(fees), feesBefore, "nothing of alice's is recycled to feeRecipient");
    }
}
```

### 3. Medium: LevPool.withdraw is repriced by the coin pool's live tick in the execution block, with no minimum payout: a one-block spot push moves part of the leaving LP's money (mark plus stress fee) to the remai

`perps/contracts/src/LevPool.sol:125`

```
        assets = (r.shares * low) / totalSupply();
```

withdraw() pays min(value at request, value now), where 'value now' is cash minus owedHigh from LevLens.liabilityRange() (perps/contracts/src/LevLens.sol:109-145). owedHigh marks every open position at whichever of the live tick, the fast price and the slow price is worst for the pool (ticks[i] = [spot, fast, slow], owedHigh += _max3(...)), and each long's pnl is capped at its max win. The live tick is the coin pool's current slot0, which anyone can move inside one block (buy, let the withdrawal execute, sell back; the cost is the coin pool's round-trip LP fee, since fast and slow are untouched). A push of +49% on a coin carrying a 10x long marks that long at its full 400% max win, so owedHigh jumps to the sum of the longs' max wins (up to coverageBps = 50% of cash) and the leaving LP is paid that much less. The withdrawn shares are burned in full (line 131), so the unpaid ETH stays with the remaining shareholders, which the pusher can be (they need LP shares and the ability to order two swaps around the victim's withdraw in one block, e.g. by being or bundling through the sequencer). The LP has no slippage parameter: withdraw() takes no minAssets and the request-time snapshot only caps the payout from above. Compare deposit(), which prices at owedLow, a minimum over the three marks, so a push can never improve a depositor's price. Compounding effect (reported separately by the economics specialist as a low, merged here because it is the same function, root cause and fix): line 127 reads the stress-fee tier from the same momentarily reduced 'low', so the LP also pays a 0.5% to 2.5% stress fee computed from a ratio that the push created, on a pool in which no trader won anything. In the reproduction the mark costs 0.8 ETH and the fee adds 0.108 ETH (ratio 7.2025/8.0025 = 0.90 -> 150 bps). perps/AUDIT.md invariant 4 says LP share pricing can't be gamed. Fix: value withdrawals (and the stress-fee ratio) at the fast and slow marks only, keeping the live tick out of owedHigh; or add a minAssets argument to withdraw() so an LP can refuse a repriced payout. The proof asserts the first fix.

**Reproduction**

Fresh LevPool seeded with 0.001 ETH, LevExchange + LevLens as navSource, risk config with bands/spread switched off (as perps/contracts/test/Base.t.sol does), one market on a MockOracle at tick 0 with 400 ETH depth, maxLeverage 10, netCap 5 ETH. lp deposits 8 ETH. alice deposits 10 ETH and opens a 10x long with stake 0.2 ETH (size 2 ETH, max win 400% = 0.8 ETH). lp calls requestWithdraw(all shares): snapshot = 8.0025 ETH. Warp 1 day. Fast and slow still at tick 0. Expected payout: shares*low/supply with low = cash - 0 = 8.0025 ETH (capped by the snapshot), fee 0 since ratio 1.0. Attacker sets only the live tick to +4000 (~+49%) for that block (MockOracle.set(4000, 0, 0)); lp calls withdraw(). Actual payout: 7.0946 ETH (owedHigh = 0.8 ETH max win; pool.withdrawFeeBps() reads 150 in that block, so 0.108 ETH is kept as a stress fee as well). The live tick is reset right after; 0.908 ETH stays in the pool for the remaining shares. Reproduced: perps/contracts/test/scratch/LpWithdrawSpotPush.t.sol, run with `cd perps/contracts && forge test --match-path test/scratch/LpWithdrawSpotPush.t.sol`; fails on this code with '7094560679915010624 != 8002499687539057617'.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {LevExchange} from "src/LevExchange.sol";
import {LevExchangeAdmin} from "src/LevExchangeAdmin.sol";
import {LevPool} from "src/LevPool.sol";
import {LevLens} from "src/LevLens.sol";
import {RiskConfig} from "src/LevTypes.sol";
import {ILevPool, ILevExchange, ILevNav} from "src/interfaces/ILevPool.sol";
import {MockOracle} from "src/mocks/MockOracle.sol";

/// @dev An LP's matured withdrawal is repriced by whatever the coin pool's live tick shows in the block the
///      withdrawal executes. Fast and slow are untouched, so this is a one-block spot push, not a market move.
///      The LP has no minimum-payout parameter, so whatever the push takes stays with the remaining shares.
contract LpWithdrawSpotPushTest is Test {
    LevPool pool;
    LevExchange ex;
    LevExchangeAdmin exa;
    LevLens lens;
    MockOracle o;

    address owner = makeAddr("owner");
    address treasury = makeAddr("treasury");
    address lp = makeAddr("lp");
    address alice = makeAddr("alice");

    function setUp() public {
        vm.warp(1_750_000_000);
        pool = new LevPool{value: 0.001 ether}(owner);
        ex = new LevExchange(ILevPool(address(pool)), owner, treasury, address(new LevExchangeAdmin()));
        exa = LevExchangeAdmin(payable(address(ex)));
        lens = new LevLens(ex);
        vm.startPrank(owner);
        pool.setExchange(ILevExchange(address(ex)));
        pool.setNavSource(ILevNav(address(lens)));
        exa.setRiskConfig(
            RiskConfig({
                openBandSpotTicks: 30_000,
                openBandTrendTicks: 30_000,
                pumpBandTicks: 30_000,
                spreadBaseBps: 0,
                spreadImpactBps: 0,
                spreadMaxBps: 0,
                sizeTier5xBps: 500,
                sizeTier2xBps: 500,
                hourlyGrowthBps: 60_000,
                platformSizeBps: 100_000
            })
        );
        vm.stopPrank();
        o = new MockOracle(0, 400 ether);
        vm.prank(owner);
        exa.listMarket(o, 10, 5 ether);

        vm.deal(lp, 100 ether);
        vm.prank(lp);
        pool.deposit{value: 8 ether}();
        vm.deal(alice, 100 ether);
        vm.prank(alice);
        ex.deposit{value: 10 ether}();
    }

    function test_withdrawRepricedByOneBlockSpotPush() public {
        // alice: 10x long, 0.2 ETH stake (size 2 ETH = the coin cap), max win 400% = 0.8 ETH reserved
        vm.prank(alice);
        ex.open(0, true, 10, 0.2 ether, type(int24).max);

        // LP asks to leave with every share; the request snapshots the value at today's prices
        uint256 shares = pool.balanceOf(lp);
        vm.prank(lp);
        pool.requestWithdraw(shares);
        (, uint256 snapshot,) = pool.withdrawRequests(lp);

        vm.warp(block.timestamp + pool.withdrawCooldown());
        // nothing changed on the market: fast and slow still at tick 0
        (uint256 lowBefore,) = pool.navRange();
        uint256 honest = (shares * lowBefore) / pool.totalSupply();
        if (honest > snapshot) honest = snapshot;

        // one-block live-tick push of +49% (fast and slow untouched): every long marks at its max win
        o.set(4000, 0, 0);
        uint256 balBefore = lp.balance;
        vm.prank(lp);
        pool.withdraw();
        uint256 paid = lp.balance - balBefore;
        o.set(0, 0, 0); // the push is undone right after

        // Expected: the LP is paid what the request was worth (fast and slow never moved). Actual: 0.8 ETH less.
        assertEq(paid, honest, "withdrawal repriced by a one-block spot push");
    }
}
```

### 4. Low: LevLens._feesOwedLowerBound is not a lower bound: deposit-side NAV credits close fees (and holding fees) that bankrupt or liquidated positions never pay

`perps/contracts/src/LevLens.sol:163`

```
        uint256 closeFeeShare = (s.size * c.openFeeSizeBps * c.poolFeeShareBps) / (BPS * BPS);
```

liabilityRange() computes owedLow, from which LevPool prices deposits at high = cash - owedLow (perps/contracts/src/LevPool.sol:86-88, 172-176). The doc comment says the fee credit is 'A floor, so deposits never pay for fees that might not arrive'. _feesOwedLowerBound credits every open position on a side with the pool's share of a size-based close fee (size * openFeeSizeBps * poolFeeShareBps / BPS^2, line 163) plus accrued holding fees, regardless of the position's equity. But a position whose equity is <= 0 settles through LevExchange._outcome's liquidation branch with no fee and no holding fee beyond the stake+margin the pool already gets; liabilityRange already counts that position at -withMargin (line 138). So the same position is credited twice: once as the full stake+margin loss and again as a close-fee share and holding fee that will never be paid. The same over-credit applies to liquidations with small positive equity (fees = left - reward, which can be below the size-based fee) and to keeper max-win/trigger closes (the pool share is taken after keeperRewardBps). Effect: while such positions are open, previewDeposit/deposit price LP shares above any value the pool can realise, so new LPs overpay and existing LPs (and DEAD house shares) capture the difference. Magnitude per bankrupt position: 0.125% of size (defaults openFeeSizeBps 25, poolFeeShareBps 5000) plus any holding fee above the free waiver; bounded, and it grows with bankrupt open interest (e.g. on a stale feed). Fix: only credit closeFeeShare and holding fees for positions with positive equity at the pool-favourable price, i.e. compute the fee credit per position inside the liabilityRange loop and cap each position's total (pnl clamp + hold + fee share) at its stake+margin (lo += max(v - hold_i - feeShare_i, -withMargin)), and apply the keeper-reward haircut to the fee share.

**Reproduction**

Default config, neutral risk config, market listed at tick 0 with 400 ETH liquidity, LP deposits 8 ETH. Alice opens a 10x long with stake 0.2 ETH (size 2 ETH). After 60 s the oracle moves all ticks to -1625 (~-15%): pnl ~ -0.3 ETH, equity < 0, position not yet liquidated. pool.navRange() high = 8.206000 ETH. A keeper calls liquidate(id): equity <= 0 so the pool books exactly the 0.2 ETH stake and no fee. navRange() afterwards (no positions left) = 8.203500 ETH. Expected: high before liquidation <= 8.2035 ETH. Actual: 8.2060 ETH, overstated by 0.0025 ETH = 2 ETH * 25 * 5000 / 1e8, the close-fee share of a position that pays no fee. Reproduced: perps/contracts/test/scratch/NavFloor.t.sol, run with `cd perps/contracts && forge test --match-path test/scratch/NavFloor.t.sol`; fails on this code with '8206000000000000000 > 8203500000000000000'.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {LevExchange} from "src/LevExchange.sol";
import {LevExchangeAdmin} from "src/LevExchangeAdmin.sol";
import {LevPool} from "src/LevPool.sol";
import {LevLens} from "src/LevLens.sol";
import {RiskConfig} from "src/LevTypes.sol";
import {ILevPool, ILevExchange, ILevNav} from "src/interfaces/ILevPool.sol";
import {MockOracle} from "src/mocks/MockOracle.sol";

/// A bankrupt, not-yet-liquidated position: liabilityRange's "lower bound" still credits the pool with that
/// position's close-fee share, so the deposit price (cash - owedLow) is above what the pool can ever book.
contract NavFloorTest is Test {
    LevPool pool;
    LevExchange ex;
    LevExchangeAdmin exa;
    LevLens lens;
    MockOracle o0;
    address owner = makeAddr("owner");
    address lp = makeAddr("lp");
    address alice = makeAddr("alice");

    function setUp() public {
        vm.warp(1_750_000_000);
        pool = new LevPool{value: 0.001 ether}(owner);
        ex = new LevExchange(ILevPool(address(pool)), owner, makeAddr("treasury"), address(new LevExchangeAdmin()));
        exa = LevExchangeAdmin(payable(address(ex)));
        lens = new LevLens(ex);
        vm.startPrank(owner);
        pool.setExchange(ILevExchange(address(ex)));
        pool.setNavSource(ILevNav(address(lens)));
        exa.setRiskConfig(
            RiskConfig({
                openBandSpotTicks: 30_000,
                openBandTrendTicks: 30_000,
                pumpBandTicks: 30_000,
                spreadBaseBps: 0,
                spreadImpactBps: 0,
                spreadMaxBps: 0,
                sizeTier5xBps: 500,
                sizeTier2xBps: 500,
                hourlyGrowthBps: 60_000,
                platformSizeBps: 100_000
            })
        );
        o0 = new MockOracle(0, 400 ether);
        exa.listMarket(o0, 10, 5 ether);
        vm.stopPrank();
        vm.deal(lp, 100 ether);
        vm.prank(lp);
        pool.deposit{value: 8 ether}();
        vm.deal(alice, 10 ether);
        vm.prank(alice);
        ex.deposit{value: 10 ether}();
    }

    function test_depositPriceCountsCloseFeeOfBankruptPosition() public {
        vm.prank(alice);
        uint256 id = ex.open(0, true, 10, 0.2 ether, type(int24).max); // size 2 ETH
        vm.warp(block.timestamp + 60);
        o0.setAll(-1625); // about -15%: pnl about -0.3 ETH on a 0.2 ETH stake, equity < 0

        (, uint256 highBefore) = pool.navRange();
        // Liquidating books exactly the stake to the pool (equity <= 0: no fees, no reward).
        vm.prank(makeAddr("keeper"));
        ex.liquidate(id);
        (uint256 lowAfter, uint256 highAfter) = pool.navRange();
        assertEq(lowAfter, highAfter, "no positions left");

        // The deposit price must never be above what the pool really ends up holding for that position.
        assertLe(highBefore, highAfter, "deposit-side NAV overstated before the liquidation");
    }
}
```

### 5. Low: PepesFamilyRemote.transferCreator leaves a pending launchpad-side handover in place, so the old creator can keep the fee role after passing it on

`contracts/src/PepesFamilyRemote.sol:174`

```
    function transferCreator(address token, address to) external {
```

Two handover paths exist for a remote-launched token: handOver (line 166, proposes creatorOf[token] as the launchpad's creatorPayout via pad.setCreatorPayout, which the creator later accepts) and transferCreator (line 174, changes creatorOf in the remote only). They are not mirrored: transferCreator does not cancel a proposal the old creator already made on the launchpad (pad.pendingCreatorPayout[token]). After handOver then transferCreator(to), the old creator can still call pad.acceptCreatorPayout(token) (contracts/src/PepesFamily.sol:511-516) and becomes the launchpad's creatorPayout, taking every future creator fee directly. The new creator's handOver then reverts on the launchpad (PepesFamily.setCreatorPayout checks msg.sender == creatorPayout, contracts/src/PepesFamily.sol:506, which is now the old creator), and remote.collectCreatorFees forwards nothing because the launchpad no longer pays the remote. Low because the old creator must have been the creator to set it up, so the loss is confined to whoever bought or was handed the role from them. Fix: in transferCreator, if pad.pendingCreatorPayout(token) != address(0) call pad.setCreatorPayout(token, address(0)) to cancel it (the remote is still the launchpad payout at that point); and revert transferCreator/handOver when pad.creatorPayout(token) != address(this), since the role has already left the remote.

**Reproduction**

State: token launched via remote.launchFor with creator alice, FeeSplit(100,100,100). Sequence: (1) alice calls remote.handOver(token): pad.pendingCreatorPayout(token) == alice. (2) alice calls remote.transferCreator(token, bob): remote.creatorOf(token) == bob. (3) alice calls pad.acceptCreatorPayout(token). Expected: bob holds the creator role and receives creator fees; alice's accept should fail. Actual: pad.creatorPayout(token) == alice; bob's remote.handOver(token) reverts with PepesFamily.NotCreator; after a 10 WETH buy, remote.collectCreatorFees(token) returns 0 and pad.collectCreatorFees(token) pays alice 0.1 WETH. Reproduced with a scratch test (contracts/test/scratch/RemoteTransferCreator.t.sol, asserting the actual behaviour above) that passes on this code, run with `cd contracts && forge test --match-path test/scratch/RemoteTransferCreator.t.sol`.

---

Judge's submission `d1b6311f93af8d08e7efea8824ccedb3e47cc325c70d9460221bf2f8f804ab05`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
