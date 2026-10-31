# Audit report

> Audit contracts/SqueekPot.sol (version 2, live on Sepolia at 0x845AC45012405B8Fa1Ff017320304b665b915F86). Read contracts/AUDIT-SCOPE.md first: it describes the intended behaviour and the trust assumptions we accept. Look hardest at: funds can never be lost, locked or taken; no double refunds or payouts; settle/void/refund timing edges (lock time, endTime + 3 days); reentrancy and the 30,000-gas payout stipend in _pay; and anything the owner or resolver can do beyond the scope. SqueekPotV1.sol is lower priority.

| | |
|---|---|
| Repository | https://github.com/StasBokhan/squeek-picks.git |
| Commit | `6ba3b13ee924403e79007a1c666472f67db51ed8` |
| Job | `06d98304-78a4-4089-815a-2be96ef1f7c5` |
| Judged | 2026-10-31 14:10 UTC |
| Findings | 3 low · 4 info |

Four agents audited the code as it is at `6ba3b13`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Low: refund and withdrawOwed pay only msg.sender and revert on failure, so a contract player that cannot receive plain ETH has its refund or owed payout locked forever

`contracts/SqueekPot.sol:146`

```
        (bool ok, ) = msg.sender.call{value: amount}("");
        require(ok, "send failed");
```

refund() (lines 146-147) and withdrawOwed() (lines 156-157) send to msg.sender only and revert the whole call if the send fails. There is no way to name another recipient. A ticket can be bought by any contract account (a smart wallet or bot contract that makes arbitrary calls but has no payable receive/fallback, or whose receive reverts). If that night is voided or times out, refund() always reverts with 'send failed' and the ticket price can never leave the contract. If such a contract wins, _pay's 30,000-gas send fails and the amount is credited to owed as designed, but withdrawOwed() then also always reverts, so the owed balance is stuck too. Nobody, including the owner, can move it. This contradicts scope item 1 ('every wei ... stays claimable in owed') for that class of player; for an EOA or any contract with a working receive it holds. The same two functions in contracts/SqueekPotV1.sol (lines 128-129 and 138-139) have the same shape. Minimal fix that keeps the design: add a recipient parameter (refundTo(night, to) / withdrawOwedTo(to), with the msg.sender versions kept as wrappers), so a contract player can route the ETH to an address that accepts it. Merged from the economics specialist; reproduced here.

**Reproduction**

Chain 31337, vm.warp(1_700_000_000), pot = new SqueekPot(0.01 ether, resolver). Contract W has exec(target,value,data) and receive() { revert(); }. W.exec(pot, 0.01 ether, buyTicket(openNight(),1,1,true)) succeeds (ticket 0). Warp to endTime(night); resolver calls voidNight(night). W.exec(pot, 0, refund(night)). Expected: W gets 0.01 ether back, or can name a recipient. Actual: the call returns ok == false ('send failed') every time and address(pot).balance stays 0.01 ether. Variant: W and an EOA each buy one ticket; resolver settles winners [0] bps [10000]; owed[W] == 0.02 ether; W.exec(pot, 0, withdrawOwed()) returns ok == false every time. Both cases are test_contractPlayerRefundLocked and test_contractPlayerOwedLocked in test/scratch/Review.t.sol (both pass, i.e. the lock is confirmed).

### 2. Low: _pay copies the winner's return data, so a winning contract can raise settle's gas cost about 5x within the 30,000-gas stipend (return-data bomb)

`contracts/SqueekPot.sol:252`

```
        (bool ok, ) = to.call{value: amount, gas: 30_000}("");
```

The 30,000-gas stipend bounds what the winner can spend, but not what settle() itself spends afterwards. For a low-level call with a discarded return value, solc 0.8.24 still copies the full returndata into memory (RETURNDATACOPY) and advances the free-memory pointer, so the copies accumulate across the up-to-10-winner loop and memory expansion cost grows quadratically. Within 30,000 gas a receive() can `return(0, 96000)`. The winner's payout succeeds, so the attacker loses nothing; the resolver (the payout bot, which pays gas) bears the cost. Measured: settle with 10 such winners costs 2,448,860 gas against 477,954 gas when the same 10 winners revert instead. Funds are never lost: every payout still either sends or goes to owed, and the bot in settler/settle.mjs uses ethers' default gas estimation with no fixed gas limit, so settle still lands, just about 5x more expensively, for every night such tickets win. If the bot were ever given a fixed gas cap below the inflated cost, settle would fail until the 3-day window closes and the night would fall through to refunds, taking the prize from honest co-winners. contracts/SqueekPotV1.sol line 229 has the same pattern. Minimal fix that keeps the stipend and the owed fallback: make the send in assembly without copying return data, e.g. `assembly { ok := call(30000, to, amount, 0, 0, 0, 0) }`. Merged from the math and economics specialists (one finding each, same mechanism, same line); reproduced here with the figures above.

