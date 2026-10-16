# Hamster Hour token-design review

**Scope and conclusion.** This is a pre-build economic and integration review of the deployed HamsterHour at `0xc5217f129da200a8e86229de4eabf3686eef64b1` and the proposed `$HAMSTER`/MiningVault. HamsterHour is treated as immutable. The design should not launch unchanged: its largest problems are (1) an on-chain vault cannot enumerate bettors from views or logs, (2) 12% emission makes controlled opposite-side farming profitable whenever HAMSTER trades above the opening price, (3) the cap is much too large for the stated volume, and (4) the proposed vault staking story does not automatically connect to HamsterHour's existing staking flow.

## Evidence and confidence

**Verified facts.** The IMD Explorer describes six ten-minute rounds per hourly window, minimum 0.5 IMD bets, 256 maximum EXACT entries, public window/position views, the 91/5/3/1 split, one-shot staking and jackpot token configuration with 48-hour timelocks, and pull-based claims. The verified source exposes `window(k)`, `position(k,account)`, `exactEntries(k)`, `exactGuess(k,index)`, `currentLine()`, `windowTimes(k)`, `Bet`, `Settled`, `MarketVoided`, `WindowVoided`, `StakingDistributed`, and related events. The current published source rejects an oracle attestation issued before `endsAt`; the Explorer page also records an earlier review finding about that boundary, so deployment/source versions must be pinned before implementation.

