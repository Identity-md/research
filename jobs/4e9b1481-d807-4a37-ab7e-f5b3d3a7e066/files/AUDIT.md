# Audit report

> Project: PepesFamily, Pepes World vault
> Repo: github.com/0xtenang/PepesFamily (commit 6d550a2)
> Scope: contracts/src/world/PepesWorldVault.sol (about 150 lines). Tests: contracts/test/PepesWorld.t.sol and contracts/test/PepesWorld.fork.t.sol
> Chain: Robinhood Chain (4663)
>
> What it does
> A lifetime access pass for Pepes World, a browser game. A wallet can play if it holds at least 1 $EARN (one Pepes Earn IMD NFT, 0xf2363c208B1772C3c9dB7a3fe84d75Bf2881fc20) or if it entered through this vault.
>
> enter() / enterFor(player): the caller deposits passPrice $PEPES (0xE2C46c7068566740A33A4C93f5445B07BCfE5644, 50,000 at launch). It's one-time and non-refundable, and the pass never expires. Fee-on-transfer amounts are rejected.
> canPlay(player): true if the player has a pass or holds 1 $EARN or more.
> Owner only:
> grantPass: free passes.
> setPassPrice: future passes only; existing passes are never revoked.
> claimRewards(to): claims the IMD that the deposited $PEPES earns as a dividend token, and sends it on.
> withdraw(token, to, amount): any token.
> Two-step ownership transfer.
> Intended trust model: deposits belong to the team (the owner). Players get only the pass.
>
> Please check
>
> Can anyone except the owner move tokens out of the vault, including IMD rewards?
> Can a player's approval to the vault be used to take more than passPrice, or tokens from another wallet?
> Can anyone get a pass without paying (other than grantPass), or pay without getting one?
> Can anything lock the vault: enter reverting for honest users, or claimRewards / withdraw getting stuck?
> Interaction with $PEPES (PadTokenV1): plain transfers have no fee, the vault counts as a normal dividend holder, and claim() pays IMD to msg.sender. Any reentrancy or accounting issue in claimRewards?
> Is the canPlay check via $EARN.balanceOf >= 1e18 correct for DN404 (NFT = whole token)?
> Any problem with passPrice = 0, or with changing the price between a player's approve and their enter?
> Out of scope: the game website (access is checked in the browser only, and the game has no prizes). $PEPES and $EARN are already audited.

| | |
|---|---|
| Repository | https://github.com/0xtenang/PepesFamily.git |
| Commit | `6d550a2dd8daba2bec451431336125e584f0cb9e` |
| Job | `4e9b1481-d807-4a37-ab7e-f5b3d3a7e066` |
| Judged | 2026-10-05 08:47 UTC |
| Findings | 3 low · 2 info |

Four agents audited the code as it is at `6d550a2`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Low: enter()/enterFor() have no caller-side price ceiling: a setPassPrice that lands between approve and enter charges a player with excess allowance the new price

`contracts/src/world/PepesWorldVault.sol:89`

```
        uint256 amount = passPrice;
```

_enter reads passPrice from storage at execution time and pulls exactly that amount from msg.sender; the player cannot state the price they agreed to. The site (web/world/index.html, enterVault) approves exactly the displayed price, so for that path a raise makes enter() revert with SafeTransfer.TransferFailed (PadTokenV1's InsufficientAllowance is swallowed by the low-level call) and nothing moves; the player loses gas and must re-approve. But a wallet holding a larger or unlimited allowance to the vault (the default of many wallet prompts, and what the repo's own test setUp at contracts/test/PepesWorld.t.sol:62 does) is charged whatever passPrice is when its transaction executes, with no revert. Only the owner can raise the price, so this is a documented owner power rather than a permission bypass; it is the one path by which a player's approval can be used to take more than the price the player saw, which the brief asked about. Everything else checked for the brief holds: only the owner can move $PEPES or IMD out; _enter pulls only from msg.sender; hasPass is set before the pull inside one transaction, so nobody pays without a pass or gets one without paying (other than grantPass or a zero price); PadTokenV1 plain transfers have no fee so WrongAmountReceived never trips for honest users; IMD has no transfer hooks and claimRewards is owner-only, so there is no reentrancy surface; DN404._unit() is not overridden by PepesEarnToken, so balanceOf >= 1e18 is exactly one whole $EARN. Fix that keeps the design: add a maxPrice argument, e.g. enter(uint256 maxPrice) / enterFor(address player, uint256 maxPrice), and revert with a PriceAboveMax error when passPrice > maxPrice; the site passes the price it displayed. The no-arg overloads can stay as type(uint256).max wrappers.

