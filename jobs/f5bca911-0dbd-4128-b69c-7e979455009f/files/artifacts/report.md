# Why the "followers on all three lists" Oracle question was rejected, and how to word it so it passes

*Research date: 2026-09-27 (UTC). Tests were run against the live control plane at `https://api.imd.fun` between about 05:45 and 05:52 UTC.*

## Short answer

- **Why it failed (fact, reproduced):** The control plane's free quote step (`POST /requests/quote`) refuses this question with HTTP **422 `invalid_input` / `ambiguous_question`**. The message is:
  > "TypeSafe judged this question to have more than one reasonable reading (confidence 0.94). Pin the term, period, unit or rounding under definitions, or resubmit with allowAmbiguous: true to ask it as written."

  The same refusal came back for `answerType` `uint256` and `bool`, and for `evidence` `panel` and `chain`. Across repeated runs the confidence was 0.94–0.96.
- **Why the sentence "An ambiguous answer is allowed." didn't help (inference, strongly supported):** The ambiguity check reads that sentence as part of the question. It is not a switch. The override is a separate request **field**, `allowAmbiguous: true`. With that field set, the unchanged question got a valid quote (HTTP 201).
- **Wordings that pass (fact, tested):**
  1. Your original text plus the field `"allowAmbiguous": true` → **201 quoted**.
  2. A reworded, precise question: *"How many X (Twitter) accounts currently follow all three of @frenpetonbase, @0xSunflowerLand and @YieldFields_RH?"* with `answerType: "uint256"` → **201 quoted**. It passed both with and without `definitions`, and passed twice in a row.
- **Important caveat (inference):** Passing the check only means the network will **accept and charge for** the job. The quote says `"resultGuaranteed": false`. A full three-way follower-list intersection is much harder for the panel than the X questions that have worked before, so a paid request may well end `disagreed` with no signed answer (details below).

## 1. Evidence: what the check says

### 1.1 Reproduction of your rejection (fact)

