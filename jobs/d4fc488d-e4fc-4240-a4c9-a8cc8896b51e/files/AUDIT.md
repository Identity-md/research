# Audit report

> # Audit brief: MSFT95Vault
>
> **Scope:** `contracts/MSFT95Vault.sol`. The mocks in `contracts/mocks/` are test-only.
>
> **Compiler and libraries:** Solidity 0.8.24, optimizer 500 runs, EVM target shanghai, OpenZeppelin Contracts 5.1.0.
>
> **Chain:** Robinhood Chain, an Arbitrum Orbit chain with a single sequencer. Testnet is 46630 and mainnet is 4663.
>
> ## Trust model
>
> - **Admin** is fully trusted. It is a Safe, plus a timelock on mainnet. It can:
>   - list and unlist tokens;
>   - change limits;
>   - grant SIGNER and COSIGNER;
>   - sweep funds, subject to `dailyCap`.
> - **SIGNER** is trusted to sign only withdrawals the off-chain ledger allows. A compromised SIGNER can take, per token per 24h window, up to `dailyCap`, in pieces no larger than `cosignAbove`. Anything above `cosignAbove` also needs COSIGNER.
> - **GUARDIAN** can only pause.
> - **Players** are untrusted.
>
> ## Invariants to check
>
> 1. A voucher pays at most once: `nonceUsed[user][nonce]` is set before the external transfer, and a reverted payout leaves it unset.
> 2. Funds from `withdraw` only ever go to `w.user`, whoever calls it.
> 3. A voucher is only valid on this chain and this vault, before its `deadline`, and at most 24h ahead of `block.timestamp`.
> 4. `amount > cosignAbove` requires two distinct keys, one with SIGNER and one with COSIGNER. One key can never hold both roles (`_grantRole` override). The same signature or key can't be counted twice.
> 5. Per token, within one window, player withdrawals plus `sweep` never exceed `dailyCap`. At most 2× `dailyCap` can leave inside any 24 hours, across a window boundary.
> 6. `Deposited.amount` equals the real balance increase. This holds for fee-on-transfer tokens; rebasing tokens are not supported.
> 7. Only an admin can unpause, change config, sweep, edit the allowlist or grant roles. A GUARDIAN can only pause.
> 8. Plain ETH sent to the vault reverts. ETH can only enter through `depositETH` or `fundBankroll`.
> 9. The token balance always equals deposits plus bankroll minus withdrawals minus sweeps. A randomized test covers this over 300 operations.
>
> ## Areas worth extra attention
>
> - `_verify`: signature-ordering edge cases, role revocation between signing and submission, and `ECDSA.recover` with malformed signatures.
> - `_spend`: window rollover at exactly `start + WINDOW`, and `uint192` / `uint64` casts.
> - Reentrancy through ERC-777-style hooks or ETH receivers. Every external entry point is `nonReentrant`, and `deposit` reads the balance before and after the transfer.
> - `AccessControlDefaultAdminRules` interaction with the `_grantRole` override, so admin handover still works.
> - Tokens with blocklists (USDC): a blocklisted user's withdrawal reverts. Confirm it fails cleanly and the nonce stays unused.
>
> ## Off-chain assumptions (for the step-2 backend review)
>
> - **Deposit indexing.** The indexer credits each `Deposited` event exactly once, keyed by `(chainId, txHash, logIndex)` or `depositId`, after enough confirmations. Reorgs are handled.
> - **Ledger before signing.** The ledger debits the player before signing a voucher. If the voucher expires unused, it re-credits only after `deadline` has passed and `nonceUsed` is confirmed false at a final block.
> - **Unique nonces.** Nonces are unique per user and never reused across voucher re-issues.
> - **Key custody.** SIGNER and COSIGNER keys live in separate KMS/HSM accounts. The GUARDIAN bot pauses withdrawals when reconciliation fails, that is, when the sum of ledger liabilities is greater than the vault balance.

