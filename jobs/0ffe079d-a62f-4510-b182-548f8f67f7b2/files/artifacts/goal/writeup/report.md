# IMD Contract-Build & Token-Launch Security Checklist

Drawn from 30 public DeFi exploits of 2025–2026. For each incident: what failed, the general pattern, and the check that would have caught it before deployment.

---

## Incident Table

| # | Incident | Date | Chain | Loss (USD) | Pattern | SC Bug? |
|---|----------|------|-------|------------|---------|---------|
| 1 | zkLend | 2025-02-11 | Starknet | ~$9.5M | Rounding/precision loss in accumulator lending math | Yes |
| 2 | Four.meme | 2025-02-11, 03-18 | BNB Chain | ~$183K + ~$130K | Unvalidated external pool state / pool-init front-run | Yes |
| 3 | Bybit | 2025-02-21 | Ethereum | ~$1.43B | Key/signer compromise via frontend supply-chain attack | No |
| 4 | Infini | 2025-02-24 | Ethereum | ~$49.5M | Key/signer compromise + excessive privileged access | No |
| 5 | 1inch Fusion v1 | 2025-03-05 | Ethereum | ~$5M | Integer underflow in Yul assembly | Yes |
| 6 | Abracadabra | 2025-03-25 | Arbitrum | ~$13M | Liquidation state-accounting desynchronization | Yes |
| 7 | SIR.trading | 2025-03-30 | Ethereum | ~$355K | Transient-storage aliasing / callback validation failure | Yes |
| 8 | KiloEx | 2025-04-14 | Multi-chain | ~$7.49M | Missing access control in meta-tx forwarder | Yes |
| 9 | ZKsync Airdrop | 2025-04-15 | ZKsync Era | ~$5M | Key/signer compromise + unvalidated privileged function | No |
| 10 | Loopscale | 2025-04-26 | Solana | ~$5.8M | Missing program-identity validation on price source | Yes |
| 11 | MobiusDAO | 2025-05-11 | BNB Chain | ~$2.15M | Decimal-scaling error (double multiplication) | Yes |
| 12 | Cetus Protocol | 2025-05-22 | Sui | ~$223M | Integer overflow / faulty bounds check in shared math lib | Yes |
| 13 | Cork Protocol | 2025-05-28 | Ethereum | ~$11.9M | Hook callback access control + unbounded time-decay pricing | Yes |
| 14 | Meta Pool | 2025-06-17 | Ethereum | ~$130K | Mis-adapted ERC-4626 vault / inherited free-mint path | Yes |
| 15 | Silo Finance | 2025-06-25 | Ethereum, Sonic | ~$522K | Unvalidated calldata injection / arbitrary external call | Yes |
| 16 | Resupply | 2025-06-26 | Ethereum | ~$9.5M–$10M | ERC-4626 vault inflation + rounding-to-zero in LTV check | Yes |
| 17 | GMX v1 | 2025-07-09 | Arbitrum | ~$42M | Cross-contract reentrancy via gas-refund callback | Yes |
| 18 | Kinto ($K) | 2025-07-10 | Arbitrum | ~$1.55M | Uninitialized upgradeable proxy (CPIMP attack) | Yes |
| 19 | Arcadia Finance | 2025-07-14/15 | Base | $3.6M | Arbitrary low-level call to unvalidated router | Yes |
| 20 | SuperRare staking | 2025-07-28 | Ethereum | ~$730K | Inverted access control (`!=` instead of `==`) | Yes |
| 21 | Bunni v2 | 2025-09-01/02 | Ethereum, Unichain | ~$8.4M | Rounding direction across multi-step state updates | Yes |
| 22 | Typus Finance | 2025-10-15 | Sui | ~$3.44M | Discarded authorization result (missing `assert!`) | Yes |
| 23 | Balancer v2 | 2025-11-03 | Ethereum + L2s | $94.8M–$128M | Rounding asymmetry in token scaling (batch atomicity) | Yes |
| 24 | Yearn yETH | 2025-11-30 | Ethereum | ~$9M | Unchecked fixed-point solver + reachable bootstrap branch | Yes |
| 25 | Truebit | 2026-01-08 | Ethereum | $26.4M–$26.6M | Integer overflow (Solidity <0.8.0, no SafeMath) | Yes |
| 26 | CrossCurve | 2026-01/02 | Multi-chain | $1.4M–$3M | Bridge fast-path `expressExecute()` missing gateway validation | Yes |
| 27 | Moonwell cbETH | 2026-02-15 | Base | $1.78M | Oracle misconfiguration (ratio feed used as dollar price) | No |
| 28 | Resolv (USR) | 2026-03-22 | Ethereum | ~$25M | Privileged-key compromise + no on-chain mint cap | No |
| 29 | Drift Protocol | 2026-04-01 | Solana | ~$285.26M | Social-engineered multisig signers + no timelock | No |
| 30 | KelpDAO rsETH | 2026-04-18 | Ethereum, Unichain | ~$292M | 1-of-1 DVN + poisoned RPC nodes forging bridge attestation | No |

