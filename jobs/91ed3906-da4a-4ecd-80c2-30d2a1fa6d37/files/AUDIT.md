# Audit report

> MSFT95Vault v2: custody vault for a Stake-style crypto casino on Robinhood Chain (Arbitrum Orbit, single sequencer). Players deposit ETH or ERC-20s (MSFT95, USDC, NET, IMD), play off-chain against a backend ledger, and withdraw with EIP-712 vouchers the backend signs. Large withdrawals need a second COSIGNER signature. Per-token limits (maxWithdrawal, dailyCap, cosignAbove) cap losses if a signing key is stolen.
>
> Audit ONLY the MSFT95Vault.sol inside the msft95-casino folder (v2). Ignore any older msft95-vault folder (v1). v2 fixes all 9 findings from audit job d4fc488d; AUDIT-RESPONSE.md (same folder) maps each finding to its fix and test, and AUDIT.md is the updated brief with trust model and invariants. Tests: npm install --legacy-peer-deps && npx hardhat test (43 tests).
>
> Look hardest at:
> 1. Fund theft or double payout: can any voucher pay twice, pay someone other than w.user, pay after deadline, or pay without the required signer/cosigner signatures? Check _verify ordering, role revocation and re-grant, and malformed or high-s signatures.
> 2. The new voucher-time rules: issuedAt and deadline (deadline <= issuedAt + 24h, issuedAt <= block.timestamp + 5 min skew, block.timestamp >= deadline is expired) and voidVouchersIssuedBefore. Can a voucher outlive 24h from signing? Can the guardian, or anyone, brick withdrawals forever?
> 3. Outflow limits: can player withdrawals plus sweeps exceed dailyCap per window (beyond the documented 2x across a boundary)? Check the cast to uint192, rollover at exactly start + 1 day, and the NO_COSIGN sentinel versus the cosignAbove < maxWithdrawal rule.
> 4. Access control after the fixes: fundBankroll restricted to admin or BANKROLL_ROLE; sweep blocked while withdrawals are paused; GUARDIAN can only pause and void; only admin unpauses. Does the _grantRole override (SIGNER, COSIGNER and GUARDIAN must be three different keys) break AccessControlDefaultAdminRules admin handover, or let a role escape the rule?
> 5. The new Setup constructor: can it be deployed in a dangerous state (zero admin, inconsistent token limits, overlapping keys)? Does it apply exactly the same validation as setToken?
> 6. Reentrancy and odd tokens: ERC-777-style hooks, fee-on-transfer, blocklisting tokens like USDC, ETH receivers that revert or re-enter.
> 7. Anything that would make the off-chain ledger disagree with the chain: events missing or wrong (Deposited, Withdrawn, HouseWithdrawal, BankrollFunded), or value moving without an event.

| | |
|---|---|
| Repository | https://github.com/DrTatum/MSFT95.git |
| Commit | `427291e7312aa504214bf6961b64e30cba505f16` |
| Job | `91ed3906-da4a-4ecd-80c2-30d2a1fa6d37` |
| Judged | 2026-10-12 13:32 UTC |
| Findings | 1 medium · 3 low · 1 info |

Four agents audited the code as it is at `427291e`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Medium: issuedAt is signer-chosen and only checked against the submission block: future-dated sleeper vouchers outlive 24h, survive voidVouchersIssuedBefore (which can never pass block.timestamp) and are revi

`msft95-casino/contracts/contracts/MSFT95Vault.sol:381`

```
        if (issuedBefore <= minIssuedAt || issuedBefore > block.timestamp) revert BadConfig();
```

