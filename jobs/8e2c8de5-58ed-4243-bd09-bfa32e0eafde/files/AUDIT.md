# Audit report

> # BMC ILLUMINATI — PRE-MAINNET SECURITY AUDIT
> ## Existing Staking Contract #1357
>
> **TASK: Independent smart contract security audit and real NFT integration verification.**
>
> ### Project repositories
>
> STAKING — Main repository:
> https://github.com/0xSt3w/launch-1357-project-bmc-illuminati
>
> NFT COLLECTION — BMC PASS:
> https://github.com/0xSt3w/launch-1356-project-bmc-illuminati-pass
>
> BMC ERC-20 — Ethereum Mainnet:
> 0x38224239f2BDae357D47cb864BC533d7f72dF961
>
> ### Current development status
>
> - Staking: 81 Foundry tests passed, 0 failed.
> - NFT collection: 43 Foundry tests previously passed.
> - Real NFT source integration test passed for Genesis #1 and #2.
> - No staking deployment has been authorized.
> - NFT Mystery reveal integration requires additional testing.
>
> These results are developer tests, not an independent security certification.
>
> ### Audit scope
>
> **1. BMC Token Staking**
>
> Review deposit and withdrawal accounting, principal protection, token transfer fees, balance-delta checks, rounding, reward accrual, insolvency scenarios and reentrancy.
>
> Verify that users can recover their deposited principal without depending on treasury operations or reward-reserve solvency.
>
> **2. BMC PASS NFT Staking**
>
> Review NFT custody, ERC-721 receiver callbacks, owner verification, duplicate staking prevention, metadata assumptions, withdrawals and reward weighting.
>
> Verify these exact NFT tiers and weights:
>
> - Legendary Genesis #1: 5x
> - Early-minted Genesis #2–40: 3x
> - Revealed Mystery Genesis: 2x
> - Revealed Standard: 1x
> - Pending NFT: not eligible
>
> The actual NFT contract uses Pending, LegendaryGenesis, Genesis and Standard. Do not introduce incompatible enum values.
>
> **3. Combined BMC + PASS Staking**
>
> Audit the 20% linked-exposure bonus, minimum BMC requirement, per-NFT weight caps, deposit order, withdrawals, transfers and prevention of double counting.
>
> Verify that the bonus is a relative reward weight, not a guaranteed APY.
>
> **4. Reward Funding and Treasury**
>
> Review the existing 55% token / 25% NFT / 15% combined bonus / 5% reserve allocation.
>
> Verify prefunding, reward liabilities, reward claims, treasury recovery, end-of-program settlement, rounding dust and preservation of unclaimed rewards.
>
> Review multisig authentication and all privileged functions.
>
> **5. Real BMC PASS Integration**
>
> Use the actual BMCIlluminatiPass.sol contract, not only MockPass.
>
> Extend integration tests to cover:
> - Genesis #1 and #2.
> - All 40 sequential Genesis NFTs.
> - Pending Mystery NFTs rejected by staking.
> - Chainlink VRF v2.5 fulfillment.
> - Revealed Mystery Genesis and Standard.
> - In-order reveal finalization.
> - NFT staking and safe withdrawal after reveal.
> - Reward weights and accounting across all tiers.
>
> Use the actual Chainlink coordinator mock where possible.
>
> **6. Mainnet Fork Verification**
>
> Use an Ethereum Mainnet fork to verify compatibility with the actual BMC token, without broadcasting transactions or transferring real assets.
>
> Report limitations where live behavior cannot be exercised.
>
> **7. Security and Invariants**
>
> Review:
> - Reentrancy and external calls.
> - ERC-20 and ERC-721 custody.
> - Reward pool solvency.
> - Arithmetic bounds.
> - Access control.
> - Malicious NFT contracts.
> - Unsupported ERC-20 behavior.
> - Emergency withdrawals.
> - Denial of service.
> - Time manipulation assumptions.
> - Permanent program termination.
> - Authenticity checks for the configured NFT collection.
>
> Run Foundry unit tests, fuzz tests and invariant tests.
>
> ### Deliverables
>
> Provide:
> 1. Independent audit report with Critical, High, Medium, Low and Informational findings.
> 2. Reproduction steps or proof-of-concept tests for significant findings.
> 3. Exact file and line references.
> 4. Recommended remediations.
> 5. Remaining mainnet deployment blockers.
> 6. Results of actual NFT integration tests.
> 7. GitHub pull request for proposed fixes, if needed.
> 8. Retest results after remediation.
>
> Do not silently modify economic rules, staking weights, NFT supply or minting prices.
>
> ### Strict execution restrictions
>
> DO NOT deploy contracts.
>
> DO NOT broadcast transactions.
>
> DO NOT request wallet private keys or seed phrases.
>
> DO NOT request real BMC approvals.
>
> DO NOT transfer or burn real BMC.
>
> DO NOT fund any staking pool.
>
> DO NOT merge pull requests automatically.
>
> **FIRST ACTION: Perform the free IMD feasibility/security check and display the complete audit price before requesting payment.**
>
> Wait for explicit approval before any paid audit or on-chain action.