**Loss totals:** ~$2.22B across all 30 incidents. 21 were smart-contract bugs; 9 were operational/key-compromise failures.

---

## Part A: Smart-Contract Checklist (grouped by pattern)

### A1. Token Contracts — Minting, Decimals, and Supply Integrity

| # | Check | How | Would Have Caught |
|---|-------|-----|-------------------|
| A1.1 | Verify mint amount matches deposited value within 1% tolerance for real input values | Unit test with known deposit amounts | MobiusDAO [rek.news/mobiusdao-rekt] |
| A1.2 | Invariant: `mintedAmount <= (depositedAmount * price) / 1e18 * (1 + maxSlippage)` for any deposit size | Fuzz test with random deposit amounts | MobiusDAO |
| A1.3 | Every integer division in share-to-asset conversion must round against the caller: ceil on withdrawal, floor on deposit | Review rule + unit test with extreme values | zkLend [rekt.news/zklend-rekt; halborn.com; blocksec.com] |
| A1.4 | Fuzz the withdraw path with extreme accumulator values; assert a user's withdrawable amount never exceeds deposits plus accrued interest | Invariant test (Foundry/Medusa) | zkLend |
| A1.5 | Any `a / b` where `b` derives from an external or attacker-influenceable source must carry a documented lower bound before feeding a health/solvency calculation | Review rule | Resupply [ackee.xyz; blocksec.com] |
| A1.6 | For token sale contracts: compile with Solidity ≥0.8.0 (or use SafeMath); fuzz `getPurchasePrice(amount)` to `type(uint256).max` and assert non-zero price for non-zero amount | Deploy-time check + fuzz test | Truebit [certik.com; DeFiHackLabs] |

### A2. Uniswap v4 Hooks

| # | Check | How | Would Have Caught |
|---|-------|-----|-------------------|
| A2.1 | Every hook callback (`beforeSwap`, `afterSwap`, `beforeAddLiquidity`, etc.) must revert when called directly by an arbitrary EOA — only the PoolManager may invoke it | Unit test: call each hook from a non-PoolManager address, assert revert | Cork Protocol [cork.tech/blog/post-mortem; rekt.news/cork-protocol-rekt] |
| A2.2 | Enumerate every `TSTORE`/`TLOAD` in hook contracts; reject sharing a callback-authority transient slot with a numeric return value; use distinct slots and clear authority on swap completion | Review rule + same-tx invariant test | SIR.trading [docs.sir.trading; verichains.io; slowmist.medium.com] |
| A2.3 | Same-transaction regression test: complete a legitimate mint/swap, then attempt another callback before the tx ends with varying amounts and unauthorized callers — only the original pool must succeed | Invariant test | SIR.trading |
| A2.4 | Every `mulDiv` in hook state-update arithmetic must justify its rounding direction across sequences, not only singly — a rounding "safe" once can compound across many small operations | Review rule + sequence fuzz test | Bunni v2 [blog.bunni.xyz; rekt.news/bunni-rekt; Cyfrin audit] |

### A3. Vaults (ERC-4626, Lending, Yield)