withdraw() bounds a voucher's life to MAX_VOUCHER_LIFETIME after w.issuedAt (line 238) and refuses issuedAt more than MAX_CLOCK_SKEW ahead of the submission block (line 237). Nothing ties issuedAt to when the signature was actually produced: whoever holds the SIGNER key (plus COSIGNER for amounts above cosignAbove) picks it. A voucher signed at T with issuedAt = T + 30 days, deadline = T + 31 days is rejected (VoucherNotYetValid) until that day and then becomes payable for 24h. The documented kill switch cannot reach it: voidVouchersIssuedBefore refuses any issuedBefore > block.timestamp for every caller, including the admin, while the sleeper's issuedAt stays in the future until the day it fires. The same root cause gives the void a permanent 5-minute blind spot (a voucher with issuedAt = now + 5 min, allowed by line 237, survives voidVouchersIssuedBefore(now)) and lets an honest voucher live 24h + 5 min from real signing. This contradicts AUDIT.md invariant 3 ('no voucher can pay more than 24h after it was signed'), the natspec of voidVouchersIssuedBefore ('void every voucher signed before issuedBefore') and AUDIT-RESPONSE #2 ('re-granting a key can't revive old vouchers'). The suite's F2 test submits a future-dated voucher only immediately (VoucherNotYetValid) and never warps to its issuedAt. Preconditions: SIGNER signatures obtainable at some point (abused signing API in front of a KMS/HSM, insider, backup) and the key still, or again, holding SIGNER_ROLE when the chosen date arrives. The operator's documented fast response (guardian: pause + void(now)) therefore does not neutralise pre-signed vouchers; only revoking the key and never re-granting it does. Loss per token is still bounded by maxWithdrawal/cosignAbove/dailyCap per window, which is why this is medium, but one batch per future day drains up to dailyCap per day with no on-chain warning, weeks after the incident was 'closed'. Merged from four specialists (audit_permissions, audit_economics, audit_flow, audit_math) plus the two sub-notes on the 5-minute skew band and the 24h+5min lifetime, which share this root cause. Fix that keeps the design and the Withdrawal ABI: add uint256 public voucherEpoch to storage, mix it into the digest in hashWithdrawal (or a new typed-data field), and have voidVouchersIssuedBefore (or a new guardian/admin voidAllVouchers()) increment it so every outstanding voucher dies regardless of its claimed issuedAt; the backend reads the epoch when signing and re-issues. Alternatively let the admin (not the guardian) set minIssuedAt past block.timestamp. In either case reword invariant 3 to say what is actually enforced ('24h after the issuedAt it claims'). Verified: the attached proof (3 tests) fails on this code and passes with the epoch patch applied to a copy of the contract.

**Reproduction**

State: vault with ETH listed (maxWithdrawal 0.4 ETH, dailyCap 2 ETH, cosignAbove 0.1 ETH), SIGNER key S, GUARDIAN G, admin A, 50 ETH bankroll, T = block.timestamp. 1) S signs Withdrawal{user: attacker, token: ETH, amount: 0.1 ETH, nonce: 1, issuedAt: T + 30 days, deadline: T + 31 days}; withdraw() now reverts VoucherNotYetValid. 2) At T + 1h: G calls voidVouchersIssuedBefore(block.timestamp) (succeeds, minIssuedAt = T+1h); A calls voidVouchersIssuedBefore(T + 365 days): reverts BadConfig. 3) At T + 30 days anyone calls withdraw(w, [sigS]). Expected: revert (voucher signed before the void; 30 days after signing). Actual: all checks on lines 236-239 pass (T+30d < deadline; issuedAt == block.timestamp; deadline - issuedAt == 1 day; issuedAt >= minIssuedAt) and attacker receives 0.1 ETH. Variant: A revokes SIGNER from S at T+1h, G voids, A re-grants S at T+29d: the voucher pays at T+30d. Variant: voucher signed at T with issuedAt = T + 5 min; G voids at T+10s; the voucher pays at T + 5 min + 24h - 1s. Ran test/scratch/SleeperVoucher.t.sol with forge (OZ 5.1.0, solc 0.8.24): 3 failed on current code ('sleeper voucher paid 30 days after it was signed, after the void', 're-grant revived a voucher signed 30 days earlier', 'voucher inside the skew band paid after the void'); 3 passed on a copy with voucherEpoch mixed into hashWithdrawal and incremented by voidVouchersIssuedBefore. The three specialist proofs (Proof_ce3a71b5a9b9, Proof_83137df81cd9, Proof_d05ed22c1989) were also run and all fail on this code for the stated reason.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.24;

