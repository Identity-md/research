# Audit report

> TokenDrops: the treasure hunt for Courier World on Robinhood Chain (4663). The treasury (owner) funds drops of a launchpad token (CourierPad 0x90c3aaae34cf4681701452379D3819D6Bc8Fe8CC) or $STAMP: tokens per coin, coins out per day, a per-wallet daily cap, a daily cap across everyone, and a number of days. Players with an open post office (PostOffice 0x26D80804D0FA2F4598369E0062bFC9536d115D82) claim coins they found, for that day or the next, with EIP-712 vouchers Finds(player, drop, day, coins, deadline) signed by the game server’s key; claimMany pays several drops at once. Owner: topUp, endDrop (after today), withdraw (once claims have closed, or while paused), setSigner, setPaused; no renounce.
>
> Please check: that no drop can pay more than its own tokens or its caps allow, that drops’ tokens never mix, voucher replay across drops, days and wallets, the claim windows and day edges, re-entry, the owner’s powers, and the withdraw rules.
>
> Source: contracts/src/TokenDrops.sol; tests in contracts/test/TokenDrops.t.sol. Commit 30ade10.

| | |
|---|---|
| Repository | https://github.com/AdamNakamoto/courierworld.git |
| Commit | `30ade100d5b6f9463fcc1d1af46ede154f0833eb` |
| Job | `9755203f-4263-447d-b876-007724cd321b` |
| Judged | 2026-10-12 20:55 UTC |
| Findings | 1 medium · 2 low · 5 info |

Four agents audited the code as it is at `30ade10`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Medium: A day's payout is never bounded by `spots`: with dailyCoins = 0 (the default) or dailyCoins > spots a drop pays more coins than it put out, so a leaked signer key or server bug drains the whole pool i

`contracts/src/TokenDrops.sol:169`

```
        if (d.dailyCoins != 0) {
```

The brief lists four per-drop limits: tokens per coin, coins out per day (`spots`), a per-wallet daily cap (`maxPerWallet`) and a daily cap across everyone (`dailyCoins`). claimable() (lines 160-175) applies only the last two and the pool: `spots` is validated at createDrop (1..MAX_SPOTS, maxPerWallet <= spots) and stored, but never read on the claim path, and createDrop accepts any `dailyCoins`, including 0 ('only the pool limits it', the value the admin form sends for an empty field) and values far above `spots` (the admin form's default is dailyCoins = 100 with spots = 10). Since the game lays out exactly `spots` coins of a drop per day, any day on which paidCoins[id][day] exceeds `spots` is paying for coins that do not exist. With an honest server this cannot happen, but the contract's own threat model (setPaused NatSpec: 'if the server key leaks') is the case where it does: whoever holds the key signs Finds(wallet, id, day, maxPerWallet, deadline) for as many wallets with an open office as they control (an office costs 0.005 ETH and is permanent), for today and yesterday, and with dailyCoins = 0 takes the entire `left` of every drop before the owner can react. AUDIT.md section 13 states the exposure as 'up to each drop's daily limits ... until the owner pauses'; for dailyCoins = 0 there is no daily limit, so that statement is not true of the code. Merged from four specialists (audit_math, audit_permissions, audit_economics, audit_flow), all reproduced. Fix (defence in depth, keeps the design): in claimable() also bound the day's room by `d.spots - paidCoins[id][day]` (or use `d.spots` as the day cap when `d.dailyCoins == 0`), and in createDrop reject `dailyCoins > spots` or clamp it. Either changes what dailyCoins = 0 means, so it is a product decision for the treasury; if 'no daily limit' is wanted on purpose, AUDIT.md must say the pool is the only per-day bound and `spots` is informational.

**Reproduction**

createDrop(coin, perCoin = 1000e18, spots = 10, maxPerWallet = 10, dailyCoins = 0, startDay = today, days = 7, amount = 100_000e18). Alice (office open) claims a signer voucher Finds(alice, id, today, 10, deadline): 10 coins paid. Bob (office open) claims Finds(bob, id, today, 10, deadline). Expected: at most 10 coins paid for a day with 10 out, so bob gets 0 (NothingToClaim). Actual: bob is paid 10 more coins; paidCoins(id, today) == 20 while drop(id).spots == 10 and 20_000e18 tokens have left the drop. With three wallets paidCoins == 30; with dailyCoins = 1000 createDrop is accepted (test_DailyAboveSpots in test/scratch/JudgeProbe.t.sol). The attached proof fails on this code with 'a day paid more coins than were out: 20 > 10'.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import {Test} from "forge-std/Test.sol";
import {TokenDrops, IDropsPad, IDropsPostOffice} from "src/TokenDrops.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract PlainCoin {
    string public name = "Coin";
    string public symbol = "COIN";
    uint8 public decimals = 18;
    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    constructor(address to, uint256 amount) {
        balanceOf[to] = amount;
        totalSupply = amount;
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
        allowance[f][msg.sender] -= a;
        balanceOf[f] -= a;
        balanceOf[to] += a;
        return true;
    }
}