| | |
|---|---|
| Repository | https://github.com/0xSt3w/launch-1357-project-bmc-illuminati.git |
| Commit | `2eebb2a84e3913197de16d15c2b916378f932029` |
| Job | `8e2c8de5-58ed-4243-bd09-bfa32e0eafde` |
| Judged | 2026-10-12 06:59 UTC |
| Findings | 1 medium · 3 low · 4 info |

Four agents audited the code as it is at `2eebb2a`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Medium: Strict mint-order reveal finalization with no re-request path: one expired VRF request permanently leaves every later mystery NFT Pending and ineligible for staking

`integration/contracts/BMCIlluminatiPass.sol:321`

```
while (done < maxCount && tokenId <= totalMinted && _revealStatus[tokenId] == RevealStatus.RandomnessStored) {
```

finalizeReveals() starts at token GENESIS_PHASE_SUPPLY + revealedCount + 1 and stops at the first token whose status is not RandomnessStored; rawFulfillRandomWords() (line 312) only stores the word and then calls the same strictly ordered routine. A token whose own randomness has been delivered therefore stays Tier.Pending (artworkIdOf == 0) for as long as any lower-numbered mystery token's request is unfulfilled, and BMCStaking.nftWeight()/stakeNFT() (src/BMCStaking.sol:434-437) reject it with PendingReveal. The contract header (lines 36-39) justifies the absence of any reroll/re-request by claiming 'Chainlink VRF v2.5 requests remain pending while the subscription is unfunded and are fulfilled once it is funded again'. That is incorrect: the Chainlink VRF v2.5 subscription documentation (docs.chain.link/vrf/v2-5/overview/subscription, 'Minimum subscription balance', checked 2026-10-12) states 'If your balance is below the minimum, your requests remain pending for up to 24 hours before they expire' and that refunding only processes pending requests 'as long as they have not expired'. A single 24-hour funding lapse during a mint window, or an owner setVRFConfig pointing future mints at a subscription that is not kept funded, produces a request that will never be fulfilled, and the contract has no re-request, skip or owner recovery path. Consequence: that token and every token minted after it (up to 459) stay Pending forever with no final metadata and no staking eligibility, even though their holders each burned 350,000 BMC; the staking program's 25% NFT budget and 15% bonus budget are then shared only by Genesis #1-40 and tokens revealed before the gap, and the idle emission flows back to the treasury via recoverUnallocated. The staking contract itself behaves correctly (pending tokens must be rejected); the defect is in the collection's fairness mechanism converting a single dependency failure into a collection-wide, permanent denial. Merged from audit_permissions and audit_economics (same mechanism, same line). Remediation (design decision for the requester, must be re-reviewed before the collection is bound): (1) finalize in order of randomness delivery rather than mint order (the draw already hashes tokenId with the word, so the outcome is still unpredictable at mint time), or (2) add a bounded recovery such as a permissionless re-request for a token whose request has been AwaitingRandomness longer than a fixed window (store the new requestId, leave the old one unmapped), or (3) at minimum correct the header comment and document the subscription-funding SLA in DEPLOYMENT.md as a launch requirement.

**Reproduction**

