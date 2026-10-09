# Audit report

> Project: PepesFamily launchpad v5, re-check after audit 8f96baf6
> Repo: github.com/0xtenang/PepesFamily (commit 5e84e99)
> Scope: contracts/src/PepesFamily.sol, contracts/src/PepesFamilyLens.sol, contracts/src/PepesFamilyRouter.sol
> Tests: contracts/test/PepesFamily.t.sol (section “v5 audit (8f96baf6)”), contracts/test/Fork.t.sol
>
> Changes since 8f96baf6
>
> Finding 1: afterSwap reverts with PartialFill unless the pool traded the whole specified amount, net of the specified-side fee or burn taken in beforeSwap (FEE_SLOT + BURN_SLOT).
> Findings 2 and 3: _burn mints ERC-6909 claims of the token to the launchpad (pendingBurn). flush(token) burns those claims and takes the tokens to 0x…dEaD, then pays holder fees. Mid-unlock, only our routers may flush.
> Finding 4: creatorFee and holderFee are computed from their own bps; the protocol takes the remainder.
> Finding 5: lens paging uses limit > n - offset.
> Finding 6: marketCap moved to the lens, using supply minus totalBurned minus pendingBurn.
> Finding 7: creator payout is two-step: setCreatorPayout proposes (address(0) cancels), and acceptCreatorPayout must be called by the proposed address.
> Please check
>
> Can the full-fill check be bypassed, or does it reject any legitimate full-fill swap? Think about rounding in exact-in and exact-out, and tiny amounts.
> Are the token claims always backed: claims of each token equal pendingBurn[token]? Does flush mid-unlock from our routers always have the tokens to take?
> Could pending burns be stuck or griefed? Does flush with no holder fees but a pending burn behave correctly?
> Any regression of v4 guarantees or of earlier findings.

| | |
|---|---|
| Repository | https://github.com/0xtenang/PepesFamily.git |
| Commit | `5e84e99a980828ee6741c9300045b7c9be5bfd61` |
| Job | `f963ea4d-f3a8-4ff7-9f13-1d330a275035` |
| Judged | 2026-10-09 07:21 UTC |
| Findings | 3 info |

Four agents audited the code as it is at `5e84e99`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Info: Stated invariant 'token claims == pendingBurn' (and 'IMD claims == pending fees') is only '>=': anyone can mint or transfer ERC-6909 claims to the launchpad, and _flush/_collect burn only the accounte

`contracts/src/PepesFamily.sol:529`

```
            poolManager.burn(address(this), Currency.wrap(token).toId(), burn);
```

