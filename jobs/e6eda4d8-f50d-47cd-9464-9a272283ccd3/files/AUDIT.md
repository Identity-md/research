# Audit report

> Audit request: Pepes Earn IMD (NFT collection with IMD holder rewards)
>
> Repository: https://github.com/0xtenang/PepesFamily
> Commit: 9c00fa216b38dda7b6a05936d47468d19637e586
> Chain: Robinhood Chain (chain ID 4663), Uniswap v4
> Status: not deployed yet; this audit is before deployment
>
> Scope (new code)
>
> contracts/src/earn/PepesEarnIMD.sol: pool owner and Uniswap v4 hook
> contracts/src/earn/PepesEarnToken.sol: $EARN, a DN404 base token with holder rewards, 30-day expiry and $Pepes buyback
> contracts/src/earn/PepesEarnMirror.sol: the ERC-721 side (DN404 mirror) with an ERC-2981 royalty
> contracts/src/earn/PepesEarnRenderer.sol and LibEarnString.sol: on-chain SVG art, JSON and Base64
> Context (already audited, reused unchanged): PepesFamilyRouter.sol, PepesFamilyEthRouter.sol, lib/SafeTransfer.sol, and the hook logic from PepesFamily.sol (v3). DN404 is the upstream library at contracts/lib/dn404, commit 3397cb1. Please review how we integrate with it, not DN404 itself.
>
> Tests: contracts/test/PepesEarn.t.sol (22 tests) and contracts/test/PepesEarn.fork.t.sol, a mainnet-fork lifecycle test. Run the fork test with FORK_RPC=https://robinhood.drpc.org forge test --mc PepesEarnForkTest.
>
> What it does
>
> Supply: 2,000 $EARN tokens. Each whole token shows as one on-chain NFT (DN404). Wallets get NFTs; contracts don't. EIP-7702 delegated wallets count as wallets.
> Pool: PepesEarnIMD.openPool(token) (owner, one-time) puts the whole supply into a $EARN/IMD Uniswap v4 pool as single-sided liquidity owned by the hook, which has no way to remove it.
> Fee: every swap pays 4% of its IMD side, the same hook as PepesFamily v3: 1% to feeRecipient and 3% to $EARN holders pro rata. Holders claim manually with claim().
> Marketplaces: NFTs can be traded on marketplaces. The mirror reports a 4% ERC-2981 royalty paid to PepesEarnIMD in ETH. convertRoyalties(minOut) (owner) swaps it to IMD on the IMD/ETH pool and splits it 1% / 3% in the same way.
> Expiry: if a wallet neither claims nor moves any $EARN for 30 days, its unclaimed rewards expire, except what it earned during those 30 days. Anyone can call recycle(holder) to move expired rewards into buybackReserve.
> Buyback: the reserve can only be spent through buybackAndBurnPepes(imdIn, minOut, deadline) (owner), which buys $Pepes through the PepesFamily v1 router and sends all of it to 0x…dEaD.
> No owner on the token: owner() returns address(0). DN404's default infinite Permit2 allowance is disabled.
> Trust model (please confirm or break)
>
> The PepesEarnIMD owner can only:
> change feeRecipient;
> transfer ownership (two-step);
> open the pool once;
> convert royalties, choosing the minimum output;
> time buybacks, choosing the minimum output.
> The owner must never be able to take holders' tokens, rewards, the buyback reserve, the pool liquidity, or royalty IMD meant for holders, or change fees.
> Nobody but a holder can claim that holder's rewards. Recycling can only move rewards that have expired, and only into the reserve.
> Please look hardest at
>
> DN404 integration with reward accounting. Rewards are updated in _moved(), called after _transfer (ERC-20 side) and _transferFromNFT (NFT side, which changes balances directly).
> Is any other path able to change balances without updating corrections, eligibleSupply or lastActive? Consider mirror operations, setSkipNFT, initialisation, and transfers to and from excluded addresses.
> Can any sequence make eligibleSupply or the corrections inconsistent, or let rewards be claimed twice?
> Expiry maths (expiredRewardsOf, recycle, magAt, _checkpoint).
> The design assumes a holder's balance is unchanged since lastActive, because every balance change updates it. Can that assumption be broken?
> Can recycling ever take rewards earned in the last 30 days, or more than the holder's withdrawable amount? Check rounding: "recent" rounds up in the holder's favour.
> Is the checkpoint array (one entry per second with distributions, binary search) correct and safe from gas problems over years of use?
> Accepted by design: sending someone a dust amount resets their timer. That only delays expiry.
> Accounting invariant. The token's IMD balance should always be at least accountedBalance + buybackReserve, and distribute() must never hand out the reserve. Check every path: claim, recycle, buyback, royalties, donations, and the first buy before any holder exists.
> Flash-borrowed pool tokens (the v3 audit finding).
> While the PoolManager is unlocked, only the hook may distribute.
> flush mid-unlock only distributes when called by our routers.
> convertRoyalties distributes inside the hook's own unlock. We believe no one else can hold borrowed $EARN there; please verify.
> Buyback and burn. Owner-only, limited to the reserve, approval reset to 0 afterwards, burned amount measured by balance difference, nonReentrant. The $Pepes token and v1 router addresses are fixed at deployment. Any way to misuse or redirect the reserve?
> Royalty conversion. receive() accepts any ETH. Check the ETH settlement amount, the 1/4 vs 3/4 split, minOut, and whether stray ETH could break anything.
> Hook and pool. It's a copy of v3 with a single token and openPool validation (the token's hook, routers, PoolManager and IMD must match, and the full supply must be held by the hook). Anything new compared with v3?
> NFT gas. Buying N whole tokens mints N NFTs in one transaction. Is there a buy or sell size, or a sequence, that runs out of gas or traps funds? Is the router path (transferFrom and take with DN404) safe?
> The _skipNFTDefault override: the EIP-7702 check (code.length == 23 && bytes3(code) == 0xef0100). Any address type it misclassifies in a harmful way?
> Renderer. tokenURI gas is about 2.8M typical and about 9M maximum. There's no user input, so no injection. Please confirm the Base64 assembly is memory-safe.
> Known and accepted (no need to report unless you see more impact)
>
> Partial fill: the hook charges 4% of the requested amount when a third-party swap with a tight price limit only partly fills (same as v3, medium finding). Our routers always fill fully.
> First-buy rebate: the first buyer's own 3% waits in the token and goes to whoever holds at the next distribution, which can be that buyer (same as v3, info).
> Optional royalties: marketplace royalties depend on the marketplace; only pool trades are guaranteed to pay 4%.
> No editable OpenSea collection page: owner() is zero on the token and mirror, so nobody can claim the collection page on OpenSea. This is intentional.
> Planned deployment parameters
>
> PoolManager 0x8366a39CC670B4001A1121B8F6A443A643e40951
> IMD 0x5F7Bb59365ce557C26dbcAa4EE9d39A4b95B7127
> IMD/ETH pool: fee 10000, tick spacing 100, no hooks
> Starting market cap: about 2,000 IMD (1 IMD per NFT)
> $Pepes 0xE2C46c7068566740A33A4C93f5445B07BCfE5644
> PepesFamily v1 router 0xA73604EA3C393B47573986ff9Ce5A9EAb61883dC
> Fee recipient and owner: 0x3c8A4d94B3219F6633F2cC94094f4765b30c691C
> What we'd like back
>
> A plain-language answer: Can anyone, including the owner, take holders' NFTs, tokens or rewards? Can the expiry ever take rewards earned in the last 30 days?
> All findings with severity, a reproduction and a suggested fix.
> Anything that should change before deployment, since the contracts can't be changed afterwards.