| # | Check | How | Would Have Caught |
|---|-------|-----|-------------------|
| A3.1 | Every path that increases shares or `totalUnderlying` must increase the vault's actual custodied assets by at least the credited amount; fuzz all entry points | Invariant test | Meta Pool [solidityscan.com; quillaudits.com] |
| A3.2 | When forking ERC-4626 and dropping the transfer step from `_deposit`, enumerate every inherited entry point reaching it (`deposit`, `mint`, `depositETH`, etc.) and either make it payable-with-check or disable it | Review rule | Meta Pool |
| A3.3 | Fuzz the oracle/price path across the full `uint256` range; assert `exchangeRate > 0` and that a 1-wei-collateral position is never solvent while debt > 0 | Invariant fuzz test | Resupply [blocksec.com; Resupply post-mortem; ackee.xyz] |
| A3.4 | Validate initialization before enabling a market: require the ERC-4626 vault seeded with minimum non-zero liquidity, or reject a market whose `convertToAssets(1e18)` exceeds a sane upper bound | Deployment check | Resupply |
| A3.5 | After every `liquidate()` call, a liquidated position must not pass `borrow()` and return a non-zero amount; every state-mutating function that empties a record must set an explicit `isActive` flag | Invariant test + review rule | Abracadabra [rekt.news; web3isgoinggreat.com; defillama.com] |
| A3.6 | Property-test `_calc_supply` (with `add_liquidity`/`remove_liquidity`/`update_rates`) over extreme imbalanced inputs; assert that the product term `Π` is never zero and LP minted per call is bounded by deposited value | Fuzz test with skewed dust deposits | Yearn yETH [github.com/yearn/yearn-security; blocksec.com; rekt.news/yearn-rekt3] |
| A3.7 | Replace `unsafe_*` arithmetic with checked math so a domain violation reverts; permanently disable the bootstrap/initialization branch after the first deposit | Review rule + ops check | Yearn yETH |

### A4. Upgradeable Proxies

| # | Check | How | Would Have Caught |
|---|-------|-----|-------------------|
| A4.1 | Deploy and initialize every upgradeable proxy atomically in one transaction: `new ERC1967Proxy(impl, abi.encodeCall(Logic.initialize, (admin)))` — never deploy with empty init data | Unit test + deploy script check | Kinto ($K) [dedaub.com; nethermind.io; rekt.news/just-bad-luck] |
| A4.2 | Assert the EIP-1967 implementation slot equals the legitimate implementation immediately after deployment (no window between deploy and init) | Invariant check in deploy script | Kinto ($K) |
| A4.3 | Monitor that the implementation slot never changes outside an event-logged upgrade; where delayed init is unavoidable, restrict `initialize()` to a single hard-coded deployer | Review rule + on-chain monitoring | Kinto ($K) |

### A5. Access Control

| # | Check | How | Would Have Caught |
|---|-------|-----|-------------------|
| A5.1 | Every access-control `require` must name who is *allowed* (`==`), not who is *excluded* (`!=`); statically flag `require(msg.sender != X || msg.sender != Y)` as always-true tautologies | Static analysis rule + unit test: call privileged function from a fresh address, assert revert | SuperRare [verichains.io; solidityscan.com; veridise.com] |
| A5.2 | Every security predicate returned by a pure function must be consumed by an `assert!`/`if`/`require` — flag discarded return values from authorization checks | Review rule (Move: no unused-return warning) + unit test from non-whitelisted caller | Typus Finance [medium.com/@TypusFinance; slowmist.medium.com; halborn.com] |
| A5.3 | When inheriting a meta-transaction base (e.g. `MinimalForwarderUpgradeable`), require an explicit `onlyOwner`/`AccessControl` guard on `execute()`; never let `msg.sender == forwarder` alone substitute for checking the recovered signer against an allow-list | Review rule + invariant fuzz test | KiloEx [rekt.news/kiloex-rekt; slowmist.medium.com; solidityscan.com] |
| A5.4 | Enumerate every inherited public entry point on bridge receivers (e.g. `expressExecute()`); require symmetric validation between fast and normal execution paths | Review rule (Slither entrypoint list) + unit test from non-Gateway EOA | CrossCurve [cantina.xyz; mixbytes; blocksec.com; github.com/axelarnetwork] |
| A5.5 | Assert no code path moves value out of a bridge vault unless `gateway.validateContractCall()` approved the (commandId, sourceChain, sourceAddress, payloadHash) tuple | Invariant fuzz test | CrossCurve |

