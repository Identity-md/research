# Audit report

> RPC trust (can a compromised/fallback RPC cause a bad trade), mixed-protocol 2-tx routes (leg 1 confirms, leg 2 fails — is the wallet stuck?), V3 creation-call quote (can a fake pool return a wrong quote), and approval scope (100x limits, REVOKE ALL completeness).

| | |
|---|---|
| Repository | https://github.com/identity-md-launches/launch-3068-fix-one-bug-v4.git |
| Commit | `ff2a23a03492bbd06b2cca00d9a9bcfce7e80623` |
| Job | `fee44163-9c52-422a-a624-9abf2e17950f` |
| Judged | 2026-11-08 18:28 UTC |
| Findings | 1 high · 4 medium · 2 low · 2 info |

Four agents audited the code as it is at `ff2a23a`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. High: Auto mode sends a round trip whose own return quote shows a loss, and repeats it every poll while the ticks stay GREEN

`index.html:911`

```
      if (best.verdict !== "GREEN" || !(best.netPercent > thresholdOrDefault())) return;
```

maybeAutoExecute() decides to trade on a GREEN verdict and Net% computed from the two pools' last-swap ticks (rankSpreads/protocolAutoDecision), then runs quoteSpread() -> dryRun() -> send() without comparing the quotes it just fetched with the input. quoteSpread() already holds the expected return: selected.finalQuote for routes with a V3 leg (index.html:842) and, for V4/V4 routes, the return quote showGasEstimate() fetches at index.html:794 for display only. Neither gates send(). The only on-chain floors are swap 1 amountOutMinimum = buy quote - 0.5% and, for V3 routes, swap 2 minimum = sell quote - 0.5% (index.html:378); for V4/V4 the field default 0 applies. So when the ticks are stale or the sell pool is thin, auto mode executes a trade its own quote says loses money, and for V3 routes sets the floor AT the losing quote, locking the loss in. A successful losing swap is not a failure, so runAction()'s auto-off branch (index.html:448) never fires and the next 30 s poll repeats the trade while the ticks still read GREEN, up to the 100x approval the page granted. Merged from audit_flow (b921c909) and audit_economics (194c60ac); both reproduce. Fix: in maybeAutoExecute() (auto only), after quoteSpread() require the quoted return (selected.finalQuote, or the V4/V4 sell quote, which must then be fetched before send rather than for display) to exceed selected.amountIn (plus gas when netAfterGasUsd is available), otherwise throw so auto mode switches itself off; also refuse to auto-execute a V4/V4 route while the minimum-return field is 0.

**Reproduction**