import "forge-std/Test.sol";
import {MSFT95Vault} from "msft95-casino/contracts/contracts/MSFT95Vault.sol";

/// Finding: `issuedAt` is chosen by whoever holds the SIGNER key and is only checked against the
/// submission block (`issuedAt <= block.timestamp + 5 min`). A voucher signed today with `issuedAt`
/// 30 days ahead is dormant for 30 days, survives `voidVouchersIssuedBefore(now)` (which cannot be
/// raised past `now`, by guardian or admin), survives a revoke + re-grant of the key, and then pays.
/// AUDIT.md invariant 3 ("no voucher can pay more than 24h after it was signed") and the documented
/// meaning of the void ("void every voucher signed before issuedBefore") do not hold.
///
/// Fails on the current code (the sleeper pays). Passes once a void makes every voucher signed
/// before it unpayable regardless of its self-declared issuedAt (e.g. a voucher epoch committed in
/// the signed digest and bumped by the void, or an admin-only void that may be set past `now`).
contract SleeperVoucherTest is Test {
    MSFT95Vault vault;
    uint256 signerPk = 0xA11CE;
    uint256 cosignerPk = 0xB0B;
    address signer = vm.addr(signerPk);
    address cosigner = vm.addr(cosignerPk);
    address guardian = address(0x6A);
    address admin = address(0xAD);
    address attacker = address(0xBAD);

    function setUp() public {
        vm.warp(1_800_000_000);
        MSFT95Vault.TokenSetup[] memory ts = new MSFT95Vault.TokenSetup[](1);
        ts[0] = MSFT95Vault.TokenSetup({
            token: address(0),
            config: MSFT95Vault.TokenConfig({listed: true, depositsEnabled: true, minDeposit: 1, maxWithdrawal: 0.4 ether, dailyCap: 2 ether, cosignAbove: 0.1 ether})
        });
        vault = new MSFT95Vault(MSFT95Vault.Setup({
            admin: admin, adminDelay: 0, signer: signer, cosigner: cosigner, guardian: guardian,
            bankroller: address(0), allowlistOnly: false, allowed: new address[](0), tokens: ts
        }));
        vm.deal(admin, 100 ether);
        vm.prank(admin);
        vault.fundBankroll{value: 50 ether}(address(0), 50 ether);
    }

    function _sign(uint256 pk, MSFT95Vault.Withdrawal memory w) internal view returns (bytes memory) {
        (uint8 v, bytes32 r, bytes32 s) = vm.sign(pk, vault.hashWithdrawal(w));
        return abi.encodePacked(r, s, v);
    }

    /// Signed at T with a (then) compromised key. At T+1h the operator voids as far as the contract
    /// allows (guardian: now; admin: also tries a far-future cut-off). The key stays in service
    /// (HSM key, only the signing API was abused). Expected: the voucher can never pay. Actual: pays at T+30d.
    function test_sleeperSurvivesVoid() public {
        uint256 T = block.timestamp;
        MSFT95Vault.Withdrawal memory w = MSFT95Vault.Withdrawal({
            user: attacker, token: address(0), amount: 0.1 ether, nonce: 1,
            issuedAt: T + 30 days, deadline: T + 31 days
        });
        bytes[] memory sigs = new bytes[](1);
        sigs[0] = _sign(signerPk, w);

        // not payable yet
        vm.expectRevert(MSFT95Vault.VoucherNotYetValid.selector);
        vault.withdraw(w, sigs);

        vm.warp(T + 1 hours);
        vm.prank(guardian);
        vault.voidVouchersIssuedBefore(block.timestamp);
        vm.prank(admin);
        try vault.voidVouchersIssuedBefore(T + 365 days) {} catch {}

        vm.warp(T + 30 days);
        uint256 before = attacker.balance;
        (bool paid,) = address(vault).call(abi.encodeCall(vault.withdraw, (w, sigs)));
        assertFalse(paid, "sleeper voucher paid 30 days after it was signed, after the void");
        assertEq(attacker.balance, before, "attacker received funds");
    }

    /// Same sleeper; the operator revokes the key, voids, and later re-grants the same key.
    /// AUDIT-RESPONSE #2: "re-granting a key can't revive old vouchers". Actual: it does.
    function test_sleeperRevivedByRegrant() public {
        uint256 T = block.timestamp;
        MSFT95Vault.Withdrawal memory w = MSFT95Vault.Withdrawal({
            user: attacker, token: address(0), amount: 0.1 ether, nonce: 2,
            issuedAt: T + 30 days, deadline: T + 31 days
        });
        bytes[] memory sigs = new bytes[](1);
        sigs[0] = _sign(signerPk, w);

        bytes32 SR = vault.SIGNER_ROLE();
        vm.warp(T + 1 hours);
        vm.prank(admin);
        vault.revokeRole(SR, signer);
        vm.prank(guardian);
        vault.voidVouchersIssuedBefore(block.timestamp);
        vm.prank(admin);
        try vault.voidVouchersIssuedBefore(T + 365 days) {} catch {}

        vm.warp(T + 29 days);
        vm.prank(admin);
        vault.grantRole(SR, signer); // key put back into service

        vm.warp(T + 30 days);
        uint256 before = attacker.balance;
        (bool paid,) = address(vault).call(abi.encodeCall(vault.withdraw, (w, sigs)));
        assertFalse(paid, "re-grant revived a voucher signed 30 days earlier");
        assertEq(attacker.balance, before, "attacker received funds");
    }

    /// The same root cause gives the void a permanent 5-minute blind spot: a voucher with
    /// issuedAt = now + MAX_CLOCK_SKEW (accepted by withdraw) survives voidVouchersIssuedBefore(now)
    /// and pays until 24h + 5 min after the void block.
    function test_skewBandSurvivesVoid() public {
        uint256 T = block.timestamp;
        MSFT95Vault.Withdrawal memory w = MSFT95Vault.Withdrawal({
            user: attacker, token: address(0), amount: 0.1 ether, nonce: 3,
            issuedAt: T + 5 minutes, deadline: T + 5 minutes + 1 days
        });
        bytes[] memory sigs = new bytes[](1);
        sigs[0] = _sign(signerPk, w);

        vm.warp(T + 10);
        vm.prank(guardian);
        vault.voidVouchersIssuedBefore(block.timestamp);
        vm.prank(admin);
        try vault.voidVouchersIssuedBefore(T + 365 days) {} catch {}

        vm.warp(T + 5 minutes + 1 days - 1);
        uint256 before = attacker.balance;
        (bool paid,) = address(vault).call(abi.encodeCall(vault.withdraw, (w, sigs)));
        assertFalse(paid, "voucher inside the skew band paid after the void");
        assertEq(attacker.balance, before, "attacker received funds");
    }
}
```

### 2. Low: Setup accepts any adminDelay: an oversized value makes admin handover and delay changes impossible or multi-year, and cannot be corrected afterwards

`msft95-casino/contracts/contracts/MSFT95Vault.sol:150`

```
        AccessControlDefaultAdminRules(s.adminDelay, s.admin)
