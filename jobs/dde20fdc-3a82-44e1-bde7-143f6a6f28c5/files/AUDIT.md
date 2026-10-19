# Audit report

> Audit e69e04f63832b9fa1e84c7d58c685ce37924a490. Focus on changes since 357201be804e18ab48567172fb6c8b07acb30a2c and closure of findings 1-4 in https://explorer.imd.fun/jobs/7db42bb7-5204-4805-894f-db1a2c11cd8e.
>
> Verify full-horizon true/false receipt acceptance on Ethereum and Robinhood native clocks; enforced minimum age policy and preflight agreement; owner expiry strictly after deadline+300+86400; requester-only original-asset top-ups for committed Delivered/None untriggered asks, exact escrow/cap/refund accounting, preserved identity and refreshed maturity.
>
> Check snapshotted Intake/action/asset quotes, fail-closed funded SDK/UI readiness, separate bounded approval/top-up readbacks, and wallet/account/chain/requester changes during those flows. Review codec.validateReview extraction: preserve canonical bool/question/window/panel checks, requester-domain signatures/ERC1271 caller context, epochs/revocation, replay and settlement. Preserve prior lifecycle fixes and terminal false verdicts.
>
> Reproduce material findings; rerun isolated cold ERC1271 callback <=200000 gas and runtime <=24576 bytes. Separate code defects from documented cadence assumptions and unperformed live-pilot checks. No deployment or spending.

| | |
|---|---|
| Repository | https://github.com/identity-md-launches/launch-1811-build-technical-foundation-hooks.git |
| Commit | `e69e04f63832b9fa1e84c7d58c685ce37924a490` |
| Job | `dde20fdc-3a82-44e1-bde7-143f6a6f28c5` |
| Judged | 2026-10-19 08:09 UTC |
| Findings | 2 low · 2 info |

Four agents audited the code as it is at `e69e04f`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Low: UI top-up approval/funding re-reads the requester field after validation and never checks the wallet chain, so the bounded approval and topUpReserve can go to an unvalidated spender or network

`site/automatic-ui.js:137`

```
    await send(p.token, '0x095ea7b3' + A.address(requester()) + A.uint(p.amount));
```

Merged from audit_economics (chain) and audit_flow (requester re-read); both reproduced. topUpParameters() (lines 118-134) validates ownership, phase, candidate, unspent ask and cap against the requester address read from the input field at that moment and returns {job, ask, amount, token, data}, but not the requester address. The approveTopUp handler then builds the ERC-20 approval spender from a fresh requester() read (line 137) and reads requester() a third time for the allowance readback (line 138); the topUp handler sends p.data (built for the validated job) to send(requester(), ...) (line 145), again re-reading the field. connected() (lines 13-19) only re-checks eth_accounts and automaticBindingSupported(); no code path in the top-up, verdict, commit, cancel or renew flows ever requests eth_chainId. Only openParameters (line 41) compares the wallet chain with the HookSpec. So if the requester field is edited, or the wallet switches network, between the validation reads and eth_sendTransaction, the wallet is asked to sign an approval whose spender or chain was never validated, while the output still reports the validated job/ask. Where the requester has no code on the new chain the flow fails closed (BigInt('0x') throws), so the chain exposure is limited to same-address deployments (CREATE2/deterministic, Sepolia rehearsal vs mainnet). No contract funds move without the user's wallet signature, and the contracts enforce the final limits atomically, hence low. This is a gap against the stated requirement to handle wallet/account/chain/requester changes during these flows: account changes are handled, chain and requester changes are not. The SDK path (sdk/automatic.py top_up_reserve) is not affected: it reads once and emits unsigned transactions. Fix: capture const to = requester() once inside topUpParameters and return it in p; use p.requester for the approval spender, the allowance readback and the topUp send; record eth_chainId at connect (or at the status read) and have connected() throw when it differs, exactly as openParameters does for HookSpec.

