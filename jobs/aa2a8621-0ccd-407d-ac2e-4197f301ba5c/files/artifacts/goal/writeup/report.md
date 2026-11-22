# Not delivered: no token, no staking contract and no website were launched

**Status on 2026-11-22, 23:25 UTC: the goal asked for three launches and none of them exists.** There is no token on Sepolia, no staking contract and no website. This report therefore contains no contract address, no transaction hash and no site URL, because there is none to give. What the goal did produce is unlaunched source code and a launch order that the network's checker now accepts but that was never admitted. Both are described below so that the launch can still be made; neither is the thing that was asked for.

The goal, in the requester's words: *"laucnh a token on sepolia called test and ticker test, then launch a smart contract to stake these tokens and you get points on lengths staked based on your share, and launch a website for it"*.

## 1. Where each of the three parts stands

| Asked for | Live? | What exists instead |
| --- | --- | --- |
| A token on Sepolia called test, ticker test | **No.** No address, no transaction. | `src/TestToken.sol` on the trunk, tested locally only |
| A staking contract for it, points by share and time staked | **No.** No address, no transaction. | `src/ShareStaking.sol` on the trunk, tested locally only |
| A website for it | **No.** No URL, no IPFS CID, no ENS name. | `site/` on the trunk, never published and never opened in a real browser |

The code is in the goal's repository, its trunk:

- repository: https://github.com/identity-md-launches/goal-3352-laucnh-token-sepolia-called.git
- commit the goal's waves reached: `423999f8ba694b2b9534fece6545207072e87b4b` (wave 1; no later wave merged)

## 2. Why nothing was launched

On this network a goal's workers cannot deploy anything. The requester's note of 2026-11-22 22:47 UTC says so: *"Nothing a goal item writes can be deployed: contracts reach Sepolia only through an order."* An order is a separate job the orchestrator opens through one of the goal's doors. I, the orchestrator, sent three orders. All three were refused before any work started, and the goal's five episodes are now spent. The public record of the goal lists them (`GET https://api.imd.fun/goals/aa2a8621-0ccd-407d-ac2e-4197f301ba5c/children`, read again while writing this report):

| Episode | Order key | Door | State | The refusal, as recorded |
| --- | --- | --- | --- | --- |
| 2 | `ep02-test-token` | `launch.open` | refused | "launch.open opens a job that ends in a launch; set onchain to true or to a launch kind" |
| 3 | `test-staking-launch-site` | `workflow.open` | refused | "The checker is not sure the request wants publication or archival of source code or research reports, separate from public website hosting, which the plan includes. Say whether it does." |
| 5 | `test-staking-launch-site-2` | `workflow.open` | refused | "Automatic submission of a launch requires permissions.onchain matching the launch's chain (11155111) and kind." |

None of the three has a job, a launch or a workflow behind it. The goal's own snapshot in its last episode showed the budget for such jobs untouched: two on-chain deployments and one website were bought, and none was used.

Each refusal was a mistake in the order I wrote, not a fault of the network and not anything the requester did:

1. **Episode 2.** I ordered the token alone through `launch.open` and left out the `onchain` setting that door requires. The requester's note then replaced that plan: token and staking contract must be in one workflow, because an order cannot name an address that another order deployed.
2. **Episode 3.** The combined order did not say whether the source code should be published. The checker asked.
3. **Episode 4.** I opened nothing. The goal's snapshot showed one effect pending and no outcome for the episode 3 order, and I waited rather than risk a duplicate launch. The order had in fact been refused, so the episode was lost.
4. **Episode 5, the last.** I answered the publication question but sent the order without a `permissions` block. The public documentation says `permissions.onchain` is "Required here" for a workflow, and the network's free check, run without it, returns exactly the blocker the order was then refused with (`deployment_permission_missing`; I ran it again for this report and it still does). I had seen that answer before sending and assumed the goal's door fills the block in by itself. It does not. That was my error, and it cost the last chance to launch inside this goal.

This write-up step cannot open orders, so it cannot repair that.

## 3. What the goal built (not launched)

Two batches ran, both code waves. Seven of the goal's 50 items were used.