Reproduced in test/scratch/RealPassRepro.t.sol::testStuckPredecessorBlocksLaterRevealsAndStaking with a minimal coordinator stub (returns sequential request ids; fulfill() calls rawFulfillRandomWords). Setup: real BMCIlluminatiPass with CID and VRF config set, 40 Genesis minted; BMCStaking configured, funded (1,000,000 BMC) and activated with the pass bound. Steps: alice mintMystery() -> token 41 / request 1; bob mintMystery() -> token 42 / request 2; coordinator fulfils ONLY request 2 (word 0xBEEF). State: revealStatusOf(42) == RandomnessStored. finalizeReveals(10) returns 0; tierOf(42) == Pending; artworkIdOf(42) == 0; after warping 200 days finalizeReveals(10) still returns 0. bob approves and calls staking.stakeNFT(42): reverts PendingReveal(). bob mints 43, request 3 is fulfilled, finalizeReveals(10) returns 0 and pendingReveals() == 3. Expected from a holder's view: a token whose own randomness was delivered becomes revealed and stakeable, or some recovery route exists. Actual: blocked indefinitely by token 41; only delivering request 1 (which Chainlink will not do after 24h expiry) unblocks it, after which all three finalize in order.

### 2. Low: configureCollection binds any ERC-721 that exposes totalSupply(); a wrong-ABI collection is bound irrevocably and all NFT staking fails after funds are committed

`src/BMCStaking.sol:199`

```
try IBMCIlluminatiPass(collection_).totalSupply()
```

configureCollection is the one-shot binding of the collection (line 182 rejects any second call) and is the only on-chain guard between the treasury's address choice and the NFT + combined-bonus program (40% of funding). Its validation checks only ERC-165 support for IERC721 and that totalSupply() returns <= 500. It never probes tierOf(uint256) or artworkIdOf(uint256), the two selectors nftWeight() actually depends on (lines 429-432), so any plain ERC-721 with a totalSupply() getter passes. Because fundRewards()/activate() require the collection to be set first (_requireConfigured), a mistake is discovered only after funding is irrevocably committed and there is no rebind path: every stakeNFT() reverts for the program's lifetime, the NFT and bonus budgets emit idle, and the only exit is recoverUnallocated after the program ends. docs/DEPLOYMENT.md line 26 tells the operator to 'Check ERC165 support for both ERC721 and the custom interface ID generated from the final reviewed ABI', but the contract performs no such check and the real pass registers no custom interface id, so the procedure and the code disagree about where the protection lives. Actor is the treasury making a configuration error, not an attacker; reported under the brief's 'Authenticity checks for the configured NFT collection' item. Remediation: in configureCollection additionally static-call tierOf(1) and artworkIdOf(1) inside try/catch and require that each either returns or reverts with the collection's NonexistentToken error (not a missing-selector failure), or require supportsInterface(type(IBMCIlluminatiPass).interfaceId) if the pass is changed to advertise it; and align DEPLOYMENT.md step 4 with whatever the code checks.

**Reproduction**

Reproduced in test/scratch/StakingEdgesRepro.t.sol::testPlainERC721WithTotalSupplyIsAcceptedAndBoundForever. Setup: BMCStaking with a 3-owner/threshold-2 treasury; PlainEnumerableNFT = OpenZeppelin ERC721 plus a public uint256 totalSupply (no tierOf/artworkIdOf); mint token 1 to bob. Steps: treasury calls configureProgram(365 days, 100e18, 500e18) then configureCollection(plain, keccak256('mistaken review')). Expected: InvalidConfiguration (collection lacks the integration ABI). Actual: succeeds and collection() == plain. Then configureCollection(mockPass, ...) reverts InvalidConfiguration (one-shot), fundRewards(1_000_000e18) and activate() succeed, and bob's stakeNFT(1) and nftWeight(1) both revert on the missing tierOf selector.

### 3. Low: Real BMC PASS integration test uses a codeless VRF coordinator, so mystery mint, VRF fulfilment, in-order reveal, Pending rejection and revealed-tier staking are untested against the real collection

`test/RealBMCPassIntegration.t.sol:42`

```
address(0x1234)
```