I built the request the way the community client *imd-compose* does ([source](https://github.com/identity-md-launches/launch-185-imd-compose-repository-commit-repourl-ba), `server.py` → `/local/quote`). The body was `{requestKey, action:"oracle.request", input}` with a fresh random bearer token, and it was POSTed to `https://api.imd.fun/requests/quote`. The quote is free, and no payment was signed. Here is the input, with your question verbatim:

```json
{"v":1,"question":"How many followers appear on all three of the the followers lists of these twitter/x accounts; @frenpetonbase,  @0xSunflowerLand, and @YieldFields_RH? An ambiguous answer is allowed.",
 "chainId":1,"window":{"hours":24},"answerType":"uint256","evidence":"panel",
 "panelSize":5,"quorum":4,"validForSeconds":86400}
```

| Case | Change | Result |
|---|---|---|
| A | as above (`uint256`, panel) | 422 `ambiguous_question` (confidence 0.94; 0.96 on a rerun) |
| B | `answerType: "bool"` (the form's default) | 422 `ambiguous_question` (0.96; 0.94 on a rerun) |
| C | `uint256`, `evidence: "chain"` | 422 `ambiguous_question` (0.94; 0.96 on a rerun) |
| D | case A + `"allowAmbiguous": true` | **201 quoted** (order status `quoted`, 0.5 IMD, `resultGuaranteed:false`) |
| E | reworded question + `definitions` + `guards.minSources:1` | **201 quoted** |
| F | E + `toleranceBps: 1000` | **201 quoted** |
| G, H | reworded question alone, no `definitions` (run twice) | **201 quoted** both times |

The refusal is a semantic judgement by a component the API calls **"TypeSafe"**. Its confidence moved between identical runs, which suggests it is a model-based classifier, not a fixed rule (inference). It is **not** one of the structural limits that imd-compose checks locally. Those cover question length 1–2,000, panel size, quorum, window, and so on (`index.html`, the `oracle.request` validation block). Your request would have passed the local checks and then failed at the quote.

### 1.2 Why the original wording reads as ambiguous (inference)

The API's own hint names the fix: "Pin the term, period, unit or rounding". Several things in the original text allow more than one reading:

- "How many **followers** appear on all three … **followers lists**": this could mean accounts that follow all three, or something about the lists themselves. "Followers" vs "following" is a common mix-up; past successful X requests define it explicitly (e.g. "not the number of accounts this account follows", request `4642b9db…`).
- There is no time reference ("currently", "at observation time"), and follower lists change constantly.
- "An ambiguous answer is allowed" is itself open-ended: does it mean an estimate, a range, "unknown"? The answer type `uint256` can hold only one integer.
- Small issues: the doubled "the the" and the mixed "twitter/x".

### 1.3 The override field exists but is not in the community client (fact + inference)

- **Fact:** The API error text names `allowAmbiguous: true`, and the API accepted it (case D).
- **Fact:** imd-compose (commit `3a7087e`, 2026-09-26; documented limits "control plane 23659b86, 23 Sep 2026") has no `allowAmbiguous` anywhere in `index.html`. Its `fromOracle()` / `buildOracle()` copy only known fields: question, chainId, window, answerType, evidence, panelSize, quorum, validForSeconds, head, toleranceBps, definitions, guards, consumer. **If you paste JSON containing `allowAmbiguous` into imd-compose, the field is silently dropped, and the quote will still fail.**
- **Unknown:** I could not find public documentation of `allowAmbiguous` beyond the API's own error message. I also don't know which client you used to send the job.

## 2. Recommended wording (ready to paste)

### Option 1: preferred. A precise question with definitions (passes without the override)

```json
{"action":"oracle.request","input":{
 "v":1,
 "question":"How many X (Twitter) accounts currently follow all three of @frenpetonbase, @0xSunflowerLand and @YieldFields_RH?",
 "chainId":1,"window":{"hours":24},
 "answerType":"uint256","evidence":"panel",
 "panelSize":5,"quorum":4,"validForSeconds":86400,
 "toleranceBps":1000,
 "definitions":{
  "metric":"The number of distinct X accounts that currently follow all three of @frenpetonbase, @0xSunflowerLand and @YieldFields_RH (the intersection of their three follower lists). Followers only, not accounts they follow. Count each account once.",
  "account":"https://x.com/frenpetonbase, https://x.com/0xSunflowerLand, https://x.com/YieldFields_RH (handles as of the observation time).",
  "observation":"Use the freshest complete public follower lists; record UTC observation time and source URLs. If a full list cannot be retrieved, report inability rather than guessing; inaccessible data is not zero."},
 "guards":{"minSources":1}}}
```

This exact input (case F) was quoted successfully. `toleranceBps: 1000` lets panel answers within ±10% of each other count as agreeing. That is the closest the typed format gets to "an approximate answer is fine". Precedent: request `5f234bfc…` used tolerance and rounding and was attested, while an exact-count version of the same question (`a1adc1e4…`) ended `disagreed` at 5/8.

### Option 2: your wording as-is, with the override field

Keep your text and add `"allowAmbiguous": true` to the `input` object (case D). Delete the sentence "An ambiguous answer is allowed." because the field now does that job. You must send this with a client that passes the field through, such as your own script calling `/requests/quote`. imd-compose drops it (§1.3).

### Option 3: questions the panel is more likely to answer

These are my suggestions and I did **not** quote-test them. Questions about one account or one relationship match what has actually been attested:

- "Does @X follow @frenpetonbase, @0xSunflowerLand and @YieldFields_RH?" (`bool`, one account at a time), like the attested `c29c3948…` ("Is @blknoiz06 following @surfcoderepeat").
- "How many followers does @YieldFields_RH have?" (`uint256` with tolerance), like the attested `5f234bfc…`.

For a true three-list intersection, a `job.open` with the `research-report` skill fits better than an oracle. It can return a methodology, a range and caveats, which the oracle's single integer cannot.

## 3. Will the network actually answer it? (feasibility)

**Facts:**
- Follower counts at 2026-09-27 ~05:50 UTC, from `https://api.fxtwitter.com/<handle>`: @frenpetonbase **21,074**; @0xSunflowerLand **95,126**; @YieldFields_RH **27,421** (account joined 2026-08-28).
- Unauthenticated access to the lists: `https://x.com/frenpetonbase/followers` returns a JavaScript shell with no follower data. `https://api.x.com/2/users/by/username/frenpetonbase` returns HTTP 401. fxtwitter has no followers endpoint (404).
- In a past panel run (`9209aba6…`), a seat wrote: "X's direct list endpoint returned 403". That run ended `disagreed` (5 of 8 needed).
- All five X-related oracle requests among the latest 100 (`GET /oracle/requests?limit=100`) were about a single follower count, a single threshold, or a single follow relationship. 3 were attested and 2 disagreed. None asked for a list intersection.

**Inferences:**
- To answer exactly, each seat would need all ~143,600 follower entries across the three lists and would then intersect them. Without authenticated X API access, that is unlikely to be possible. Seats would probably have to report inability or give very different estimates, so the panel would likely end `disagreed`. The 0.5 IMD is a fee for admission (`"purchase":"action-admission","resultGuaranteed":false`), so it would be spent either way.
- The ceiling is known: the answer can be no more than 21,074, the smallest list.

## 4. What is still unknown

- I did not pay for or submit any request. Whether the panel would actually reach quorum on Option 1 or 2 is untested.
- I don't know exactly how TypeSafe works (model, threshold, whether `definitions` are weighted). Its confidence changed between identical runs, so a borderline question may pass on one try and fail on the next.
- Beyond its name in the error message, I don't know whether `allowAmbiguous` changes how the panel answers, or only skips the pre-check.
- I don't know which client you used and what error text it showed you. If it said anything other than `ambiguous_question`, a different check may have fired (for example, the published capabilities give `minPanelSize: 5` for `oracle.request`, while imd-compose allows 2).

## Sources

- Live API (primary): `https://api.imd.fun/requests/capabilities` (limits `oracle.request` minPanelSize 5, maxPanelSize 100); `POST https://api.imd.fun/requests/quote` (tests A–H above); `https://api.imd.fun/oracle/requests?limit=100` and `/oracle/requests/{id}` for `c29c3948-dcd3-4cb1-a6e0-71e1589f31b7`, `9209aba6-a2e2-48a1-9345-1801045990e4`, `5f234bfc-bec8-4d84-b4d1-ae97eb7dc74c`, `4642b9db-fc17-44eb-8b41-c3837e22acc3`, `a1adc1e4-759b-40d0-9b7a-51f8e0745714`.
- imd-compose community client: https://github.com/identity-md-launches/launch-185-imd-compose-repository-commit-repourl-ba (commit `3a7087ea218c729c51949788805ddb71f9e2b57d`): README (quote returns 422 with problems), `index.html` (local validation, `fromOracle`/`buildOracle`), `server.py` (quote proxy).
- Background: https://github.com/mtezy/imd-writeup (oracle.request = "a typed question answered by a panel", 0.5 IMD), https://github.com/johnfreeman777/imd-node-guide (oracle work runs on the small model at low effort).
- Follower counts: `https://api.fxtwitter.com/frenpetonbase`, `/0xSunflowerLand`, `/YieldFields_RH` (a third-party mirror, not X itself).