**Reproduction**

Node harness (same shape as test/automatic-funding-ui.test.cjs) whose mock wallet serves state for requester 0x1212...12 and sets the requester field to 0x9999...99 when it answers the head() read, which is the last read in topUpParameters(). Steps: click connect, click approveTopUp. Expected: the approval transaction's spender is the validated 0x1212121212121212121212121212121212121212 (or the flow refuses to send), and at least one eth_chainId request is made before sending. Actual (reproduced with `node --test`): sent.length == 1, sent[0].to == token, spender decoded from calldata == 0x9999999999999999999999999999999999999999, assertion fails with 'approval granted to an address topUpParameters never validated'; calls.some(c => c.method === 'eth_chainId') is false (no chain read in the whole flow). Full test (save as test/scratch/ui-topup-race.test.cjs, run `node --test test/scratch/ui-topup-race.test.cjs`):
'use strict';
const {test} = require('node:test');
const assert = require('node:assert/strict');
const {readFileSync} = require('node:fs');
const vm = require('node:vm');
const A = require('../../site/automatic.js');
const requester = '0x'+'12'.repeat(20), other = '0x'+'99'.repeat(20), creator = '0x'+'23'.repeat(20), token = '0x'+'34'.repeat(20);
const job = '0x'+'56'.repeat(32), ask = '0x'+'67'.repeat(32);
const words = (...values) => '0x'+values.map(x => A.uint(x)).join('');
function wallet() {
  const state = {price:501n, reserve:500n, cap:1000n, allowance:0n};
  const elements = new Map(), sent = [], calls = [];
  const el = id => { if (!elements.has(id)) elements.set(id, {value:'',textContent:'',addEventListener(e,fn){this.click=fn;}}); return elements.get(id); };
  el('requester').value = requester; el('job').value = job; el('ask').value = ask; el('topUpAmount').value = '1';
  const provider = {async request({method,params}) {
    calls.push({method,params});
    if (method === 'eth_accounts' || method === 'eth_requestAccounts') return [creator];
    if (method === 'eth_estimateGas') return '0x20000';
    if (method === 'eth_sendTransaction') { sent.push(params[0]); return job; }
    if (method === 'eth_getTransactionReceipt') return {status:'0x1'};
    const {to,data} = params[0];
    if (data.startsWith('0xdd62ed3e')) return words(state.allowance);
    if (data === '0x'+A.selectors.automatic) return words(1);
    if (data === '0x'+A.selectors.asset) return '0x'+A.address(token);
    if (data === '0x'+A.selectors.maxPrice) return words(state.cap);
    if (data === '0x'+A.selectors.head) { el('requester').value = other; return words(900008); }
    if (data.startsWith('0x'+A.selectors.job)) { const w = Array(15).fill(A.uint(0)); w[0] = A.address(creator); w[3] = A.uint(2); w[4] = A.uint(0); return '0x'+w.join(''); }
    if (data.startsWith('0x'+A.selectors.ask)) return ask;
    if (data.startsWith('0x'+A.selectors.askContext)) return words(1,0,0,0,0,0,0,0,0);
    if (data.startsWith('0x'+A.selectors.candidate)) return words(1);
    if (data.startsWith('0x'+A.selectors.reserveDeadline)) return words(1800086400);
    if (data.startsWith('0x'+A.selectors.reserve)) return '0x'+A.address(token)+A.uint(state.reserve)+A.uint(0);
    throw Error('unexpected call '+data);
  }};
  vm.runInNewContext(readFileSync('site/automatic-ui.js','utf8'), {AutoHooks:A,document:{getElementById:el},window:{ethereum:provider},setTimeout});
  return {state, el, sent, calls};
}
test('approveTopUp approves the requester field value read after validation, and never anchors the chain', async () => {
  const w = wallet();
  await w.el('connect').click();
  await w.el('approveTopUp').click();
  assert.equal(w.sent.length, 1);
  assert.equal(w.sent[0].to, token);
  const spender = '0x' + w.sent[0].data.slice(10, 74).slice(24);
  assert.equal(spender, requester, 'approval granted to an address topUpParameters never validated: ' + spender);
  assert.ok(w.calls.some(c => c.method === 'eth_chainId'), 'top-up flow never reads eth_chainId');
});