| | |
|---|---|
| Repository | https://github.com/0xtenang/PepesFamily.git |
| Commit | `9c00fa216b38dda7b6a05936d47468d19637e586` |
| Job | `e6eda4d8-f50d-47cd-9464-9a272283ccd3` |
| Judged | 2026-10-04 13:50 UTC |
| Findings | 3 medium · 2 low · 5 info |

Four agents audited the code as it is at `9c00fa2`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Medium: Owner can take most of the holders' royalty ETH by sandwiching its own convertRoyalties call (the only price bound is a minimum the owner picks)

`contracts/src/earn/PepesEarnIMD.sol:370`

```
if (imdOut < minImdOut) revert Slippage();
```

convertRoyalties() sells the hook's whole ETH balance on the IMD/ETH pool in one swap with price limit MIN_SQRT_PRICE+1. The only price protection is minImdOut, chosen by the caller, and the caller is the owner. The brief says the owner 'must never be able to take ... royalty IMD meant for holders'; with minImdOut = 0 the owner can, in one transaction (owner is a contract, or batches calls): (1) buy IMD with ETH on the same pool, pushing the IMD price up, (2) call convertRoyalties(0) so the royalty ETH buys IMD at the inflated price, (3) sell the IMD from step 1 back into the pool that now holds the royalty ETH. Holders (3/4) and feeRecipient (1/4) receive a fraction of the fair IMD and the owner keeps the difference minus the 1% pool fee on its two legs. It pays once the accumulated royalty ETH exceeds roughly 1-2% of the pool's ETH depth, and the owner alone decides how long royalties accumulate. A third party cannot do this if the owner sets a tight minimum; this is an owner power that contradicts the stated trust model, and it cannot be removed after deployment. Merged from three specialist reports (economics, flow, permissions). Fix that keeps the design (owner times the conversion, output only to feeRecipient and holders): cap the ETH converted per call to a small fraction of the IMD/ETH pool's virtual ETH reserve read inside the unlock (e.g. 0.5%, so a sandwich pays more in pool fees than it can capture) and enforce a minimum interval between calls; larger balances convert over several calls. With that bound the function can also be permissionless, which removes the dependency on a live owner. Otherwise, state plainly in the docs that the owner is trusted for fair execution of this swap.