**Reproduction**

Against the real src/v1/PadTokenV1.sol (test contract as pad). State: vault with passPrice = 50_000e18; bob holds 200_000e18 $PEPES and has approved the vault for type(uint256).max. Owner calls setPassPrice(150_000e18); bob calls enter(). Expected (from what bob saw when approving): 50_000e18 taken, or a revert. Actual: the call succeeds and bob's balance is 50_000e18 (150_000e18 taken). Control: alice approves exactly 50_000e18, owner sets price to 50_000e18 + 1, alice calls enter(): revert SafeTransfer.TransferFailed(), balance unchanged, no pass. Both run in a scratch Foundry test (test/scratch/Judge.t.sol, test_unlimitedAllowancePaysRaisedPrice and test_exactAllowanceRevertsOnRaise).

### 2. Low: withdraw() of the deposited $PEPES before claimRewards() forfeits the vault's share of holder fees still pending in the launchpad

`contracts/src/world/PepesWorldVault.sol:128`

```
        token.transferOut(to, amount);
```

PadTokenV1 credits holder fees at distribution time, not trade time: fees from swaps through routers other than the v1 router sit in PepesFamily v1 pendingHolderFees[token] until flush (AUDIT.md section 8, 'Fee timing on other routers'), and PadTokenV1.claim() calls pad.flush first, which distributes to whoever holds $PEPES at that moment. withdraw(pepes, to, amount) moves the vault's $PEPES out without claiming first, so any fee share earned by the vault's balance but not yet flushed is credited to the remaining holders at the next flush, and a later claimRewards returns 0 for it. The NatSpec (lines 18-20) promises the owner both the deposits and the IMD they earn; the two owner functions only deliver that when called in the order claimRewards then withdraw, which nothing enforces or documents. The fork test happens to claim before it withdraws, and the unit test test_withdrawKeepsPasses uses a mock with no pending-fee stage, so neither can see it. Fix that keeps the design: in withdraw, when token == pepes, call IPepesToken(pepes).claim() before transferOut (the claimed IMD stays in the vault for claimRewards or withdraw(imd)); at minimum document the required ordering in the NatSpec and the admin page.

**Reproduction**

Against the real src/v1/PadTokenV1.sol behind a stub pad whose flush forwards pending IMD to the token and calls distribute(). State: holders alice 150,000, bob 200,000, carol 1,000,000 and the vault 50,000 $PEPES (alice entered at 50_000e18); 14e18 IMD pending in the pad, withdrawableDividendOf(vault) == 0. Sequence A: owner calls withdraw(pepes, team, 50_000e18) then claimRewards(team). Expected: about 0.5e18 IMD (50,000/1,400,000 of 14e18). Actual: claimRewards returns 0 and carol's withdrawable dividend is positive; the share went to the other holders. Sequence B, same state, claimRewards(team) then withdraw: returns 0.5e18 minus dust. The attached proof (test/scratch/WithdrawOrder.t.sol) fails on this commit with '0 !~= 500000000000000000'.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {PepesWorldVault} from "src/world/PepesWorldVault.sol";
import {PadTokenV1} from "src/v1/PadTokenV1.sol";

/// @dev Minimal IMD stand-in.
contract QuoteToken {
    mapping(address => uint256) public balanceOf;

    function mint(address to, uint256 amt) external {
        balanceOf[to] += amt;
    }

    function transfer(address to, uint256 amt) external returns (bool) {
        balanceOf[msg.sender] -= amt;
        balanceOf[to] += amt;
        return true;
    }
}

