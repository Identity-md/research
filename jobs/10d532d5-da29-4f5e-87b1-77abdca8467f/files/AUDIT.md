# Audit report

> MineWorldCraft – third re-check: fixes for IMD Swarm second re-check 52b534f9
>
> Repo: https://github.com/AdamNakamoto/MineWorld   Commit: 25121ea
> History: audit 0792975e (ba2a8ed), re-check 8c7ba957 (49830f2), second re-check 52b534f9 (4de227d). Every finding of
> 52b534f9 and its fix (file:line and the tests) is in AUDIT.md section 10. forge test: 243 passed, 10 fork tests
> skipped without a fork (all 10 pass on a Robinhood Chain fork). Also new since 4de227d: the I'M DIO mint is free with
> at most 3 per wallet at launch, and the collection's ownership can never be renounced (so OpenSea Studio editing
> stays possible).
>
> Please verify each fix and check the changed code for anything new:
> 1. MEDIUM late initialisation: MiningSites.initialize now runs only inside the proxy's own constructor
>    (address(this).code.length == 0, for anyone); the late path is removed, so a proxy deployed without initialize can
>    never be set up. Your FakeVaultHijackTest is in the suite as submitted, plus the own-vault variant.
> 2. LOW free re-roll: after the 256-block window seal() reverts EntropyExpired; only the owner can call
>    moveEntropyOn(), at most MAX_ENTROPY_MOVES = 3 times (event each time), after which the reveal is Stuck. Anyone can
>    still seal within the window; the panel and dev.sh send seal() right after reveal() and retry. A fuzz test shows a
>    seal anywhere in the window always fixes the seed.
> 3. LOW level clamp: _import and bookOf keep the raw level (bounded by MAX_LEVELS); the rate is clamped only where
>    used (_siteRate), and _nextLevel reverts MaxLevel at or past the top. Your hop scenario and a 3-hop case pass.
> 4. INFO: revealStatus says Sealable only while current - entropyBlock < 256 (one block of margin).

| | |
|---|---|
| Repository | https://github.com/AdamNakamoto/MineWorld.git |
| Commit | `25121ea568bdca173068a2d6a101fade9691a29e` |
| Job | `10d532d5-da29-4f5e-87b1-77abdca8467f` |
| Judged | 2026-10-15 03:41 UTC |
| Findings | 3 low · 2 info |

Four agents audited the code as it is at `25121ea`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Low: A vault whose distributor has no code can never be given a working distributor: initialize calls bookOf on the codeless predecessor

`contracts/src/MiningSites.sol:204`

```
            try MiningSites(current).bookOf(address(0)) {}
```

Since fix #1, MiningSites.initialize is the only way a proxy is ever set up, and it treats any vault.distributor() other than itself as a predecessor that must answer bookOf(address(0)). If that address has no code, Solidity's high-level call reverts in the caller on the extcodesize check before the try/catch can catch anything (so not even BadPredecessor): the proxy's constructor reverts and ERC1967Proxy bubbles it as FailedCall(). MineVault's constructor takes a predicted distributor address and cannot check it has code (the proxy is deployed next), so any launch where the MiningSites proxy did not land at the predicted address (an extra transaction from the deployer between the vault and the proxy broadcasts, or a manual launch skipping Deploy.s.sol's require) leaves the vault naming a codeless address. From then on every replacement proxy built from this implementation reverts in its constructor, acceptDistributor can never pass (it needs a contract whose predecessor() equals the codeless address, and only initialize sets predecessor), and MineToken's ownership is renounced with the vault as its only minter. This contradicts AUDIT.md section 4 guarantee 6 ('a distributor can always be replaced') and MineVault's recovery NatSpec. It is a recoverability gap behind an operator mistake, not an attack, and the way out post-launch exists (a new MiningSites implementation tolerant of a codeless predecessor, since initialize runs on the replacement's own implementation), hence Low. Fix: in initialize, when current.code.length == 0 record it as predecessor without calling bookOf (and make _import/bookOf skip a codeless predecessor), or make the predicted-address check a hard launch precondition in the docs. Reproduced by the attached test (fails with FailedCall() on 25121ea).

