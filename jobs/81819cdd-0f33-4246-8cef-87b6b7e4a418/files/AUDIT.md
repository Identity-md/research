# Audit report

> Weir Townies: AUDIT ONLY. Review src/WeirTownies.sol from this repository as it arrives (do not edit src/, test/, foundry.toml or lib/) and report findings; do NOT deploy anything, do NOT create a token, pool, distributor or website. The owner deploys from script/Deploy.s.sol with their own key after findings at medium or above are fixed. Context: an ERC-721 (OpenZeppelin v5.5.0: ERC721, ERC721Enumerable, ERC2981, Ownable2Step, MerkleProof, ReentrancyGuard) for 3,333 tokens on Robinhood Chain (chainId 4663, Arbitrum Orbit, cancun). Token ids are laid out by the owner before the sale (setLayout, sealPools): an owner-minted reserve, then role pools each with its own Merkle root and a one-claim-per-wallet rule, then the general range sold first to a Merkle allowlist and then publicly at an ETH price with a per-wallet cap of 3. Metadata is off-chain at baseURI + id and the contract emits ERC-4906 events from an updater address. Money: msg.value must equal price x qty; withdraw() sends the balance to the treasury and anyone may call it. Please look hardest at: the id layout arithmetic (ranges never overlap, never exceed MAX_SUPPLY, no id minted twice), the Merkle leaf encoding (double keccak of abi.encode(address)) and proof misuse across pools, the per-wallet caps, reentrancy through _safeMint receivers, owner powers after the sale (nothing should touch sold tokens), and the withdraw path. Build: forge build && forge test (20 tests incl. fuzz and a reentrant receiver). Report any finding at medium or above and block on high or critical. Do not claim an independent audit.

| | |
|---|---|
| Repository | https://github.com/weircool/townies-contracts.git |
| Commit | `0365a3cdfa5899cd0688f594cb39a67c2e7dd7c2` |
| Job | `81819cdd-0f33-4246-8cef-87b6b7e4a418` |
| Judged | 2026-10-27 01:37 UTC |
| Findings | 1 medium · 1 low · 7 info |

Four agents audited the code as it is at `0365a3c`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Medium: setTreasury() rotates the withdraw destination but leaves the ERC-2981 royalty receiver at the old treasury

`src/WeirTownies.sol:280`

```
        treasury = t;
```

The storage comment on `treasury` (line 52) says it 'receives withdrawals and royalties' and the constructor couples the two with _setDefaultRoyalty(treasury_, 500). setTreasury() rewrites only the `treasury` slot and never refreshes ERC2981's default receiver, so royaltyInfo() keeps naming the previous address until the owner separately calls setRoyalty(bps), which re-reads `treasury`. Neither the README deploy steps nor script/Configure.s.sol (which has no royalty action) include that second call, so the documented operational flow leaves the two sinks diverged after any rotation, with no on-chain signal (TreasurySet fires, no royalty event does). Impact: after a treasury rotation, which is most likely exactly when the old key is lost or compromised, every marketplace that honours ERC-2981 keeps paying the 5% secondary-sale royalty to the retired address while withdraw() pays the new one. Owner-recoverable with one extra setRoyalty call, so medium rather than high. Minimal fix that preserves the design: keep the royalty fraction in storage (set by setRoyalty, default 500) and in setTreasury call _setDefaultRoyalty(t, royaltyBps) after `treasury = t;` (or read the current fraction via royaltyInfo(0, _feeDenominator())). Merged from four specialists (math, permissions, economics, flow) who all reported the same mechanism; severity taken from the permissions specialist because the compromised-key scenario leaks revenue for an unbounded period.

**Reproduction**

Deploy WeirTownies(owner, T1, 100, prov, 0, 0.001 ether). royaltyInfo(1, 1 ether) == (T1, 0.05 ether). Owner calls setTreasury(T2). Expected per line 52: treasury() == T2 and royaltyInfo(1, 1 ether) == (T2, 0.05 ether). Actual: treasury() == T2 but royaltyInfo(1, 1 ether) == (T1, 0.05 ether). Only a subsequent setRoyalty(500) moves the receiver. Reproduced in test/scratch/Judge.t.sol::test_royaltyDrift (passes on current code asserting the stale receiver) and by the attached proof, which fails on the current code with 'royalty receiver still points at the old treasury' and passes once setTreasury also refreshes the default royalty receiver.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {WeirTownies} from "src/WeirTownies.sol";