| Batch | Items | Outcome |
| --- | --- | --- |
| `sepolia-staking-app` | 4: token, staking, website, release | 4 accepted, merged into the trunk as commit `423999f` |
| `ep02-integrate` | 3: staking, website, release | 1 accepted (release), 2 failed; I cancelled the wave after the requester ruled out more rebuilding, and nothing of it was merged |

The trunk at `423999f` holds nine files:

- `src/TestToken.sol`, with `test/TestToken.t.sol`. A fixed-supply ERC-20. `name()` and `symbol()` are both the lowercase string `test`, `decimals()` is 18. The constructor takes the supply in base units and mints all of it to the deployer; there is no later mint or burn. (Result `sepolia-staking-app/token`.)
- `src/ShareStaking.sol`, with `test/ShareStaking.t.sol`. The staking contract, described in section 4. (Result `sepolia-staking-app/staking`.)
- `site/index.html`, `site/style.css`, `site/app.js`. A static dashboard with no dependencies. It reads `deployment.json` from its own folder, works through a browser wallet, asks it to switch to Sepolia, checks that the staking contract's `token()` is the token in `deployment.json`, and shows the wallet's token balance, stake, share of the pool, points and the total staked, with one amount field and buttons to stake and withdraw. It asks for an approval of the exact amount when the allowance is too small and waits for each receipt. Without a wallet it shows only a prompt to open the page in a browser that has one. Without `deployment.json` it shows "Setup required", which is its state on the trunk today. (Result `sepolia-staking-app/website`.)
- `release/deploy.py`, `release/README.md`. A deployment script. Do not rely on the trunk's copy: the one accepted item of the cancelled wave (result `ep02-integrate/release`) reports that it found and fixed bugs in it (artifact lookup, `cast` argument order, `cast` JSON output), and that fixed version was never merged. Section 6 uses plain `forge create` instead.

### What was checked, and by whom

By the workers, as their results report (I did not rerun these):

- token: 32 tests pass on Solidity 0.8.24 and 0.8.26, four of them fuzz tests at 1,024 runs;
- staking: 2 tests pass, after the worker repaired a rounding loss its first run found;
- website: `node --check` passes, and a scratch test with a simulated wallet passed; the worker states that browser rendering and real wallet behaviour were not verified, and that scratch test is not in the repository;
- release (cancelled wave, not on the trunk): `forge build`, `forge fmt --check` and 19 Python tests against a local chain passed; its own gate reads `unverified`, and it states that "Local anvil receipts are not Sepolia evidence; no live deployment, signing or RPC was done."

By me, on the machine that wrote this report, from a fresh clone at `423999f` with Foundry 1.8.3 and Solidity 0.8.26:

- `forge test --use 0.8.26`: 34 tests passed, 0 failed (32 token, 2 staking; fuzz tests at the default 256 runs).
- On a disposable local chain started with chain id 11155111, the two `forge create` commands of section 6 deployed both contracts. Read back: `name()` "test", `symbol()` "test", `decimals()` 18, the whole supply held by the deployer, and `ShareStaking.token()` equal to the token's address.
- On that chain, two accounts ran the worked example of section 4 with real transactions at set timestamps. The result was exactly 125 and 175 points (in 18-decimal units), both stakes came back in full, the contract held no tokens afterwards, and 600 further seconds with nothing staked added no points.
- The `site/` folder with a `deployment.json` naming those local contracts was served over HTTP: all four files returned 200. This checks that the files are servable and nothing more. No browser and no wallet were involved.

**None of this is evidence of anything on Sepolia.** A local chain with Sepolia's chain id is not Sepolia, and a folder served on one machine is not a published website. The local addresses and hashes are deliberately left out of this report so that nobody mistakes them for a deployment.

### What was never done

- No independent security review of either contract. The first order would have included one; no order ran.
- The staking contract has two tests and no fuzz tests. The item meant to strengthen them failed.
- The dashboard was never rendered in a real browser or used with a real wallet.

## 4. The staking rule as built

The goal says points depend on "lengths staked based on your share". The contract reads that as follows, and the requester should confirm it is what they meant:

- In every second in which anything is staked, the pool as a whole earns exactly one point (10^18 units; points have 18 decimals like the token).
- That point is divided among the stakers in proportion to their stake over the total stake during that second.
- Seconds in which nothing is staked earn nothing.
- Points only grow. They are kept after a withdrawal. They are a number in the contract, not a token: they cannot be transferred or spent.
- There is no lockup, fee, owner or admin. `withdraw` returns any part of a stake at any time.

So points measure share multiplied by time, not amount multiplied by time: someone staking alone earns one point a second whether they stake 1 token or 1,000,000.

Worked example, which I ran on a local chain (section 3):

| Seconds | Staked | A earns | B earns |
| --- | --- | --- | --- |
| 0 to 100 | A 100 | 100 | 0 |
| 100 to 200 | A 100, B 300 | 25 | 75 |
| 200 to 300 | B 300 | 0 | 100 |
| after 300 | nothing | 0 | 0 |
| **Total** | | **125** | **175** |

Interface: `constructor(address tokenAddress)`, `token()`, `stake(uint256)`, `withdraw(uint256)`, `stakedBalance(address)`, `totalStaked()`, `pointsOf(address)`, events `Staked` and `Withdrawn`. A staker first calls the token's `approve(stakingAddress, amount)`.

One thing I noticed reading the source, for whoever reviews it: `stake` moves the tokens in before it updates its own balances. With the plain token here, which makes no outside calls, that order cannot be exploited; with a token that calls back into its receiver it would need a second look. The contract also assumes the token delivers exactly the amount transferred.

## 5. Way forward, route 1: place the launch order (recommended)

This is the launch the requester's note described: one workflow that builds, reviews and deploys the token and the staking contract together on Sepolia, then builds the website on the live contracts and hosts it. It has to be placed by the requester, or by the network giving the goal another episode; I cannot place it from here.

The body below is the order refused in episode 5, with the missing `permissions` block added. On 2026-11-22 I sent this exact body to the network's two free validations:

- `POST https://api.imd.fun/requests/check` with action `workflow.open`: `blockers: []`, `suggestions: []`. Its plan: build and test the contracts; audit them, as another agent; deploy on Sepolia; build the site against the live contracts; host the site on IPFS, source on GitHub.
- `POST https://api.imd.fun/requests/quote`: `created: true`, status `quoted`. The quote was not paid and lapsed after ten minutes. No order was placed.

These validate the public door. They do not prove the goal's own door would admit the same body; the goal's reference shows that door taking only `request` and `draft`, and it has never been tried there with `permissions`.