**Reproduction**

Reproduced in the repository's unit-test setup (contracts/test/PepesEarn.t.sol: IMD/ETH pool fee 10000, tick spacing 100, price 1:1, full-range liquidity 10,000e18). alice buys $EARN with 100 IMD and bob with 10 IMD; vm.deal(hook, 500 ether). Baseline: owner calls hook.convertRoyalties(0) -> returns 471.653168175321581705 IMD. Attack, all as owner: PoolSwapTest.swap{value: 7000 ether}(imdEthKey, SwapParams(true, -7000 ether, MIN_SQRT_PRICE+1)); hook.convertRoyalties(0); PoolSwapTest.swap(imdEthKey, SwapParams(false, -int256(imdReceivedInFirstSwap), MAX_SQRT_PRICE-1)). Expected (trust model): about 471.65 IMD is split between feeRecipient and holders and the owner gains nothing. Actual: convertRoyalties returns 167.793624011776061612 IMD (holders get 3/4 of that, about 125.8 instead of about 353.7), the owner's IMD balance is unchanged and its ETH balance goes from 7000 to 7211.823556036828024221, i.e. the owner nets about 211.8 ETH of the 500 ETH of royalties.

### 2. Medium: Owner can redirect part of the buyback reserve to itself by sandwiching buybackAndBurnPepes (size, timing and minPepesOut are all owner-chosen)

`contracts/src/earn/PepesEarnToken.sol:298`

```
IPepesRouter(pepesRouter).buy(pepes, imdIn, minPepesOut, deadline);
```