### 2. Low: topUpReserve and retryVerdict compare an original-asset reserve against the current maxPrice, which is denominated in whatever asset setProtocol last set; after an asset rotation a committed build-pai

`src/imd/automatic/AutoHookJobRequester.sol:444`

```
        if (amount == 0 || total > maxPrice) revert InvalidConfig();
```

From audit_math; reproduced. `total` is `p.reserve + amount` in base units of the job's original asset (`p.asset`, which topUpReserve pulls at line 448), but `maxPrice` is one storage value that setProtocol (line 578) rewrites together with `asset`. After the owner rotates the protocol asset, the two sides of the comparison are in different units. The runbook (docs/AUTOMATIC_BINDING.md, 'The resulting total reserve must not exceed the current maxPrice, including after protocol rotation') documents the cap as the live value, and the legacy requester's own comment (src/imd/HookJobRequester.sol line 913, 'a ceiling means nothing in another asset') acknowledges the unit problem, so this is a documented design interaction with an owner power, not a permission bypass. Its numeric consequence was not examined: (1) rotating from an 18-decimal asset (cap 1e18) to a 6-decimal asset (cap 2e6) makes every top-up of an existing 18-decimal reserve revert InvalidConfig, since even reserve + 1 (0.5e18 + 1) exceeds 2e6; the committed, build-paid job can no longer be funded when the Intake's price in the original asset rises, and the only exit is to wait for the reserve deadline, cancelReserve and withdraw, with the build fee sunk. The identical `reserve > maxPrice` check in retryVerdict (line 491) blocks any retry of an Unanswered ask for such a job. (2) The inverse rotation (6-decimal cap 2e6 to 18-decimal cap 2e18) lets a requester reserve up to 2e18 base units of the 6-decimal token for a legacy job, so the ceiling no longer bounds what one ask may cost in that asset (bounded only by the requester's own funds and the Intake quote). Precondition: the owner calls setProtocol with a different asset while legacy-asset jobs are live; the runbook recommends rotating with no pending work but nothing enforces it. Fix requires a scope decision: snapshot the cap per job at openJob (add `uint256 cap` to Payment, compare `total > p.cap` here and `reserve > p.cap` in retryVerdict), or apply the live maxPrice only when `p.asset == asset` and otherwise the snapshotted cap. Either keeps the owner's ability to raise or lower the ceiling for new jobs while keeping a legacy-asset job's limit in its own units. The runtime is 108 bytes under EIP-170, so the fix must be measured with `forge build --sizes`.

**Reproduction**

Fixture: AutomaticFixture from test/AutomaticBinding.t.sol with asset IMD (18 decimals); requester deployed with maxPrice = 2 * FEE = 1e18; _open() with verdictReserve FEE = 0.5e18; _deliver; _commit; roll 8 blocks. Owner: setProtocol(intake, sixDecimalToken, 2e6, jobAction(), reviewAction()). intake.setPrice(reviewAction(), IMD, FEE + 1) so verdictFunding(askId) returns price 0.5e18 + 1 > reserve 0.5e18 (not funded, the case topUpReserve exists for). vm.prank(creator); automatic.topUpReserve(jobId, 1). Expected: reserve becomes 0.5e18 + 1 IMD base units (within the 1e18 IMD ceiling the job was opened under; no IMD ceiling was ever lowered) and reserved[IMD] == FEE + 1. Actual (reproduced with forge 1.8.3, test test/scratch/Proof_c6de9093b4e6.t.sol from the specialist): revert InvalidConfig(), because total 500000000000000001 > maxPrice 2000000. The same state makes retryVerdict(jobId, FEE) revert InvalidConfig after an Unanswered verdict (reserve 0.5e18 > 2e6). Inverse: deploy with a 6-decimal asset and cap 2e6, open a job, rotate to an 18-decimal asset with cap 2e18, then topUpReserve(jobId, 1e18) passes the cap check and reserves 1e18 base units (1e12 whole tokens) of the 6-decimal asset.

