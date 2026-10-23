# Audit report

> Audit the contracts in 0xtenang/Runner as they are.

| | |
|---|---|
| Repository | https://github.com/0xtenang/Runner.git |
| Commit | `9f1a6892d7fce7bb549e1c5589841e6267b19461` |
| Job | `28c0a5e2-0f75-404e-a9d9-37a528840d88` |
| Judged | 2026-10-23 19:14 UTC |
| Findings | 7 low · 1 info |

Four agents audited the code as it is at `9f1a689`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Low: Self-transfer (transfer or transferFrom with from == to) records a false daily minimum and strips the wallet's holder-reward weight for the day

`contracts/RunnerToken.sol:535`

```
        _track(from, fromBal, fromBal - value, today);
```

_move() has no from == to short-circuit. It debits `from`, calls _track() with newBal = fromBal - value (which lowers today's checkpoint minBalance, lowers eligibleSupply and subtracts the drop from _days[today].shares), and only then credits `to` and tracks the raise. The balance ends unchanged, but a checkpoint's minBalance can only fall, so the wallet's lowest balance for the day is now recorded as balance - value. The documented rule (contract header, README) is 'the lowest balance it held that day'; the wallet never held less. eligibleBalanceOn(wallet, today) therefore returns 0 when value >= balance - 300,000 (and balance - value otherwise), and the wallet loses that share of today's 2% holder tax; the unclaimed slice is later swept to the protocol wallet. Trigger paths: a wallet's own 'send to self' (some wallets and UIs do this as a test), or any approved spender calling transferFrom(holder, holder, v), which needs only an allowance of v: a spender with a 1 wei allowance zeroes a 300,000 RUNNER holder's weight for the day without moving a token. The existing test 'self-transfer keeps balance' (tests/token.test.mjs:85) asserts only the balance, so the suite does not catch it. Reported by three specialists (flow, math, permissions); merged here. Fix: in _move(), after the InsufficientBalance check, `if (from == to) { emit Transfer(from, to, value); return; }` so checkpoints only see real balance changes (no economic rule changes), or compute the net balance change per address before calling _track().

**Reproduction**

Day D: team transfers 1,000,000 RUNNER to alice. Day D+1 (any time): eligibleBalanceOn(alice, D+1) == 1,000,000e18. alice calls transfer(alice, 1_000_000e18). Expected: balanceOf(alice) == 1,000,000e18 and eligibleBalanceOn(alice, D+1) still 1,000,000e18. Actual: balanceOf(alice) == 1,000,000e18 but eligibleBalanceOn(alice, D+1) == 0, and dayInfo(D+1).shares drops by 1,000,000e18. Variant: alice.approve(spender, 1); spender calls transferFrom(alice, alice, 1): eligibleBalanceOn(alice, D+1) becomes 999,999.999999999999999999e18 (a 300,000e18 holder would drop to 0). Foundry: test/scratch/SelfTransferMin.t.sol, both tests fail on the current code ('0 != 1000000000000000000000000' and '999999999999999999999999 != 1000000000000000000000000') and pass with the from == to short-circuit.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.24;

import "forge-std/Test.sol";
import "contracts/RunnerToken.sol";

/// A transfer with from == to leaves the balance unchanged, so the wallet's lowest balance for
/// the day must not change either. On the current code _move() debits and checkpoints the sender
/// before crediting it back, so the checkpoint records a dip that never happened and the wallet
/// loses its holder-reward weight for the day.
contract SelfTransferMinTest is Test {
    RunnerToken token;
    address owner = address(0xA11CE);
    address liq = address(0xB0B);
    address team = address(0xCAFE);
    address alice = address(0xA1);
    address spender = address(0xB2);
    uint256 constant DAY = 1 days;
    uint256 day0;

    function setUp() public {
        vm.warp(20_500 * DAY + 3600);
        day0 = block.timestamp / DAY;
        token = new RunnerToken(owner, liq, team);
        vm.prank(team);
        token.transfer(alice, 1_000_000 ether);
    }

    function test_selfTransferKeepsDayMinimum() public {
        uint256 d1 = day0 + 1;
        vm.warp(d1 * DAY + 10);
        assertEq(token.eligibleBalanceOn(alice, d1), 1_000_000 ether);

        vm.prank(alice);
        token.transfer(alice, 1_000_000 ether);

        assertEq(token.balanceOf(alice), 1_000_000 ether);
        assertEq(token.eligibleBalanceOn(alice, d1), 1_000_000 ether, "self-transfer must not lower the day minimum");
    }

    function test_transferFromSelfKeepsDayMinimum() public {
        uint256 d1 = day0 + 1;
        vm.warp(d1 * DAY + 10);
        vm.prank(alice);
        token.approve(spender, 1);

        vm.prank(spender);
        token.transferFrom(alice, alice, 1);

        assertEq(token.balanceOf(alice), 1_000_000 ether);
        assertEq(token.eligibleBalanceOn(alice, d1), 1_000_000 ether, "transferFrom(self, self) must not lower the day minimum");
    }
}
```

### 2. Low: addPair() excludes a pool from holder rewards retroactively, but past days' share totals keep its weight: holders of those days are diluted and the pool's slice is stranded for the protocol sweep

`contracts/RunnerToken.sol:266`

```
        if (excludedFromHolderRewards[holder]) return 0;
```

_exclude() (lines 568-577, called from addPair) removes the newly registered pool's balance only from today's _days[today].shares and from eligibleSupply. eligibleBalanceOn() however reads the current exclusion flag for every day, so for the up-to-7 still-claimable days before registration it returns 0 for the pool while those days' frozen share totals still contain the pool's balance. The sum of claimable weights is then strictly below _days[d].shares: every real holder's share for those days is divided by a denominator that includes the pool, and the pool's slice of that day's holder tax can be claimed by nobody; sweepExpired() sends it to protocolWallet after the window. Preconditions are normal operation: a contract that already held >= 300,000 RUNNER at the start of a day on which a registered pool produced holder tax, and that is registered on a later day (a second DEX pool; or liquidity added to a pool the day before it is registered, which the admin flow 'add liquidity, then register' makes easy). Reported by the math and permissions specialists; merged here. Fix that keeps the design: in _exclude(), for each still-claimable day d in [today-7, today-1] subtract eligibleBalanceOn(account, d) from _days[d].shares before setting the flag (bounded loop of 7). Alternative: store an excludedFromDay and have eligibleBalanceOn() return 0 only for day >= excludedFromDay, which keeps the pool's past weight claimable by the pool itself. There is no on-chain way to repair past days once rewards were recorded, so the admin tooling should also refuse or warn when the pool's balance is already >= MIN_HOLDING on an earlier day.

**Reproduction**

Deploy RunnerToken(owner, liq, team) on day D at 01:00 UTC. Day D: liq transfers 10M to poolA, owner addPair(poolA); team transfers 1,000,000 to holder; liq transfers 50M to poolB (a pool contract that is not yet registered). Day D+1: poolA sends 1,000,000 to a buyer (taxed): dayInfo(D+1) == (shares 190M including poolB's 50M, rewards 20,000e18). Day D+2: holderClaimable(holder) == 20,000e18 * 1M / 190M. Owner calls addPair(poolB). Expected: either poolB keeps its weight for D+1, or D+1's shares drop to 140M so claimable weights add up to the share total. Actual: eligibleBalanceOn(poolB, D+1) == 0 while dayInfo(D+1).shares stays 190M; the sum of eligibleBalanceOn over all wallets for D+1 is 140M; the 50M/190M slice (5,263e18) of day D+1's tax is unclaimable and goes to protocolWallet on sweepExpired after day D+8. Foundry: test/scratch/RetroactivePairExclusion.t.sol fails on the current code with 'day-1 claimable weights no longer add up to its share total: 140000000000000000000000000 != 190000000000000000000000000' and passes once _exclude() subtracts the pool's past-day weights (checked against a patched copy). The permissions specialist's proof was run and fails for the stated reason, but it also asserts that the share total stays unchanged while the pool's weight is 0, which no fix can satisfy, so it is replaced.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.24;

import "forge-std/Test.sol";
import "contracts/RunnerToken.sol";

/// Minimal pool: reports RUNNER as token0 so addPair accepts it, and can send tokens out.
contract MockPool {
    address public token0;
    address public token1 = address(1);
    constructor(address t) { token0 = t; }
    function send(address t, address to, uint256 a) external { RunnerToken(t).transfer(to, a); }
}

/// addPair() excludes the new pool from holder rewards for every day (eligibleBalanceOn reads the
/// current flag), but the share totals of still-claimable past days keep the pool's balance.
/// Invariant that must hold for every claimable day: the sum of eligibleBalanceOn over all
/// wallets that held tokens equals the day's share total, otherwise part of the day's holder tax
/// can be claimed by nobody and every other holder is diluted.
contract RetroactivePairExclusionTest is Test {
    RunnerToken token;
    address owner = address(0xA11CE);
    address liq = address(0xB0B);
    address team = address(0xCAFE);
    address holder = address(0xD00D);
    address buyer = address(0xEEEE);
    MockPool poolA;
    MockPool poolB;

    uint256 constant DAY = 1 days;

    function setUp() public {
        vm.warp(20_500 * DAY + 3600);
        token = new RunnerToken(owner, liq, team);
        poolA = new MockPool(address(token));
        poolB = new MockPool(address(token));

        // Day 0: pool A gets liquidity and is registered right away.
        vm.prank(liq);
        token.transfer(address(poolA), 10_000_000 ether);
        vm.prank(owner);
        token.addPair(address(poolA));
        vm.prank(team);
        token.transfer(holder, 1_000_000 ether);
        // Pool B receives 50M liquidity on day 0 but is NOT registered yet.
        vm.prank(liq);
        token.transfer(address(poolB), 50_000_000 ether);
    }

    function _sumWeights(uint256 day) internal view returns (uint256) {
        return token.eligibleBalanceOn(holder, day) + token.eligibleBalanceOn(liq, day)
            + token.eligibleBalanceOn(team, day) + token.eligibleBalanceOn(address(poolA), day)
            + token.eligibleBalanceOn(address(poolB), day) + token.eligibleBalanceOn(buyer, day)
            + token.eligibleBalanceOn(owner, day) + token.eligibleBalanceOn(address(token), day);
    }

    function test_addPairKeepsPastDaysConsistent() public {
        uint256 day1 = block.timestamp / DAY + 1;
        vm.warp(day1 * DAY + 10);
        // Day 1: a trade through pool A creates holder tax (2% of 1,000,000 = 20,000).
        poolA.send(address(token), buyer, 1_000_000 ether);
        (uint256 sharesBefore, uint256 rewards,) = token.dayInfo(day1);
        assertEq(rewards, 20_000 ether);
        assertEq(_sumWeights(day1), sharesBefore, "consistent before registration");

        // Day 2: owner registers pool B (normal operation: a second DEX pool).
        vm.warp((day1 + 1) * DAY + 10);
        vm.prank(owner);
        token.addPair(address(poolB));

        // Weights that can still be claimed for day 1 must add up to day 1's share total.
        (uint256 sharesAfter,,) = token.dayInfo(day1);
        assertEq(_sumWeights(day1), sharesAfter, "day-1 claimable weights no longer add up to its share total");
    }
}
```

### 3. Low: claim(): the signature does not bind `instant`, so anyone holding a runner's signed claim can force it into a 7-day lock and the runner's instant claim reverts

`contracts/RunnerToken.sol:302`

```
        if (instant && msg.sender != account) revert OnlyRunnerCanClaimInstantly();
```

The EIP-712 struct is Claim(account,totalEarned,deadline); the payout choice `instant` is a plain calldata flag outside the signature. Line 302 only stops a third party from choosing instant=true. The locked branch is open to any msg.sender, and both branches consume the same (account, totalEarned) because claimed[account] is set to totalEarned on the first successful submission. Whoever lands first decides the payout mode: a third party who sees the pending instant claim (public mempool, a relayer, or anyone the signed payload was shared with) submits it with instant=false and the runner's own transaction reverts with NothingToClaim. The runner then has no per-lock early exit: releaseEarly() pays out ALL unfinished locks at 80% and burns 20% of each, so a runner holding earlier voluntary locks they wanted at 100% must either wait up to 7 days or burn 20% of those too. The forced lock also occupies one of the 30 active lock slots. No funds are stolen and the griefer gains nothing but gas, so this is griefing (low). Reported by the flow, permissions and economics specialists; merged here. Fix: include the payout choice in the signed struct (Claim(address account,uint256 totalEarned,uint256 deadline,bool instant)) so the server signs what the runner asked for, keeping the msg.sender == account rule for instant; or require msg.sender == account on both paths; or add a per-lock early release. The server (api/_lib/eth.js claimDigest) and app need the same struct change in the first option.

**Reproduction**

Owner setSigner(S), startEmission(). Server signs Claim(alice, 1000e18, deadline=now+1h) -> (v,r,s). Bob calls claim(alice, 1000e18, deadline, v, r, s, false) before alice. Alice calls claim(alice, 1000e18, deadline, v, r, s, true). Expected: alice receives 800e18 now and 200e18 is burned (her explicit choice). Actual: bob's call succeeds; alice's call reverts NothingToClaim(); balanceOf(alice) == 0; locksOf(alice) == (locked 1000e18, unlocked 0, nextUnlockAt now+7d, activeLocks 1). Second scenario: alice holds a voluntary 10,000e18 lock from day 0; on day 6 bob forces her new 1,000e18 claim (total 11,000e18) into a lock; alice calls releaseEarly() and receives 8,800e18 while 2,200e18 is burned (20% of the 10,000e18 lock she never chose instant for), versus the 800e18-now-plus-untouched-lock she attempted. Foundry: test/scratch/Verify.t.sol test_frontRunForcesLock and test_forcedLockThenReleaseEarlyBurnsOtherLocks (both assert the actual outcome and pass on the current code).

### 4. Low: The 4% tax and the 300k holder threshold are per-address rules that pooled intermediaries sidestep, and singleton DEXes (Uniswap V4 PoolManager, intent settlers) can never be registered

`contracts/RunnerToken.sol:421`

```
        if (_poolToken(pair, 0x0dfe1681) != address(this) && _poolToken(pair, 0xd21220a7) != address(this)) revert NotAPool(); // token0(), token1()
```

Tax applies only when `from` or `to` is in isPair, and holder-reward eligibility is any non-excluded address whose lowest daily balance is >= MIN_HOLDING. Both are evaluated per address, so a plain contract holding RUNNER on behalf of others defeats the stated rules: (a) a vault that accepts deposits from many sub-300k wallets reaches 300k itself, is not excluded, calls claimHolderRewards() and forwards the holder tax to depositors who individually do not qualify; (b) a wrapper token (wRUNNER) traded on any pool looks like a wallet-to-wallet transfer to RunnerToken and pays no tax, so volume can migrate to an untaxed venue; (c) any DEX whose pool is a singleton without per-pool token0()/token1() (Uniswap V4 PoolManager, CoW/UniswapX settlers, aggregators with internal balances) cannot be registered because addPair() requires token0()/token1() to return this token, so trades through them are permanently untaxed. The owner cannot exclude a wrapper either, because addPair is the only exclusion path and has the same gate. The README/NatSpec promise ('tax on every buy/sell through exchange pools; rewards only for wallets holding >= 300,000') therefore does not hold economically. AUDIT.md #10 already documents the V3/V4 incompatibility for a different reason (fee-on-transfer), so part of this is a known limitation. This is a design limitation rather than a code bug, which is why it is kept at low rather than the economics specialist's medium. Fixing it is a scope decision: accept and document 'registered V2-style pools only' and that the threshold is per address, or add an owner-gated exclusion/tax list for arbitrary contracts (with its own centralisation trade-off), or drop the per-address threshold.

**Reproduction**

Foundry (test/scratch/Verify.t.sol test_wrapperAggregation, passes on current code asserting the actual outcome): deploy RunnerToken, register a MockPool exposing token0()==RUNNER and fund it with 10M. Deploy Wrapper (deposit() does transferFrom into itself; harvest() calls claimHolderRewards()). Ten wallets each receive 30,000 RUNNER (below MIN_HOLDING) and deposit it. Next day the pool sends 1,000,000 RUNNER to a buyer, collecting 20,000 RUNNER holder tax. Expected per the stated rule: none of the ten wallets qualifies, so their 300k earns nothing. Actual: eligibleBalanceOn(wrapper, day) == 300,000e18 and wrapper.harvest() returns 31.578947368421052631e18 (300k/190M of the 20k), which the wrapper can forward. Separately: owner calls addPair(address of a contract with no token0()/token1()) -> reverts NotAPool(), so a V4-style singleton can never be taxed.

### 5. Low: The deployment day's share total is frozen at 0 before the initial mints, so 100% of launch-day holder tax goes to the protocol wallet

`contracts/RunnerToken.sol:171`

```
        _startDay(today);
```

The constructor calls _startDay(today) before the three mints, so _days[deployDay].shares is frozen at 0 while the liquidity and team wallets hold 200M RUNNER from the first block (eligibleSupply becomes 200M right after, but the day's share total is never re-read). Every 2% holder cut collected that day has no eligible claimant: _holderShareOf() returns 0 when shares == 0, holderClaimable() is 0 for every wallet, and after 7 days sweepExpired() moves the whole amount to protocolWallet (the owner by default). Per the launch sequence 'deploy -> add liquidity -> register the pool right away', the deploy day is launch day and typically the heaviest trading day, and the first liquidity transfer into the registered pool is itself taxed. This is consistent with the strict 'held for the whole day' rule (nobody held tokens at 00:00 UTC of the deploy day), so it may be intended, but the NatSpec says the 2% goes 'to holders' and the owner 'can never take tokens out of the holder-reward bucket', and on this day the owner-controlled wallet receives 100% of the holder cut instead of 50%. If intended, document it; otherwise mint before calling _startDay() in the constructor so deploy-day shares equal the initial eligible supply, and/or roll a zero-share day's rewards into the next day's bucket instead of sweeping them.

**Reproduction**

Foundry (test/scratch/Verify.t.sol test_deployDaySharesZero; the test's final assertion expected 20,000e18 and the actual sweep was 220,000e18 because the 10M liquidity transfer into the registered pool in setUp was also taxed, which confirms the behaviour): deploy RunnerToken(owner, liq, team) at 01:00 UTC on day D; dayInfo(D).shares == 0 although liq and team hold 100M each. Register a MockPool, fund it with 10M from liq (200,000e18 holder cut), and have it send 1,000,000 RUNNER to a buyer the same day (20,000e18 holder cut): dayInfo(D).rewards == 220,000e18. Day D+1: holderClaimable(liq) == 0 and holderClaimable(team) == 0. Day D+9: sweepExpired(10) returns 220,000e18 and balanceOf(owner) rises by 220,000e18. Expected per README: holders share the 2%; actual: the protocol wallet receives all of it.

### 6. Low: RunnerGenesis.mint() delivers the token to msg.sender without the ERC-721 receiver check, so a contract that cannot handle NFTs pays and gets a token it can never move

`contracts/RunnerGenesis.sol:140`

```
        _mint(msg.sender, tokenId);
```

mint() is the only way to obtain a token and it writes ownership to msg.sender without calling onERC721Received when msg.sender has code, unlike safeTransferFrom() which enforces it. A contract without onERC721Received and without any transfer/approve logic (a minimal multisig, a contract that forwards a mint call) pays the full price, receives the NFT, and can never move or use it; the ETH has already gone to the treasury and the id is permanently taken out of the 9,999 supply. Self-harm only, no effect on other holders; reported because the collection is sold through a wallet-connected web page where contract wallets are common. Reported by the flow and math specialists; merged here. Fix: after _mint, if msg.sender.code.length > 0 require onERC721Received to return its selector (the same code path as safeTransferFrom), which keeps EOA and Safe minting unchanged.

**Reproduction**

Deploy RunnerGenesis. Deploy a contract C with only `function buy(g, id) external payable { g.mint{value: msg.value}(id); }` and no onERC721Received; fund it with 1 ETH. C.buy(g, 1) with msg.value == priceOf(1) == 0.005 ether. Expected (safe-mint semantics): revert UnsafeRecipient and no payment taken. Actual: ownerOf(1) == C, the treasury balance rises by 0.005 ETH, and C has no code path to call transferFrom/approve, so token 1 is stuck. Foundry: test/scratch/Verify.t.sol test_genesisMintNonReceiver (asserts the actual outcome; passes on current code).

### 7. Low: transferOwnership is single-step in both contracts: a mistyped or undeployed address permanently loses every owner function

`contracts/RunnerToken.sol:471`

```
    function transferOwnership(address newOwner) external onlyOwner {
```

Ownership moves in one call with only a zero-address check and nothing verifies the new owner can act. The same code is at contracts/RunnerGenesis.sol:291. AUDIT.md's own 'before mainnet' step is to move ownership to a multisig, which is exactly the call where a wrong or not-yet-deployed address is most likely. After a bad transfer on the token nobody can rotate the server signer, pause claims, change the emission schedule, register a new pool or move the protocol wallet, for the lifetime of the token; on the NFT nobody can change the treasury that receives all mint ETH, the royalty receiver, pausing, URIs or the ERC-721C validator, and the OpenSea collection manager role is lost. Reported twice by the permissions specialist (one per contract) and by the flow specialist; merged here. Fix: two-step handover (pendingOwner set by the owner, acceptOwnership() by the pending owner, as in OpenZeppelin Ownable2Step) in both contracts. This keeps the owner role and its powers unchanged.

**Reproduction**

Owner calls token.transferOwnership(0x0000000000000000000000000000000000000001) (any typo of the intended multisig, or a Safe not yet deployed on this chain). Expected: recoverable until the new owner accepts. Actual: owner() == 0x...0001 immediately and the former owner's next setSigner() reverts NotOwner(); no function can recover ownership. Same on RunnerGenesis: setTreasury/setRoyaltyReceiver/setPaused/setBaseURI/setContractURI/setTransferValidator/withdraw all revert NotOwner() for the former owner. Foundry: test/scratch/Verify.t.sol test_singleStepOwnership (asserts the actual outcome; passes on current code).

### 8. Info: Trust assumptions: the owner key can route up to 20M RUNNER/day from the reward pool to itself, redirect the protocol share and swept rewards, pause claims, and freeze NFT transfers

`contracts/RunnerToken.sol:436`

```
    function setSigner(address newSigner) external onlyOwner {
```

Not a permission bypass: this is the privileged-power inventory the review relies on, recorded so the trust assumptions are explicit (AUDIT.md #1, #4, #16 acknowledge most of it). The owner (an EOA, the dev wallet, per README) can: (1) setSigner() to a key it controls and, after setEmissionSchedule(20_000_000e18, 7, 20_000_000e18) takes effect the next UTC day, claim up to 20M RUNNER/day (2.5% of the 800M pool) through claim() with instant=false until the key is rotated, bounded only by MAX_DAILY_EMISSION and rewardsRemaining(); (2) setProtocolWallet() to redirect the 2% protocol cut and every swept holder-reward day; (3) addPair() on any contract that returns this token from token0()/token1(), which taxes every transfer touching it and excludes it from holder rewards (a wallet cannot be targeted, a user-deployed vault that happens to expose token0() can); (4) setClaimsPaused(true) to stop run-reward payouts while locks keep maturing. On RunnerGenesis the owner can setTransferValidator() to a contract that reverts, freezing all NFT transfers, and setTreasury() to a contract that reverts, halting mint(). The NatSpec sentence 'The owner can never take tokens out of the run-reward pool' is true only up to the daily emission cap. Reported by the flow and economics specialists; merged here. Recommended, consistent with AUDIT.md: multisig owner on both contracts and the two-step handover from the previous finding.

**Reproduction**

State: owner O holds the key on day D. O calls setEmissionSchedule(20_000_000e18, 7, 20_000_000e18) and setSigner(K). Day D+1: emissionOn(D+1) == 20_000_000e18; K signs Claim(O, 20_000_000e18, deadline) and O calls claim(O, 20_000_000e18, deadline, v, r, s, false): succeeds, locksOf(O).locked == 20_000_000e18, released at 100% after 7 days; repeatable every day. No contract check stops this; only key custody does. Foundry: test/scratch/Verify.t.sol test_ownerDrains20MPerDay (asserts the actual outcome; passes on current code).

---

Judge's submission `937960866e42cc84c35513286d1aaaa240b038bdfc0b656eb5d02599515c4407`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
