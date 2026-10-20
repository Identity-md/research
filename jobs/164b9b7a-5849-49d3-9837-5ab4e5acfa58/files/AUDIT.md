# Audit report

> Audit the contracts in AdamNakamoto/delivermail as they are.

| | |
|---|---|
| Repository | https://github.com/AdamNakamoto/delivermail.git |
| Commit | `e796f38c17729de0e79b62482dee7445800c109e` |
| Job | `164b9b7a-5849-49d3-9837-5ab4e5acfa58` |
| Judged | 2026-10-20 02:22 UTC |
| Findings | 3 low · 5 info |

Four agents audited the code as it is at `e796f38`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Low: Owner can keep minting for free after the sale first closes by reopening it at price 0; the ownerMint lock is cosmetic

`p2e/contracts/src/MessengerNFT.sol:154`

```
        if (open && seed != 0) revert AlreadyRevealed(); // the sale can't reopen once traits are knowable
```

AUDIT.md's admin table says the MessengerNFT owner can't 'mint after the sale closed' and guarantee 13 says ownerMint works only until the sale first closes. ownerMint (line 148) is indeed refused once saleClosedAt != 0, but setSaleOpen(true) only refuses to reopen once seed != 0, setPrice has no bound, and the public mint checks only saleOpen and msg.value == price * quantity. So after the first close the owner can reopen the sale, set the price to 0 and call mint(10) repeatedly, minting any number of remaining ids to itself for nothing: the same effect ownerMint was locked to prevent, by the same actor. The trait-knowledge protection still holds (a reveal needs a close in an earlier block, and mint needs the sale open, so the owner cannot mint in or after the reveal block), so this is a gap between the documented guarantee and the code rather than a loss path for holders. Fix options, which are a design decision: (a) make the first close final by reverting in setSaleOpen when open && saleClosedAt != 0, which matches the stated guarantee but removes pause-and-resume of the public sale; or (b) keep reopening and correct AUDIT.md and the ownerMint comment to say the owner can reopen the sale at any price, including 0, until the reveal, and that only trait-known minting is prevented.

**Reproduction**