**Reproduction**

State: MineVault(token, owner, never) where `never` has no code (a predicted proxy address that was never used), token.setMinter(vault), token.renounceOwnership(). Owner: vault.proposeDistributor(P) with P its next CREATE address; deploy new ERC1967Proxy(impl, abi.encodeCall(MiningSites.initialize, (token, vault, owner, treasury, signer, 1, 1_500e18, 35_000e18))) at P. Expected: the proxy deploys, records `never` as predecessor with empty books, and acceptDistributor two days later makes it the distributor. Actual: the proxy constructor reverts with FailedCall() (the undecodable bookOf call to a codeless address), vault.distributor() stays `never`, acceptDistributor reverts NotAContract forever, and the vault can never mint. Ran in Foundry on 25121ea: test_AVaultWithACodelessDistributorCanStillBeReplaced fails with FailedCall().

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import {Test} from "forge-std/Test.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {IERC721} from "@openzeppelin/contracts/token/ERC721/IERC721.sol";
import {ERC1967Proxy} from "@openzeppelin/contracts/proxy/ERC1967/ERC1967Proxy.sol";
import {MineToken} from "src/MineToken.sol";
import {MineVault} from "src/MineVault.sol";
import {MiningSites} from "src/MiningSites.sol";
import {CrafterLevels} from "src/CrafterLevels.sol";
import {MinePayments} from "src/MinePayments.sol";