```json
{
  "request": "Launch three things on Sepolia (chain id 11155111), in one workflow.\n\n1. A token named test with ticker TEST: the launch's standard token, on the platform's standard launch terms. I ask for no other supply, split or transfer rule.\n\n2. A staking contract for that token, ShareStaking, deployed in the same launch and bound to the token by its constructor, which takes the token's address as its only argument. It has no owner, no admin, no fee, no lockup and no upgrade. Functions: stake(uint256 amount), which pulls the tokens from the caller after an approval; withdraw(uint256 amount), which returns any part of the caller's stake at any time; token(); totalStaked(); stakedBalance(address); pointsOf(address). Events: Staked(account, amount) and Withdrawn(account, amount).\n\nPoints rule: stakers earn points by how long they have staked and by their share of the total stake. In every second in which anything is staked, the whole pool earns exactly one point (10^18 units, 18 decimals), divided among the stakers in proportion to stake over total stake during that second. Seconds in which nothing is staked earn nothing. Points only grow, are kept after a withdrawal, cannot be transferred or spent, and are not a token. Use a cumulative index and carry the rounding remainders, so that the sum of all points never exceeds the number of occupied seconds. Worked example the tests must reproduce exactly: A stakes 100 at second 0, B stakes 300 at second 100, A withdraws all at second 200, B withdraws all at second 300; A ends with 125 points and B with 175, and each gets back exactly what they staked.\n\n3. A website for it, built on the live contracts: a static dashboard that reads the deployment record, asks the wallet to switch to Sepolia, checks that the staking contract's token() is the launched token, and shows the connected wallet's token balance, allowance, stake, the total staked, the wallet's share of the pool in percent, and its points, refreshed as time passes. It has controls to approve the exact amount, stake and withdraw, each waiting for its receipt and showing success or the error.\n\nTest the contracts with Foundry, including fuzz tests of the points rule, and have an independent security review of the contracts by another agent before anything is deployed.\n\nPublication: yes, publish the source code of the contracts and of the website to GitHub. The built site is hosted on IPFS under an ENS name; that hosting is separate from the source publication. I ask for no research report and no other archive.",
  "draft": {
    "objective": "Build the test (TEST) launch token and ShareStaking with Foundry tests and an independent review, deploy both on Sepolia in one launch, then build the staking dashboard against the live deployment.",
    "shape": "chain",
    "onchain": "evm_project",
    "chainId": 11155111,
    "github": true,
    "ipfs": true,
    "contracts": [
      "TestToken",
      "ShareStaking"
    ],
    "steps": [
      {
        "skill": "build-contract-project",
        "objective": "The launch token (name test, symbol TEST) and ShareStaking bound to it by constructor, with a Foundry project and tests of the points rule.",
        "acceptanceCriteria": [
          "name() returns test and symbol() returns TEST",
          "ShareStaking.token() returns the launch token and cannot change",
          "A 100 at second 0, B 300 at 100, A out at 200, B out at 300 gives A 125 points and B 175 points, 18 decimals",
          "Seconds with nothing staked add no points, and the sum of points never exceeds occupied seconds",
          "Every staker can withdraw the full stake at any time; no owner, fee or lockup"
        ]
      },
      {
        "skill": "frontend-for-contract",
        "objective": "A static dashboard on the deployed addresses: connect a wallet, switch to Sepolia, approve, stake, withdraw, and read balance, stake, total staked, share and points.",
        "acceptanceCriteria": [
          "Shows token balance, allowance, stake, total staked, share percent and points for the connected wallet",
          "Approve, stake and withdraw wait for their receipts and show success or the error",
          "Refuses to transact when staking.token() differs from the deployment record's token"
        ]
      },
      {
        "skill": "adversarial-review"
      }
    ]
  },
  "permissions": {
    "github": true,
    "ipfs": true,
    "onchain": {
      "kind": "evm_project",
      "chainId": 11155111
    }
  }
}
```

To place it: open https://explorer.imd.fun/launch with a browser wallet and paste the body in, or follow https://imd.fun/skill.md (steps 2 to 4). The price shown by the network is 0.5 IMD per request, paid on Ethereum mainnet or Robinhood Chain; the launch itself lands on Sepolia. The network's terms say payment buys admission of the work, not a guaranteed result, and that there are no refunds, so run the free check again first: the checker's answer can change.

### What the requester should know before placing it

Three things in this order were decided by me or by the platform, not by the requester:

1. **Ticker.** The goal says "ticker test"; the requester's later note says "ticker TEST". The order follows the note: name `test`, symbol `TEST`. Change `TEST` in the body if lowercase was meant.
2. **Source publication.** The order answers the checker's question with yes: contract and website source go to GitHub. The requester never wrote that. I answered yes because the documented workflow publishes the source before it deploys, so there is no launch without it.
3. **Token terms.** The check states these as fixed by the platform for this kind of launch, and the goal chose none of them: supply 1,000,000,000 with 18 decimals, minted once; plain transfers with no fees, limits, pausing or minting; 10% to the swarm and 90% to the requester, of which 80% goes into a pool unless chosen otherwise and the rest to the paying wallet; the pool paired with ETH, opening at a 20 ETH market cap; a trading fee of 1.25% of every trade, 1% to the requester and 0.25% to the network; no upgrades. So this route yields a traded token with a pool, which is more than "a token called test". If that is not wanted, use route 2.

The contracts and site this route produces are built afresh by the workflow from the order's words. The trunk's code is the specification they were written from, not what gets deployed.

### What to record when it completes

`GET https://api.imd.fun/workflows/<workflow id>` gives the launch status, the manifest with both addresses, and the site's IPFS CID and ENS name. The three values this report is missing are then: the token address, the staking address and the site address.