/// @dev Stands in for $EARN: balanceOf only.
contract QuoteEarn {
    mapping(address => uint256) public balanceOf;
}

/// @dev Stands in for PepesFamily v1: holder fees from other routers sit pending until `flush`, which forwards
///      them to the token and distributes to whoever holds at that moment (PadTokenV1.claim() calls flush first).
contract StubPad {
    QuoteToken public imd;
    PadTokenV1 public token;
    uint256 public pending;

    function init(QuoteToken imd_) external {
        imd = imd_;
    }

    function launch(address router, address pm) external returns (PadTokenV1 t) {
        t = new PadTokenV1("Pepes", "PEPES", "", address(imd), address(this), router, pm);
        token = t;
    }

    function give(address to, uint256 amt) external {
        token.transfer(to, amt);
    }

    function addPending(uint256 amt) external {
        imd.mint(address(this), amt);
        pending += amt;
    }

    function flush(address) external {
        if (pending == 0) return;
        uint256 amt = pending;
        pending = 0;
        imd.transfer(address(token), amt);
        token.distribute();
    }
}

/// @notice Fails on the current code: `withdraw(pepes, ...)` moves the deposit out without claiming first, so the
///         holder fees still pending in the launchpad are distributed to the other holders and `claimRewards`
///         returns 0. Passes once `withdraw` claims the vault's dividend before moving $Pepes out.
contract WorldVaultWithdrawOrderTest is Test {
    QuoteToken imd = new QuoteToken();
    QuoteEarn earn = new QuoteEarn();
    StubPad pad = new StubPad();
    PadTokenV1 pepes;
    PepesWorldVault vault;
    address team = makeAddr("team");
    address alice = makeAddr("alice");
    address bob = makeAddr("bob");
    address carol = makeAddr("carol");
    uint256 constant PRICE = 50_000e18;

    function setUp() public {
        pad.init(imd);
        pepes = pad.launch(makeAddr("router"), makeAddr("pm"));
        vault = new PepesWorldVault(address(pepes), address(earn), team, PRICE);
        pad.give(alice, 200_000e18);
        pad.give(bob, 200_000e18);
        pad.give(carol, 1_000_000e18);
        vm.startPrank(alice);
        pepes.approve(address(vault), PRICE);
        vault.enter();
        vm.stopPrank();
    }

    function test_withdrawThenClaimKeepsVaultShare() public {
        // 14 IMD of holder fees earned while the vault holds 50k of 1.4M eligible supply, not yet flushed
        pad.addPending(14e18);
        assertEq(pepes.withdrawableDividendOf(address(vault)), 0, "nothing flushed yet");

        vm.startPrank(team);
        vault.withdraw(address(pepes), team, PRICE);
        uint256 got = vault.claimRewards(team);
        vm.stopPrank();

        // expected: the vault's 50k/1.4M share of 14 IMD, about 0.5 IMD, reaches the team either way
        assertApproxEqAbs(got, 0.5e18, 2, "the vault's share of pending fees");
        assertApproxEqAbs(imd.balanceOf(team), 0.5e18, 2, "team received it");
        assertEq(pepes.balanceOf(team), PRICE, "deposit withdrawn");
    }
}
```

### 3. Low: Constructor does not validate its dependencies: an ETH-quoted pad token makes claimRewards revert forever, and the $EARN mirror address makes canPlay false for every NFT holder

`contracts/src/world/PepesWorldVault.sol:62`

```
        imd = IPepesToken(pepes_).quote();
