# Audit report

> OGPass (src/OGPass.sol), deployed on Ethereum mainnet at 0xca9dc9064ffc695d979ea7da9a35130376bb3217 (commit 4527ed9). A soulbound ERC-721 club pass: 49 founders claim free via a Merkle root, with a fixed 100,000 OG buyback paid from a funded founder reserve. Public passes sit on a bonding curve, 1M + 10k*(n-1) OG; sells pay 92.5% and burn 7.5%. Cap of 1,000 passes, one per wallet. Look hardest at curve reserve solvency, the founder reserve and burnUnclaimedFounderReserve after the deadline, Merkle claim safety, soulbound enforcement, owner powers (pause, setBaseURI only), reentrancy, and slippage and deadline checks.

| | |
|---|---|
| Repository | https://github.com/identity-md-launches/launch-1343-ogpass-soulbound-erc-721-membership.git |
| Commit | `4527ed978e9f295e70dfc044f180f1aa23e96852` |
| Job | `ac2d0346-fc13-4cbc-9240-3aea5e8dd231` |
| Judged | 2026-10-12 08:40 UTC |
| Findings | 2 low · 3 info |

Four agents audited the code as it is at `4527ed9`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Low: Founder reserve accepts unbounded deposits; any excess over outstanding need is burnable by anyone from the deadline

`src/OGPass.sol:210`

```
        founderReserve += amount;
```

fundFounderReserve accepts any amount at any time and has no notion of the claim deadline or of how much the reserve can ever pay out. burnUnclaimedFounderReserve is permissionless from claimDeadline and keeps only founderOutstanding * FOUNDER_BUYBACK. Any deposit above that (before the deadline: above founderCount * FOUNDER_BUYBACK, 4,900,000 OG on mainnet) can never reach a founder and is sent to 0xdEaD by the first caller of the burn, including a searcher in the same block as a post-deadline top-up. There is no withdrawal path, so a depositor who mistypes an amount or tops up after founders have already sold loses the excess permanently. The README documents the burn, so this is a footgun on a permissionless entry point rather than a bypass; the contract gives the depositor no revert and no recovery. Merged from audit_permissions and audit_economics. Minimal fix that keeps the design: in fundFounderReserve revert when founderReserve + amount exceeds (block.timestamp < claimDeadline ? founderCount : founderOutstanding) * FOUNDER_BUYBACK, or clamp the deposit to that shortfall.

**Reproduction**

State: founderCount = 2, one founder has claimed (founderOutstanding = 1), founderReserve = 0, block.timestamp == claimDeadline. Depositor calls fundFounderReserve(300_000e18): succeeds, founderReserve == 300_000e18. Any address then calls burnUnclaimedFounderReserve(): returns 200_000e18, founderReserve becomes 100_000e18 and OG.balanceOf(0xdEaD) grows by 200_000e18. Expected: a deposit above what the one outstanding founder can ever draw (100_000e18) is refused or recoverable. Actual: accepted, then burned by a third party. Same before the deadline: deposit 250_000e18 with founderCount = 2 and no claims; at claimDeadline anyone burns all 250_000e18. Reproduced with test/scratch/Judge.t.sol::test_postDeadlineOverfundBurnable and test_preDeadlineOverfundBurnedAtDeadline (both pass, i.e. the behaviour executes as described).

### 2. Low: Allowlisted founder who already holds a public pass cannot claim and must pay the 7.5% sell fee to become eligible

`src/OGPass.sol:175`

```
        if (balanceOf(msg.sender) != 0) revert AlreadyMember();
```

claimFounder rejects any caller whose ERC-721 balance is non-zero. Public buys are open from deployment while founder claims need an off-chain proof, so a founder who buys a public pass first is told AlreadyMember and the only way back is sell(), which pays 92.5% of P(publicSupply) and burns 7.5% (75,000 OG at publicSupply 1, more at higher supply). There is no path to claim while holding or to convert a public pass into a founder pass, and the 30-day deadline makes the lockout irreversible if missed. This follows the stated one-pass-per-wallet rule and is a design consequence, not a bypass; it is reported because the brief says founders claim free and neither the brief nor the README calls out this cost. Merged from audit_permissions and audit_math. Minimal fix preserving one-per-wallet: in claimFounder, if the caller holds exactly one public pass, burn it with the normal sell accounting inside the claim, or distribute proofs before buys open and document the fee in the claim instructions.

**Reproduction**

State: founder F is a leaf of founderRoot, publicSupply == 0, F holds 10_000_000e18 OG approved to the pass. F calls buy(1_000_000e18, block.timestamp): succeeds, F owns token 1, balance 9_000_000e18. F calls claimFounder(validProof): reverts AlreadyMember(). F calls sell(1, 0, block.timestamp): receives 925_000e18 (balance 9_925_000e18), 75_000e18 goes to 0xdEaD. F calls claimFounder(validProof): now succeeds. Expected per the brief: the founder claim costs nothing. Actual: it cost 75_000e18 OG, and if the sell happens at or after claimDeadline the claim is forfeited. Reproduced with test/scratch/Judge.t.sol::test_founderHoldingPublicPassMustSellToClaim.

### 3. Info: Trust assumption: owner can make the buy pause permanent by renouncing ownership while paused

`src/OGPass.sol:288`

```
    function setBuysPaused(bool paused) external onlyOwner {
```