```

The constructor validates the three role keys and every token config with the same _setToken rules as setToken, and OpenZeppelin rejects a zero admin, but s.adminDelay is passed straight through unchecked. AccessControlDefaultAdminRules 5.1.0 computes SafeCast.toUint48(block.timestamp) + delay in checked uint48 arithmetic in both _beginDefaultAdminTransfer (line 221 of the OZ file) and _changeDefaultAdminDelay (line 287), and when the delay is decreased the waiting period is currentDelay - newDelay. An absurd initial delay is therefore permanent: with type(uint48).max both beginDefaultAdminTransfer and changeDefaultAdminDelay revert on uint48 overflow forever; with a plausible unit mistake (2 days written in milliseconds = 172,800,000; deploy.js reads ADMIN_DELAY through Number() with no bound) a handover or a delay reduction waits about 5.5 years. The Safe stays admin, so funds are not at risk, but the documented ability to rotate the admin (README: 'Handing over admin later takes ADMIN_DELAY and must be accepted') is lost and the contract must be redeployed and migrated. Fix: bound it in the constructor like the token limits, e.g. if (s.adminDelay > 30 days) revert BadConfig(); and mirror the bound in deploy.js.

**Reproduction**

Deploy MSFT95Vault(Setup{admin: 0xAD, adminDelay: type(uint48).max, signer, cosigner, guardian, one ETH token}). Admin calls beginDefaultAdminTransfer(alice): expected a scheduled transfer; actual revert (Panic 0x11, uint48 overflow). Admin calls changeDefaultAdminDelay(0): actual revert for the same reason, so the state can never be corrected. With adminDelay = 172_800_000, changeDefaultAdminDelay(0) succeeds but pendingDefaultAdminDelay().schedule is 172,800,000 s (about 5.5 years) ahead. Both verified with forge against OZ 5.1.0 (test_maxAdminDelayBricksHandover, test_largeAdminDelayMs passed, i.e. the reverts and the 5.5-year schedule were observed). By contrast a token config with the same kind of mistake is rejected with BadConfig.

### 3. Low: setToken rejects the all-zero config, so a token cannot be unlisted by clearing it; the cosignAbove < maxWithdrawal rule is enforced even when listed == false

`msft95-casino/contracts/contracts/MSFT95Vault.sol:326`

```
        if (cfg.cosignAbove != NO_COSIGN && cfg.cosignAbove >= cfg.maxWithdrawal) revert BadConfig();
