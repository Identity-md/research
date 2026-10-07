# Fren Pet widget implementation and evidence

Checked on 2026-10-07 UTC. This report addresses whether an ID-selected, borderless
widget can show the pet view with animated sprites and a timestamp-based TOD.

## Result

Implemented a static widget in `index.html`, `app.js`, `model.mjs`, and `style.css`.
Users enter a numeric pet ID; `?pet=1&embed=1` hides the selector for embedding.
The displayed view contains name/ID, timer, animated pet, state, level, attack,
defense, and points. It has a transparent background and no view border.
No runtime libraries or build downloads are required. Local sprite assets and
sprite CSS are included. Live data still requires the external game API.

This is a useful current-game implementation, **not a verified exact reproduction
of the historical pet.fun/mypet petview**. The historical page could not be inspected.

## Observed facts and attributable sources

- A direct HTTPS GET of [pet.fun](https://pet.fun/) returned 200 with server
  `DPS/2.0.0` and a GoDaddy frame-ancestor CSP. A GET of
  [pet.fun/mypet](https://pet.fun/mypet) returned 404. These are observations from
  this environment on the date above, not a claim about all past or future versions.
- [Fren Pet's overview](https://fren-pet-docs.vercel.app/) identifies Fren Pet as a
  Base game and points to frenpet.xyz for installation. The retrieved
  [frenpet.xyz](https://frenpet.xyz/) HTML has title `Fren Pet`.
- The current application's
  [data/utility bundle](https://frenpet.xyz/_next/static/chunks/3865-bb53b90f245d91a1.js)
  defines the GraphQL endpoint `https://api.pet.game`, queries `pets` with `id_in`,
  and maps DNA values 0–5 to original pets and 6–13 to cat, sheep, pepe, penguin,
  dragon, monkey, panda, and dog. Its age helper uses elapsed whole days. Its
  hibernation helper adds 604800 seconds to `timeUntilStarving`.
- A POST to [the game API](https://api.pet.game) with the query saved in
  `evidence/api.json` successfully returned pet #1 and its name, DNA, timer,
  stats, owner, and score. The response included `access-control-allow-origin: *`.
  Introspection confirmed `dna` is a string, `createdAt` and
  `timeUntilStarving` are integer fields. The live schema does **not** include
  `timePetBorn`; the implementation uses `createdAt`.
- The
  [sprite component bundle](https://frenpet.xyz/_next/static/chunks/330-55d886b379673382.js)
  selects sprite layers by DNA, age, and state. Its countdown renderer displays
  days/hours/minutes/seconds and `RIP` at completion.
  [The game's sprite CSS](https://frenpet.xyz/_next/static/css/8f103b4fc1096fcb.css)
  uses stepped, repeating background-position animation. Relevant pet rules and
  images are bundled locally; exact image source URLs appear in
  `vendor/sources.json`. The original ghost SVG is also included.
- The current
  [pet page bundle](https://frenpet.xyz/_next/static/chunks/app/(pages)/page-41ffdd1e97b4fc5a.js)
  passes `timeUntilStarving * 1000` to its countdown, or its hibernation helper's
  deadline. [Gameplay documentation](https://fren-pet-docs.vercel.app/gameplay)
  describes feeding every three days and a seven-day hibernation period.

## Implementation decisions and inferences

- The current endpoint is inferred to be the appropriate successor integration
  because the current Fren Pet application itself uses it. No historical domain
  migration or ownership continuity was independently established.
- `createdAt` is used as the birth timestamp for daily sprite growth. This is an
  inference from schema naming and the game's elapsed-days helper; equivalence
  to the unavailable `timePetBorn` field is not independently proven.
- Timer display is calculated afresh from an absolute deadline and `Date.now()`;
  it does not decrement a mutable counter. This avoids accumulated timer drift
  when callbacks are delayed. It uses ceiling seconds to avoid showing RIP before
  the deadline. A wrong local system clock can still produce a wrong countdown.
- At feeding expiry, nonburned pets move to a `needs-hibernation` display with a
  seven-day revive deadline, following the current game's helper. The label changes
  to “Revive before”; it is not a new feeding allowance.
- The widget selects only passive pet information. Game navigation, wallet,
  feeding, battles, and purchase actions are omitted. DOM text is set using
  `textContent`; rapid ID switching aborts obsolete requests.

## Local verification

The six dependency-free tests in `tests/model.test.mjs` passed using Node v24.21.0.
They cover input validation, DNA/data validation, fixed-point score precision,
wall-clock countdown and expiry, hibernation/burn/training states, and successful,
missing, malformed, and failed API responses. `node --check` passed for app.js and
model.mjs. Live API lookup for pet #1 succeeded. These checks are self-performed;
no independent reviewer or verifier has certified behavior.

A headless Chrome 155 browser check against the locally served widget passed:
live pet #1 lookup, countdown text changing after elapsed time, sprite group
transform changing between animation frames, zero-width pet-view border,
unknown-ID error with the old pet hidden, recovery by entering #1, selector hidden
in embed mode, and no JavaScript exceptions. A screenshot is saved as
`evidence/widget.png`. The test browser and system-library scaffolding were kept
outside the deliverable; the widget does not depend on them. An initial screenshot
had no text because the test environment lacked font configuration; after adding
temporary browser font configuration, the screenshot and text assertions succeeded.
The widget also includes a local Inter Latin webfont and its upstream license.
These browser observations cover pet #1, not every possible DNA/equipment state.

## Uncertainty and unanswered questions

- Exact historical petview layout and field membership remain unknown because
  pet.fun/mypet returned 404. Pixel-perfect fidelity is not claimed.
- Equipped accessories, generated hats, rare-pet overrides, rewards, and game
  interactions are not implemented. Base DNA sprites are supported.
- Public API uptime, future schema stability, indexer lag, rate limits, and
  permission to redistribute artwork have not been guaranteed or established.
  The copied assets retain their original owners' rights.
- Offline verification can inspect source and run logic tests. It cannot fetch
  a user's current pet. No invented or cached pet is presented as live data.
- A path/byte verifier establishes delivery integrity only; it does not establish
  correctness of these observations or certify browser behavior.