The only test that uses the actual BMCIlluminatiPass.sol constructs it with address(0x1234) as the Chainlink VRF v2.5 coordinator. That address has no code, so mintMystery() always reverts (requestRandomWords returns no data and ABI decoding of the uint256 fails). lib/chainlink contains only IVRFCoordinatorV2Plus, IVRFSubscriptionV2Plus and VRFV2PlusClient, no coordinator mock, and DEPENDENCIES.md does not list the chainlink files. Consequently brief items 5.b-5.h (all 40 Genesis, Pending mystery rejected by staking, VRF fulfilment, revealed Mystery Genesis 2x and Standard 1x, in-order finalization, stake/withdraw after reveal, cross-tier accounting) are exercised only through MockPass, whose tierOf/artworkIdOf are set directly and whose artwork formula differs from the real Fisher-Yates draw. The '81 passed' result therefore says nothing about tokens 41-500 against the real contract. Merged from audit_math, audit_economics and audit_flow. Independent extension performed for this review with a minimal coordinator stand-in confirms the staking code is correct against the real pass: configureCollection accepts supply 500; nftWeight(1)==5, nftWeight(2..40)==3; nftWeight(41..500) and stakeNFT(41) revert PendingReveal while pending; after fulfilling all 460 requests and finalizing, exactly 37 Genesis outcomes (artwork 41..77, weight 2) and 423 Standard outcomes (artwork 1..423, weight 1); staking all 500 gives NFT pool weight 619 (5+117+74+423); after 365 days the sole staker's NFT pending is 250,000e18 within 1 unit; all 500 withdraw to a third party. Remediation: vendor a coordinator mock (Chainlink's VRFCoordinatorV2_5Mock, or a minimal stand-in under test/mocks) as ordinary files, list it in DEPENDENCIES.md, and port the above cases into test/RealBMCPassIntegration.t.sol; keep the existing #1/#2 test.

**Reproduction**

Reproduced in test/scratch/RealPassRepro.t.sol::testCodelessCoordinatorCannotMintMystery: with the committed fixture (pass = new BMCIlluminatiPass(address(this), BMC_ADDRESS, address(0x1234))), after 40 mintGenesis() calls and pass.setVRFConfig(1, bytes32(uint256(1)), 500000, 3, false), alice's pass.mintMystery() reverts (address(0x1234).code.length == 0). Expected for an integration suite: a pending token 41 whose fulfilment, in-order reveal and staking can be driven. Actual: unreachable in the committed fixture; forge test --match-path test/RealBMCPassIntegration.t.sol exercises only tokens #1 and #2. The positive coverage described above is in testFullSellOutTierCountsAndWeights of the same scratch file and passes on current code.

### 4. Low: docs/INTERFACE.md, README.md and DEPLOYMENT.md publish an NFT ABI and Tier encoding (isArtworkAssigned, 5-value enum, custom ERC165 id) that contradict the shipped interface and the real pass

`docs/INTERFACE.md:55`

```
// Tier ABI encoding (uint8): Pending=0, Standard=1, RandomGenesis=2,
```

docs/INTERFACE.md lines 50-59 ('Proposed NFT integration ABI') tell UI and integration authors that the collection exposes isArtworkAssigned(uint256) returns (bool) behind a custom ERC165 interface id and encodes tiers as Pending=0, Standard=1, RandomGenesis=2, EarlyGenesis=3, LegendaryGenesis=4. The compiled src/interfaces/IBMCIlluminatiPass.sol (lines 8-13, 20-23) and the real integration/contracts/BMCIlluminatiPass.sol (lines 47-52, 376) use enum Tier { Pending=0, LegendaryGenesis=1, Genesis=2, Standard=3 } and artworkIdOf(uint256) returns (uint16) (0 while pending); isArtworkAssigned does not exist in src/ or integration/ (grep: no hits), and the real pass registers only the OpenZeppelin ERC721/ERC721Metadata ERC165 ids. README.md lines 51-52 ('collection-reported Early tier', 'Random Genesis tier') and line 102 (isArtworkAssigned), and docs/DEPLOYMENT.md line 26 (check 'the custom interface ID generated from the final reviewed ABI') repeat the stale ABI. The brief explicitly says the real collection uses Pending, LegendaryGenesis, Genesis and Standard and that incompatible enum values must not be introduced: the code complies, the published documents do not. A front end or indexer built from INTERFACE.md decodes tierOf()==1 as 'Standard' (actually LegendaryGenesis, weight 5) and calls a selector that reverts; the DEPLOYMENT.md step-4 check can never be satisfied against the real collection. Merged from audit_permissions, audit_economics and audit_flow. Remediation: rewrite INTERFACE.md lines 53-59 and README.md lines 48-55 and 102 to the shipped ABI (tierOf with Pending=0, LegendaryGenesis=1, Genesis=2, Standard=3; artworkIdOf(uint256) returns (uint16), 0 = pending; totalSupply), drop isArtworkAssigned and the custom-interface-id requirement, and state in DEPLOYMENT.md step 4 exactly which on-chain checks configureCollection performs. No staking code change.

**Reproduction**

