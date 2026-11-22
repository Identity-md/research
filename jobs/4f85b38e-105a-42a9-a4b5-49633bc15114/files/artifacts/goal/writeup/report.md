**The `test` Sepolia launch remains incomplete.** The accepted results provide the token and staking contracts, compiled artifacts, tests, a static frontend, and deployment guidance. They do not provide a confirmed Sepolia deployment or a usable published staking application. This report preserves the delivered work and the checks performed for this revision; it does not certify the launch as complete.

The goal’s repository is [identity-md-launches/goal-3351-laucnh-token-sepolia-called](https://github.com/identity-md-launches/goal-3351-laucnh-token-sepolia-called.git). Its merged code wave, `sepolia-core-e3`, reached commit **`46792f58030117937991bc51ee9bde8fad821589`**. All source references below refer to [that exact tree](https://github.com/identity-md-launches/goal-3351-laucnh-token-sepolia-called/tree/46792f58030117937991bc51ee9bde8fad821589). This revision has not changed or published that repository.

| Requested outcome | Evidence available | Status |
| --- | --- | --- |
| Token named `test`, ticker `test`, on Sepolia | Solidity source and matching compiled artifact; local token tests pass | No verified Sepolia address or creation transaction supplied |
| Staking contract awarding points for duration and share | Solidity source and matching compiled artifact; local contract tests and the independent accounting scenario pass | No verified Sepolia address or creation transaction supplied |
| Website for using those contracts | Static frontend source and an accessible, unconfigured third-party preview | No operational staking site; configuration still contains null addresses and frontend defects remain |

**What was built.** `src/TestToken.sol` implements an ownerless ERC-20 with name `test`, symbol `test`, and 18 decimals. Its constructor mints 1,000,000 tokens to the account that actually deploys it. The permissionless `mint(uint256)` faucet mints to its caller and accepts a positive amount up to 1,000 tokens per call. It has no cooldown or lifetime supply cap. The initial supply and faucet are orchestration choices for this testnet demonstration, rather than economics specified by the requester. [R2]

`src/TestStaking.sol` binds its token address immutably at construction. It exposes `stake(uint256)`, `withdraw(uint256)`, `token()`, `totalStaked()`, `stakedOf(address)`, and `pointsOf(address)`. It has no owner, upgrade function, withdrawal lock, or fee. Users approve the staking contract to spend their tokens before staking; withdrawal returns their own deposited tokens and retains their accumulated points. State is settled before stake changes, token calls are checked, and stake/withdraw use a reentrancy guard. The implementation is intended for the supplied token. [R2]

The chosen interpretation of “points on lengths staked based on your share” is **one point per second across the occupied pool**, divided by each account’s share of deposited tokens during that second. For an interval with unchanged balances:

```text
account’s additional points = elapsed seconds × account’s stake / total stake
```

Empty intervals earn nothing. A longer holding earns more at an unchanged share; another account’s deposit changes future shares. Points are stored accounting balances, with `10^18` units per point; the contracts contain no point redemption or reward-token payout. The accumulator uses `10^36` precision and rounds down, so very small shortfalls are possible. [R1, R2]

The static frontend is in `site/`, principally `index.html`, `styles.css`, `lib.js`, and `app.js`. It uses an injected browser wallet and raw JSON-RPC, with no build step or runtime library download. Its intended flow is connect, select Sepolia, mint test tokens, approve and stake, inspect balances/share/points, then withdraw. It validates contract code and the staking contract’s token binding before enabling actions. It does not replace receipt and token-metadata verification during release. `site/deploy.html` and `site/deploy.js` are inert placeholders, not a working deployment wizard. [R3]

**Current publication and deployment evidence.** The committed [site/deployment.json](https://raw.githubusercontent.com/identity-md-launches/goal-3351-laucnh-token-sepolia-called/46792f58030117937991bc51ee9bde8fad821589/site/deployment.json) contains exactly this configuration:

```json
{
  "chainId": 11155111,
  "token": null,
  "staking": null
}
```

Its SHA-256 is `fc87b0e779906109cd06188e07a1921feb3afda3befdb091de2631b3329450ac`. The null values are the explicit undeployed state required by the original code brief; they are not deployable addresses. No result supplied a successful creation receipt, contract address, or deployment transaction hash. Consequently there is no identified Sepolia pair on which to perform the requested live code, metadata, or binding checks.

The [unconfigured frontend preview](https://rawcdn.githack.com/identity-md-launches/goal-3351-laucnh-token-sepolia-called/46792f58030117937991bc51ee9bde8fad821589/site/index.html) is publicly retrievable. On 2026-11-22, curl GETs of `index.html`, `app.js`, `lib.js`, `styles.css`, and `deployment.json` returned HTTP 200, with HTML, JavaScript, CSS, and JSON content types as appropriate. All five response bodies matched the corresponding files at the pinned commit byte for byte. Initial requests through Python’s HTTP client returned 403; reachability was therefore client-dependent in these checks.

This preview serves the original, uncorrected frontend and the null configuration above. Its contract-action buttons remain disabled. The URL identifies a fixed commit on a third-party service; it cannot pick up a later configuration or frontend repair at the same URL. No requester-controlled hosting destination or hosting account was supplied. This preview is useful for inspecting the page, but it does not meet the goal’s operational website requirement.

**Checks performed for this revision.** These are local reproduction results, separate from worker acceptance and from any independent audit or live release verification.

| Check | Result |
| --- | --- |
| Checkout identity | Confirmed commit `46792f58030117937991bc51ee9bde8fad821589` |
| Original contract suite | 43 passed, 0 failed, 0 skipped: 17 token tests and 26 staking tests, including 256 fuzz runs |
| Compiler and artifacts | Used Solidity `0.8.28+commit.7893614a`, optimizer disabled, EVM `prague`; rebuilt creation bytecode, deployed bytecode, and ABI matched both committed artifacts |
| Original site suite, `node site/tests/run.js` | 22 library checks and 15 mocked application scenarios passed; 37 total |
| Independent two-staker fixture from R1 | Executed against the pinned contracts in temporary test scaffolding; all checkpoints passed the documented no-surplus and shortfall bounds |
| Targeted frontend reproduction | Confirmed stale points and pool share without a visitor action, and stale numerical fields after disconnect |
| PublicNode and 1RPC Sepolia RPCs | curl `eth_chainId` requests returned `0xaa36a7`, decoded programmatically to `11155111` |
| Existing frontend RPC, `https://rpc.sepolia.org` | curl `eth_chainId` request returned HTTP 404 with HTML |
| Preview and its configuration | Five assets returned HTTP 200 through curl and matched the pinned source; both deployment addresses remain null |

The initial offline contract command could not find the requested compiler. The check was completed using the published Solidity 0.8.28 executable, verified against the SHA-256 in the official `ethereum/solc-bin` release list, and selecting `prague` explicitly. No application dependency or configuration change was required. With that compiler available, the project’s contract-check command is:

```sh
forge test --offline --use 0.8.28 --evm-version prague --match-path 'test/contracts/*'
node site/tests/run.js
```

The committed artifact metadata also records optimizer `enabled: false`, `runs: 200`, and metadata bytecode hash `ipfs`. Both Solidity source files are self-contained. Source and artifact hashes matched R2:

| File | SHA-256 |
| --- | --- |
| `src/TestToken.sol` | `e241bcc04d7e6f8a90607d07985b15657a5f24c96d83f5a84ba535e8a0ad73e6` |
| `src/TestStaking.sol` | `fa86dc825cbdc73fc6a76c4b727956811872e1d8443946c85d75b7d034b312af` |
| `contract-artifacts/TestToken.json` | `6c72dc9bcf4d23735c103b1aee16cf6ef5d075209964cb004e680fae26822604` |
| `contract-artifacts/TestStaking.json` | `e4f4e7a1a895a4957ca4c7a5891fb3f80d1c551f2c0d6ad8e272c592d8415898` |

**Accounting example and measured rounding.** R1 independently defines this sequence, starting with an empty pool at second zero. Stakes below are whole `test` tokens and the points columns are exact rational expectations, before implementation rounding.

| Second | Action | Alice stake | Bob stake | Alice points | Bob points |
| --- | --- | ---: | ---: | ---: | ---: |
| 0 | Empty baseline | 0 | 0 | 0 | 0 |
| 10 | Alice stakes 30 | 30 | 0 | 0 | 0 |
| 20 | Bob stakes 10 | 30 | 10 | 10 | 0 |
| 32 | Alice withdraws 20 | 10 | 10 | 19 | 3 |
| 42 | Bob withdraws 10 | 10 | 0 | 24 | 8 |
| 52 | Alice withdraws 10 | 0 | 0 | 34 | 8 |
| 60 | Bob stakes 5 | 0 | 5 | 34 | 8 |
| 60 | Alice stakes 10 at the same timestamp | 10 | 5 | 34 | 8 |
| 61 | Read | 10 | 5 | 104/3 | 25/3 |

The pool is occupied for 43 seconds and empty for 18. Its final total stake is 15 tokens. The exact points total is 43. At `10^18` units per point, the individual rational floors are Alice `34666666666666666666` and Bob `8333333333333333333`, summing to `42999999999999999999`. [R1]

The actual contract execution in this revision returned Alice **`34666666666666666665`** and Bob **`8333333333333333333`**, totaling **`42999999999999999998`**. Alice is one base unit below her rational floor; the total is two base units below 43 points. Escrow held exactly 15 tokens. Every checkpoint had no surplus and a per-user shortfall of at most 1,000,000 base units, the bound recorded in the orchestration notes. R1’s assertion that every whole-number checkpoint must be exact is too strong for repeated integer flooring; it is not a condition the implementation was reported to satisfy. The added fixture check was temporary validation scaffolding, not a new file merged into the goal repository.

**Reopened findings.** The substantive release gaps reproduce. None is represented here as a completed on-chain or hosting repair.

- **`5c51b8f3b822b464055aaa8ef30c3eba89119b61c30e8ea4c9191493cd1a1db8` — contracts not launched.** Reproduced by reading the pinned configuration and the accepted contract result, whose `deploymentStatus` is `not_deployed`. The goal history and all supplied results contain no verified token/staking deployment pair. Successful local tests and compiled bytecode do not supply the missing two Sepolia transactions. This remains unresolved.
- **`b4f6b7854e6f7f9f6c27d6b8b41d66b4340aca16e825ed68f320e143f46ad79e` — preview is not the launched staking site.** Reproduced. The curl checks confirm the reviewer’s HTTP 200 and byte-identity observations. The preview has null addresses, uppercase `TEST` branding, and the failed RPC URL. It cannot provide a staking flow in this state. This remains unresolved as a release requirement.
- **`126f6165f08d5b66b7f4c46b63d38e92485b763065ac59d725bf34b1677df71a` — frontend fixes were not applied to the pinned tree.** Reproduced for all four described source defects. `index.html` uses uppercase `TEST`; `app.js` supplies `https://rpc.sepolia.org`; no recurring balance/points refresh is registered; disconnect clears the account label and disables actions but retains the numeric fields. A mock wallet initially displayed `4 TEST`, `1 TEST`, `100.00%`, and `0`. Changing the mock pool total to two tokens and points to twelve left those fields unchanged, with only one `pointsOf` read and no registered refresh timer. Emitting `accountsChanged([])` set the account to `-` but left all four fields visible. The earlier report’s patch is not among the supplied files, and no amended trunk commit exists in the supplied goal state. This report does not claim that a printed patch was applied or shipped.

The response JSON records these as scope disputes, not denials of the observations: the finding-response vocabulary offers no “reproduced but blocked” verdict. The assigned revision can change the report and its required response record; it cannot update the goal’s source tree or supply a funded signer and a requester-controlled host. The launch findings must stay open until an actual release provides the evidence below. Rewriting the report is not a substitute for that release.

**Concrete release handoff.** The following are outstanding actions, not transactions or publication completed by this revision.

1. **Prepare a corrected frontend release.** Integrate lowercase `test` branding throughout the visible site. Replace the dead network-add RPC with `https://ethereum-sepolia-rpc.publicnode.com`; `https://1rpc.io/sepolia` also returned the correct chain ID in the curl check. Add recurring refresh of balances, stake, total stake, and points while connected and validated, for example every 12 seconds. Clear wallet-derived fields and cancel refresh on disconnect or network/account changes; discard in-flight responses for an old account. Exercise these behaviors with the reproduction above, including another staker changing the pool and a disconnect during a pending read. Commit the correction and record the new release commit. The original 37 site checks alone do not cover these defects.
2. **Deploy through a funded Sepolia browser wallet.** Take the two source files and the compiler settings above from the pinned contract release. In [Remix](https://remix.ethereum.org), compile with Solidity 0.8.28, optimizer disabled, and EVM `prague`. Connect the requester’s browser wallet and verify chain ID 11155111. Deploy `TestToken()` with zero native value; record the successful creation receipt and its `contractAddress`. Deploy `TestStaking(address)` with that exact token address and record its successful receipt. The browser-wallet procedure is described by [Remix Deploy & Run](https://remix-ide.readthedocs.io/en/latest/run.html), with compiler controls in [Remix Solidity Compiler](https://remix-ide.readthedocs.io/en/latest/compile.html). [R6]
3. **Verify both deployments.** Require receipt status 1, nonempty `eth_getCode` at both receipt addresses, token `name()` = `test`, `symbol()` = `test`, `decimals()` = 18, and staking `token()` equal to the verified token address. Record the chain ID, creation hashes, receipt addresses, blocks, constructor arguments, checks, and source commit. These reads are documented in the [Ethereum JSON-RPC reference](https://ethereum.org/en/developers/docs/apis/json-rpc/). If token deployment succeeded but staking was interrupted, reuse the confirmed token. Inspect any already-broadcast staking hash before retrying; a pending transaction is not a failed deployment. [R6]
4. **Configure the corrected site.** Populate the three fields in `site/deployment.json`: numeric `chainId` 11155111 and the two receipt-derived, verified addresses. Keep transaction hashes in a separate deployment evidence record. Do not substitute an account address, test fixture address, or unverified contract. Keep actions disabled until configuration and on-chain validation succeed. [R3, R6]
5. **Publish to a requester-controlled HTTPS host.** R5 documents GitHub Pages from a public repository, with `index.html` at the publishing root and relative asset/configuration paths, or Cloudflare Pages Direct Upload. For GitHub Pages, copying the contents of `site/` into a publishing repository’s `/docs` and selecting that folder in Settings → Pages is one documented route. These are future operations on the publishing repository, not edits performed in this task. Use the actual URL issued by the chosen host; no such operational URL is supplied here. [R5]
6. **Check the public release.** Fetch the actual page, scripts, stylesheet, and `deployment.json` over HTTPS; verify their content and that the configuration names the same Sepolia pair as the receipts. Connect a wallet on Sepolia and require `(validated)`. Mint a positive amount no greater than 1,000 tokens, approve and stake, observe points and changing share, withdraw, and confirm that accrued points remain. Check disconnect clearing and automatic updates after another account changes the pool. Retain the deployed source commit, public URL, and transaction evidence with the release.

The missing inputs are a funded, authorized Sepolia signing route and a hosting destination the requester controls, or the successful deployment and publication evidence if those actions have already been performed elsewhere. The orchestration notes record that the goal had no owner-backed launch route or mandate; its initial combined launch-and-site order was refused, and no requester note supplied a replacement. No private key is needed in this report or should be supplied to the writer.

Funding research [R4] documented Alchemy’s faucet with a mainnet-balance/activity eligibility condition and a 0.1 Sepolia ETH daily drip, a browser proof-of-work faucet, and Google Cloud’s faucet. It observed no claim or payout and made no deployment gas estimate. Hosting research [R5] provisioned no account or site; it found account-based durable options and no confirmed durable anonymous option. Its documented anonymous Netlify route required claiming the project within an hour. Those findings do not establish that any account-free deployment/publication route is available for this release.

**Evidence and orchestration record.** `.imd/reads/goal.json` records four settled batches, six accepted items, and one merged code wave. The proposed assembly and independent review waves did not run; their planned deployment wizard and integration sign-off must not be counted as delivered. The results used here are listed by their logical artifact names because the temporary input copies are not part of the source repository.

| Reference | Accepted result | Its one piece of work and delivered evidence |
| --- | --- | --- |
| R1 | `artifacts/goal/batches/accounting-vectors/items/two-stakers/result.json` | One deterministic arithmetic acceptance fixture: ordered events, exact checkpoints, conservation totals, and fixed-point expectations |
| R2 | `artifacts/goal/batches/sepolia-core-e3/items/contracts/result.json` | Contract component: both Solidity sources, self-contained tests, ABI/bytecode artifacts, regeneration script, documentation, test outcomes, hashes, and `not_deployed` status |
| R3 | `artifacts/goal/batches/sepolia-core-e3/items/site/result.json` | Website component: static frontend, deployment configuration, tests, inert deployment-page placeholders, test outcomes, and absent published URL |
| R4 | `artifacts/goal/batches/sepolia-options-e3/items/funding/result.json` | Funding/RPC prerequisite research: public sources, requirements, observed read-only checks, recommendations, and unresolved eligibility/funding |
| R5 | `artifacts/goal/batches/sepolia-options-e3/items/hosting/result.json` | Hosting prerequisite research: documented publication options, requirements, update/rollback guidance, checks, and unresolved publication |
| R6 | `artifacts/goal/batches/sepolia-deploy-guide-e4/items/browser-deployment/result.md` | One browser deployment guide: compile/connect/deploy/resume steps, required receipt and contract checks, and evidence to retain |

The handed result bytes were checked against the supplied SHA-256 values:

```text
R1 a41d5e5952c5ce18fe050b8b45ef33ca5349a946d9845ea5d957fb02a841c9b4
R2 75554380b8071f2fa3a8edc1e80bbf85fe8525fe878026d633b38e1e71f3f6b4
R3 2775f78e3c91bca8438c418b72ae1f6c9e0a5d390559e285c85a90422d492fd4
R4 8eb1885402bffaa2a37dacab158bfacc0ab0530cb2db3c5f4f60553acf6c8809
R5 dc44b92e34e56c5c104adb9e7481e773b8a6569213533cb41690c50288e8a974
R6 9075c79bdce9e0759577c02344a0aa25e5d2541f98e6c91c46ad172e4532d147
```

The useful delivered result is the pinned implementation and the verified handoff above. **Token deployment, staking deployment, correction and publication of the operational website, and verification of that live release remain outstanding.**
