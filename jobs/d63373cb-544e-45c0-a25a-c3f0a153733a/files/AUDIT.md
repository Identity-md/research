# Audit report

> Audit github.com/MirakoolDev/ham-maze/tree/robinhood-score-nft (commit f102368), the Solidity in contracts/src.
> This is a re-audit after fixes from the last one. Look hardest at:
> - HamBackerPass.sol (new): airdrop and lockMint, the ERC-721 Enumerable bookkeeping on transfer, safeTransferFrom.
> - HamPowerUps.sol: the game address is now a list of allowed games (setGame with a true/false flag). Check that only allowed games can record runs.
> - HamRobinhood.sol: free runs and the holder bonus when the holder NFT is a transferable pass, booster limits, fee and pot payouts, and signature replay.
> Rank the findings by severity.

| | |
|---|---|
| Repository | https://github.com/MirakoolDev/ham-maze.git |
| Commit | `f1023680fe7eac17b48697228af85c51118bbd4b` |
| Job | `d63373cb-544e-45c0-a25a-c3f0a153733a` |
| Judged | 2026-11-25 08:53 UTC |
| Findings | 1 high · 2 medium · 6 low · 1 info |

Four agents audited the code as it is at `f102368`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. High: HamPowerUps.open: a sealed pack's gun is re-dealt whenever any pack is opened, so its holder chooses the gun by choosing when (and in what order) to open

`contracts/src/HamPowerUps.sol:197`

```
        uint256 r = rnd % (MAX_PACKS - opened);
```