Compare docs/INTERFACE.md lines 53-56 with src/interfaces/IBMCIlluminatiPass.sol lines 8-23: documented uint8(Tier.LegendaryGenesis)==4 vs actual 1; documented Standard==1 vs actual 3. grep -n isArtworkAssigned src/ integration/ returns nothing. Against the real pass (test/scratch/RealPassRepro.t.sol fixture) tierOf(1) returns 1 and staking.nftWeight(1) returns 5, i.e. the shipped meaning of 1 is LegendaryGenesis, not the documented Standard; a call to isArtworkAssigned(1) reverts because the selector does not exist. Expected: documentation matches forge inspect IBMCIlluminatiPass abi. Actual: three documents describe a different ABI.

### 5. Info: Bonus weight floors to zero for an eligible account when linked exposure is below 5 raw units (reachable only with a sub-5-unit minimumBMC)

`src/BMCStaking.sol:574`

```
next = Math.mulDiv(linked, BONUS_BPS, 10_000);
```

_refreshBonus treats an account as eligible when a.principal >= minimumBMC && a.nftWeight != 0, but the bonus weight is floor(linked * 2000 / 10000) = floor(linked / 5). configureProgram (line 161) only requires minimumBMC_ != 0, so a minimum of 1..4 raw units is accepted; an account that meets the minimum with principal 1..4 and holds a staked NFT is 'eligible' yet gets bonusWeight 0 and earns nothing from the bonus pool, while a 5-unit account earns bonus weight 1. With 18-decimal BMC and any realistic minimum (100e18 gives 20e18) this is unreachable, so impact is nil in the intended configuration; it is a configuration boundary where the eligibility predicate and the weight formula disagree. Fix: in configureProgram require minimumBMC_ >= 10_000 / BONUS_BPS (5) so eligibility implies a non-zero bonus weight, or document the floor.

**Reproduction**

Reproduced in test/scratch/StakingEdgesRepro.t.sol::testBonusTruncatesToZeroAtTinyMinimum. Inputs: treasury.configureProgram(365 days, 1, 500e18); configureCollection(MockPass); fund 1,000,000e18; activate. alice: stakeBMC(4, 0); mint PASS #1 (LegendaryGenesis) to alice and stakeNFT(1). Expected: alice meets the configured minimum (4 >= 1) and holds NFT weight 5, so a non-zero bonus weight. Actual: accounts(alice).bonusWeight == 0 and pools[2].totalWeight == 0; after stakeBMC(1, 0) (principal 5) bonusWeight becomes 1.

### 6. Info: withdrawNFT to a recipient whose code (e.g. an EIP-7702-delegated EOA) lacks onERC721Received reverts; staker must choose another recipient

`src/BMCStaking.sol:325`

```
collection.safeTransferFrom(address(this), recipient, tokenId);
```

withdrawNFT uses safeTransferFrom, which invokes onERC721Received on any recipient with code. Since Pectra a mainnet EOA can carry a 23-byte EIP-7702 delegation designator, so 'my own wallet address' may have code; if the delegate does not implement the hook, OpenZeppelin ERC721 reverts with ERC721InvalidReceiver(recipient). The staker is not locked out: withdrawNFT accepts any recipient != 0 and != staking, so they can withdraw to another address or clear the delegation. This is standard ERC-721 behaviour and not an accounting defect; it is recorded because the brief asks about emergency withdrawals and the committed tests model only a reverting contract receiver, not a delegated EOA. Fix (optional, no economic change): document in INTERFACE.md that recipients with code must implement IERC721Receiver and that 7702-delegated wallets may need a plain recipient; do not switch to transferFrom, which would let NFTs be lost to non-receiver contracts.

**Reproduction**

Reproduced in test/scratch/StakingEdgesRepro.t.sol::testWithdrawNFTToCodeBearingRecipientWithoutHookReverts. State: program active; alice stakes PASS #1; advance one block; recipient address 'delegated' is etched with 0xef0100 || address(MockTreasury) (a 7702 designator pointing at a contract without onERC721Received). Input: alice calls withdrawNFT(1, delegated). Expected by a user: NFT returned to their EOA. Actual: revert ERC721InvalidReceiver(delegated); the position remains intact and withdrawNFT(1, bob) then succeeds with ownerOf(1) == bob. The audit_math specialist observed the same on a mainnet fork at block 26174679 with the makeAddr('alice') address, which carries a live 7702 designator.