```

The constructor only zero-checks pepes_, earn_ and owner_; pepes, earn and imd are immutable, so a wrong argument is irreversible and there is no deploy script for the vault in contracts/script. Two mistakes slip through silently. (1) PadTokenV1 (and PadToken) use quote == address(0) for ETH-paired launches, and claim() pays such dividends with a raw ETH call to msg.sender. The vault stores imd = address(0), has no receive() or fallback(), so once any dividend is withdrawable, IPepesToken(pepes).claim() reverts with SafeTransfer.TransferFailed and claimRewards can never complete; withdraw(address(0), ...) cannot help because the ETH never arrives, and moving the $PEPES out does not move the dividend already accrued to the vault's address, so it is stranded in the token. (2) $EARN is a DN404 with two addresses: the token 0xf236...fc20 and its mirror 0x0e4b...5489 (deployments/robinhood-earn.json). DN404Mirror.balanceOf returns the NFT count (lib/dn404/src/DN404Mirror.sol:140), so with earn_ = mirror a wallet with one NFT reads 1 and canPlay's >= 1e18 is false for every holder; with an earn_ without code, canPlay reverts for everyone. The live $PEPES (0xE2C4...5644) is IMD-quoted and the fork test asserts vault.imd() == IMD, so the launch deployment is unaffected; this matters for a redeploy, another PepesFamily token, or a wrong argument. Fix: after reading quote(), `if (imd == address(0)) revert ZeroAddress();` (or add receive() if ETH-quoted tokens are meant to be supported, since SafeTransfer.transferOut already handles the address(0) path), and sanity-check earn_ with a read only the token satisfies (e.g. earn_.code.length != 0 and totalSupply() == 2_000e18).

**Reproduction**

(1) Deploy PadTokenV1 with quote_ = address(0) (test contract as pad, empty flush); new PepesWorldVault(token, earn, team, 50_000e18) succeeds and vault.imd() == address(0). Transfer 50_000e18 to the vault, send 1 ether to the token, call distribute(): withdrawableDividendOf(vault) is about 1e18. Owner calls claimRewards(team). Expected: team receives the owed ETH, or the constructor had rejected the token. Actual: revert TransferFailed() (trace: PadTokenV1.claim -> PepesWorldVault::receive reverts -> TransferFailed), on every later attempt as well. The attached proof (the audit_math specialist's test, run here) fails on this commit with exactly that error. (2) new PepesWorldVault(PEPES, 0x0e4bf5b83740F9E93ED739b2064165561CE75489, team, 50_000e18) with a wallet owning one Pepes Earn IMD NFT (mirror.balanceOf == 1, token.balanceOf == 1e18): canPlay(wallet) expected true, actual false, and earn is immutable so the vault must be redeployed.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {PepesWorldVault} from "src/world/PepesWorldVault.sol";
import {PadTokenV1} from "src/v1/PadTokenV1.sol";

/// @dev Stands in for $EARN: balanceOf only.
contract QuoteEarn {
    mapping(address => uint256) public balanceOf;
}

/// @notice PepesWorldVault built on a PadTokenV1 whose quote() is address(0) (dividends paid in ETH).
///         The test contract is the "pad" (PadTokenV1 sets pad = msg.sender): it holds the supply and answers flush.
contract WorldVaultEthQuoteTest is Test {
    address team = makeAddr("team");
    uint256 constant PRICE = 50_000e18;

    function flush(address) external {}

    /// Fails on the current code: the constructor stores imd = address(0), the vault has no receive(), so
    /// PadTokenV1.claim() cannot pay the vault and claimRewards reverts with TransferFailed while rewards are
    /// owed. Passes once the constructor rejects a token whose quote() is address(0), or the vault can take ETH.
    function test_ethQuotedPepesBricksClaimRewards() public {
        PadTokenV1 pepes =
            new PadTokenV1("Pepes", "PEPES", "", address(0), address(this), makeAddr("router"), makeAddr("pm"));
        QuoteEarn earn = new QuoteEarn();
        PepesWorldVault vault;
        try new PepesWorldVault(address(pepes), address(earn), team, PRICE) returns (PepesWorldVault v) {
            vault = v;
        } catch {
            return; // the constructor rejects an ETH-quoted token: fixed
        }
        assertEq(vault.imd(), address(0), "quote is ETH");

        // the vault holds one deposit; trades pay 1 ETH of holder fees to the token, which distributes them
        pepes.transfer(address(vault), PRICE);
        (bool ok,) = address(pepes).call{value: 1 ether}("");
        assertTrue(ok);
        pepes.distribute();
        uint256 owed = pepes.withdrawableDividendOf(address(vault));
        assertGt(owed, 0.99 ether, "the vault is owed about 1 ETH");

        vm.prank(team);
        uint256 got = vault.claimRewards(team); // current code: revert TransferFailed()
        assertEq(got, owed);
        assertEq(team.balance, owed);
    }
}
```