/// Fails on 25121ea; passes once the defect is fixed.
contract CodelessDistributorProofTest is Test {
    address owner = makeAddr("owner");
    address treasury = makeAddr("treasury");

    /// A vault whose distributor of the moment has no code must still be replaceable by its owner (AUDIT.md section 4,
    /// guarantee 6: "a distributor can always be replaced").
    function test_AVaultWithACodelessDistributorCanStillBeReplaced() public {
        MineToken token = new MineToken(address(this), address(0), 0);
        MiningSites impl = new MiningSites();
        address never = makeAddr("neverDeployed");
        MineVault vault = new MineVault(token, owner, never);
        token.setMinter(address(vault));
        token.renounceOwnership();

        address next = vm.computeCreateAddress(address(this), vm.getNonce(address(this)));
        vm.prank(owner);
        vault.proposeDistributor(next);
        MiningSites replacement = MiningSites(
            address(
                new ERC1967Proxy(
                    address(impl),
                    abi.encodeCall(
                        MiningSites.initialize,
                        (IERC20(address(token)), vault, owner, treasury, owner, 1, 1_500e18, 35_000e18)
                    )
                )
            )
        );
        assertEq(address(replacement), next);
        vm.warp(block.timestamp + 2 days);
        vm.prank(owner);
        vault.acceptDistributor();
        assertEq(vault.distributor(), next, "the vault never got a working distributor");
    }
}
```

### 2. Low: CrafterLevels.initialize and MinePayments.initialize keep the late path MiningSites lost: a proxy deployed uninitialised is anyone's

`contracts/src/CrafterLevels.sol:55`

```
    function initialize(IERC20 token_, IERC721 crafters_, address owner_, address treasury_) external initializer {
```

Fix #1 made MiningSites.initialize revert InitializeOutsideConstructor unless address(this).code.length == 0, so nobody can take over a proxy someone else deployed. CrafterLevels.initialize (CrafterLevels.sol:55) and MinePayments.initialize (MinePayments.sol:57), on the same OwnedUUPS base and the same ERC1967Proxy deploy pattern, have only OpenZeppelin's `initializer`, so a proxy of either deployed in two steps (empty constructor data, initialize later) is initialised by whoever calls first. That caller becomes owner (setUpgradeCosts, setUpgradeBurnBps, setTreasury, upgradeToAndCall on CrafterLevels; addKind, setKindBurn, setTreasury, upgradeToAndCall on MinePayments) and treasury, so every DIO level bought or shop/ticket payment routed to that proxy pays its treasury share to the stranger, who can also swap the implementation. Reachable only through an operator two-step deploy (Deploy.s.sol initialises in the proxy's constructor), hence Low; merged from the two specialist findings since the root cause and the fix are one. Fix: the same one-line guard as MiningSites.sol:191 in both initializers, or move it into OwnedUUPS.__Owned_init so every proxy of the family has it.

**Reproduction**

address levels = address(new ERC1967Proxy(address(new CrafterLevels()), "")); address payments = address(new ERC1967Proxy(address(new MinePayments()), "")); then from any account `stranger`: CrafterLevels(levels).initialize(token, IERC721(anyContract), stranger, stranger) and MinePayments(payments).initialize(token, stranger, stranger). Expected (the guarantee fix #1 gives MiningSites): both revert and the proxies can never be set up. Actual: both succeed; owner() == stranger and treasury() == stranger on each. Ran in Foundry on 25121ea: test_StrangerCannotInitialiseLateLevelsOrPaymentsProxies fails ('a stranger initialised a CrafterLevels proxy deployed uninitialised').

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import {Test} from "forge-std/Test.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {IERC721} from "@openzeppelin/contracts/token/ERC721/IERC721.sol";
import {ERC1967Proxy} from "@openzeppelin/contracts/proxy/ERC1967/ERC1967Proxy.sol";
import {MineToken} from "src/MineToken.sol";
import {MineVault} from "src/MineVault.sol";
import {MiningSites} from "src/MiningSites.sol";
import {CrafterLevels} from "src/CrafterLevels.sol";
import {MinePayments} from "src/MinePayments.sol";

/// Fails on 25121ea; passes once the defect is fixed.
contract LateInitProofTest is Test {
    address stranger = makeAddr("stranger");

    /// CrafterLevels' and MinePayments' proxies, like MiningSites', must not be anyone's to set up after deployment.
    function test_StrangerCannotInitialiseLateLevelsOrPaymentsProxies() public {
        MineToken token = new MineToken(address(this), address(0), 0);
        address levels = address(new ERC1967Proxy(address(new CrafterLevels()), ""));
        address payments = address(new ERC1967Proxy(address(new MinePayments()), ""));

        vm.startPrank(stranger);
        (bool okLevels,) = levels.call(
            abi.encodeCall(CrafterLevels.initialize, (IERC20(address(token)), IERC721(address(token)), stranger, stranger))
        );
        (bool okPayments,) =
            payments.call(abi.encodeCall(MinePayments.initialize, (IERC20(address(token)), stranger, stranger)));
        vm.stopPrank();
        assertFalse(okLevels, "a stranger initialised a CrafterLevels proxy deployed uninitialised");
        assertFalse(okPayments, "a stranger initialised a MinePayments proxy deployed uninitialised");
        assertEq(CrafterLevels(levels).owner(), address(0));
        assertEq(MinePayments(payments).owner(), address(0));
    }
}
```

### 3. Low: Free mint: the 3-per-wallet limit is per msg.sender only, so one actor sweeps the supply through throwaway contracts

`contracts/src/MineWorldCrafters.sol:233`

```
        if (mine > walletLimit) revert WalletLimit();
```

New since 4de227d: the I'M DIO mint is free with walletLimit = 3. The only bound on how many DIOs one actor takes is mintedBy[msg.sender], and mint lets any contract be msg.sender (_mint with no receiver or caller check). A contract that creates fresh child contracts, each minting 3 in its constructor and transferring them out, is a new msg.sender every time, so the per-wallet limit bounds nothing per person. With price 0 the cost is gas only: 100 children (300 DIOs) cost about 22M gas in one transaction in the reproduction, under Arbitrum's per-transaction limit, so about twelve transactions take all 3,333 the moment setSaleOpen(true) lands. The documented rule (AUDIT.md section 10 and the panel: 'free, at most 3 per wallet') promises a spread the contract cannot keep: a paid mint priced the sybil out, a free one does not. This is a limitation of the chosen rule rather than a bypass of its letter, hence Low: the owner should decide whether a free launch needs a gate a fresh contract cannot pass (a per-wallet server signature like MiningSites' vouchers, an allowlist, or a price), or document that the limit is per address only.

**Reproduction**

State: sale open, price 0, walletLimit 3 (the launch defaults). Input: attacker EOA calls Sweeper.sweep(crafters, 100); Sweeper does new Child(crafters, msg.sender) 100 times; each Child's constructor calls crafters.mint(3) then transferFrom to the attacker. Expected under the stated rule: one actor ends with at most 3. Actual: the attacker holds 300 after one transaction (about 21.9M gas), mintedBy[attacker] == 0, totalMinted == 300. Ran in Foundry on 25121ea: test_OneActorHoldsAtMostThreeAfterOneTx fails with '300 > 3'.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import {Test} from "forge-std/Test.sol";
import {MineWorldCrafters} from "src/MineWorldCrafters.sol";
import {CrafterArt} from "src/CrafterArt.sol";

/// A validator that allows every transfer (stands in for OpenSea's registry).
contract OpenValidator {
    function validateTransfer(address, address, address, uint256) external pure {}
}

/// A throwaway wallet: mints the per-wallet maximum and hands the Crafters to its maker, all in its constructor.
contract Child {
    constructor(MineWorldCrafters c, address to) {
        uint256 first = c.totalMinted() + 1;
        c.mint(3);
        for (uint256 i; i < 3; i++) {
            c.transferFrom(address(this), to, first + i);
        }
    }
}

/// One actor, one transaction: `n` fresh wallets, 3 each.
contract Sweeper {
    function sweep(MineWorldCrafters c, uint256 n) external {
        for (uint256 i; i < n; i++) {
            new Child(c, msg.sender);
        }
    }
}

contract SybilMintTest is Test {
    MineWorldCrafters crafters;
    address owner = makeAddr("owner");
    address treasury = makeAddr("treasury");
    address attacker = makeAddr("attacker");

    function setUp() public {
        crafters = new MineWorldCrafters(
            owner, treasury, 0, keccak256(abi.encode(uint256(1))), address(new OpenValidator()), new CrafterArt()
        );
        vm.prank(owner);
        crafters.setSaleOpen(true);
    }

    /// The launch rule "free, at most 3 per wallet" holds per msg.sender only: one actor ends one transaction holding
    /// 300 Crafters, minted through 100 throwaway contracts, for about 18M gas (one Arbitrum transaction); twelve
    /// such transactions take all 3,333. Fails on the code as it is (the actor holds 300); passes once a free mint
    /// is gated by something a fresh contract can't supply (an allowlist or a server signature per wallet, say).
    function test_OneActorHoldsAtMostThreeAfterOneTx() public {
        Sweeper s = new Sweeper();
        vm.prank(attacker);
        (bool ok,) = address(s).call{gas: 30_000_000}(abi.encodeCall(Sweeper.sweep, (crafters, 100)));
        emit log_named_string("sweep went through", ok ? "yes" : "no");
        emit log_named_uint("attacker holds", crafters.balanceOf(attacker));
        emit log_named_uint("attacker's own mintedBy", crafters.mintedBy(attacker));
        assertLe(crafters.balanceOf(attacker), 3, "one actor holds more than the per-wallet limit after one tx");
    }
}
```

### 4. Info: Trust assumption: in practice the owner alone decides whether each 26-second window is sealed, and holds a choice among up to four seeds

`contracts/src/MineWorldCrafters.sol:310`

```
    function moveEntropyOn() external onlyOwner returns (uint256 next) {
```

Fix #2 is correctly implemented: seal() reverts EntropyExpired past 256 blocks, only the owner can moveEntropyOn, at most MAX_ENTROPY_MOVES = 3 times with an event each, Stuck afterwards, and the suite's fuzz test shows a seal anywhere in the window fixes the seed (verified: the Crafters suite passes, 50 tests). What remains is a trust assumption worth stating in the launch material rather than a code defect: 'anyone can seal within the window' holds for 256 L2 blocks, about 26 seconds, after an owner transaction nobody can anticipate on a sequenced chain with no public mempool, and the only sealer shipped is the owner's own panel. So in practice the owner decides whether a window is sealed and can choose among up to four public seeds (the first window plus three moves), picking the one that gives wallets it controls the most Legendaries (6%) and Rares (25%); the mint being free and the limit per msg.sender makes holding many DIOs cheap. The edge is modest (best of four) and every move is public; the design is accepted in AUDIT.md 3.7. No code change is required; holders wanting the 'anyone seals' guarantee must run a sealer watching SecretRevealed/EntropyBlockMoved, or the owner should pre-announce the reveal.

**Reproduction**

Owner reveals at chain block n (entropyBlock = n+1). At n+2 the owner computes S0 = keccak256(abi.encode(secret, hash(n+1))) and its wallets' rarities under S0 and sends no seal. If nobody seals by n+257, revealStatus() == Expired and seal() reverts EntropyExpired; the owner calls moveEntropyOn() (entropyBlock = n+259), computes S1 at n+260, and so on for S2 and S3, sealing at the first seed it prefers. Expected per the contract NatSpec: 'the owner can't pick looks'. Actual: the owner chooses one of up to four public outcomes whenever no third party seals within the window. Mechanics confirmed in Foundry on 25121ea: after vm.roll(entropyBlock + 257) seal() reverts EntropyExpired, a stranger's moveEntropyOn reverts, the owner's succeeds (entropyBlock = +258, entropyMoves = 1); the suite's test_TheOwnerMovesOnAtMostThreeTimes shows the three moves then NoMovesLeft and Stuck.

### 5. Info: revealStatus's one-block Sealable margin is about 100 ms on Robinhood Chain, shorter than a transaction's sequencing latency

`contracts/src/MineWorldCrafters.sol:333`

```
        if (current - b < ENTROPY_WINDOW) return RevealStatus.Sealable;
```

Fix #4 makes revealStatus() answer Sealable only while current - entropyBlock < ENTROPY_WINDOW, documented as 'only while a seal sent now can still land in the window (a block to spare)'. The margin is one L2 block, roughly 100 ms on Robinhood Chain's ~0.1 s blocks, less than the time a signed transaction takes to reach the sequencer and be included. A client that trusts Sealable near the end of the window sends a seal that lands past it and reverts EntropyExpired. In the panel this is worse than a retry: send() simulates against the latest block (still Sealable), broadcasts, and on a reverted receipt throws Error('seal failed') (web/chain.js:173), which revealAndSeal does not recognise as RevealTooSoon/EntropyExpired/AlreadyRevealed and so rethrows (web/chain.js:445) instead of moving on to the owner's move. Impact is bounded (a wasted seal and a confusing error at the very end of a window the panel normally seals in its first second), hence Info. A margin in the order of the chain's latency (20-30 blocks) or the panel comparing chainBlock() with entropyBlock() itself would make the status mean what its NatSpec says.

**Reproduction**

State: entropyBlock = E, chain at E + 255, entropyMoves = 0. revealStatus() returns Sealable (2). A client sends seal() on seeing it; on Robinhood Chain the transaction is sequenced several L2 blocks later, at E + 258 say. Expected (per the NatSpec): the seal lands in the window. Actual: seal() at E + 258 reverts EntropyExpired (current - b = 258 > 256); the panel's send() throws 'seal failed' and revealAndSeal rethrows it. Confirmed in Foundry on 25121ea: reveal at block 1000 (E = 1001), vm.roll(E + 255) gives revealStatus() == Sealable, vm.roll(E + 256) gives Expired where seal() still succeeds, vm.roll(E + 257) makes seal() revert EntropyExpired.

---

Judge's submission `8ba05731348758baecf835925654eee8aa2e51d50315c7923d68262c9d5ba86d`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