Owner powers are confirmed to be exactly setBaseURI and setBuysPaused plus Ownable2Step transfer/renounce; the owner cannot move OG, change prices, the root, the deadline, or mint. The one material edge: the pause has no expiry and renounceOwnership is a single step inherited unchanged, so the owner (0x5b95A971B4583A5f011E9DA082acdD679b870D06 on mainnet, confirmed via owner() at block 26175235) can call setBuysPaused(true) then renounceOwnership(), after which nobody can ever set buysPaused back to false. The same freeze results from losing the owner key while paused. Sells, founder claims, sellFounder, fundFounderReserve and burnUnclaimedFounderReserve keep working, so no funds are trapped and the curve unwinds to zero; only new entry is closed. Reported as a trust assumption, not a defect, as the brief lists the pause as an intended owner power. Merged from audit_flow, audit_permissions, audit_math and audit_economics. Optional hardening that keeps the design: override renounceOwnership to revert while buysPaused is true (or clear the pause first), or give the pause a maximum duration.

**Reproduction**

State: fresh deployment, buysPaused == false. Owner calls setBuysPaused(true), then renounceOwnership(); owner() == address(0). Any wallet with OG approved calls buy(type(uint256).max, block.timestamp): reverts BuysPaused(). Former owner calls setBuysPaused(false): reverts OwnableUnauthorizedAccount. A holder calling sell(tokenId, 0, block.timestamp) still receives 925_000e18 and publicSupply decrements. Expected if the pause is an emergency measure: buys can be resumed by a privileged party. Actual: irreversible. Reproduced with test/scratch/Judge.t.sol::test_pauseThenRenounceIsPermanent and by the existing test/OGPassAdversarial.t.sol::test_renouncedOwnerFreezesPauseStateButNeverExits.

### 4. Info: 1,000-pass cap is unreachable: 951 public passes need 5.47B OG against a fixed 1B OG total supply

`src/OGPass.sol:41`

```
    uint256 public constant MAX_SUPPLY = 1000;
```

curveReserve must hold the sum of P(i) for i = 1..publicSupply. Filling the 951 public slots needs 5,468,250,000 OG. The OG token at 0xCe7EB1Ad9e2E1c784ea05F7eA4A0Fe625923D10A is a fixed-supply contract (verified source on Sourcify, totalSupply is a constant 1,000,000,000e18; read on 2026-10-12 at block 26175235, with 52,689,865 OG already at 0xdEaD and 5,900,000 OG inside the pass). Even if every OG in existence were deposited into the curve, publicSupply cannot exceed 358 (cumulative 997,030,000 OG; the 359th pass at 4,580,000 OG exceeds 1B). The SupplyCapReached branch and the 951 figure in the README and brief therefore describe a state the system cannot enter, and the realistic price range is P(1)..P(~350). Not exploitable; accounting stays exact at every reachable supply. The requester should decide whether to lower BASE_PRICE/PRICE_STEP, lower MAX_SUPPLY, or accept that the cap is nominal.

**Reproduction**

Compute sum_{n=1}^{951} priceOf(n) = 5_468_250_000e18 and compare with OG.totalSupply() = 1_000_000_000e18; sum_{n=1}^{358} priceOf(n) = 997_030_000e18 <= 1e27 and adding priceOf(359) = 4_580_000e18 exceeds it. State: publicSupply == 358 with every OG token already inside the contract; the next buy must _pullExact(buyer, 4_580_000e18) and no address can hold it, so publicSupply == 359 is unreachable, let alone 951. Expected: the documented 951 public passes are attainable. Actual: unreachable by a factor of about 5.5 in total cost. Checked in test/scratch/Judge.t.sol::test_capUnreachable.

### 5. Info: Open item: deployed founder root cannot be verified from the repository; a mis-encoded root strands the funded 4.9M OG reserve

`src/OGPass.sol:176`

```
        bytes32 leaf = keccak256(bytes.concat(keccak256(abi.encode(msg.sender))));
```

claimFounder hashes the caller as the OpenZeppelin StandardMerkleTree leaf (double keccak of abi.encode(address)) and verifies against the immutable founderRoot. Only the root 0xb9c8ed16...dc6c8 is in the tree; nothing in code, tests or script can confirm it was built with this encoding and sorted-pair hashing over the 49 intended addresses. The live contract (read at block 26175235) holds founderReserve = 4,900,000 OG with founderClaimed = 0, has no withdrawal function, and burnUnclaimedFounderReserve is permissionless from claimDeadline (1794344615). If the root does not verify for the founders under this encoding, every claim reverts InvalidProof for 30 days, the 49 slots open to the public, and anyone can burn the whole reserve. The code behaves as specified in that scenario; the risk is an unverifiable deployment input with an irreversible outcome, and it is not confirmed (the root may well be correct). Kept from audit_economics as an open item, not a code defect. Mitigation: dry-run one founder proof with eth_call against claimFounder before relying on the window; for future deployments add a deploy-time or test check of one known leaf against the root.

**Reproduction**

State: deploy OGPass with founderRoot = sortedPairHash(keccak256(abi.encodePacked(f0)), keccak256(abi.encodePacked(f1))) (single-hash leaves, a common allowlist encoding), founderCount = 2; donor funds 200_000e18 via fundFounderReserve. f0 calls claimFounder([keccak256(abi.encodePacked(f1))]), a proof MerkleProof.verify accepts for the single-hash leaf. Expected (requester intent): f0 receives a founder pass. Actual: revert InvalidProof because the contract hashes keccak256(bytes.concat(keccak256(abi.encode(f0)))). At block.timestamp == claimDeadline anyone calls burnUnclaimedFounderReserve(): returns 200_000e18, founderReserve == 0. Reproduced with test/scratch/Judge.t.sol::test_wrongLeafEncodingStrandsReserve. The first successful claimFounder on mainnet would close this item; founderClaimed was 0 at block 26175235.

---

Judge's submission `f308601aa9fc92d16858f72e7ce3febed595cf2c982715f181e27aa2e41923c7`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
