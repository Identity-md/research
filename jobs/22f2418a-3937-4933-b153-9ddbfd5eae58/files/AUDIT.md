# Audit report

> Audit the SigilNFT contract in this repository (src/SigilNFT.sol, 142 lines, Solidity 0.8.26, OpenZeppelin v5 submodule lib/openzeppelin-contracts at fcbae5394ae8ad52d8e580a3477db99814b9d565, forge-std at bf647bd6046f2f7da30d0c2bf435e5c76a780c1b). It is the "Illuminati.Earth Magik Sigil" ERC-721 collection (name constant "Illuminati.Earth Magik Sigil" in script/DeploySigilNFT.s.sol; confirm the README, deploy script, tests and integration guide all use exactly that name), intended for a real Base mainnet deploy: 2,300 max supply, free mint (gas only), fixed 10% EIP-2981 royalty to a treasury set once at deploy, mint and rework gated by EIP-712 vouchers signed by an owner-rotatable signer. Write nothing to the repository; deliver report.md. REPORT BRANDING: this review is published as part of Illuminati.Earth marketing. Title report.md "Illuminati.Earth Magik Sigil: Contract Review" and call the collection "Illuminati.Earth Magik Sigil" (exactly that spelling and capitalisation) everywhere in the report. Keep the tone factual and plain: no hype, no claims of safety beyond the evidence, no investment language, and no statement that the contract is "audited" or "secure".
>
> SCOPE: src/SigilNFT.sol, script/DeploySigilNFT.s.sol, test/SigilNFT.t.sol (27 tests), README.md and docs/INTEGRATION.md. Check that the README and integration guide match the code exactly.
>
> HARD QUESTIONS (answer each with a verdict and evidence, a reproducible test where possible):
> 1. Voucher replay and binding: can a mint or rework voucher be redeemed by anyone except the named caller? Across chains, across contract deployments, or after a signer rotation? Is the EIP-712 domain (name "SigilNFT", version "1", chainId, verifyingContract) correct, and are the MINT and REWORK typehashes exactly consistent with the encoded structs, including the dynamic string tokenURI hashed with keccak256(bytes(...))? Any signature malleability or ECDSA edge case (zero address recovery, s-value, 65 vs 64-byte signatures)?
> 2. Supply and sigil mapping: can supply exceed MAX_SUPPLY (2300)? Is the ordering of the _nextTokenId check, the tokenOfSigil check and the writes safe? Can a sigilId be minted twice, or a token be reissued after transfer? Is tokenOfSigil == 0 a safe "unminted" sentinel given token ids start at 1?
> 3. Reentrancy: _safeMint calls onERC721Received on the recipient. State is written before the call; confirm no reentrant path through mint or rework can mint extra supply, reuse a voucher, or corrupt tokenVersion or tokenURI.
> 4. Rework logic: tokenVersion strictly increases; can a version be skipped or reused to brick or hijack a token's metadata? Does the holder-only check (_ownerOf) behave for non-existent tokens? Is MetadataUpdate (ERC-4906) emitted on mint and rework, and does supportsInterface advertise ERC-4906, ERC-2981 and ERC-721 correctly through the multiple-inheritance override?
> 5. Owner and signer powers: confirm owner can only call setSigner, ownership transfer and renounce behave as OpenZeppelin v5 Ownable2-less Ownable (single-step) and the risks that creates; the signer cannot touch tokens it does not hold. State what a compromised signer can and cannot do.
> 6. Royalty: _setDefaultRoyalty(treasury, 1000) with an unchecked treasury argument; what if treasury is the zero address (it reverts in ERC2981, confirm). Any way to change royalty after deploy?
> 7. Deadline and timing: block.timestamp > deadline comparison, voucher expiry edge cases, deadlines near uint256 max.
> 8. Gas and DoS: unbounded strings (tokenURI length), large calldata, any griefing of mint for other users.
> 9. Deploy script and tests: does the deploy script pass the right arguments, does the test suite genuinely cover the risks above, and what is missing?
>
> METHOD: use the Pashov methodology and specialties. Reproduce every finding against the code; discard unreproducible claims. Rate each finding by severity and likelihood, give a concrete fix, and separate real defects from design trade-offs already documented in the README threat model. Do not claim this review is a substitute for an independent human audit.

| | |
|---|---|
| Repository | https://github.com/ToknWrks/magik-sigil-nft.git |
| Commit | `e466fcb14c1c7d53b39b2c01a5dc742dc216a62f` |
| Job | `22f2418a-3937-4933-b153-9ddbfd5eae58` |
| Judged | 2026-10-04 02:15 UTC |
| Findings | 2 low |

Four agents audited the code as it is at `e466fcb`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Low: A maximum voucher version permanently prevents subsequent rework

`src/SigilNFT.sol:113`