contract StubPad {
    mapping(address => uint64) public created;

    function add(address t) external {
        created[t] = uint64(block.timestamp);
    }

    function launches(address t) external view returns (address, address, uint64, uint64, bool) {
        return (address(0), address(0), created[t], 0, false);
    }
}

contract StubOffice {
    mapping(address => bool) public isOpen;

    function open(address w) external {
        isOpen[w] = true;
    }

    function offices(address w) external view returns (bool, uint8, uint8, uint16, uint64, address, uint256, uint256, uint256) {
        return (isOpen[w], 0, 0, 0, 0, address(0), 0, 0, 0);
    }
}

/// A drop puts `spots` coins out per day, yet with dailyCoins = 0 (the "no limit" default) the contract pays
/// any number of coins for one day: here 20 coins are paid on a day that had 10 out.
contract DropsSpotsCapTest is Test {
    TokenDrops drops;
    PlainCoin coin;
    PlainCoin stamp;
    StubPad pad;
    StubOffice office;
    address treasury = makeAddr("treasury");
    address alice = makeAddr("alice");
    address bob = makeAddr("bob");
    uint256 signerKey = 0x5160;
    uint256 constant PER = 1_000e18;

    function setUp() public {
        vm.warp(30 days);
        stamp = new PlainCoin(treasury, 1e24);
        coin = new PlainCoin(treasury, 1e27);
        pad = new StubPad();
        pad.add(address(coin));
        office = new StubOffice();
        office.open(alice);
        office.open(bob);
        drops = new TokenDrops(
            IERC20(address(stamp)), IDropsPad(address(pad)), IDropsPostOffice(address(office)), vm.addr(signerKey), treasury
        );
        vm.prank(treasury);
        coin.approve(address(drops), type(uint256).max);
    }

    function _voucher(address player, uint256 id, uint32 day, uint16 coins, uint64 deadline) internal view returns (bytes memory) {
        bytes32 structHash = keccak256(abi.encode(drops.FINDS_TYPEHASH(), player, id, day, coins, deadline));
        bytes32 domain = keccak256(
            abi.encode(
                keccak256("EIP712Domain(string name,string version,uint256 chainId,address verifyingContract)"),
                keccak256("Courier World Drops"),
                keccak256("1"),
                block.chainid,
                address(drops)
            )
        );
        (uint8 v, bytes32 r, bytes32 s) = vm.sign(signerKey, keccak256(abi.encodePacked("\x19\x01", domain, structHash)));
        return abi.encodePacked(r, s, v);
    }

    function claimAs(address who, uint256 id, uint32 day, uint16 coins) external returns (uint256) {
        uint64 deadline = uint64(block.timestamp + 1 hours);
        bytes memory sig = _voucher(who, id, day, coins, deadline);
        vm.prank(who);
        return drops.claim(id, day, coins, deadline, sig);
    }

    function test_ADayNeverPaysMoreCoinsThanItHasOut() public {
        uint32 day = drops.today();
        vm.prank(treasury);
        // 10 coins out a day, a wallet may be paid all 10, no cap across everyone (the "0: no limit" default).
        uint256 id = drops.createDrop(address(coin), PER, 10, 10, 0, day, 7, 100_000e18);

        this.claimAs(alice, id, day, 10);
        // Bob's voucher also says 10 found: with 10 coins out, only 0 can be left for him.
        try this.claimAs(bob, id, day, 10) {} catch {}

        assertLe(drops.paidCoins(id, day), drops.drop(id).spots, "a day paid more coins than were out");
        assertLe(coin.balanceOf(alice) + coin.balanceOf(bob), 10 * PER, "a day paid more tokens than its coins are worth");
    }
}
```

### 2. Low: claimMany is all-or-nothing: one voucher that is TooLate, Expired, FutureDay or NotRunning reverts the whole batch, contrary to its NatSpec, and the server's yesterday+today batches hit this at midnig

`contracts/src/TokenDrops.sol:196`

```
            total += _claim(c.drop, c.day, c.coins, c.deadline, c.signature);