### 3. Info: Recorded Robinhood isolated callback gas (192,652 for the 22-cold-read ERC-1271 case) is not reproduced on Foundry 1.8.3, which measures 195,152; still under 200,000 but with 4,848 gas of margin and o

`docs/checks/audit-7db42bb7/README.md:81`

```
| Robinhood native mock | 130,509 | 175,570 | **192,652** |
```

Merged from audit_economics, audit_math and audit_flow, which reported the same measurement; reproduced. Not a code defect: a documentation/measurement discrepancy. Rerunning the README's command `forge test --isolate --match-contract 'AutomaticGasTest|ReviewReceiptGasTest|JobProtocolGasTest' -vv` on this tree with Foundry 1.8.3 reproduces the Ethereum and Local rows exactly (127,301 / 172,362 / 189,444 and 127,122 / 172,182 / 189,264) but every Robinhood figure is 2,500 gas higher than recorded: EOA 133,009, 5-of-7 ERC-1271 178,070, 22-cold-read ERC-1271 195,152. The constant 2,500 delta equals one cold-minus-warm account access (2,600 - 100): the fixture routes arbBlockNumber() at address(100) through vm.mockFunction to a storage-reading mock (test/helpers/WindowArbSysMock.sol), and Foundry 1.8.3 and the README's 1.8.5 charge that redirect differently. All 27 isolated tests pass, every figure stays under the 200,000 stipend, and `forge build --sizes` reproduces AutoHookJobRequester 24,468 runtime bytes (108 under EIP-170) and HookRequestCodec 16,966. The codec runtime pin 0xfb28d0...11ea matches the build (openJob succeeds in the suites). The point for the requester: neither number models the real ArbSys precompile cost, and the primary target chain's worst case sits within 5,000 gas of the ceiling under the stricter accounting, so production callback gas with the live ArbSys and the production ERC-1271 registry is a live-pilot requalification the README already calls for and that has not been performed. Suggested doc fix: record the Foundry version per row or re-measure on the verifier's release.

**Reproduction**

On this commit with forge 1.8.3 (cae51ad): `forge test --isolate --match-contract RobinhoodAutomaticGasTest -vv`. Expected per README table: 'Automatic 22-cold-read ERC1271 minimum forwarded callback gas: 192652' (EOA 130509, 5-of-7 175570). Actual: 'Automatic EOA minimum forwarded callback gas: 133009', 'Automatic cold 5-of-7 ERC1271 minimum forwarded callback gas: 178070', 'Automatic 22-cold-read ERC1271 minimum forwarded callback gas: 195152', all PASS. EthereumAutomaticGasTest (127301 / 172362 / 189444) and AutomaticGasTest (127122 / 172182 / 189264) match the README exactly. `forge build --sizes`: AutoHookJobRequester 24,468 runtime bytes, margin 108; HookRequestCodec 16,966.

### 4. Info: Cadence floors are documented policy assumptions, not code defects: the Ethereum bound is exact with zero spare blocks, a live Robinhood sample gives about 103 ms/block (about 2x margin), and live Int

`src/imd/automatic/HookRequestCodec.sol:84`

```
        if (block.chainid == 1 || block.chainid == 11155111) return 14_433;
```