buybackAndBurnPepes() spends up to the whole reserve in one v1-router buy on the thin $Pepes/IMD curve. The only price protection is minPepesOut, supplied by the owner. The brief says the owner must never be able to take the buyback reserve and that it 'can only be spent buying $Pepes and burning it'. The owner can buy $Pepes through the same v1 router first, run the buyback with minPepesOut = 0 at the inflated price, then sell its $Pepes into the price the reserve just pushed up: most of the reserve's IMD leaves the pool in the owner's sell and far fewer $Pepes are burned. The cost is the v1 hook's 4% on each of the owner's two legs (of which 1% goes to the v1 fee recipient, per the brief the same address as this owner), so it pays once the reserve exceeds a few percent of the $Pepes pool's IMD depth; the owner decides how large the reserve grows before it buys. Who loses: the burn (expired holder rewards). Not exploitable by third parties when the owner sets a tight minimum. Merged from three specialist reports. Fix that keeps the design: cap imdIn per call to a small fraction of the $Pepes pool's IMD depth (well under the 8% round-trip fee, e.g. 2%) plus a minimum interval between buybacks, so a sandwich always costs more than it captures; the owner still times buybacks and sets minPepesOut, and with the cap the call can be permissionless. Trade-off: large reserves take several calls.

**Reproduction**

Reproduced on a Robinhood Chain fork (chain id 4663, FORK_RPC=https://robinhood.drpc.org) using the setup of contracts/test/PepesEarn.fork.t.sol (real PoolManager, IMD, $Pepes 0xE2C4...5644 and v1 router 0xA736...83dC; the test contract is the owner). alice and bob each router.buy(earn, 8_000e18, 0, now); warp 31 days; recycle(alice); recycle(bob) -> buybackReserve = 479.999999999999999999 IMD. Baseline: earn.buybackAndBurnPepes(reserve, 0, now) burns 16,903,096.41 $Pepes. Attack, as owner in one transaction starting with 3,000 IMD: v1Router.buy(PEPES, 3_000e18, 0, now); earn.buybackAndBurnPepes(reserve, 0, now); v1Router.sell(PEPES, <all bought in step 1>, 0, now). Expected: about 16.9M $Pepes burned and no gain for the owner. Actual: 5,923,531.63 $Pepes burned (65% fewer) and the owner's IMD balance ends at 3,063.043006514956115223, i.e. +63.04 IMD after all fees (before counting the v1 protocol fee that also goes to the same address).

### 3. Medium: Royalties paid in an ERC-20 (WETH for accepted offers and bids, or IMD) are stuck in the hook forever: only native ETH can be converted

`contracts/src/earn/PepesEarnIMD.sol:367`

```
uint256 ethIn = address(this).balance;
```

PepesEarnMirror.royaltyInfo names PepesEarnIMD as royalty receiver for every sale, whatever the sale currency, and marketplaces pay ERC-2981 royalties in the currency of the sale: native ETH for listings, but WETH (or another ERC-20, e.g. IMD) for accepted offers and collection bids. convertRoyalties only reads address(this).balance and swaps native ETH. No function of PepesEarnIMD moves an ERC-20 the hook holds: its own fee flows are ERC-6909 claims inside the PoolManager (collectProtocolFees and flush burn claims), and there is no unwrap or sweep. The holders' 3% and the protocol's 1% of every offer-side sale are therefore locked permanently, and the contract cannot be changed after deployment. Merged from three specialist reports (two rated it medium, one low; kept at medium because the loss is permanent and the path is an ordinary marketplace flow). Fix that keeps the rule 'royalty value only reaches feeRecipient and holders': take the chain's WETH address as a constructor immutable and have convertRoyalties call WETH.withdraw(balance) before reading address(this).balance; and split any IMD the hook itself holds 1/4 to feeRecipient and 3/4 to the token followed by distribute() (outside an unlock, or inside the hook's own). Note on the specialist's attached test: it fails for the stated reason, but its second assertion (feeRecipient +1 IMD) would not hold after a correct fix because collectProtocolFees in the same test also pays 1 IMD of trade fees, so it is not attached here.

**Reproduction**