```

claimMany's doc (line 191) and AUDIT.md section 13 say 'any that would pay nothing are skipped' / 'skips claims that would pay nothing and reverts only if all do'. That is true only when claimable() returns 0 (line 223). Every time-window failure inside _claim reverts instead: Expired (212), FutureDay (214), TooLate (215), NotRunning (217), plus UnknownDrop (211) and BadSignature (219), and claimMany has no per-entry skip. The integration relies on the documented semantics: the room signs vouchers for both day-1 and day with a 3600 s deadline (multiplayer/src/index.js lines 444-446) and the client submits all of them in one claimMany (web/chain.js claimAll, web/office.js line 537). A batch fetched shortly before 00:00 UTC and mined after it carries a day-1 voucher that is now two days old, so the whole transaction reverts with TooLate and the still-valid vouchers for the other day are not paid; the player loses the gas and must re-fetch and retry. A voucher whose one-hour deadline lapses in the mempool, or a server clock a few seconds ahead of the chain at the day edge (FutureDay), has the same effect. No funds are at risk. Merged from four specialists, all reproduced. Fix: in claimMany evaluate the window conditions (deadline, day > today, today >= day + CLAIM_DAYS, day outside the drop's days) per entry and `continue` on failure, keeping BadSignature/UnknownDrop as reverts and the final `total == 0` revert; or change the NatSpec and AUDIT.md and have the client drop stale vouchers before sending.

**Reproduction**

Drop 0: coin, perCoin 1e18, spots 10, maxPerWallet 10, dailyCoins 0, from day D-1 for 7 days, 100e18 in. Alice has an open office. At block.timestamp = (D+1)*86400 - 30 (23:59:30 on day D) the signer signs Finds(alice, 0, D-1, 3, deadline = now + 3600) and Finds(alice, 0, D, 2, same deadline). Alice calls claimMany([both]) at block.timestamp = (D+1)*86400 + 10 (00:00:10 on D+1, inside the deadline). Expected per the NatSpec: the D-1 entry pays nothing and is skipped, the D entry pays 2e18, total 2e18. Actual: the call reverts with TooLate() and nothing is paid; claim() with the D entry alone pays 2e18. The attached proof fails on this code with TooLate().

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import {Test} from "forge-std/Test.sol";
import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {TokenDrops, IDropsPad, IDropsPostOffice} from "src/TokenDrops.sol";

contract StalePad {
    function launches(address) external pure returns (address, address, uint64, uint64, bool) {
        return (address(0), address(0), 1, 1, false);
    }
}

contract StaleOffice {
    mapping(address => bool) public isOpen;

    function open(address who) external {
        isOpen[who] = true;
    }

    function offices(address who) external view returns (bool, uint8, uint8, uint16, uint64, address, uint256, uint256, uint256) {
        return (isOpen[who], 0, 0, 0, 0, address(0), 0, 0, 0);
    }
}

contract StaleCoin is ERC20 {
    constructor(address to) ERC20("Coin", "COIN") {
        _mint(to, 1_000_000e18);
    }
}

/// claimMany is documented as skipping claims that pay nothing, but a voucher for a day whose claim window has
/// just closed reverts the whole batch, so the still-valid vouchers in it are not paid.
contract DropsBatchStaleTest is Test {
    TokenDrops drops;
    StaleOffice office;
    StaleCoin coin;
    StaleCoin stamp;
    address treasury = makeAddr("treasury");
    address alice = makeAddr("alice");
    uint256 signerKey = 0x5160;

    function setUp() public {
        vm.warp(30 days);
        office = new StaleOffice();
        office.open(alice);
        coin = new StaleCoin(treasury);
        stamp = new StaleCoin(treasury);
        drops = new TokenDrops(stamp, IDropsPad(address(new StalePad())), IDropsPostOffice(address(office)), vm.addr(signerKey), treasury);
        vm.startPrank(treasury);
        coin.approve(address(drops), type(uint256).max);
        drops.createDrop(address(coin), 1e18, 10, 10, 0, drops.today(), 7, 100e18);
        vm.stopPrank();
    }

    function _voucher(uint256 id, uint32 day, uint16 coins, uint64 deadline) internal view returns (bytes memory) {
        bytes32 structHash = keccak256(abi.encode(drops.FINDS_TYPEHASH(), alice, id, day, coins, deadline));
        bytes32 domain = keccak256(
            abi.encode(
                keccak256("EIP712Domain(string name,string version,uint256 chainId,address verifyingContract)"),
                keccak256("Courier World Drops"),
                keccak256("1"),
                block.chainid,
                address(drops)
            )
        );
        (uint8 v, bytes32 r, bytes32 s) = vm.sign(signerKey, keccak256(abi.encodePacked("\x19\x01", domain, structHash)));
        return abi.encodePacked(r, s, v);
    }

    /// Vouchers for yesterday (D-1) and today (D) are fetched at 23:59:30 on day D with a one hour deadline, as the
    /// server issues them. The transaction lands at 00:00:10 on D+1. The D-1 voucher is now outside its claim
    /// window ("would pay nothing"); the day-D voucher is still valid and should be paid.
    function test_StaleYesterdayVoucherShouldNotBlockTodays() public {
        uint32 day = drops.today() + 1; // D
        vm.warp(uint256(day + 1) * 1 days - 30); // 23:59:30 on day D
        uint64 deadline = uint64(block.timestamp + 1 hours);
        TokenDrops.Claim[] memory cs = new TokenDrops.Claim[](2);
        cs[0] = TokenDrops.Claim(0, day - 1, 3, deadline, _voucher(0, day - 1, 3, deadline));
        cs[1] = TokenDrops.Claim(0, day, 2, deadline, _voucher(0, day, 2, deadline));

        vm.warp(uint256(day + 1) * 1 days + 10); // 00:00:10 on day D+1: still inside the deadline
        vm.prank(alice);
        uint256 total = drops.claimMany(cs);
        assertEq(total, 2e18, "today's finds are paid even though yesterday's window has closed");
        assertEq(coin.balanceOf(alice), 2e18);
    }
}
```

