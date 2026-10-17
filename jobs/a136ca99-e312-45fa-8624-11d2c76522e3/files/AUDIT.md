# Audit report

> Audit commit b157921170c318f8eeee638b06025a81cf768c02 against base 575e8a8f74da581298a8527f493e9eab8a45901f. Focus on the job-callback correction and its interactions with existing protections. Review only: no source edits, deployment or paid Intake calls.
>
> Verify against https://imd.fun/docs/: onJobResult(bytes32,bytes32,string), registered selector, exact supplied resultHash, JobDelivered and JobResultURI. Independently test canonical protocol encoding, not just agreement between consumer and mock.
>
> Check Intake-only authorization, unknown IDs, duplicates, malformed data, late delivery and preservation of finalized NotPassed reviews. Examine untrusted URI decoding/rendering, ABI/readers and unchanged oracle callbacks. Check for regressions in payment accounting, caller price caps, replay protection and listing/ad escrow.
>
> Rerun Foundry, site/ABI and isolated cold-gas tests under pinned settings. Preserve all assertions, the 200k callback cap and 24,576-byte runtime limit. Verify docs/checks/job-protocol-tuple/ evidence independently. Report any SDK receipt-wait race separately from contract failures.
>
> Return reproducible findings with file/line, impact and tests. Distinguish material deployment blockers, disclosed owner powers and remaining live-Intake/oracle-mapping/signer-gas checks. Local tests are not proof of a working paid end-to-end service.

| | |
|---|---|
| Repository | https://github.com/identity-md-launches/launch-1811-build-technical-foundation-hooks.git |
| Commit | `b157921170c318f8eeee638b06025a81cf768c02` |
| Job | `a136ca99-e312-45fa-8624-11d2c76522e3` |
| Judged | 2026-10-17 02:35 UTC |
| Findings | 1 low · 3 info |

Four agents audited the code as it is at `b157921`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Low: Status page renders bidi/zero-width control code points in the result URI unescaped, allowing visual spoofing of the unverified location

`site/index.html:168`

```
        details = "Result URI (unverified): " + (decodeResultURI(l.data) || "(empty URI)");
```

decodeResultURI enforces canonical ABI layout, a 32 KiB bound and strict UTF-8, but valid UTF-8 includes the Unicode bidirectional overrides (U+202A-U+202E, U+2066-U+2069), zero-width characters (U+200B-U+200F, U+FEFF) and C0/C1 controls. The decoded string is written to td.textContent with no escaping and no CSS bidi isolation. textContent blocks HTML/script injection (already covered by the node tests), but not display reordering: a URI chosen by whoever controls the Intake writer or the result location can appear on the page as a different location than the bytes on chain. The contract is unaffected (the event carries the exact bytes); only the reader's display is. Not a deployment blocker. Fix (reader only): before display, map code points outside printable ranges (C0/C1 controls, U+200B-U+200F, U+202A-U+202E, U+2066-U+2069, U+FEFF) to visible escapes such as \u{202E}, and/or style the details cell with `unicode-bidi: isolate; white-space: pre-wrap; overflow-wrap: anywhere`; add a case to the 'history exposes URI only as unverified text' test asserting the rendered textContent contains no raw bidi/control code points. Merged from audit_flow; reproduced by the judge.

**Reproduction**

Input: a JobResultURI log whose string is "ipfs://QmSafe/result.json\u202E nosj.tluser/moc.live//:sptth" (data from `cast abi-encode 'f(string)' ...`), address = the requester, topics = [JobResultURI topic, request id]. Load the <script> of site/index.html in the same node vm harness test/requester-abi.test.cjs uses (window.ethereum returning that single log) and call history("", addr, id, ""). Expected: the details cell shows the bytes unambiguously (escaped or bidi-isolated). Actual (node v22.22.1, this tree): the cell's textContent is "Result URI (unverified): ipfs://QmSafe/result.json\u202E nosj.tluser/moc.live//:sptth" with the raw U+202E retained, so a browser renders the tail reversed and it reads as https://evil.com/result.json. Reproduction script: test/scratch/bidi.cjs (exits 1 listing 'U+202E' as retained).

### 2. Info: Measured URI ceiling under the 200k callback stipend is about 20,224 bytes on a cold job; larger URIs burn the single Intake attempt and the fee (documented, not a blocker)

`src/imd/HookJobRequester.sol:337`

```
        emit JobResultURI(requestId, uri);
```