Separation of documented assumptions from code defects, as the assignment requests; the code is correct against its stated policy and nothing here needs a code change. Verified against the code in this review: (a) full-horizon true and false acceptance on Ethereum, Sepolia, Robinhood native clock and local at exactly 8 + ceil(173100 s / cadence) blocks (14,433 / 3,462,008 / 173,108), with one further block rejected by `currentBlock - att.toBlock > r.maxWindowAgeBlocks` (line 129); preflight_automatic.window_policy computes the identical table and requires equality with the codec; constructor, setPanel, paymentHead and validateReview all enforce the per-chain minimum. (b) confirmReviewExpiry reverts at now == deadline + 300 + 86400 and succeeds one second later; no conforming answer can be admitted after that instant since expiresAt <= issuedAt + 1 day <= deadline + 300 + 1 day. (c) topUpReserve is requester-only, requires Delivered/None, committed candidate, uncancelled, untriggered ask, positive amount and total <= current maxPrice, pulls exactly the job's original asset, raises reserved[] so sweep cannot touch it, keeps job/ask/candidate identity and restarts the eight-block maturity; surplus and cancellation refunds remain pull-once. (d) verdictFunding quotes the snapshotted Intake/action/asset and SDK/UI treat an unavailable, zero or above-reserve quote as not ready. (e) codec.validateReview keeps the chain, question-hash, exact-window, age, timestamp, panel, requestId/panelJobId, 32-byte and canonical-bool checks while signatures, consumer domain, ERC-1271 caller context, epochs, replay and settlement stay in the requester; NotPassed stays terminal (retryVerdict and topUpReserve revert). Assumptions, not defects: Ethereum's 14,433 is exact at the 12 s slot time, so the bound can be reached but never exceeded within the horizon and there is no spare block; a future slot-time change needs a setPanel raise (owner trust assumption, documented). Robinhood (4663): the public RPC on 2026-10-19 returned block 92,364,676 at timestamp 1,792,387,154 and block 92,462,155 at 1,792,397,178, i.e. 97,479 native blocks in 10,024 s, about 102.8 ms/block, so the 50 ms floor holds today with roughly 2x margin and 3,462,008 blocks corresponds to about 4.1 days of acceptance against the 2.0-day signed horizon. Not performed in this review or in the repository's evidence: real Intake callback delivery and gas with the actual ArbSys precompile, the production ERC-1271 registry, action availability and pricing on the live Intake, and signer policy. These remain operator duties per docs/AUTOMATIC_BINDING.md. Coverage of this review: forge build and --sizes, the 27 isolated gas tests, suites Audit7db42bb7, AutomaticBinding, OracleWindowRegression and Audit2218802d (61 tests passing), `node --test test/*.test.cjs` (37 passing), `python3 -m unittest test.test_automatic_funding test.test_automatic` (18 passing). The full 660-test forge run, forge fmt --check, the vendored-source check and Slither/Mythril were not rerun here.

**Reproduction**

Boundary (reproduced with a scratch test extending test/Audit7db42bb7.t.sol): _chain(1); _prepared(); requestVerdict; attestation with issuedAt = deadline + 300, expiresAt = issuedAt + 1 days; vm.warp(expiresAt); _advance(14_425) gives head - toBlock == 14,433 and intake.complete returns true; with _advance(14_426) head - toBlock == 14,434 and intake.complete returns false (codec InvalidWindow). Expiry boundary: after _ready(), vm.warp(deadline + 300 + 1 days) then confirmReviewExpiry reverts DeadlineNotReached; vm.warp(deadline + 300 + 1 days + 1) then confirmReviewExpiry succeeds. Live sample: `curl -s https://rpc.mainnet.chain.robinhood.com -H 'content-type: application/json' -d '{"jsonrpc":"2.0","id":1,"method":"eth_getBlockByNumber","params":["0x582dc4b",false]}'` and the same for 0x5815f84; timestamps 1792397178 and 1792387154, 10,024 s apart for 97,479 blocks.

---

Judge's submission `b77b087442ba64ebcbaea8ac4ad3055eb4c517ed12fcd515b9f2129c5f73508c`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
