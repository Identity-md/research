# Audit report

> Audit Courier Companions: an ERC-1155 collection of in-game companions for Courier World (https://courierworld.fun), sold only for $STAMP on Robinhood Chain (chain 4663). Contracts review only: no deployment.
>
> Repo: github.com/AdamNakamoto/courierworld, commit bbe1784eabeeb6a0fe4d0746958a72ad3977c652
> In scope: contracts/src/CourierCompanions.sol (and its use in contracts/script/DeployCompanions.s.sol)
> Tests: contracts/test/CourierCompanions.t.sol, contracts/test/CourierCompanions.invariant.t.sol (forge test --match-contract CourierCompanions)
> Dependencies: OpenZeppelin Contracts 5.4.0. $STAMP is contracts/src/StampToken.sol (ERC20 + ERC20Permit + ERC20Burnable, no transfer tax), deployed at 0xBaB43AF01C32a952ff14B395D026cf1874932Bc5.
>
> What it does: each companion kind is a token id with a $STAMP price, a max supply, a per-wallet limit (0 = none) and an open flag. buy(id, quantity, maxCost) and buyWithPermit(...) take price x quantity $STAMP straight from the buyer to the treasury (the contract never holds tokens) and mint the companions. 1 to 10 per buy. Resales pay an ERC-2981 royalty (5% to the treasury at deploy, owner can change it up to 10%).
>
> Promises to verify:
> - Nothing can be minted without paying the current price; the owner has no free mint and no way to take anyone's tokens.
> - A buyer never pays more than maxCost, and pays exactly price x quantity, all to the treasury.
> - A kind's supply can only shrink, never below what's been minted; minted never exceeds maxSupply.
> - Wallet limits count lifetime purchases, not balances; transfers don't reset them.
> - No reentrancy through onERC1155Received or the $STAMP transfer; a failed mint reverts the whole buy (no $STAMP moves).
> - A front-run permit doesn't break buyWithPermit.
> - Safe casts (uint128 price, uint32 supply/minted/perWallet) and no overflow.
> - Owner powers are only: setKind, setTreasury, setBase, setRoyalty (max 10%), two-step ownership transfer.
> - ERC-1155 and ERC-2981 compliance; name/symbol/uri work on OpenSea.
> - The deploy script sets up the lineup as intended.
>
> Please report findings by severity with suggested fixes; don't push to the repository, and I'll fix and ask for a re-check.

| | |
|---|---|
| Repository | https://github.com/AdamNakamoto/courierworld.git |
| Commit | `bbe1784eabeeb6a0fe4d0746958a72ad3977c652` |
| Job | `145af84f-02c5-4db7-8dc3-3ec3a300b8f1` |
| Judged | 2026-10-13 22:45 UTC |
| Findings | 3 low · 6 info |

Four agents audited the code as it is at `bbe1784`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Low: setTreasury rotates sale proceeds but leaves the ERC-2981 royalty receiver at the old treasury

`contracts/src/CourierCompanions.sol:148`

```
        treasury = treasury_;
```

The constructor binds both destinations to one address: sales go to `treasury` and `_setDefaultRoyalty(treasury_, 500)` makes it the royalty receiver. The deploy script documents TREASURY as 'where the $STAMP goes, and the 5% royalty' and the brief says the royalty is '5% to the treasury'. setTreasury only rewrites `treasury`; the royalty receiver stays on the previous address until the owner separately calls setRoyalty and re-supplies the bps. A treasury rotation (move to a multisig, lost or compromised key) therefore keeps routing every marketplace royalty to the abandoned address, and nothing (event, revert, test) signals the split. Reported by all four specialists; merged. Fix (keeps the design): in setTreasury, carry the royalty over when it still points at the old treasury, e.g. `(address r, uint256 fee) = royaltyInfo(0, _feeDenominator()); if (r == treasury) _setDefaultRoyalty(treasury_, uint96(fee));` before assigning, or document in setTreasury's NatSpec and the runbook that setRoyalty must be called alongside it, and add a test asserting royaltyInfo after setTreasury.

**Reproduction**

Deploy with treasury T (royaltyInfo(1, 1000e18) == (T, 50e18)). Owner calls setTreasury(N), N != T. Expected (per '5% to the treasury'): royaltyInfo(1, 1000e18) == (N, 50e18). Actual: treasury() == N and the next buy pays N, but royaltyInfo(1, 1000e18) still returns (T, 50e18). Reproduced in test/scratch/Judge.t.sol::test_setTreasuryLeavesRoyaltyReceiver (passes on current code, asserting the stale receiver). The existing test_newTreasuryGetsTheNextSales never reads royaltyInfo.

### 2. Low: renounceOwnership is a live one-step, irreversible owner power outside the stated set, and it freezes the lineup

`contracts/src/CourierCompanions.sol:22`

```
contract CourierCompanions is ERC1155, ERC2981, Ownable2Step, ReentrancyGuard {
```

The brief lists the owner powers as setKind, setTreasury, setBase, setRoyalty and a two-step ownership transfer. Ownable2Step still inherits Ownable.renounceOwnership(), which is not overridden: a single call with no acceptance step sets owner to address(0) permanently. Afterwards no kind can be closed, repriced or shrunk, the treasury and royalty receiver can never be rotated, and the base URI can never change, while every open kind keeps selling at its frozen price to the frozen treasury forever. A mis-click, an ops script that renounces (the project's other deploys do), or a compromised owner key does this in one transaction, defeating the reason Ownable2Step was chosen. Not an unprivileged bypass; it is a deviation from the stated owner-power list with an unrecoverable outcome. Reported by all four specialists; merged. Fix: `function renounceOwnership() public view override onlyOwner { revert(); }` (or a custom error) plus a test that it reverts; or, if renouncing is wanted, list it as an intended power and decide what lineup state it should leave behind.

**Reproduction**

State: fresh deploy, kind 1 open at 100e18. Owner calls renounceOwnership(). Expected per the stated powers: revert or a pending step. Actual: owner() == address(0); the former owner's setKind(1, 100e18, 300, 0, false) reverts OwnableUnauthorizedAccount(owner); alice can still approve and buy(1, 1, 100e18), receives one companion, and 100e18 STAMP goes to the now-unchangeable treasury. Reproduced in test/scratch/Judge.t.sol::test_renounceFreezes. No existing test touches renounceOwnership.

### 3. Low: 'No free mint' holds only nominally: the owner can price a kind at 1 wei and buy, and with owner == treasury (as the deploy runbook directs) owner buys are free at any price

`contracts/src/CourierCompanions.sol:130`

```
        if (price == 0 || price > type(uint128).max) revert BadPrice();
```

The promise is that nothing is minted without paying the current price and the owner has no free mint. Literally true: the owner has no mint function. But setKind accepts any price >= 1 wei, any perWallet (0 = none), and takes effect immediately, so the owner can atomically set a scarce kind to 1 wei, buy 10 per call, and restore the price, taking legendaries for 1e-17 STAMP each. Separately, script/deploy-companions.sh says 'Sign with the treasury wallet: it becomes the owner', so in the intended deployment owner == treasury, and _buy's safeTransferFrom(buyer, treasury, cost) is then a self-transfer: every owner purchase is free at the listed price, no price change needed. Neither is a permission bypass (the owner role is the agreed design), but both contradict the stated guarantee and the 'limited stays limited' economics, since minted supply of a 25-30 unit kind can be taken by the owner at no cost. Reported by three specialists as trust-assumption/low; merged and kept at low because the deploy runbook makes the free path the default configuration. Fix options that preserve the owner role: (a) state the trust assumption in README/AUDIT.md and the NatSpec instead of 'the owner has no free mint'; (b) add a MIN_PRICE floor (e.g. 1e18) and/or a delay on price cuts for existing kinds; (c) deploy with a treasury distinct from the owner.

**Reproduction**

Path 1: owner holds >= 10 wei STAMP; kind 31 at 2500e18, supply 30, perWallet 1. Owner calls setKind(31, 1, 30, 0, true); approve(shop, 10); buy(31, 10, 10); setKind(31, 2500e18, 30, 1, true). Actual: owner STAMP balance drops by exactly 10 wei, balanceOf(owner, 31) == 10, kinds(31).price == 2500e18, minted == 10. Path 2: deploy with treasury_ == owner_; owner approves and calls buy(31, 10, type(uint256).max) at 2500e18. Actual: owner STAMP balance unchanged, owner holds 10 of kind 31. Expected per promise: the owner cannot obtain companions without paying the going price. Reproduced in test/scratch/Judge.t.sol::test_ownerNearFreeMint and ::test_ownerIsTreasuryBuysFree.

### 4. Info: buyWithPermit leaves a residual allowance of maxCost - cost on the shop, and hides permit failures behind an allowance error

`contracts/src/CourierCompanions.sol:103`

```
        try IERC20Permit(address(stamp)).permit(msg.sender, address(this), maxCost, deadline, v, r, s) {} catch {}
```

Two related behaviours, neither a loss on this code. (1) The permit is signed for maxCost (the buyer's ceiling) but _buy pulls only price x quantity, so whatever slack the front end adds stays approved to the shop indefinitely. The shop only ever calls safeTransferFrom(msg.sender, ...), so nobody else can spend it today, but wallets show a standing approval and it would become live exposure if a future version added any pull path keyed on an address other than msg.sender. (2) The blanket try/catch is what makes a front-run permit harmless (good, and verified by the existing test_permitUsedFirstStillBuys), but it also swallows a bad, expired or wrong-value signature, so the buyer sees ERC20InsufficientAllowance with no hint the signature was the problem. The 'never pays more than maxCost' and 'pays exactly price x quantity' promises hold. Reported by three specialists; merged. Optional fixes: have the front end sign the permit for the exact quoted cost when it does not need slack and document the standing approval; after the catch, if stamp.allowance(msg.sender, address(this)) < cost revert with a dedicated PermitFailed error (or emit an event in the catch branch).

**Reproduction**

(1) Kind 1 at 100e18; alice signs permit(alice, shop, 150e18, deadline) and calls buyWithPermit(1, 1, 150e18, deadline, v, r, s). Actual: treasury +100e18, one companion minted, stamp.allowance(alice, shop) == 50e18 afterwards. (2) alice signs a permit for 100e18 + 1 but calls buyWithPermit(1, 1, 100e18, ...) with no prior allowance. Actual: revert ERC20InsufficientAllowance(shop, 0, 100e18), nonce unconsumed; expected: a permit-specific error. Reproduced in test/scratch/Judge.t.sol::test_permitLeftoverAllowance and ::test_badPermitMaskedAsAllowance.

### 5. Info: setTreasury accepts the shop's own address, and the contract has no way to recover tokens sent to it

`contracts/src/CourierCompanions.sol:147`

```
        if (treasury_ == address(0)) revert ZeroAddress();
```

The only rejected treasury is address(0). If the owner mis-pastes the deployed address into setTreasury (or the constructor), every buy still succeeds and the contract that 'never holds tokens' accumulates $STAMP with no sweep or rescue function, so it is locked forever. Likewise any ERC-20 sent to the shop by mistake is unrecoverable. Owner misconfiguration only. Reported by two specialists; merged. Fix: also revert when treasury_ == address(this) in setTreasury and the constructor; optionally add an owner-only rescue(IERC20, to) limited to the shop's own balance (it never legitimately holds anything, so this adds no power over user funds).

**Reproduction**

Owner calls setTreasury(address(shop)); alice approves and calls buy(1, 1, 100e18). Actual: buy succeeds, stamp.balanceOf(address(shop)) == 100e18 and no function can move it. Expected: setTreasury reverts for the shop's own address. Reproduced in test/scratch/Judge.t.sol::test_treasuryCanBeShop.

### 6. Info: The resale royalty is advisory only: no transfer validator (unlike CourierSkins) and no contractURI

`contracts/src/CourierCompanions.sol:82`

```
        _setDefaultRoyalty(treasury_, 500);
```

royaltyInfo is correct and supportsInterface advertises ERC-2981, but ERC-2981 only reports a royalty; safeTransferFrom and safeBatchTransferFrom are the stock OpenZeppelin implementations with no transfer hook, so any peer-to-peer sale or any marketplace that ignores royaltyInfo pays the treasury nothing. The sibling CourierSkins collection enforces its 5% through an OpenSea creator-fee transfer validator (SKINS_VALIDATOR in launch.env, validateTransfer in CourierSkins.sol), so the two collections sold under one brand carry different royalty guarantees. There is also no contractURI() (ERC-7572), so the collection-level name, description and royalty shown on OpenSea depend on marketplace settings. Fine if intended; the brief's 'Resales pay an ERC-2981 royalty' is the standard phrasing for an advisory royalty. Reported by two specialists; merged. Options: add a contractURI() getter; if enforcement is wanted, add the ERC-1155 equivalent of the Skins validator pattern (owner-replaceable validator consulted in _update for non-mint transfers); otherwise say in README/AUDIT.md that enforcement depends on the marketplace.

**Reproduction**

alice buys kind 31 for 2500e18; treasury STAMP balance = T. bob pays alice 10_000e18 STAMP directly (stamp.transfer), then alice calls shop.safeTransferFrom(alice, bob, 31, 1, ''). Actual: bob holds kind 31, treasury balance still == T, nothing reverts. royaltyInfo(31, 10_000e18) returns (treasury, 500e18) but nothing acts on it. Reproduced in test/scratch/Judge.t.sol::test_royaltyAdvisory.

### 7. Info: Per-wallet limits bound purchases per address, and MAX_PER_BUY bounds a call, so neither limits distribution: one actor can sweep a kind

`contracts/src/CourierCompanions.sol:114`

```
        if (k.perWallet != 0 && already + quantity > k.perWallet) revert WalletLimit();
```

Both mechanisms do exactly what the brief says (lifetime purchases per address, unaffected by transfers; 1 to 10 per buy). Trust assumption, recorded so the lineup is not marketed as 'one per player': a buyer with N wallets buys N x perWallet and consolidates with safeTransferFrom, so the 1-per-wallet legendaries (ids 31, 32, 41-43) can be bought out by one actor from fresh EOAs in a block; and for the perWallet = 0 kinds (ids 1-3, 11-13) a contract can loop buy(id, 10, ...) and take an entire 300-unit supply in a single transaction at launch. 'Limited' kinds are limited in total, not in distribution. Reported by three specialists; merged. No contract fix short of allowlists; if fair distribution matters, give every kind a perWallet (accepting the sybil caveat) or state the limit's meaning in the game copy.

**Reproduction**

(a) Kind 1 open at 100e18, maxSupply 300, perWallet 0. A contract holding 30_000e18 STAMP approves the shop and calls buy(1, 10, max) thirty times inside one external call (its onERC1155Received returns the selector). Actual: it holds 300 of kind 1 after one transaction and alice's next buy(1, 1, 100e18) reverts SoldOut. (b) Kind 31 perWallet 1: alice buys 1, wallet a2 buys 1 and transfers it to alice. Actual: balanceOf(alice, 31) == 2 while bought[alice][31] == 1. Reproduced in test/scratch/Judge.t.sol::test_wholeKindSweptInOneTx and ::test_walletLimitSybil.

### 8. Info: Deploy script lineup is correct, but it points at metadata and a companions.js that are not in the tree, and new kinds emit no URI event

`contracts/script/DeployCompanions.s.sol:45`

```
        string memory base = vm.envOr("COMPANIONS_BASE", string("https://courierworld.fun/companions/"));
```

The lineup itself matches the brief: broadcasting the script on a local Anvil node (StampToken deployed first, DEV_CHAIN=true) produced owner == broadcaster, treasury == TREASURY, royaltyInfo(1, 10000) == (TREASURY, 500), kindCount 13, and ids 1-3 at 100e18/300/0, 11-13 at 250e18/150/0, 21-22 at 500e18/50/2, 31-32 at 2500e18/30/1, 41-43 at 3000e18/25/1, all open, uri(41) == base + '41.json'. Two flow gaps remain before it is broadcast for real: (1) the script's comment says 'The game's companions.js draws each id', but web/ has no companions.js, no companions/ directory and no reference to companions at all (export-web.sh is already wired to merge deployments/robinhood-companions.json), so at the default base every uri(id) 404s and OpenSea shows nothing until the 13 JSON files and the drawing code are published; since the script opens every kind immediately, buyers could pay STAMP for ids the game cannot show. (2) setKind for a new kind emits KindSet but no ERC-1155 URI event (only setBase loops them), so indexers keyed on URI events will not pick up new kinds' metadata until setBase is called again. Not contract defects. Reported by two specialists; merged. Pre-deploy items: publish web/companions/{1,2,3,11,12,13,21,22,31,32,41,42,43}.json and companions.js (or point COMPANIONS_BASE where they already live) before running deploy-companions.sh, or deploy with open = false and open kinds once the game reads them; optionally emit URI(uri(id), id) in setKind when a kind is first added.

**Reproduction**

`grep -ri companion web/` returns nothing and `ls web/companions` fails with 'No such file or directory' at commit bbe1784. Broadcasting DeployCompanions on Anvil and calling uri(1) returns 'https://courierworld.fun/companions/1.json', a path the site does not serve, while kinds(1).open == true so buy(1, 1, 100e18) succeeds immediately.

### 9. Info: Test gaps: royalty after setTreasury, renounceOwnership, malformed permits, treasury == shop, transfers in the invariant handler, and the deploy script are untested

`contracts/test/CourierCompanions.t.sol:311`

```
    function test_newTreasuryGetsTheNextSales() public {
```

The suites are strong on the buy path (exact payment, maxCost, supply shrink, reentrancy via onERC1155Received, failed-mint atomicity, permit front-run, fuzz on price x quantity; 24 unit tests and 3 invariants pass, 128k handler calls). Edges left unexercised: (1) test_newTreasuryGetsTheNextSales never reads royaltyInfo after setTreasury (it would have caught the receiver asymmetry); (2) no test calls renounceOwnership; (3) no test passes a wrong-value, wrong-spender or expired permit to buyWithPermit with no allowance, nor checks the residual allowance; (4) no test calls setTreasury(address(shop)) or setRoyalty(address(0), x) (OZ reverts ERC2981InvalidDefaultRoyaltyReceiver); (5) no safeBatchTransferFrom / balanceOfBatch coverage; (6) the invariant handler never transfers, so invariant_boughtMatchesBalances only restates the handler's own behaviour, and handler.configure wraps setKind in try/catch with supply bounded to 1..500, so SupplyCanOnlyShrink reverts are swallowed (0 configure reverts across 63k calls); (7) DeployCompanions.run() is never executed in a test, so the 13-kind lineup is only checked by eye. Reported by all four specialists; merged. Suggested additions: assert royaltyInfo after setTreasury; a renounceOwnership test (reverting once the override lands); malformed-permit and residual-allowance tests; a transfer action in the handler with the invariant restated as bought[b][id] >= balance obtained by purchase; assert configure revert reasons; a script test that deploys a StampToken, sets STAMP/TREASURY via vm.setEnv and runs the lineup (note: run() must be called without an active prank, since startBroadcast and pranks are incompatible).

**Reproduction**

`forge test --match-contract CourierCompanions`: 25 tests pass. `grep -n 'renounceOwnership\|royaltyInfo\|allowance(\|safeBatchTransferFrom\|DeployCompanions' test/CourierCompanions.t.sol test/CourierCompanions.invariant.t.sol` shows royaltyInfo only in test_uriRoyaltyAndInterfaces (never after setTreasury) and no hits for the others. The scratch tests in test/scratch/Judge.t.sol exercise each listed edge and show behaviour the current suite does not pin down.

---

Judge's submission `5a110d421ebe6ebd52955c9a70e8c082bbe6780191563d965ba25cfa76201f80`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
