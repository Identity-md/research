# Audit report

> MineWorldCraft – full smart contract audit before mainnet (Robinhood Chain)
>
> Repo: https://github.com/AdamNakamoto/MineWorld   Commit: <COMMIT>
> Foundry project in contracts/ (forge test). Detailed brief: AUDIT.md in the repo root.
>
> SCOPE (contracts/src)
> - MineToken.sol: $MINE, a line-for-line copy of Courier World's audited StampToken (21M cap, one-shot minter)
> - MineVault.sol: the only minter of $MINE: at most 35,000 a day and 10.5M in total
> - MiningSites.sol (UUPS proxy): mining sites (bought with ETH), site levels 1–5 paid in $MINE, EIP-712 voucher claims
> - MinePayments.sol (UUPS): in-game $MINE payments (shop 75% burned, rocket tickets 100% to treasury)
> - CrafterLevels.sol (UUPS): Crafter NFT levels paid in $MINE (75% burned)
> - MinePayer.sol, UpgradeCosts.sol, lib/OwnedUUPS.sol, ICrafterAttributes.sol: shared bases
> - MineWorldCrafters.sol + CrafterArt.sol: 3,333 fully on-chain NFTs, ERC721-C enforced 5% royalty, commit-reveal mint
> - MineHook.sol, MineRouter.sol, MineEthRouter.sol: Uniswap v4 hook (4% fee) and routers, derived from Courier
>   World's audited StampHook/routers (IMD audits ea514609, ca28d248, 19b34b9b). Please diff them against
>   github.com/AdamNakamoto/courierworld contracts/src and review every difference.
> Out of scope: tests, scripts, web/, multiplayer/ (except the trust assumptions below).
>
> WHAT TO CHECK
> 1. Token: total minted can never exceed 21,000,000; burns are permanent; the minter is set once (the vault);
>    ownership renounced at deploy; no proxy, pause, blacklist or transfer tax (must look clean on token scanners).
> 2. MineVault: never mints more than 35,000 $MINE in a UTC day or 10.5M in total, whoever the distributor is,
>    including across a distributor change; the distributor can only change after the 2-day delay (cancellable);
>    it can't mint to anyone but through its distributor; not upgradeable.
> 3. MiningSites: voucher signatures (replay, deadline, malleability, EIP-712 domain surviving proxy upgrades);
>    a claim never pays more than (lifetime total − settled) × the site's rate, within the wallet cap, the global cap
>    and the vault's room; settled/claimed accounting and rounding (in the vault's favour); site price sent straight
>    to the treasury; upgradeSite takes exactly the cost (75% burned, 25% treasury) and never touches the vault;
>    bounds on rates (10–100%, non-decreasing), costs, caps and added levels.
> 4. CrafterLevels: only the Crafter's current owner can level it; levels stay with the token; costs and burn split;
>    levels can be added, never removed; the Level attribute it returns is safe inside tokenURI.
> 5. MinePayments: pay() burns the kind's share and sends the rest to the treasury, emits Paid; nobody can spend
>    another wallet's $MINE; bounds on kinds and burn shares.
> 6. MineWorldCrafters: the 5% royalty enforcement can't be bypassed or removed; the commit-reveal is fair (no
>    one can pick traits); mint limits and price; links and images stay editable after mint-out; a reverting or
>    gas-heavy attributes extension can't break tokenURI; ERC-4906 events.
> 7. MineHook and routers: the 4% fee can't be changed and its recipient is final after the renounce; launch
>    liquidity locked for good; market-cap maths with the 21M supply.
> 8. Upgradeability: OwnedUUPS and the ERC-7201 storage layouts (no collisions), only the owner can upgrade, all
>    state survives an upgrade, implementations can't be initialized, two-step ownership with no renounce.
> 9. Reentrancy and approvals wherever $MINE or ETH moves; front-running of owner price changes.
> 10. Deploy scripts: the predicted proxy address, the order of setMinter / renounce / hook renounce, and
>     ownership handed to the owner wallet 0x6e85Dc9f094b7DD35a2A981AbBd0AC9C496670eD.
>
> KNOWN AND ACCEPTED (please confirm the risk is bounded as described)
> - The game server's voucher key decides earnings: a leaked key can take at most the daily caps until the owner
>   pauses claims or replaces the signer.
> - MiningSites, CrafterLevels and MinePayments are UUPS-upgradeable by the owner with no delay; the vault's
>   35,000-a-day limit is the hard guarantee whatever their code is.
> - Rocket tickets are checked by the server from the Paid event; shop items live in the player's browser.
> - A site's conversion rate applies when the player claims.
>
> Please report findings by severity with file:line and a suggested fix.