**Reproduction**

Chain 31337, pot = new SqueekPot(0.01 ether, resolver). Deploy 10 Bomb contracts whose receive() is `assembly { return(0, 96000) }`; each buys one ticket for openNight() (tickets 0..9). Warp to endTime(night). Resolver calls settle(night, [0..9], [1000 x10]) and the gas consumed is measured with gasleft(). Expected: roughly the same as a settle whose winners revert or are EOAs (a few hundred thousand gas), since the stipend should bound the per-winner cost. Actual: 2,448,860 gas, against 477,954 gas for the identical run where receive() reverts instead (test_returndataBombGas in test/scratch/Review.t.sol, which asserts the bomb run costs more than 4x the revert run and passes).

### 3. Low: setOwner is a single-step handover: a mistyped address permanently removes the only admin role, after which the resolver can never be rotated

`contracts/SqueekPot.sol:223`

```
        owner = next;
```

setOwner writes the new owner immediately with only a non-zero check; there is no pending/accept step. The owner is the only role that can rotate the resolver (setResolver) and the ticket price. A typo, a wallet from the wrong network, or a contract that cannot send transactions leaves the contract with no admin for good. The owner holds no fund-moving power, so player funds are not directly at risk: unsettled nights still time out and refund after endTime + 3 days. The residual risk is that the only defence against a lost or leaked resolver key (setResolver) is gone: a lost resolver means every future night with tickets can only end in a timeout refund, and a leaked resolver can settle every subsequent night to its own ticket within the documented trust, with no on-chain remedy except redeploying. setResolver has the same single-step shape but is recoverable while the owner is intact. On the live Sepolia deployment owner and resolver are different EOAs, so the owner key is the single point of recovery. This is a trust-assumption gap, not a permission bypass. Fix that keeps the agreed design: store pendingOwner in setOwner and let the new address call acceptOwner(); setResolver can stay single-step. Merged from the permissions specialist (low) and the flow specialist (info); reproduced here.

**Reproduction**

State: pot deployed with owner = deployer, resolver = 0xB0B. Input: owner calls setOwner(0x000000000000000000000000000000000000dEaD). Expected (two-step design): nothing changes until 0xdead accepts. Actual: owner becomes 0xdead at once; afterwards setResolver(0x1) and setOwner(deployer) from the deployer revert with NotOwner() and no function can restore the role (test_setOwnerTypoLocksAdmin in test/scratch/Review.t.sol).

### 4. Info: Trust assumption to record: the resolver, and the owner via setResolver in two transactions, can direct any night's whole pot to a ticket they hold

`contracts/SqueekPot.sol:166`

```
    function settle(uint32 night, uint256[] calldata winners, uint16[] calldata bps) external onlyResolver nonReentrant {
```

Not a permission bypass: settle is correctly restricted to the resolver and the scope accepts that the resolver chooses winners and shares without on-chain checking. It is recorded so the stated guarantee is precise. settle() only checks that each winner is an existing, non-duplicate ticket of the night and that the shares total 10,000. So the practical guarantee is not 'nobody can withdraw the pot' but 'the resolver can pay any night's whole pot to any ticket of that night, including one it bought itself, for the price of one ticket'. Because setResolver takes effect immediately, the owner has the same power in two transactions, even though the scope lists the owner as unable to take funds in any other way. On Sepolia today owner and resolver are distinct EOAs, so each key individually controls every pot. The only on-chain signals players have are ResolverChanged and NightSettled, and a settle cannot be undone. No code change is required for the accepted testnet design. Narrowing it is a scope decision (for example a delay between setResolver and the first settle, or committing the night's result hash before payout). Merged from the permissions and economics specialists; reproduced here.

**Reproduction**

State: night d has one ticket each from p1, p2, p3 at 0.01 ETH, and the owner buys ticket 3 with a wallet it controls. Input after endTime(d): owner calls setResolver(owner), then settle(d, [3], [10000]). Expected under a literal reading of 'nobody, the owner and resolver included, should be able to withdraw the pot': not possible. Actual: the owner's wallet receives the whole 0.04 ETH pot and all guards pass (test_ownerTakesPotViaResolver in test/scratch/Review.t.sol). The resolver key alone can do the same without the setResolver step.

### 5. Info: getNight quotes the global ticketPrice before a night has tickets, so an owner setTicketPrice mined before the first ticket makes that purchase revert

`contracts/SqueekPot.sol:235`