### A6. External Calls and Calldata Validation

| # | Check | How | Would Have Caught |
|---|-------|-----|-------------------|
| A6.1 | Every `call()`/`delegatecall()` to a caller-supplied address must validate the target against a hardcoded or governance whitelist, or restrict calldata to known function selectors | Review rule + unit test with non-whitelisted router and arbitrary calldata | Arcadia Finance [rekt.news/arcadiafi-rekt]; Silo Finance [quillaudits.com] |
| A6.2 | Invariant: the contract's token balance must never decrease except through the intended swap/rebalance path; fuzz arbitrary `_swapArgs`/calldata payloads | Invariant fuzz test | Silo Finance; Arcadia Finance |
| A6.3 | After `createAndInitializePoolIfNecessary` in a launch/migration, verify `pool.slot0().sqrtPriceX96` equals the intended price; use non-zero `amount0Min`/`amount1Min` slippage guards | Unit test + review rule | Four.meme [verichains.io; chaincatcher.com; cointelegraph.com] |
| A6.4 | Pre-launch tokens must be untransferable to the future pair/LP address; fuzz transfer attempts to the predicted CREATE2 pair address | Review rule + unit test | Four.meme |

### A7. Arithmetic — Overflow, Rounding, and Precision

| # | Check | How | Would Have Caught |
|---|-------|-----|-------------------|
| A7.1 | Every Yul assembly block using a user-supplied unsigned integer in pointer arithmetic must explicitly validate it against overflow before the addition | Review rule + fuzz test with boundary values | 1inch Fusion v1 [rekt.news/1inch-rekt; decurity.io] |
| A7.2 | Fuzz the computed write offset with arbitrary `interactionLength` values; assert no underflow: `add(add(ptr, offset), length) >= add(ptr, offset)` | Invariant test | 1inch Fusion v1 |
| A7.3 | Unit/fuzz test on shared math library primitives: `checked_shlw(n)` must return `(0, true)` for every `n >= 1 << 192`; fuzz the full u256 range | Unit + fuzz test | Cetus Protocol [medium.com/@CetusProtocol; verichains.io; slowmist.medium.com; halborn.com] |
| A7.4 | At the pool level: depositing `x` of token A never mints liquidity recovering more than `x` on withdrawal | Invariant test | Cetus Protocol |
| A7.5 | Treat shared math libraries as in-scope for audit, not out-of-bounds; review every guard constant for correctness against the mathematical invariant it enforces | Review rule | Cetus Protocol |
| A7.6 | Fuzz swap sequences through `batchSwap`/multi-hop and assert the invariant `D_post >= D_pre - fees` across extreme balance ratios, single-wei amounts, and varied token decimals | Invariant fuzz test | Balancer v2 [rekt.news/out-of-balance; quillaudits.com; github.com/balancer] |
| A7.7 | Round-trip property test: for every `upscale(x, s)` / `downscale(y, s)` pair, assert compose-and-round-trip never produces net invariant loss; every scaling path must round conservatively for the pool | Property test + review rule | Balancer v2 |
| A7.8 | Fuzz time-to-expiry T with random trade volumes in rollover/AMM pricing; assert risk premium rT < 10,000% and initialization price > 1% of reserve assets | Fuzz test | Cork Protocol |

### A8. Oracle and Price Validation

| # | Check | How | Would Have Caught |
|---|-------|-----|-------------------|
| A8.1 | Route all collateral pricing through one `verify_price_source(program_id, market)` helper; require any PR touching a collateral integration to prove the check sits on every path | Review rule + invariant test with hostile source (fuzz `remaining_accounts` with attacker-owned programs) | Loopscale [blog.loopscale.com; rekt.news/loopscale-rekt; halborn.com; oshield.io] |
| A8.2 | Price-sanity bounds in every oracle adapter: `require(price >= minPrice && price <= maxPrice)` with bounds from the asset's known market price, run on every oracle update | Integration test comparing oracle output to a known reference price (e.g. Chainlink) | Moonwell [rekt.news/moonwell-rekt; forum.moonwell.fi] |