State: fresh MessengerNFT (seed == 0, as in P2E.t.sol setUp). Owner: setSaleOpen(true); setSaleOpen(false) -> saleClosedAt = block.number. Owner: ownerMint(owner, 1) -> reverts SaleClosed as documented. Owner: setSaleOpen(true) -> succeeds (only seed != 0 is refused); setPrice(0); mint(10) with msg.value 0 -> succeeds; mint(10) again -> succeeds. Expected per AUDIT.md ('Can't: mint after the sale closed'): no owner-driven minting after the first close. Actual: totalMinted rises by 20 and the owner holds 20 new Messengers for 0 ETH. Reproduced on this tree with test/scratch/GameJudge.t.sol::test_OwnerMintsForFreeAfterFirstClose (passes, i.e. the bypass works) and with the specialist's proof test/scratch/Proof_671c.t.sol, which fails here with 'owner minted after the sale first closed: 1 != 0' and passes once reopening after the first close is refused.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {MessengerNFT} from "src/MessengerNFT.sol";
import {DevTransferValidator} from "src/DevTransferValidator.sol";

/// Fails on the current code: after the sale first closes the owner reopens it at price 0 and mints for free.
/// Passes once the first close is final (setSaleOpen(true) reverts when saleClosedAt != 0) or public mint
/// is refused after the first close.
contract NoMintAfterFirstCloseTest is Test {
    MessengerNFT nft;
    address owner = makeAddr("owner");
    address treasury = makeAddr("treasury");

    function setUp() public {
        vm.prank(owner);
        nft = new MessengerNFT(owner, treasury, owner, 0.01 ether, keccak256(abi.encode(bytes32("s"))), address(new DevTransferValidator()), "ipfs://x/");
    }

    function test_NoMintingAfterTheSaleFirstCloses() public {
        vm.startPrank(owner);
        nft.setSaleOpen(true);
        nft.setSaleOpen(false); // first close
        vm.expectRevert(MessengerNFT.SaleClosed.selector);
        nft.ownerMint(owner, 1); // documented: no owner minting from here on
        // The bypass: reopen, price 0, public mint.
        try nft.setSaleOpen(true) {} catch {}
        nft.setPrice(0);
        try nft.mint(1) {} catch {}
        vm.stopPrank();
        assertEq(nft.totalMinted(), 0, "owner minted after the sale first closed");
    }
}
```

### 2. Low: Donations to the MAIL/ETH pool are accepted and permanently stranded: the hook's donate revert stubs never run because the hook address carries no donate flags

`p2e/contracts/src/MailHook.sol:465`

```
    function beforeDonate(address, PoolKey calldata, uint256, uint256, bytes calldata) external pure returns (bytes4) {
        revert HookNotAllowed();
    }
```

The 'Disabled hook paths' section implements beforeDonate and afterDonate as unconditional HookNotAllowed reverts, reading as 'donating to this pool is refused like adding liquidity is'. But HOOK_FLAGS (line 71) and the permissions validated in the constructor (lines 149-150: beforeDonate: false, afterDonate: false) do not include BEFORE_DONATE_FLAG or AFTER_DONATE_FLAG, and the deploy script and tests mine an address with exactly 0x28CC. v4-core's Hooks library only calls a hook function whose flag bit is set in the hook address, so PoolManager.donate on the pool goes straight through and the two stubs are dead code (as are afterInitialize, afterAddLiquidity, before/afterRemoveLiquidity). Donated ETH or MAIL is credited as fee growth to the single launch position owned by the hook, and the hook has no code path that calls modifyLiquidity after openPool (that is guarantee 18), so the donated value can never be collected by anyone; collectProtocolFees moves only ERC-6909 claims and never sees it. The loss falls on whoever donates (a mistaken integration, a 'tip the pool' UI, a router that pays fees via donate), so there is no third-party victim, but the contract's stated intent and its behaviour disagree and the suite never calls donate. Fix, preserving the design: add Hooks.BEFORE_DONATE_FLAG to HOOK_FLAGS and set beforeDonate: true in the validated permissions (the mined flags become 0x28EC; the deploy config and the tests' _flags() change with it) so donate reverts HookNotAllowed as the stub promises; or delete the unreachable stubs and document that donations are accepted and unrecoverable.

**Reproduction**

State: pool opened (openPool) and one buy done so the launch position is in range (router.buy{value: 1 ether}). Input: alice calls PoolDonateTest(pm).donate{value: 1 ether}(hook.poolKey(mail), 1 ether, 0, ''). Expected (per the stub and the 'Disabled hook paths' comment): revert MailHook.HookNotAllowed. Actual: the call succeeds, address(pm).balance rises by exactly 1e18 wei, hook.pendingProtocolFees(address(0)) is unchanged, the hook's ERC-6909 ETH claim balance is unchanged, and no function on MailHook or MailRouter can withdraw that ETH. Before any buy the same call reverts, but with v4's NoLiquidityToReceiveFees (no in-range liquidity), not with the hook's error. Reproduced on this tree with test/scratch/HookJudge.t.sol::test_DonateIsNotBlockedAndIsStranded (passes) and test_DonateBeforeAnyBuy (reverts NoLiquidityToReceiveFees), using PoolManager and PoolDonateTest from v4-core at the pinned commit.

### 3. Low: The 4% fee is pool-scoped, not token-scoped: a second MAIL/ETH pool without the hook trades fee-free, so 'every trade pays 4% through any router' is not enforceable

`p2e/contracts/src/MailHook.sol:419`

```
    function beforeInitialize(address, PoolKey calldata, uint160) external pure returns (bytes4) {
        revert HookNotAllowed();
    }
```

README and the audit request say that 'every trade pays 4% of its ETH side to the fee recipient, through any router'. The hook only governs pools whose PoolKey names MailHook: beforeInitialize blocks a second pool on this hook, but MailToken is a plain ERC20 with no transfer tax, so anyone can initialize another Uniswap v4 pool for the same pair with hooks = address(0) (or list MAIL on any other DEX), seed it with MAIL bought once from the official pool plus ETH, and route all further trading there. None of MailHook's callbacks run for that pool, pendingProtocolFees never grows and feeRecipient earns nothing on that volume. Arbitrage keeps both pools priced alike, so the fee-free venue attracts volume over time and the 4% revenue assumption in the tokenomics is not enforceable on-chain. This is a design limit of 'tax in the hook, not in the token' rather than a guard failure; there is no contract-level fix that keeps the stated no-transfer-tax design. AUDIT.md's own wording ('every swap in the pool') is accurate; the README and request wording ('every trade', 'through any router') is not. Fix: state the limit in AUDIT.md next to 'The token itself has no transfer tax' and correct the README tokenomics wording, or accept a transfer tax, which is a scope decision.

**Reproduction**

State: official pool open (hook.openPool(mail)). 1) alice: router.buy{value: 10 ether}(mail, 1, now) -> hook.pendingProtocolFees(ETH) == 0.4 ether. 2) anyone: pm.initialize(PoolKey{currency0: ETH, currency1: MAIL, fee: 3000, tickSpacing: 60, hooks: address(0)}, sqrtPriceX96 of the official pool) -> succeeds (MailHook.beforeInitialize is never consulted because the key's hook is address(0)). 3) alice: PoolModifyLiquidityTest.modifyLiquidity{value: 5 ether}(key, {-887220, 887220, 1e15, 0}) -> succeeds (MailHook.beforeAddLiquidity not consulted). 4) bob: PoolSwapTest.swap(key, {zeroForOne: true, amountSpecified: -1 ether, limit: MIN_SQRT_PRICE + 1}) receives MAIL, then sells all of it back on the same key. Expected per README: 4% of each ETH side credited to the hook (0.04 ether on the buy plus 4% of the sell output). Actual: hook.pendingProtocolFees(ETH) is still exactly 0.4 ether and feeRecipient receives nothing. Reproduced on this tree with test/scratch/HookJudge.t.sol::test_SecondPoolTradesWithoutTheFee (passes, i.e. the bypass works).

### 4. Info: ETH-specified dust swaps that yield nothing are accepted: a 1 wei exact-in buy through a generic router pays the 1 wei fee and receives 0 MAIL; a 1 wei exact-out sell pays an effective 50% fee

`p2e/contracts/src/MailHook.sol:271`

```
            if (exactIn ? poolQuote + fee != requested : poolQuote != requested + fee) revert PartialFill();
```

In beforeSwap the fee is rounded up (mulDivRoundingUp), so for an exact-in buy of amount <= 25 wei the fee is 1 wei and the pool receives amount - 1; for amount == 1 that is 0. v4's HookDeltaExceedsSwapAmount check only rejects a sign flip, so a zero amount reaches Pool.swap, whose loop exits at once with a zero delta. afterSwap then evaluates poolQuote + fee != requested as 0 + 1 != 1, which is false, so the full-fill guard passes, a Trade event with tokenAmount 0 is emitted, and the trader has paid 1 wei for nothing. A 1 wei exact-out sell has the same shape: fee = ceil(1 * 400 / 9600) = 1 wei, the seller gives 1,361,586 wei of MAIL (at the test price) and gets 1 wei of ETH, 50% rather than 4%. MailRouter is protected by its own out == 0 Slippage check, so only direct PoolManager callers or other routers are exposed, and the loss is bounded by the dust the caller chose to swap. If the hook is meant to be the single source of truth for 'every swap is a real trade', revert in the ETH-specified branch when tokenAmount == 0 (or when amount <= fee); otherwise document that ETH-specified swaps of 25 wei or less are all fee.

**Reproduction**

State: pool opened. Input 1: alice (EOA) calls PoolSwapTest(pm).swap{value: 1}(hook.poolKey(mail), SwapParams(zeroForOne: true, amountSpecified: -1, sqrtPriceLimitX96: MIN_SQRT_PRICE + 1), TestSettings(false, false), ''). Expected: revert, as MailRouter.buy would with Slippage, since nothing was bought. Actual: the swap succeeds, alice's ETH balance falls by 1 wei, hook.pendingProtocolFees(address(0)) rises by exactly 1, and alice's MAIL balance does not change. Input 2, after one 1 ether buy: SwapParams(zeroForOne: false, amountSpecified: 1, sqrtPriceLimitX96: MAX_SQRT_PRICE - 1) -> fee charged 1 wei, MAIL in 1,361,586 wei, ETH out 1 wei. Both measured on this tree with test/scratch/HookJudge.t.sol::test_OneWeiBuyPaysFeeGetsNothing and test_OneWeiExactOutSellCharges50Percent (both pass, logging fee 1, mail in 1361586, eth out 1).

### 5. Info: Trust assumption: 'the validator can be replaced but never removed' is only a code-size check; a permissive validator removes royalty enforcement and a reverting one freezes every holder

`p2e/contracts/src/MessengerNFT.sol:348`

```
        if (validator.code.length == 0) revert NotAContract();
```

The only constraint on setTransferValidator is that the target has code. Every wallet-to-wallet _update (lines 356-358) calls validateTransfer on whatever contract that is. A contract whose validateTransfer is a no-op makes the 'ENFORCED' 5% royalty unenforced on every marketplace, which is functionally the removal that the comment at line 342 and AUDIT.md guarantee 14 say is impossible. A contract that always reverts blocks every transfer of every Messenger, holders included, which together with the office lock lets the owner freeze the whole collection in place; AUDIT.md says 'holders can always move their own'. The 5% rate itself stays fixed, as stated. Only the owner can do either, so this is a trust assumption the admin table should state explicitly ('replace the transfer validator' currently reads as a neutral maintenance power). If the requester wants it enforced in code rather than by trust, restrict replacement to a known registry list or route setTransferValidator through a timelock so holders can see a change coming; either changes the agreed ownership model and is the requester's call.

**Reproduction**

State: Messenger #1 owned by alice; alice has approved operator market. market.transferFrom(alice, bob, 1) -> reverts DevTransferValidator.UnauthorizedTransfer, as intended. Owner: setTransferValidator(AllowAll) where AllowAll.validateTransfer is an empty pure function -> accepted (code.length != 0). market.transferFrom(alice, bob, 1) -> succeeds, ownerOf(1) == bob, no royalty check ran. Owner: setTransferValidator(DenyAll) where validateTransfer always reverts -> accepted. bob.transferFrom(bob, alice, 1) -> reverts DenyAll.Nope: the holder cannot move their own token. Expected per AUDIT.md: enforcement 'can be replaced but never removed' and holders can always move their own. Actual: both are at the owner's discretion. Reproduced on this tree with test/scratch/GameJudge.t.sol::test_PermissiveValidatorRemovesRoyaltyEnforcement (passes).

### 6. Info: Trust assumption: pause + revokeRoot lets the owner void any posted day at any time; the 24-hour revoke window is a lower bound, not an upper bound

`p2e/contracts/src/DeliveryRewards.sol:145`

```
        if (days_[day].claimed != 0) revert AlreadyClaimedFrom();
```

revokeRoot is gated only on 'nobody has claimed yet' and has no time bound; pause() stops every claim path (claim, claimNow and the batch variants run whenNotPaused) but not revokeRoot. Together, the owner can pause at any point, which guarantees claimed stays 0 for every day whose claims have not yet started, then revoke those days (including days long past claimableFrom and maturesAt), unpause, and the players' proven allocations for those days are gone with no on-chain recourse; totalPosted is reduced so the budget can be re-posted differently by the poster. AUDIT.md frames revoke as a protection against a bad root ('at least 24 hours after it was posted') and pause as an emergency stop, but does not state that the combination gives the owner a discretionary veto over any unclaimed day, and the admin table's 'Can't: revoke a day once claimed' is only as strong as players' ability to claim, which the same owner controls. No unprivileged actor can trigger this, so it is a trust assumption to document rather than a defect in a guard. If a code bound is wanted: refuse revokeRoot for a day once block.timestamp >= claimableFrom(day) unless the contract was paused before claimableFrom(day), or simply require revokes before claimableFrom(day); both trade away revoking a bad root discovered late, which is a scope decision.

**Reproduction**

State: day 0 closed; poster posts root R for day 0 with total 100e18 (alice's single leaf). Owner: pause() before postedAt + dayLength. Warp 30 days (past claimableFrom(0) and maturesAt(0)). Anyone: claim(alice, 0, 100e18, proof) -> reverts Pausable.EnforcedPause. Owner: revokeRoot(0) -> succeeds (claimed == 0), totalPosted == 0, days_[0] deleted. Owner: unpause(). claim(alice, 0, 100e18, proof) -> reverts NoRoot. Expected per AUDIT.md: a posted day is revocable in the window before claims and never once players are owed. Actual: any day is revocable at any time as long as the owner pauses first. Reproduced on this tree with test/scratch/GameJudge.t.sol::test_PauseThenRevokeAnyDay (passes).

### 7. Info: A seller can stamp a Messenger's play day with assign+unassign in the sale block, so the buyer cannot assign it until the next reward day

`p2e/contracts/src/MailOffice.sol:175`

```
        messengers.setLocked(id, false, msg.sender, clock.currentDay());
```

Both assign and unassign write lastPlayedDay = day + 1 and lastPlayer = msg.sender on the NFT (MessengerNFT.setLocked lines 246-247), and assign for any other wallet is refused for the rest of that reward day (MailOffice line 161, MessengerNFT line 239). That is the intended one-wallet-per-reward-day rule (re-check 5ccf142c finding 1). The consequence is that a seller, in the same block as or just before a marketplace sale settles, can call assign(id) then unassign() at no cost beyond gas: the sale still goes through (the token is unlocked again), but the buyer's assign reverts TooSoon until the next reward day, and nothing on-chain lets the buyer tell at purchase time, since the stamp can be placed after the listing was read. A buyer loses at most one reward day of the Messenger's stamina (12+ paid deliveries); the seller gains nothing, so this is a griefing edge of the accepted design. If it matters, clear lastPlayedDay/lastPlayer in _update on an ownership change only when the previous holder never actually played that day (an 'assigned this day' flag set by assign and cleared by the next assign), or document that a Messenger bought the day it was unassigned plays from the next reward day.

**Reproduction**

State: P2E.t.sol-style setUp; alice owns id 1 and has an office; bob has an office; day D = rewards.currentDay(). Input: alice calls office.assign(1) then office.unassign() (same block), then nft.transferFrom(alice, bob, 1); bob calls office.assign(1). Expected from the buyer's point of view: bob, owner of an unlocked Messenger that no other wallet is using, can assign it. Actual: bob's assign reverts MailOffice.TooSoon (nft.lastPlayedDay(1) == D + 1 and nft.lastPlayer(1) == alice); after vm.warp(+1 day) the same call succeeds. The existing test test_F3_OneMessengerOneWalletPerRewardDay covers only the case where alice really played. Reproduced on this tree with test/scratch/GameJudge.t.sol::test_SellerStampBlocksBuyerForTheDay (passes).

### 8. Info: setOffice is the one trust-critical setter that accepts address(0) and non-contracts; a zero office makes assign and levelUp revert for every player until it is set again

`p2e/contracts/src/MessengerNFT.sol:226`

```
        office = office_;
```

Every other privileged pointer in the system is validated: setTransferValidator requires code (NotAContract), the treasury setters and setPoster reject address(0), and the MailOffice and Wardrobe constructors reject zero. setOffice takes any value. The office is the only caller allowed into setLocked(.., true, ..) and raiseLevel, so with office == address(0) (or a typo address) MailOffice.assign and MailOffice.levelUp revert NotOffice for all wallets, while unassign keeps working through lockedBy. The owner can repair it with another setOffice, and AUDIT.md already treats the office as trusted, so this is an asymmetry in input validation rather than a bypass. Fix: if (office_.code.length == 0) revert NotAContract(); in setOffice, matching _setValidator (zero fails that check too); if an intentional 'no office' state is wanted, document it instead.

**Reproduction**

State: P2E.t.sol-style setUp (office linked, alice owns ids 1 and 2 and has opened an office). Input: owner calls nft.setOffice(address(0)); alice calls office.assign(1). Expected: a setter on a trusted pointer rejects the zero address like setTreasury, setPoster and setTransferValidator do. Actual: setOffice succeeds, nft.office() reads 0, and assign reverts MessengerNFT.NotOffice (setLocked line 237: msg.sender != office) until the owner calls setOffice again; office.levelUp hits the same check in raiseLevel (line 253). Reproduced on this tree with test/scratch/GameJudge.t.sol::test_SetOfficeZeroBricksAssign (passes).

---

Judge's submission `2970a2ac628d492b442d2d6f5a98c91d5086558cb30dac0be5e9dc73db8d8527`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