| | |
|---|---|
| Repository | https://github.com/DrTatum/MSFT95.git |
| Commit | `984db98bba67daa1aef19e342002088d131f0e74` |
| Job | `d4fc488d-e4fc-4240-a4c9-a8cc8896b51e` |
| Judged | 2026-10-12 12:01 UTC |
| Findings | 2 low · 7 info |

Four agents audited the code as it is at `984db98`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Low: fundBankroll is permissionless and skips every inbound gate (allowlistOnly, depositsPaused, depositsEnabled), so uncredited value can enter from anyone while deposits are closed

`msft95-vault/contracts/MSFT95Vault.sol:138`

```
    function fundBankroll(address token, uint256 amount) external payable nonReentrant {
        if (!tokenConfig[token].listed) revert TokenNotListed(token);
```

deposit() and depositETH() go through _checkDeposit(), which enforces depositsPaused, TokenConfig.depositsEnabled and allowlistOnly/allowed[msg.sender]. fundBankroll() moves value into the same vault but checks only `listed`, has no role check, and emits BankrollFunded, which the indexer does not credit. Consequences: (1) the KYC allowlist (README: 'only listed wallets can deposit') and the GUARDIAN's pauseDeposits() brake cover only one of the two inbound paths; any wallet can still push ETH or any listed ERC-20 into custody while deposits are paused or the token has depositsEnabled=false. (2) A player who hits this selector by mistake (wrong UI button, wallet routing) loses the funds to house bankroll with no Deposited event and no on-chain claim, which is exactly the outcome receive() reverts to prevent. The function's NatSpec calls it 'house bankroll', while the Hardhat suite has alice call it successfully, so the intended caller set is ambiguous and must be decided. Access-control classification: public, unrestricted, state-changing (moves funds). Merged from audit_flow, audit_permissions and audit_economics (same function, same mechanism). Fix preserving the design: restrict fundBankroll to DEFAULT_ADMIN_ROLE or a dedicated BANKROLL_ROLE granted to the treasury wallet; if donations must stay open, at minimum apply the depositsPaused and allowlistOnly checks and document that this path is never credited.

**Reproduction**

State: admin calls setAllowlistOnly(true); guardian calls pauseDeposits(); stranger 0x5717 is not in `allowed`, holds 10e18 tok (approved) and 1 ether. Input: stranger calls deposit(tok, 10e18) -> reverts DepositsClosed (expected). stranger calls fundBankroll(tok, 10e18) -> expected: revert (same caller, same paused/non-allowlisted state); actual: succeeds, vault tok balance +10e18, stranger balance 0, BankrollFunded(stranger, tok, 10e18) emitted, no Deposited event. stranger calls fundBankroll{value: 1 ether}(address(0), 0) -> expected revert; actual: succeeds, vault ETH +1 ether. Same result with depositsEnabled=false on the token. Reproduced in Foundry (solc 0.8.24, OZ 5.1.0, evm shanghai): test_fundBankrollBypass passes on current code; the attached proof fails on current code and passes with an onlyRole(DEFAULT_ADMIN_ROLE) gate added to fundBankroll.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.24;

import {Test} from "forge-std/Test.sol";
import {MSFT95Vault} from "msft95-vault/contracts/MSFT95Vault.sol";
import {TestToken} from "msft95-vault/contracts/mocks/Mocks.sol";