```
        return (n.price == 0 ? ticketPrice : n.price, n.pot, n.status, n.tickets);
```

getNight returns the global ticketPrice as the night's price while the night has no tickets, but buyTicket only fixes n.price at the first purchase (line 101) and requires msg.value == n.price exactly (line 102). Between a buyer reading the quote and the purchase landing, the owner can change ticketPrice, so the buyer's transaction reverts rather than over- or under-paying. No funds are lost or taken and, once any ticket exists, later setTicketPrice calls do not affect that night (verified), so this is within the owner powers the scope accepts. Recorded because it is the one place the owner can interfere with a player action and because a page that trusts getNight before the first ticket can show a stale price. If the requester wants to remove even this, buyTicket could take a maxPrice argument, or the page can re-read ticketPrice right before sending. Kept from the permissions specialist; reproduced here.

**Reproduction**

State: night d has no tickets, ticketPrice = 0.01 ETH; getNight(d).price returns 0.01 ETH. Input: owner's setTicketPrice(0.02 ether) is mined, then p1's buyTicket{value: 0.01 ether}(d, 1, 1, true). Expected from the quote: ticket bought at 0.01 ETH. Actual: revert 'wrong ticket price'. Then p1 buys at 0.02 ETH, owner sets 0.05 ETH, and p2 still buys at 0.02 ETH, confirming the price is fixed by the first ticket (test_priceFrontRunFirstTicket in test/scratch/Review.t.sol).

### 6. Info: openNight() underflows (Panic 0x11) when block.timestamp < 12 hours on the local chain the constructor explicitly supports

`contracts/SqueekPot.sol:90`

```
    function openNight() public view returns (uint32) { return uint32((block.timestamp - LOCK_OFFSET) / DAY + 1); }
```

The constructor allows chain id 31337 for local testing, but openNight() subtracts LOCK_OFFSET (43,200) from block.timestamp with checked arithmetic. Foundry and anvil start at block.timestamp == 1 unless warped, so on a fresh local chain openNight(), buyTicket() and changePicks() all revert with an arithmetic panic rather than a readable message. Unreachable on Sepolia (timestamps are about 1.76e9), so no impact on the live deployment; it only makes the contract unusable in the default local environment without a warp and gives no hint at the cause. Minimal fix: compute `(block.timestamp + DAY - LOCK_OFFSET) / DAY` (identical result for every real timestamp, no underflow) or add a require with a message. Kept from the flow specialist; reproduced here.

**Reproduction**

Chain 31337, vm.warp(1), pot = new SqueekPot(1e16, resolver). Call openNight(). Expected: a night number or a readable revert. Actual: revert with Panic(0x11). With vm.warp(43200) openNight() returns 1 (test_openNightUnderflowAtGenesis in test/scratch/Review.t.sol).

### 7. Info: No test suite in the repository: the timing, double-refund, reentrancy and conservation edges in AUDIT-SCOPE.md are not pinned by any test the author can rerun

`contracts/compile.cjs:3`

```
//   npm install solc@0.8.24  &&  node contracts/compile.cjs
```

The repository compiles the contract with a plain solc script and has no test directory, foundry.toml or hardhat config, so none of the edges the scope asks about are covered by a test that runs in the project. During this review each of them was exercised with Foundry against the current source and all behaved as specified: buy and changePicks succeed at lockTime - 1 and revert with 'night not open' at lockTime; settle reverts at endTime - 1 ('night not over') and at endTime + 3 days ('refund window open'); refund reverts at endTime + 3 days - 1 and succeeds at endTime + 3 days; a second refund reverts 'nothing to refund'; a settled night cannot be refunded or voided; voidNight after the timeout with some tickets already refunded still lets the rest refund, leaves a zero balance and keeps settle blocked; winners that reenter withdrawOwed, burn all 30,000 gas, or revert are credited to owed and the contract balance equals the sum of owed; a refund callback that reenters refund reverts the whole refund with 'send failed'; and a fuzz over 2 to 12 tickets with any two-way bps split leaves the contract balance at exactly zero. Suggest committing these cases (test/scratch/Review.t.sol from this review can be the starting point) so a future change to the refund window, the stipend or the share maths cannot silently break them. Merged from the permissions and flow specialists; reproduced here.

**Reproduction**

State: a fresh checkout. Input: `ls test` and a search for forge, hardhat or mocha in any package.json. Expected: a runnable suite covering scope items 1 to 4. Actual: no test directory exists and the only dependencies are the wallet/ and settler/ bots; contracts/compile.cjs compiles without testing. The twelve-test scratch suite described above passes against the current source.

---

Judge's submission `d4f6d10f8332d35309d531c850c0ce1a028bcda854524247bfb402abd25bb8e6`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