```

The trust model says the admin can 'list and unlist tokens'. The natural unlist call, setToken(token, TokenConfig(false, false, 0, 0, 0, 0)), reverts BadConfig because cosignAbove (0) >= maxWithdrawal (0) and the consistency checks do not consider cfg.listed. Unlisting only works with a non-zero maxWithdrawal/dailyCap left in storage, or with cosignAbove = NO_COSIGN, which leaves a stale opt-out sentinel that silently disables the cosigner if the token is later re-listed from the stored struct. Under time pressure (delisting a token found to be malicious) a Safe/timelock proposal with the zeroed struct fails and must be re-queued. Fix: skip the maxWithdrawal/cosignAbove consistency checks when cfg.listed is false (or accept an all-zero config), and consider deleting the struct on unlist.

**Reproduction**

Vault with ETH listed (test fixture config). Admin calls setToken(ETH, {listed: false, depositsEnabled: false, minDeposit: 0, maxWithdrawal: 0, dailyCap: 0, cosignAbove: 0}). Expected: ETH unlisted. Actual: revert MSFT95Vault.BadConfig. The same call with maxWithdrawal = 1, dailyCap = 1 succeeds (listed becomes false), showing the rejection is only the cosignAbove >= maxWithdrawal comparison on zeros. Verified with forge (test_zeroConfigUnlistReverts).

### 4. Low: scripts/sign-withdrawal.js still signs the v1 Withdrawal type (no issuedAt); every voucher it produces is rejected by the v2 vault with BadSignatures

`msft95-casino/contracts/scripts/sign-withdrawal.js:10`

```
const TYPES = { Withdrawal: [
  { name: "user", type: "address" }, { name: "token", type: "address" }, { name: "amount", type: "uint256" },
  { name: "nonce", type: "uint256" }, { name: "deadline", type: "uint256" } ] };