| | |
|---|---|
| Repository | https://github.com/AdamNakamoto/MineWorld.git |
| Commit | `ba2a8edc688e94a48b810f83ccc3ea9d66c9e0f9` |
| Job | `0792975e-220d-4fe2-a11c-d611efec47bd` |
| Judged | 2026-10-14 20:49 UTC |
| Findings | 2 medium · 3 low · 3 info |

Four agents audited the code as it is at `ba2a8ed`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Medium: Owner can choose the Crafters reveal seed by choosing the reveal block (traits and rarity can be picked)

`contracts/src/MineWorldCrafters.sol:188`

```
        uint256 s = uint256(keccak256(abi.encode(secret, blockhash(block.number - 1))));
```

reveal() mixes the committed secret with blockhash(block.number - 1) of whichever block the owner's reveal transaction lands in. The only timing constraint is block.number > saleClosedAt: there is no fixed target block and no deadline. The owner knows the secret, and every candidate parent hash is public before the reveal is sent, so for each later block the owner can compute keccak256(abi.encode(secret, blockhash(b-1))) off chain (or simulate reveal with eth_call), run the trait derivation for the tokens it or associates hold (the mint is free, walletLimit up to 50, any number of wallets), and submit reveal(secret) only in a block whose seed makes those tokens Legendary (6% weight, so a chosen token comes out Legendary within a few dozen L1 blocks) or steers the collection's rarity split. The commit only proves the secret was fixed in advance; it does not stop the revealer from choosing the second input. This contradicts the contract's own guarantee ('can't pick looks') and brief item 6 ('no one can pick traits'); rarity affects resale value and in-game mining boosts. Reported by four specialists; merged here. Suggested fix (keeps the owner role and the commit-reveal flow): fix the entropy block when the sale closes, e.g. in setSaleOpen(false) store revealBlock = block.number + 1 (or an ArbSys L2 block), and in reveal() require block.number > revealBlock, use blockhash(revealBlock) and revert if it is 0 (more than 256 blocks late; re-closing the sale re-arms a new fixed block, which anyone can verify). Optionally allow anyone to finalize after N blocks so a bad outcome can't be withheld either, or use a VRF.

**Reproduction**

State: collection deployed with seedCommit = keccak256(abi.encode(secret)); owner opens the sale, alice mints 5 (or the owner mints its own), owner closes the sale at block C. For each candidate block b > C the owner simulates reveal(secret) and reads rarityOf(1). Expected: one closed sale plus one committed secret gives one seed, whatever block reveal() is called in. Actual: reveal at C+1 and reveal at C+7 (same secret, same closed sale, from the same state snapshot) store different seeds (in the proof: 89110138109460661580911489495598206716565743752638812713435134057975102108917 vs 17416135721765145890079825158127499930264022087608429494583600355493153399605), and looping over candidate blocks until rarityOf(1) == 2 finds a block that makes the owner's own Crafter #1 Legendary (specialist test test_ownerGrindsItsOwnCrafterToLegendary, re-run here, fails with 'the owner found a reveal block that makes its Crafter #1 Legendary'). The attached proof fails on the current code with 'the owner can pick among seeds by choosing the reveal block'.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import {Test} from "forge-std/Test.sol";
import {MineWorldCrafters} from "src/MineWorldCrafters.sol";
import {CrafterArt} from "src/CrafterArt.sol";

contract OkValidator {
    function validateTransfer(address, address, address, uint256) external view {}
}

