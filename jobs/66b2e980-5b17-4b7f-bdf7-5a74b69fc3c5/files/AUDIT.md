# Audit report

> Audit the contracts in 0xtenang/Runner as they are.

| | |
|---|---|
| Repository | https://github.com/0xtenang/Runner.git |
| Commit | `cca0b03d5ebfc06936adb283b2238d1588596e85` |
| Job | `66b2e980-5b17-4b7f-bdf7-5a74b69fc3c5` |
| Judged | 2026-10-24 04:29 UTC |
| Findings | 1 medium · 4 low · 2 info |

Four agents audited the code as it is at `cca0b03`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Medium: addPair/_exclude shrinks past days' share totals after payouts: a pool that already claimed makes other holders' claims revert and permanently bricks sweepExpired

`contracts/RunnerToken.sol:597`

```
            if (!past.started) continue;
```

Merged from audit_math, audit_economics and audit_flow (same root cause, same line) and audit_permissions' payout-asymmetry report (same mechanism, secondary consequence). _exclude, reached only from addPair, subtracts the newly registered account's eligible weight from _days[d].shares for each still-claimable day d (today-7..today-1). It does not check holderClaimedDay[account][d]. If the account already claimed day d, its slice was paid at the old denominator and _days[d].paidOut already contains it, but the remaining holders are now priced at a smaller denominator, so day d's payouts sum to rewards_d * (1 + w/shares_new) > rewards_d. The comment above _exclude and AUDIT.md item 2 ('claims already paid can never exceed a day's tax') hold only when the excluded account never claimed. Consequences, all reproduced with Foundry: (a) when no other day's unclaimed tax sits in the bucket, the last honest claimer's `holderRewardsHeld -= total` (line 237) underflows and claimHolderRewards reverts with panic 0x11; because the loop always visits day d while it is in the 7-day window, that holder cannot claim ANY holder rewards until day d expires, after which the unpaid rest is swept to the protocol wallet; (b) when another day's unclaimed tax covers the excess, the overpayment is silently taken from that day's holders and _days[d].paidOut ends above _days[d].rewards; from then on sweepExpired reverts at line 250 (`uint256(day.rewards) - day.paidOut` underflows) as soon as nextSweepDay reaches d, and since nextSweepDay only advances through d, no later expired day can ever be swept: every future unclaimed holder tax is stuck in the contract forever; (c) even when the registered pool never claimed, late claimers of day d are paid rewards*bal/S_new while earlier claimers of the same day with the same balance were paid rewards*bal/S_old, so identical holders are paid different amounts depending on whether they claimed before or after the owner's addPair (2.7% difference in the reproduction). Preconditions: the owner registers (addPair) a contract that answers token0()/token1() with RUNNER, that held >= 300,000 RUNNER through a full UTC day inside the 7-day window on which holder tax was collected; for (a)/(b) that contract must also have called claimHolderRewards before registration (a plain Uniswap V2 pair cannot, but any pool/vault/wrapper contract with an arbitrary-call or harvest path can, and the README tells the owner to add liquidity first and register afterwards). The owner acts within intended operation; the unprivileged amplifier is the pool's own claim. Fix (minimal, keeps the IMD #2 behaviour for the normal case): in the _exclude loop skip days the account already claimed: `if (!past.started || holderClaimedDay[account][d]) continue;`. Verified: all three specialist proofs and my scratch tests (claim revert, paidOut > rewards, sweep brick) pass with this one-line change. It does not remove consequence (c); if the requester also wants that, freeze a day's denominator once anyone has been paid from it (`if (!past.started || past.paidOut > 0) continue;`), accepting that the pool's slice of such days goes to the protocol through sweepExpired instead of to holders, or document that addPair must be called the same UTC day a pool first receives RUNNER.

**Reproduction**

Foundry (forge 1.8.3, solc 0.8.24), tests under test/scratch and the attached proof. Case (a), attached proof: deploy at 00:00 UTC of day D0 with owner 0xA, liquidity 0xB, team 0xC. 0xB sends 1,000,000 to H and 1,000,000 to P (a contract whose token0() is the token and which can call claimHolderRewards), the rest of liquidity and all of team to pool X; owner addPair(X). Day D1: X transfers 5,000,000 to a buyer -> dayInfo(D1) = shares 2,000,000e18, rewards 100,000e18. Day D2: P.claim() receives 50,000e18. Owner addPair(P) -> dayInfo(D1).shares becomes 1,000,000e18. H calls claimHolderRewards: expected 50,000e18 paid and D1 total <= 100,000e18; actual revert panic 0x11 (holderRewardsHeld is 50,000e18, code subtracts 100,000e18). Test output: `[FAIL: panic: arithmetic underflow or overflow (0x11)] test_holderCanStillClaimAfterPoolRegisteredLate()`; with the one-line fix: PASS. Case (b), test_sweepBricksWhenDayOverpaid: deploy day 20000 (L, T 100M each, owner = test); addPair(Q); L->P 50M, T->H1 90M, L->Q 10M (day 20000 tax 200,000, shares L 40M + T 10M). Day 20001: L->Q 1M (tax 20,000, shares 189M). Day 20002: P.harvest() takes 20,000*50/189 = 5,291; owner addPair(P) -> day 20001 shares 139M; L claims (day 20000 160,000 + day 20001 20,000*39/139 = 5,611), H1 claims 20,000*90/139 = 12,949 (succeeds because T's unclaimed day-20000 slice covers it). dayInfo(20001) = shares 139,000,000e18, rewards 20,000e18, paidOut 23,852.156e18 > rewards. Day 20010: sweepExpired(20) -> `[Revert] panic: arithmetic underflow or overflow (0x11)` at RunnerToken.sweepExpired; nextSweepDay stays at 20001 forever. Expected: sweep passes day 20001 and later days are swept. With the fix: PASS. Case (c), test_asymmetricPayout: alice and bob each hold 1,000,000 all of day 20001 (200,000 tax, shares 190M incl. unregistered pool P 5M). Day 20002: alice claims 1,052.631e18; owner addPair(P); bob claims 1,081.081e18. Expected equal; actual bob gets 2.7% more.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.24;

import "forge-std/Test.sol";
import "contracts/RunnerToken.sol";

/// A contract that passes addPair's pool check (token0() == RUNNER) and can also call
/// claimHolderRewards before it is registered.
contract ClaimingPool {
    address public token0;
    address public token1;
    constructor(address t) { token0 = t; token1 = address(0xdead); }
    function claim(RunnerToken t) external { t.claimHolderRewards(); }
}

/// A plain pool used only to generate taxed trades.
contract TaxPool {
    address public token0;
    address public token1;
    constructor(address t) { token0 = t; token1 = address(0xdead); }
}

/// Fails on the current code: registering a pool that already claimed a day's holder reward
/// removes its weight from that day's share total, so the remaining holders' slices add up to
/// more than the day's tax and the last honest claimer reverts with an arithmetic underflow.
/// Passes once _exclude leaves the share total of days the account already claimed untouched.
contract ExcludeAfterClaimTest is Test {
    RunnerToken t;
    ClaimingPool P;
    TaxPool X;
    address owner = address(0xA);
    address liq = address(0xB);
    address team = address(0xC);
    address H = address(0x111);

    function setUp() public {
        vm.warp(1_800_000_000 - (1_800_000_000 % 1 days)); // 00:00 UTC of day D0
        t = new RunnerToken(owner, liq, team);
        X = new TaxPool(address(t));
        P = new ClaimingPool(address(t));
        vm.startPrank(liq);
        t.transfer(H, 1_000_000 ether);
        t.transfer(address(P), 1_000_000 ether);
        t.transfer(address(X), t.balanceOf(liq)); // the rest of the liquidity allocation into the pool
        vm.stopPrank();
        uint256 tb = t.balanceOf(team);
        vm.prank(team);
        t.transfer(address(X), tb);               // team wallet out of the picture as well
        vm.prank(owner);
        t.addPair(address(X));
    }

    function test_holderCanStillClaimAfterPoolRegisteredLate() public {
        uint256 d0 = block.timestamp / 1 days;
        uint256 d1 = d0 + 1;
        vm.warp(d1 * 1 days + 1);                 // day D1: H and P each held 1,000,000 all day
        vm.prank(address(X));
        t.transfer(address(0x999), 5_000_000 ether); // one 5M buy -> 100,000 holder tax on D1
        (uint256 sharesBefore, uint256 rewards,) = t.dayInfo(d1);
        assertEq(sharesBefore, 2_000_000 ether);
        assertEq(rewards, 100_000 ether);

        vm.warp((d0 + 2) * 1 days + 1);           // day D2: D1 is claimable
        uint256 pBefore = t.balanceOf(address(P));
        P.claim(t);                                // P takes 50,000 (1M / 2M of 100,000)
        uint256 pGot = t.balanceOf(address(P)) - pBefore;
        assertEq(pGot, 50_000 ether);

        vm.prank(owner);
        t.addPair(address(P));                    // owner registers P after it already claimed D1

        // Expected: H's slice of D1 stays 50,000 and is payable.
        // Actual (current code): D1 shares drop to 1,000,000, H is owed 100,000, and the claim
        // reverts because holderRewardsHeld (50,000) underflows.
        uint256 hBefore = t.balanceOf(H);
        vm.prank(H);
        t.claimHolderRewards();
        uint256 hGot = t.balanceOf(H) - hBefore;
        assertLe(pGot + hGot, rewards, "D1 paid out more than D1 collected");
        assertEq(hGot, 50_000 ether);
    }
}
```

### 2. Low: claimable() ignores emission start, pause, daily cap, signer and pool balance, so the view promises amounts claim() rejects

`contracts/RunnerToken.sol:300`

```
        return totalEarned > done ? totalEarned - done : 0;
```

Merged from audit_economics (info) and audit_flow (low). The view is documented as 'How much account can claim with a server signature for totalEarned' but returns the raw delta totalEarned - claimed[account]. claim() with the same inputs additionally requires !claimsPaused, emissionStartDay != 0, a non-zero matching signer, claimedOnDay[today] + amount <= emissionOn(today) and rewardsRemaining() >= amount. Every other view (holderClaimable, emissionToday, locksOf, rewardsRemaining) matches its write path; this one does not, so a front end or integrator that gates submission on it sends transactions that revert with EmissionNotStarted, ClaimsPaused, DailyCapReached or PoolEmpty. No funds at risk. Fix: return 0 when emission has not started, claims are paused or signer is zero, and cap the delta by emissionOn(today) - claimedOnDay[today] and by rewardsRemaining(); or rename/document it as the raw unclaimed difference.

**Reproduction**

Foundry test test_claimableIgnoresChecks (test/scratch/Leads.t.sol) passes on current code, i.e. the divergence is real: right after deployment (emissionStartDay == 0) claimable(alice, 100e18) returns 100e18 while claim() for alice reverts EmissionNotStarted before the signature check. After setSigner, startEmission and setClaimsPaused(true): claimable(alice, 1e18) returns 1e18 while claim reverts ClaimsPaused. With emission started on the launch schedule (10,000,000e18/day), claimable(alice, 30_000_000e18) returns 30,000,000e18 while a correctly signed claim reverts DailyCapReached. Expected: 0 or the amount payable now; actual: the full delta.

### 3. Low: A proposed ownership transfer cannot be cancelled; a mistaken pendingOwner keeps the right to take over indefinitely (token and NFT)

`contracts/RunnerToken.sol:482`

```
        if (newOwner == address(0)) revert ZeroAddress();
```

From audit_permissions, reproduced. transferOwnership is the only writer of pendingOwner besides acceptOwnership and it rejects address(0), so there is no way to withdraw a proposal. Once transferOwnership(X) is sent, X can call acceptOwnership at any later time until the owner overwrites the slot with another non-zero address. The two-step design protects against an address nobody controls but not against proposing an address someone else controls (wrong multisig, former team member, a key found compromised after the proposal). The only workaround, transferOwnership(owner) to overwrite the slot, is undocumented. The identical code is in RunnerGenesis.transferOwnership (contracts/RunnerGenesis.sol line 302). Fix: allow transferOwnership(address(0)) to clear pendingOwner (emit OwnershipTransferStarted(owner, address(0))) or add cancelOwnershipTransfer(); acceptOwnership already cannot be called by address(0).

**Reproduction**

Foundry test test_pendingOwnerCannotBeCleared (test/scratch/Leads.t.sol) passes on current code, confirming the behaviour: owner calls transferOwnership(0xA1); owner calls transferOwnership(address(0)) -> reverts ZeroAddress(); pendingOwner() still returns 0xA1; vm.warp(+365 days); 0xA1 calls acceptOwnership() -> succeeds, owner() == 0xA1. Expected: the current owner can withdraw a pending proposal; actual: the proposal stays live until accepted or overwritten.

### 4. Low: setProtocolWallet accepts the token's own address, turning the protocol tax and expired holder rewards into run rewards without any tokens leaving

`contracts/RunnerToken.sol:438`

```
        if (wallet == address(0)) revert ZeroAddress();
```

From audit_flow, reproduced. Only address(0) is rejected. With protocolWallet == address(this): (1) in _transfer, _move(from, protocolWallet, protocolCut) credits the 2% protocol cut to the token contract; balanceOf[address(this)] grows while holderRewardsHeld and totalLocked do not, so rewardsRemaining() grows and the protocol's income becomes claimable through signer-signed claim(); (2) in sweepExpired, _move(address(this), protocolWallet, total) is a self-transfer that returns early after emitting Transfer, while holderRewardsHeld -= total (line 260) and day.paidOut = day.rewards (line 252) still run, so expired holder rewards are marked paid and released into the run-reward pool instead of reaching a wallet. Owner misconfiguration, but silent and irreversible for the swept amounts. Fix: `if (wallet == address(0) || wallet == address(this)) revert ZeroAddress();` (or a dedicated error).

**Reproduction**

Foundry test test_protocolWalletSelf (test/scratch/Leads.t.sol) passes on current code, confirming: deploy day 20000, register pool Q, owner setProtocolWallet(address(token)). L transfers 10,000e18 to Q: rewardsRemaining() rises by exactly 200e18 (the protocol cut) and holderRewardsHeld is 200e18. Warp to day 20009 and call sweepExpired(10): holderRewardsHeld becomes 0, token.balanceOf(address(token)) is unchanged, rewardsRemaining() is now 400e18 above its starting value. Expected: 200e18 protocol cut and 200e18 expired holder tax reach the protocol wallet and the contract balance falls with holderRewardsHeld; actual: nothing leaves and both amounts become run rewards.

### 5. Low: setTreasury (and setRoyaltyReceiver) accept the NFT contract's own address; treasury == address(this) bricks every mint and withdraw

`contracts/RunnerGenesis.sol:272`

```
        if (newTreasury == address(0)) revert ZeroAddress();
```

From audit_flow, reproduced. Only address(0) is rejected. RunnerGenesis has no receive or fallback function, so with treasury == address(this) the `treasury.call{value: msg.value}("")` in mint (line 144) fails and every mint reverts PaymentFailed after _mint and _checkReceiver have run; withdraw() fails the same way, so stray ETH stays stuck until the owner sets another treasury. setRoyaltyReceiver has the same gap: a royalty receiver equal to the contract cannot accept royalty payments from marketplaces that send ETH. Owner misconfiguration, recoverable by the owner, but it halts the sale. Fix: reject newTreasury == address(this) in setTreasury and newReceiver == address(this) in setRoyaltyReceiver.

**Reproduction**

Foundry test test_genesisTreasurySelf (test/scratch/Leads.t.sol) passes on current code, confirming: deploy RunnerGenesis(owner = test, treasury = test, royaltyReceiver = test, 'u/', 'c'); owner calls setTreasury(payable(address(genesis))); alice (funded 1 ether) calls mint{value: priceOf(1)}(1) -> reverts PaymentFailed, no token minted. After setTreasury back to a payable EOA the same mint succeeds. Expected: a configured treasury receives the price and the token is minted; actual: all mints revert while this state holds.

### 6. Info: Trust assumption: the token owner key can redirect the run-reward pool to itself at up to 20,000,000 RUNNER per UTC day from the next day, pause claims, redirect protocol income, and tax any pool-shap

`contracts/RunnerToken.sol:444`

```
    function setSigner(address newSigner) external onlyOwner {
```

From audit_permissions; documented owner power, reported separately as the methodology requires, not a permission bypass. setSigner has no delay and no zero/EOA check, setEmissionSchedule takes effect the next UTC day up to MAX_DAILY_EMISSION, and claim accepts any signature from the current signer up to emissionOn(today). A compromised owner key therefore drains the pool at 20M/day (2.5% of 800M per day, the whole pool in 40 days) with no on-chain brake other than another owner action. The same key can setProtocolWallet (immediate redirect of the 2% protocol tax and of every future sweepExpired), setClaimsPaused(true) (blocks claim(), including the matured-lock release inside it; release() remains available) and addPair (irreversible 4% tax and loss of holder rewards for any contract that reports RUNNER as token0/token1). The contract header and AUDIT.md item 8 state this and recommend a multisig; at the pinned commit the constructor makes owner and protocolWallet the same address (lines 166-167). If the requester wants an on-chain bound rather than key custody: a one-day delay on setSigner taking effect, or capping setEmissionSchedule increases relative to the current schedule.

**Reproduction**

Code reading of lines 444-447, 466-477, 308-345: owner (or holder of a stolen owner key) calls setEmissionSchedule(20_000_000e18, 7, 20_000_000e18) and setSigner(attackerSigner) on day D; emissionOn(D+1) == 20_000_000e18. On day D+1 the attacker signs Claim(attacker, 20_000_000e18, deadline, false) with attackerSigner and calls claim(): all checks pass, totalLocked becomes 20_000_000e18, and 20M RUNNER are paid out 7 days later; repeated daily. Expected per the design: at most the day's emission leaves the pool; actual matches the design. Reported as a trust assumption.

### 7. Info: Trust assumption: the NFT owner can freeze every transfer by pointing the validator at an address without code, and can halt minting through the treasury address

`contracts/RunnerGenesis.sol:233`

```
        if (validator != address(0)) ITransferValidator(validator).validateTransfer(msg.sender, from, to, tokenId);
```

From audit_permissions; documented owner powers, reported separately. setTransferValidator has no code-size check: pointing it at an EOA or a reverting contract makes every transferFrom/safeTransferFrom revert until the owner changes it (the validator runs before the ownership check, which is the correct order for the ERC-721C re-entrancy concern). setTreasury has only a zero check, so a treasury that rejects ETH halts the sale (see the separate low finding for the self-address case). Neither is a bypass; both are the intended owner surface listed in AUDIT.md. They matter because at the pinned commit owner, treasury and royaltyReceiver are all the same wallet. The un-cancellable ownership proposal reported for the token applies here too (line 302).

**Reproduction**

Foundry test test_genesisTreasurySelf (test/scratch/Leads.t.sol) passes on current code, confirming the validator part: alice mints token 1; owner calls setTransferValidator(0x000000000000000000000000000000000000dEaD) (no code); alice calls transferFrom(alice, bob, 1) -> reverts (high-level call to an address without code fails extcodesize check), so every transfer and marketplace sale fails until the owner calls setTransferValidator(address(0)). Expected: owner powers behave as documented; actual matches. Reported as a trust assumption.

---

Judge's submission `24d0fa9c9fcea668a1f4d4c1dcd51475f1c25b94c5b2e8b6e02b79fb26e8403d`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