onJobResult copies the whole calldata string into a LOG (8 gas per byte plus memory expansion) inside the Intake's fixed 200,000-gas one-shot try, and puts no bound on the URI length. When the stipend runs out the callback reverts, the Intake records delivered=false and keeps the fee, and the job stays Open until the requester expires it. This is already disclosed in docs/IMD_INTEGRATION.md ('An excessive URI can exhaust the fixed callback gas'; only 4,096 bytes measured) and the protocol specifies short URIs (ipfs://CID/result.json or the plane's /intake-results/:id), so it is not a deployment blocker and no source change is required. Recorded so the operator's pilot checklist pins the real ceiling instead of the page's 32 KiB display bound: cold, exact-200k delivery accepts 20,224 bytes and fails at 20,256 bytes (judge measurement in 32-byte steps, pinned 0.8.26/Cancun/200 runs, same result with and without --isolate). The two specialist measurements (18,432 fits / 20,480 fails; 16,384 fits / 20,480 fails) are consistent with this and are merged here. Optional: state the ceiling in the 'Callback gas budget' section of docs/IMD_INTEGRATION.md.

**Reproduction**

State: an Open job id allocated in an earlier transaction. Input: from msg.sender == intake, call onJobResult(id, keccak256('h'), string(new bytes(N))) with exactly 200,000 gas after vm.cool(requester), restoring state between trials. Expected per docs: unspecified ceiling. Actual: N = 20,224 succeeds (status Delivered); N = 20,256 and above runs out of gas, the job stays Open and MockIntake.reqs(id).settled is true (attempt consumed, fee retained). Run: `forge test --match-path test/scratch/CanonicalEncoding.t.sol --match-test testUriLengthCeilingUnder200k -vv` (logs 'largest URI bytes delivered under exact 200k (cold): 20224' and 'smallest ... that runs out of gas: 20256'); `--isolate` gives the same numbers.

### 3. Info: Protocol citation uses a non-existent anchor #what-comes-back; the published page's anchor is #intake-what-comes-back

`docs/IMD_INTEGRATION.md:27`

```
The [protocol's completion tuple](https://imd.fun/docs/#what-comes-back) is
```

The new 'Job result callback and URI' section, and docs/checks/job-protocol-tuple/README.md line 9, justify the callback correction by linking https://imd.fun/docs/#what-comes-back. The published page defines no element with id 'what-comes-back'; the section that states '(bytes32 requestId, bytes32 resultHash, string uri)' and 'resultHash is the keccak-256 of its bytes' has id 'intake-what-comes-back'. A reader following the citation lands at the top of a ~670 KB page. The tuple, hash semantics and 'Gas 200,000 for the call, once, inside a try' stated in the repository docs do match the page text (verified by the judge), so this is a citation defect only, not a protocol mismatch. Fix: change both links to https://imd.fun/docs/#intake-what-comes-back.

**Reproduction**

curl -sL https://imd.fun/docs/ -o docs.html; grep -o 'id="[^"]*comes[^"]*"' docs.html -> only id="intake-what-comes-back"; grep -c 'id="what-comes-back"' docs.html -> 0 (fetched 2026-10-17). Expected: the anchor in docs/IMD_INTEGRATION.md:27 and docs/checks/job-protocol-tuple/README.md:9 resolves to the tuple section. Actual: it does not resolve; only #intake-what-comes-back exists.

### 4. Info: SDK integration harness reads the transaction receipt once with no wait; misreports as 'local transaction failed' on any non-automining node (test harness only, not a contract defect)

`test/test_store_sdk.py:77`

```
        receipt = cls.rpc("eth_getTransactionReceipt", [tx_hash])
```

StoreSdkTest.send submits with eth_sendTransaction and immediately calls eth_getTransactionReceipt exactly once; a null receipt raises AssertionError('local transaction failed'), indistinguishable from a reverted transaction. Under the suite's own disposable Anvil (default automine) the receipt is available synchronously and all 10 tests pass on this tree (judge rerun: Ran 10 tests, OK), so no race was observed in the pinned configuration. The race appears only if the node does not automine (Anvil with --block-time or --no-mining, or any real RPC). This is pre-existing harness code, not changed by commit b157921, and it does not affect the job-callback change or any contract behaviour; it is reported separately from contract failures as the assignment asked. Fix (optional): poll eth_getTransactionReceipt until non-null with a bounded timeout, then check status. Merged from audit_economics and audit_math.

**Reproduction**

State: anvil --host 127.0.0.1 --port 18545 --chain-id 31337 --block-time 3. Input: eth_sendTransaction({from: accounts[0], to: accounts[0], value: 0x1, gas: 0x5208}) followed immediately by eth_getTransactionReceipt(hash). Expected by send(): a receipt with status 0x1. Actual (judge's 20-line urllib script, same sequence as send()): 'receipt immediately after send: None', then 'receipt after 4s status: 0x1', so send() would raise AssertionError('local transaction failed') for a transaction that mines successfully three seconds later. With the suite's default automine Anvil, python3 -m unittest discover -s test -p 'test_*.py' -v passes 10/10.

---

Judge's submission `952764ba5be9edd84c82c82037e7598aff98d9d9a44faa1212cdcb1cb8269413`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
