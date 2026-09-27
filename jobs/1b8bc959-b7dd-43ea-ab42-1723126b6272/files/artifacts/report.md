# A keychain-sized Fren Pet viewer: what it would take

*Research date: 2026-09-27. Everything about Fren Pet's API, contracts and client code was observed live on that date. None of it is a documented, stable interface.*

## How to read this report

Each claim carries one of these labels:

| Tag | Meaning |
|---|---|
| **[F-doc]** | Fact from a primary published source (official docs, vendor spec page). The link follows the claim. |
| **[F-obs]** | Fact I observed directly: a live API response, an on-chain call, or the shipped pet.game JavaScript/CSS. The method is given so it can be reproduced. |
| **[F-2nd]** | Fact from a secondary source (press, wiki, forum). Treat with more caution. |
| **[I]** | My inference or engineering judgement. It is not verified. |
| **[?]** | Unknown or uncertain. |

---

## 1. Short answer

1. **You don't have to build it from scratch.** Off-the-shelf ESP32 boards with a small screen and Wi-Fi already exist at keychain size, and they cost roughly $10–$25. Examples are the M5Stack AtomS3 (24 × 24 mm) and M5StickC Plus2 (48 × 24 mm, with battery, RTC and buzzer), and the Waveshare 1.28″ round board. They can fetch pet data over Wi-Fi when you ask them to, then render the pet locally from a clock. The remaining hardware work is mostly an enclosure and a battery choice. **[F-doc]** for specs (§4), **[I]** for fitness.
2. **Commercial Tamagotchis can't realistically be repurposed.** The original P1 runs from mask ROM. The Tamagotchi Uni has an ESP32 Wi-Fi module, but its firmware is closed and I found no public custom-firmware route (§4.3).
3. **Fren Pet's data model suits an offline device well.** The game is on the Base chain. Each pet has 3-number on-chain DNA that never changes, plus a birth timestamp and an *absolute* starvation timestamp. With those three values the device can compute appearance, growth stage and the "time until death" countdown from its own clock alone. One fetch per feeding (at most every ~3 days) is enough to keep the countdown correct (§2, §3).
4. **The main open questions are not about hardware.** They are about permission to use the artwork, the stability of undocumented APIs, the exact rules behind "hungry/starving/dying", and the product scope (§6).

---

## 2. What Fren Pet is, and which data identifies a pet

### 2.1 Game facts (documentation)