### A9. Reentrancy

| # | Check | How | Would Have Caught |
|---|-------|-----|-------------------|
| A9.1 | Apply `nonReentrant` to every order-execution or position-management path that makes an external call before finalizing state; unit test deploys a mock attacker as the account, reenters from the callback, and asserts revert | Unit test + review rule | GMX v1 [rekt.news/gmx-rekt; quillaudits.com] |
| A9.2 | Fuzz/invariant test opening random positions from EOA and contract accounts, executing decrease-orders, and asserting global accumulators (`globalShortAveragePrice` or equivalent) never deviate more than a few basis points from the oracle price | Invariant fuzz test | GMX v1 |

---

## Part B: Operational Controls (Keys, Multisigs, Signing, Configuration)

These incidents were **not** smart-contract bugs. Each exploited a key compromise, signing blind spot, or configuration gap that code alone could not prevent.

| # | Check | How | Would Have Caught |
|---|-------|-----|-------------------|
| B.1 | Every multisig signer must decode and inspect raw transaction calldata on a separate, air-gapped device before signing — never trust the UI alone | Operational procedure | Bybit [rekt.news/bybit-rekt; rekt.news/not-so-safe; safe.global] |
| B.2 | Deploy a canary script that loads the signing frontend, simulates a transaction, and verifies calldata matches the displayed intent; alert on any divergence | Automated monitoring | Bybit |
| B.3 | Pre-launch role inventory: assert no plain EOA holds any privileged role; every holder must be a multisig or timelock contract. Revoke deployer roles immediately after launch | Review rule + invariant test on withdraw path | Infini [rekt.news/infini-rekt; halborn.com; quillaudits.com]; ZKsync Airdrop [cointelegraph.com; halborn.com; zksync.mirror.xyz] |
| B.4 | After an airdrop claim window closes, audit every privileged function on distribution contracts; any mint/transfer/burn path must be timelock-gated, multisig-gated, or permanently disabled | Review rule + ops procedure | ZKsync Airdrop |
| B.5 | Every completed mint/swap must satisfy `mintedAmount <= collateralIn * collateralPrice / (1 - maxSlippageBps)`, bounded by hard per-tx and per-period caps and a total-supply ceiling — even when the signing key is valid | On-chain invariant (contract-level) | Resolv [resolv.xyz/blog; chainalysis.com; rekt.news/resolv-labs-rekt] |
| B.6 | Move mint authorization off a single long-lived EOA: use multisig/MPC with one key per contract; add real-time monitoring wired to an automatic pause on anomalous mints | Operational design | Resolv |
| B.7 | Every admin action that can move or rehypothecate user funds must pass a timelock (≥12h) plus an emergency pause any council member can trigger. Review rule: "Can any N-of-M signers move funds instantly? If yes, governance is incomplete" | Governance design rule + invariant test on admin capabilities | Drift Protocol [rekt.news/drift-protocol-rekt] |
| B.8 | Assert no single admin tx, nor any 24h sequence, can reduce total vault TVL by more than N% without a timelock expiry — fuzz the admin action space on a mainnet-fork simulation | Invariant test | Drift Protocol |
| B.9 | Deployment-gating config test: assert `requiredDVNCount + optionalDVNCount >= 2` with independently operated DVNs and fail CI/deploy otherwise; refuse to sign as the sole required attestor on any bridge channel | Config test + review rule | KelpDAO [layerzero.network; rekt.news/kelpdao-rekt; chainalysis.com; blocksec.com] |
| B.10 | Cross-chain invariant monitoring: continuously assert `released_on_dest <= burned_on_src` and `dest_inbound_nonce <= src_outbound_nonce` per channel; scan source-chain logs for every claimed `PacketSent` event | Operational monitoring | KelpDAO |
| B.11 | Oracle configuration integration test: compare oracle output to a known reference price (e.g. Chainlink ETH/USD × derivative rate), asserting within ±10%, run in CI before every governance vote | CI integration test | Moonwell [rekt.news/moonwell-rekt; forum.moonwell.fi] |
| B.12 | Re-audit and re-run the full test suite on every post-audit change, however small — multiple exploits (SuperRare, GMX v1, Loopscale) were introduced after audits in changes that skipped re-review | Operational process | SuperRare [veridise.com; cointelegraph.com]; GMX v1; Loopscale |

