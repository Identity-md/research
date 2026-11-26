**Morpho Midnight Adapter — security review deliverable**

26 November 2026. Requester-only deliverable. No submissions, accounts or team contact.

**Result: two findings survived the independent technical checks, both rated Low. No Medium or High finding survived.** Neither demonstrated theft or depositor loss. Both may reasonably be classified Informational, and their competition eligibility remains **UNVERIFIED**: the prior-audit registers have source-validation flags, and documented behavior overlaps both mechanisms. The report preserves those qualifications rather than treating a passing PoC as proof of eligibility.

| Finding | Proposed severity | Demonstrated effect | Independent evidence |
| --- | --- | --- | --- |
| [ACC-1: Partial fills consume more shortfall allowance](#acc-1) | Low: Low impact × Medium likelihood | A 10,000-unit sale uses 50.069921111211219809 tokens of allowance in one fill versus 52.599017994081945687 in 20 fills. With a 51-token allowance, the final partial fill fails. | `verify/accounting`: unchanged PoC, fresh pinned clone, 10 passing tests including inherited tests. |
| [FUZZ-1: Direct revocation leaves unused whitelist approvals valid](#fuzz-1) | Low: Medium impact × Low likelihood | A revoked borrower submits an outstanding approval and then borrows 1e18 base units against collateral. | `verify/fuzz`: unchanged PoC, fresh pinned clone, two passing tests after artifact prebuild; six additional bounding tests. |

[Ranked observations](#observations), [coverage/limits](#coverage), [complete proofs](#proofs), [provenance](#provenance).

**Target and evidence standard**

Repository: [morpho-org/vault-v2](https://github.com/morpho-org/vault-v2/tree/bbeda7b27ae80abcf070e0158cb8a31e87bb2286), commit `bbeda7b27ae80abcf070e0158cb8a31e87bb2286`; Midnight dependency `4e2570e51171d09228645b2d5bdf84ef24b1720b`. The goal record has `trunk: null`: no separate code repository or merged code-wave commit exists. Complete sources of the two finding tests are embedded below.

Scope under `src/adapters/midnight/`: `MidnightAdapter.sol`, `MidnightAdapterFactory.sol`, `gates/IKRCompatibleEnterGate.sol`, `gates/IKRCompatibleEnterGateFactory.sol`, `gates/WhitelistEnterSubGate.sol`, `gates/WhitelistEnterSubGateFactory.sol`, `libraries/PackedDurationsLib.sol`, both `ratifiers/MidnightAdapter{Price,Rate}RatifierV1.sol`, and interfaces under `interfaces/`, `gates/interfaces/`, `ratifiers/interfaces/`. Vault V2 and Midnight code are integration context. References use pinned checkout line numbers.

Previous audit findings, expected trusted-role behavior and accepted risks are excluded. The initial register reports reading adapter README/NatSpec, Vault V2 and Midnight docs and the linked May 2026 whitepaper. That register is available here through the goal notes and `root-1-01`; fresh verification of the whitepaper coverage is **UNVERIFIED**.

**Independent reproduction** means a different worker reran the finding on a clean pinned clone and attempted refutation: ACC-1 and FUZZ-1 meet this standard. GATE-1 and N1–N4 received independent tests written from scratch but are not additional vulnerabilities. **Author-tested; independent verification UNVERIFIED** identifies notes without the separate refutation step. **UNVERIFIED** also marks static claims, missing execution/source validation and untested fixes. Workflow acceptance is not behavioral certification.

`b01-build` reports `forge build` succeeded in 450 seconds using Forge 1.8.3 and solc 0.8.19/0.8.21/0.8.26/0.8.28/0.8.34/0.8.37. Exact full-suite summary:

```text
Ran 61 test suites in 294.23s (567.07s CPU time): 850 tests passed, 0 failed, 0 skipped (850 total tests)
```

| Baseline command | Passed | Failed | Skipped |
| --- | ---: | ---: | ---: |
| `forge test --match-path 'test/MidnightAdapter*.sol'` | 390 | 0 | 0 |
| `forge test --match-path test/integration/MidnightAdapterIntegrationTest.sol` | 8 | 0 | 0 |
| `forge test --match-path test/PackedDurationsLibTest.sol` | 2 | 0 | 0 |
| `forge test` | 850 | 0 | 0 |

The narrower runs overlap the full suite. These are landed results, not Foundry runs performed during writing.

[Cantina's published matrix](https://docs.cantina.security/standards/severity/competition), checked during report preparation, maps Low impact/Medium likelihood and Medium impact/Low likelihood to Low. Protocol intent and prior acknowledgement also affect eligibility. The competition-specific page could not be independently reopened; its additional rules remain subject to the source limitations below.

<a id="acc-1"></a>
**ACC-1 — Partial fills consume more shortfall allowance than the equivalent single sale**

**Severity: Low, with Informational plausible.** Impact is operational: the guardrail can interrupt an intended sale sooner than a single-fill budget predicts. Likelihood is Medium because outside takers can choose partial-fill sizes on an already-ratified maker sell offer; ordinary fragmented execution has the same effect. No malicious curator or allocator is needed to split that offer. The allocator-take comparison is supporting arithmetic evidence only. No depositor loss or material NAV mispricing was demonstrated. Evidence: `b03-accounting.candidates[0]`, `b04-accounting.checks[0]`.

**Affected code:** [MidnightAdapter.sol:643–648](https://github.com/morpho-org/vault-v2/blob/bbeda7b27ae80abcf070e0158cb8a31e87bb2286/src/adapters/midnight/MidnightAdapter.sol#L643-L648) computes and charges each sale's shortfall; [lines 649–686](https://github.com/morpho-org/vault-v2/blob/bbeda7b27ae80abcf070e0158cb8a31e87bb2286/src/adapters/midnight/MidnightAdapter.sol#L649-L686) distribute it over active markets, including the sold market. Related documentation: lines 145–148 and adapter README lines 112–124.

`onSell` values the sold credit using the market's current `netRate`. If proceeds are below that amortized value, it subtracts the difference from `shortfallAllowance`. The spread then lowers rates to absorb the shortfall, including the rate on the sold market's remaining credit. Its remaining credit consequently has a higher book value per unit. A later partial fill at the same price is charged against that revised value and consumes additional allowance. Equal completed aggregate sales can therefore consume different budgets while ending with essentially the same portfolio value.

The reachable outside-taker sequence is:

1. The vault already holds a seven-day credit position bought for 100,000 asset tokens. One day elapses.
2. An allocator ratifies a 10,000-unit maker sell offer at price `989932200000000000` (WAD). The curator supplies 51 tokens of shortfall allowance through the normal configuration path.
3. One outside taker can fill all 10,000 units in one call, consuming `50069921111211219809` base units of allowance.
4. From the same snapshot, that taker instead tries twenty 500-unit fills. Nineteen fills complete, totaling 9,500 units. The twentieth fails with `ShortfallAllowanceExceeded`, selector `0x8ea54d94`.

The log says `fill reverted at piece 19` because the loop is zero-indexed. It is the **20th attempted fill**, not the 19th. At that point the allowance is not literally zero: `49834436012548795750` of the initial `51000000000000000000` has been consumed. The remaining budget is insufficient for the next 500-unit fill. Smaller shortfall trades can still fit; this is not an unconditional freeze of every sale.

The second test completes both paths with ample allowance, isolating the equal-volume effect:

| Measurement, 18-decimal asset | One sale | Twenty sales |
| --- | ---: | ---: |
| Credit sold | 10,000 tokens | 10,000 tokens |
| Allowance consumed, base units | 50069921111211219809 | 52599017994081945687 |
| Final idle + `realAssets`, base units | 100084346798189681319247 | 100084346798608551701820 |
| Final `netRate` | 8735599645 | 8735599636 |

The additional charge is `2529096882870725878` base units, about **5.05%**. The NAV difference is less than 0.000001 token, within the test's rounding tolerance. Do not compare the incomplete maker run's consumed budget with the complete single-fill run as if the sold amounts were equal. The 51-token example has only about 1.86% headroom above the single-fill charge and is a deliberately tight configuration, not a claim about typical deployments.

**Independent challenge:** the unchanged PoC used real Vault V2, Midnight, adapter and price ratifier with token/oracle fixtures; production code was untouched. Six-decimal reruns reported charges of 50,069,921 versus 52,599,028 base units and the same final-fill failure. The checker also varied size, fill count, price and market composition, but its supplemental `Variants.t.sol` source was not supplied; those variants are not necessary to reproduce this finding. (`b04-accounting`.)

**Limits and exclusion check:** sales at or above book value, force-sellable sales and withdrawals are unaffected by this allowance issue. Raising the allowance uses `increaseShortfallAllowance` and its timelock; other configured exit routes may remain available. The adapter README explicitly defines consumption per below-book sale and describes these controls as operational aids. Thus the evidence establishes fill-size dependence, not a contradiction of a promised fill-size invariant. The checker distinguishes Cantina 3.1.1 (deferred allocator-controlled losses), 3.6.6 (buy-side partition rounding) and TrustSec R-7/R-14 (bounds/rounding). Both prior drafts predate this allowance according to the independent check. `known2/more` found no exact documentary duplicate, but its flagged provenance leaves competition novelty **UNVERIFIED**. This operational interpretation is why Informational remains plausible.

**Suggested fix — UNVERIFIED:** first decide whether the budget is intended to measure economic shortfall independently of fill partitioning. If so, keep a distinct allowance-accounting basis that does not reprice previously absorbed shortfall as a new charge, with explicit rules for buys, losses and time passage. Test single versus split fills across multiple markets and both decimal configurations before adopting it. Merely taking each callback's pre-sale rate is insufficient: the current code already does that. If per-fill current-value accounting is intended, document the partition dependence and size allowances accordingly; a minimum fill policy can limit fragmentation. No proposed accounting patch was implemented or validated in this review.

**PoC:** `test/poc/ShortfallAllowanceChunking.t.sol`, complete source and exact independent command/output in the [proof appendix](#acc-proof).

<a id="fuzz-1"></a>
**FUZZ-1 — Direct whitelist revocation does not invalidate an unused signed approval**

**Severity: Low, with Informational plausible.** The independent assessment uses Medium impact for failure of a peripheral access-control decision, and Low likelihood for the required outstanding signature and revocation sequence. No fund loss is shown: the resulting loan is collateralized, and ordinary offer/cap checks still apply. Treating impact as Low would instead give Informational. Evidence: `b03-fuzz.candidates[0]`, `b04-fuzz.checks[0]`.

**Affected code:** [WhitelistEnterSubGate.sol:52–56](https://github.com/morpho-org/vault-v2/blob/bbeda7b27ae80abcf070e0158cb8a31e87bb2286/src/adapters/midnight/gates/WhitelistEnterSubGate.sol#L52-L56) changes status without invalidating signatures; [lines 59–87](https://github.com/morpho-org/vault-v2/blob/bbeda7b27ae80abcf070e0158cb8a31e87bb2286/src/adapters/midnight/gates/WhitelistEnterSubGate.sol#L59-L87) permit anyone to submit a valid signed change. `IKRCompatibleEnterGate.sol:56,60` delegates ordinary credit/debt decisions to the subgate. Related documentation: adapter README lines 174–175.

Signed changes use `nonces[creditSide][whitelister][account]`. The direct setter changes only `isWhitelisted`. An unused signature with the current nonce therefore remains applicable after a direct denial, provided its deadline has not passed and the signer still holds the relevant whitelister role. The equal-nonce branch consumes the nonce and writes the signed status without considering intervening direct changes.

The delivered PoC demonstrates:

1. An onboarding whitelister issues a debt-side approval for the taker at nonce 0, valid for 30 days.
2. Another authorized whitelister directly sets that taker's status to false. Debt admission is false, the signing whitelister's nonce remains 0, and the attempted gated trade fails.
3. The unprivileged taker submits the unused approval itself. Debt admission becomes true.
4. The taker borrows against collateral through the adapter's buy offer. Logged debt, vault assets lent and adapter net credit are each exactly `1000000000000000000` base units.

This is **not replay of an already-consumed approval after revocation**. In that case, the stale-nonce branch checks current status and rejects a different status with `WhitelistedStatusChanged`. Nor is it a proof of uncapped borrowing: the available offer, collateral and caps bound the transaction.

**Independent challenge:** the checker reproduced both original tests byte-for-byte after building production artifacts. Six additional tests confirmed rejection of consumed, expired and future-nonce signatures and of a signer whose role had been removed. The behavior also reproduced on the credit side, with the original signer performing the direct denial, and with an unrelated submitter. Two whitelisters' unused approvals undid two successive denials. Those six tests' output is reported by the checker, but their source was not handed over; they are supplementary to the delivered end-to-end PoC.

Each signed nonce can restore status only once after a denial; consumed signatures cannot repeatedly reverse later denials. The check that a future nonce fails *before* it becomes current does not establish a lifetime bound of one re-admission per whitelister. The report makes no such broader claim. Multiple outstanding authorizations must be considered when cancelling access.

Existing mitigations are a false-status counter-signature at the same nonce, removal of the signing whitelister while it remains removed, and short deadlines. Signer removal invalidates that signer's outstanding approvals globally while the role is absent, which is broader than cancelling one account. The delivered second test proves counter-signature cancellation. Its source comment calling it the “only cancellation path” describes that tested nonce-consuming path; signer removal is also available.

**Exclusion check:** the independent verifier reports that neither October draft scoped this gate. TrustSec **TRST-R-5**, PDF page 18 (printed page 17), describes the same pattern in the two ratifiers' direct root setters. The difference here is a new gate contract and permissionless submission by the revoked account; ratifier relaying has additional authorization. TrustSec CR-1 also documents gate-controller trust. The README already describes signature validity based on expiry/current signer status, but does not explain that direct denial leaves pending approvals intact. The technical effect survives; whether this is a distinct eligible finding, a known-pattern duplicate or documented operational behavior remains **UNVERIFIED**. The broader flagged audit register cannot settle that decision.

**Suggested fix — UNVERIFIED:** bind signed approvals to a per-`(side, account)` revocation epoch and advance that epoch on direct changes, or add explicit cancellation whose authority and coverage across whitelisters are clear. Incrementing only the direct caller's existing per-whitelister nonce would not cancel an approval issued by another whitelister, including the delivered PoC's case. Add regression cases for both sides, same/different revokers, multiple signers and already-used signatures. At minimum, document the counter-signature/removal procedure. No fix was implemented or tested.

**PoC:** `test/poc/WhitelistSigSurvivesRevocation.t.sol`, complete source and exact independent command/output in the [proof appendix](#whitelist-proof). A fresh checkout needs the production artifact prebuild; omitting it caused a setup failure before either test ran.

<a id="observations"></a>
**Ranked Low/Informational observations**

ACC-1 and FUZZ-1 are the two proposed Low findings above. The following list ranks additional observations by operational usefulness. They are **Informational**, except historical Low items explicitly labeled known/out of scope. None is counted as another surviving vulnerability. For entries without an explicit independent recheck, execution was by the author only and **independent verification is UNVERIFIED**. Fix suggestions throughout this list are unimplemented and **UNVERIFIED**.

**1. N1 — Force-sale price-floor decreases are immediate despite the NatSpec.** Independent recheck: `b20-notes`, from `b19-list`. Adapter `:54–55` describes relaxing guardrails as timelocked, but `:334–338` is immediate, matching README `:123`. With a 30-day selector timelock configured, the curator lowered a 0.95e18 floor to zero and the allocator sold 1,000e18 credit for zero assets; book value fell `994100700000304196258` base units. Trusted roles and prior force-sale activation are required. Correct the NatSpec; timelocking decreases would change policy. Related: Cantina 3.2.10/TRST-L-5.

**2. N3 — Zero-asset IKR cannot synchronize a fully wiped market.** Independent recheck: `b20-notes`, from `b15-midnight-assumptions`. Adapter `:469` calls Midnight `take`, which rejects `lossFactor == uint128.max` (Midnight `:332`). Both zero- and one-asset requests failed; stored credit/allocation remained `100593430826474621736007` while NAV was correctly zero. Sentinel `deallocate(market,0)` through adapter `:716–737` cleared credit, allocation and market slot. This is stale cap capacity, not further loss. Document the permissioned cleanup exception. General staleness is known as Cantina 3.2.5.

**3. N2 — Immediate tightening leaves scheduled relaxations executable.** Independent recheck: `b20-notes`, from `b19-list`. Adapter `:191–226,258–270,291–332` retains pending calldata after a tightening. After seven days a stranger executed the old curator submissions: sell-rate bound `317097919830`, allowance `1e24`, minimum buy rate zero. A sentinel's `revoke` control instead produced `DataNotTimelocked`. This follows the documented timelock design, not an authorization bypass. Emergency procedures should revoke each pending relaxation alongside tightening; schedules are keyed by full calldata.

**4. N4 — Sub-ratifier disable is a pause, not cancellation.** Independent recheck: `b20-notes`, from `b15-maker-offers`. Adapter `:348–352,503–505` leaves roots intact. An old proof failed while disabled, then filled after allocator re-enable, increasing credit from `50296715413237310868003` to `75445073119855966302004`; a sentinel could not re-enable. Root persistence is documented in price-ratifier `:21`. State this on the toggle and explicitly unratify roots when cancellation is intended. An epoch-based replacement remains untested.

**5. GATE-1 — IKR size need not match the recipient's shares: refuted as a vulnerability.** `b20-ikr-size` independently reproduced and downgraded `b15-gates-config`'s Low. Adapter `:430` requires positive shares, and Vault V2 `:790–799` allows an authorized separate penalty payer. A one-share holder received 50,000e18 credit at face value; another consenting account paid a 1,000e18 penalty. No vault loss occurred. README `:162` and adapter `:50` document shareholder admission and penalty-based sizing. Clarify this for gate operators; proportional sizing would change intended behavior.

**6. Force-sale activation does not configure its price floor.** Author test: `b06-forcesell-shortfall`; adapter `:273–277,334–338,638–639`. A ratified 5,000-unit offer at price 0.5 became fillable after activation with the default zero floor, receiving 2,500 tokens and losing about 2,344.93 in book value without consuming allowance. This requires trusted configuration and overlaps Cantina 3.2.4. Review live offers and set the floor when scheduling activation. The spread loop `:649–686` also includes distressed/force-sellable markets; excluding them would be an untested accounting-policy change.

**7. Whole-position IKR requests can become stale before inclusion.** Author test: `b05-ikr-redeem`. Adapter `:436–469` uses a reduce-only sale against updated gross credit (Midnight `:370–383,794–816`). Continuous fees or another shareholder's one-unit IKR made an exact full-position request revert; a reduced request succeeded. The dust front-run cost two asset base units and one share. No loss was shown. Periphery should calculate live credit at execution; the adapter cannot silently clamp an amount the vault later pulls exactly. This differs from the fixed dedicated-offer issue TRST-L-1.

**8. A shareholder can synchronize partial-loss caps without repairing NAV.** Author tests: `b15-vault-roles-caps`, `b05-ikr-redeem`, `b15-midnight-assumptions`; adapter `:427–477,716–738,816–859`. Zero-asset IKR reduced stored allocation from 30,000e18 to live 8,000e18 at zero penalty. NAV already used live credit, so no second loss occurred. Known general issue: Cantina 3.2.5. Document this public cleanup route and N3's full-wipe exception. Zero-asset calls on unheld sibling maturities produced events without changing credit (`b11-fix-force-ratify`).

**9. `forceRemove` permanently abandons later recoveries.** Author test: `b19-list`; adapter `:375–391,435,631,726`. After removal and repayment, Midnight showed 1e18 withdrawable credit, but adapter NAV was zero and withdrawal/sync/IKR reverted `ForceRemoved`. README `:135–138` documents the irreversible choice. Operational tooling should explain that consequence; the existing force-sale policy is more appropriate where recovery remains possible. This trusted write-off behavior is excluded as a new vulnerability.

**10. A first zero-asset buy uses a raw division panic.** Author tests: `b07-usdc-precision`, `b15-liveness`, `b15-maker-offers`, `b19-list`; adapter `:535–547`. A positive one-unit fill rounding payment to zero can panic `0x12` when carried value is zero; a two-unit fill succeeded in the liveness fixture. Only the caller's trade fails. Inline `:546`, NatSpec `:24` and Cantina §3.4 discuss the boundary. A named error would improve diagnosis. Existing-position zero-asset fills donate credit and can recognize rounding dust early.

**11. Gate governance uses the credit-side administrator.** Author test: `b15-gates-config`; `IKRCompatibleEnterGate.sol:27–36`. The debt setter could not register factories; changing the credit setter transferred authority, and setting it to zero froze future registration. Registrations are permanent by design. An admission-disabled gate was rejected by an IKR-requiring adapter even when ordinary credit was open (`MidnightAdapter.sol:564–571`). Validate the subgate, credit administrator and admission flag at deployment. Arbitrary custom-subgate safety remains UNVERIFIED.

**12. First-position self-funding can hit `ZeroAllocation`.** Author test: `b05-funding`; adapter `:579–584,606–611`, Vault V2 `:576–581`. Funding withdrawal precedes allocation, so self-funding a first family position from the bought market failed; established-family, other-market and second-adapter funding worked. Document the first-entry constraint. Separately, named funding sources supply the full `buyerAssets` even with idle cash, and empty callback data reverts (`:36–38,578–584`, `b19-list`). Integrators must use the current documented encoding.

**13. Early repayment withdrawal realizes discount and forgives associated pending fee.** Known: Cantina 3.6.5. Author tests: `b15-midnight-assumptions`, `b05-funding`; adapter `:716–738`, Midnight `:481–486`. With 1% annual fees, withdrawing 50,000e18 reduced net credit by `49990410958929440000000` and raised idle plus book value about 294.965 tokens. Self-funded buys can realize the same discount. No loss is shown; vault accrual timing/maxRate still apply. Document the step gain and distinguish book value from cached recorded assets.

**14. Dust can occupy all 250 slots if offers are ratified in those markets.** Author test: `b15-liveness`; adapter `:96–98,548–553,837–863`. Two-unit fills blocked a 251st new-market buy with `TooManyMarkets`; existing-market buys remained available. Cold fixture gas: `realAssets` 1,946,060; deposit 2,049,489; dust removal 2,296,041; refill 2,854,394. These are measurements, not a chain-wide gas guarantee. NatSpec explicitly accepts dust-filled slots. Monitor capacity or consider minimum-fill policy; do not re-report this as new DoS.

**15. Duration caps are inclusive, adapter-local and bounded by constructor validation.** Initial tests summarized in `b14-list` 6/14/18, plus `b11-fix-force-ratify` and `b19-list`. Adapter `:64–71,161–169,586–603,816–834`: a seven-day position ages out of that bucket one second later; read `durationAllocations`, not vault duration-ID allocations. Raw `PackedDurationsLib.sol:5–30` packing `[2^32+4,2]` decoded `[4,3]`, but constructor bounds block it. Accepted uint32-max thresholds exceed Midnight's maturity ceiling and never apply. Validate useful deployment thresholds. Exhaustive eight-bucket coverage remains incomplete.

**16. Ratifier edge encodings did not forge an offer.** Author tests with mocks: `b17-ratifier-forgery`; initial boundaries in `b14-list`. Rate ratifier `:105–108` panics on overflowing rate×TTM, rather than bypassing a bound. Both ratifiers' decode paths accept trailing bytes; typed offer leaves are still recomputed. `HashLib.sol:131–142` accepts root-as-leaf with an empty proof, but no attacker-controlled typed-offer preimage was found. Use bounded rates and canonical encoding in tooling. These are diagnostics; complete real-stack proof/signature combinations remain UNVERIFIED.

**17. Midnight delegation also grants ratification rights.** Known/documented: price-ratifier `:20–21`, related TRST-R-6. Author test: `b11-fix-force-ratify`/`b19-list`, price-ratifier `:38–44,74–80`. A Midnight delegate ratified on behalf of an allocator; that authority applies wherever the principal serves as allocator. Review this scope before appointing relayers. Rate-ratifier `:42–48,76–82` was source-compared, not separately executed for this particular note; that extension is UNVERIFIED by test.

**18. Factory membership does not certify the parent vault, but the attempted credit bypass failed.** Known: Cantina 3.6.3 item 7. Factory `:29–41` accepts a custom parent; gate `:40–48` trusts deployment provenance. `b17-rogue-adapter` reached admission, then the zero-credit reduce-only sale reverted `MakerCreditOrDebtIncreased`; recipient credit stayed zero. Honest IKR was the control. `b19-list` downgraded the unproven Low. Review parent/factory assumptions; no durable admission or cross-market theft was demonstrated.

**19. Nested valuation in a loss-market sale can reject the caller's composition.** Author test: `b21-bad-debt-combos`, resolving static notes in `b15-liveness`/`b17-nested-trades`. Adapter `:848–853` produced `OtherSellInProgress` for deposit inside a taker's `onBuy`; try/catch still allowed a 2,500e18 fill, then an unrelated taker filled the rest. Healthy-market deposit worked. No persistent third-party DoS was found. Nested caps can see higher pre-sale credit (`:591–603,817–829`), becoming stricter; allocations reconciled afterward. Document these composition limits.

**20. Tick-zero IKR relies on the pinned zero-price invariant.** Author tests: `b05-ikr-redeem`, `b11-fix-force-ratify`, `b19-list`. Adapter `:436–456`, Midnight `:346–352,717–722`, `TickLib.sol:46–53`. Zero seller assets make group consumption zero and settlement-fee rounding match exactly. Group-0 consumption at uint128-max did not block IKR; six- and 18-decimal cases left no adapter dust. Earlier fee-residue/cancellation hypotheses were refuted. Preserve this invariant when changing the dependency.

**Additional hardening — UNVERIFIED as exploitable:** gate `unadmit()` is permissionless and admission uses one transient slot (`IKRCompatibleEnterGate.sol:38–56`); adapter force-ratification bypasses offer checks while its flag is set (`:465–469,493,520–526`). No test reached an untrusted state-changing call in that window; admission is cleared before transfers and leakage probes failed. Narrower checks require compatibility tests (`b07-stateful-gated`, `b11-fix-force-ratify`, `b19-list`). High-s/stale signature replays with already-matching status are idempotent; domains bind chain/contract, omitting name/version. Indexers should deduplicate by signer/account/nonce (`b15-gates-config`, `b14-list` 19). All three factories bind caller and constructor arguments in CREATE2; shared bundlers should include the initiator in preSalt. The old vault/salt lookup is gone, and duplicate same-caller calls collide (`b11-fix-force-ratify`, `b14-list` 20, `b19-list` 14). The claimed 894-byte deployment margin used the wrong profile and is UNVERIFIED for this commit.

Other known Low/Informational material is consolidated here to avoid presenting duplicates as new findings:

| Known/design item | Code and disposition | Evidence |
| --- | --- | --- |
| Shared family/collateral cap IDs | Adapter `:787–809`; other adapters can share namespaces. **Historical Low, TRST-L-2; out of scope.** Dedicated cross-adapter aggregate exploit verification remains UNVERIFIED. | `b14-list` 1; single-adapter cap accounting tested in `b15-vault-roles-caps`. |
| Face-value allocations versus book-value relative caps | Adapter `:60–61,591–611`, Vault V2 `:539–557`. **Historical Low, TRST-L-3; out of scope.** Configure caps in the documented units. | `b14-list` 2; static observation, independent verification UNVERIFIED. |
| Ratifier direct setters leave root nonces unchanged | Price `:33–51,70–91`; Rate `:37–55,72–93`. **TRST-R-5, unchanged; out of scope.** Separate from the gate-specific FUZZ-1 eligibility question. | `b11-fix-force-ratify`, `b14-list` 4. |
| Rate-floor rounding realizes interest early | Adapter `:19–24,543–547,673–686`. **Cantina 3.2.8/3.6.6, TRST-R-14 and NatSpec.** A tested nonempty buy gained `540032400388` wei early, below its bound; zero-unit existing-position buys did not ratchet value. | `b03-accounting`, `b07-usdc-precision`, `b19-list` 7, `b21-bad-debt-combos`. |
| Matured credit is valued at par; below-par ordinary sales can fail | Adapter `:141–144,641–642,859`. Zero TTM leaves no unearned interest; a nonzero settlement fee can make a taker sale at quoted par fail. Fee-free par sales can pass. Stored nonzero rates after maturity have no valuation effect. | `b14-list` 15, `b19-list` 6, `b06-forcesell-shortfall`. |
| Cached transaction-level valuation around loss | Vault V2 `:28–33,626–627`; adapter `:25–26`. Same-transaction cached-price redemption equaled redemption immediately before loss; later-transaction redemption reflected loss. **Documented design, not a new loss-timing finding.** | `b21-bad-debt-combos`. |
| Adapter role removal pauses some live offers without cancelling roots | Adapter `:29–30,606–611,693–698`. Sentinel-only role allowed sells but not buys; IKR remained available without either role. Zeroed caps blocked new buys. **Documented.** | `b15-vault-roles-caps`, `b15-maker-offers`. |
| Direct token donations are outside `realAssets` | Adapter `:393–400,837–863`. Donated balance remained exactly on the adapter until skim; NAV did not move. **Documented.** | `b21-stateful-extended`, author-tested. |
| Shortfall exceeds total remaining interest | Adapter `:646–667`: allowance alone is insufficient; `ShortfallTooHigh` protects accounting. **Documented protective behavior.** The diagnostic log was not delivered, so that exact diagnostic reproduction is UNVERIFIED. | `b21-stateful-extended.lowInfo[1]`. |
| Fixed-price rate-ratified sells can age out | Rate ratifier `:107–108`: the acceptable sell-price floor rises as maturity approaches. Protective reverts do not establish stale-input exploitation. | `b21-stateful-extended`; seven focused fee/boundary tests in `b21-rate-ratifier-fees`, whose external sources were flagged. |
| Expensive base-unit and unusual tokens | Adapter `:19–24` and documented token assumptions. WBTC/cbBTC/two-decimal examples were not tested in the final rate lead; **UNVERIFIED and outside supported assumptions**, not new findings. | `b21-rate-ratifier-fees.lowInfo[0]`; initial register via `root-1-01`. |

The six-decimal precision report's prose contains a unit-conversion error: 994 base units across 1,000 fills is 0.000994 of a six-decimal token in total, about 0.000000994 token per fill, not 1e-9 token per fill. The integer measurements, documented rounding direction and lack of demonstrated taker profit are the evidence retained here.

<a id="coverage"></a>
**Coverage, refutations and remaining gaps**

The goal used 46 of 50 items; all batches settled. Cancelled verification items are not refutations. Later workers replaced blocked leads except the final duration campaign. Both retained findings have independent verification results.

| Angle | Coverage and evidence | Remaining limits |
| --- | --- | --- |
| Accounting | Initial accounting; ACC-1 independent rerun; `b05-funding` tested idle, same-market, other-market and second-adapter funding; `b06-forcesell-shortfall` used five markets and 256 fuzzed sales; `b07-usdc-precision` measured six-decimal buys. | Continuous-fee shortfall and general funding/cap combinations incomplete. Counts include inherited tests; mirrored formula tests are weaker than end-to-end checks. |
| Maturity/durations | Initial maturity review reported nine directed tests and packing fuzz (`root-1-01`, `b14-list`); constructor limits, threshold seconds, maturity valuation and removal; later cases in `b11-fix-force-ratify`, `b19-list`. | `b21-duration-buckets` fetched nothing and ran nothing. Exhaustive eight-bucket limits, caps lowered during aging and maturity ±1 across every operation remain incomplete, especially at six decimals. |
| Ratifiers | Component fuzz, existing suites, maker lifecycle with price ratifier; nine mock-based forgery unit tests (`b17-ratifier-forgery`); seven real-artifact fee/boundary tests (`b21-rate-ratifier-fees`). | No complete real-stack deep-Merkle/signed-ratification campaign. Fee-lead citations flagged. Its inherited fixture failed on `clz` under solc 0.8.28; standalone production-artifact deployment then passed. |
| Gates | FUZZ-1 independent rerun; role/configuration and cross-side/account/chain checks; rogue-parent attempt; GATE-1 independent recheck; two gated six-decimal invariant campaigns (`b07-stateful-gated`). | Custom/malicious subgates, nested vaults and vault share gates with IKR incomplete. Exploitable permissionless admission reset remains UNVERIFIED. |
| Roles/caps/IDs | `b15-vault-roles-caps` replaced blocked leads: exact cap boundaries, allocation reconciliation, loss sync, role changes, force removal and outsider sequences at 2,048 fuzz runs per suite. | No complete two-adapter finite-relative-cap/nested-vault model. Its fee-free fixtures do not cover all pending-fee interactions. Normal second-adapter funding was tested elsewhere. |
| Callbacks | Initial real-stack probes; isolated-transaction nested deposits/trades/IKR (`b17-nested-trades`); lossy-sale callback rejection (`b21-bad-debt-combos`). Healthy paths preserved shares and allocations. | No arbitrary callback-sequence campaign, hostile reentry into the force flag window or two adapters mutually trading in nested flows. |
| Loss/bad debt | Initial live-loss/sync checks; fee/full-wipe tests (`b15-midnight-assumptions`); N3 independent recheck; 18 tests in `b21-bad-debt-combos`, including spread before/after partial-loss sync, IKR and cached loss timing. | Total loss with nonzero fees, repeated losses, post-maturity/close-factor liquidation variants, and a different market liquidated inside a sale callback remain incomplete. |
| Factories | All three CREATE2 predictions, caller/argument binding, registries and duplicates in component tests; fake-parent admission failed to move credit. | No cross-chain campaign or reliable pinned-profile bytecode margin. Custom-parent/gate compositions not exhaustively covered. |
| Stateful/fuzz | Initial five-invariant campaigns: 143,400 handler calls. Gated follow-up: two × 25,600. Extended: 25,600 calls, 17 actions, five markets, fees, both ratifiers, finite duration cap and explicit loss classes. Initial component suite: 12 properties × 10,000 runs. | Attempts include reverts/setup, not unique successful scenarios; no general proof of safety. |

`b21-stateful-extended` checked allocation/list consistency, duration exposure against a brute-force sum, book value bounded by face credit, stored credit ≥ live, cash movement, allowance conservation and depositor/NAV changes against permitted losses. Maximum unexplained drop was zero within a model allowing a 1e9-wei tolerance. Its 25,600 calls include 5,320 reverts and 256 setup-only calls; another run had 5,178 reverts, and the seed was not pinned. Three deterministic 150-call sequences and a directed force-sale test supplemented it. EOAs, ungated markets and single-leaf roots excluded arbitrary callbacks, signed ratification, nonzero allowedTaker, vault fees, relative caps below WAD, liquidator gates and multiple adapters.

`b07-stateful-gated` covered real gates, rate-ratified offers and second-adapter funding at six decimals, but maximum caps, no continuous fees and no ordinary shortfall-spread action. Its summary and attached aggregate counters differ between passing runs; only consistent run/depth totals are used here. Thus the final notes' blanket statement that funding between adapters was never tested is superseded by `b05-funding` and this campaign. Arbitrary bilateral nested trading remains untested.

Dismissed hypotheses include IKR fee residue (exact match), group-0 cancellation blocking IKR (zero consumption), zero-unit existing-position rate ratcheting (no change), rogue-parent admission causing credit transfer (reduce-only rejection), proportional-share admission (documented IKR design), and persistent lossy-callback DoS (only the caller's composed transaction failed). Sources: `b05-ikr-redeem`, `b11-fix-force-ratify`, `b14-list.dropped`, `b17-rogue-adapter`, `b20-ikr-size`, `b21-bad-debt-combos`.

Infrastructure and harness failures were not counted as passes: round-two full disks/compiler restrictions, memory-killed full builds, missing/ambiguous artifacts and invalid precision-harness ticks. The separate `b01-build` baseline still completed 850 tests. `fix-buy`/`fix-sell` were initially static; `b19-list` later tested many specific notes. Prior-fix checks report improvements to self-offer IKR, directional controls, per-trade bounds, rounding, duration validation and CREATE2 salts, while root nonces and cap/trust semantics remain unchanged or partial. Those statuses apply to named regressions, not certification of the redesign.

**Source reliability and eligibility limits**

The two prior drafts are [Cantina, 2026-10-12](https://github.com/morpho-org/vault-v2/blob/bbeda7b27ae80abcf070e0158cb8a31e87bb2286/audits/2026-10-12-midnight-adapter-cantina-draft.pdf) and [TrustSec, 2026-10-12](https://github.com/morpho-org/vault-v2/blob/bbeda7b27ae80abcf070e0158cb8a31e87bb2286/audits/2026-10-12-midnight-adapter-trustsec-draft.pdf). The landed register reports both audited `6476e9d91245b0934377ef09edd201f6bf0e46ec`, and inventories 47 prior entries (19 Cantina, 28 TrustSec) plus 106 documentation/trust/risk statements. These are register counts, not 106 independently accepted vulnerabilities or 47 still-open defects.

The goal record flags the source checks of `known/register`, `known2/more` and `leads-f/rate-ratifier-fees`. `root-1-01` reports three problematic source checks in the first register; `root-1-02` reports thirteen in the expanded register and six in the rate/fee lead. The precise failed passages are not identified in the supplied goal metadata. Some audit text also decoded poorly. Therefore broad “no duplicate anywhere” assertions, the expanded 69-entry historical mapping, external whitepaper coverage and competition-specific quotations remain **UNVERIFIED**. This report does not repeat the prize amounts or infer eligibility from them.

The two independent finding verifiers did separately discuss the relevant October draft scopes and closest prior findings. That is stronger evidence for the specific comparison than the flagged general register, but it does not resolve all provenance flags or bind a competition judge. In this writing step, pinned source lines for both root causes and the relevant README passages were fetched and checked directly, and the general Cantina severity page was readable. The competition page could not be reopened; PDF fetching returned binary data but local text extraction was unavailable (`pdftotext` missing). The audit text was consequently not freshly re-extracted here. These limits do not invalidate the recorded execution logs, but prevent a fully verified competition-novelty claim.

<a id="proofs"></a>
**Proof appendix — complete finding test files and independent outputs**

The two Solidity blocks are complete, unchanged supplied files, including licenses. Save them at the stated paths in the pinned checkout. They use its existing fixtures/dependencies; this report does not vendor an offline Foundry distribution. No additional helper source is needed for these two original proofs.

Prepare an isolated checkout, then save the blocks before running the finding commands:

```bash
git clone https://github.com/morpho-org/vault-v2 vault-v2
cd vault-v2
git checkout bbeda7b27ae80abcf070e0158cb8a31e87bb2286
git submodule update --init --recursive
mkdir -p test/poc
```

These are reproduction instructions, not new runs in this writing task. Keep upstream settings/source unchanged. ACC-1 used Forge 1.7.1 with official exact-version solc-js wrappers for missing native compilers; FUZZ-1 used Forge 1.8.5. `--offline` assumes compilers/dependencies are present. Gas/timing may vary.

<a id="acc-proof"></a>
**File: `test/poc/ShortfallAllowanceChunking.t.sol`**

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import {console2} from "../../lib/forge-std/src/console2.sol";
import {MidnightAdapterIntegrationTest} from "../integration/MidnightAdapterIntegrationTest.sol";
import {SafeERC20Lib} from "../../src/libraries/SafeERC20Lib.sol";
import {WAD} from "../../src/libraries/ConstantsLib.sol";
import {MarketData} from "../../src/adapters/midnight/interfaces/IMidnightAdapter.sol";
import {Market, Offer} from "../../lib/midnight/src/interfaces/IMidnight.sol";
import {HashLib} from "../../lib/midnight/src/ratifiers/libraries/HashLib.sol";
import {IdLib} from "../../lib/midnight/src/libraries/IdLib.sol";
import {TickLib} from "../../lib/midnight/src/libraries/TickLib.sol";

/// @dev shortfallAllowance consumption depends on how a shortfall sale is split.
/// @dev Real Midnight + real VaultV2, setup of MidnightAdapterIntegrationTest (100k assets bought at ~0.994, 7 days).
contract ShortfallAllowanceChunkingPoC is MidnightAdapterIntegrationTest {
    Market internal mkt;

    function _buyAll() internal {
        // Same as testMakerBuy: the adapter buys `units` credit maturing in 7 days at TICK (~0.994).
        testMakerBuy();
        mkt = _market(7 days);
        // One day later the position has accrued interest, then it is partly sold at 0.99 (below amortized value).
        vm.warp(block.timestamp + 1 days);
    }

    function _tick099() internal pure returns (uint256 tick) {
        tick = TICK;
        while (TickLib.tickToPrice(tick) > 0.99e18) tick -= 4;
    }

    function _vaultValue() internal view returns (uint256) {
        return underlyingToken.balanceOf(address(vault)) + adapter.realAssets();
    }

    /// @dev An adapter maker sell offer, ratified by the allocator, is filled by an outside taker once or in 20 pieces.
    function testMakerSellFilledInPiecesConsumesMoreAllowance() public {
        _buyAll();
        uint256 sold = 10_000 * oneToken;
        uint256 tick = _tick099();
        vm.prank(curator);
        adapter.decreaseShortfallAllowance(type(uint128).max);
        _submitAndSet(address(adapter), abi.encodeCall(adapter.increaseShortfallAllowance, (51 * oneToken)));
        Offer memory offer = Offer({
            market: mkt,
            buy: false,
            maker: address(adapter),
            start: block.timestamp,
            expiry: mkt.maturity,
            tick: tick,
            group: keccak256(abi.encode("sell", mkt.maturity, sold)),
            callback: address(adapter),
            callbackData: "",
            receiverIfMakerIsSeller: address(adapter),
            ratifier: address(adapter),
            reduceOnly: true,
            maxUnits: uint128(sold),
            maxAssets: 0,
            continuousFeeCap: type(uint256).max
        });
        bytes32 root = HashLib.hashPriceRatifierV1Offer(offer, address(0));
        vm.prank(allocator);
        priceSubRatifier.setIsRootRatified(address(adapter), root, true, allocator);
        bytes memory ratifierData =
            abi.encode(address(priceSubRatifier), abi.encode(root, uint256(0), new bytes32[](0), address(0)));
        deal(address(underlyingToken), lender, sold);
        vm.prank(lender);
        SafeERC20Lib.safeApprove(address(underlyingToken), address(midnight), type(uint256).max);

        uint256 allowance0 = adapter.shortfallAllowance();
        uint256 value0 = _vaultValue();
        console2.log("allowance before", allowance0);
        console2.log("sale price (WAD)", TickLib.tickToPrice(tick));

        uint256 snap = vm.snapshotState();
        vm.prank(lender);
        midnight.take(offer, ratifierData, sold, lender, address(0), address(0), "");
        uint256 usedOne = allowance0 - adapter.shortfallAllowance();
        uint256 valueOne = _vaultValue();
        console2.log("1 fill:   allowance consumed", usedOne);
        console2.log("1 fill:   idle+realAssets", valueOne);

        vm.revertToState(snap);
        uint256 n = 20;
        uint256 filled;
        for (uint256 i; i < n; i++) {
            vm.prank(lender);
            try midnight.take(offer, ratifierData, sold / n, lender, address(0), address(0), "") {
                filled += sold / n;
            } catch (bytes memory reason) {
                console2.log("fill reverted at piece", i);
                console2.logBytes(reason);
                break;
            }
        }
        uint256 usedMany = allowance0 - adapter.shortfallAllowance();
        console2.log("20 fills: units filled", filled);
        console2.log("20 fills: allowance consumed", usedMany);
        console2.log("20 fills: idle+realAssets", _vaultValue());
        console2.log("idle+realAssets before", value0);

        // The single fill fits the 51-token allowance; the same sale in 20 pieces exhausts it before completing.
        assertEq(usedOne < 51 * oneToken, true, "single fill fits allowance");
        assertLt(filled, sold, "pieces cannot complete the same sale");
    }

    /// @dev Same sale through allocator takes: once vs 20 takes. Book value is preserved in both, allowance use differs.
    function testAllocatorSaleInPiecesConsumesMoreAllowance() public {
        _buyAll();
        uint256 sold = 10_000 * oneToken;
        uint256 tick = _tick099();
        Offer memory offer = Offer({
            market: mkt,
            buy: true,
            maker: lender,
            start: block.timestamp,
            expiry: mkt.maturity,
            tick: tick,
            group: keccak256(abi.encode("lender", mkt.maturity, sold)),
            callback: address(0),
            callbackData: "",
            receiverIfMakerIsSeller: address(0),
            ratifier: address(setterRatifier),
            reduceOnly: false,
            maxUnits: uint128(sold),
            maxAssets: 0,
            continuousFeeCap: type(uint256).max
        });
        deal(address(underlyingToken), lender, sold);
        bytes32 root = HashLib.hashOffer(offer);
        bytes memory data = abi.encode(root, uint256(0), new bytes32[](0));
        vm.startPrank(lender);
        SafeERC20Lib.safeApprove(address(underlyingToken), address(midnight), type(uint256).max);
        midnight.setIsAuthorized(address(setterRatifier), true, lender);
        setterRatifier.setIsRootRatified(lender, root, true);
        vm.stopPrank();

        uint256 allowance0 = adapter.shortfallAllowance();
        uint256 value0 = _vaultValue();
        console2.log("idle+realAssets before", value0);

        uint256 snap = vm.snapshotState();
        vm.prank(allocator);
        adapter.take(offer, data, sold, "");
        uint256 usedOne = allowance0 - adapter.shortfallAllowance();
        uint256 valueOne = _vaultValue();
        MarketData memory a = adapter.marketData(IdLib.toId(mkt));
        console2.log("1 take:   allowance consumed", usedOne);
        console2.log("1 take:   idle+realAssets", valueOne);
        console2.log("1 take:   netRate", a.netRate);

        vm.revertToState(snap);
        for (uint256 i; i < 20; i++) {
            vm.prank(allocator);
            adapter.take(offer, data, sold / 20, "");
        }
        uint256 usedMany = allowance0 - adapter.shortfallAllowance();
        uint256 valueMany = _vaultValue();
        MarketData memory b = adapter.marketData(IdLib.toId(mkt));
        console2.log("20 takes: allowance consumed", usedMany);
        console2.log("20 takes: idle+realAssets", valueMany);
        console2.log("20 takes: netRate", b.netRate);
        console2.log("extra allowance consumed", usedMany - usedOne);

        // Same economic outcome (rates and book value within 1e-6 of a token)...
        assertApproxEqAbs(valueMany, valueOne, oneToken / 1e6, "same book value");
        assertApproxEqAbs(uint256(b.netRate), uint256(a.netRate), 100, "same rate");
        // ...but ~5% more allowance consumed.
        assertGt(usedMany, usedOne + usedOne / 25, "chunked sale consumes >4% more allowance");
    }
}
```

The checker reports a clean pinned clone with only the test directory untracked and no source/library edits. Its prebuild completed with exit code zero. Exact commands, from the clone root:

```bash
forge build --offline lib/midnight/src/Midnight.sol lib/midnight/src/ratifiers/SetterRatifier.sol src/VaultV2.sol src/VaultV2Factory.sol src/adapters/midnight/MidnightAdapterFactory.sol src/adapters/midnight/ratifiers/MidnightAdapterPriceRatifierV1.sol test/imports/MidnightImport.sol
forge test --offline --match-path test/poc/ShortfallAllowanceChunking.t.sol -vv
```

Exact supplied independent output (`b04-accounting.checks[0].output`), including compilation and elapsed-time lines:

```text
Compiling 30 files with Solc 0.8.28
Compiling 9 files with Solc 0.8.37
Compiling 3 files with Solc 0.8.37
Compiling 19 files with Solc 0.8.28
Compiling 4 files with Solc 0.8.37
Compiling 25 files with Solc 0.8.37
Compiling 4 files with Solc 0.8.37
Compiling 74 files with Solc 0.8.28
Solc 0.8.28 finished in 298.80ms
Solc 0.8.37 finished in 647.63ms
Solc 0.8.37 finished in 816.45ms
Solc 0.8.37 finished in 1.69s
Solc 0.8.37 finished in 2.85s
Solc 0.8.28 finished in 3.51s
Solc 0.8.37 finished in 3.72s
Solc 0.8.28 finished in 41.13s
Compiler run successful!
Ran 10 tests for test/poc/ShortfallAllowanceChunking.t.sol:ShortfallAllowanceChunkingPoC
[PASS] testAllocatorSaleInPiecesConsumesMoreAllowance() (gas: 3933897)
Logs:
  idle+realAssets before 100084346798178607255874
  1 take:   allowance consumed 50069921111211219809
  1 take:   idle+realAssets 100084346798189681319247
  1 take:   netRate 8735599645
  20 takes: allowance consumed 52599017994081945687
  20 takes: idle+realAssets 100084346798608551701820
  20 takes: netRate 8735599636
  extra allowance consumed 2529096882870725878
[PASS] testForceDeallocate() (gas: 1184052)
[PASS] testForceSell() (gas: 1182009)
[PASS] testMakerBuy() (gas: 881516)
[PASS] testMakerSell() (gas: 1335294)
[PASS] testMakerSellFilledInPiecesConsumesMoreAllowance() (gas: 3898644)
Logs:
  allowance before 51000000000000000000
  sale price (WAD) 989932200000000000
  1 fill:   allowance consumed 50069921111211219809
  1 fill:   idle+realAssets 100084346798189681319247
  fill reverted at piece 19
  0x8ea54d94
  20 fills: units filled 9500000000000000000000
  20 fills: allowance consumed 49834436012548795750
  20 fills: idle+realAssets 100084346798597656807086
  idle+realAssets before 100084346798178607255874
[PASS] testRepayWithdrawRedeem() (gas: 1166267)
[PASS] testTakerBuy() (gas: 899462)
[PASS] testTakerSell() (gas: 1362766)
[PASS] testWrapperGateForceDeallocateAfterRevocation() (gas: 14735455)
Suite result: ok. 10 passed; 0 failed; 0 skipped; finished in 20.11ms (42.93ms CPU time)
Ran 1 test suite in 21.44ms (20.11ms CPU time): 10 tests passed, 0 failed, 0 skipped (10 total tests)
real	0m46.914s
user	1m23.542s
sys	0m4.530s
```

The maker test catches a revert without asserting its selector, so the observed `0x8ea54d94` log is material evidence of the stated cause; the source alone would only assert incomplete filling. The separate completed-sales test asserts the budget divergence and approximate equal NAV/rate. No production repair was needed (`repairDiff` empty).

<a id="whitelist-proof"></a>
**File: `test/poc/WhitelistSigSurvivesRevocation.t.sol`**

```solidity
// SPDX-License-Identifier: GPL-2.0-or-later
pragma solidity ^0.8.0;

import "../MidnightAdapterTest.sol";
import {
    SET_IS_WHITELISTED_TYPEHASH,
    EIP712_DOMAIN_TYPEHASH as WL_DOMAIN_TYPEHASH
} from "../../src/adapters/midnight/gates/interfaces/IWhitelistEnterSubGate.sol";

/// @notice A whitelister's outstanding setIsWhitelistedWithSig signature is not invalidated by a direct
/// setIsWhitelisted(false) revocation. Anyone (here: the revoked borrower) can submit it afterwards and
/// re-whitelist themselves, then borrow from the vault through the adapter in the gated market.
contract WhitelistSigSurvivesRevocationTest is MidnightAdapterTest {
    function testPoCWhitelistSigSurvivesDirectRevocation() public {
        (IKRCompatibleEnterGateFactory gateFactory, IWhitelistEnterSubGate gate) = setUpEnterGateRealVault(true);
        address wrapper = createIKRCompatibleEnterGate(gateFactory, gate);

        // Onboarding whitelister with a key (debt side). roleSetter is address(this).
        (address wl, uint256 wlKey) = makeAddrAndKey("onboardingWhitelister");
        gate.setIsWhitelister(false, wl, true);

        // 1. Onboarding whitelister signs a debt-side whitelisting of `taker`, valid 30 days, and hands it out.
        uint256 deadline = block.timestamp + 30 days;
        bytes32 structHash = keccak256(abi.encode(SET_IS_WHITELISTED_TYPEHASH, false, taker, true, uint256(0), deadline));
        bytes32 domain = keccak256(abi.encode(WL_DOMAIN_TYPEHASH, block.chainid, address(gate)));
        (uint8 v, bytes32 r, bytes32 s) = vm.sign(wlKey, keccak256(bytes.concat("\x19\x01", domain, structHash)));

        // 2. Before it is used, compliance (another whitelister, address(this)) revokes `taker` with the direct setter.
        gate.setIsWhitelisted(false, taker, false);
        assertFalse(gate.debtIncreaseAllowed(taker), "revoked");
        assertEq(gate.nonces(false, wl, taker), 0, "direct setter did not touch the signature nonce");

        // The revoked borrower cannot borrow from the adapter's offer.
        Offer memory offer = makeEnterGateBuyOffer(wrapper, true);
        vm.expectRevert();
        this.takeWithAccrual(offer, "", taker, address(0));

        // 3. The borrower submits the still-valid signature themselves (anyone may submit) and is whitelisted again.
        vm.prank(taker);
        gate.setIsWhitelistedWithSig(false, taker, true, 0, deadline, v, r, s);
        assertTrue(gate.debtIncreaseAllowed(taker), "revocation undone");

        // 4. The borrower now borrows vault funds through the adapter in the gated market.
        uint256 vaultIdleBefore = loanToken.balanceOf(address(realVault));
        take(offer);
        bytes32 marketId = _marketId(offer.market);
        uint256 debt = midnight.debt(marketId, taker);
        uint256 lent = vaultIdleBefore - loanToken.balanceOf(address(realVault));
        emit log_named_uint("revoked borrower debt (units)", debt);
        emit log_named_uint("vault assets lent to revoked borrower", lent);
        emit log_named_uint("adapter net credit", adapter.marketData(marketId).netCredit);
        assertEq(debt, 1e18);
        assertEq(lent, 1e18);
    }

    /// The only cancellation path: the signer burns the nonce by signing and submitting a counter-signature.
    function testCancellationRequiresCounterSignature() public {
        (, IWhitelistEnterSubGate gate) = setUpEnterGateRealVault(true);
        (address wl, uint256 wlKey) = makeAddrAndKey("onboardingWhitelister");
        gate.setIsWhitelister(false, wl, true);
        uint256 deadline = block.timestamp + 30 days;
        bytes32 domain = keccak256(abi.encode(WL_DOMAIN_TYPEHASH, block.chainid, address(gate)));
        (uint8 v, bytes32 r, bytes32 s) = vm.sign(
            wlKey,
            keccak256(
                bytes.concat(
                    "\x19\x01",
                    domain,
                    keccak256(abi.encode(SET_IS_WHITELISTED_TYPEHASH, false, taker, true, uint256(0), deadline))
                )
            )
        );
        (uint8 v2, bytes32 r2, bytes32 s2) = vm.sign(
            wlKey,
            keccak256(
                bytes.concat(
                    "\x19\x01",
                    domain,
                    keccak256(abi.encode(SET_IS_WHITELISTED_TYPEHASH, false, taker, false, uint256(0), deadline))
                )
            )
        );
        gate.setIsWhitelistedWithSig(false, taker, false, 0, deadline, v2, r2, s2);
        vm.expectRevert(IWhitelistEnterSubGate.WhitelistedStatusChanged.selector);
        gate.setIsWhitelistedWithSig(false, taker, true, 0, deadline, v, r, s);
        assertFalse(gate.debtIncreaseAllowed(taker));
    }
}
```

After saving the source in a clean pinned checkout, the independent checker ran:

```bash
forge build src lib/midnight/src/Midnight.sol
forge test --match-path test/poc/WhitelistSigSurvivesRevocation.t.sol --match-test "PoC|Cancellation" -vv
```

Exact supplied independent output (`b04-fuzz.checks[0].output`), retaining the initial failed attempt and successful repair:

```text
[first attempt, fresh clone, PoC file only, no prior build]
Compiler run successful!

Ran 1 test for test/poc/WhitelistSigSurvivesRevocation.t.sol:WhitelistSigSurvivesRevocationTest
[FAIL: vm.getCode: no matching artifact found] setUp() (gas: 0)
Suite result: FAILED. 0 passed; 1 failed; 0 skipped; finished in 20.21ms (0.00ns CPU time)

[after `forge build src lib/midnight/src/Midnight.sol`, same test command, Foundry 1.8.5]
Compiling 1 files with Solc 0.8.37
Compiling 32 files with Solc 0.8.37
Solc 0.8.37 finished in 51.69ms
Compiling 51 files with Solc 0.8.37
Solc 0.8.37 finished in 4.92s
Compiling 76 files with Solc 0.8.28
Solc 0.8.28 finished in 65.53s
Compiling 173 files with Solc 0.8.28
Solc 0.8.28 finished in 91.99s
Solc 0.8.37 finished in 351.69s
Compiler run successful!

Ran 2 tests for test/poc/WhitelistSigSurvivesRevocation.t.sol:WhitelistSigSurvivesRevocationTest
[PASS] testCancellationRequiresCounterSignature() (gas: 26734823)
[PASS] testPoCWhitelistSigSurvivesDirectRevocation() (gas: 29008084)
Logs:
  revoked borrower debt (units): 1000000000000000000
  vault assets lent to revoked borrower: 1000000000000000000
  adapter net credit: 1000000000000000000

Suite result: ok. 2 passed; 0 failed; 0 skipped; finished in 73.09ms (63.50ms CPU time)

Ran 1 test suite in 77.48ms (73.09ms CPU time): 2 tests passed, 0 failed, 0 skipped (2 total tests)
```

The repair was artifact preparation only; `repairDiff` is empty and the source was unchanged. `--match-path` alone did not build every contract deployed by artifact name in the inherited fixture. Both successful tests use real production gate/Vault V2/Midnight artifacts; test token/oracle fixtures provide collateral and balances. The good-faith direct denial and issuance of a test signature model legitimate whitelister actions, not powers given to the attacker.

<a id="provenance"></a>
**Evidence provenance and orchestration record**

Input IDs are provenance labels, not links to temporary files expected to survive delivery. Complete evidence for the two retained findings is embedded above. Root merges summarize earlier inputs and are not independent executions; later results supersede their stale statuses.

| Inputs | Original batch/items |
| --- | --- |
| `root-1-01`, `root-1-02` | roots/1/01, roots/1/02 |
| `b01-build` | build/build |
| `b03-accounting`, `b03-fuzz` | review/accounting, review/fuzz |
| `b04-accounting`, `b04-fuzz` | verify/accounting, verify/fuzz |
| `b05-funding`, `b05-ikr-redeem` | leads-a/funding, leads-a/ikr-redeem |
| `b06-forcesell-shortfall` | leads-b/forcesell-shortfall |
| `b07-stateful-gated`, `b07-usdc-precision` | leads-c/stateful-gated, leads-c/usdc-precision |
| `b11-fix-force-ratify` | fixes/fix-force-ratify |
| `b13-more`, `b14-list`, `b19-list` | known2/more, lowinfo/list, notes-fixes/list |
| `b15-vault-roles-caps`, `b15-gates-config`, `b15-liveness`, `b15-midnight-assumptions`, `b15-maker-offers` | corresponding items in leads-d |
| `b17-ratifier-forgery`, `b17-rogue-adapter`, `b17-nested-trades` | corresponding items in leads-e |
| `b20-ikr-size`, `b20-notes` | recheck/ikr-size, recheck/notes |
| `b21-bad-debt-combos`, `b21-stateful-extended`, `b21-duration-buckets`, `b21-rate-ratifier-fees` | corresponding items in leads-f |

Batch notes specify one baseline/register, review angle, lead, prior-fix group or candidate/refutation set per item. Required results were commands/counts/failures for builds; source, command, output, severity, exclusions and coverage for candidates; verdicts/refutation attempts for verification; and ranked notes with references/status for consolidation. Handed brief strings are truncated, so complete historical brief compliance cannot be certified here.

The terminal decision is preserved as one JSON object in the reference shape. It is embedded because this write-up assignment permits only `report.md`, not a separate decisions output; no new batch is proposed.

```json
{
  "notes": "Finish from the landed results. ACC-1 and FUZZ-1 survived independent technical checks as Low; Informational remains plausible and competition eligibility unverified. No Medium or High survived. GATE-1 is documented behavior; N1-N4 are Informational. Preserve source flags, the unrun duration lead, coverage limits and original finding proofs. No code trunk exists. Deliver only to the requester.",
  "spawn": [],
  "read": [],
  "finish": true
}
```

Report preparation checked the supplied input digests, parsed the JSON results, reconciled contradictory summaries against source/logs, and checked the embedded finding sources and outputs for byte equality with their supplied fields. This checks faithful delivery, not contract behavior. No additional Foundry run is claimed for this writing step. The report is the sole output; source, configuration and dependency files are unchanged.