Sources: [IMD Explorer, Hamster Hour](https://explorer.imd.fun/jobs/51bec67e-efec-4e88-bb68-297892343ce0), [verified HamsterHour source](https://github.com/identity-md-launches/launch-1951-workflow-contract-stage-context/blob/main/src/HamsterHour.sol), [raw source](https://raw.githubusercontent.com/identity-md-launches/launch-1951-workflow-contract-stage-context/main/src/HamsterHour.sol).

**Inferences.** Attack values below assume the stated 9% total fee, a settled non-void market, no gas/slippage, and that `$HAMSTER` is valued in IMD. They are deliberately favorable to the farmer. Exact-ticket results depend on whether ranks 1 and 2 count as “winners”; the proposed brief does not define that.

**Unanswered before build.** The requester must decide whether only the closest EXACT rank is a winner, whether a losing account's loss is gross losing stake or net of any other winning market on the same window, and whether the opening price is an immutable deployment parameter or a manipulable pool observation. These choices materially change emissions.

## Ranked defects and concrete fixes

### 1. Critical — no trustless bettor enumeration

**Verdict: no, not autonomously from public views and events alone.** `position(k, account)` is sufficient to inspect one supplied account; `window(k)` supplies result, line, market-void flags and pools; `exactEntries`/`exactGuess` can reconstruct the 256-ticket ranking. `Bet` and `Settled` are sufficient for an off-chain indexer. But an EVM contract cannot read its own event history or enumerate every address that emitted `Bet`. The vault therefore cannot discover all losers and pro-rata distribute from logs.

**Fix.** Use pull accounting: after final settlement, `claimMined(k, account)` (or `claimMined(k)` for `msg.sender`) reads the immutable position, computes the account's loss, records it once, and pays its share of a finalized `totalLoss`. A permissionless keeper may submit the same claim for an account, but the beneficiary must be the account. Finalization should be a separate permissionless call after the game is settled and should reject further claims only after a documented grace period. The stronger alternative is a HamsterHour callback on each bet and settlement, but that violates the “will not change it” constraint.

### 2. Critical — farming is profitable at the proposed launch rate

For two controlled wallets betting `x` on opposite OVER/UNDER sides, the attacker pays `2x`, receives the 91% winner share `1.82x`, and loses `0.18x` IMD: exactly 9% of turnover. If one wallet is the loser, mining emits `r x / P_open` HAMSTER, where `r` is the rate and `P_open` is IMD per HAMSTER at pool opening. At `r = 12%`, farming breaks even when the market price is:

`P_market > (0.18 / 0.12) × P_open = 1.5 × P_open`.

Thus any 50% appreciation creates positive expected value before gas and slippage. At the 0.5 IMD minimum, the pair costs 0.09 IMD and emits 0.06 HAMSTER at `P_open = 1`; the cap is nowhere near binding.

For 256 minimum-size EXACT tickets, total stake is 128 IMD. If only one ticket wins, approximately 127.5 IMD is losing stake and the fee is 11.52 IMD. At 12%, emission is 15.3 HAMSTER at a 1 IMD opening price; break-even is about `0.753 IMD/HAMSTER` (ignoring the ambiguity over ranks 2 and 3). Splitting tickets across two wallets does not create identity resistance.

**Fix.** At launch set `r <= 4%` and add a per-window IMD-equivalent emission ceiling. At 4%, the two-sided break-even price is `4.5 × P_open`; a 3% rate gives `6 × P_open`. Also require a minimum opposing organic volume or a minimum number of distinct funded bettors only as a secondary heuristic—not as a security boundary. Do not let an attacker manufacture emission by self-settling: settlement must be final and use the game’s stored result, never caller-supplied outcome data.

### 3. High — the cap is not a volume control

At launch, the vault contains 800,000,000 HAMSTER. `0.04%` per window is 320,000 tokens before the factor, or 7,680,000 tokens per day at 24 windows/day. With 200–2,000 IMD of daily bets, a 4–12% loss rate produces only roughly 8–240 IMD of nominal emission value per day, so the percentage-of-vault cap is normally irrelevant. Its 72-day half-life is a supply-decay parameter, not an anti-farming limit.

**Fix.** Use both `min(rate × eligibleLoss, remaining × capBps / 10_000, perWindowImdBudget / P_reference)`, with `perWindowImdBudget` of 2 IMD initially and a hard daily budget of 20 IMD (values can be raised after observed organic volume). Make the cap apply to all HAMSTER minted, including rounding, and never refill it.

### 4. High — predictable sleep/low-pass outcomes remain farmable

The 10%-of-line rule only suppresses an emission after the result is known and only for a narrow region. It does not prevent a bettor from placing both sides before close, then using public live hamster data or a nearly certain zero/low result to obtain the losing-side emission. A SLEEP market with both sides funded is not void; a one-sided market is void and refunds. A result just above the threshold, or a stale/high line, bypasses the zero-emission rule.

**Fix.** Do not use the threshold as the primary defense. For SLEEP and any result below `25%` of line, set eligible loss to zero; alternatively exclude SLEEP from mining entirely. Add a commit/reveal close or a short immutable no-bet buffer before the last round if the game can ever be changed. Since HamsterHour is fixed, the practical fix is no SLEEP mining plus a conservative low-result multiplier of zero.

### 5. High — staking integration is underspecified and claim order matters

HamsterHour's `stake(amount)` pulls its configured `stakingToken` from the caller, and `claimStaking()` pays IMD to that caller. Setting a vault receipt token as `stakingToken` does not make the vault receive the 5% share when users hold receipt tokens: the game pays the caller that staked the receipt token. The vault must itself hold and stake the receipt tokens, then distribute its claimed IMD internally.

A one-hour warm-up blocks same-block flash staking, but it does not stop capital from being parked for one hour immediately before a known settlement. A 24-hour cooldown prevents instant exit, yet a user can claim immediately before requesting withdrawal unless the accounting freezes the claimable balance consistently. The 30-window pre-token reserve can likewise be captured by whoever is the only eligible staker at each settlement.

**Fix.** Have the vault custody receipt shares, stake the aggregate share balance in HamsterHour, and expose deposit/withdraw requests rather than exposing the game stake directly. Snapshot eligible shares at each observed game settlement; require 1 hour minimum holding and 24 hours minimum withdrawal lock; freeze reward accrual at cooldown start; allow claim only from a separately checkpointed balance; and make reserve tranches accrue only to shares that were eligible at the settlement snapshot. Test stake, claim, cooldown, transfer, and reserve-release ordering together.

### 6. Medium — price-linked emission is reflexive

Converting an IMD loss to HAMSTER at the pool-opening price makes emissions sensitive to a manipulable, low-liquidity initial pool and creates a clear incentive to pump HAMSTER above that reference. A TWAP is better than a single spot quote but is still manipulable in a thin pool and can be unavailable during launch.

**Fix.** Prefer a price-independent fixed HAMSTER-per-IMD emission budget, selected from the 1B supply plan, with a hard IMD-denominated daily budget. If an IMD-linked conversion is required, use a long-window TWAP with minimum liquidity/observation age, a bounded deviation from the previous TWAP, and a conservative floor/ceiling; never use the same swap that receives the hook fee as its price oracle.

### 7. Medium — hook routing can block accounting or mis-account funds

The v4 hook must accept calls only from the PoolManager, validate the exact pool ID, currencies, direction and fee amount, and use checks-effects-interactions. A callback that performs arbitrary token transfers or depends on a token’s non-standard return value can revert swaps and strand the reserve. A malicious or wrong pool can route IMD to the oracle reserve without corresponding HAMSTER to the jackpot, or vice versa.

**Fix.** Make the configured pool ID and both token addresses immutable; account fees in internal ledgers during the hook callback; settle them through a guarded permissionless `sweepFees` with `SafeERC20`; reject fee-on-transfer/rebasing tokens; enforce `oracleReserve >= runway` before release; and make jackpot credit pull-based. Do not accept arbitrary ERC-20 donations as if they were the configured jackpot asset. Uniswap documents that hooks run at defined pool-manager lifecycle points; the implementation must use the corresponding v4 callback authorization and return selectors. Sources: [Uniswap v4 hooks](https://developers.uniswap.org/docs/protocols/v4/concepts/hooks), [OpenZeppelin SafeERC20/ReentrancyGuard](https://docs.openzeppelin.com/contracts/5.x/api/utils).

### 8. Medium — oracle reserve runway needs an explicit invariant

“Release reserve above 30 days” is ambiguous at 24 windows/day: it could mean 720 settlements, 30 hourly windows, or 30 calendar days of the expected 3% fee. A reserve can be drained by repeated release if the runway is checked against current liabilities rather than projected reimbursement obligations.

**Fix.** Define `runwayWindows = 720` and a conservative expected reimbursement per window, or define 30 hourly windows explicitly. Release only `max(0, oracleReserve - requiredRunway)`, reserve the 0.5 IMD reimbursement before any release, and emit the pre/post runway values. Never make the hook a direct spender of the oracle reserve.

## Answers to the eight questions

1. **No for automatic distribution; yes for a per-account pull.** Required game reads are `window`, `position`, `exactEntries`, `exactGuess`; `Bet`, `Settled`, `MarketVoided`, `WindowVoided` are useful off-chain evidence. Missing is bettor enumeration and an explicit per-account loss/finalization primitive. Exact ranking also needs a precise definition of which ranks are winners.

2. **The two-wallet attack breaks even at 1.5× opening price at 12%.** The 256-ticket example breaks even near 0.753× opening price under “only closest wins.” Set rate to 3–4%, cap with a 2 IMD per-window budget, and exclude SLEEP/low-pass losses. At 4%, the basic two-wallet attack needs 4.5× price appreciation.

3. **No.** The threshold suppresses some realized emissions but does not stop predictable outcomes, late information, or just-above-threshold farming. Exclude SLEEP and use 25% of line as the low-result cutoff if mining must remain attached to that market.

4. **Fixed price-independent rate is safer.** It avoids launch-pool manipulation and reflexive pump-to-mine behavior. A bounded, aged TWAP is an acceptable second choice, not a single opening spot price.

5. **Flash loans are mostly blocked by the one-hour warm-up, but ordering exploits remain.** A last-hour deposit can still buy the next settlement snapshot; claim-before-cooldown can be inconsistent unless frozen. Aggregate vault staking, checkpointed snapshots, freeze-at-cooldown accounting, and reserve eligibility rules are required.

6. **0.04% is a sane mathematical decay but an oversized economic cap.** It halves in about `ln(2)/(24 × -ln(0.9996)) = 72.1` days. For the stated volume, begin with 3% rate, 0.005% of remaining vault per window, 2 IMD per-window budget and 20 IMD daily budget; after 30 days of data, permit 4%, 0.01%, 5 IMD/window and 50 IMD/day only if organic volume dominates. The fixed budget, not the percentage cap, should bind at launch.

7. **Yes, if routing and accounting are not isolated.** A wrong pool, malicious token behavior, failed reserve transfer, or direct hook path can block swaps or misroute one side. Immutable pool validation, PoolManager-only callbacks, internal ledgers, SafeERC20, pull-based sweeps, and reserve liabilities fix it.

8. **Launch/check risk is high until integration is explicit.** A build will fail the “really uses IMD” bar if it merely deploys HAMSTER and a hook without provable IMD flow. The deliverable must show IMD in HamsterHour bets, 5% IMD claimed by the vault’s aggregate staking position, oracle-reserve accounting, 3% hook routing, and tests proving conservation. It must also document the immutable HamsterHour address, exact IMD address/decimals, no fake price feed, no stand-in addresses, bounded token supply, no arbitrary minting, no admin drain, no unbounded loop over all users, and ABI/deployment arguments. Pin the verified HamsterHour source revision and test the deployed interface before launch.

## Recommended parameters

| Parameter | Launch value | Rationale |
|---|---:|---|
| Total supply | 1,000,000,000 HAMSTER | As proposed; 100M swarm, 100M pool, 800M vault |
| Eligible loss rate | 3% of loss in fixed HAMSTER/IMD budget | 6× opening-price attack threshold under two-sided farming |
| Maximum later rate | 4% | Requires measured organic volume and a timelocked governance change, if governance exists |
| Per-window remaining cap | 0.005% | Supply safety; not relied on for low-volume anti-farming |
| Per-window IMD-equivalent cap | 2 IMD initially | Makes farming uneconomic after gas/slippage and limits launch leakage |
| Daily IMD-equivalent cap | 20 IMD initially | Appropriate for 200–2,000 IMD/day until observed |
| Decay | halve rate every 50,000 IMD cumulative bets | Retain the brief’s fee-linked concept, but decay the rate, not only the vault cap |
| Low-pass multiplier | 0 below 25% of line | Safer than 10%; also exclude SLEEP |
| Vesting | 7 days linear, claimable only | Keep; checkpoint before every transfer/claim |
| Warm-up / cooldown | 1 h / 24 h | Keep, with snapshot and freeze rules above |
| Oracle runway | 720 windows (30 days at 24/day) | Explicit interpretation; reserve reimbursement first |
| Hook fee | 1%: IMD to oracle reserve, HAMSTER to jackpot | Keep only with immutable pool/currency validation |

## Contract interface for the build

The following is the minimum ABI-level shape. It intentionally omits deployment addresses; those are constructor inputs or immutable values supplied from verified deployments, never guessed constants.

```solidity
interface IMiningVault {
    // Immutable wiring and accounting views
    function hamsterToken() external view returns (address);
    function imdToken() external view returns (address);
    function hamsterHour() external view returns (address);
    function totalVaultBalance() external view returns (uint256);
    function totalLoss(uint256 windowId) external view returns (uint256);
    function emission(uint256 windowId) external view returns (uint256);
    function previewLoss(uint256 windowId, address account)
        external view returns (uint256 loss, bool eligible);
    function vesting(uint256 windowId, address account)
        external view returns (uint256 total, uint256 claimed, uint64 start, uint64 end);
    function pendingIMD(address account) external view returns (uint256);
    function previewWithdraw(address account) external view returns (uint256 assets, uint64 availableAt);

    // Permissionless finalization and pull mining; beneficiary is explicit.
    function finalizeWindow(uint256 windowId) external;
    function claimMined(uint256 windowId, address beneficiary) external returns (uint256 amount);
    function claimVested(uint256 windowId, address beneficiary) external returns (uint256 amount);

    // Vault share lifecycle. Shares are the token configured in HamsterHour.
    function deposit(uint256 hamsterAmount, address receiver) external returns (uint256 shares);
    function requestWithdraw(uint256 shares, address receiver) external;
    function executeWithdraw(address receiver) external returns (uint256 hamsterAmount);
    function claimIMD(address receiver) external returns (uint256 amount);

    // Aggregate receipt-token position in the immutable game.
    function syncGameStake() external;
    function gameStake() external view returns (uint256);

    event WindowFinalized(uint256 indexed windowId, uint256 totalLoss, uint256 emission,
        uint256 remainingVault, uint256 rateBps, uint256 capBps);
    event LossRecorded(uint256 indexed windowId, address indexed account, uint256 loss,
        uint256 emissionShare);
    event MinedVestingCreated(uint256 indexed windowId, address indexed account,
        uint256 amount, uint64 start, uint64 end);
    event MinedClaimed(uint256 indexed windowId, address indexed account, uint256 amount);
    event Deposit(address indexed caller, address indexed receiver, uint256 assets, uint256 shares);
    event WithdrawRequested(address indexed owner, address indexed receiver,
        uint256 shares, uint64 availableAt);
    event Withdrawn(address indexed owner, address indexed receiver, uint256 assets, uint256 shares);
    event IMDReceived(uint256 indexed gameWindow, uint256 amount, uint256 runwayAfter);
    event GameStakeSynced(uint256 oldAmount, uint256 newAmount);
    event HookFeeAccrued(uint256 indexed poolId, uint256 imdAmount, uint256 hamsterAmount);

    // Storage that must be present or equivalently represented:
    // immutable game, IMD, HAMSTER, poolId; rate/cap/budget parameters;
    // mapping(windowId => WindowEmission{finalized,totalLoss,emission,claimedLoss});
    // mapping(windowId => mapping(account => LossRecord{loss,claimed}));
    // mapping(windowId => mapping(account => Vesting{total,claimed,start,end}));
    // mapping(account => Stake{shares,eligibleAt,cooldownAt,pendingIMD});
    // totalShares, totalGameStake, oracleReserve, reservedRunway, cumulativeBets;
    // and a non-reentrancy guard plus a pause only for claims/withdrawals if required.
}
```

The interface deliberately makes `finalizeWindow` separate from `claimMined`: all claimants must use one immutable emission total, and no account can increase the denominator after another account has claimed. `syncGameStake` must be the only path that calls HamsterHour staking functions, and the vault must use checks-effects-interactions plus safe ERC-20 transfers. OpenZeppelin documents `SafeERC20` for tokens with non-standard return behavior and `ReentrancyGuard` for nested-call protection; those are implementation requirements, not substitutes for the economic controls above.

## Build-gate checklist

- Pin and verify the exact deployed HamsterHour bytecode/source revision.
- Implement per-account pull loss calculation and test void, one-sided, tie, EXACT, SLEEP and zero-loss cases.
- Test 256 EXACT guesses without an unbounded loop and define rank-1/rank-2 eligibility.
- Prove `sum(vesting) <= 800M` and `sum(IMD liabilities) <= vault balance` under every claim order.
- Fuzz cooldown, warm-up, transfer, claim-before-withdraw and 30-day runway release ordering.
- Test hook authorization, wrong pool/currency, fee-on-transfer rejection, reentrancy and failed token calls.
- Demonstrate real IMD flows in integration tests; do not use a mock price or stand-in address in launch configuration.