/// fundBankroll() is callable by anyone and skips every inbound gate that deposit()/depositETH()
/// enforce (allowlistOnly, depositsPaused, depositsEnabled). A non-allowlisted wallet can push value
/// into the vault while the guardian has paused deposits, and gets no Deposited event, so the ledger
/// never credits it. This test fails on the current code and passes once fundBankroll is either
/// restricted to the house (admin / dedicated role) or made to honour the same gates as deposit().
contract FundBankrollGatesTest is Test {
    MSFT95Vault vault;
    TestToken tok;
    address admin = address(0xAD);
    address guardian = address(0x6A);
    address stranger = address(0x5717);
    address constant ETH = address(0);

    function setUp() public {
        vault = new MSFT95Vault(admin, 0);
        tok = new TestToken("T", "T", 18);
        MSFT95Vault.TokenConfig memory c = MSFT95Vault.TokenConfig({
            listed: true, depositsEnabled: true, minDeposit: 1, maxWithdrawal: 1000e18, dailyCap: 5000e18, cosignAbove: 100e18
        });
        vm.startPrank(admin);
        vault.grantRole(vault.GUARDIAN_ROLE(), guardian);
        vault.setToken(address(tok), c);
        vault.setToken(ETH, c);
        vault.setAllowlistOnly(true); // stranger is NOT allowlisted
        vm.stopPrank();
        vm.prank(guardian);
        vault.pauseDeposits(); // guardian brake on inflows
        tok.mint(stranger, 10e18);
        vm.deal(stranger, 1 ether);
        vm.prank(stranger);
        tok.approve(address(vault), type(uint256).max);
    }

    function test_strangerCannotPushTokensWhileDepositsPausedAndNotAllowlisted() public {
        // deposit() correctly refuses the stranger
        vm.prank(stranger);
        vm.expectRevert(MSFT95Vault.DepositsClosed.selector);
        vault.deposit(address(tok), 10e18);

        // fundBankroll() must refuse the same caller in the same state
        vm.prank(stranger);
        vm.expectRevert();
        vault.fundBankroll(address(tok), 10e18);
        assertEq(tok.balanceOf(address(vault)), 0, "tokens entered the vault through fundBankroll while deposits were paused");
    }

    function test_strangerCannotPushEthWhileDepositsPausedAndNotAllowlisted() public {
        vm.prank(stranger);
        vm.expectRevert(MSFT95Vault.DepositsClosed.selector);
        vault.depositETH{value: 1 ether}();

        vm.prank(stranger);
        vm.expectRevert();
        vault.fundBankroll{value: 1 ether}(ETH, 0);
        assertEq(address(vault).balance, 0, "ETH entered the vault through fundBankroll while deposits were paused");
    }
}
```

### 2. Low: MAX_VOUCHER_LIFETIME bounds the deadline relative to submission time, not signing time: a far-future voucher is a sleeper that activates in its last 24h

`msft95-vault/contracts/MSFT95Vault.sol:184`

```
        if (w.deadline > block.timestamp + MAX_VOUCHER_LIFETIME) revert VoucherTooLong();
```

The signed struct carries no issuance time, so the contract can only enforce that a voucher is not redeemed more than 24h before its deadline. It cannot enforce the README promise that every voucher 'expires within 24 hours at most' after it was signed. A voucher with deadline = now + 365 days is rejected with VoucherTooLong today and is accepted unchanged during the whole day [deadline - 1 day, deadline]. Invariant 3 as literally worded ('at most 24h ahead of block.timestamp') holds; the gap is between the documented lifetime and the mechanism. Practical consequences: a backend TTL bug or a briefly compromised SIGNER key can bank dormant vouchers that only become payable later; because the ledger re-credits only after `deadline`, the player's ledger debit stays locked for the whole period. Role revocation at submission (hasRole in _verify) is the only kill switch and does work, but re-granting the same key later revives every voucher it signed (confirmed). Merged from audit_math, audit_flow, audit_permissions and audit_economics. Fix options that keep the design: add an `issuedAt` field to the EIP-712 Withdrawal struct and require issuedAt <= block.timestamp && w.deadline <= issuedAt + MAX_VOUCHER_LIFETIME; or document that the 24h figure is a redemption horizon, enforce TTL in the signing service, and rotate (never re-grant) compromised keys.

**Reproduction**

State: signer holds SIGNER_ROLE, tok listed (maxWithdrawal 1000e18, cosignAbove 100e18), vault funded, T0 = block.timestamp. Input: Withdrawal{user: alice, token: tok, amount: 5e18, nonce: 1, deadline: T0 + 365 days} signed by signer. Submit at T0 -> reverts VoucherTooLong (expected). Warp to T0 + 364 days - 1 -> still VoucherTooLong. Warp to T0 + 364 days -> withdraw() succeeds and alice receives 5e18. Expected per README ('expires within 24 hours at most'): never payable 364 days after signing. Actual: paid. Reproduced in Foundry (test_sleeperVoucher). Also reproduced: revoking COSIGNER after signing makes [s, c] revert BadSignatures, and re-granting the role makes the same two signatures pay (test_sigEdges).

### 3. Info: fundBankroll ignores the `amount` argument on the ETH branch and silently records msg.value

`msft95-vault/contracts/MSFT95Vault.sol:142`

```
            received = msg.value;