Unit-test setup, pool opened, alice bought $EARN with 100 IMD. mirror.royaltyInfo(1, 100e18) returns (hook, 4e18). A marketplace pays the royalty in the sale currency: imd.transfer(hook, 4e18) (same for 0.04 WETH on a 1 WETH offer). Then owner calls hook.convertRoyalties(0) and anyone calls hook.collectProtocolFees(imd). Expected: 1 IMD to feeRecipient, 3 IMD credited to holders, hook balance 0. Actual: convertRoyalties returns 0 (ethIn == 0), collectProtocolFees only pays pending trade fees, imd.balanceOf(hook) stays 4000000000000000000. Ran the specialist's test (RoyaltyTokenStuckProof): it fails with 'royalty IMD is stuck in the hook: 4000000000000000000 != 0'.

### 4. Low: Expiry boundary is inclusive: at exactly 30 days, rewards earned exactly 30 days ago (including those earned after the holder's last activity in the same second) are recycled

`contracts/src/earn/PepesEarnToken.sol:261`

```
uint256 magCut = magAt(block.timestamp - INACTIVITY_PERIOD);
```

Answer to 'can expiry take rewards earned in the last 30 days': only at this boundary. expiredRewardsOf treats a wallet as inactive from block.timestamp == lastActive + 30 days, and magAt(t) returns the per-share value after every distribution with time <= t (a second's checkpoint holds the value after the LAST distribution of that second). So a distribution in second t is treated as expired at second t + 30 days, and at lastActive + 30 days every distribution that happened in the same second as the last activity, after it, is recycled although the holder was never inactive for longer than 30 days with respect to it. Robinhood Chain produces several blocks per second, so a buy or claim followed by another trade's distribution in the same second is the normal case. One second earlier nothing is recyclable; the holder loses the reward if a recycler calls in exactly that window or later without the holder acting. Otherwise I found no path that recycles rewards younger than 30 days: every balance change (ERC-20 _transfer and mirror _transferFromNFT, including transfers to excluded addresses) goes through _moved and updates lastActive, and 'recent' rounds up. Fix: make the boundary exclusive on the holder's side, e.g. cut at magAt(block.timestamp - INACTIVITY_PERIOD - 1) and require block.timestamp > last + INACTIVITY_PERIOD, so a distribution in the cutoff second counts as recent. No repository test covers the exact boundary.

**Reproduction**

Unit-test setup at timestamp T (use vm.getBlockTimestamp(); with via_ir a cached block.timestamp gives wrong warps). Case 1: alice router.buy 100 IMD at T, bob router.buy 100 IMD in the same second (alice is credited 5.999999999999999999 IMD). vm.warp(T + 30 days - 1): expiredRewardsOf(alice) == 0. vm.warp(T + 30 days): expiredRewardsOf(alice) == 5999999999999999999 == withdrawableDividendOf(alice); carol calls recycle(alice) and alice's withdrawable becomes 0. Case 2: alice buys at T, bob buys at T + 1 day (alice earns 5.999999999999999999 IMD at T + 1 day). At T + 31 days - 1: expired == 0. At T + 31 days (the reward is exactly 30 days old): expired == 5999999999999999999. Expected: rewards no older than 30 days stay claimable. Actual: they move to buybackReserve.

### 5. Low: Mirror can be linked by anyone before the token is deployed (the deployer check compares a caller-supplied argument), blocking the launch deployment

`contracts/src/earn/PepesEarnMirror.sol:15`

```
constructor(address hook) DN404Mirror(msg.sender) {
```

The constructor comment says only the deploying account can link the mirror. DN404Mirror does not enforce that: its linkMirrorContract(address) fallback branch compares the calldata argument with the stored deployer and then sets baseERC20 = msg.sender. Anyone who passes the deployer's public address becomes the mirror's base token. The earn contracts have no deploy script or factory and the tests deploy mirror and token as two steps; if those are two transactions, an observer can link in between. The real PepesEarnToken constructor then reverts with LinkMirrorContractFailed and that mirror is permanently bound to the attacker's contract. No holder funds are at risk (nothing is live yet) and a correctly linked collection is unaffected; the cost is a failed launch and a retry that can be front-run again. Merged from two specialist reports. Fix: deploy mirror and token atomically in one transaction from a small deployer contract (it is msg.sender for both, so DN404's check still passes), or give the mirror the precomputed token address and require msg.sender == that address before linking.