### 7. Info: Any external principal deficit, even 1 wei, blocks every principal withdrawal until the shortfall is donated back; there is no partial or pro-rata exit

`src/BMCStaking.sol:608`

```
if (afterBalance < totalPrincipal) revert Insolvent();
```

withdrawBMC reduces totalPrincipal by the gross amount before _sendBMC, and _sendBMC then requires the post-transfer balance to cover the remaining totalPrincipal. With balance B and principal P, a withdrawal of x leaves B-x which must be >= P-x; this holds only when B >= P. So once the contract's BMC balance is below total principal by any amount, every withdrawBMC call of every size reverts Insolvent, including withdrawals far smaller than the available balance; claim and new stakes also stop via _assertSolvent. The precondition is reachable only through behaviour outside the contract (token-level confiscation, supply reduction or a future upgrade of BMC), since every in-contract path checks exact debits, and docs/SECURITY_REVIEW.md and README.md 'Fees and solvency' describe the rule as deliberate (no first-withdrawer priority over unbacked principal). The live BMC token is a plain burnable ERC-20 per docs/checks/bmc-mainnet-read.json, so this is not reachable today. Recorded so the requester explicitly accepts the all-or-nothing behaviour and the recovery route (anyone transferring the shortfall to the contract unfreezes all exits) before launch. If pro-rata exits are wanted the fix is a design change (cap each withdrawal at principal * balance / totalPrincipal when B < P); otherwise document the exact rule in INTERFACE.md so the UI can explain it.

**Reproduction**

Reproduced in test/scratch/StakingEdgesRepro.t.sol::testOneWeiDeficitBlocksEveryPrincipalWithdrawal. State: program active (funded 1,000,000e18), alice and bob each stakeBMC(100 ether); one block later token.burn(address(staking), 1_000_000 ether + 1) removes the whole reward reserve plus 1 wei of principal, so balance == 200 ether - 1 and totalPrincipal == 200 ether. Input: alice calls withdrawBMC(100 ether, 0) then withdrawBMC(1, 0). Expected by a reader of README 'principal withdrawals remain possible while the full remaining principal is backed': at least the 199.99… ether present can be withdrawn. Actual: both calls revert Insolvent(). After any party transfers 1 wei to the contract, alice and bob both withdraw their full 100 ether.

### 8. Info: Bonus pool is a fixed 15% budget split by weight, so a minimum-size combined position can capture far more than 20% of its base reward; confirm this economic interpretation is accepted

`src/BMCStaking.sol:574`

```
next = Math.mulDiv(linked, BONUS_BPS, 10_000);
```

Verified as the brief requested: the 20% figure (BONUS_BPS) caps bonus weight (min(principal, nftWeight*linkedBMCPerWeight) * 20%), not payout, and nothing in the contract promises an APY. The consequence that needs explicit sign-off is that the bonus pool has its own denominator (pools[2].totalWeight), so the realised bonus is unbounded relative to the base reward when combined participation is low. Any holder of one Standard pass who stakes exactly minimumBMC gets bonus weight minimumBMC*20% and, if the only eligible account, the entire 15% budget. README 'Combined bonus rules' (line 69) documents this and itself asks for acceptance in independent review; docs/INTERFACE.md UI flow step 3 already says bonus weight is not a payout ratio. No code defect. If a payout-relative cap is intended instead, the design must change (e.g. cap bonus accrual at 20% of the account's token-pool accrual and route the excess to idle emissions), which is a requester scope decision and must not be made silently.

**Reproduction**

Reproduced in test/scratch/BonusEconRepro.t.sol::testMinimumCombinedPositionCapturesWholeBonusBudget on the StakingFixture parameters (1,000,000 BMC funded, minimumBMC 100 BMC, linkedBMCPerWeight 500 BMC): alice stakes 100 BMC and Standard NFT #41 (bonusWeight == 20e18); bob stakes 1,000,000 BMC with no NFT; advance 365 days. Observed pendingRewards(alice) = [54.99 BMC token, 250,000 BMC NFT, 150,000 BMC bonus]; pendingRewards(bob)[0] = 549,945 BMC. Expected by a reader of '20% bonus': alice's bonus near 20% of her 55 BMC base reward. Actual: her bonus is the whole 15% budget, about 2,700x her base reward, because she is the only account with bonus weight.

---

Judge's submission `04bac612998eede215e7003f708b21fb9350eb44fc296abaf1b9dc5f78fab0d0`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