/// setTreasury() rotates the withdraw destination but leaves the ERC-2981 default royalty receiver at the old
/// treasury. The contract documents `treasury` as the address that "receives withdrawals and royalties".
contract RoyaltyReceiverDriftTest is Test {
    WeirTownies t;
    address owner = makeAddr("owner");
    address oldTreasury = makeAddr("oldTreasury");
    address newTreasury = makeAddr("newTreasury");

    function setUp() public {
        t = new WeirTownies(owner, oldTreasury, 100, keccak256("prov"), 0, 0.001 ether);
    }

    function test_setTreasury_movesRoyaltyReceiver() public {
        vm.prank(owner);
        t.setTreasury(newTreasury);
        assertEq(t.treasury(), newTreasury);
        (address receiver, uint256 amount) = t.royaltyInfo(1, 1 ether);
        assertEq(amount, 0.05 ether, "royalty fraction unchanged");
        // Expected: royalties follow the treasury. Actual on current code: receiver == oldTreasury.
        assertEq(receiver, newTreasury, "royalty receiver still points at the old treasury");
    }
}
```

### 2. Low: renounceOwnership() is inherited single-step and permanently freezes every owner-gated step of the sale

`src/WeirTownies.sol:28`

```
contract WeirTownies is ERC721, ERC721Enumerable, ERC2981, Ownable2Step, ReentrancyGuard {
```

Ownable2Step only makes transferOwnership/acceptOwnership two-step. OpenZeppelin's Ownable.renounceOwnership() (lib/openzeppelin-contracts/contracts/access/Ownable.sol) remains exposed, onlyOwner, and sets owner to address(0) in one transaction with no confirmation. The contract has no other admin role, so after a mistaken or compromised-key renounce nothing can ever call setPhase, ownerMint, setAllowlistRoot, setPoolRoot, setPrices, setTreasury, setRoyalty, setBaseURI, setRenderer or setUpdater. If it happens while phase == Closed the sale can never open; mid-sale the phase can never be closed, the remaining reserve can never be minted, and a treasury that later rejects ETH (see the withdraw note) would strand the balance permanently. The file header lists the owner's powers and does not mention giving up ownership, so this is a documented-intent gap, not a design choice. Fix: `function renounceOwnership() public view override onlyOwner { revert(); }`, or gate it behind a sentinel (phase == Closed and reserveMinted == reserveSize) if a deliberate end-of-life freeze is wanted, and state the policy in the NatSpec. Merged from the permissions (low) and flow (info) specialists.

**Reproduction**

State: layout sealed, phase Public. Owner calls renounceOwnership(). Actual: owner() == address(0) in one call; owner then calling setPhase(Closed) reverts OwnableUnauthorizedAccount(owner). Expected from a reader of 'Ownable2Step' and the header's enumerated powers: no single call that removes all configuration ability. Reproduced in test/scratch/Judge.t.sol::test_renounceOneStep.

### 3. Info: Wallet-cap check adds two uint8 values, so an over-cap qty near 255 reverts with Panic(0x11) instead of WalletCapReached

`src/WeirTownies.sol:209`

```
        if (generalMintedBy[msg.sender] + qty > WALLET_CAP) revert WalletCapReached();
```

generalMintedBy[msg.sender] and qty are both uint8, so the sum is evaluated in checked uint8 arithmetic. For a wallet with m prior general mints (1..3), any qty with m + qty > 255 reverts with an arithmetic panic before the comparison runs. The cap is never bypassed (checked arithmetic reverts rather than wraps, and the sum is only wrong when it already exceeds 3), so this is a revert-reason inconsistency that affects front-end error decoding only. The same checked-narrow-add pattern in setLayout (line 118 `reserveSize_ + 1`, line 123 `next += sizes[i]`) also only ever reverts. Optional fix: `if (uint256(generalMintedBy[msg.sender]) + qty > WALLET_CAP) revert WalletCapReached();`. Merged from three specialists.

**Reproduction**

Phase Public, publicPrice 0.001 ether. Wallet E calls mintPublic{value: 0.003 ether}(3). E calls mintPublic(252): reverts WalletCapReached (3 + 252 = 255 fits). E calls mintPublic(253): expected WalletCapReached, actual Panic(0x11). E still owns exactly 3 tokens. Reproduced in test/scratch/Judge.t.sol::test_uint8Panic.

### 4. Info: Configure script silently truncates POOL_SIZES, RESERVE_SIZE and RESERVE_QTY to uint32 and seals the layout in the same run

`script/Configure.s.sol:26`

```
            for (uint256 i = 0; i < sizesU.length; i++) sizes[i] = uint32(sizesU[i]);
```

The owner's configuration script reads these values as uint256 and narrows them with bare uint32(...) casts (lines 26, 27, 41). Solidity 0.8 checked arithmetic does not cover explicit narrowing casts, so a value above 2^32-1 is reduced modulo 2^32 and passed to setLayout/ownerMint as a plausible small number; the contract's BadLayout check cannot catch it because the truncated value fits under MAX_SUPPLY. Because the `layout` action calls sealPools() in the same broadcast (line 28), a truncated pool size becomes immutable with no chance to inspect pools() first. The contract itself is unaffected by correctly typed input, and a value of exactly 2^32+k is an unlikely typo, so this is an operational note. Fix: bound-check before casting (require(sizesU[i] <= type(uint32).max) or SafeCast.toUint32), print pools and generalStart, and consider a separate ACTION for sealPools. Merged from the math and permissions specialists.

**Reproduction**

Env: MAX_SUPPLY=3333, RESERVE_SIZE=33, POOL_SIZES='1,120,4294967297,80'. uint32(4294967297) == 1 (asserted in test/scratch/Judge.t.sol::test_uint32Truncation), so setLayout(33, [1,120,1,80], roots) succeeds and sealPools() freezes an Auditor pool of size 1 instead of 500; the general range is 499 ids larger than planned. Expected: the script refuses the out-of-range value.

### 5. Info: Trust assumptions: owner powers that remain live after sealing and after the sale (none touches sold tokens or balances)

`src/WeirTownies.sol:285`

```
        _setDefaultRoyalty(treasury, bps);
```

Recorded per the brief, not bypasses. All are Ownable2Step-gated. (1) setRoyalty(bps) forwards to ERC2981._setDefaultRoyalty whose only bound is bps <= 10000, so the owner can set the advisory royalty to 100% of secondary sales at any time; the header's list of post-sale powers does not mention royalties. Optional: cap it (e.g. bps <= 1000). (2) setRenderer / setBaseURI fully control tokenURI for sold tokens; a renderer with no code or a reverting tokenURI makes tokenURI() revert for every token until the owner resets it to address(0). The provenance hash commits the art but nothing on chain ties served metadata to it. Optional: a one-way freezeMetadata(). (3) setPoolRoot may change any pool's eligibility list after sealPools (documented: 'a corrected snapshot'), including pointing it at owner wallets to take unclaimed pool ids; ranges stay frozen. (4) setPhase, setPrices and setAllowlistRoot may change at any time; because mints require msg.value == price * qty exactly, a price change in flight makes pending mints revert rather than over/under-pay. (5) ownerMint is callable in any phase but only within ids 1..reserveSize. Verified absent: no burn, no forced transfer, no transfer pause, no upgradeability, no ETH path other than mints and withdraw(). Merged from permissions (two), economics and flow specialists.

**Reproduction**

Any state. Owner calls setRoyalty(10000): royaltyInfo(1, 1 ether) returns (treasury, 1 ether). Owner calls setRenderer(EOA) after token 8 is minted: tokenURI(8) reverts for all callers; setRenderer(address(0)) restores '8'. Both reproduced in test/scratch/Judge.t.sol::test_royalty100 and ::test_rendererRevert. setPoolRoot after seal is covered by the project's own test_setPoolRootAfterSeal.

### 6. Info: withdraw() is permissionless and all-or-nothing to the current treasury: a rejecting treasury blocks payout until rotation, and rotation cannot protect a balance already held

`src/WeirTownies.sol:291`

```
        (bool ok,) = treasury.call{value: amount}("");
```

Sale proceeds can only leave through treasury.call with the full balance and all remaining gas. Two operational consequences of the intended 'anyone may call, only the treasury receives' design: (a) if the treasury is a contract whose receive()/fallback reverts or runs out of gas, every withdraw() reverts TransferFailed and ETH stays in the contract until the owner calls setTreasury; recoverable while an owner exists (see the renounceOwnership finding). (b) setTreasury() cannot be used to protect a balance already in the contract: anyone, including the holder of a leaked treasury key, can call withdraw() before the rotation is included, so the owner's rotation power is effectively the power to redirect the full balance only from that block onward. Operational mitigations: withdraw promptly after each phase; rotate before funds accumulate under a suspect key. Minor: with a zero balance withdraw() succeeds from any address and emits Withdrawn(treasury, 0), harmless indexer noise; optional `if (amount == 0) revert ZeroQuantity();`. No reentrancy path: withdraw and all mint functions share one ReentrancyGuard and state is updated before _safeMint. Merged from permissions, economics and flow specialists.

**Reproduction**

(a) Owner calls setTreasury(R) where R.receive() reverts; E mints 1 at 0.001 ether; withdraw() from any account reverts TransferFailed and the balance stays 0.001 ether; after setTreasury(T2), withdraw() succeeds and T2 receives 0.001 ether (test/scratch/Judge.t.sol::test_withdrawRejecting). (b) E mints 3 at 0.001 ether; E calls withdraw() before owner's setTreasury(T2): T1 receives 0.003 ether and the subsequent setTreasury protects nothing (::test_withdrawRace).

### 7. Info: WALLET_CAP is per address and is bypassed by fresh contract receivers or EOAs; it limits per-address UX, not concentration

`src/WeirTownies.sol:209`

```
        if (generalMintedBy[msg.sender] + qty > WALLET_CAP) revert WalletCapReached();
```

The cap is enforced on msg.sender only, and _safeMint accepts any contract implementing onERC721Received. One actor can deploy N minimal receivers in a single transaction, mint 3 per receiver, and transfer all tokens to one wallet. This is inherent to any per-address cap and standard for ERC-721 sales; recorded because the brief names the cap as a guarantee to examine. If concentration matters the usual options are a tx.origin == msg.sender check (excludes smart wallets), per-block limits, or documenting the cap as soft. Distinct mechanism from the uint8 panic finding at the same line.

**Reproduction**

Phase Public, publicPrice 0.001 ether. E calls a factory that deploys 10 Buyer contracts, each calling mintPublic{value: 0.003 ether}(3) and transferring its 3 tokens to E, all in one transaction. Result: balanceOf(E) == 30 and generalMintedBy[E] == 0. Reproduced in test/scratch/Judge.t.sol::test_capBypassViaReceivers.

### 8. Info: Unclaimed role-pool ids and unsold general ids have no mint path once the phase is Closed

`src/WeirTownies.sol:169`

```
    function ownerMint(address to, uint32 qty) external onlyOwner nonReentrant {
```

ownerMint is limited to ids 1..reserveSize. Pool ids can only be minted by a member of that pool's current root, one each, while the phase is open; general ids only via mintAllowlist/mintPublic while the phase is open. There is no owner sweep for leftovers, so the 3,333 provenance-committed ids may never be fully issued; the owner's only routes are to re-point a pool root at owner-controlled wallets (one id per wallet) or to keep Public open indefinitely. Design gap, not an exploit: no funds or sold tokens are affected. If every id should eventually exist, add an owner sweep gated on phase == Closed that mints the remaining pool/general ids sequentially; otherwise document that the final collection may be smaller. From the economics specialist.

**Reproduction**

Layout reserve 1..5, pool 0 = ids 6..7 with a single-wallet root (E). E claims id 6. Owner sets phase Closed. mintRole(0, ...) reverts WrongPhase; ownerMint reverts SoldOut once the 5 reserve ids are minted; ownerOf(7) reverts ERC721NonexistentToken. Id 7 is unmintable by any call while Closed. Reproduced in test/scratch/Judge.t.sol::test_strandedPoolIds.

### 9. Info: Merkle leaf is the bare address, so any two lists given the same root accept the same proof (root-management note)

`src/WeirTownies.sol:220`

```
        bytes32 leaf = keccak256(bytes.concat(keccak256(abi.encode(account))));
```

The leaf encoding matches OpenZeppelin StandardMerkleTree ['address'] and the double hash prevents second-preimage use of internal nodes. Because the leaf carries no pool index or list identifier, a proof is bound only to the root. Pools with distinct roots are isolated (verified: a pool-1 proof fails on pool 0 with NotOnList). A proof crosses lists only if the owner sets the same root on two pools, or on a pool and the allowlist; then a wallet on the shared list claims one id per pool plus its allowlist quota, which is consistent with the stated one-claim-per-pool rule. Single-leaf trees (root == leaf, empty proof) work for a one-wallet pool such as Mayor. No code change needed; the root-generation tooling should never reuse a snapshot root across lists by accident. From the flow specialist.

**Reproduction**

Owner sets pool 0 root = keccak256(bytes.concat(keccak256(abi.encode(E)))) and setAllowlistRoot to the same value, phase Allowlist. E calls mintRole(0, []) and receives id 6; E calls mintAllowlist(1, []) and receives id 8; both with the same empty proof. After setAllowlistRoot(leaf(T2)), E's mintAllowlist reverts NotOnList. Reproduced in test/scratch/Judge.t.sol::test_sharedRoot and test/scratch/Layout.t.sol::test_everyIdMintedOnce.

---

Judge's submission `0c24bcb45f96a8d5bf0072f983f5c8e3c1705a830a912c03bbce4a0663ff896a`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