### 3. Low: withdraw while paused empties a running drop but leaves it in activeDrops, so the game keeps laying out and signing coins that pay nothing

`contracts/src/TokenDrops.sol:302`

```
        d.left = 0;
```

withdraw zeroes `left` but never touches startDay/endDay. For a running drop taken back under pause (the documented emergency path) activeDrops(day) still lists it for every remaining day after unpausing, so the room (multiplayer/src/index.js dropsOn/layDrops) keeps placing its `spots` coins and signing vouchers for finds, the UI shows a live drop with left == 0, and every claim(id, day, n, ...) reverts NothingToClaim (inside claimMany the entry is silently skipped). The web copy for IsPaused ('Your finds stay claimable until the day after') is not true once the owner has withdrawn. The owner has to remember a separate endDrop, which still leaves today's coins out. The same state arises when a drop with dailyCoins = 0 simply runs dry. Within the owner's documented powers and not a loss of funds; reported because the on-chain list the server trusts is wrong. Merged from audit_permissions and audit_economics, reproduced. Fix: have withdraw end the drop the way endDrop does (endDay = startDay - 1 if not started, else min(endDay, today())) unless it is already over, or require endDrop first when paused; alternatively have the server skip drops whose `left` is below `perCoin`.

**Reproduction**

createDrop(coin, 1000e18, 10, 5, 0, today, 30, 100_000e18) as id; owner: setPaused(true); withdraw(id, treasury); setPaused(false). Expected: the drop is no longer listed as having coins out. Actual: drop(id).left == 0 yet activeDrops(today + 1) == [id] (and so for the next 28 days); a player's claim(id, today + 1, 1, deadline, sig) reverts NothingToClaim. The attached proof fails on this code with 'an emptied drop is still laid out: 1 != 0'.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import {Test} from "forge-std/Test.sol";
import {TokenDrops, IDropsPad, IDropsPostOffice} from "src/TokenDrops.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract PlainCoin {
    string public name = "Coin";
    string public symbol = "COIN";
    uint8 public decimals = 18;
    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    constructor(address to, uint256 amount) {
        balanceOf[to] = amount;
        totalSupply = amount;
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
        allowance[f][msg.sender] -= a;
        balanceOf[f] -= a;
        balanceOf[to] += a;
        return true;
    }
}