/// Fails on the current code: the revealed seed depends on which block the owner chooses to reveal in, so the owner
/// can wait for a block whose seed gives chosen tokens the traits they want. Passes once the entropy is bound to a
/// block fixed when the sale closes (or the reveal is otherwise made timing-independent).
contract RevealSeedTest is Test {
    address owner = makeAddr("owner");
    address alice = makeAddr("alice");
    uint256 secret = 12345;

    function _collection() internal returns (MineWorldCrafters c) {
        CrafterArt art = new CrafterArt();
        OkValidator v = new OkValidator();
        c = new MineWorldCrafters(owner, owner, 0, keccak256(abi.encode(secret)), address(v), art);
        vm.prank(owner);
        c.setSaleOpen(true);
        vm.prank(alice);
        c.mint(5);
        vm.prank(owner);
        c.setSaleOpen(false);
    }

    /// The same closed sale, revealed one block later or seven blocks later, must give every Crafter the same look.
    function test_SeedDoesNotDependOnTheRevealBlock() public {
        MineWorldCrafters c = _collection();
        uint256 closed = block.number;
        uint256 snap = vm.snapshotState();
        vm.roll(closed + 1);
        vm.prank(owner);
        c.reveal(secret);
        uint256 seedA = c.seed();
        vm.revertToState(snap);
        vm.roll(closed + 7);
        vm.prank(owner);
        c.reveal(secret);
        uint256 seedB = c.seed();
        assertEq(seedA, seedB, "the owner can pick among seeds by choosing the reveal block");
    }
}
```

### 2. Medium: Replacing the vault's distributor forces an uninitialised MiningSites proxy on chain; whoever initialises it first after acceptDistributor owns it and can have the vault mint to them

`contracts/src/MiningSites.sol:161`

```
        if (address(vault_.token()) != address(token_) || vault_.distributor() != address(this)) revert BadVault();