---

## Source Index

- **zkLend:** rekt.news/zklend-rekt; blocksec.com; halborn.com; solidityscan.com; verichains.io
- **Four.meme:** verichains.io; chaincatcher.com; cointelegraph.com; github.com/SunWeb3Sec/DeFiHackLabs
- **Bybit:** rekt.news/bybit-rekt; rekt.news/not-so-safe; x.com/Bybit_Official; x.com/safe
- **Infini:** rekt.news/infini-rekt; halborn.com; quillaudits.com; decrypt.co
- **1inch Fusion v1:** rekt.news/1inch-rekt; decurity.io; github.com/SunWeb3Sec/DeFiHackLabs
- **Abracadabra:** rekt.news; web3isgoinggreat.com; hacked.slowmist.io; defillama.com
- **SIR.trading:** docs.sir.trading; verichains.io; slowmist.medium.com; blockscope.co; rekt.news/sirtrading-rekt
- **KiloEx:** rekt.news/kiloex-rekt; slowmist.medium.com; medium.com/@KiloEx; solidityscan.com; blockscope.co
- **ZKsync Airdrop:** cointelegraph.com; halborn.com; zksync.mirror.xyz; theblock.co
- **Loopscale:** blog.loopscale.com; rekt.news/loopscale-rekt; halborn.com; quillaudits.com; oshield.io
- **MobiusDAO:** rekt.news/mobiusdao-rekt (archived)
- **Cetus Protocol:** medium.com/@CetusProtocol; verichains.io; slowmist.medium.com; halborn.com; quillaudits.medium.com; rekt.news/cetus-rekt
- **Cork Protocol:** cork.tech/blog/post-mortem; cork.tech/blog/lessons-learned; rekt.news/cork-protocol-rekt
- **Meta Pool:** solidityscan.com; quillaudits.com; medium.com/meta-pool; okx.com; crypto.news
- **Silo Finance:** quillaudits.com; etherscan.io
- **Resupply:** blocksec.com; mirror.xyz (Resupply post-mortem); rekt.news/resupplyfi-rekt; ackee.xyz; quillaudits.com
- **GMX v1:** rekt.news/gmx-rekt; quillaudits.com
- **Kinto ($K):** medium.com/mamori-finance (Kinto post-mortem); dedaub.com; nethermind.io; rekt.news/just-bad-luck; thedefiant.io
- **Arcadia Finance:** rekt.news/arcadiafi-rekt
- **SuperRare:** verichains.io; solidityscan.com; veridise.com; cointelegraph.com; hacked.slowmist.io
- **Bunni v2:** blog.bunni.xyz; rekt.news/bunni-rekt; github.com/Cyfrin (audit)
- **Typus Finance:** medium.com/@TypusFinance; slowmist.medium.com; halborn.com; defimon.xyz; mehvetero.com
- **Balancer v2:** rekt.news/out-of-balance; quillaudits.com; github.com/balancer
- **Yearn yETH:** github.com/yearn/yearn-security; blocksec.com; rekt.news/yearn-rekt3; quillaudits.com; a16zcrypto.com
- **Truebit:** certik.com; github.com/SunWeb3Sec/DeFiHackLabs; api.llama.fi/hacks
- **CrossCurve:** cantina.xyz; x.com/MixBytes; blocksec.com; quillaudits.com; github.com/axelarnetwork
- **Moonwell:** rekt.news/moonwell-rekt; forum.moonwell.fi; github.com/moonwell-fi
- **Resolv:** resolv.xyz/blog; chainalysis.com; rekt.news/resolv-labs-rekt; theblock.co
- **Drift Protocol:** rekt.news/drift-protocol-rekt
- **KelpDAO:** layerzero.network; rekt.news/kelpdao-rekt; chainalysis.com; blocksec.com; quillaudits.com; gist.github.com/banteg; migalabs.io