**Reproduction**

Deployer D deploys m = new PepesEarnMirror(hook). Attacker contract H calls address(m).call(abi.encodeWithSelector(0x0f4599e5, D)). Expected (per the constructor comment): the call is rejected. Actual: it succeeds and m.baseERC20() == H; D's following new PepesEarnToken(hook, address(m), renderer, pepes, pepesRouter) reverts. Reproduced with a Foundry test on this commit in the unit-test setup (link succeeds, baseERC20 == hijacker, token constructor reverts).

### 6. Info: openPool does not check the token's buyback targets (pepes, pepesRouter), mirror, renderer or bytecode: the reserve's only exit is whatever the owner-chosen token hard-codes

`contracts/src/earn/PepesEarnIMD.sol:210`

```
t.hook() != address(this) || t.router() != router || t.ethRouter() != ethRouter
```

Trust assumption to document, not a post-launch owner power. openPool checks hook, routers, PoolManager, IMD, balance and total supply. The guarantee 'the reserve can only buy $Pepes and burn it' rests on the pepes and pepesRouter immutables of the token the owner passes in, and on that token being PepesEarnToken bytecode; none of this is checked on-chain. A token deployed with pepesRouter set to an owner-controlled contract passes openPool, and buybackAndBurnPepes then approves the reserve to that contract. After openPool nothing can change, so holders must verify these two addresses and the verified source before trading. Fix before deployment: make the $Pepes and v1 router addresses immutables of PepesEarnIMD and add t.pepes() != PEPES || t.pepesRouter() != PEPES_ROUTER to the BadToken check (or have the hook deploy the token itself), and publish 0xE2C46c7068566740A33A4C93f5445B07BCfE5644 / 0xA73604EA3C393B47573986ff9Ce5A9EAb61883dC for holders to compare.

**Reproduction**

The repository's own setUp shows it: contracts/test/PepesEarn.t.sol deploys PepesEarnToken(hook, mirror, renderer, MockPepes, MockPepesRouter), where MockPepesRouter.buy does imd.transferFrom(msg.sender, address(this), amountIn) and mints mock tokens, and hook.openPool(earn) succeeds. test_buyback_burnsPepesWithReserveOnly then moves the whole reserve's IMD to that arbitrary router contract. Expected for holders: openPool only accepts a token whose buyback goes to $Pepes 0xE2C4...5644 through the v1 router 0xA736...83dC. Actual: any pepes / pepesRouter pair is accepted.

### 7. Info: Buyback reserve and royalty ETH have no permissionless exit: both stay locked if the owner key is lost or the owner stops acting

`contracts/src/earn/PepesEarnToken.sol:293`

```
if (msg.sender != IEarnHook(hook).owner()) revert NotOwner();
```

Trust assumption. buybackReserve leaves only through buybackAndBurnPepes (owner of PepesEarnIMD) and royalty ETH only through convertRoyalties (onlyOwner). The contracts are immutable and only the current owner can start an ownership transfer, so a lost or inactive owner freezes every expired reward and every marketplace royalty. Holders' own claimable rewards are not affected. If the two conversions are bounded per call as suggested in the two sandwich findings, they can be made callable by anyone (optionally only after N days without an owner call), which removes this dependency without giving anyone a new destination for the funds.

**Reproduction**

State: buybackReserve > 0 after a recycle and 1 ETH of royalties in the hook; the owner never calls. Any other address calls earn.buybackAndBurnPepes(reserve, 0, now) -> reverts NotOwner(); hook.convertRoyalties(0) -> reverts NotOwner() (both asserted by the repository tests test_buyback_burnsPepesWithReserveOnly and test_royalties_convertedToImdAndSplit). Expected by the design intent: expired rewards are eventually burned as $Pepes and royalties reach holders. Actual: no caller other than the owner can ever move them.

### 8. Info: Anyone can reset any holder's 30-day timer for free with a zero-amount transferFrom, so expiry can be suppressed for all holders at gas cost only