```

MiningSites.initialize refuses to run unless the vault already names this proxy its distributor, and MineVault.proposeDistributor (MineVault.sol:125) refuses any address without code. Only the launch escapes this because the vault's constructor takes the proxy's predicted address. For every later replacement (the purpose of proposeDistributor and the 2-day delay, e.g. after a key or proxy compromise) the new proxy must be deployed with empty init data, proposed, sit uninitialised through the 2-day wait, be accepted, and only then be initialised in a separate transaction from the owner (an EOA per launch.env). Between acceptDistributor() and that initialize() anyone can call initialize on the proxy with their own owner_, signer_, treasury_ and caps: initialize has no caller restriction, and an ERC1967Proxy deployed with empty data leaves it open. The hijacker then opens a site for 1 wei, signs its own vouchers and the vault mints up to 35,000 $MINE a day to it (3,500 per wallet) until the owner proposes yet another distributor, which takes 2 more days and runs the same race again. The vault's 35,000/day limit bounds the loss but the rules contract, its signer and its treasury are lost. Suggested fix (keeps the design): let initialize also accept being the vault's pending distributor (vault_.pendingDistributor() == address(this)) and drop the code-length requirement in proposeDistributor, so the owner can propose the predicted proxy address first and then deploy the proxy with its initialize call in the ERC1967Proxy constructor, never leaving it uninitialised. Alternatively require msg.sender == vault_.owner() in initialize. Either way, document that a replacement proxy must never sit uninitialised.

**Reproduction**

State: token, vault and the launch MiningSites proxy deployed as in Deploy.s.sol. (1) The owner tries proposeDistributor(predictedAddress) for a proxy not yet deployed: reverts NotAContract, so the replacement is deployed as new ERC1967Proxy(impl, "") (initialising it here would revert BadVault). (2) vault.proposeDistributor(replacement). (3) warp 2 days. (4) vault.acceptDistributor(). (5) attacker calls replacement.initialize(token, vault, attacker, attacker, attackerSigner, 1, 3_500e18, 35_000e18). Expected: revert, owner() stays the real owner. Actual: success, owner() == attacker. (6) attacker.openSite{value:1}(), signs an Earnings voucher for total 1_000_000e18 with attackerSigner and calls claim: the vault mints 3,500 $MINE to the attacker. The attached proof (two tests) fails on the current code with 'a stranger initialised the replacement distributor' and 'the vault minted 3,500 $MINE to whoever initialised the replacement distributor'.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import {Test} from "forge-std/Test.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {ERC1967Proxy} from "@openzeppelin/contracts/proxy/ERC1967/ERC1967Proxy.sol";
import {MineToken} from "src/MineToken.sol";
import {MineVault} from "src/MineVault.sol";
import {MiningSites} from "src/MiningSites.sol";

/// A replacement distributor (a second MiningSites proxy for the same vault) can only be initialised once the vault
/// already names it distributor, and the vault only accepts a proposal for an address that already has code. So the
/// replacement must sit on chain uninitialised through the 2-day wait and the owner's acceptDistributor(); whoever
/// calls initialize() first after that owns it, picks its signer and treasury, and can have the vault mint to them.
contract DistributorRaceTest is Test {
    address owner = makeAddr("owner");
    address treasury = makeAddr("treasury");
    address attacker = makeAddr("attacker");
    uint256 attackerKey = 0xA11CE;

    MineToken token;
    MineVault vault;
    MiningSites impl;

    function setUp() public {
        token = new MineToken(address(this), address(0), 0);
        impl = new MiningSites();
        address predicted = vm.computeCreateAddress(address(this), vm.getNonce(address(this)) + 1);
        vault = new MineVault(token, owner, predicted);
        address sites = address(
            new ERC1967Proxy(
                address(impl),
                abi.encodeCall(
                    MiningSites.initialize,
                    (IERC20(address(token)), vault, owner, treasury, owner, 1, 1_500e18, 35_000e18)
                )
            )
        );
        assertEq(sites, predicted);
        token.setMinter(address(vault));
        token.renounceOwnership();
    }

    function test_replacementDistributorCannotBeHijacked() public {
        bytes memory init = abi.encodeCall(
            MiningSites.initialize, (IERC20(address(token)), vault, owner, treasury, owner, 1, 1_500e18, 35_000e18)
        );
        address replacement;
        // The way a fixed design would do it: propose the predicted address, then deploy the proxy initialised.
        address predicted = vm.computeCreateAddress(address(this), vm.getNonce(address(this)));
        vm.prank(owner);
        (bool proposed,) = address(vault).call(abi.encodeCall(MineVault.proposeDistributor, (predicted)));
        if (proposed) {
            replacement = address(new ERC1967Proxy(address(impl), init));
            assertEq(replacement, predicted);
        } else {
            // What the current code forces: an uninitialised proxy, proposed once it has code.
            replacement = address(new ERC1967Proxy(address(impl), ""));
            vm.prank(owner);
            vault.proposeDistributor(replacement);
        }
        vm.warp(block.timestamp + 2 days);
        vm.prank(owner);
        vault.acceptDistributor();
        assertEq(vault.distributor(), replacement);

        // Anyone may now try to initialise the replacement as its owner and signer. It must not work.
        vm.prank(attacker);
        (bool hijacked,) = replacement.call(
            abi.encodeCall(
                MiningSites.initialize,
                (IERC20(address(token)), vault, attacker, attacker, vm.addr(attackerKey), 1, 3_500e18, 35_000e18)
            )
        );
        assertFalse(hijacked, "a stranger initialised the replacement distributor");
        assertEq(MiningSites(replacement).owner(), owner, "the replacement distributor isn't the owner's");
    }

    /// The same race, followed through to the vault minting for the hijacker.
    function test_hijackerMintsFromTheVault() public {
        address replacement = address(new ERC1967Proxy(address(impl), ""));
        vm.prank(owner);
        vault.proposeDistributor(replacement);
        vm.warp(block.timestamp + 2 days);
        vm.prank(owner);
        vault.acceptDistributor();

        address signer = vm.addr(attackerKey);
        vm.prank(attacker);
        (bool hijacked,) = replacement.call(
            abi.encodeCall(
                MiningSites.initialize,
                (IERC20(address(token)), vault, attacker, attacker, signer, 1, 3_500e18, 35_000e18)
            )
        );
        if (!hijacked) return; // fixed: nothing to show

        MiningSites s = MiningSites(replacement);
        vm.deal(attacker, 1);
        vm.prank(attacker);
        s.openSite{value: 1}();
        bytes32 structHash = keccak256(
            abi.encode(s.EARNINGS_TYPEHASH(), attacker, uint256(1_000_000e18), uint64(block.timestamp + 1 hours))
        );
        (uint8 v, bytes32 r, bytes32 sg) =
            vm.sign(attackerKey, keccak256(abi.encodePacked("\x19\x01", s.domainSeparator(), structHash)));
        vm.prank(attacker);
        uint256 paid = s.claim(1_000_000e18, uint64(block.timestamp + 1 hours), abi.encodePacked(r, sg, v));
        assertEq(paid, 3_500e18);
        assertEq(token.balanceOf(attacker), 3_500e18);
        fail("the vault minted 3,500 $MINE to whoever initialised the replacement distributor");
    }
}
```