Merged from audit_math, audit_flow and audit_economics, which reported the same mechanism. AUDIT.md section 2 states the v5 invariant as an equality (the launchpad's ERC-6909 claims of each token equal pendingBurn[token]; its IMD claims equal pendingProtocolFees + sum pendingHolderFees + sum pendingCreatorFees) and the repository test helper _assertClaimsBacked (test/PepesFamily.t.sol:1237-1248) asserts it with assertEq. The launchpad itself keeps the equality on every path I exercised: _burn adds exactly the minted amount to pendingBurn (line 464-465), _flush burns exactly pendingBurn (525-530), _chargeFee mints exactly the fee it books (454-457), and _collect/_collectCreator burn exactly the booked amounts. I confirmed claims == pendingBurn and IMD claims == booked fees after every step of 512 random sequences mixing router buys/sells, third-party exact-in/exact-out buys and sells, standalone flush and both collects, for splits (0,0,300), (100,100,100), (50,150,100) in both currency orders, and for amounts 1-9601 wei in all four swap kinds. What the contract cannot prevent is a third party crediting claims to it: PoolManager.mint(to, id, amount) and the ERC-6909 transfer let any locker mint or move claims of any currency to any address, including the launchpad. After that the launchpad's claim balance exceeds the booked amount and no code path ever burns or takes the surplus, because _flush, _collect and _collectCreator only burn what is booked; the donated claims (and the tokens or IMD backing them in the PoolManager) are stranded forever. Impact: none on solvency or on any user. The direction that matters for safety, claims >= booked, always holds, the launchpad never pays out more than it owes, the lens marketCap reads pendingBurn rather than claim balances so it is unaffected, and only the donor loses anything. It is reported so the invariant is documented and tested as '>=' (or 'claims - booked is a non-negative constant that only donations change'), so a future stateful/invariant fuzz with external actors, which AUDIT.md section 9 asks for, does not fail on a harmless donation, and so nobody later 'fixes' a surplus of IMD claims by paying it out. Fix: restate the invariant in AUDIT.md section 2 and change the two assertEq in _assertClaimsBacked to assertGe (or assert the difference is constant); optionally, if exact equality of token claims is wanted, have _flush burn poolManager.balanceOf(address(this), id) instead of pendingBurn and take that amount to DEAD, which is a sensible destination for donated token claims but not for donated IMD claims, so leave the IMD side as '>='.

**Reproduction**

State: any v5 token T launched with FeeSplit(0,0,300) and one buy of 20 IMD through PepesFamilyRouter, so the router's inline flush leaves pendingBurn[T] == 0 and the launchpad's claims of T == 0. Input: a contract D holding 1e18 T calls poolManager.unlock and in its unlockCallback does sync(T); T.transfer(poolManager, 1e18); settle(); mint(address(pad), uint256(uint160(T)), 1e18). Expected per AUDIT.md section 2 and _assertClaimsBacked: poolManager.balanceOf(pad, uint256(uint160(T))) == pad.pendingBurn(T) == 0. Actual: poolManager.balanceOf(pad, id(T)) == 1e18 while pendingBurn(T) == 0; pad.flush(T) returns at line 473 (nothing booked) and leaves the 1e18 claims; a further router buy of 1 IMD runs _flush normally and still leaves 1e18 claims; no function can ever burn them. Verified with a scratch Foundry test (test_spec_donatedClaimsExceedPendingBurn) that passes against commit 5e84e99. The same holds for IMD claims via mint(pad, id(IMD), x).

### 2. Info: Router: the ETH refund branch and its comment are dead in v5 (quote is always IMD, and a swap that reaches the end of the curve now reverts PartialFill instead of leaving a remainder); the buy/launch

`contracts/src/PepesFamilyRouter.sol:171`

```
        // Refund unspent ETH (only possible if the swap hit the end of the curve).
        if (payingEth && address(this).balance > 0) address(0).transferOut(msg.sender, address(this).balance);
```

From audit_permissions, reproduced. payingEth (line 158) is true only when the launch's quote is address(0), but PepesFamily._launch reverts UnsupportedQuote for any quote other than IMD (PepesFamily.sol:272), so pad.launches(token).quote is IMD for every token and the branch at line 172 can never execute; msg.value on an IMD trade is rejected at line 159, so no ETH can ever sit in the router. The comment's premise is also stale since finding 1 of audit 8f96baf6: a swap stopped by its price limit (including the end of the curve) now reverts in afterSwap with PartialFill (PepesFamily.sol:400) instead of leaving an unspent remainder, so even with an ETH quote there would be nothing to refund. The NatSpec of buy (line 121, 'send ETH as msg.value, or approve this router for IMD') and of launch (line 92, 'For IMD launches approve this router') likewise still describe a two-quote router. Dead code and misleading comments only; no funds are at risk. Fix: drop payingEth and the refund branch, make the `payable`/msg.value check a plain `if (msg.value != 0) revert BadAmount()`, and reword the three comments, or state explicitly that the branch is kept for a future ETH quote.

**Reproduction**

Call router.launch("X","X","",address(0),0,0) or pad.launchWithSplit("X","X","",address(0),FeeSplit(0,300,0)): both revert UnsupportedQuote (repo test test_onlyImd; scratch test test_spec_routerEthBranchDead), so every launched token has quote == IMD and payingEth is false on every call to _swap; router.buy{value: 1}(token, 1e18, 0, deadline) on an IMD token reverts BadAmount at line 159. Expected per the comment at line 171: a refund path for ETH left over when a swap hits the end of the curve. Actual: the branch is unreachable, and such a swap reverts with PartialFill (repo test test_v5audit_partialFillsRevert).

### 3. Info: Test gap: the PartialFill regression test covers only the quote-is-currency0 order, and no test asserts that legitimate exact-out swaps pass the full-fill check in either order

`contracts/test/PepesFamily.t.sol:1330`

```
        PadToken t = _launchSplit(0, 150, 150, true);
```

From audit_math, reproduced as a coverage gap, not a code defect. test_v5audit_partialFillsRevert launches with quoteIsCurrency0 == true only, so the four PartialFill cases (exact-in/out x buy/sell) are checked for one orientation of the sign-flipping logic in afterSwap (quoteSpecified = (exactIn == zeroForOne) == quoteIs0 at PepesFamily.sol:390, and q/t picked from amount0/amount1 at 382-383). The other orientation, which every launch whose token address sorts below IMD gets, has no partial-fill test, and the trailing 'a limit that is never reached still trades' assertion is exact-in only; the committed suite's exact-out swaps all go through test_split_feesForEverySwapKind and testFuzz_split with open limits, so a regression that made the check reject full exact-out fills in the token-is-currency0 order would only show up there indirectly. I verified independently that the check is correct in both orders: with a limit 0.1% past spot every kind reverts in the token-is-currency0 order too, and with the open limit exact-in buy/sell and exact-out buy/sell of 1, 2, 3, 7, 23, 24, 25, 26, 99, 100, 101, 9599, 9600 and 9601 wei fill without PartialFill for splits (0,300,0), (0,0,300), (100,100,100) and (200,0,100) in both orders, with claims equal to the books after each; after a full exit (price on the start tick, no active liquidity) a buy still fills in both orders. The pool's delta passed to afterSwap has specified side equal to amountToSwap minus the unfilled remainder (v4-core Pool.sol:453-461), so the two inequalities at PepesFamily.sol:400 are true exactly when the remainder is non-zero. Fix: loop the launch over both orders as test_split_feesForEverySwapKind does (o < 2, with buy = zeroForOne flipped when the token is currency0), and add explicit open-limit exact-out buy and sell swaps after the reverting cases.

**Reproduction**

Run the existing test: it only ever launches _launchSplit(0, 150, 150, true). Change the argument to false and flip the zfo table (buy is zeroForOne == false when the token is currency0): nothing in the committed suite asserts those four reverts or an exact-out full fill for that orientation. A scratch test (test_q1_partialFillRevertsTokenIsCurrency0 and test_q1_tinyFullFillsPass, both orders, exact-in and exact-out, buy and sell, limit 0.1% past spot and open limits) passes on commit 5e84e99, confirming the behaviour, not the coverage.

---

Judge's submission `17af39026248d7af87bb65570a84031b711b586323ac12adc783046ff40a0535`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