```
        if (version <= tokenVersion[tokenId]) revert StaleVersion();
```

Illuminati.Earth Magik Sigil accepts any nonzero uint256 version at mint (lines 83 and 95), and any larger version at rework (lines 113 and 120). A valid voucher can therefore set tokenVersion to 2**256 - 1, leaving no representable version for any later rework. Transfers and signer rotation cannot repair this state. This contradicts the repeatable rework behavior described at README.md lines 23-26 and persists for a subsequent holder; the README threat model discusses changing art before sale but does not disclose irreversible loss of rework capability. Severity: low. Likelihood: low, because the current signer must approve this extreme version and the named holder must submit it. This is a signer-dependent input/liveness defect, not an authorization bypass or a way for the signer alone to alter another holder's token. Fix: require mint version 1 and rework version exactly the current version plus 1, so saturation cannot be reached by an arbitrary jump, and allocate versions in the backend. That fix changes the currently permitted version-jump policy and should be explicit. If arbitrary metadata versions must remain, separate them from an on-chain sequential authorization nonce and define their saturation semantics.

**Reproduction**

Executed with Foundry 1.8.3, Solidity 0.8.26, and the pinned dependencies in /tmp/sigil-judge-tests/Reproductions.t.sol: test_maxMintVersionDisablesReworkAfterTransferAndRotation and test_maxReworkVersionDisablesReworkAfterTransfer. Set chainId=8453 and timestamp=100. Deploy with name Illuminati.Earth Magik Sigil, symbol SIGIL, treasury=address(0x777), signer=vm.addr(42). Using key 42 and domain {name:SigilNFT,version:1,chainId:8453,verifyingContract:address(nft)}, sign Mint(address(0x1111),bytes32(0),first,2**256-1,10000), hashing the URI with keccak256(bytes(uri)); redeem as 0x1111. Transfer token 1 to 0x2222 and rotate the signer to vm.addr(43). Sign Rework(0x2222,1,next,2**256-1,10000) with key 43 and redeem as 0x2222: StaleVersion(). Every other uint256 version is smaller and fails the same guard. tokenVersion stays at the maximum and tokenURI stays first. A second executed test reaches the same terminal state by minting at version 1, applying a valid rework at the maximum, transferring, then attempting another valid maximum-version rework. Expected: a voucher cannot irreversibly eliminate a later holder's rework capability without an explicit freeze feature; actual: both mint and rework can establish this permanent terminal state.

### 2. Low: On-chain version reads do not prevent concurrent rework voucher collisions

`docs/INTEGRATION.md:116`

```
- Use `version` strictly greater than `tokenVersion(tokenId)`. Reading it on-chain avoids collisions
  if a user requests two reworks before the first lands.
```

The Illuminati.Earth Magik Sigil integration guide incorrectly claims that reading tokenVersion on-chain avoids collisions between reworks requested before the first transaction lands. Reads do not reserve a version: concurrent requests can both read 1 and receive valid, distinct version-2 vouchers. Once either is redeemed, the contract correctly rejects the other with StaleVersion(). Severity: low; likelihood: medium where overlapping requests or retries are allowed. Impact is an unusable legitimate voucher, gas expense if a reverting transaction is submitted, and required reissuance. No backend implementation or actual off-chain payment loss was established. This is a documentation/integration defect, not a permission bypass. Fix: describe the race and serialize issuance per token through confirmation or expiry, or atomically reserve pending versions with explicit ordering, supersession, stale-voucher reissuance and reorg handling. Distinct allocated versions alone do not solve out-of-order redemption because a higher version invalidates a lower one. The four specialist reports of this mechanism are merged here.

**Reproduction**

Executed in test_concurrentVersionReadsDoNotReserveVersions in /tmp/sigil-judge-tests/Reproductions.t.sol with Foundry 1.8.3 and Solidity 0.8.26. Set chainId=8453, timestamp=100, treasury=0x777 and signer=vm.addr(42); deploy with name Illuminati.Earth Magik Sigil and symbol SIGIL. Mint sigilId=bytes32(uint256(123)) to Alice=0x1111 with version=1, URI first and deadline=10000. Before either rework is submitted, independently compute versionA=tokenVersion(1)+1 and versionB=tokenVersion(1)+1; both equal 2. Using key 42 and the correct deployed EIP-712 domain, sign Rework(Alice,1,ipfs://request-a,2,10000) and Rework(Alice,1,ipfs://request-b,2,10000). Alice submits A, then B at timestamp 100. Expected according to the quoted guide: the on-chain reads avoid a collision. Actual: A succeeds; B reverts StaleVersion(); tokenVersion(1) remains 2 and tokenURI(1) remains ipfs://request-a.

---

Judge's submission `cba3408a9b46bf241b3e3ff2cac841baaa0acbfbf4b090ed0b89f4acce7f9bd8`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