- Fren Pet is an idle pet game on **Base**, an Ethereum L2. You feed, train and battle pets. **[F-doc]** [docs.frenpet.xyz](https://docs.frenpet.xyz/)
- The game runs at **pet.game**. The page title is "Fren Pet", and the web-app manifest says `"name": "FrenPet"`. **[F-obs]** (fetched `https://www.pet.game/` and `/manifest.json`)
- Feeding resets the pet's **Time of Death (TOD) to 3 days**. A pet that isn't fed goes into a **7-day hibernation**. **[F-doc]** [Gameplay](https://docs.frenpet.xyz/gameplay/)
- Pets "start as an EGG and advance to its full reveal as the time passes". Each pet has "**onchain DNA composed of 3 parameters: legs, head and ears**, it is randomly decided on mint and can't be changed". **[F-doc]** [V2 blog, 9 Nov 2023](https://docs.frenpet.xyz/blog/v2/)
- The V2 contracts on Base use a Diamond (EIP-2535) at `0x0e22b5f3e11944578b37ed04f5312dfc246f443c`. The pet NFT is at `0x5b51Cf49Cb48617084eF35e7c7d7A21914769ff1`. **[F-doc]** [Contracts](https://docs.frenpet.xyz/contracts)
- **Outdated documentation:** the V2 blog names `api.frenpet.xyz/graphql` as the public API. On 2026-09-27 that hostname served a TLS certificate for `*.cloudwaysapps.com` (a hostname mismatch), so the documented endpoint is effectively dead. **[F-obs]** (`curl -v`)

### 2.2 What the live system actually exposes (observed)

- **GraphQL indexer:** the pet.game client uses `https://api.pet.game`. It accepts unauthenticated POSTs and allows introspection. The `pet(id)` type includes these fields:
  - `dna` (string, e.g. `"12-0-3"`)
  - `createdAt`
  - `timeUntilStarving`
  - `status`
  - `level`, `score`
  - `attackPoints`, `defensePoints`
  - `shieldExpires`
  - `owner`, `name`

  `_meta` showed the indexer at Base block 51,847,700, roughly 5 seconds behind wall-clock time. **[F-obs]**
- **`timeUntilStarving` is an absolute Unix timestamp, not a duration.** Pet #18594 returned `1790640851`, which is about 43 hours after the time of the query. Pet #84052, minted on the day of the query, had `timeUntilStarving − createdAt = 259,200 s`, exactly 3 days. That matches the documented TOD. **[F-obs]**
- **On-chain fallback:** a plain `eth_call` to the Diamond over the public RPC `https://mainnet.base.org` works without an API key:
  - `getStatus(uint256)` (selector `0x5c622a0e`) returned `0` ("happy") for the sampled pets.
  - `getInfos(uint256)` (selector `0x46c27e8c`) returned the same `timeUntilStarving` and birth time as the indexer.

  **[F-obs]** I did **not** fully decode the `getInfos` struct, so I haven't confirmed where the DNA sits in it. **[?]**
- **Accessories** come from a different endpoint, `https://www.pet.game/api/equip/<id>`. It returns `hat`/`mask`/`glasses` item ids. Some pets also have an **AI-generated hat**, which is a PNG hosted on Vercel Blob with its own position and size. **[F-obs]**

### 2.3 How the web client turns data into a picture

Everything below comes from the shipped pet.game JS/CSS bundles, downloaded 2026-09-27. **[F-obs]**

- **Status codes:** `["happy","hungry","starving","dying","dead","hibernating","training"]`, indexed 0–6.
- **DNA index 0** selects the sprite family:
  - `< 6` → the original "ogpet" layered sprite, where index 0 also selects the ears layer.
  - `6..13` → `cat, sheep, pepe, penguin, dragon, monkey, panda, dog`.
- **DNA index 1** selects the head sprite and **index 2** the legs. So the documented "legs, head, ears" list is not in index order. The client uses `[ears/species, head, legs]`.
- **Growth stage** = `floor((now − birth) / 86400)` days. Days 0–4 map to stages A–E (child/toddler, with parts appearing progressively). Day 5 and later is stage F (adult). This is pure clock math.
- **"Needs hibernation"** is shown when `timeUntilStarving ≤ now` and the pet isn't already hibernating (status 5). The client also defines a constant of **604,800 s (7 days)** that it adds to `timeUntilStarving` as the revival deadline.
- **Sprites are small pixel art:**
  - Newer species are 32 px-tall strips. `panda.png` is 704 × 32, about 22 frames of 32 × 32 in 2–3 colours.
  - The layered "ogpet" parts are 246 × 96 two-frame strips of about 1–2 KB each.

  **[F-obs]** (PNG headers read, and images viewed)

**What this means for a device [I]:** you need about 40 bytes of *static* identity (id, DNA triple, birth timestamp) plus one *changing* timestamp (`timeUntilStarving`). From those you can compute species, parts, growth stage, the countdown and the revival deadline locally. The pixel art already matches tiny low-colour screens: 32 × 32 frames scaled 3–4× fill a 128 × 128 display. A full sprite set is probably a few hundred KB, which fits easily in the 8–16 MB flash of the boards in §4.

`tools/fetch-pet.mjs` in this repo reproduces all of this. It prints the compact "pet card" (433–548 bytes as minified JSON for the pets tested) that a device would store.

---

## 3. What can be computed locally, and what goes stale

| Readout | Local from clock + stored data? | Notes |
|---|---|---|
| Species / parts / colours | **Yes**, forever | DNA is immutable on mint **[F-doc]** |
| Growth stage (egg → adult) | **Yes** | `days since birth`, capped at 5 **[F-obs]** |
| "Time until starving" countdown | **Yes, until the owner feeds** | Feeding moves the timestamp 3 days forward **[F-doc]**. Stale data only makes the countdown *pessimistic*, never wrong in the dangerous direction **[I]** |
| "Needs hibernation / revive by" | **Yes** | `timeUntilStarving` and `+7 d` **[F-obs]** |
| happy / hungry / starving / dying | **Partly** | The contract computes these. I did not find the time thresholds in client code **[?]**. You could approximate by time left, but it might disagree with the game |
| Training, shield, attacks, score, level, ATK/DEF | **No** | These change with gameplay and other players' attacks. Show them as "as of last sync" |
| Accessories / AI hat | **Snapshot only** | The AI hat is a remote PNG that needs downloading and scaling **[F-obs]** |
| Death / burn / transfer | **No** | Only a refresh can detect these |

**Recommended model [I]:**
- Store `{id, dna, bornAt, timeUntilStarving, shieldExpires, accessories, fetchedAt}`.
- Render entirely from an RTC.
- Show a "last synced X h ago" badge.
- Sync on a button press, or at most around daily.

Sync paths, in rough order of simplicity:
1. Wi-Fi → `api.pet.game`.
2. Wi-Fi → Base public RPC. This is more durable because it depends only on the chain.
3. Phone → BLE push, where a phone app or web page does the fetch.
4. Manual entry of the DNA triple plus birth date. This covers **appearance and growth stage only**. The countdown would need the last feeding time typed in too, which is awkward on 1–3 buttons.

---

## 4. Existing hardware options

### 4.1 Ready-made ESP32 boards, keychain size or close to it

| Device | Size | Screen | Radio | Battery / RTC | Source |
|---|---|---|---|---|---|
| M5Stack **AtomS3** | 24 × 24 × 12.9 mm, 6.9 g | 0.85″ IPS 128 × 128 | Wi-Fi, BLE (ESP32-S3) | **No battery**, USB-C only | [docs.m5stack.com](https://docs.m5stack.com/en/core/AtomS3) **[F-doc]** |
| M5Stack **StickC Plus2** | 48 × 24 × 13.5 mm | 1.14″ TFT 135 × 240 | Wi-Fi (ESP32-PICO-V3-02, 8 MB flash/2 MB PSRAM) | **200 mAh** battery, **BM8563 RTC**, 3 buttons, buzzer, IMU | [docs.m5stack.com](https://docs.m5stack.com/en/core/M5StickC%20PLUS2) **[F-doc]** |
| Waveshare **ESP32-S3-LCD-1.28** | ~9 g board | 1.28″ **round** IPS 240 × 240 | Wi-Fi + BLE 5 | LiPo charge header, IMU; **$15.99** | [waveshare.com](https://www.waveshare.com/esp32-s3-lcd-1.28.htm) **[F-doc]** |
| LilyGO **T-Display-S3** | larger (stick) | 1.9″ 170 × 320 | Wi-Fi + BLE 5 | JST battery connector; listed at $9.04 (sold out when checked) | [lilygo.cc](https://lilygo.cc/products/t-display-s3) **[F-doc]** |
| SQFMI **Watchy** | wristwatch | 200 × 200 **e-paper** | ESP32-S3 Wi-Fi/BLE | Open-source hardware (OSHWA), Arduino/MicroPython | [watchy.sqfmi.com](https://watchy.sqfmi.com/) **[F-doc]** |

**Assessment [I]:**
- The **M5StickC Plus2** is the closest to "flash it and it works". It already has a battery, a real-time clock, buttons and a buzzer, which is everything a Tamagotchi needs. At 48 mm it is keychain-ish rather than egg-sized.
- The **AtomS3** has the right size but needs a battery added.
- The **round Waveshare board** gives the most "toy-like" look inside a custom 3D-printed shell.
- An **e-paper** device (Watchy-class) gives weeks of battery life and suits a mostly static pet, at the cost of animation.

### 4.2 Other programmable pocket devices

- **Arduboy Mini:** about 50 × 35 mm and keychain-sized, with a 128 × 64 mono OLED and a 16 MHz ATmega32u4. **It has no radio**, so pet data could only be entered by hand or at flash time. It is also powered over USB-C from an external battery, according to press coverage. **[F-2nd]** [Hackaday](https://hackaday.com/2022/12/22/arduboy-mini-is-a-fresh-take-on-an-8-bit-favorite/), [Electronics-Lab](https://www.electronics-lab.com/meet-the-new-arduboy-mini-the-size-of-a-coin-pocket/)
- **Flipper Zero:** 128 × 64 mono screen, BLE but **no Wi-Fi**, 100 × 40 × 26 mm. It's too big for a keychain but workable as a prototyping target with phone-over-BLE sync. **[F-doc]** [docs.flipper.net](https://docs.flipper.net/zero/development/hardware/tech-specs)
- **Pebble (Core Devices):** PebbleOS is now 100% open source. Pebble Time 2 shipping was about 80% fulfilled in July 2026, and Round 2 was targeted to ship by the end of September 2026. Apps can use the phone for network access. It's a wrist device, not a keychain. **[F-doc]** [repebble.com, July 2026](https://repebble.com/blog/pebble-mega-update-july-2026) · **[F-2nd]** [gadgetsandwearables](https://gadgetsandwearables.com/2025/11/24/pebble-open-source/)

### 4.3 Real Tamagotchi hardware

- **Original P1 (1996):** it can be *emulated*. ArduinoGotchi runs the TamaLib emulator on an Arduino Uno with a 128 × 64 SSD1306 OLED, 3 buttons and a buzzer, but you have to supply the copyrighted ROM yourself. That shows a 3-button, 128 × 64 layout is enough for a virtual pet, but emulation doesn't help render Fren Pets. **[F-doc]** [github.com/GaryZ88/ArduinoGotchi](https://github.com/GaryZ88/ArduinoGotchi)
- **Tamagotchi Uni:** community sources report that its Wi-Fi module is an ESP32, and that reverse-engineering so far covers network traffic, not custom firmware. **[F-2nd]** [Tamagotchi Wiki FAQ](https://tamagotchi.fandom.com/wiki/User_blog:NightBladeSequel/Tamagotchi_Uni_FAQ), [GBAtemp thread](https://gbatemp.net/threads/tamagotchi-uni-research-hacking.636515/). **[?]** I found no public way to run custom code on it. **[I]** Treat it as not viable.
- **Cheap "virtual pet keychain" clones:** in my experience these use one-time-programmable or mask-ROM MCUs with segment or tiny dot-matrix screens. **[I]**, not source-verified. Swapping the board inside the *shell* is possible, but that is effectively a custom build.

### 4.4 Build-from-scratch path, if a true egg-sized device is wanted [I]

Parts: an ESP32-C3/S3 module, a 0.96–1.3″ OLED or a 1.54″ e-paper panel, a 100–300 mAh LiPo, a charger IC, 3 buttons, a piezo buzzer, and a custom PCB in a 3D-printed or injection-moulded shell. The ESP32-S3 has an RTC in its low-power domain, but a dedicated RTC chip (as on the StickC Plus2) keeps better time during deep sleep. This is a normal hobbyist project. The risk is in battery life, drift and enclosure, not feasibility.

---

## 5. Suggested minimal build [I]

1. **Hardware:** M5StickC Plus2 (no soldering) or a round ESP32-S3 board in a printed shell.
2. **Firmware:** Arduino/ESP-IDF with LVGL or TFT_eSPI. Store the sprite sheets in flash as indexed-colour arrays.
3. **Pairing:** a first-boot captive portal (phone connects to the device's Wi-Fi) where the user enters a **pet id**, or an **owner address** so the device can list the owner's pets via the observed `pets(where:{owner})` query. Wi-Fi credentials are entered in the same step.
4. **Sync:** button-triggered, or once a day if on Wi-Fi. Use `api.pet.game` GraphQL, falling back to Base RPC `getInfos`/`getStatus`, then deep sleep.
5. **Offline logic:**
   - stage = f(now − bornAt)
   - countdown = timeUntilStarving − now
   - "revive by" = timeUntilStarving + 7 d
   - buzzer alert at, say, 12 h remaining
   - "stale" badge after 24 h without sync
6. **Manual fallback:** enter the DNA triple and birth date on the buttons. This gives an appearance-only mode.

---

## 6. Questions still to answer

**Permission and legal**
1. Are you allowed to reproduce Fren Pet artwork on a device, especially one that is **sold**? The docs link brand assets but state **no licence terms**. **[F-doc]** [Branding](https://docs.frenpet.xyz/branding). `pet.game/terms` and `/tos` returned 404. **[F-obs]** You would need explicit permission from the team.
2. Would the team sanction or officially support a hardware companion, for example a stable public endpoint or a sprite pack?

**Data and API**

3. How stable is `api.pet.game`? It's undocumented, and the documented `api.frenpet.xyz` is already dead. Could the game migrate chains or contracts? The chain-RPC fallback reduces but doesn't remove this risk.
4. What exact on-chain rules produce hungry → starving → dying? These are needed if the device should show those moods offline. **[?]**
5. What is the exact layout of the `getInfos` struct, including where the DNA sits, if you want to depend only on the chain? **[?]** (partly probed)
6. How should accessories be handled: item-id sprites (hat/mask/glasses) and **AI-generated hats** (arbitrary remote PNGs)? Options are downloading and dithering them, ignoring them, or asking the team for a small-size variant.
7. Are the species list (ids 6–13) and the "ogpet" part counts final, or will new species appear? New species would need firmware or sprite updates over the air.

**Product and UX**

8. Is the device **view-only**, or should it trigger actions such as feeding? Actions need a wallet signature. That brings in key storage on the device, or a phone round-trip, plus security review, which is a much larger scope. **[I]**
9. How do you identify the pet: pet id, wallet address (multiple pets), or QR code/NFC tap from the phone? Should you support one pet or several?
10. What screen type do you want? Colour LCD gives animation but lasts about 1–2 days on 200 mAh when awake. E-paper gives weeks but little animation. What battery life target? **[I]**, not measured.
11. How much clock drift is acceptable? Without an RTC chip or occasional NTP sync, drift makes the countdown less accurate.
12. How big is the full sprite asset set and what licence covers it? I sampled only a few files.
13. If it's sold as a product: FCC/CE (a pre-certified module helps), battery shipping rules, and the unit cost of the enclosure. **[I]**

---

## 7. Method and limits

- **What I checked directly:**
  - live GraphQL introspection and queries against `api.pet.game`
  - `eth_call` against Base mainnet
  - the downloaded pet.game JS/CSS bundles and sample sprite PNGs
  - the `/api/equip` endpoint

  All on 2026-09-27. Pet ids sampled: 0, 15770, 18594, 84052.
- **Not done:**
  - no hardware was built or measured, so battery and drift figures are estimates
  - the `getInfos` struct was not fully decoded
  - I didn't extract mood thresholds
  - I didn't contact the Fren Pet team about licensing
  - vendor prices and stock change often
- **Sources:** product and spec claims come from vendor or official pages where possible. The Tamagotchi Uni and Arduboy Mini details are from secondary or community sources, and are labelled that way.
- **No independent review:** this report was produced and checked by a single agent. A structural pass means the file exists in scope. It does not certify that the research is correct.