`contracts/src/earn/PepesEarnToken.sol:190`

```
lastActive[from] = block.timestamp;
```

The brief accepts that sending dust resets the recipient's timer. The reach is wider: _moved also marks `from` active, and DN404's transferFrom(from, to, 0) needs no allowance, so a third party can reset any holder's lastActive without holding or spending $EARN. A keeper calling it for every holder once per 30 days keeps expiredRewardsOf at zero for everyone, and the buyback reserve never fills. It never takes anything from a holder (it only delays expiry), hence informational. Fix if expiry should be enforceable: in _moved skip the lastActive updates when amount == 0, and consider marking only the initiating side active (the sender on transfers, the caller on claim).

**Reproduction**

Unit-test setup: alice and bob each router.buy 100 IMD; warp 31 days; expiredRewardsOf(alice) == 5999999999999999999. dan, who has no allowance from alice and holds no $EARN, calls earn.transferFrom(alice, dan, 0). Expected: alice's expired rewards remain recyclable. Actual: the call succeeds, lastActive[alice] == block.timestamp, expiredRewardsOf(alice) == 0 and recycle(alice) returns 0.

### 9. Info: At most 1,999 NFTs can ever exist: the liquidity buffer and rounding dust go to the burn address, so the 2,000th whole token cannot be assembled

`contracts/src/earn/PepesEarnIMD.sol:253`

```
uint256 amount = TOTAL_SUPPLY - LIQUIDITY_BUFFER;
```

openPool adds TOTAL_SUPPLY - 1e9 wei (less rounding) as liquidity and line 267 sends the remainder to 0x...dEaD. The pool therefore holds strictly less than 2,000e18 $EARN, and the last tokens sit at the far end of a range that runs to the maximum usable tick, so the supply outside the pool can never reach 2,000 whole tokens. No funds are at risk; it matters because the on-chain description ('2,000 on-chain Pepes' in metadata()) and any rarity statement that counts 2,000 pieces cannot be changed after deployment. Keeping single-sided full-supply liquidity needs the buffer, so the practical fix is wording: 'up to 1,999 NFTs'.

**Reproduction**

After hook.openPool(token): earn.balanceOf(0x...dEaD) = d >= 1e9 wei and earn.balanceOf(poolManager) = 2000e18 - d (test_openPool_locksWholeSupplyInPool asserts the pool balance is within 1e9 of the supply and the hook keeps 0). For any sequence of buys, the sum of balances outside the pool and the burn address is <= 2000e18 - d < 2000e18, so floor(sum / 1e18) <= 1,999 NFTs. Expected by the description: 2,000 NFTs obtainable. Actual: at most 1,999.

### 10. Info: sellWithPermit / sellForEthWithPermit cannot be used for $EARN: DN404 has no EIP-2612 permit, so the routers only work after a separate approve

`contracts/src/PepesFamilyRouter.sol:128`

```
PermitHelper.permit(token, tokenAmount, deadline, v, r, s);
```

The routers are reused unchanged. PermitHelper.permit calls token.permit(...); PepesEarnToken inherits DN404, which has no permit, so the call reaches DN404's fallback and reverts, and the trade proceeds only if an allowance already exists. No funds are at risk; a front end that offers the gasless-approval sell flow for $EARN will produce reverting transactions. Fix: disable the permit path for this collection in the site (or add EIP-2612 to the token before deployment).

**Reproduction**

Unit-test setup: alice buys $EARN with 100 IMD and sets earn.approve(router, 0). alice calls router.sellWithPermit(earn, 1e18, 0, block.timestamp, 27, bytes32(1), bytes32(1)). Expected (router docs): the permit is applied and 1 $EARN is sold. Actual: the call reverts (permit selector not recognised by the token, allowance 0). The same sale succeeds only after a separate earn.approve(router, amount) transaction.

---

Judge's submission `2f104a270c5ce2a6c58113d932ea9285ae533d519cd891949f31184b82609996`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