contract StubPad {
    mapping(address => uint64) public created;

    function add(address t) external {
        created[t] = uint64(block.timestamp);
    }

    function launches(address t) external view returns (address, address, uint64, uint64, bool) {
        return (address(0), address(0), created[t], 0, false);
    }
}

contract StubOffice {
    function offices(address) external pure returns (bool, uint8, uint8, uint16, uint64, address, uint256, uint256, uint256) {
        return (true, 0, 0, 0, 0, address(0), 0, 0, 0);
    }
}

/// Withdrawing a running drop while paused empties it but leaves it running: once unpaused, activeDrops still
/// lists it, so the game server keeps laying its coins out and signing vouchers that pay nothing.
contract DropsWithdrawLeavesActiveTest is Test {
    TokenDrops drops;
    PlainCoin coin;
    PlainCoin stamp;
    StubPad pad;
    address treasury = makeAddr("treasury");
    uint256 constant PER = 1_000e18;

    function setUp() public {
        vm.warp(30 days);
        stamp = new PlainCoin(treasury, 1e24);
        coin = new PlainCoin(treasury, 1e27);
        pad = new StubPad();
        pad.add(address(coin));
        drops = new TokenDrops(
            IERC20(address(stamp)), IDropsPad(address(pad)), IDropsPostOffice(address(new StubOffice())), vm.addr(1), treasury
        );
        vm.prank(treasury);
        coin.approve(address(drops), type(uint256).max);
    }

    function test_AWithdrawnDropIsNotStillOut() public {
        uint32 day = drops.today();
        vm.startPrank(treasury);
        uint256 id = drops.createDrop(address(coin), PER, 10, 5, 0, day, 30, 100_000e18);
        drops.setPaused(true);
        drops.withdraw(id, treasury);
        drops.setPaused(false);
        vm.stopPrank();

        assertEq(drops.drop(id).left, 0);
        // Tomorrow the server reads the running drops to lay coins out: an empty drop must not be among them.
        vm.warp(block.timestamp + 1 days);
        assertEq(drops.activeDrops(day + 1).length, 0, "an emptied drop is still laid out");
    }
}
```

### 4. Info: claimable() ignores the claim window, the drop's days and pause, so it quotes payouts for days and states claim() rejects

`contracts/src/TokenDrops.sol:160`

```
    function claimable(uint256 id, address player, uint32 day, uint16 coins) public view returns (uint16 n, uint256 amount) {
```

claimable() is the public quote the front end reads (web/chain.js claimable) and the project's fuzz test uses to decide whether a claim is worth sending. It applies maxPerWallet, the pool and dailyCoins, but not startDay/endDay, FutureDay, TooLate or paused, which _claim() enforces at lines 212-217 and _checkClaimer() at 202 before calling it. The view therefore returns a non-zero (n, amount) for a future day, a day whose two-day window has closed, a day the drop was not running, and while paused. Harmless inside _claim() because the window checks run first; the gap is only in what integrators are told. Fix: return (0, 0) at the top of claimable() when `paused || day > today() || today() >= day + CLAIM_DAYS || day < d.startDay || day > d.endDay`, keeping the explicit reverts in _claim() for error reporting.

**Reproduction**

createDrop(coin, 1e18, 10, 10, 0, D, 1, 100e18): a one-day drop. claimable(id, alice, D+5, 3) returns (3, 3e18) although claim(id, D+5, 3, deadline, sig) reverts FutureDay(); claimable(id, alice, D-3, 3) returns (3, 3e18) although claim() reverts TooLate(); after setPaused(true) claimable(id, alice, D, 3) still returns (3, 3e18). Expected (0, 0) in each case. Reproduced in test/scratch/JudgeProbe.t.sol::test_ClaimableIgnoresWindow (passes on this code, documenting the behaviour).

### 5. Info: Owner powers recorded as trust assumptions: pause+withdraw(+unpause) can be atomic and takes tokens players have found but not claimed; setSigner lets the owner author vouchers; endDrop cannot express

`contracts/src/TokenDrops.sol:300`

```
        if (!paused && !cancelled && today() < d.endDay + CLAIM_DAYS) revert StillRunning();
```

These are the powers the brief asks for and they are implemented as specified (Ownable2Step, renounce disabled, so there is always an owner); none is a permission bypass. Recorded so the requester can weigh them and correct AUDIT.md section 13 where it overstates the protection. (1) setPaused(true); withdraw(id, to); setPaused(false) succeed as three calls in one block, so the statement that the owner 'can withdraw a running drop only by pausing first, which stops all claims, so players see it happen' gives players no actual window: finds have no on-chain record until claimed, so vouchers for today and yesterday that were still inside their window pay nothing afterwards. (2) setSigner(anyAddress) lets the owner install a key it controls and sign Finds for any wallet with an office, so a running drop's tokens can leave without any paused state, bounded only by maxPerWallet, dailyCoins and the pool (it is the treasury's own deposit, so no third-party loss, but the signer role is no independent check on the owner). (3) endDrop takes no day: an endDrop sent at 23:59:59 on day D and mined at 00:00:01 on D+1 ends on D+1 (`last = today()`), one extra day of coins. (4) The signer is a hot key in the server's environment (DROPS_KEY) and the sole authority for payouts; its blast radius is the subject of the medium finding. Merged from four specialists' trust entries, all reproduced. Optional narrowing that keeps the design: require a drop to be ended (or endDay + CLAIM_DAYS passed) before withdraw-while-paused unless an explicit emergency flag is passed; give endDrop an intended last-day parameter and revert if today() is already past it; emit the previous signer in SignerSet.

**Reproduction**

(1) createDrop(coin, 1e18, 10, 10, 0, today, 30, 100e18); alice holds a valid voucher for 1 coin today. Owner in one block: setPaused(true); withdraw(id, treasury); setPaused(false). All succeed; alice's claim(id, today, 1, ...) reverts NothingToClaim; treasury holds the 100e18 (test/scratch/JudgeProbe.t.sol::test_PauseWithdrawUnpauseAtomic). (2) Owner calls setSigner(A) where A is its own key, signs Finds(W, id, today, 10, now+3600) for office wallet W and W calls claim: 10e18 moves with paused == false (same mechanism as the shipped test_NewSignerOnly). (3) Drop endDay = D+29; owner's endDrop(id) mined at (D+1)*86400 + 1: drop(id).endDay == D+1, not D (test_EndDropAcrossMidnight).

### 6. Info: Tokens sent straight to the contract, or any balance above the drops' summed `left`, are stranded: withdraw only moves a drop's own `left` and there is no sweep

`contracts/src/TokenDrops.sol:301`

```
        uint256 amount = d.left;
```

Drop isolation is done correctly through per-drop `left` (verified: two drops of the same token keep their balances apart through a drain of one and a paused withdraw of the other, test/scratch/JudgeProbe.t.sol::test_SameTokenIsolation). The flip side is that any balance that is not some drop's `left` has no owner: a treasury transfer made directly instead of through topUp, or a launchpad token airdropped to the address, can never be recovered. Self-inflicted and low impact; a sweep of `balanceOf(token) - sum of that token's left` (tracked per token in createDrop/topUp/_claim/withdraw), owner only, would recover it.

**Reproduction**

Drop 0 of coin with 10e18. Treasury calls coin.transfer(drops, 5e18) directly. Owner: setPaused(true); withdraw(0, treasury). Expected: the treasury can recover everything it put in. Actual: coin.balanceOf(drops) == 5e18 with drop(0).left == 0 and no function that moves it (test_DirectTransferStuck).

### 7. Info: Deploy script defaults the drops owner to the broadcasting key when DROPS_OWNER is unset

`contracts/script/DeployTokenDrops.s.sol:30`

```
        address owner = vm.envOr("DROPS_OWNER", msg.sender);
```

The owner holds every treasury power over the drops (fund, end, pause, withdraw, set signer) and ownership can only move in two steps, never be renounced. The script falls back to msg.sender for the owner and deploy-drops.sh relies on the operator remembering to 'sign with the treasury'. If the broadcast is signed with another deployer key, the drops are owned by it until a transferOwnership/acceptOwnership round and the treasury's createDrop reverts OwnableUnauthorizedAccount. Suggest requiring DROPS_OWNER on chain 4663 (as PAD is required) or asserting owner == the treasury recorded in deployments/robinhood.json before broadcasting.

**Reproduction**

Run `DROPS_SIGNER=0x... ./script/deploy-drops.sh --broadcast --sender <deployerNotTreasury>` with DROPS_OWNER unset. Expected: the treasury owns TokenDrops. Actual: owner == <deployerNotTreasury> (line 30 picks msg.sender); treasury.createDrop(...) reverts OwnableUnauthorizedAccount(treasury) until ownership is transferred and accepted.

### 8. Info: Test suite pins every timestamp to 00:00:00 UTC and never exercises many wallets in one day, a failing batch entry, same-token isolation or claimable() outside the window

`contracts/test/TokenDrops.t.sol:80`

```
        vm.warp(30 days);
```

setUp warps to exactly 30 days and every later warp adds whole days, so every claim, endDrop and withdraw in the suite runs at the first second of a day (no '86400 - 1' or 'hours' warp exists). The day-edge rules (line 215 `now_ >= day + CLAIM_DAYS`, line 300 `today() < d.endDay + CLAIM_DAYS`) are never asserted at 23:59:59 against 00:00:00, which is where claimMany's atomicity bites and endDrop's timing matters. Also untested: more wallets than `spots` claiming on one day with dailyCoins = 0 (testFuzz_NeverOverpays uses two wallets with maxPerWallet 8 against spots 10, so it can never cross spots); claimMany with one stale or expired entry; claimable() for a day outside the drop or the window, or while paused; two drops of the same token with one drained and the other withdrawn under pause; a drop whose `left` is 0 still appearing in activeDrops; dailyCoins > spots being accepted; a $STAMP drop claimed against GOLDEN_SPOTS. The exact-second day edge, same-token isolation and replay-after-topUp checks pass in test/scratch/JudgeProbe.t.sol (the design holds there); the others surface the findings above. Merged from three specialists.

**Reproduction**

Observed from the test source: setUp() sets block.timestamp = 30 days (line 80) and every later warp is vm.warp(vm.getBlockTimestamp() + N days), so block.timestamp % 86400 == 0 in every test. Adding vm.warp(uint256(day + 2) * 1 days - 1) before a claim for `day` and vm.warp(uint256(day + 2) * 1 days) before the next claim and a withdraw gives assertions the suite lacks (both hold on this code: test_DayEdgeExactSeconds). A three-wallet claim on a dailyCoins = 0 drop asserting paidCoins <= spots fails on this code.

---

Judge's submission `a289264e76180c4657d1b1752c9231a4533127cd46c3abaf1445bb8d52355015`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