### 3. Low: tokenURI is not isolated from the attributes extension: a gas-heavy attributesOf, or one returning malformed data, reverts every Crafter's metadata

`contracts/src/MineWorldCrafters.sol:217`

```
        try ICrafterAttributes(x).attributesOf(tokenId) returns (string memory a) {
```

extraAttributes() is called first in tokenURI() and forwards all but 1/64 of the remaining gas to the extension, with no stipend and no bound on the returned data. Solidity's try/catch only catches the external call reverting. Two cases still revert tokenURI for every token: (a) the extension consumes the gas it is given (an unbounded loop in a buggy upgrade of the owner-upgradeable CrafterLevels proxy): the catch branch runs with only the 1/64 held back, which is far short of the ~1.5M gas rendering the on-chain SVG and base64-encoding the JSON needs, so tokenURI runs out of gas under any ordinary eth_call budget (reproduced at 10M and at 30M gas); (b) the extension's attributesOf exists but its return data does not decode as (string), e.g. no return data: the ABI decode failure happens in the caller's frame and is not caught. The NatSpec ('if it can't be read: the metadata never breaks for it') and brief item 6 ('a reverting or gas-heavy attributes extension can't break tokenURI') therefore hold only for a plainly reverting extension. The extension is owner-set, so this is a misconfiguration or bad-upgrade hazard, recoverable with setAttributesExtension(address(0)); impact is metadata unavailability on marketplaces and wallets meanwhile. Reported by three specialists; merged here. Suggested fix: call the extension with a fixed gas stipend (e.g. a raw staticcall{gas: 300_000} or try ... attributesOf{gas: 300_000}(tokenId)), check success and that the return data is a well-formed ABI string (returndatasize() >= 64, offset == 0x20, length consistent and below a few KB) before decoding, otherwise fall back to ""; optionally call the extension after the art has been rendered.

**Reproduction**

Deploy CrafterArt and MineWorldCrafters, open the sale, mint token #1, close, roll one block, reveal. Baseline: staticcall tokenURI(1) with 10,000,000 gas returns ok. Owner sets the extension to a contract whose attributesOf reverts: still ok. Owner sets it to a contract whose attributesOf is `while (true) {}`: staticcall tokenURI(1) with 10,000,000 gas returns ok == false, and with 30,000,000 gas also ok == false (expected: a data: URI without extra traits). Owner sets it to a contract with `function attributesOf(uint256) external pure {}` (no return data): tokenURI(1) reverts (expected: a URI without extra traits). Scratch test JudgeTest (test_gasHogExtensionBreaksTokenURI, test_gasHogAt30M, test_noReturnExtensionBreaksTokenURI) fails on all three on the current code.

### 4. Low: A treasury that rejects ETH makes openSite() (and a paid Crafters mint) revert for every player

`contracts/src/MiningSites.sol:197`

```
        Address.sendValue(payable(treasury()), address(this).balance);
```

openSite() forwards the whole ETH balance to the treasury in the same call, and MinePayer._setTreasury (MinePayer.sol:67-72) only rejects address(0) and the contract itself. The treasury is shared with the $MINE flows, so the owner can legitimately point it at a contract that takes ERC-20s but has no payable receive or fallback (a plain token-holding contract, a splitter without receive, a module). From that moment every openSite() reverts with Address.FailedCall, so no new player can convert earnings until the owner changes the treasury again. MineWorldCrafters.mint has the same shape at MineWorldCrafters.sol:173 whenever price > 0 (setTreasury there has the same checks). The launch TREASURY in launch.env is an EOA, so this is a configuration hazard rather than an attack, but nothing on chain prevents it and the existing test test_TreasuryCantReenter only covers a reentrant treasury, not a non-payable one. Suggested fix: in MinePayer._setTreasury and MineWorldCrafters.setTreasury probe that the address accepts ETH (a zero-value call that must succeed), or decouple the ETH recipient from the $MINE recipient, or make the ETH leg pull-based.

**Reproduction**

State: MiningSites proxy initialised with sitePrice 0.005 ETH. Owner calls setTreasury(np) where np is a contract with no receive or fallback (`contract NonPayable {}`): accepted. alice calls openSite{value: 0.005 ether}(). Expected: the site opens and the treasury receives the ETH, or the setter had refused np. Actual: the call reverts (Address.FailedCall) and openSite is unusable for everyone until the treasury is changed. Scratch test JudgeTest.test_nonPayableTreasuryBlocksOpenSite fails on the current code with 'openSite reverts with a non-payable treasury'.

### 5. Low: upgradeSite() and CrafterLevels.upgrade() take no maxCost, so a cost raise mined just before the call charges whatever the wallet has approved

`contracts/src/MiningSites.sol:203`

```
    function upgradeSite() external nonReentrant returns (uint256 level) {
```

upgradeSite() (and CrafterLevels.upgrade(tokenId), CrafterLevels.sol:89, same pattern) reads the next level's cost from storage at execution time and pulls it with burnFrom plus transferFrom. The only thing that stops a setUpgradeCosts() or setUpgradeBurnBps() transaction mined just before the player's upgrade from charging more than the price the player saw is the size of the player's allowance. The contracts' NatSpec relies on the web client approving exactly the cost, but any wallet or third-party front end that grants a larger or unlimited allowance (a common wallet default) loses that protection: the owner, or whoever holds the owner key, can raise a level to MAX_UPGRADE_COST (1,000,000 $MINE for sites, 2,000,000 for Crafters) and take it. The owner is trusted, but brief item 9 asks that front-running of owner price changes be bounded, and the contract itself should bound it rather than the client. Suggested fix: add an explicit maxCost parameter (and optionally the expected level) to upgradeSite and upgrade, `if (cost > maxCost) revert`, and keep the client approving exactly the cost. MinePayments.pay() already carries the amount and is unaffected.

**Reproduction**

State: alice holds 1,000,000 $MINE, has opened a site (level 1) and approved MiningSites for type(uint256).max; upgradeCost(2) is 4,620e18. Owner sends setUpgradeCosts([1_000_000e18, 18_942e18, 77_662e18, 318_415e18]) and it lands first; alice's upgradeSite() lands next. Expected: alice pays 4,620 $MINE or the call reverts. Actual: upgradeSite() succeeds, alice's balance goes from 1,000,000 to 0 (750,000 burned, 250,000 to the treasury). Scratch test JudgeTest.test_costRaiseChargesUnlimitedApproval passes on the current code (i.e. the overcharge happens). Same with CrafterLevels.upgrade and MAX_UPGRADE_COST = 2,000,000e18.

### 6. Info: Royalty enforcement is only as strong as the validator the owner points at: setTransferValidator accepts any contract, including one that approves every transfer

`contracts/src/MineWorldCrafters.sol:356`

```
        if (validator.code.length == 0) revert NotAContract();
```

Brief item 6 asks to confirm the 5% royalty enforcement can't be bypassed or removed. The 5% rate (ROYALTY_BPS) is fixed and the validator can't be unset, but the only check on a new validator is that it has code, so the owner can replace it with a contract whose validateTransfer is a no-op, after which marketplaces that ignore ERC-2981 can move Crafters with no royalty; conversely a validator that always reverts blocks every holder-to-holder transfer until replaced. The contract's trust notes document this as an intentional owner power (needed if OpenSea moves registries), so it is reported as a trust assumption with a concrete bypass, not a permission bug. Two specialists reported it; merged here. Cheap hardening: require the new validator to support the ICreatorTokenTransferValidator interface id (ERC-165) marketplaces check, and state plainly in the docs and brief that the owner can relax enforcement. Also note the launch validator (0xA000027A9B2802E1ddf7000061001e5c005A0000) only enforces a policy for this collection once its security policy is registered with that validator after deploy; the deploy scripts do not do this, so it is an open launch item for the owner.

**Reproduction**

Owner calls setTransferValidator(address(new PassValidator())) where PassValidator.validateTransfer(address,address,address,uint256) is an empty view function (the project's own tests and the specialists' scratch tests use exactly such a validator; the launch deploy uses script/DevTransferValidator.sol on a dev chain). Expected per the brief: enforcement cannot be removed. Actual: the call succeeds, and any transferFrom by an approved marketplace then passes _update's validator call with no royalty check.

### 7. Info: After the hook's renounce the fee recipient can still be moved by the current recipient, contrary to the renounce NatSpec and brief item 7

`contracts/src/MineHook.sol:361`

```
        if (msg.sender != owner && msg.sender != feeRecipient) revert NotOwner();
```

renounceOwnership's NatSpec (MineHook.sol:380) says 'Gives up ownership for good: the fee recipient can never change again', and the brief says the recipient 'is final after the renounce'. But setFeeRecipient also lets msg.sender == feeRecipient repoint the fees after the renounce. setFeeRecipient's own NatSpec documents this, the project's test test_FeeRecipientCanMoveItsOwnFees asserts it, and the code is identical to Courier World's audited StampHook (Courier World audit 19b34b9b finding 3). No third party can redirect fees, so this is a documentation and expectation mismatch, not a theft path, but a compromised fee-recipient key can redirect all future 4% fees for good. Suggested fix: correct the renounce NatSpec and the brief to 'only the current recipient can move it', or, if true finality is wanted, drop the feeRecipient branch once owner == address(0).

**Reproduction**

After openPool and renounceOwnership (owner == address(0)), the feeRecipient calls setFeeRecipient(X). Expected per the renounce doc and brief item 7: revert. Actual: it succeeds, feeRecipient == X and every later collectProtocolFees pays X (the project's own test test_FeeRecipientCanMoveItsOwnFees in test/MineHook.t.sol exercises exactly this and passes).

### 8. Info: Hook diff vs StampHook: the start-tick floor is -300,000 (MIN_START_TICK) instead of -400,000; the only code difference in the hook, routers and token

`contracts/src/MineHook.sol:151`

```
        if (startTick_ % TICK_SPACING != 0 || startTick_ > MAX_START_TICK || startTick_ < MIN_START_TICK) revert BadTick();
```

Diffing contracts/src/MineHook.sol, MineRouter.sol, MineEthRouter.sol and MineToken.sol against Courier World's StampHook.sol, StampRouter.sol, StampEthRouter.sol and StampToken.sol (github.com/AdamNakamoto/courierworld, contracts/src) after renaming $STAMP to $MINE and Stamp* to Mine*: every difference is a rename or a comment except this line and the new constant MIN_START_TICK = -300_000 (MineHook.sol:86). StampHook rejects startTick_ < -MAX_START_TICK (-400,000); MineHook rejects startTick_ < -300,000, so the accepted range is narrower and a start market cap needing a tick between -400,000 and -300,000 fails at construction instead of launching (Deploy.s.sol uses the same bound). No security impact: the fee, liquidity-lock, renounce and market-cap logic are byte-for-byte the same, and the 21M launch supply stays far below v4's per-tick liquidity cap at either bound. Reported so the reviewed diff is complete; no change needed unless the lower tick range is wanted.

**Reproduction**

Input: new MineHook(..., startTick_ = -350_000, ...). StampHook with the same arguments constructs; MineHook reverts BadTick(). At startTick_ = -300_000 both construct. The diff command `sed 's/Stamp/Mine/g; s/STAMP/MINE/g' StampHook.sol | diff - MineHook.sol` shows these two lines as the only non-comment differences; the routers and token show none.

---

Judge's submission `bda268f35903d85a1ff27026350c60c95f79d3ca7c3a03ced6a6ebf2206d3b6c`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