## 6. Way forward, route 2: deploy the trunk's code yourself

This needs Foundry, a Sepolia RPC endpoint, an account with Sepolia ETH, and a choice of supply. It produces exactly the prototype: both `name()` and `symbol()` are lowercase `test`, the supply is whatever is passed in, all of it goes to the deploying account, and there is no pool. It gets no independent review and no hosting; the site still has to be put on a host of the requester's choosing.

```sh
git clone https://github.com/identity-md-launches/goal-3352-laucnh-token-sepolia-called.git
cd goal-3352-laucnh-token-sepolia-called
git checkout 423999f8ba694b2b9534fece6545207072e87b4b
forge test --use 0.8.26

# SUPPLY_BASE_UNITS: the supply times 10^18, a choice the goal leaves to the requester.
forge create --use 0.8.26 --rpc-url "$SEPOLIA_RPC_URL" --account "$FOUNDRY_ACCOUNT" --broadcast \
  src/TestToken.sol:TestToken --constructor-args "$SUPPLY_BASE_UNITS"
# TOKEN_ADDRESS: the "Deployed to" address printed by the command above.
forge create --use 0.8.26 --rpc-url "$SEPOLIA_RPC_URL" --account "$FOUNDRY_ACCOUNT" --broadcast \
  src/ShareStaking.sol:ShareStaking --constructor-args "$TOKEN_ADDRESS"

# Check, then write the site's deployment record. STAKING_ADDRESS: from the second command.
cast chain-id --rpc-url "$SEPOLIA_RPC_URL"                                  # 11155111
cast call "$TOKEN_ADDRESS" 'name()(string)' --rpc-url "$SEPOLIA_RPC_URL"    # "test"
cast call "$TOKEN_ADDRESS" 'symbol()(string)' --rpc-url "$SEPOLIA_RPC_URL"  # "test"
cast call "$STAKING_ADDRESS" 'token()(address)' --rpc-url "$SEPOLIA_RPC_URL" # the token address
printf '{"chainId":11155111,"token":"%s","staking":"%s"}\n' "$TOKEN_ADDRESS" "$STAKING_ADDRESS" > site/deployment.json
```

Then publish the `site/` folder, with that `deployment.json` in it, on any static host; its files use relative paths.

I ran these commands against a local chain with chain id 11155111 and they worked as written, with one difference: I signed with the local chain's built-in development key through `--private-key`, so the `--account` keystore flag itself was not exercised. On Sepolia they have not been run by anyone in this goal.

## 7. What is missing

Everything the goal asked for:

1. A Sepolia address of a token whose `name()` reads `test` and whose `symbol()` reads as the requester chooses.
2. A Sepolia address of a staking contract whose `token()` is that address.
3. A website address that opens in a browser and works against those two contracts.

Also missing, and needed before real value is staked: an independent review of the staking contract, wider tests of it, and a test of the dashboard in a real browser with a real wallet.

The goal is not done until route 1 or route 2 has been carried out and those three values exist. This report should then be amended with them, each one checked: the token and staking addresses by reading them on Sepolia, the site by opening it.

## 8. Sources

- The goal's record: `.imd/reads/goal.json` (objective, five episodes of orchestrator notes, the requester's note, both batches).
- Results handed to this write-up: `sepolia-staking-app/token`, `sepolia-staking-app/staking`, `sepolia-staking-app/website`, `sepolia-staking-app/release`, `ep02-integrate/release`.
- The trunk: https://github.com/identity-md-launches/goal-3352-laucnh-token-sepolia-called.git at `423999f8ba694b2b9534fece6545207072e87b4b`, cloned and tested for this report.
- The network's public record and documentation, read on 2026-11-22: `https://api.imd.fun/goals/aa2a8621-0ccd-407d-ac2e-4197f301ba5c` and `/children` under it (the three refusals; state `executing`, 7 items, 5 accepted, 2 failed); https://imd.fun/skill.md and https://imd.fun/skill/workflows.md (order shape, the required `permissions.onchain`, how a workflow runs); `https://api.imd.fun/requests/check` and `/requests/quote` (the validations in section 5).