Merged from audit_economics and audit_flow (same root cause). open() fixes only the random word keccak256(blockhash(boughtAt), tokenId); _draw then reduces it modulo (MAX_PACKS - opened) and walks the kinds by cap - minted. Both change every time any pack is opened, so the same sealed pack maps to a different gun in every deck state. From the block after the purchase the word is public, so the holder can eth_call open() (or check in a contract) and only open when the pack shows the kind they want; otherwise they open one of their other sealed packs (or wait for anyone else's open) to re-deal. This breaks the header's guarantee that 'a bot cannot re-roll by choosing when to open'. Caps are finite, so each rare steered to the attacker is removed from honest buyers' odds; the flow specialist measured 81 EPICs out of 100 packs with selective opening versus 22 in id order, same hashes. Fix (keeps caps and the deck model): make the deck state a pack is dealt against independent of the holder, e.g. resolve packs strictly in tokenId order via a permissionless cursor once each purchase hash exists, or assign each pack a deck position at purchase and resolve via a lazy Fisher-Yates keyed by the purchase-block hash.

**Reproduction**

Lineup 4000/2000/2000/1000/1000, locked. Block 1000: alice buys pack #1, bob buys #2..#21; roll to 1001 with blockhash(1000) set. Simulated open(1) gives kind 1 (Marker). After bob opens one of his own packs, simulated open(1) gives kind 2. Expected: pack #1's contents fixed once blockhash(1000) exists. Actual: they change with every foreign open. Ran test/scratch/Proof_78dfad91592a.t.sol: FAIL 'pack #1 holds a different gun after someone else opened a pack: 1 != 2'. The flow specialist's 20-pack self-reordering proof also fails ('13 != 0' of 19 orderings change pack 1).

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {HamPowerUps} from "src/HamPowerUps.sol";

/// A sealed pack's contents must be fixed once the hash of its purchase block exists: the contract
/// says "a bot cannot re-roll by choosing when to open". Here alice's pack is priced against every
/// deck state bob's opens produce; a fair draw gives the same gun in all of them.
contract PackDrawOrderTest is Test {
    HamPowerUps pu;
    address owner = makeAddr("owner");
    address alice = makeAddr("alice");
    address bob = makeAddr("bob");

    function setUp() public {
        vm.warp(20_000 days + 3 hours);
        vm.roll(1000);
        pu = new HamPowerUps(owner);
        vm.startPrank(owner);
        pu.addKind("Marker", "COMMON", 4000);
        pu.addKind("Frost dart", "RARE", 2000);
        pu.addKind("Pulse", "RARE", 2000);
        pu.addKind("Blinker", "EPIC", 1000);
        pu.addKind("Snare", "EPIC", 1000);
        pu.lock();
        vm.stopPrank();
        vm.deal(alice, 100 ether);
        vm.deal(bob, 100 ether);
    }

    /// What alice's pack #1 holds if she opens it now (state is rolled back afterwards).
    function _peek() internal returns (uint256 kind) {
        uint256 snap = vm.snapshotState();
        kind = pu.kindOf(1);
        if (kind == 0) {
            vm.prank(alice);
            kind = pu.open(1);
        }
        vm.revertToState(snap);
    }

    function test_sealedPackContentsDoNotDependOnWhenItIsOpened() public {
        vm.prank(alice);
        pu.buy{value: 1 ether}(1); // pack #1
        vm.prank(bob);
        pu.buy{value: 1 ether}(20); // packs #2..#21, same block
        vm.roll(1001);
        vm.setBlockhash(1000, keccak256("the purchase block"));

        uint256 first = _peek(); // the hash of block 1000 is known: the contents should be settled
        for (uint256 id = 2; id <= 21; ++id) {
            vm.prank(bob);
            try pu.open(id) {} catch {} // other people opening their own packs
            assertEq(_peek(), first, "pack #1 holds a different gun after someone else opened a pack");
        }
    }
}
```

### 2. Medium: HamPowerUps.open: after 256 untouched blocks a pack is dealt from blockhash(block.number - 1), which the opener knows before sending

`contracts/src/HamPowerUps.sol:178`

```
        if (h == 0) h = blockhash(block.number - 1);
```

Merged from audit_math, audit_permissions, audit_economics, audit_flow. _keepSeal only stores blockhash(_lastBuyBlock) and only runs inside buy() and open(). If nobody calls either within 256 blocks after a purchase, blockhash(bought) and blockSeal[bought] are both 0 forever and open() falls back to the previous block's hash, which is public before the opening transaction is built and changes each block. The holder simulates open() per block and sends it only in a block that gives the kind they want; a failed attempt (someone touched the contract inside the window) costs nothing. Once lapsed, the pack stays re-rollable indefinitely. Fix: never deal from a hash known at call time; in the fallback re-commit (set boughtAt[tokenId] = block.number and require a second open in a later block), and/or add a public keepSeal() anyone can call.

**Reproduction**

Two kinds of 5000. Mallory buys pack #1 at block 1000; nobody buys or opens. For n = 1300..1339 with blockhash(n-1) = keccak256(abi.encode('block', n-1)), simulated open(1) returns kind 1 in some blocks and kind 2 in others. Expected: one kind regardless of the block. Actual: kind follows the block. Ran test/scratch/Proof_d68613aa4334.t.sol: FAIL 'the kind a pack opens to depends on the block its holder chooses'.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {HamPowerUps} from "src/HamPowerUps.sol";

/// A pack bought in block B, with no other buy or open on the contract for the next 256 blocks, has no
/// stored hash for B. `open` then falls back to blockhash(block.number - 1), which the holder knows before
/// sending: the same pack opens to a different kind depending on the block the holder picks.
contract LateOpenRerollTest is Test {
    HamPowerUps pu;
    address owner = makeAddr("owner");
    address mallory = makeAddr("mallory");

    function setUp() public {
        vm.warp(20_000 days + 3 hours);
        vm.roll(1000);
        pu = new HamPowerUps(owner);
        vm.startPrank(owner);
        pu.addKind("Marker", "Common", 5000);
        pu.addKind("Snare", "Legendary", 5000);
        pu.lock();
        vm.stopPrank();
        vm.deal(mallory, 1 ether);
    }

    function test_holderCannotPickTheKindByPickingTheBlock() public {
        vm.prank(mallory);
        uint256 id = pu.buy{value: 0.01 ether}(1);
        uint256 bought = block.number;

        // nobody touches the contract; mallory looks at 40 later blocks and what the pack would be in each
        uint256 first;
        bool differs;
        for (uint256 n = bought + 300; n < bought + 340; ++n) {
            uint256 snap = vm.snapshotState();
            vm.roll(n);
            vm.setBlockhash(n - 1, keccak256(abi.encode("block", n - 1)));
            vm.prank(mallory);
            try pu.open(id) returns (uint256 kind) {
                if (kind != 0) {
                    if (first == 0) first = kind;
                    else if (kind != first) differs = true;
                }
            } catch {}
            vm.revertToState(snap);
        }
        assertFalse(differs, "the kind a pack opens to depends on the block its holder chooses");
    }
}
```

### 3. Medium: HamRobinhood: the holder bonus is read from a momentary balanceOf, so one transferable Backer Pass gives the +10% bonus to every wallet it passes through in a day

`contracts/src/HamRobinhood.sol:856`

```
            holder: isHolder(player)
```

Merged from audit_math, audit_permissions, audit_economics, audit_flow. The free run is bound to the pass id (freeRunUsed[day][passId]), but _mintScore stamps holder = isHolder(player) (holderToken.balanceOf(player) > 0 at that moment) for every run, paid or free, and _settlePlace pays HOLDER_BONUS_BPS (10% of the place) from the treasury share for each top-3 holder-flagged Score. HamBackerPass is freely transferable (and safeTransferFrom calls onERC721Received, so a contract can borrow it for one transaction), so one pass flags any number of wallets per day: one pass can take 7% of the pot (4+2+1%) instead of at most 4%, with referral rewards then computed on the inflated amounts. Fix (keeps the perk following the holder): have the run name a passId with ownerOf(passId) == msg.sender and allow one holder-flagged run (or bonus) per pass per day, as playFreeRun does, or have the referee sign the holder flag. Note: boostBps is likewise only as strong as the referee's off-chain boostOf read at signing time if a booster token is transferable.

**Reproduction**

HamBackerPass with one pass (#3, airdropped to alice, lockMint), set as holderToken; fee 0.01 ETH; pot funded with 10 ETH. alice plays pass #3's free run (9000 pts), transfers #3 to bob, bob plays a paid run (8000), transfers #3 to carol, carol plays a paid run (7000). settle(day). Expected: at most one prize carries the bonus. Actual: all three prizes exceed their base share by 10%. Ran test/scratch/Proof_e1ff03733fbd.t.sol: FAIL 'one pass paid the holder bonus to more than one wallet's Score in a day: 3 > 1'.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {HamRobinhood} from "src/HamRobinhood.sol";
import {HamBackerPass} from "src/HamBackerPass.sol";

/// One Backer Pass is handed from wallet to wallet during a day. The free run is already one per pass per
/// day; the holder bonus is not: every wallet the pass passes through gets a holder-flagged Score, and each
/// top-3 one is paid +10% out of the treasury share.
contract HolderBonusPerPassTest is Test {
    HamRobinhood game;
    HamBackerPass pass;
    uint256 refereeKey = 0xA11CE;
    address owner = makeAddr("owner");
    address treasury = makeAddr("treasury");
    address alice = makeAddr("alice");
    address bob = makeAddr("bob");
    address carol = makeAddr("carol");
    uint256 constant FEE = 0.01 ether;

    function setUp() public {
        vm.warp(20_000 days + 3 hours);
        game = new HamRobinhood(
            owner,
            vm.addr(refereeKey),
            treasury,
            FEE,
            HamRobinhood.GameConfig({
                mazeSize: 12,
                cellSize: 7,
                sentries: 8,
                sentryHealth: 60,
                sentryDamage: 20,
                playerHealth: 100,
                magSize: 30,
                loops: 0
            })
        );
        pass = new HamBackerPass(owner);
        address[] memory to = new address[](1);
        uint256[] memory ids = new uint256[](1);
        to[0] = alice;
        ids[0] = 3;
        vm.startPrank(owner);
        pass.airdrop(to, ids);
        pass.lockMint();
        game.setHolderToken(address(pass));
        vm.stopPrank();
        vm.deal(bob, 1 ether);
        vm.deal(carol, 1 ether);
        vm.deal(address(this), 100 ether);
    }

    function _signed(address p, uint32 points)
        internal
        view
        returns (HamRobinhood.RunResult memory r, bytes memory sig)
    {
        uint256 day = game.currentDay();
        r = HamRobinhood.RunResult({points: points, timeMs: 90_000, kills: 2, completed: true, attempt: 0, boostBps: 0});
        bytes32 h = keccak256(
            abi.encodePacked("\x19Ethereum Signed Message:\n32", game.runDigest(day, p, 0, points, 90_000, 2, true, 0))
        );
        (uint8 v, bytes32 rr, bytes32 s) = vm.sign(refereeKey, h);
        sig = abi.encodePacked(rr, s, v);
    }

    function test_onePassPaysOneHolderBonusADay() public {
        uint256 day = game.currentDay();
        game.fundPot{value: 10 ether}(day);

        // alice uses pass #3's free run
        (HamRobinhood.RunResult memory r, bytes memory sig) = _signed(alice, 9000);
        vm.prank(alice);
        uint256 a = game.playFreeRun(r, sig, address(0), 3);

        // the same pass goes to bob, who pays for a run, then to carol, who pays for a run
        vm.prank(alice);
        pass.transferFrom(alice, bob, 3);
        (r, sig) = _signed(bob, 8000);
        vm.prank(bob);
        uint256 b = game.playRun{value: FEE}(r, sig, address(0));

        vm.prank(bob);
        pass.transferFrom(bob, carol, 3);
        (r, sig) = _signed(carol, 7000);
        vm.prank(carol);
        uint256 c = game.playRun{value: FEE}(r, sig, address(0));

        (uint256 pot,,,,,,) = game.dayInfo(day);
        vm.warp((day + 1) * 1 days + 16 minutes);
        game.settle(day);

        // there is one pass, so at most one prize may carry the holder bonus
        uint256 bonuses;
        if (game.prizeOf(a) > pot * 4000 / 10_000) bonuses++;
        if (game.prizeOf(b) > pot * 2000 / 10_000) bonuses++;
        if (game.prizeOf(c) > pot * 1000 / 10_000) bonuses++;
        assertLe(bonuses, 1, "one pass paid the holder bonus to more than one wallet's Score in a day");
    }
}
```

### 4. Low: HamDailyRun.enterFree: free run is still per wallet, so any transferable holder token gives a free entry to every wallet it visits

`contracts/src/HamDailyRun.sol:265`

```
        if (freeRunUsed[day][msg.sender]) revert FreeRunUsed();
```

From audit_flow. The per-pass fix was applied in HamRobinhood only. HamDailyRun (still in src and in script/Deploy.s.sol) checks isHolder(msg.sender) and a per-wallet flag, and its docs allow an ERC-721 or ERC-20 holder token. With any transferable holder token (HamBackerPass, an ERC-20) one token gives unlimited free entries per day, each competing for the pot paid by others; settle() also reads isHolder(p) at settle time (line 322), so the bonus goes to whoever holds the token then. Severity low because the intended Ethereum deployment uses the non-transferable FundingWorks pass; it becomes medium if configured with a transferable token. Fix: key the free run by token id (ownerOf(passId) == msg.sender, freeRunUsed[day][passId]) and record holder status at run time, or restrict setHolderToken to non-transferable tokens and document it.

**Reproduction**

HamDailyRun with HamBackerPass (one pass #3 to alice) as holderToken. alice.enterFree; alice transfers #3 to bob; bob.enterFree; bob transfers to carol; carol.enterFree. Expected: 1 free entry. Actual: dayInfo.entries == 3. Ran test/scratch/Lows.t.sol::test_dailyRunFreePerWallet: FAIL 'one pass gave several free runs in a day: 3 > 1'.

### 5. Low: HamRobinhood.withdrawTreasury zeroes the owed counters after the ETH call, erasing shares a re-entrant settle() adds; the ETH is stranded

`contracts/src/HamRobinhood.sol:590`

```
        if (amount != 0 && _trySend(treasury, amount)) {
            treasuryOwed = 0;
```

Merged from audit_math, audit_economics, audit_flow. withdrawTreasury caches treasuryOwed/backersOwed, sends with all gas, then assigns 0. settle() is not nonReentrant and adds to both counters, so if the treasury or backers recipient (documented as possibly a buyback vault or payout splitter) calls settle(day) for a due day while receiving, that day's shares are overwritten with 0. The ETH stays in the contract with no ledger entry and no function can ever release it. Only the recipients' own code can trigger it, hence low; the loss is permanent. Fix: subtract what was sent (treasuryOwed -= amount; backersOwed -= toBackers), or mark settle() nonReentrant.

**Reproduction**

treasury (= backers) is a contract whose receive() calls settle(d2) once. Day d1: alice plays (0.01 ETH), d1 settled. Day d2: bob plays, pot 0.014 ETH, not settled. After d2+1 day+16 min, withdrawTreasury(). Expected: treasuryOwed + backersOwed = 20% of d2 pot = 0.0028 ETH. Actual: 0, d2 settled. Ran test/scratch/Lows.t.sol::test_withdrawErasesReentrantSettle: FAIL 'settled share erased: 0 != 2800000000000000'.

### 6. Low: HamRobinhood: holder bonuses plus referral rewards can exceed the 10% treasury share; lower places are silently short-paid

`contracts/src/HamRobinhood.sol:510`

```
            uint256 bonus = _min(amount * HOLDER_BONUS_BPS / BPS, remainingTreasury);
```

From audit_math. Both the holder bonus and the referral reward are carved from treasuryShare (10% of the pot) and clamped with _min in place order. Three holder winners need 4%+2%+1% = 7% of the pot; their referrers then take 5% (10% with a crew) of the boosted prizes, another 3.85% (7.7%). Demand is 10.85%-14.7% against a 10% budget, so third (and partly second) place lose their promised bonus/reward depending only on rank order. Fix needs a decision: scale pro-rata when demand exceeds the share, or document that lower places can lose them.

**Reproduction**

Traced in _settlePlace with pot P, three holder-flagged winners all referred by dave with crewSize >= CREW_SIZE: 1st: bonus 0.04P, reward 0.044P (remaining 0.016P); 2nd: bonus 0.016P (promised 0.02P), reward 0 ; 3rd: bonus 0 (promised 0.01P), reward 0; treasuryOwed += 0. Expected: each holder gets +10%. Actual: 2nd/3rd shortchanged.

### 7. Low: HamPowerUps.recordRun: unbounded signed kills overflow the uint32 counter, after which the gun's stats freeze for good

`contracts/src/HamPowerUps.sol:230`

```
        s.kills += kills;
```

From audit_math. HamRobinhood caps points and boostBps but passes r.kills (any uint32) to recordRun; s.kills += kills is checked, so once kills reach near 2^32-1 every later recordRun reverts and is swallowed by the try/catch in _notifyRun: runs and kills never move again and the NFT shows ~4.29B kills. Requires a referee-signed absurd kills value (the faulty/leaked-key case the points cap exists for). Fix: bound r.kills in _play (sentries <= 64) or saturate the add.

**Reproduction**

Alice's equipped gun is token 1; she submits a signed run with kills = 4294967295, then a normal run with kills = 2. Expected: stats(1).runs == 2. Actual: 1. Ran test/scratch/Lows.t.sol::test_killsOverflowFreezesGun: FAIL 'second run not recorded: 1 != 2'.

### 8. Low: HamRobinhood.claimFinalize leaves prizeOf at the paid amount and approvals intact, so a paid, now-transferable Score still reads as a live prize

`contracts/src/HamRobinhood.sol:550`

```
        claimed[tokenId] = true;
```

Merged from audit_math, audit_economics, audit_flow. sweep() zeroes prizeOf, claimFinalize() does not; once claimed, isFrozen() is false again and pre-existing approvals/operator approvals survive. A seller can claimIntent, wait CLAIM_DELAY, claim, and have an older listing/bid fill against a Score whose prizeOf() still shows the prize, contradicting the header's 'no path to double-dip' for any buyer or marketplace reading prizeOf. Fix: set prizeOf[tokenId] = 0 in claimFinalize (the amount is in PrizeClaimed), and consider clearing _approved[tokenId] at claimIntent.

**Reproduction**

alice is the only player (fee 0.01 ETH), settle: prizeOf(1) = 0.004 ETH. claimIntent(1), +10 min, claimFinalize(1) pays 0.004 ETH. Expected: prizeOf(1) == 0. Actual: 4000000000000000, with claimed == true and isFrozen == false. Ran test/scratch/Lows.t.sol::test_prizeOfAfterClaim: FAIL 'prizeOf still shows a paid prize: 4000000000000000 != 0'.

### 9. Low: HamRobinhood: once claimIntent is called, a Score held by a contract that cannot receive ETH can neither be paid nor moved, and the prize is swept

`contracts/src/HamRobinhood.sol:553`

```
        _send(holder, amount);
```

From audit_economics. claimFinalize only pays msg.sender (the owner) and reverts TransferFailed if refused; after claimIntent the token is frozen (transferFrom reverts TokenFrozen) and there is no way to cancel the intent or name a recipient. After CLAIM_WINDOW anyone sweeps the prize into the pot. Fix: claimFinalize(tokenId, to) letting the owner choose the recipient, or allow cancelling an intent.

**Reproduction**

Traced: Score #1 with prize held by contract N without receive(). N.claimIntent(1); after CLAIM_DELAY N.claimFinalize(1) reverts TransferFailed (line 553 -> _send); N.transferFrom(N, alice, 1) reverts TokenFrozen (isFrozen true since claimed is false). After CLAIM_WINDOW, sweep(day, 1) moves the prize to the pot. Expected: owner can redirect payout. Actual: prize lost.

### 10. Info: Trust assumption: setBackers / setTreasury redirect already-accrued backersOwed / treasuryOwed

`contracts/src/HamRobinhood.sol:755`

```
    function setBackers(address backers_) external onlyOwner {
```

From audit_permissions. withdrawTreasury pays whatever address is current, and setBackers/setTreasury do not settle what is already owed, so the owner can redirect accrued backer payouts. Owner power by design; documented as a trust assumption. If backers should be protected, pay out backersOwed to the old address before switching.

**Reproduction**

backersOwed == 1 ether; owner calls setBackers(ownerWallet); anyone calls withdrawTreasury(): 1 ether goes to ownerWallet.

---

Judge's submission `acd41d4798486473c22d6d56cdc56c616a183770e7f4fec10d88831866eca217`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
