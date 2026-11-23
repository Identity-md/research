# Test (TEST) on Sepolia: token, staking contract and website

Write-up of the goal, 2026-11-23.

The goal asked for a token called Test (ticker TEST) on Sepolia whose launch opens its Uniswap v4 pool, one staking contract where holders stake TEST and earn points in proportion to their share of the total staked, and one website where people can see the token and stake. Two contracts and one website, all on Sepolia.

## 1. Result in brief

All three exist and are live on Sepolia (chain 11155111):

| Asked for | Delivered | Where |
| --- | --- | --- |
| Token Test (TEST) | `LaunchToken`, name `Test`, symbol `TEST`, 18 decimals, fixed supply 1,000,000,000 | `0xc5485f4136ab7fd5d427442fa9658f9d93afd607` |
| Its Uniswap v4 pool, opened by the launch | TEST/ETH pool, initialized and funded with about 800,000,000 TEST in the launch transaction | pool ID `0x39c40a15a18ec0f3c3d5c4e1606b503293d7de601c65bef876f466ff4fa72d21` |
| Staking contract with proportional points | `TestStaking`, bound to that token, 1 point per second shared by all stakers | `0xba90e29755f7efde50796e92cf243a6471188c01` |
| Website to see the token and stake | Published static site, bound to those two addresses | https://test-bcf3.imd.site (ENS `test-bcf3.identitymd.eth`) |

Everything on chain came from one transaction, `0x711e61c123a139e197c89fa3decdbbbc8a4c50e299ab3f4568d69a5942a6d53d`, in Sepolia block 12197127 (2026-11-23 17:28:12 UTC).

Three things a reader should know before relying on "it works":

1. **Nobody has traded or staked yet.** At block 12197342 (18:14:12 UTC) the pool had no `Swap` event and the staking contract had no stake. Buying TEST with ETH is shown to execute by quotes and by read-only replays of the site's own transaction. Selling TEST cannot execute until someone has bought, because the pool holds only TEST. Staking behaviour is shown by tests and a fork simulation, not by a mined stake.
2. **The launch created three contracts, not two.** Besides the token and the staking contract, the platform's launch created its own `MerkleDistributor` (`0x9bdda1f1eb05892f45ef85fc006c4082aee54066`) and sent it 10% of the supply for the network's workers. The requester did not ask for that split; it is the platform's launch policy.
3. **The goal's own verification stages never ran.** They were cancelled because a worker could not reach the child's result. The checks in this report are ones I ran myself while writing, read-only, on 2026-11-23 between 18:03 and 18:20 UTC. They can be re-run from section 9.

Nothing in this report was signed or broadcast by me.

## 2. How the release is tied to this goal

The goal's notes record one order, `test-sepolia-release-e01` (a `workflow.open` with two deployments), and two job IDs for it that the earlier episodes could not reconcile: `48ad7795-23de-4483-90d3-a8789ee539ee` from the children list and `bcf313c5-810c-4236-95ef-495008dada68` from the completion wake. The result `e03-release-evidence/release` reports that neither result could be read because no service origin was documented.

The origin is documented publicly: https://imd.fun/skill.md says a job's result is at `GET https://api.imd.fun/jobs/JOB_ID/result`. Reading those records settles the question:

| Record | What it says |
| --- | --- |
| `https://api.imd.fun/workflows/b48935c9-5fc8-4bc3-8353-c79a2372b880` | status `completed`, chain 11155111; `contracts.id` = job `48ad7795…`, `frontend.id` = job `bcf313c5…`; launch `0fb2b93f-9684-43e6-b003-fa5d77b2c1a0` `live`; site `test-bcf3`, status `named` |
| `https://api.imd.fun/jobs/48ad7795-23de-4483-90d3-a8789ee539ee` | contract stage of that workflow, created 16:58:33 UTC, `completed`; `project.head` = `bcf313c5…`; delivery repository and commit as in section 3 |
| `https://api.imd.fun/jobs/bcf313c5-810c-4236-95ef-495008dada68` | frontend stage, `parentJobId` = `48ad7795…`, updated 17:51:49.884 UTC (the exact time of the wake in the goal's notes); carries the site record |
| `https://api.imd.fun/launches/0fb2b93f-9684-43e6-b003-fa5d77b2c1a0` | launch number 3361, kind `evm_project`, the four addresses of this report, and the launch transaction |

So the two job IDs are the two stages of one workflow, `b48935c9-5fc8-4bc3-8353-c79a2372b880`, which is the workflow the notes recorded in episode 2. The workflow's objective is the order's words ("Launch Test (TEST) on Sepolia with its launch opening a tradable Uniswap v4 pool. In that same launch deploy TestStaking…") and its brief says it is "a child job a paid goal opens for the goal's owner".

The chain agrees with those records independently of the platform. The launch transaction's calldata contains the repository URL of the contract stage, and a registry event in the same transaction (`0x90aaedd35073e2a31861276e58081251a601aad9`, log index 421) carries launch number 3361, the source commit `d706f89f307cb0f54ebff75c1db34f8db4c99bd4` and the attestation hash `20126179680ca0433c8d4c552678702a5c53d0beb5575113da91e3d60584045b`, both of which the published site also shows. In the 16,000 Sepolia blocks before my reading (about two days), this was the only v4 pool initialized for a token named Test with symbol TEST.

What I could not show: none of the public records names this goal's id or the order key `test-sepolia-release-e01`. The link from the goal to the release is the job ID that the goal's children list gave.

## 3. Repositories and commits

`trunk` is `null` in `goal.json`: the goal ran no code wave, so it has no repository or commit of its own. The code belongs to the child workflow and is public in two repositories:

| Stage | Repository | Commit |
| --- | --- | --- |
| Contracts | https://github.com/identity-md-launches/launch-3361-workflow-contract-stage-context | `d706f89f307cb0f54ebff75c1db34f8db4c99bd4` |
| Website | https://github.com/identity-md-launches/launch-3362-workflow-frontend-stage-context | `b4f9dd17e8d77f576d6fd71cc4e53252782ecc85` |

The website repository contains the contract sources too, plus `web/` (source) and `dist/` (the published export).

## 4. What I checked, and what each check shows

Each line says what kind of evidence it is. A **live read** is an `eth_call`, log or code read on Sepolia at a stated block. A **replay** is an `eth_call` of a real transaction payload with no state overrides. A **simulation** runs on a local fork and changes nothing on chain. A **local test** runs source code only. A **platform record** is what the platform's API says and is not independent.

Blocks used: launch block 12197127 (hash `0xfdd98da3da9e15611367b2195d807a90844a88376a6a1cdb4b49762a8fd32204`); review block 12197304 (hash `0xcc89520cff4867d35e7d938b511d36a743b3066d9a4612bc15dfe1f4bfa89fc9`, 18:05:48 UTC); recheck block 12197342 (hash `0x3c90dae02f1fb45fb0fce0cac8f9c2430a8e6a30ffc09d9b01f21612c13c0faa`, 18:14:12 UTC).

### 4.1 Token

| Check | Result | Kind |
| --- | --- | --- |
| `name()`, `symbol()`, `decimals()` | `Test`, `TEST`, 18 | live read, 12197304 |
| `totalSupply()` | 1,000,000,000 TEST (10^27 base units) | live read |
| No code at the address before block 12197127, 1,722 bytes after | created by the launch transaction | live read |
| Deployed bytecode against the public source at `d706f89f` (solc 0.8.26, optimizer 200, cancun) | byte-identical | rebuilt here |
| `owner()` | reverts: the token has no owner, mint, pause or upgrade path in its source | live read and source |

Where the supply went, from the four `Transfer` logs of the launch transaction: 1,000,000,000 minted to the launch factory, then 799,999,999.999999999999998187 TEST to the Uniswap v4 PoolManager, 100,000,000 TEST to the MerkleDistributor, and 100,000,000.000000000000001813 TEST to the launch owner `0x047f606fd5b2baa5f5c6c4ab8958e45cb6b054b7`. Balances at block 12197304 still equal those amounts, and no other TEST transfer has happened.

### 4.2 Staking contract

| Check | Result | Kind |
| --- | --- | --- |
| `token()` | the TEST address above | live read, 12197304 |
| `owner()`, `pendingOwner()` | `0x047f606fd5b2baa5f5c6c4ab8958e45cb6b054b7`, none | live read |
| `pointsPerSecond()` | 10^18, which is 1 point per second with 18 point decimals | live read |
| `totalStaked()`, TEST held by the contract | 0, 0 | live read, also at 12197342 |
| Deployed bytecode against source at `d706f89f` | 3,975 bytes, identical except the six immutable slots, which hold the TEST address | rebuilt here |
| Creation-code hashes against the launch record | match for both contracts (`f522bc33…`, `e93e383b…`) | rebuilt here and platform record |
| The repository's own Foundry suites at `d706f89f` | 54 tests passed, 0 failed (13 token, 32 staking, 8 adversarial-token, 1 invariant campaign) | local test |
| The six vectors of `e01-staking-points-acceptance/points-spec` written as a new test against this source | 6 passed with zero tolerance (section 6) | local test |
| Stake, accrue, withdraw on the deployed contract | passed, details below | simulation |

The simulation forked Sepolia at block 12197304 and used the deployed contracts. Two fresh accounts received 1,000 and 3,000 TEST from the owner's balance (impersonated in the fork only), approved and staked in the same second.

- After 100 seconds: 25 and 75 points, exactly one quarter and three quarters of the 100 points emitted.
- The larger staker withdrew and got 3,000 TEST back. After 50 more seconds the remaining staker had 75 points (all 50 new points) and the other still had 75.
- The last staker withdrew. After 1,000 seconds with nothing staked, nobody's points changed and total emitted points stayed at 150.
- The contract ended holding 0 TEST. A non-owner's `setPointsPerSecond` reverted, and so did a withdrawal with no stake.

That is the behaviour the goal asks for: points over time in proportion to each holder's share of the total currently staked. Because the deployed bytecode equals the tested source, the local tests apply to the live contract. No real stake has been mined yet.

### 4.3 Pool

| Check | Result | Kind |
| --- | --- | --- |
| `Initialize` log from the PoolManager `0xE03A1074c86CFeDd5C142C4F04F1a1536e203543` in the launch transaction (log index 416) | currency0 native ETH (`address(0)`), currency1 TEST, fee 12500, tick spacing 60, hooks `0xa0602cb30558d5dd17415b6268a4feea3a0ca000`, sqrtPriceX96 `560227709747861399187319382274582`, tick 177284 | live read |
| Pool ID recomputed as `keccak256(abi.encode(key))` | equals the log's indexed id | computed here |
| Token mint, `Initialize` and `ModifyLiquidity` order | log indexes 411, 416, 417 of the same transaction; no other `Initialize` for this id in the 40,000 blocks before or since | live read |
| `ModifyLiquidity` (log index 417) | sender is the launch factory `0x84cf2bc1dc2af577dba5d62e26f90d041ca38f7a`, range −887220 to 177240, liquidity 113387377674367368214378 | live read |
| `StateView.getSlot0` at 12197127 and 12197304 | same price and tick as at initialization, LP fee 12500, protocol fee 0 | live read |
| `StateView.getLiquidity` (liquidity active at the current tick) at both blocks | **0** | live read |
| Quote, buy with 0.01 ETH | 491,270.717279012453704024 TEST | live read, 12197304 |
| Quote, buy with 1 ETH | 46,311,571.271819422098048455 TEST | live read |
| Quote, sell TEST | reverts with `NotEnoughLiquidity(poolId)` | live read |
| The buy transaction the live site built (0.001 ETH, minimum 48,662.695887824967916158 TEST, Universal Router `0x3A9D48AB9751398BbFa63ad67599Bb04e4BdF98b`), called from the owner's address, which holds real Sepolia ETH | succeeds; gas estimate 360,148. The same call with the minimum raised reverts | replay, 12197342 |
| Buy 0.01 ETH through the Universal Router, then sell half back through Permit2 | received exactly the quoted 491,270.717… TEST; tick moved to 177227 and active liquidity became 113387377674367368214378; selling half returned 0.004877297515229249 ETH | simulation |
| `Swap` logs for this pool, launch block to 12197342 | **none** | live read |

Reading these together:

- The pool is this token's pool, it was first initialized by the launch, and the launch funded it in the same transaction.
- The opening price is 50,000,000 TEST per ETH, which values the whole supply at 20 ETH.
- The seed is a single position holding only TEST, placed just below the opening price (its upper bound, tick 177240, is 44 ticks under the current tick 177284). That is why active liquidity reads 0: no liquidity is in range until the first buy moves the price into the position. The first buy does that, as the quote, the replay and the simulation all show.
- A sale has nothing to be paid from until buyers have put ETH into the pool. After a buy, selling works, as the simulation shows.
- The position belongs to the launch factory, not to the owner. The pool's hook existed before the launch (488 bytes of code in the block before). Its address bits select only the before-initialize callback, so swaps do not call it. The platform's record names it `PoolInitializationGuard`. I did not review its code.

"It trades there" is therefore true in this sense: anyone with Sepolia ETH can buy TEST now, and sell once there has been buying. It has not been demonstrated by a mined trade.

### 4.4 Website

| Check | Result | Kind |
| --- | --- | --- |
| `GET https://test-bcf3.imd.site/` | 200, title "Test staking: stake TEST, earn points on Sepolia" | live fetch |
| All 11 files declared in the served `imd-deployment.json` | each SHA-256 matches its declared digest | live fetch |
| Served `imd-deployment.json` | byte-identical to `dist/imd-deployment.json` at commit `b4f9dd17`; names chain 11155111, the token and staking addresses and the pool key of this report | live fetch |
| Rebuild of `web/` at `b4f9dd17` (`npm ci`, `npm run build`) | all 12 output files byte-identical to the committed `dist/`, so the served site is the build of the public source | rebuilt here |
| The site's own tests (`npx vitest run`) | 15 passed (mocked wallet and chain: approve then stake, withdraw, wrong network, buy, sell) | local test |
| ENS `contenthash` of `test-bcf3.identitymd.eth` on Ethereum mainnet | decodes to CID `bafybeihblnrsdfxnwwjho7hjxtuckkvph7oeljlapsrg3jexuk6ibzhrli`, the CID in the platform's site record; the naming transaction `0xc6babf18cef03e46f9d2cd9a61a8509bee0ff9028084ccdb3481ac18534cc7a0` (mainnet block 26479452) succeeded | live read |
| Live site in headless Chromium 141 at 390×844, no wallet | renders with no console errors; shows "Total staked: 0 TEST · Points per second, shared: 1", pool price "1 ETH = 50,000,000 TEST", both contract addresses, the owner, the pool ID and key, and explorer links; stake and buy buttons disabled with "Connect a wallet to stake" | live browser |
| Horizontal overflow at 320, 390 and 1440 wide | 0 px | live browser |
| Connect with an injected stand-in wallet reporting the owner's public address on Sepolia (no key; every send request is recorded, then declined) | header shows `0x047F…54B7`; "Wallet 100,000,000 TEST", "Staked 0 TEST", "Share 0%", "Points 0", "Available: 103.4199 ETH", all read live from Sepolia | live browser |
| Enter 5 in the stake field and press the button | button reads "Approve 5 TEST"; the wallet is asked to send `approve(TestStaking, 5000000000000000000)` to the TEST token; after the decline the page says "Not sent. You declined the request in your wallet. Nothing was sent." | live browser |
| Withdraw tab, amount 1 | "You have 0 TEST staked. Enter that much or less." | live browser |
| Trade card, 0.001 ETH | "You receive about 49,154.23827 TEST" and "At least 48,662.695887 TEST after 1% slippage"; pressing buy asks the wallet to send 0.001 ETH to the Universal Router with the pool key of this report (the payload replayed in 4.3) | live browser |
| Trade card, sell 1,000 TEST | "Unable to quote: The contract refused this transaction in simulation.", consistent with 4.3 | live browser |

The site lets a visitor see the token and takes them through connect, approve, stake and withdraw against the live contracts. I did not complete a stake through the site, because that needs a real signature and I hold no key. The second step (`stake`) and a successful withdrawal are covered by the site's mocked tests and by the contract simulation, not by a live click-through.

## 5. Settings actually used

The requester left supply, pool economics and points parameters open. These are the values the release chose, read from chain unless marked.

| Setting | Value |
| --- | --- |
| Supply | 1,000,000,000 TEST, fixed, minted once |
| Supply split | 80% pool, 10% platform MerkleDistributor, 10% launch owner |
| Pool pair | TEST against native ETH |
| Pool fee | 12500 (1.25%), static; the contract README says 1% is for the paying wallet and 0.25% for the platform, which I did not verify |
| Tick spacing, hook | 60; `0xa0602cb30558d5dd17415b6268a4feea3a0ca000` |
| Opening price | 50,000,000 TEST per ETH (20 ETH for the whole supply). The manifest's `initialPrice` field says 2^96 (1:1) and was not what the launch used; the README says the service derives the price from its policy |
| Points rate | 1 point per second in total, shared by all stakers; 18 point decimals |
| Rate control | the owner may set it from 0 to 1,000,000 points per second, with no timelock; accrual up to the change uses the old rate |
| Staking owner | `0x047f606fd5b2baa5f5c6c4ab8958e45cb6b054b7`, the wallet the platform records as the payer; two-step ownership transfer |
| Owner powers | the points rate and ownership only. The source has no path to move principal, remove points, pause, change the token or upgrade |
| Stake cap, precision | 10^27 base units (the whole supply); accumulator scale 10^36 with carried remainders |
| Fees, lockups | none on stake or withdraw |
| Points | an on-chain score only: not a token, not transferable, not redeemable |
| Tokens sent straight to the staking contract | not stake, and not recoverable: there is no rescue function |

## 6. Against the goal's two acceptance specifications

The goal's first two batches produced specifications for a later review. Neither evaluated a deployment (their gates say `liveLaunchVerified: not_evaluated` and `implementationVerified: not_evaluated`). Here is how the release stands against each, on my checks.

**`e01-v4-pool-acceptance/pool-spec` (nine checks)**

| Check | Standing |
| --- | --- |
| sepolia-infrastructure | Mostly met. Chain id, PoolManager, StateView, Universal Router and Permit2 are the addresses on Uniswap's deployments page, and StateView and both quoters report that PoolManager. The site's Quoter, `0x61b3f2011a92d183c7dbadbda940a7555ccf9227`, is not the one that page lists today (`0x68aFa8b853cAa7a2D40B0F6AEE5C4DbC147C8244`); the two returned the identical quote. I did not compare periphery bytecode with a tagged release |
| pool-identity | Met |
| fee-spacing-hooks | Met for fee, spacing and tick alignment. The hook's code was not reviewed |
| launch-attribution | Met for causation: token creation, first initialization and seeding are one transaction. **Not met for the count**: the same transaction also created the MerkleDistributor, which this specification calls a failure of the two-contract limit |
| initial-price | No price was authorized by the requester, so there is nothing to compare with. The event's price and tick agree with each other and with the platform's stated 20 ETH policy |
| seed-active-liquidity | **Not met as written.** Seed funding settled, but active liquidity is 0 at launch completion and at review. The position is in place and one buy brings it into range |
| quote | Met for buying. Selling reverts |
| router-simulation | Met for buying, by the replay from a funded real address with no overrides. The fork simulation used a test account with dealt ETH |
| confirmed-swap | **Not met.** No swap has been mined |

**`e01-staking-points-acceptance/points-spec`**

- The rule (rate × seconds × stake ÷ total, nothing while empty), settling before every change, points kept after exit, and views that include pending accrual are all in the deployed code. The six vectors pass exactly on the source the deployment was built from: one staker (120); unequal stakes (30 and 90); staggered entry (90 and 30); partial then full exit (60 and 60); empty pool and re-entry (90 and 90, 180 in total); and a rate change from 12 to 20 (27 and 81).
- Required reads exist: `token()`, `totalStaked()`, `stakes(account)`, `pointsPerSecond()`, `ACC_PRECISION()`, `pendingPoints(account)` (lifetime total including pending, rounded down), `userPointRemainder(account)` for the fraction, and `owner()`.
- One difference from the specification: `Staked` and `Withdrawn` carry the account and the amount, but not the resulting user stake and total stake that the specification asks events to carry.
- One design difference, within the specification's allowance for equivalent accounting: on each stake change the contract discards the global rounding remainder (the README bounds each loss below 10^-9 of the smallest point unit) so that a newcomer cannot receive earlier dust.

## 7. What is missing, and what to know

1. **No mined trade and no mined stake.** Section 4 says what stands in their place. One small buy on the site would settle the pool question and bring liquidity into range.
2. **Three contracts were created, and 10% of TEST went to the platform's distributor** for its workers, with another 10% to the owner. The objective said two contracts and said nothing on allocation. The platform counts two project contracts.
3. **The liquidity is not the owner's.** The position is held by the launch factory. I did not examine how its fees are paid out or whether it can be withdrawn.
4. **Sells fail until there are buys**, and the site shows "Unable to quote" for a sale today.
5. **The owner can change the points rate at any time**, including to zero. This is the owner-settable answer to a parameter the objective left open.
6. **Reviews I did not read.** The platform's record shows five accepted review steps on the contracts and an admission check saying "no unresolved blocking findings"; their texts are not in the repository. `docs/REVIEW.md` there is the author's own review and says no Slither, Mythril or independent audit was run.
7. **Source verification on the explorer** is marked done for both contracts in the platform's record. I did not open the explorer to confirm it.
8. **Site coverage.** One headless Chromium run. No real wallet, phone, Safari or Firefox. The page also posts to `cca-lite.coinbase.com` (the Coinbase wallet library's metrics), which a visitor might not expect.
9. **Hosting.** `test-bcf3.imd.site` is the platform's gateway. From this machine the public gateways did not serve the CID (ipfs.io answered 403, dweb.link 429), so availability outside the platform rests on the ENS record and on the platform's own validation, which reports the assets reachable from the CID. That validation states that it does not execute JavaScript, test wallets or simulate swaps.
10. **The goal's planned checks did not run**, and its notes for episodes 3 and 4 say the release could not be verified. That was an access problem, not a finding about the release; this report supersedes it. My checks are one writer's, made read-only, and carry no independent authority.

## 8. How the goal ran

| | |
| --- | --- |
| Episodes | 4 of 5 used |
| Items | 3 of 50 used |
| Children bought | 2 deployments and 1 website; all spent on the one order `test-sepolia-release-e01` |
| Trunk | none |

| Batch | Item | Outcome |
| --- | --- | --- |
| `e01-v4-pool-acceptance` | `pool-spec` | accepted; the pool specification used in section 6 (SHA-256 `b49d4db3d6e3fbe8080f4dcad8933649a6fe8b42f1d7c84fd9f957be43bc1e75`) |
| `e01-staking-points-acceptance` | `points-spec` | accepted; the points specification used in section 6 (SHA-256 `438ecdfac458119750ce317255234c9cc92d9885bcee6f93745b65f7d4043ce5`) |
| `e03-release-evidence` | `release` | accepted; it records that the child results could not be reached and leaves every gate `unverified` (SHA-256 `16a7f68f5f37db1e4c8295da5ef08a01d20a821c7d4e17da3f241f27b10fc320`) |
| `e03-token-check`, `e03-pool-check`, `e03-staking-check`, `e03-site-check` | `release` | cancelled before running, because each waited on a `pass` gate in the manifest above. They are not failed tests |

Episode 1 sent the one combined order, so that the staking contract and the site could take the token's address by reference, and started the two specifications. Episode 2 waited on the child. Episode 3 laid out the evidence manifest and four checks behind it. Episode 4 found the manifest empty and the checks cancelled, and finished for a write-up. The release itself completed on the platform's side at 17:53 UTC.

## 9. Reproducing the checks

Public Sepolia RPC: `https://ethereum-sepolia-rpc.publicnode.com`. Pin reads to block 12197304 unless stated.

- Launch: `eth_getTransactionReceipt` for `0x711e61c1…d53d`; logs 411 to 422 hold everything in sections 4.1 and 4.3. `eth_getCode` at block 12197126 and 12197127 for the token, staking contract and distributor shows which were created.
- Token and staking reads: `eth_call` of the getters named in 4.1 and 4.2.
- Pool: `keccak256(abi.encode(address(0), token, uint24(12500), int24(60), hooks))`; `getSlot0(bytes32)` and `getLiquidity(bytes32)` on StateView `0xe1dd9c3fa50edb962e442f60dfbc432e24537e4c`; `quoteExactInputSingle(((address,address,uint24,int24,address),bool,uint128,bytes))` on either quoter with `zeroForOne = true`.
- Bytecode: clone the contracts repository at `d706f89f`, run `forge build`, and compare `deployedBytecode` with `eth_getCode`, allowing for the `token` immutable in TestStaking. `forge test` runs the 54 tests.
- Spec vectors: deploy `LaunchToken` and `TestStaking` in a Foundry test, set the rate to 12, and replay the six cases of the points specification with stakes in base units.
- Fork simulation: `forge test --fork-url <Sepolia RPC> --fork-block-number 12197304` with a test that stakes on the live contract and swaps through `execute(bytes,bytes[],uint256)` on the Universal Router (command `0x10`, actions `0x060c0f`, pool key above).
- Site: fetch `https://test-bcf3.imd.site/imd-deployment.json` and hash each listed asset; in `web/` at `b4f9dd17` run `npm ci`, `npx vitest run`, `npm run build` and compare `dist/`.
- ENS: `contenthash(namehash("test-bcf3.identitymd.eth"))` on the name's resolver on Ethereum mainnet.

## 10. Sources

- Goal results: `e01-v4-pool-acceptance/pool-spec`, `e01-staking-points-acceptance/points-spec`, `e03-release-evidence/release`; the goal's notes and batch list in `goal.json`.
- Child records: the four `api.imd.fun` addresses in section 2, and https://imd.fun/skill.md for the documented result route.
- Code: the two repositories and commits in section 3.
- Chain: Sepolia transaction `0x711e61c123a139e197c89fa3decdbbbc8a4c50e299ab3f4568d69a5942a6d53d` and state at the blocks named in section 4; Ethereum mainnet transaction `0xc6babf18cef03e46f9d2cd9a61a8509bee0ff9028084ccdb3481ac18534cc7a0`.
- Uniswap v4 deployments page, https://developers.uniswap.org/docs/protocols/v4/deployments (Sepolia section, read 2026-11-23).
- The published site, https://test-bcf3.imd.site.