node test/scratch/repro.js (runs the real index.html inline script against js/test/mock-wallet.js and js/test/v3-mock.js exactly as js/test/ui.test.js does). Case A (V4/V4, mocks unchanged): MockWallet.addSwap(3000,60,-292916), addSwap(30000,600,-292000); the 30000/600 pool exists with quote 0 (LIVE_PRICE_X36, as the live pool on 2026-11-07). Spread row is GREEN; after selecting it gas-info reads 'Expected return 0.0 USDG for 0.01 USDG (-0.01000 USDG)'. Connect, APPROVE PERMIT2, tick auto-mode. Expected: nothing sent (the page's own return quote is 0). Actual: eth_sendTransaction sent with swap 1 {amountIn 10000, amountOutMinimum 52096879755458694} and swap 2 {amountIn 52096879755458694, amountOutMinimum 0}; status 'Swap confirmed'; USDG 25000000 -> 24990000; auto-mode checkbox still checked; next poll sends an identical swap, USDG 24980000. Case B (V3/V3): V3Mock with the sell leg returning 1% of the fixture rate (1 PONS -> 0.0022 USDG), Protocol V3, USDG->SwapRouter02 allowance 1000000, auto-mode on. Row 'V3 0.30% | V3 1.00% | 9.592 | 1.300 | 8.292 | GREEN'; quote-info 'Return quote: 0.00011 USDG; minimum after 0.5%: 0.000109'; approval-limits 'Enforced minimum return: 0.000109 USDG'. Expected: refused (return quote 110 < input 10000). Actual: exactInput(amountIn 10000, amountOutMinimum 109) sent and confirmed, USDG 25000000 -> 24990110 (9890 of 10000 base units lost), auto mode still on.

### 2. Medium: V4/V4 routes, including auto mode, execute swap 2 with amountOutMinimum 0 by default while the same sell quote is enforced as a floor for V3 routes

`index.html:839`

```
      if (E.protocolOf(spread.buy) === "V3" || E.protocolOf(spread.sell) === "V3") {
```

quoteSpread() quotes the sell leg and sets selected.minimumReturn = finalQuote - 0.5% only when one leg is V3 (index.html:839-846). readAmounts() (index.html:378) raises the operator's field to that floor, and routeSnapshot() rejects a zero minimum only for V3 routes (js/v4-arb-encoder.js:2368). For a V4/V4 spread the same sell quote is fetched by showGasEstimate() (index.html:794) but used for display only; minUsdgOut stays at the field default '0' (index.html:177) and buildCalldata() accepts amountOutMinimum 0 for swap 2. The transaction therefore protects swap 1 (bridge minimum) but lets swap 2 accept any output, including 0, so a moved or thin sell pool or a sandwich takes the whole second leg. The README documents 'minimum 0' as a small-amount manual test, but auto mode executes V4/V4 spreads with no click beyond the signature, so the only branch that can run unattended is the unprotected one. Merged from audit_permissions (02d9ed86) and audit_math (208e01a8). Fix (keeping the manual-test behaviour available): set selected.minimumReturn = applySlippage(sellQuote) for every route in quoteSpread() and let the operator lower it only by explicit entry when auto mode is off; have routeSnapshot()/prepareSwap() refuse minUsdgOut == 0 for every route.

**Reproduction**

node test/scratch/repro.js case C: MockWallet with addSwap(3000,60,-292916), addSwap(30000,600,-292000) and a healthy 30000/600 quote (price 5e48); connect, select the GREEN row, APPROVE PERMIT2, BUILD CALLDATA & DRY RUN. gas-info shows 'Expected return ... USDG for 0.01 USDG'; min-out field is '0'; status 'Dry run succeeded'. Decoding the calldata element: swap 1 {amountIn 10000, amountOutMinimum 52096879755458694}, swap 2 {amountIn 52096879755458694, amountOutMinimum 0}. Expected (as the V3 path does, see case B where amountOutMinimum = sell quote x 0.995): a non-zero floor derived from the sell quote. Actual: 0. Case A shows the same transaction being sent by auto mode with a sell quote of 0.

### 3. Medium: Every on-chain minimum is derived from the monitoring RPC's quote (with silent 429/5xx fallback) and no sanity bound; a deflated quote reduces the slippage floor to 1 base unit while the wallet-side d

`index.html:843`

```
          selected.minimumReturn = E.applySlippage(selected.finalQuote);
```

All quotes (V3 creation-call eth_call, V4 router-revert eth_call) go to the public RPC client created at index.html:248, never to the wallet provider. createRpcClient.post() (js/v4-arb-encoder.js:1312-1331) retries the same payload once against RPC_FALLBACK_URL on HTTP 429 or any 5xx and returns whichever answers; nothing records or shows which endpoint produced a quote. quoteV3ExactIn() (js/v4-arb-encoder.js:616-620) and decodeQuoteRevert() (js/v4-arb-encoder.js:1439-1444) accept any well-formed revert payload. The quote alone sets selected.bridgeAmount (swap 1's minimum and swap 2's input) and selected.minimumReturn (the enforced floor at index.html:378). There is no cross-check against the tick-derived price the page already holds (pool.price/displayPrice from Swap logs or slot0), no lower bound relative to amountIn, and the min-out field defaults to 0, so a deflated quote passes routeSnapshot()'s only check (minimum != 0). The dry run and send go through the wallet provider, but a swap with amountOutMinimum 1 simulates fine at the real price, so the 'wallet re-simulates the same bytes' safety net does not catch it. An over-stated quote fails closed (revert); the exploitable direction is 'too small'. A primary endpoint that merely answers 429 moves trust to the second provider for that one request. The V3 creation-call quote itself is sound (factory-bound pool, callback authenticates msg.sender == pool, exact selector and length, partial fills rejected; validateV3Pools() rejects a pasted pool the factory does not return), so the RPC is the only party that can forge a quote. Merged from audit_flow (f6296ace), audit_economics (24957ca7) and audit_math (94cb8165). Fix: bound the accepted quote against the log/slot0-implied price (refuse when the quote-implied price deviates more than a configurable few percent from 1.0001^tick scaled by decimals), refuse a round-trip minUsdgOut below usdgIn x (1 - 2 x SLIPPAGE_BPS/10000) unless the operator explicitly opts in, cross-check quotes through the wallet provider's eth_call, and surface fallback use in the status bar.

**Reproduction**

node test/scratch/repro.js case E: V3Mock, Protocol V3, USDG->SwapRouter02 allowance 1000000; the page's fetch (monitoring RPC) is patched so the sell-leg creation-call eth_call reverts with V3QuoteResult(amountInUsed = amount, amountOut = 2) while the wallet path is untouched. Observed: quote-info 'Return quote: 0.000002 USDG; minimum after 0.5%: 0.000001', approval-limits 'Enforced minimum return: 0.000001 USDG', dry run 'Dry run succeeded', SEND sends exactInput(amountIn 10000, amountOutMinimum 1) and the receipt confirms. Honest sell output for the 0.04975 PONS bridge in the same fixture is 10945 (floor 10890). Case H (client level): createRpcClient(E.RPC_URL, fetch, {fallbackUrl: E.RPC_FALLBACK_URL}) where the primary answers HTTP 429 and the fallback returns V3QuoteResult(49750000000000000, 2): quotePool() returns 2 after contacting ['https://rpc-robinhood.blockmachine.io','https://robinhood.drpc.org'], applySlippage(2) = 1, with no indication to the caller that the fallback answered. Expected: a floor near 10890 or a refusal/visible warning; actual: floor 1 of 10000 input base units.

### 4. Medium: Trade size and the 100x approval limits are scaled with decimals() read from the monitoring RPC; a lying primary or fallback RPC multiplies the amount the wallet signs while every display stays consis

`index.html:820`

```
      const amountIn = ethers.utils.parseUnits(inText, meta.decimals1);
```

Token metadata that converts the operator's typed amounts into base units comes only from the monitoring RPC: createPoolMonitor/createAllPairsMonitor/createManualMonitor read symbol() and decimals() through rpc.request/rpc.batchRequest (js/v4-arb-encoder.js:369-378, 1497-1499), and index.html uses meta.decimals1 in quoteSpread() (line 820) and readAmounts() (lines 376-377) to build usdgIn and minUsdgOut, and in every format() call, the balance bar and the approval-limits text. Nothing re-reads decimals through the wallet provider or checks them against the fixed table of known tokens (USDG 6, PONS 18, WETH 18) the file already carries. Because the same wrong decimals drive both the base-unit conversion and every formatted display, the operator sees '0.01 USDG', 'V3 Router limit: 1.0 USDG' and a balance bar that all agree, while the transaction, the 100x SwapRouter02 approval and the 100x Permit2 approval are built from a 100x larger base-unit amount. The wallet-side eth_call passes because the inflated amount is covered by balance and by the allowance the page's own APPROVE button just granted. Together with the quote finding, a compromised RPC controls amountIn, amountOutMinimum and the approval limits of what the operator signs. Distinct mechanism and fix from the quote finding, so kept separate. From audit_permissions (72134f2a). Fix: read decimals()/symbol() through the wallet provider before building amounts (or compare and refuse on mismatch), and pin the known tokens' decimals in the encoder, rejecting RPC values that disagree.

**Reproduction**

node test/scratch/repro.js case F: V3Mock whose fetch path (monitoring RPC) answers USDG decimals() = 8 while the wallet path is untouched; Protocol V3; default input '0.01'; select the GREEN V3/V3 spread; APPROVE V3 ROUTER; BUILD CALLDATA & DRY RUN. Observed: quote-info 'Swap 1 quote: 0.01 USDG -> 5.0 PONS', approval-limits 'V3 Router limit: 1.0 USDG (100 test swaps)', balance bar '0.25 USDG' (the real 25 USDG shown with 8 decimals), USDG.approve(SwapRouter02, 100000000) signed (= 100 real USDG, displayed as 1.0), and the dry-run calldata is exactInput(amountIn 1000000, amountOutMinimum 1094500) (= 1 real USDG sold, displayed as 0.01). Expected: amountIn 10000 and approval 1000000, or a refusal because the RPC's decimals disagree with the wallet's/known value. Same with the plain module: E.createPoolMonitor({request: async () => {}, batchRequest: async () => [abi.encode(['string'],['PONS']), abi.encode(['uint8'],[18]), abi.encode(['string'],['USDG']), abi.encode(['uint8'],[8])], protocol: 'V4'}).loadPair(E.PONS, E.USDG) yields decimals1 = 8 and parseUnits('0.01', 8) = 1000000.

### 5. Medium: REVOKE ALL revokes only currency1's ERC20 allowances; the currency0 allowance to SwapRouter02 the page grants on V4-buy/V3-sell routes and both tokens' Permit2 router allowances survive while the stat

`index.html:962`

```
      const done = await wallet.revokeAll(meta.currency1, meta.symbol1);
```

wallet.revokeAll(token) (js/v4-arb-encoder.js:2618-2644) sets token.approve(V3_ROUTER, 0) and token.approve(PERMIT2, 0) for ONE token, and the click handler passes only meta.currency1. But the page itself grants allowances on currency0 too: approveRouteV3() approves 100x the V3 leg's input to SwapRouter02, and routeApprovals() (js/v4-arb-encoder.js:2376-2380) makes that input currency0 (the bridge token) for a mixed V4-buy/V3-sell route; approveRoutePermit2()/approveBothPermit2() write Permit2 allowances to the Universal Router for currency1 and, in V4/V4 and V3->V4 routes, currency0 (100x, 30 days). None of these is touched. The README's justification ('with the ERC20 allowance at 0 the router cannot pull anyway') holds only for currency1: currency0's ERC20 allowance to Permit2 (operator-granted, typically unlimited) is never revoked, so currency0's Permit2 -> router entry stays spendable, and currency0's direct allowance to SwapRouter02 stays at 100x the bridge. After the button finishes the page reports 'REVOKE ALL finished for USDG. Approvals are needed again before the next swap', which is false: a V4->V3 route can be re-sent at once. No third party can spend these allowances (both routers pull only from msg.sender), so this is a completeness and false-assurance defect rather than a direct drain. Merged from audit_flow (88e0287e), audit_permissions (e5108a8f), audit_economics (7c0b4819) and audit_math (0693167e). Fix: in the click handler iterate over [meta.currency0, meta.currency1]; extend revokeAll() to call Permit2.approve(token, ROUTER, 0, 0) (encodePermit2Approve already supports amount 0) when readPermit2 shows a non-zero amount; update the Section 2 text and final status, or rename the button to state its single-token scope.

**Reproduction**

node test/scratch/repro.js case D: V3Mock with V4 3000/60 at tick -293000 (cheaper) and V3 0.30% at tick -292000 -> V4 buy, V3 sell mixed route; select it, connect, APPROVE V3 ROUTER (PONS.allowance(owner, SwapRouter02) becomes 4975000000000000000 = 100 x 0.04975 bridge), APPROVE PERMIT2 (Permit2.allowance(owner, USDG, UniversalRouter) = 1000000), dry run, SEND (both legs confirm). Click REVOKE ALL. Observed: one transaction USDG.approve(Permit2, 0) (USDG -> SwapRouter02 was already 0); revoke-status 'USDG allowances revoked: Permit2 0x..05'; status 'REVOKE ALL finished for USDG. Approvals are needed again before the next swap.' Afterwards: PONS -> SwapRouter02 = 4925250000000000000 (still live), PONS -> Permit2 = MaxUint256, Permit2(USDG -> UniversalRouter) = 990000 with its 30-day expiry, USDG -> SwapRouter02 = 0, USDG -> Permit2 = 0. Expected: every allowance the page granted at 0, or a status that states the single-token scope.

### 6. Low: Mixed 2-tx route: after leg 1 confirms and leg 2 fails there is no leg-2-only retry or sell path; the only in-page continuation re-executes leg 1 and doubles the bridge exposure

`js/v4-arb-encoder.js:2458`

```
      return [route.buy, route.sell].map(function (pool, index) {
```

sendRoute() (js/v4-arb-encoder.js:2502-2560) sets prepared = null, sends leg 1, waits for its receipt, then checks bridge balance, deadline and leg-2 allowance, simulates and sends leg 2. Any failure after firstReceipt (leg-2 eth_call revert because the sell pool moved below minUsdgOut, deadline passed during a slow leg 1, wallet rejection, revert, receipt timeout) throws 'Leg 1 confirmed (...). Leg 2 did not confirm' and leaves the wallet holding the bridge token. The wallet is not stuck in the sense of locked funds (the bridge token is a normal balance and TRANSFER ALL can move it), but the page has no entry point that builds or sends only the sell leg: routeTransactions() always begins with the buy leg, prepareRoute()/sendRoute() only accept a full route, and the leg-2 floor (selected.minimumReturn) is quoted at selection time and never refreshed after leg 1 confirms. So the operator who follows the UI's only path (re-select the spread, dry run, send) buys a second bridge amount before any of the first is sold. The README documents that leg 1 cannot be rolled back and that restarting is never automatic, but not that the tool cannot finish the trade. Merged from audit_flow (e1bcd169), audit_permissions (5abe9b16), audit_economics (722a3a17) and audit_math (db4c0a83). Fix: after a confirmed leg 1 keep a 'leg 2 pending' context (bridge amount actually received, sell pool, deadline), re-quote the sell leg for a fresh minimum, re-run the allowance/deadline checks and expose a single-leg 'retry leg 2 / sell bridge' action built from routeTransactions(route, ...)[1]; at minimum make prepareRoute() refuse a new mixed route while the wallet holds the unsold bridge amount without an explicit acknowledgement.

**Reproduction**

node test/scratch/repro.js case G: V3Mock with V3 0.30% at tick -293000 (cheaper) and V4 3000/60 at -292000 -> V3 buy, V4 sell; PONS balance 0; select, connect, APPROVE V3 ROUTER, APPROVE PERMIT2, dry run; set rejectSend so the wallet rejects leg 2; SEND. Observed: status 'Wallet request rejected. Leg 1 confirmed (0x..03). Leg 2 did not confirm; check both hashes...'; bal-a '0.05 PONS'; bal-b '24.99 USDG'; SEND disabled; the page has no control whose id matches sell/leg/resume/retry. Clear the rejection and take the only path offered: click the same spread, BUILD CALLDATA & DRY RUN, SEND. Observed: prepared transactions[0].to = 0xcaf681a66d020601342297493863e78c959e5cb2 (SwapRouter02) with exactInput(amountIn 10000, amountOutMinimum 49750000000000000), i.e. leg 1 again; after send the wallet holds 0.05025 PONS and 24.990945 USDG, and the sent targets are [USDG approve, Permit2 approve, SwapRouter02, SwapRouter02, UniversalRouter]. Expected: one transaction selling the 0.05 PONS already held. The repository's own test 'mixed second-leg rejection leaves bridge funds visible and never repeats the first leg' (js/test/ui.test.js:875) asserts the stop but exercises no continuation.

### 7. Low: The RPC proxy Worker is an open relay: any origin can forward any JSON-RPC method through the operator's Cloudflare account and upstream quota

`worker/rpc-proxy.js:36`

```
    "access-control-allow-origin": "*",
```

handle() accepts any POST whose body parses as a JSON-RPC object or array (validPayload, lines 58-65), forwards it unchanged to the primary and on 429/5xx to the fallback, and answers with access-control-allow-origin: *. There is no origin allow-list, no method allow-list (eth_sendRawTransaction, debug_*, trace_* are forwarded), no shared secret and, by design comment, no rate limit. Once deployed and set as RPC_URL the URL is public in the served page, so a third party can exhaust the operator's Worker quota and the upstream providers' per-origin limits; because the page itself falls back on 429, that traffic also pushes the legitimate page onto the fallback provider, which is the trust expansion described in the quote finding. The upstream endpoints are public and keyless, so the gain to an attacker is the operator's quota rather than a secret. From audit_math (ebe79e58). Fix: restrict access-control-allow-origin to the page's origin, allow-list the methods the page uses (eth_call, eth_getLogs, eth_getBlockByNumber, eth_blockNumber, eth_gasPrice, eth_chainId), and add a per-IP rate limit (Cloudflare rate-limiting rule or a Workers KV counter).

**Reproduction**

Node, no network: const P = require('./worker/rpc-proxy.js'); await P.handle({method:'POST', headers: new Map([['origin','https://evil.example']]), text: async () => JSON.stringify({jsonrpc:'2.0', id:1, method:'eth_sendRawTransaction', params:['0x02']})}, recordingFetch). Observed: status 200, access-control-allow-origin '*', and recordingFetch received exactly that body for https://rpc-robinhood.blockmachine.io. Expected: rejected on origin or method. Deployed, the same holds for curl -X POST https://<worker>/ with any JSON-RPC body in a loop.

### 8. Info: V3 creation-call quote short-circuits to (0, 0) when in-range liquidity() is 0, excluding a factory pool whose positions sit just outside the current tick although the real swap would fill

`src/V3Quote.sol:69`

```
        if (IV3QuotePool(pool).liquidity() == 0) revert V3QuoteResult(0, 0);
```

Uniswap V3 liquidity() is the liquidity at the current tick only. A pool whose positions lie entirely above or below the current price has liquidity() == 0, yet an exact-input swap crosses into those positions and fills. V3Quote returns (0, 0) before calling swap(), quoteV3ExactIn() returns 0, the page shows 'Warning: no liquidity' and disables execution (index.html:830-836), and readPoolHealthBatch() marks the same pool EMPTY from liquidity() (js/v4-arb-encoder.js:1540-1541). This is a false negative (missed trades), never an over-quote or an under-protected trade: a pool that only partially fills is still rejected by the client's amountInUsed != amountIn check (js/v4-arb-encoder.js:619), and swap() already handles received == 0. On the fake-pool question the review was asked: the quote path is bound to the hardcoded factory (lines 59, 66-68), the callback authenticates msg.sender == pool (line 47) and quote() the creator (line 34), the client requires the exact V3QuoteResult selector with 68 bytes, the embedded bytecode matches the pinned artifact (node scripts/embed-v3-quote.js --check), and validateV3Pools() requires factory.getPool(...) == the pasted address before execution, so a pasted or RPC-supplied fake pool cannot alter the quoted amount; only the RPC can (see the quote finding). Merged from audit_flow (d115b1da) and audit_permissions (0c0bfb1d). Fix, if exactness is wanted: drop the pre-check and let the callback report the real (amountInUsed, amountOut); if kept for gas, treat it as 'possibly empty' rather than 'no liquidity'.

**Reproduction**

forge test --match-path test/V3Quote.t.sol: test_ZeroLiquidityReturnsZeroWithoutAttemptingSwap (test/V3Quote.t.sol:76-80) passes on this tree: pool.configure(0, 1) (liquidity 0, swap() configured to revert) and new V3Quote(USDG, PONS, 3000, 10000) reverts V3QuoteResult(0, 0) without swap() being called, which pins the shortcut. On a real pool with current tick between two initialised ranges and all liquidity in, e.g., [tick+60, tick+600] with zeroForOne = false: eth_call of the V3Quote creation code with (tokenIn, tokenOut, fee, amount). Expected exact quote: V3QuoteResult(amount, amountOut > 0) after crossing into range. Actual: V3QuoteResult(0, 0); the page disables the row and auto mode skips it.

### 9. Info: Single JSON-RPC responses are accepted without checking id or jsonrpc, unlike array batch responses

`js/v4-arb-encoder.js:1349`

```
      return body.result;
```

batchRequest() matches array replies to requests by id through resultOf() (js/v4-arb-encoder.js:1333-1340, used at 1402), which also requires jsonrpc === '2.0' and a present result. request() (lines 1342-1350) does neither: any 2xx JSON object without an error key is accepted and body.result (possibly undefined) is returned. Every quote, allowance read, balance read and gas price taken over rpc.request therefore trusts a reply that may belong to another request when a proxy, CDN or misbehaving node replays or cross-wires replies. The Worker in this repository forwards bodies unchanged, so this is defence in depth rather than a live break. From audit_math (4e6bda01). Fix: route request() through resultOf(body, call.id).

**Reproduction**

Node, no network (node test/scratch/repro.js case H): const rpc = E.createRpcClient('https://example.invalid', async () => ({ok: true, status: 200, json: async () => ({jsonrpc: '2.0', id: 999, result: '0xdead'})})); await rpc.request('eth_call', []) (envelope id 1) resolves to '0xdead'. Expected: 'RPC returned an invalid response for id 1', as resultOf() reports for a batch. Actual: the mismatched result is returned to the caller.

---

Judge's submission `4b15419f2214afb9426ca9668ab029f95208d3fd913c88a1c3dbde071549a12f`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