```

For token == ETH the function never reads `amount`; it records and emits msg.value. The ERC-20 branch is stricter (rejects a stray msg.value), so a caller who passes the intended amount but attaches a different value gets a smaller or larger top-up with no error. The event reports what actually arrived, so no funds are mis-accounted; this is an input-validation asymmetry. Fix: on the ETH branch require amount == msg.value (or amount == 0), or document that `amount` is ignored for ETH.

**Reproduction**

State: ETH listed. Input: alice calls fundBankroll{value: 1 ether}(address(0), 999 ether). Expected by analogy with the ERC-20 branch's msg.value check: revert because amount and msg.value disagree. Actual: succeeds and emits BankrollFunded(alice, address(0), 1 ether). Reproduced in Foundry (test_fundBankrollEthIgnoresAmount, vm.expectEmit on the 1 ether value).

### 4. Info: Voucher deadline is inclusive: a voucher pays at block.timestamp == deadline, so the ledger must only re-credit when a final block has timestamp strictly greater than deadline

`msft95-vault/contracts/MSFT95Vault.sol:183`

```
        if (block.timestamp > w.deadline) revert VoucherExpired();
```

The expiry comparison is strict, so a block whose timestamp equals the deadline still pays the voucher, while AUDIT.md invariant 3 says 'before its deadline'. Harmless on-chain, but the step-2 backend's definition of 'deadline has passed' must be finalBlock.timestamp > deadline, not >=; a ledger that re-credits at timestamp == deadline while a withdraw() in that same block pays out would double-pay the player. Merged from audit_math and audit_flow. Fix: change the check to `>=` to match the wording, or document that the deadline second is itself valid.

**Reproduction**

State: tok listed, signer holds SIGNER_ROLE. Input: Withdrawal{alice, tok, 5e18, nonce 1, deadline T} with vm.warp(T), then withdraw(). Expected per the brief's literal wording: VoucherExpired. Actual: succeeds, alice receives 5e18. A second voucher (nonce 2, same deadline T) submitted at T + 1 reverts VoucherExpired. Reproduced in Foundry (test_deadlineInclusive).

### 5. Info: sweep is not stopped by withdrawalsPaused: the GUARDIAN's reconciliation pause does not cover house outflows (trust assumption to document or close)

`msft95-vault/contracts/MSFT95Vault.sol:272`

```
    function sweep(address token, address to, uint256 amount) external onlyRole(DEFAULT_ADMIN_ROLE) nonReentrant {
        if (!tokenConfig[token].listed) revert TokenNotListed(token);
```

withdraw() reverts WithdrawalsClosed while withdrawalsPaused is true; sweep() checks only `listed`, non-zero amount/to and the daily cap. The brief says the GUARDIAN bot pauses withdrawals when ledger liabilities exceed the vault balance, which is exactly when the house's own outflow (up to dailyCap per token per window, 2x across a boundary, ignoring maxWithdrawal and cosignAbove) worsens the shortfall for players. The admin is fully trusted and timelocked on mainnet, so this is a trust-assumption gap, not a bypass. Merged from audit_flow, audit_permissions and audit_economics. Fix if the pause is meant as a full outflow brake: add `if (withdrawalsPaused) revert WithdrawalsClosed();` to sweep() so an admin unpause (visible through the timelock) is required first; otherwise state in README/AUDIT.md that sweeps are exempt from the pause.

**Reproduction**

State: guardian calls pauseWithdrawals(); tok listed with dailyCap 5000e18, maxWithdrawal 1000e18; vault holds 20000e18 tok. Input: a valid SIGNER voucher for 10e18 -> reverts WithdrawalsClosed. admin calls sweep(tok, 0xBEEF, 5000e18) in the same state -> expected if the pause is a full brake: WithdrawalsClosed; actual: succeeds, 0xBEEF receives 5000e18 (five times maxWithdrawal, no cosigner) while player withdrawals are frozen. Reproduced in Foundry (test_sweepWhilePaused).

### 6. Info: setToken accepts cosignAbove == maxWithdrawal, which silently makes the COSIGNER requirement unreachable for that token

`msft95-vault/contracts/MSFT95Vault.sol:265`

```
        if (cfg.cosignAbove > cfg.maxWithdrawal || cfg.maxWithdrawal > cfg.dailyCap) revert BadConfig();
```

withdraw() rejects amount > maxWithdrawal before deciding whether a cosigner is needed (amount > cosignAbove), so with cosignAbove == maxWithdrawal no payable voucher ever needs the second key: a single SIGNER can take maxWithdrawal per voucher and dailyCap per window. The validation already rejects cosignAbove > maxWithdrawal, so it is clearly meant to keep the limits consistent, but it is off by one for the equality. This is admin-only configuration (trusted role), the project's own Hardhat suite deliberately uses cosignAbove == maxWithdrawal (E(40)/E(40)) to disable cosigning in a test, and the mainnet limits in scripts/deploy.js all keep cosignAbove < maxWithdrawal, so this is reported as a configuration hazard rather than a defect (downgraded from audit_economics' low). Fix: reject `cfg.cosignAbove >= cfg.maxWithdrawal` unless an explicit sentinel (e.g. type(uint128).max) is used to opt out of cosigning for a token, and update the suite accordingly.

**Reproduction**

State: admin calls setToken(tok, {listed, depositsEnabled, minDeposit 1, maxWithdrawal 1000e18, dailyCap 5000e18, cosignAbove 1000e18}). Expected if the limits must keep the cosigner reachable: BadConfig. Actual: accepted. Then Withdrawal{alice, tok, 1000e18, nonce 1, deadline now+3600} signed by the SIGNER key only is paid in full (alice +1000e18) with no COSIGNER signature. Reproduced in Foundry (test_cosignEqualMax).

### 7. Info: Invariants 8 and 9 are not strict on-chain: ETH can be forced in by SELFDESTRUCT and ERC-20s sent directly, so reconciliation must use balance >= liabilities

`msft95-vault/contracts/MSFT95Vault.sol:154`

```
    receive() external payable {
        revert UseDepositETH();
    }
```

receive() rejecting plain transfers achieves its stated purpose, but it cannot stop value entering by other routes: a contract that SELFDESTRUCTs with the vault as beneficiary (unconditional on the shanghai target; still allowed same-transaction after EIP-6780) credits the balance with no code executed and no event, and any ERC-20 can be transfer()ed to the vault address directly. Neither emits Deposited or BankrollFunded, so 'ETH can only enter through depositETH or fundBankroll' (invariant 8) and 'balance always equals deposits plus bankroll minus withdrawals minus sweeps' (invariant 9) hold only for the contract's own paths. No funds are at risk (surplus is sweepable by the admin within dailyCap), but the GUARDIAN reconciliation bot must compare liabilities <= balance, not ==, or an outsider could trigger a withdrawal pause with a 1 wei transfer. Merged from audit_flow and audit_permissions. Fix: reword the two invariants and the bot's rule; no contract change needed.

**Reproduction**

State: vault deployed with ETH listed, balance 500 ether. Input: deploy `contract Bomb { constructor(address payable to) payable { selfdestruct(to); } }` with 1 ether and to = address(vault). Expected per invariant 8: revert. Actual: address(vault).balance becomes 501 ether, no event, receive() never runs; a plain 1 wei call to the vault in the same test does revert. Reproduced in Foundry (test_forcedEth, evm_version shanghai).

### 8. Info: Hardhat suite does not exercise the edges the brief lists (exact window boundary, malformed/high-s signatures, two SIGNER keys, cosigner revocation, blocklisted recipient, hook-token reentrancy, fundB

`msft95-vault/test/vault.test.js:148`

```
      await time.increase(DAY);
```

The 29 tests cover happy paths and the main revert paths, but none pins the cases AUDIT.md singles out: (a) _spend rollover at exactly start + WINDOW (time.increase(DAY) after several mined blocks lands at start + DAY + k, so the >= branch is only confirmed by inspection) and the resulting 2x dailyCap within one second; (b) ECDSA.recover with 64-byte, empty and high-s signatures and that nonceUsed stays false; (c) two distinct SIGNER keys for amount > cosignAbove (must revert), [signer, outsider], cosigner-only, and amount == cosignAbove with one signature; (d) COSIGNER revocation between signing and submission, and re-grant; (e) an ERC-777-style token whose sender hook re-enters deposit(); (f) a USDC-style blocklisted w.user leaving nonceUsed false and window.spent unchanged; (g) fundBankroll from a non-allowlisted wallet during a deposit pause and sweep during a withdrawal pause; (h) ETH in the randomized invariant test. All of (a)-(f) were run in Foundry during this review and the contract behaves correctly (reentrancy reverts ReentrancyGuardReentrantCall, malformed signatures revert in ECDSA rather than BadSignatures, blocklist revert keeps the nonce unused, window.start is set to exactly start + WINDOW), so this is a coverage gap, not a defect; (g) are the findings above. Merged from audit_flow, audit_permissions and audit_economics. Fix: add these as regression tests so a refactor of _verify or _spend cannot regress silently.

**Reproduction**

Example untested input: setToken(tok, {maxWithdrawal 100e18, dailyCap 100e18, cosignAbove 100e18}); withdraw 100e18 at T (window.start = T); at T + 1 days - 1 a 1 wei withdraw reverts DailyCapExceeded(100e18 + 1, 100e18); at exactly T + 1 days remainingToday(tok) == 100e18 and a 100e18 withdraw succeeds with window(tok) == (T + 1 days, 100e18). Expected and actual agree (documented 2x behaviour) but no test in test/vault.test.js asserts it; likewise none passes a 64-byte or high-s signature, two SIGNER keys, a blocklisting token or a hook token. Verified in Foundry (test_windowBoundary, test_sigEdges, test_blocklist, test_hookReentrancy).

### 9. Info: Deploy script leaves the deployer EOA as DEFAULT_ADMIN until the Safe accepts, and acceptance is only possible strictly after the full ADMIN_DELAY (open deployment item)

`msft95-vault/scripts/deploy.js:52`

```
  const vault = await Vault.deploy(deployer.address, delay);
```

Outside the contract scope, reported as an open deployment item. The vault is constructed with the hot deployer key as default admin, configured, and then beginDefaultAdminTransfer(ADMIN) is called. With AccessControlDefaultAdminRules the Safe can only call acceptDefaultAdminTransfer() once block.timestamp is strictly past schedule = now + delay (2 days on mainnet); until then, or forever if the Safe never accepts, the deployer EOA holds full admin power (setToken, sweep up to dailyCap per token per window, grantRole). The script also only rejects SIGNER == COSIGNER, not SIGNER == GUARDIAN or COSIGNER == GUARDIAN. Mitigation that keeps the design: deploy with the Safe as the constructor admin and run configuration from the Safe (or deploy with delay 0, hand over, then raise it with changeDefaultAdminDelay), and extend the equality check to all three role addresses.

**Reproduction**

State: vault deployed with delay 2 days by `admin`, beginDefaultAdminTransfer(newAdmin) called at time T. Input: newAdmin calls acceptDefaultAdminTransfer() at exactly T + 2 days -> reverts AccessControlEnforcedDefaultAdminDelay (OpenZeppelin requires schedule < block.timestamp); the same call at T + 2 days + 1 succeeds and defaultAdmin() == newAdmin. During the delay hasRole(DEFAULT_ADMIN_ROLE, deployer) is true. Also verified that handing admin to an account already holding SIGNER_ROLE works through the _grantRole override. Reproduced in Foundry (test_adminHandover).

---

Judge's submission `059650338e18194b949eaebdea608852419c65b206a089690da844e2e5534826`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