```

Outside the .sol scope but shipped in the same v2 folder and referenced by README ('Voucher signing example' and testnet step 4). The contract's WITHDRAWAL_TYPEHASH is Withdrawal(address user,address token,uint256 amount,uint256 nonce,uint256 issuedAt,uint256 deadline) and hashWithdrawal encodes six fields. The script's EIP-712 type omits issuedAt and the voucher JSON it prints has no issuedAt, so withdraw() cannot be called with it as-is, and if issuedAt is filled in by hand the digest differs from hashWithdrawal, ECDSA.recover yields an unrelated address, hasRole fails and withdraw reverts BadSignatures. test/helpers.js and backend/src/chain.ts carry the correct six-field type, which is why the suite does not notice. Merged from three specialists (audit_economics, audit_flow, audit_math). Fix: add { name: 'issuedAt', type: 'uint256' } before deadline, set issuedAt = now and deadline = issuedAt + TTL (TTL <= 86400), print issuedAt, or import the type from one shared module.

**Reproduction**

Sign Withdrawal{alice, ETH, 0.1 ether, nonce 1, deadline t+3600} with the SIGNER key over the five-field type string keccak256('Withdrawal(address user,address token,uint256 amount,uint256 nonce,uint256 deadline)') and the vault's domainSeparator(), then call withdraw({alice, ETH, 0.1 ether, 1, issuedAt: t, deadline: t+3600}, [sig]). Expected (per README): payout. Actual: revert BadSignatures. Verified with forge (test_v1TypeSignatureRejected) by hashing exactly the type the script uses against the deployed vault's domain separator.

### 5. Info: Trust assumption: a GUARDIAN key (or a stolen one) can irreversibly void every outstanding honest voucher, and the backend only re-credits those players after each voucher's deadline

`msft95-casino/contracts/contracts/MSFT95Vault.sol:379`

```
    function voidVouchersIssuedBefore(uint256 issuedBefore) external {
```

Unlike pauseWithdrawals(), which the admin can undo, raising minIssuedAt has no admin counterpart: nothing lowers it. One call with issuedBefore = block.timestamp from the monitoring bot's key invalidates every voucher already handed to players; those vouchers keep nonceUsed == false, and the backend refund rule (backend/src/withdrawals.ts expireWithdrawals, 'w.deadline < confirmed block timestamp') only re-credits a voucher once a confirmed block is strictly past its deadline, so affected players wait up to WITHDRAWAL_TTL (<= 24h) with their balance debited while the funds sit in the vault. Repeated calls each block amount to a withdrawal pause the admin can lift only by revoking the guardian (Safe + timelock). This is within the documented GUARDIAN powers and is reported as a trust assumption, not a bypass: the blast radius of a stolen guardian key is 'all pending withdrawals delayed up to 24h and the key must be revoked', not merely 'paused until admin unpauses'. If that is not intended, let the backend refund a voucher as soon as a confirmed block shows issuedAt < minIssuedAt (it is provably unpayable), which removes the 24h wait without touching the contract.

**Reproduction**

Signer signs W = {alice, ETH, 0.05 ether, nonce 1, issuedAt t, deadline t+3600}. Guardian calls voidVouchersIssuedBefore(t+1). withdraw(W, [sigS]) reverts VoucherVoided; nonceUsed(alice, 1) == false; the ABI has no function that lowers minIssuedAt (voidVouchersIssuedBefore reverts BadConfig for issuedBefore <= minIssuedAt). Backend query 'deadline < confirmedBlock.timestamp' is false until t+3600, so alice's balance stays debited until then. Contract behaviour verified with forge; backend rule read from withdrawals.ts lines 59-65.

---

Judge's submission `c7d3743d2f5928ee0f1440cffcc281ed1bc7be24e43292f8ad9fb24483735943`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