### 4. Info: passPrice = 0 turns enter()/enterFor() into open enrollment, including free passes for arbitrary addresses

`contracts/src/world/PepesWorldVault.sol:94`

```
        pepes.transferFrom(msg.sender, address(this), amount);
```

Nothing rejects a zero price. With passPrice == 0, _enter calls transferFrom(msg.sender, vault, 0), which PadTokenV1 accepts with no allowance and no balance (allowed < 0 is never true, and 0 <= balance), the balance-delta check is 0 == 0, and the pass is granted. Any wallet then gets a pass for free, and any caller can set hasPass[x] = true for any address x through enterFor, so passes stops being a count of paid entries while totalDeposited stays unchanged, and grantPass is redundant during that period. Nothing of value is lost (a pre-granted pass only makes that address's later enter()/grantPass() revert with AlreadyEntered), and it is consistent with the brief's team-set price, so this is behaviour to be aware of rather than a defect: zero means a free period. If free entry is meant to go only through grantPass, setPassPrice should reject 0 or _enter should require amount != 0.

**Reproduction**

Against the real PadTokenV1. Owner calls setPassPrice(0). A fresh address with 0 $PEPES and no approval calls enter() and then enterFor(carol). Expected if a zero price were meant to pause sales: revert. Actual: both succeed, hasPass(nobody) and hasPass(carol) are true, passes == 2, totalDeposited == 0 (test/scratch/Judge.t.sol, test_zeroPriceOpenEnrollment).

### 5. Info: Unit tests run only with an unlimited approval and mock tokens; the edges the brief asks about are untested

`contracts/test/PepesWorld.t.sol:62`

```
        pepes.approve(address(vault), type(uint256).max);
```

The 14 unit tests cover the happy paths, the owner guards and the fee-on-transfer rejection, but every entry test runs with alice holding a type(uint256).max approval and against MockPepesToken, whose claim() mints a preset amount with no eligible-supply, pending-fee or distribution stage. So the suite cannot show: a price raise between approve and enter (exact approval must revert, excess approval currently overpays); passPrice == 0 (free entry, no allowance); withdraw before claimRewards forfeiting pending fees; claimRewards returning 0 without reverting when nothing is owed; a PadToken whose quote() is address(0); transferOwnership(address(0)) as a cancel; withdraw of IMD or an unrelated token. test_enterNeedsBalanceAndApproval uses a bare vm.expectRevert() that also passes on an unrelated revert. The only coverage against the real token and the real $EARN is PepesWorld.fork.t.sol, which skips itself when FORK_RPC is unset, so CI reports green with no fork coverage. src/v1/PadTokenV1.sol deploys standalone (pad = msg.sender) and can be unit-tested behind a stub flush, as the scratch tests for this review do. There are no fuzz tests.

**Reproduction**

Run `forge test --match-path test/PepesWorld.t.sol`: 14 pass, none sets passPrice to 0, none changes passPrice between an approve and an enter, none calls claimRewards with nothing claimable, none uses PadTokenV1, none constructs the vault on a token whose quote() is address(0). Concrete missing assertions: approve exactly 50_000e18, setPassPrice(50_000e18 + 1), enter -> expected revert SafeTransfer.TransferFailed; approve type(uint256).max, setPassPrice(150_000e18), enter -> balance drops by 150_000e18; setPassPrice(0) then enter from a wallet with no allowance -> hasPass true, totalDeposited 0; claimRewards(team) on a fresh vault -> 0, no revert. All verified in test/scratch/Judge.t.sol during this review.

---

Judge's submission `fe7175cbef9cd0de4d39e453a06aeadc99409444948a851a0a88cd29b86e07f6`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
