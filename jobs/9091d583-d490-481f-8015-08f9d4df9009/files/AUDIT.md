# Audit report

> Adversarial review of the Regen rail contracts in github.com/ToknWrks/imdo at the given commit (branch regen-rail, PR #1): src/regen/ and its tests. Foundry; Solidity 0.8.26, evm_version cancun, via_ir, optimizer_runs 44444444, bytecode_hash = "none"; vendored lib/ (OpenZeppelin, forge-std, Uniswap v4). The rest of the tree (IMDO token, hook, treasury, staking, claim, RegenDrop) was reviewed by IMD swarm job 37ac5d94-da10-4a27-84d9-246c17a2c3f7 and is NOT in scope except where src/regen/ touches it (ImdoTreasury.payOffsets and offsetsSafe).
>
> Purpose: a permissionless, ownerless rail on Base that turns ETH fees from any registered project into retired Regen City Forest credits on Klima's Retirement Aggregator, with the project as beneficiary. Nothing has an owner, pause, setter or withdrawal. Deployment target: Base mainnet (chain 8453) for RegenRegistry, RegenRouter, UniswapV3Venue, RegenReceiverFactory; Ethereum mainnet for OffsetsForwarder. Nothing is deployed yet.
>
> Contracts (src/regen/):
> 1. RegenRegistry. register(string name, string regenAddress, address beneficiary) returns uint256 id (1-based). Name: 1..64 bytes printable ASCII 0x20..0x7E, no '|', no leading/trailing space, unique. regenAddress: 44 chars, "regen1" + 38 bech32 chars. Errors ZeroAddress, BadName, NameTaken(id), BadRegenAddress, UnknownProject(id). Event ProjectRegistered. project(id), exists(id), validName(bytes), validRegenAddress(bytes) pure. No update, no delete.
> 2. RegenRouter. constructor(Config c) with struct Config { RegenRegistry registry; IKlimaRetirementAggregator aggregator; IERC20 usdc; address classVault; address creditA; address creditB; address creditC; IEthToTokenSwap venue; IPriceFeed ethUsd; uint256 maxFeedAge; uint256 minBatch; uint256 maxBatch; uint256 bountyBps; uint256 minOutBps; } (all addresses non-zero; minBatch > 0, maxBatch >= minBatch, bountyBps < 10000, 0 < minOutBps <= 10000, maxFeedAge > 0, feed decimals == 8). Intended values: minBatch 0.001 ether, maxBatch 0.05 ether, minOutBps 9700, bountyBps small (tens of bps), maxFeedAge about 1 hour. deposit(uint256 projectId) payable credits balanceOf[projectId][msg.sender]; plain receive() reverts DirectEthRefused. process(uint256 projectId, address depositor) nonReentrant: ethIn = min(balance, maxBatch), revert BelowMinBatch under minBatch; Chainlink ETH/USD read (stale or non-positive => emit Skipped("feedStale"), return); first credit token of creditA/B/C the aggregator can price (none => emit Skipped("classEmpty"), return); debit balance; bounty = ethIn * bountyBps / 10000; swap ethIn - bounty via venue.swapEthToToken(usdc, minUsdcOut(ethIn - bounty, price), router) and revert SwapShort if under minOutBps of the oracle value; quote tonnes for ALL USDC held (previous dust included), floor to 1e12 steps, revert NothingRetired on 0; forceApprove, aggregator.retireCreditViaKlima(credit, 0, 0, tonnes, usdc, classVault, held, 0, RetireDetails{retiringAddress: router, retiringEntityString: "Regen Retirement Router", beneficiaryAddress: p.beneficiary, beneficiaryString: p.name, retirementMessage: message(projectId, p, depositor), rest empty}); approve back to 0; retiredOf[projectId] and totalRetired += tonnes; emit Processed(projectId, depositor, caller, creditToken, ethIn, bounty, usdcBought, usdcSpent, tonnes); pay the bounty to msg.sender by call; a failed bounty call re-credits the depositor's balance and emits BountyForfeited. message() builds retirement grammar v1 (frozen with Regen 2026-10-07): the project's name, regen address and "src:8453:<depositor>". Errors: ZeroAddress, UnknownProject, ZeroDeposit, BadParameter, BelowMinBatch, SwapShort, NothingRetired, DirectEthRefused.
> 3. UniswapV3Venue. constructor(ISwapRouter02 router, address weth, uint24 fee). swapEthToToken(address token, uint256 minOut, address to) payable: SwapRouter02.exactInputSingle with msg.value, WETH->token at the fixed fee tier, recipient `to`; reverts WrongToken for anything but the configured token path. Stateless.
> 4. RegenReceiver + RegenReceiverFactory. One receiver per project at a CREATE2 address predictable before deployment (salt = projectId, fixed init code): predict(projectId), deploy(projectId) (AlreadyDeployed, UnknownProject). Receiver: receive() accepts anything (the OP Stack bridge finalisation call must succeed on minimal gas); forward() permissionless, sends the whole balance to router.deposit{value}(projectId), NothingToForward on 0; event Forwarded(projectId, amount).
> 5. OffsetsForwarder (Ethereum). constructor(IOffsetsSource treasury, IL1StandardBridge bridge, address receiverOnBase, uint32 minGasLimit). forward() permissionless: calls treasury.payOffsets() (the ImdoTreasury pays only its immutable offsetsSafe, which is this contract), then bridges its entire ETH balance with bridge.depositETHTo(receiverOnBase, minGasLimit, "") (L1StandardBridge 0x3154Cf16ccdb4C6d922629664174b904d80F2C35). receive() accepts. NothingToForward on 0. No other function.
>
> Review questions (each needs a concrete answer):
> - Can ETH ever leave RegenRouter other than as a retirement input, the caller's bounty, or stay as USDC dust for the next batch? Can anyone extract USDC or credits? Reentrancy through the venue, the aggregator, a credit token, or the bounty call?
> - Griefing: can process() be made to revert forever for a project (feed, aggregator quote, tonnes rounding, dust accumulation, a depositor that is a contract)? Can the bounty be farmed with tiny deposits? Is minBatch/maxBatch sizing sound against a 0.05 ETH batch on Base liquidity?
> - Oracle floor: is minUsdcOut(ethIn, price) correct in decimals (USDC 6, feed 8, ETH 18)? Can a sandwich on the V3 pool pass the 97% floor and what is the maximum extractable per batch? Stale-feed handling: maxFeedAge, negative or zero answers, round completeness.
> - Aggregator integration: are the quoteRetireCreditForInputTokenInViaKlima and retireCreditViaKlima argument orders and semantics right for Klima's Base aggregator 0xdA0A793D7C32AB80bcdab7F8c725c96DB22464f4 with classVault 0xf4699531e0a5F6e9351a36De3753Deaad329Bf45 and credit tokens 0xE6628083Ab9A9Ab235e80f63e7ecd810B54A71B8, 0x3D1bf942619cB9FC71543721Ef3D5496FAf283B8, 0xb77A0be47A686c525a38fbb10c0D424929471d7D? What happens if the aggregator spends less than `held`, or more tonnes than quoted, or if a credit token is paused or delisted mid-call?
> - Registry: can a name collide by case or whitespace, can a malicious name or regen address break the retirement message or any off-chain reader (the message is read by Regen's indexer); is the bech32 charset check sufficient and does a wrong checksum matter here?
> - Receivers and bridge: CREATE2 prediction correctness across projects; can a receiver's ETH be redirected; can ETH bridged to a not-yet-deployed receiver be lost; L1StandardBridge gas limit and failure modes; can OffsetsForwarder strand ETH; reentrancy from payOffsets.
> - Cross-contract: ImdoTreasury pays offsetsSafe by pull. Confirm the forwarder works as that seat, and that nothing in the treasury can brick forward().
>
> Rules: read-only review; do not modify src/, script/, foundry.toml, lib/ or test/ outside test/scratch/. Scratch tests may be added under test/scratch/ only. Every finding needs a severity, exact file:line, a concrete reproduction and, where possible, a Foundry proof that fails on this code. Run forge test (163 tests; test/fork/RegenRouterBaseFork.t.sol forks Base at block 52335751 via https://base.gateway.tenderly.co and may be skipped if no RPC) and forge fmt --check, and report the result. Do not claim an audit; this is a review by the IMD swarm. Wording in any report: "regenerative contribution" and "retired credits", never "carbon offset" or "net zero".

| | |
|---|---|
| Repository | https://github.com/ToknWrks/imdo.git |
| Commit | `43935b019879a0046651ac154016105d31d79754` |
| Job | `9091d583-d490-481f-8015-08f9d4df9009` |
| Judged | 2026-10-12 00:18 UTC |
| Findings | 1 high · 2 medium · 7 low · 4 info |

Four agents audited the code as it is at `43935b0`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. High: process() has no price floor on the USDC -> kVCM leg: the caller can sandwich the Aerodrome pool in one transaction and keep most of each batch's retired credits

`src/regen/RegenRouter.sol:175`

```
            aggregator.quoteRetireCreditForInputTokenInViaKlima(credit, 0, held, address(usdc), classVault, 0);
```

Merged from audit_economics, audit_permissions and audit_flow (one mechanism). The router floors only the first leg (ETH -> USDC against Chainlink, minOutBps). The second leg is unguarded: line 175 asks the aggregator how many tonnes `held` USDC buys and line 179 retires exactly that with maxInputTokenIn = held, so the retirement can never fail on price and any kVCM price is accepted. Klima's RetireFacet prices USDC -> kVCM off the spot reserves of a single Aerodrome volatile pool (0x5C0D76fab1822bDeb47308eD6028231761ED723E, 30 bps). Verified on a Base fork at block 52335751: the pool held 538,950 kVCM against 15,453 USDC (~$15k depth), and live at block 52487147 it held 521,302 kVCM / 15,768 USDC. Because process() is permissionless and pays the caller, the keeper is the attacker and no mempool ordering is needed: buy kVCM, call process() for every pending (project, depositor) slice, sell back, all in one transaction. Fork measurements with bountyBps 50, one 0.05 ETH batch: honest 6.1965 t; front-run 2,000 USDC -> attacker +15.80 USDC, 4.865 t; 5,000 -> +27.52, 3.549 t; 8,000 -> +31.20, 2.702 t; 12,000 -> +29.48, 1.975 t; 16,000 -> +23.64, 1.506 t. With 0.25 ETH pending (five slices) and a 15,768 USDC front-run: attacker +404.37 USDC plus the bounty, 7.516 t retired instead of ~31 t. The NatSpec at lines 29-32 ('a sandwich ... can never take more than (10000 - minOutBps) of a batch') is false for this leg; no ETH or USDC is taken from the router, but most of each batch's regenerative contribution is diverted to whoever processes it, for every batch, forever. Fix (preserving the ownerless design): bound tonnes per USDC against a reference the caller cannot move in the same block, e.g. an immutable minTonnesPerUsdc / maxUsdcPerTonne checked as tonnes * 1e6 / held >= floor, or the Aerodrome pool's time-weighted quote (Pool.quote(USDC, held, granularity)) scaled by minOutBps; emit Skipped('priceOff') or revert when violated so the ETH waits. A proof is attached: test/scratch/RegenCreditLegSandwich.t.sol mirrors the live pool with Klima's two Aerodrome formulas and fails on this code (attacker 15,000 -> 15,416.19 USDC, 7.785 t retired against 30.557 t fair); it passes once a second-leg floor makes the manipulated batches revert or skip.

**Reproduction**

Fork Base at block 52335751 (test/scratch/JudgeFork.t.sol, FOUNDRY_PROFILE=fork): registry with project 1, router with the real aggregator 0xdA0A793D..., USDC, class vault 0xf4699531..., credits C02-004/003/006, UniswapV3Venue fee 500, Chainlink feed, minBatch 0.001 ETH, maxBatch 0.05 ETH, bountyBps 50, minOutBps 9700. Depositor deposits 0.05 ETH for project 1. Attacker (holding 8,000 USDC): transfer 8,000 USDC to the Aerodrome pool and swap for kVCM; call router.process(1, depositor); sell all kVCM back. Expected: the caller cannot profit beyond the bounty and the batch retires ~6.20 t. Actual: attacker USDC +31,197,266 (+31.20 USDC), retiredOf(1) = 2.702229 t. Offline: forge test --match-path test/scratch/RegenCreditLegSandwich.t.sol fails with 'process() caller profited from sandwiching the USDC -> kVCM leg: 15416186879 > 15000000000'.

### 2. Medium: Credit liveness is probed with 1 USDC but the batch is quoted with `held`: a credit that can absorb $1 but not the batch leaves one project's USDC to be retired under the next project, or reverts ever

`src/regen/RegenRouter.sol:261`

```
                order[i], 0, 1e6, address(usdc), classVault, 0
```

Merged from audit_math (leftover attribution, medium) and audit_economics (sub-step remainder, low): same root cause and same fix. _firstLiveCredit() (lines 257-273) selects the first credit whose one-dollar quote is non-zero; process() then quotes ALL USDC held (line 175), floors to TONNE_STEP (line 176), reverts NothingRetired on zero (line 177) and retires with maxInputTokenIn = held. The contract's model (lines 33-35, test_dustCarriesToTheNextBatch) is that the leftover is under one tonne step (~20 micro-USDC). That only holds when the chosen credit can absorb the whole batch. The A/B/C fall-through exists precisely for a credit running dry, and in that state the two quotes disagree. (a) If the aggregator caps the quote to the remaining supply (the semantics the project's own MockAggregator in test/unit/RegenRouter.t.sol lines 135-136 models), the retirement spends only part of `held` and the rest, up to a full batch (~$125 at maxBatch), stays in the router with no per-project attribution; the next process() for ANY project (anyone can register one and deposit minBatch) falls through to the next credit and retires the leftover with that project's beneficiary, name and regen address in RetireDetails and in the retirement message that Regen indexes. Attribution with the project as beneficiary is the stated purpose of the rail. (b) If the remaining supply is non-zero but under 1e-6 t, the probe passes, the floored batch quote is 0 and every process() for every project reverts NothingRetired until some third party changes that credit's remainder on Klima. (c) If the live aggregator instead reverts the `held` quote (line 175 is outside try/catch), the same halt occurs. The live quote at block 52487147 caps at the pool (1e12 USDC -> 784.75 t) so the supply-cap branch could not be exercised on the fork; the code-level mismatch is independent of which branch the diamond takes. Fix: run the real `held` quote per credit in fixed order inside try/catch and take the first whose floored tonnes is non-zero AND whose tokenAmount (second return) covers held minus one step; otherwise emit Skipped('classEmpty'). Alternatively compare spent against held after the retirement and either fall through in the same call or keep a per-project USDC carry so leftover is only retired for the project that paid for it.

**Reproduction**

Supply-capping aggregator (same semantics as test/unit/RegenRouter.t.sol MockAggregator), 22 USDC/t, creditA 0.1 t left ($2.20), creditB/C stocked; bountyBps 50, minBatch 0.001 ETH, maxBatch 0.05 ETH. Project 1 (beneficiary victimSafe) deposits 0.02 ETH; process(1, depositor) swaps 0.0199 ETH -> 49.75 USDC, probe passes on creditA, quote is capped to 0.1 t, retirement pulls 2.20 USDC, 47.55 USDC stays. Attacker registers project 2 (beneficiary attacker), deposits 0.001 ETH, calls process(2, attacker): held = 50.0375 USDC, creditB retires 2.274431 t with beneficiaryAddress = attacker. Expected: project 2's retirement is paid only by its own 2.4875 USDC. Actual: the aggregator pulls 50,037,482 micro-USDC for the attacker's project; retiredOf(2) = 2.274431e18, retiredOf(1) = 0.1e18. forge test --match-path test/scratch/RegenRouterLeftoverAttribution.t.sol fails with '50037482 > 2487501'. Branch (b): setCredit(creditA, 5e11), setCredit(creditB, 1000e18), setCredit(creditC, 1000e18), deposit 0.05 ETH, process(1, depositor): expected creditB retires 5.6 t; actual revert NothingRetired() for every caller (test/scratch/RegenProbeMismatch.t.sol, the specialist proof, fails with NothingRetired()).

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {RegenRegistry} from "src/regen/RegenRegistry.sol";
import {RegenRouter} from "src/regen/RegenRouter.sol";
import {
    IKlimaRetirementAggregator,
    RetireDetails,
    DiscountedForwardBalanceContext,
    UpdateLiquidSupplyRateLimiterParams
} from "src/regen/interfaces/IKlimaRetirementAggregator.sol";
import {IEthToTokenSwap, IPriceFeed} from "src/regen/interfaces/IEthToTokenSwap.sol";

contract Usdc6 is ERC20 {
    constructor() ERC20("USDC", "USDC") {}

    function decimals() public pure override returns (uint8) {
        return 6;
    }

    function mint(address to, uint256 a) external {
        _mint(to, a);
    }
}

contract Feed8 is IPriceFeed {
    function decimals() external pure returns (uint8) {
        return 8;
    }

    function latestRoundData() external view returns (uint80, int256, uint256, uint256, uint80) {
        return (1, 2500e8, block.timestamp, block.timestamp, 1);
    }
}

/// @dev Honest pool at exactly the oracle price: 2500 USDC per ETH.
contract Venue is IEthToTokenSwap {
    Usdc6 public token;

    constructor(Usdc6 t) {
        token = t;
    }

    function swapEthToToken(address, uint256 minOut, address to) external payable returns (uint256 out) {
        out = msg.value * 2500e6 / 1e18;
        require(out >= minOut, "venue: min");
        token.mint(to, out);
    }
}

/// @dev Aggregator stand-in with the same semantics as the project's own MockAggregator (test/unit/RegenRouter.t.sol):
///      a quote for more USDC than the credit token can supply is capped to the supply, and the retirement pulls
///      only the USDC the capped tonnes cost. 22 USDC per tonne.
contract CappingAggregator is IKlimaRetirementAggregator {
    Usdc6 public usdc;
    uint256 public constant PRICE = 22e6;
    mapping(address => uint256) public supply;
    address public lastBeneficiary;
    uint256 public lastTonnes;
    uint256 public lastPulled;

    constructor(Usdc6 u) {
        usdc = u;
    }

    function setSupply(address c, uint256 tonnes) external {
        supply[c] = tonnes;
    }

    function quoteRetireCreditForInputTokenInViaKlima(
        address credit,
        uint256,
        uint256 amount,
        address,
        address,
        uint256
    )
        external
        view
        returns (
            uint256 tonnes,
            uint256,
            uint256,
            DiscountedForwardBalanceContext memory d,
            UpdateLiquidSupplyRateLimiterParams memory u
        )
    {
        tonnes = amount * 1e18 / PRICE;
        if (tonnes > supply[credit]) tonnes = supply[credit];
        return (tonnes, tonnes * PRICE / 1e18, PRICE, d, u);
    }

    function quoteRetireCreditViaKlima(address, uint256, uint256, address, address, uint256)
        external
        pure
        returns (
            uint256,
            uint256,
            DiscountedForwardBalanceContext memory d,
            UpdateLiquidSupplyRateLimiterParams memory u
        )
    {
        return (0, 0, d, u);
    }

    function retireCreditViaKlima(
        address credit,
        uint256,
        uint256,
        uint256 tonnes,
        address,
        address,
        uint256 maxIn,
        uint256,
        RetireDetails memory details
    ) external {
        require(tonnes <= supply[credit], "supply");
        uint256 cost = tonnes * PRICE / 1e18;
        require(cost <= maxIn, "slippage");
        require(usdc.transferFrom(msg.sender, address(this), cost), "pull");
        supply[credit] -= tonnes;
        lastBeneficiary = details.beneficiaryAddress;
        lastTonnes = tonnes;
        lastPulled = cost;
    }
}

/// @notice The $1 liveness probe in `_firstLiveCredit` selects a credit token that cannot absorb the batch. The quote
///         for `held` is capped, the retirement spends a fraction of the USDC, and the rest stays in the router as
///         "dust" that is far larger than one tonne step. The next `process` for ANY project retires that USDC with
///         the other project as beneficiary: project 1's regenerative contribution is attributed to project 2.
contract RegenRouterLeftoverAttributionTest is Test {
    RegenRegistry reg;
    Usdc6 usdc;
    CappingAggregator agg;
    RegenRouter router;

    address creditA = makeAddr("creditA");
    address creditB = makeAddr("creditB");
    address creditC = makeAddr("creditC");
    address victimSafe = makeAddr("victim-beneficiary");
    address victimDepositor = makeAddr("victim-depositor");
    address attacker = makeAddr("attacker");

    function setUp() public {
        vm.warp(1_800_000_000);
        reg = new RegenRegistry();
        usdc = new Usdc6();
        agg = new CappingAggregator(usdc);
        router = new RegenRouter(
            RegenRouter.Config({
                registry: reg,
                aggregator: agg,
                usdc: IERC20(address(usdc)),
                classVault: makeAddr("vault"),
                creditA: creditA,
                creditB: creditB,
                creditC: creditC,
                venue: new Venue(usdc),
                ethUsd: new Feed8(),
                maxFeedAge: 3600,
                minBatch: 0.001 ether,
                maxBatch: 0.05 ether,
                bountyBps: 50,
                minOutBps: 9700
            })
        );
        reg.register("Victim", "regen183ht37fsp2fhnq3gneyjycp08c3ju4xnvxnvan", victimSafe);
        // creditA is nearly exhausted: 0.1 t ($2.20) left, which is more than the $1 probe needs.
        agg.setSupply(creditA, 0.1e18);
        agg.setSupply(creditB, 1000e18);
        agg.setSupply(creditC, 1000e18);
        vm.deal(victimDepositor, 1 ether);
        vm.deal(attacker, 1 ether);
    }

    function test_leftoverUsdcFromOneProjectIsRetiredForAnother() public {
        // Project 1 pays in 0.02 ETH; after the 0.5% bounty 0.0199 ETH is swapped for 49.75 USDC.
        vm.prank(victimDepositor);
        router.deposit{value: 0.02 ether}(1);
        // A fixed router may instead revert here (refuse the batch) or fall through to creditB; both are acceptable,
        // what matters is what the attacker can retire with their own 0.001 ETH below.
        try router.process(1, victimDepositor) {} catch {}

        // The attacker registers a project and pays in the minimum batch: 0.001 ETH -> 0.000995 ETH -> 2.4875 USDC.
        vm.startPrank(attacker);
        uint256 attackerProject = reg.register("Attacker", "regen183ht37fsp2fhnq3gneyjycp08c3ju4xnvxnvan", attacker);
        router.deposit{value: 0.001 ether}(attackerProject);
        router.process(attackerProject, attacker);
        vm.stopPrank();

        // The attacker's retirement must be paid for by the attacker's ETH only (allow one tonne step of rounding).
        uint256 attackerOwnUsdc = 2.4875e6;
        assertEq(agg.lastBeneficiary(), attacker);
        assertLe(
            agg.lastPulled(),
            attackerOwnUsdc + 1,
            "project 1's USDC was retired with the attacker's project as beneficiary"
        );
    }
}
```

### 3. Medium: retireCreditViaKlima is not guarded: when the probed credit reverts on retirement (paused, delisted, or 1 wei of it sitting on the diamond) process() reverts for every project with no fall-through to

`src/regen/RegenRouter.sol:179`

```
        aggregator.retireCreditViaKlima(
```

Merged from audit_permissions (medium) and audit_flow (low). _firstLiveCredit() decides from a view quote wrapped in try/catch, but the retirement itself is a bare external call. Any state where the quote succeeds and the retire reverts stops process() for all projects and depositors; the three credit addresses and their order are immutable, so nothing on the router side can route around it, and the ETH stays in balanceOf until the state clears on Klima's side. Two such states are confirmed: (1) a credit whose retire path is paused or delisted while its quote path still prices it (mock); (2) on the live diamond, LibRetire.swapCallerTokenForCarbon ends with a strict `balanceOf(address(this)) != amount` check, so any pre-existing balance of the chosen credit on the aggregator makes every USDC retirement of that credit revert InvalidAmountReceived() (selector 0xc20c3993). Verified on a Base fork at block 52335751: after transferring 1 wei of C02-004 from the class vault to the aggregator, router.process(1, pot) reverts 0xc20c3993. The credit token is a plain transferable ERC20 (the vault's transfer succeeded), but at that block its entire supply (2,089.27 t) sits in the class vault, so the donation path needs an outside party that can obtain credit tokens without retiring them; the pause/delist path needs Klima action. Only Klima's owner can sweep such dust (approveToken). No funds are lost, but the rail is offline for the duration and the Offsets leg keeps bridging into it. Fix: wrap the retirement in try/catch and on failure try the next credit in order (re-quoting for it), or emit Skipped and leave the batch untouched (the ETH must then be re-credited since line 169 has already debited it, and the USDC bought must stay for the next batch), mirroring the feedStale/classEmpty paths. The attached proof fails on this code with 'Paused' and passes once the router falls through or skips.

**Reproduction**

Mock aggregator that quotes every credit at 22 USDC/t but whose retireCreditViaKlima reverts 'Paused' for creditA and succeeds for creditB/C; register project 1, deposit 0.05 ETH, call process(1, depositor). Expected: the batch retires through creditB, or Skipped with the ETH kept. Actual: revert 'Paused'; no project can be processed until the aggregator changes. forge test --match-path test/scratch/RegenRetireNoFallthrough.t.sol fails with 'Paused'. Live shape: FOUNDRY_PROFILE=fork, Base block 52335751, deposit 0.05 ETH for project 1, vm.prank(classVault) C02-004.transfer(aggregator, 1), then process(1, pot) reverts with 0xc20c3993 = InvalidAmountReceived() (test/scratch/JudgeFork.t.sol::test_oneWeiDonationHaltsRetire).

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {RegenRegistry} from "src/regen/RegenRegistry.sol";
import {RegenRouter} from "src/regen/RegenRouter.sol";
import {
    IKlimaRetirementAggregator,
    RetireDetails,
    DiscountedForwardBalanceContext,
    UpdateLiquidSupplyRateLimiterParams
} from "src/regen/interfaces/IKlimaRetirementAggregator.sol";
import {IEthToTokenSwap, IPriceFeed} from "src/regen/interfaces/IEthToTokenSwap.sol";

/// @notice `_firstLiveCredit` picks a credit from a view quote, but `retireCreditViaKlima` is called outside any
///         try/catch. When the chosen credit quotes fine and the retirement reverts (paused or delisted token, or on the
///         live diamond any pre-existing balance of that credit on the aggregator, which makes LibRetire revert), every
///         process() for every project reverts and the two other credits are never tried. This test fails on this code
///         with "Paused" and passes once the router falls through to the next credit (or emits Skipped and keeps the ETH).
contract U is ERC20 {
    constructor() ERC20("USDC", "USDC") {}

    function decimals() public pure override returns (uint8) {
        return 6;
    }

    function mint(address to, uint256 a) external {
        _mint(to, a);
    }
}

contract Feed is IPriceFeed {
    function decimals() external pure returns (uint8) {
        return 8;
    }

    function latestRoundData() external view returns (uint80, int256, uint256, uint256, uint80) {
        return (1, 2500e8, block.timestamp, block.timestamp, 1);
    }
}

contract Venue is IEthToTokenSwap {
    U immutable t;

    constructor(U u) {
        t = u;
    }

    function swapEthToToken(address, uint256 minOut, address to) external payable returns (uint256 out) {
        out = msg.value * 2500e6 / 1e18;
        require(out >= minOut, "venue: min");
        t.mint(to, out);
    }
}

/// @dev Quotes every credit at 22 USDC/t; the retirement of `pausedCredit` reverts, the others succeed.
contract Agg is IKlimaRetirementAggregator {
    U immutable u;
    address public immutable pausedCredit;
    address public lastCredit;
    uint256 public retirements;

    constructor(U u_, address paused) {
        u = u_;
        pausedCredit = paused;
    }

    function quoteRetireCreditForInputTokenInViaKlima(address, uint256, uint256 amount, address, address, uint256)
        external
        pure
        returns (
            uint256,
            uint256,
            uint256,
            DiscountedForwardBalanceContext memory d,
            UpdateLiquidSupplyRateLimiterParams memory l
        )
    {
        return (amount * 1e18 / 22e6, amount, 22e6, d, l);
    }

    function quoteRetireCreditViaKlima(address, uint256, uint256, address, address, uint256)
        external
        pure
        returns (
            uint256,
            uint256,
            DiscountedForwardBalanceContext memory d,
            UpdateLiquidSupplyRateLimiterParams memory l
        )
    {
        return (0, 0, d, l);
    }

    function retireCreditViaKlima(
        address c,
        uint256,
        uint256,
        uint256 tonnes,
        address,
        address,
        uint256,
        uint256,
        RetireDetails memory
    ) external {
        require(c != pausedCredit, "Paused");
        u.transferFrom(msg.sender, address(this), tonnes * 22e6 / 1e18);
        lastCredit = c;
        ++retirements;
    }
}

contract RegenRetireNoFallthroughTest is Test {
    RegenRouter router;
    Agg agg;
    address creditA = makeAddr("C02-004");
    address creditB = makeAddr("C02-003");
    address creditC = makeAddr("C02-006");
    address depositor = makeAddr("pot");

    function setUp() public {
        vm.warp(1_800_000_000);
        RegenRegistry reg = new RegenRegistry();
        reg.register("IMDO", "regen183ht37fsp2fhnq3gneyjycp08c3ju4xnvxnvan", makeAddr("imdo-safe"));
        U usdc = new U();
        agg = new Agg(usdc, creditA);
        router = new RegenRouter(
            RegenRouter.Config({
                registry: reg,
                aggregator: agg,
                usdc: IERC20(address(usdc)),
                classVault: makeAddr("vault"),
                creditA: creditA,
                creditB: creditB,
                creditC: creditC,
                venue: new Venue(usdc),
                ethUsd: new Feed(),
                maxFeedAge: 3600,
                minBatch: 0.001 ether,
                maxBatch: 0.05 ether,
                bountyBps: 50,
                minOutBps: 9700
            })
        );
        vm.deal(depositor, 1 ether);
    }

    function test_retireRevertOnFirstCreditDoesNotHaltTheRouter() public {
        vm.prank(depositor);
        router.deposit{value: 0.05 ether}(1);
        // Expected: the batch is retired through creditB (or Skipped with the ETH kept). Actual: revert "Paused".
        router.process(1, depositor);
        if (agg.retirements() != 0) {
            assertEq(agg.lastCredit(), creditB, "fell through to the next credit");
        } else {
            assertEq(router.balanceOf(1, depositor), 0.05 ether, "skipped: ETH stays credited");
        }
    }
}
```

### 4. Low: Flooring to TONNE_STEP leaves no slack for the aggregator's round-up: some batch sizes revert SlippageExceeded by one micro-USDC and cannot be processed until the pools move

`src/regen/RegenRouter.sol:176`

```
        tonnes = tonnes / TONNE_STEP * TONNE_STEP;
```

From audit_permissions, reproduced exactly. The router quotes tonnes for exactly `held`, floors to 1e12 and retires with maxInputTokenIn = held. The live aggregator computes the USDC it needs for the floored tonnes with a round-up, so when the flooring removes almost nothing the requirement exceeds held by one micro-USDC and retireCreditViaKlima reverts SlippageExceeded(required, held). ethIn is fixed at min(balance, maxBatch), so for a given pool state the revert is deterministic for that depositor's balance; the batch waits until the WETH/USDC or USDC/kVCM pool moves enough to change `held`, and a keeper that sent the transaction pays ~4M gas for nothing. The specialist's sweep of 40 sizes hit it once. No ETH is lost. Fix: quote for held minus a small margin (e.g. 1e3) while still passing held as maxInputTokenIn, or after flooring check quoteRetireCreditViaKlima(credit, 0, tonnes, usdc, classVault, 0).retirementPrice <= held and subtract one more TONNE_STEP if not.

**Reproduction**

FOUNDRY_PROFILE=fork, Base block 52335751, router with bountyBps 50, minOutBps 9700, maxBatch 0.05 ETH, UniswapV3Venue fee 500: deposit 16076923077018104 wei for project 1 and call process(1, depositor). Expected: a retirement of the floored tonnes with up to ~20 micro-USDC of dust. Actual: revert 0x71c4efed SlippageExceeded(40534313, 40534312) from the aggregator (test/scratch/JudgeFork.t.sol::test_roundingSlippageExceeded logs the raw revert bytes).

### 5. Low: Remainders below minBatch, including a forfeited bounty, are stranded per (project, depositor) with no way to retire them

`src/regen/RegenRouter.sol:155`

```
        if (balance < minBatch) revert BelowMinBatch(balance, minBatch);
```

From audit_math, reproduced. process() takes min(balance, maxBatch) and refuses any balance under minBatch; there is no withdrawal, no merge across depositors and no sub-minimum path, so whenever balance mod maxBatch lands in (0, minBatch) the last slice is stuck until the SAME depositor deposits again for the SAME project. A bridge receiver tops itself up, but a one-off direct depositor (a Safe, which the contract's own doc names as a use case) loses up to minBatch (~$2.5 at 0.001 ETH) for good. The bounty-forfeit path (line 210) makes a new stranded bucket on its own: a keeper contract that cannot take ETH re-credits bountyBps of the batch (0.00025 ETH at 50 bps) into the depositor's balance, which is itself below minBatch. Design intent ('dust is not worth the gas') is documented, but the forfeited bounty being unreachable is not. Options that keep the design: let process() accept a sub-minBatch balance when the caller waives the bounty, or let a depositor fold its remainder into another depositor's balance for the same project, or at least document the loss bound.

**Reproduction**

minBatch 0.001 ETH, maxBatch 0.05 ETH, bountyBps 50 (test/scratch/JudgeUnit.t.sol::test_remainderStuck). Depositor deposits 0.0505 ETH for project 1; an EOA keeper calls process(1, depositor): ethIn = 0.05, balance = 0.0005 ETH; process(1, depositor) now reverts BelowMinBatch(500000000000000, 1000000000000000). Depositor tops up to 0.05 ETH; a contract without receive() calls process(): bounty 0.00025 ETH is forfeited into balanceOf[1][depositor]; process() reverts BelowMinBatch(250000000000000, 1000000000000000). Expected: every deposited wei is eventually retirable.

### 6. Low: Registry uniqueness is byte-exact: case, interior-space and look-alike variants of a registered name are accepted with other beneficiaries, defeating the stated reason for unique names

`src/regen/RegenRegistry.sol:43`

```
        bytes32 h = keccak256(bytes(name));
```

Merged from four specialists (economics info, math low, permissions low, flow low). The contract's own rationale (lines 12-13) is that a second 'IMDO' would carry a different beneficiary and confuse every reader of the retirement log. The check hashes the raw bytes, so 'imdo', 'IM DO', 'IMD0', 'IMDO  x' (double inner space) and 'IMDO (official)' all register permissionlessly with any beneficiary and regen address, and each appears as beneficiaryString and as the name: field of the retirement message in Klima's events and Regen's index. Grammar v1 itself cannot be broken (no '|', no control characters, no leading/trailing space; ':' inside a name does not split the ' | '-separated fields). test_nameIsUniqueCaseSensitive asserts the current behaviour, so this is a limitation to decide on rather than an accident; on-chain readers can key on id or beneficiary. Fix if wanted: hash a normalised key (lowercase ASCII, collapsed runs of spaces) in idByName while storing the display name as given; grammar v1 is unchanged.

**Reproduction**

register('IMDO', R, A) -> 1; register('imdo', R, B) -> 2; register('IM DO', R, C) -> 3; register('IMD0', R, D) -> 4; register('IMDO  x', R, D) -> 5; only register('IMDO', R, E) reverts NameTaken(1) (test/scratch/JudgeUnit.t.sol::test_registryLookalikes). Expected per lines 12-13: the variants collide with id 1.

### 7. Low: Regen address checksum is not verified and a registration is permanent: a mistyped address burns the project's unique name and every retirement for that id carries an address nobody controls

`src/regen/RegenRegistry.sol:82`

```
            if (!_bech32Char(s[i])) return false;
```

From audit_flow, reproduced. Only the length, the 'regen1' prefix and the bech32 charset are checked; the six-character bech32 checksum is not. Any 38 charset characters pass. Because there is no update or delete and names are unique, a typo takes the name permanently: deposits and process() work from the moment register() returns (nothing on chain is provisional, contrary to the comment at lines 72-73), so retirements are written with a regen: field no Regen indexer will accept and the credits cannot be mirrored to the intended account. The grammar is not at risk and the credits are only landed by Regen after its own verification, so this is an operational trap rather than a fund-safety defect. Fix: verify the bech32 checksum on chain (polymod over the 5-bit data, ~40 iterations, a few thousand gas) so BadRegenAddress rejects it; or allow the registrant a one-time correction before the first retirement; at minimum document that the address must be checksum-verified off chain before the registration transaction is sent.

**Reproduction**

register('Typo', 'regen183ht37fsp2fhnq3gneyjycp08c3ju4xnvxnvaq', 0x5) (last character of the valid test address changed, checksum invalid). Expected: BadRegenAddress. Actual: returns id 2 and 'Typo' is taken forever (test/scratch/JudgeUnit.t.sol::test_registryBadChecksumAccepted).

### 8. Low: Receiver addresses are predictable for ids that do not exist yet and ids are sequential and permissionless: a forwarder fixed to predict(id) before the project's register() lands can be captured by wh

`src/regen/RegenReceiver.sol:54`

```
    function predict(uint256 projectId) public view returns (address) {
```

Merged from audit_flow (receiver front-run) and audit_permissions (name squatting): one deploy-order hazard. predict(id) is valid before the id exists (by design, so OffsetsForwarder.receiverOnBase can be fixed first), deploy() only requires that SOME project holds the id, register() is permissionless and ids are sequential, and OffsetsForwarder.receiverOnBase and ImdoTreasury.offsetsSafe are immutable. If the forwarder is constructed on Ethereum (or the treasury funded) before IMDO's register() lands on Base, anyone who registers first takes that id with their own name, regen address and beneficiary; every ETH leg bridged thereafter is retired under that identity and nothing can redirect it. The same first-come rule lets a watcher take the name 'IMDO' with their own beneficiary if the registry is deployed in one transaction and the project registered in a later one. The CREATE2 prediction itself is correct (salt = id, init code = creationCode ++ abi.encode(router, id), asserted in deploy()). The tree has no written deployment order for the rail (docs cover the IMDO launch only) and the forwarder constructor cannot check Base state. Fix: register the project and deploy its receiver on Base first, record the id, and only then construct the forwarder; register the first projects in the registry's deployment transaction; or derive the receiver salt from keccak256(name, beneficiary) so a predicted address cannot be claimed by a different registration.

**Reproduction**

test/scratch/JudgeUnit.t.sol::test_receiverIdFrontRun: factory.predict(2) is taken as the forwarder target while only project 1 exists; a squatter calls registry.register('Squat', R, squatter) and gets id 2; factory.deploy(2) succeeds; 0.05 ETH 'bridged' to the predicted address is forwarded and process(2, receiver) retires it with beneficiary = squatter, retiredOf(2) > 5.6 t. Expected: the leg is retired for the intended project.

### 9. Low: OffsetsForwarder and ImdoTreasury point at each other through immutables with no code check: the shipped scripts seat a Safe as offsetsSafe, and a mispredicted treasury address makes forward() revert

`src/regen/OffsetsForwarder.sol:48`

```
        try treasury.payOffsets() {} catch {}
```

Merged from audit_economics, audit_permissions and audit_flow. ImdoTreasury.payOffsets() pays only its immutable offsetsSafe (src/ImdoTreasury.sol:235-240); OffsetsForwarder's treasury is immutable and non-zero-checked (line 35). Whichever is deployed second must be given a predicted address of the first. script/DeployImdo.s.sol:93-110 passes c.offsetsSafe straight from config with no forwarder step, script/rehearse-mainnet.sh:8 sets OFFSETS to a Safe (0xb41E9b47..., the same address as REGEN) and docs/DEPLOYMENT.md:12 still calls offsetsSafe a Safe. As rehearsed, the forwarder is not the seat: payOffsets() reverts Unauthorized inside the try/catch and forward() reverts NothingToForward while the 25% Offsets leg accrues to the Safe. Separately, payOffsets() has no return value, so Solidity 0.8.26 performs the extcodesize check in the caller before the call; try/catch does not cover it. A forwarder built against an address with no code (a nonce shift in the multi-transaction broadcast that docs/DEPLOYMENT.md already warns about) reverts on every forward() and whatever ETH it holds can never be bridged, contrary to the 'nothing can be stranded' comment at lines 20-22. Nothing in the treasury can brick a correctly seated forwarder: payOffsets is nonReentrant, pays by a plain call the empty receive() accepts, and a reverting pull is swallowed. Fix: require treasury_.code.length != 0 and bridge_.code.length != 0 in the constructor; in the deploy script predict the forwarder address ahead of the treasury (as DeployImdo already does for expectedClaim) and assert treasury.offsetsSafe() == address(forwarder) and forwarder.treasury() == treasury after deployment; or make the pull a low-level call so a codeless target cannot block bridging.

**Reproduction**

(1) new OffsetsForwarder(IOffsetsSource(0xBEEF), bridge, receiver, 100000) with 0xBEEF having no code; vm.deal(forwarder, 1 ether); forwarder.forward(). Expected per the @dev comment: bridges 1 ETH. Actual: reverts before the try/catch, bridge received 0 (test/scratch/JudgeUnit.t.sol::test_codelessTreasuryStrandsForwarder). (2) Deploy per script/DeployImdo.s.sol with offsetsSafe = S (a Safe), then deploy OffsetsForwarder(treasury, bridge, receiver, gas); fund the treasury and call treasury.process() so offsetsOwed > 0; forwarder.forward(): payOffsets reverts Unauthorized (caught), balance 0, revert NothingToForward; offsetsOwed stays claimable only by S (same shape as test/unit/RegenReceiver.t.sol test_onlyTheForwarderCanPullTheLeg with the roles swapped).

### 10. Low: OffsetsForwarder accepts any minGasLimit: a value above the OP Stack resource limit makes forward() revert on every call and permanently strands the treasury's Offsets leg; zero makes every relay need

`src/regen/OffsetsForwarder.sol:41`

```
        minGasLimit = minGasLimit_;
```

Merged from audit_economics (info), audit_math (low) and audit_permissions (info). minGasLimit is a uint32 immutable with no bounds. It flows to L1StandardBridge.depositETHTo -> L1CrossDomainMessenger.sendMessage, whose baseGas() adds overhead and multiplies by 64/63 before OptimismPortal.depositTransaction meters it against the resource config (maxResourceLimit 20,000,000). Verified on an Ethereum mainnet fork against the real bridge 0x3154Cf16ccdb4C6d922629664174b904d80F2C35: a forwarder built with type(uint32).max reverts on forward() with 1 ETH held, while 100,000 bridges it. Because ImdoTreasury.offsetsSafe is immutable and payOffsets() pays only that address, a forwarder deployed with an unusable value has no second chance: the whole Offsets leg (25% of every processed fee) is unpullable on either side. At the other end, 0 is accepted and bridges on L1, but every L2 finalisation then fails its gas check and sits in L2CrossDomainMessenger.failedMessages until someone replays it with more gas (the ETH is not lost; the receiver's empty receive() needs on the order of 50-60k gas including finalizeBridgeETH). Fix: bound the constructor argument, e.g. 50_000 <= minGasLimit_ <= 1_000_000, and document the replay procedure.

**Reproduction**

FOUNDRY_PROFILE=fork, Ethereum mainnet fork (test/scratch/JudgeBridgeFork.t.sol): new OffsetsForwarder(src, 0x3154Cf16..., 0xBEEF, type(uint32).max); vm.deal(f, 1 ether); f.forward() reverts (test_hugeMinGasLimitRevertsForever); the same with 100_000 bridges the ETH and leaves balance 0; with 0 the constructor and forward() also succeed (test_zeroMinGasLimitAccepted). Expected: the constructor rejects a limit that cannot execute finalizeBridgeETH or cannot be deposited at all.

### 11. Info: Feed handling: a future updatedAt makes process() revert with a checked-arithmetic panic instead of Skipped; min/maxAnswer clamp, round completeness and the Base sequencer uptime feed are not consider

`src/regen/RegenRouter.sol:243`

```
        if (answer <= 0 || updatedAt == 0 || block.timestamp - updatedAt > maxFeedAge) return 0;
```

Merged from audit_math and audit_permissions. Decimals are right (ethIn 1e18 x price 1e8 / 1e20 -> USDC 1e6; the fork fill lands 0.07% under Chainlink) and negative, zero and stale answers skip as documented. Gaps, all liveness-only: (1) updatedAt > block.timestamp underflows and process() reverts Panic(0x11) rather than emitting Skipped('feedStale'); Chainlink's proxy takes updatedAt from the update block so this needs a replaced or misbehaving feed; (2) the aggregator's minAnswer/maxAnswer clamp is not handled: if ETH trades below minAnswer the floor demands more USDC than any pool pays and process() reverts SwapShort until the market recovers (ETH stays credited); (3) roundId/answeredInRound are not compared and the L2 Sequencer Uptime Feed is not consulted, so after a sequencer outage shorter than maxFeedAge the last pre-outage answer is accepted. The 97% floor and the 0.05 ETH cap bound the value at stake. Fix: `updatedAt > block.timestamp || block.timestamp - updatedAt > maxFeedAge` and, optionally, the uptime feed.

**Reproduction**

MockFeed.set(2500e8, block.timestamp + 1); depositor has 0.01 ETH credited; router.process(1, depositor). Expected: Skipped(1, depositor, 'feedStale') and return. Actual: revert with arithmetic underflow (panic 0x11) (test/scratch/JudgeUnit.t.sol::test_futureUpdatedAtPanics).

### 12. Info: UniswapV3Venue does not pin the output token: WrongToken only rejects WETH, unlike the stated 'anything but the configured token path'

`src/regen/UniswapV3Venue.sol:41`

```
        if (token == weth) revert WrongToken();
```

Merged from audit_economics and audit_math. The venue has no configured output token; it swaps WETH into whatever `token` the caller names at the fixed fee tier. The router always passes its immutable USDC and checks its own USDC balance delta, and the venue holds nothing and delivers to `to`, so no funds are at risk; anyone may use it as a generic WETH -> X swapper at their own cost. Reported so the documented guarantee matches the code: either amend the spec or add a `token` immutable and compare against it.

**Reproduction**

venue.swapEthToToken{value: 1 wei}(someOtherToken, 0, to) does not revert WrongToken; it attempts a WETH -> someOtherToken swap at the configured fee (test/scratch/JudgeUnit.t.sol::test_venueNotPinned: only the WETH call reverts WrongToken). Expected per the task description: WrongToken for anything but the configured token.

### 13. Info: Bounty does not cover process() gas at the lower end of the batch range; the bounty cannot be farmed, and the thin pool is Aerodrome's, not Uniswap's

`src/regen/RegenRouter.sol:170`

```
        uint256 bounty = ethIn * bountyBps / BPS;
```

From audit_permissions, confirmed. A real process() on the Base fork costs ~3.99M gas (gas report: 3,987,207 and 3,991,086 for the two fork runs; two aggregator quotes, the V3 swap and the Klima diamond retirement). With minBatch 0.001 ETH and bountyBps in the tens, the bounty is 0.00001 to 0.00005 ETH; at a Base base fee of 0.01 to 0.05 gwei the call costs 0.00004 to 0.0002 ETH, so batches below roughly 0.01 to 0.05 ETH are not worth a third-party keeper's gas and a sub-maxBatch remainder can wait until the project processes it itself. Conversely the bounty cannot be farmed: a 0.001 ETH deposit yields at most a few ten-thousandths of itself while the rest is retired, so a farmer always loses. Sizing against the WETH/USDC 0.05% V3 pool is sound (millions of USDC of depth; a 0.05 ETH batch moves it far less than the 3% floor); the ~15k USDC Aerodrome USDC/kVCM pool is the thin one (see the high finding).

**Reproduction**

FOUNDRY_PROFILE=fork forge test --gas-report on test/fork/RegenRouterBaseFork.t.sol: process(1, ...) 3,987,207 gas for a 0.01 ETH batch. Bounty at 50 bps on minBatch = 0.000005 ETH; gas at 0.02 gwei = 0.00008 ETH. Expected per the design ('the caller earns bountyBps of the batch'): a positive keeper margin. Actual: negative at minBatch.

### 14. Info: Trust assumption: the Klima aggregator, class vault, credit tokens and Aerodrome pool are immutable dependencies with no exit; a Klima migration ends the rail while the treasury keeps bridging into it

`src/regen/RegenRouter.sol:119`

```
        aggregator = c.aggregator;
```

From audit_economics; reported as the brief asks, not as a code defect. The aggregator is an EIP-2535 diamond whose owner can replace facets, change the USDC/kVCM/pool configuration or delist credits; the credit tokens are registry tokens under Klima's control. The router hardcodes all of them. If all three credits stop quoting, process() emits Skipped('classEmpty') forever and balanceOf keeps the ETH with no withdrawal, while OffsetsForwarder keeps bridging the treasury's 25% leg into the dead router because ImdoTreasury.offsetsSafe is immutable too. Each process() also hands the diamond an allowance of exactly `held` and trusts its retire path, so a malicious facet upgrade could take one batch plus dust per call without retiring. The project should document that a Klima migration permanently ends the rail and decide the Ethereum-side policy in advance (a forwarder whose receiver can be re-pointed by a timelocked role, or accepting that the Offsets accrual would then have to stop).

**Reproduction**

Mock the aggregator to revert every quote (test/unit/RegenRouter.t.sol test_emptyClassSkipsAndKeepsTheEth with all three credits unsupported): deposit 0.05 ETH, process(): Skipped('classEmpty'), balance unchanged; no function returns the ETH to the depositor or the project. Expected by design; listed so the dependency is explicit.

---

Judge's submission `4071b5866b009929f0267ae021640429af8ac3a4f6d690cf85e1d05bcc5cd1b0`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
