# Setting up premium media tools for an IMD/identity-md worker

**Skills covered:** `create video`, `create audio`, `create image`
**Research date:** 1 October 2026. All prices and model names were read from official provider pages on this date.
**Audience:** Seat holders who are new to connecting AI agents (Claude Code, Codex, or similar) to paid generation APIs.

---

## How to read this report

Each claim is labeled with one of these tags:

| Tag | Meaning |
|---|---|
| **[Fact]** | Stated on an official provider page. The source is linked inline and again in the final list. |
| **[Inference]** | My reasoning from the official facts, such as why one option ranks above another. |
| **[Uncertain]** | I could not fully verify it, or it is likely to change soon. |

**Currency.** Providers publish prices in USD. GBP figures are my conversions using the European Central Bank reference rates for **1 Oct 2026** (EUR 1 = USD 1.1298 = GBP 0.85373), which gives **USD 1 ≈ GBP 0.7556** ([ECB daily rates](https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml)). None of the four providers publish a GBP price list on the pages I checked. Your card statement may differ because of your bank's FX margin. Taxes such as UK VAT may be added (for example, ElevenLabs says "Prices exclude all taxes, levies and duties").

**Why everything here is an API.** A worker agent cannot sign in to a consumer website for you. It needs a **developer API** that it can call with a key. Every recommendation below is the provider's *developer/API* product, not its consumer app subscription. Consumer plans such as ChatGPT Plus, Gemini app plans, the Runway web app or the ElevenLabs web Studio generally do **not** give an agent API access. ElevenLabs is the exception: its subscription plans also cover API usage.

---

## Summary: the two picks per skill

| Skill | Pick 1 | Pick 2 |
|---|---|---|
| **create video** | Google Gemini API: **Gemini Omni Flash** / **Veo 3.1** *(Multi)* | **Runway API (Runway Dev)**: Gen-4.5, Aleph 2.0, plus hosted Seedance/Veo *(Multi)* |
| **create image** | OpenAI API: **GPT Image 2.5** (Sunburst / Flare) *(Multi)* | Google Gemini API: **Nano Banana Pro** (`gemini-3-pro-image`) *(Multi)* |
| **create audio** | **ElevenLabs API**: voice, music, sound effects *(Audio)* | Google Gemini API: **Gemini 3.8 Flash TTS** + **Lyria 3.5** music *(Multi)* |

Three of the four providers produce more than one kind of media, so they are described once in the **Multi** section. ElevenLabs is the only audio-only pick.

**Simplest setup for beginners [Inference].** One Google Gemini API key covers all three skills at premium quality. Add ElevenLabs if the job needs top-end voice work, and add Runway if it needs professional video delivery formats (ProRes/HDR).

> **Important time-sensitive finding [Fact].** OpenAI's Sora 2 video models and Videos API were **shut down on 24 September 2026**. OpenAI states that "no one-to-one replacement API is available" ([OpenAI video guide](https://developers.openai.com/api/docs/guides/video-generation), [OpenAI deprecations](https://developers.openai.com/api/docs/deprecations)). Older guides that recommend Sora for agent video work are now out of date. OpenAI is therefore listed here for image and audio only.

---

# 1. MULTI (tools covering more than one media type)

## 1.1 Google Gemini API (video + image + audio + music)

### Why it was chosen [Inference, based on the facts below]
- It is the only single account and key that covers **all three skills** with current flagship models: video (Gemini Omni Flash, Veo 3.1), image (Nano Banana Pro / Nano Banana 2), speech (Gemini 3.8 Flash TTS) and music (Lyria 3.5).
- **[Fact]** Google calls Gemini Omni Flash its default video model, citing "superior video coherence, multi-input reasoning (supporting text, images, audio, and video inputs simultaneously), character consistency, factual accuracy, and multi-turn conversational editing". It also says to use Veo 3.1 for "scene extension, last-frame control" ([Gemini video overview](https://ai.google.dev/gemini-api/docs/video)).
- **[Fact]** Veo 3.1 generates video **with native audio** and offers 4K output on the Standard and Fast tiers ([pricing](https://ai.google.dev/gemini-api/docs/pricing)).
- **[Fact]** Google publishes official coding-agent support: a Gemini Docs MCP server and installable "Gemini API Skills". It names Claude Code explicitly ([coding agent setup](https://ai.google.dev/gemini-api/docs/coding-agents)). This helps an agent use the current API correctly.
- **[Fact]** On the free tier, the pricing page marks content as "Used to improve our products: Yes". On the paid tier it says "No" ([pricing](https://ai.google.dev/gemini-api/docs/pricing)). **For premium/client work, use the paid tier.**

### Costs [Fact: Gemini API pricing page, 1 Oct 2026]
**Video** (charged per second of generated video; audio included by default; no free tier)

| Model (ID) | USD | GBP (≈) |
|---|---|---|
| Gemini Omni Flash (`gemini-omni-1.1-flash`), 720p | ≈ $0.10 / sec (token-billed: $17.50 per 1M video output tokens, 5,792 tokens/sec) | ≈ £0.076 / sec |
| Veo 3.1 Standard (`veo-3.1-generate-preview`), 720p/1080p | $0.40 / sec | £0.30 / sec |
| Veo 3.1 Standard, 4K | $0.60 / sec | £0.45 / sec |
| Veo 3.1 Fast (`veo-3.1-fast-generate-preview`), 720p / 1080p / 4K | $0.10 / $0.12 / $0.30 per sec | £0.076 / £0.091 / £0.23 per sec |
| Veo 3.1 Lite (`veo-3.1-lite-generate-preview`), 720p / 1080p | $0.05 / $0.08 per sec | £0.038 / £0.060 per sec |

*Worked example [Inference]:* an 8-second 1080p clip on Veo 3.1 Standard costs **$3.20 (≈ £2.42)**. On Omni Flash at 720p it is about **$0.80 (≈ £0.60)**. Agents often need several attempts per usable clip, so budget a multiple of these figures.

**Image**

| Model (ID) | USD per image | GBP (≈) |
|---|---|---|
| Nano Banana Pro (`gemini-3-pro-image`), 1K/2K | $0.134 | £0.10 |
| Nano Banana Pro, 4K | $0.24 | £0.18 |
| Nano Banana 2 (`gemini-3.1-flash-image`), 1K / 2K / 4K | $0.067 / $0.101 / $0.151 | £0.051 / £0.076 / £0.114 |

Batch mode is half price for both image models.

**Audio**

| Model (ID) | USD | GBP (≈) |
|---|---|---|
| Gemini 3.8 Flash TTS (`gemini-3.8-flash-tts`) | Through 31 Dec 2026: ≈ $0.00225 per 10 sec of audio (≈ $0.0135/min). From 1 Jan 2027: ≈ $0.0045 per 10 sec (≈ $0.027/min) | ≈ £0.010/min → ≈ £0.020/min |
| Lyria 3.5 music (`lyria-3.5`) | $0.08 per full song | £0.060 per song |
| Lyria 3 Clip Preview (`lyria-3-clip-preview`) | $0.04 per 30-second clip | £0.030 |

### Requirements
1. **Google account** and a **Google AI Studio project** [Fact].
2. **Gemini API key.** Get it from the AI Studio API keys page. The SDKs read it from the `GEMINI_API_KEY` (or `GOOGLE_API_KEY`) environment variable [Fact] ([API keys](https://ai.google.dev/gemini-api/docs/api-key)).
3. **Paid tier / billing** [Fact]. Veo, Omni Flash, Nano Banana Pro and Lyria have **no free tier**. To upgrade you link a Cloud billing account and usually **prepay at least $5 (≈ £3.78)**. Requests are served only while the prepaid balance is positive. Tier 1 starts with a **$250 (≈ £189) billing cap**, which rises with spend and account age ([billing](https://ai.google.dev/gemini-api/docs/billing)).
4. **SDK:** `pip install google-genai` (Python) or `npm install @google/genai` (Node) [Fact] ([libraries](https://ai.google.dev/gemini-api/docs/libraries)).

### How to obtain them
- Go to [Google AI Studio](https://aistudio.google.com/), sign in, open **Get API key**, and create a key in a project.
- On that page (or the Projects page), click **Set up billing**, add a billing account and prepay credit ([billing](https://ai.google.dev/gemini-api/docs/billing)).

### Other useful info
- **[Fact]** Google's coding-agent page recommends `npx add-mcp "https://gemini-api-docs-mcp.dev"`. This is a **documentation** MCP: it helps the agent write correct code but does not generate media itself. It also recommends `npx skills add google-gemini/gemini-skills --skill gemini-api-dev --global` ([coding agent setup](https://ai.google.dev/gemini-api/docs/coding-agents)).
- **[Fact]** Several models are still labeled "preview" (for example, the Veo 3.1 IDs). Preview models can change or be retired.
- **[Fact]** For Veo, "You will only be charged if your video is successfully generated."

---

## 1.2 Runway API, "Runway Dev" (video, plus image and audio)

### Why it was chosen [Inference, based on the facts below]
- It is built for professional video delivery. **[Fact]** Gen-4.5 and Aleph 2.0 can output **ProRes, PNG sequences, 10-bit SDR, and true HDR** (HDR10, HLG, 12-bit masters, ACEScg EXR). It also offers **video upscaling, frame-rate conversion and SDR-to-HDR** ([models](https://docs.dev.runwayml.com/guides/models/)). These are deliverable formats a premium client may ask for, and the Gemini API does not list them.
- **[Fact]** One Runway key reaches many leading third-party models: Seedance 2.5/2.0, Veo 3.1, Gemini Omni Flash, MiniMax H3, WAN 3.0 and Grok Imagine for video; GPT Image 2.5, Nano Banana Pro/2 and Seedream 5 for image; ElevenLabs v4/v3 for audio. It also has a **Model Router** that "automatically route[s] each request to the best available model… No additional cost" ([models](https://docs.dev.runwayml.com/guides/models/)). For a beginner this means one bill and one key for many top models.
- **[Fact]** Aleph 2.0 edits existing video (video + text/image in, video out). Act-Two does performance/character animation.

### Costs [Fact: Runway pricing page]
Credits cost **$0.01 each (≈ £0.0076)**, and sales tax may apply. The **minimum first payment is $10 (≈ £7.56)** ([setup](https://docs.dev.runwayml.com/guides/setup/), [pricing](https://docs.dev.runwayml.com/guides/pricing/)).

| Model (ID) | Credits | USD | GBP (≈) |
|---|---|---|---|
| Gen-4.5 (`gen4.5`) | 12 / sec | $0.12 / sec | £0.091 / sec |
| Aleph 2.0 (`aleph2`) video editing | 28 / sec (min 56 per job) | $0.28 / sec | £0.21 / sec |
| Seedance 2.5 (`seedance2_5`), 1080p | 68 / sec output (+34 / sec of input video; min 80) | $0.68 / sec | £0.51 / sec |
| Veo 3.1 with audio (`veo3.1`) | 40 / sec | $0.40 / sec | £0.30 / sec |
| Gemini Omni Flash 1.1 (`gemini_omni_flash_1.1`), 1080p / 4K | 15 / 30 per sec | $0.15 / $0.30 per sec | £0.11 / £0.23 per sec |
| ProRes / PNG-sequence surcharge | +5 / sec | +$0.05 / sec | +£0.038 / sec |
| HDR / 10-bit surcharge | +20 / sec (+40 above ~4K) | +$0.20 / sec (+$0.40) | +£0.15 (+£0.30) |
| GPT Image 2.5 (`gpt_image_2_5_sunburst` / `_flare`), high, 1K/2K | 16 per image | $0.16 | £0.12 |
| Nano Banana Pro (`gemini_image3_pro`), 1K/2K / 4K | 20 / 40 per image | $0.20 / $0.40 | £0.15 / £0.30 |
| ElevenLabs v3 via Runway (`eleven_v3`) | 1 per 50 characters | $0.20 per 1K characters | £0.15 |

*Worked example [Inference]:* a 10-second Gen-4.5 clip is 120 credits, or **$1.20 (≈ £0.91)**. Delivering it as HDR10 adds 200 credits (+$2.00 ≈ £1.51).

*Note [Inference]:* reselling through Runway can cost more than going direct. ElevenLabs v3 is $0.20 per 1K characters through Runway versus $0.08 direct, and Nano Banana Pro is $0.20 versus $0.134 direct. Veo 3.1 with audio is the same price ($0.40/sec) either way.

### Requirements
1. **Runway Developer Portal account** (separate from the Runway web app) [Fact].
2. **Project + API key.** Keys are project-scoped and **shown only once**. The SDK reads the `RUNWAYML_API_SECRET` environment variable [Fact] ([setup](https://docs.dev.runwayml.com/guides/setup/)).
3. **Credits:** at least $10 prepaid [Fact].
4. **SDK:** Python package `runwayml`; Node package `@runwayml/sdk` [Fact] ([SDKs](https://docs.dev.runwayml.com/api-details/sdks/)).

### How to obtain them
Sign up at [dev.runwayml.com](https://dev.runwayml.com/). Create a project, open **API Keys**, create a key and copy it immediately. Then open **Billing** and add credits ([setup](https://docs.dev.runwayml.com/guides/setup/)).

### Other useful info
- **[Fact]** Runway provides a "Runway Dev" MCP server at `https://dev.runwayml.com/mcp` with official commands for both clients:
  - Claude Code: `claude mcp add --transport http --scope user runway-dev-mcp https://dev.runwayml.com/mcp`
  - Codex: `codex mcp add runway-dev-mcp --url https://dev.runwayml.com/mcp`, then `codex mcp login runway-dev-mcp --scopes openid,profile,email,mcp:read,mcp:write`

  This MCP is for **managing your account, tasks and docs, not for generating media**. Runway says a separate "generation MCP at mcp.runwayml.com… creates media in chat" ([Runway MCP page](https://docs.dev.runwayml.com/guides/mcp/)). Runway also says to complete OAuth yourself in a browser and not to let the agent automate sign-in.
- **[Uncertain]** I did not verify whether `mcp.runwayml.com` bills against API credits or a Runway web-app plan. The reliable route for a worker is the API key + SDK (see the setup steps in section 3).
- **[Fact]** Runway has a "Go-live checklist" and usage tiers that affect concurrency. Check them before taking high-volume jobs.

---

## 1.3 OpenAI API (image + audio; no video since 24 Sep 2026)

### Why it was chosen (for **image**) [Inference, based on the facts below]
- **[Fact]** OpenAI's current image models are `gpt-image-2.5-sunburst` ("for workflows where editing precision matters most") and `gpt-image-2.5-flare` ("fast, high-quality everyday image generation"). Both add **`xhigh` and `max` quality** settings and support sizes up to **3840 px** (4K) and transparent backgrounds ([image generation guide](https://developers.openai.com/api/docs/guides/image-generation)).
- They have strong prompt-following and image-editing endpoints (generate and edit, reference images, `input_fidelity`), which suit premium jobs that need iteration on a brief [Fact: features; Inference: suitability].
- Codex users will already have an OpenAI platform account if they use API billing [Inference].

### Costs [Fact: OpenAI pricing + image guide]
- GPT Image 2.5 (both variants) is billed per token: **$30 per 1M image-output tokens**, $8 per 1M image-input tokens and $5 per 1M text-input tokens. In GBP: ≈ £22.67 / £6.05 / £3.78. Batch is half price ([pricing](https://developers.openai.com/api/docs/pricing)).
- OpenAI does **not** publish a flat per-image USD price for 2.5. For reference, the predecessor `gpt-image-2` costs **$0.006 (low) / $0.053 (medium) / $0.211 (high) per 1024×1024 image**, which is ≈ £0.0045 / £0.040 / £0.16 ([image guide](https://developers.openai.com/api/docs/guides/image-generation)).
- **[Inference]** Runway's resale price for GPT Image 2.5 ($0.16 high, $0.28 xhigh, $0.63 max at 1K/2K) gives a rough ceiling. Direct OpenAI pricing is likely at or below this. Check the `usage` field in API responses for real costs.
- Audio (not a top-2 pick): `gpt-4o-mini-tts` costs $0.60 per 1M text-input tokens + $12 per 1M audio-output tokens (≈ £0.45 / £9.07). `tts-1-hd` costs $30 per 1M characters (≈ £22.67).

### Requirements
1. **OpenAI Platform account** at platform.openai.com (separate from ChatGPT subscriptions) [Fact].
2. **API key** in the `OPENAI_API_KEY` environment variable [Fact] ([quickstart](https://developers.openai.com/api/docs/quickstart)).
3. **Prepaid credit.** Usage Tier 1 requires **$5 paid** (≈ £3.78) and allows $100/month ([rate limits](https://developers.openai.com/api/docs/guides/rate-limits)) [Fact].
4. **API Organization Verification** "may" be required before using GPT Image models [Fact] ([image guide](https://developers.openai.com/api/docs/guides/image-generation)).
5. **SDK:** `pip install openai` or `npm install openai` [Fact].

### How to obtain them
Sign in at [platform.openai.com](https://platform.openai.com/). Add a payment method and credit under **Billing**, create a key under **API keys**, and complete **Organization Verification** in the developer console settings if prompted.

**[Uncertain]** OpenAI's help-center articles on prepaid billing and Organization Verification returned HTTP 403 to my fetches. I could not quote the exact verification requirements (for example, a government ID) or the processing time.

### Other useful info
- **[Fact]** OpenAI's usage policy requires telling end users that a TTS voice is AI-generated ([TTS guide](https://developers.openai.com/api/docs/guides/text-to-speech)).
- **[Fact]** Spend limits and alerts can be set per organization or project ([rate limits](https://developers.openai.com/api/docs/guides/rate-limits)). Set these before handing the key to an agent.

---

# 2. SINGLE-MEDIA CATEGORIES

## 2.1 VIDEO
Both video picks are multi-media tools. See **1.1 Google Gemini API** (Pick 1) and **1.2 Runway API** (Pick 2).

**Why Google first, Runway second [Inference]:**
- Choose **Google** for general premium generation at the lowest cost per second with native audio. Omni Flash adds conversational editing.
- Choose **Runway** when the client needs editorial or HDR deliverables (ProRes, EXR, HDR10), video-to-video editing (Aleph), upscaling, or access to other leading models such as Seedance 2.5 under one key.
- OpenAI Sora is **no longer an option** (shut down 24 Sep 2026) [Fact].

## 2.2 IMAGE
Both image picks are multi-media tools. See **1.3 OpenAI GPT Image 2.5** (Pick 1) and **1.1 Google Nano Banana Pro** (Pick 2).

**Why [Inference]:**
- **GPT Image 2.5** has the widest quality range (up to `max`), 4K output, precise editing (Sunburst) and transparent backgrounds.
- **Nano Banana Pro** is cheaper and more predictable per image ($0.134 at 1K/2K), offers 4K, half-price batch mode and optional Google Search grounding.
- Both are also available through a single Runway key if a seat holder prefers one account.

## 2.3 AUDIO

### Pick 1: ElevenLabs API (dedicated audio)

#### Why it was chosen [Inference, based on the facts below]
- It covers every premium audio need from one key [Fact]: text-to-speech (Eleven v4, v3, Multilingual v2, Flash), **music** generation (up to 5 minutes, 44.1 kHz, commercial licensing on Starter+), **sound effects**, voice cloning, voice changer, voice isolation, dubbing (v2 covers 92 languages) and speech-to-text ([API pricing](https://elevenlabs.io/pricing/api)).
- **[Fact]** ElevenLabs maintains an **official MCP server** (`elevenlabs-mcp`) that generates and saves audio files directly from an agent ([GitHub: elevenlabs/elevenlabs-mcp](https://github.com/elevenlabs/elevenlabs-mcp)), plus an official skill (`npx skills add elevenlabs/skills`) ([quickstart](https://elevenlabs.io/docs/eleven-api/quickstart)). It is the easiest of all the picks to plug into an agent.
- **[Fact]** Runway resells ElevenLabs models ([Runway models](https://docs.dev.runwayml.com/guides/models/)), which suggests other platforms treat it as a premium audio backend [Inference].

#### Costs [Fact: ElevenLabs API pricing page, 1 Oct 2026]
**Plans** (monthly; they include usage and add pay-as-you-go overage):

| Plan | USD / month | GBP / month (≈) | Included TTS (v4 characters, per page) |
|---|---|---|---|
| Free / Pay-as-you-go | $0 + usage | £0 + usage | 10,000 |
| Starter | $6 | £4.53 | ~273,000 |
| Creator | $22 (first month $11) | £16.62 (first month £8.31) | ~1,000,000 |
| Pro | $99 | £74.81 | ~4,500,000 |
| Scale | $299 | £225.94 | ~13,591,000 |
| Business | $990 | £748.09 | ~45,000,000 |

The included-character figures are read from the v4 column of the plan table while v4 is discounted. I did not fully confirm how these quotas map across models.

**Per-unit rates:**

| Product | USD | GBP (≈) |
|---|---|---|
| TTS Eleven v4 | $0.08 per 1K characters (**$0.022 promo until 12 Oct 2026**) | £0.060 (promo £0.017) |
| TTS Eleven v3 / Multilingual v2 | $0.08 per 1K characters (~1 min of speech) | £0.060 |
| TTS Flash/Turbo, v3 Conversational | $0.04 per 1K characters | £0.030 |
| Music | $0.15 per minute (+$1.50 per finetune) | £0.11/min (£1.13) |
| Sound effects | $0.12 per minute | £0.091 |
| Dubbing v2 | $2.20 per minute | £1.66 |

**[Fact]** Commercial licensing (including for music) requires **Starter or above**. The free tier is not suitable for client work ([pricing](https://elevenlabs.io/pricing)).

#### Requirements
1. **ElevenLabs account** and a **paid plan** (Starter or higher for commercial use) [Fact].
2. **API key** in the `ELEVENLABS_API_KEY` environment variable [Fact] ([quickstart](https://elevenlabs.io/docs/eleven-api/quickstart)).
3. **For the MCP route:** `uv` (Python package runner) installed. The server is started with `uvx elevenlabs-mcp` [Fact] ([GitHub](https://github.com/elevenlabs/elevenlabs-mcp)).
4. **For the SDK route:** `pip install elevenlabs` [Fact]. Model ID example: `eleven_v4`.

#### How to obtain them
Sign up at [elevenlabs.io](https://elevenlabs.io/), choose a plan, then create a key in the dashboard's API keys section ([quickstart](https://elevenlabs.io/docs/eleven-api/quickstart)).

#### Other useful info
- **[Fact]** The MCP server writes files to `ELEVENLABS_MCP_BASE_PATH` (default `~/Desktop`) and only reads input files inside that folder. Point it at your job's working folder.
- **[Fact]** The 72% v4 discount ends on 12 Oct 2026. Budget at the regular $0.08 per 1K characters.

### Pick 2: Google Gemini TTS + Lyria (see 1.1)
**Why second [Inference]:** it is far cheaper for narration (≈ $0.0135/min versus ElevenLabs v3 ≈ $0.08/min) and uses the same key as video and image. Lyria 3.5 makes a full song for $0.08. Google describes Gemini 3.8 Flash TTS as "engineered for studio-grade voice fidelity, expressive acting, and long-form stability" [Fact]. However, ElevenLabs has the broader feature set (voice cloning, sound effects, dubbing, voice library) and a ready-made generation MCP, so it ranks first for premium audio.

---

# 3. Step-by-step: adding a tool to your worker (Claude Code or Codex)

These steps work for any of the four providers. Provider-specific values are in the table at the end of this section.

### Step 1: Create the developer account and add billing
Use the provider's **developer/API** console, not the consumer app. Prepay the minimum and set a **spend limit/alert** if the provider offers one. Premium video can cost several dollars per attempt.

### Step 2: Create an API key and store it as an environment variable
Never paste the key into a chat with the agent, a prompt, or a file that gets committed.
- **macOS/Linux:** add `export PROVIDER_KEY_NAME="your-key"` to `~/.bashrc` or `~/.zshrc`, then open a new terminal.
- **Windows:** `setx PROVIDER_KEY_NAME "your-key"`, then open a new terminal.
- Restart Claude Code or Codex from that new terminal so it inherits the variable.

### Step 3: Install the provider's SDK
Use the `pip install …` or `npm install …` command from the table below.

### Step 4: Connect the tool to your agent. Choose A or B.

**A. MCP server (when the provider has a generation MCP; currently ElevenLabs)**
- **Claude Code:** `claude mcp add --transport stdio --env ELEVENLABS_API_KEY=$ELEVENLABS_API_KEY elevenlabs -- uvx elevenlabs-mcp`. This is Claude Code's documented `--env` + `--` stdio pattern ([Claude Code MCP docs](https://code.claude.com/docs/en/mcp)). Check it with `/mcp` inside a session.
- **Codex:** `codex mcp add elevenlabs --env ELEVENLABS_API_KEY=$ELEVENLABS_API_KEY -- uvx elevenlabs-mcp`. Alternatively, add a `[mcp_servers.elevenlabs]` table to `~/.codex/config.toml` with `command = "uvx"`, `args = ["elevenlabs-mcp"]` and the key passed via `env_vars` ([Codex MCP docs](https://developers.openai.com/codex/mcp)).
- **[Inference]** Passing `$VAR` on the command line writes the key's *value* into the agent's config file. Keep that file private. In Codex, `env_vars = ["ELEVENLABS_API_KEY"]` forwards the variable without storing it.

**B. A small "skill" that wraps the SDK (works for every provider)**
Both Claude Code and Codex support the open **Agent Skills** format: a folder containing a `SKILL.md` with `name` and `description` frontmatter, plus optional scripts.
- Claude Code reads personal skills from `~/.claude/skills/<skill-name>/SKILL.md` ([Claude Code skills](https://code.claude.com/docs/en/skills)).
- Codex reads them from `~/.agents/skills/<skill-name>/SKILL.md`, or `.agents/skills` inside a repo ([Codex skills](https://developers.openai.com/codex/skills)).

Put a short script in the skill folder (for example, `generate.py`) that calls the SDK and saves the output file. Use `SKILL.md` to say when to use it, which model ID to default to, cost guardrails (for example, "use Veo 3.1 Fast for drafts; only use Standard/4K for the final render") and where to save files. Installing an official skill package is the quickest way to do this:
- Google: `npx skills add google-gemini/gemini-skills --skill gemini-api-dev --global`
- ElevenLabs: `npx skills add elevenlabs/skills`

### Step 5: Run a cheap test
Ask the agent for one low-cost output. Then confirm that the file was saved and that the charge shows up in the provider's usage dashboard. Suggested tests:
- 4–5 s on Veo 3.1 Lite/Fast or Gen-4.5
- one 1K image at medium quality
- one short sentence of TTS

### Step 6: Write a default policy for premium jobs
Record these in `CLAUDE.md` / `AGENTS.md` or the skill:
- which model to use for drafts and which for finals
- maximum spend per job
- output folder
- the AI-disclosure rule (required by OpenAI for TTS)
- **paid tier only** for client data (Google's free tier may use your content to improve its products)

### Provider quick reference

| Provider | Key env var | SDK install | Agent connection |
|---|---|---|---|
| Google Gemini API | `GEMINI_API_KEY` | `pip install google-genai` / `npm install @google/genai` | Skill + script (Docs MCP for documentation only) |
| Runway API | `RUNWAYML_API_SECRET` | `pip install runwayml` / `npm install @runwayml/sdk` | Skill + script (Dev MCP for account/docs only) |
| OpenAI API | `OPENAI_API_KEY` | `pip install openai` / `npm install openai` | Skill + script |
| ElevenLabs API | `ELEVENLABS_API_KEY` | `pip install elevenlabs` / `uvx elevenlabs-mcp` | Official generation MCP, or skill |

---

# 4. Limits, gaps and suggested follow-ups

### What I'm confident in
Prices, model IDs, key names, billing minimums and MCP/skill commands were all read directly from official pages on 1 Oct 2026. I believe the report is complete enough for a seat holder to choose tools and set them up.

### Where data is incomplete or uncertain
1. **"Best" is a judgement, not a measured ranking [Inference].** The brief excluded reviews and customer stories, so I had no independent quality benchmarks. The rankings rest on official capabilities, output formats, pricing and agent integration.
   *Follow-up:* run a small paid bake-off with the same 5–10 prompts across Omni Flash, Veo 3.1, Gen-4.5 and Seedance 2.5 (and the image/audio equivalents), and have a human score the outputs.
2. **OpenAI per-image cost for GPT Image 2.5** is published only as token rates.
   *Follow-up:* generate test images at each quality level and record the `usage` numbers.
3. **OpenAI Organization Verification and prepaid billing details.** The help-center pages returned 403.
   *Follow-up:* read them from a logged-in browser.
4. **Runway's generation MCP (`mcp.runwayml.com`).** I did not confirm whether it uses API credits or a web-app plan, or how it authenticates.
5. **GBP figures are conversions,** not provider GBP prices, and exclude VAT.
   *Follow-up:* check what a UK-billed account is actually charged, including VAT and currency.
6. **ElevenLabs plan quotas** shown are v4 character equivalents during a promotion. Their mapping to other models (v3, music) is not fully clear from the page.
7. **Fast-changing data.** Several Google models are "preview". The ElevenLabs promo ends 12 Oct 2026, and Gemini TTS prices double on 1 Jan 2027. Sora was retired one week before this research.
   *Follow-up:* re-check prices quarterly.

### Gaps in the instructions, and useful information that wasn't asked for
- **Licensing, IP and content-policy terms** for commercial client deliverables (who owns the output, watermarking/C2PA, disclosure rules) were not requested but matter for premium jobs. OpenAI's TTS disclosure rule and ElevenLabs' "commercial license on Starter+" show these differ by provider.
  *Follow-up:* a job comparing each provider's commercial-use terms, provenance/watermark behaviour, and likeness/voice-cloning consent rules.
- **Data privacy:** Google's free tier marks content as used to improve products. Client confidentiality should be a standard checklist item.
  *Follow-up:* a short data-handling comparison (retention, training use, UK/EU data residency).
- **Rate limits and concurrency** (usage tiers at Google, OpenAI and Runway) affect whether a worker can deliver a large job on time. I noted the tiers but did not map them to job sizes.
- **The brief didn't define "worker" technically** (local CLI, cloud sandbox, OS). I assumed a local Claude Code or Codex CLI.
  *Follow-up:* if IMD workers run in sandboxes without a browser, the OAuth-based MCPs (Runway Dev) may not work, and env-var + SDK skills should be the standard.

---

# 5. Official sources

**Google Gemini API**
- [Pricing](https://ai.google.dev/gemini-api/docs/pricing)
- [Video generation overview (Omni Flash / Veo)](https://ai.google.dev/gemini-api/docs/video)
- [Image generation (Nano Banana)](https://ai.google.dev/gemini-api/docs/image-generation)
- [Speech generation (TTS)](https://ai.google.dev/gemini-api/docs/speech-generation)
- [API keys](https://ai.google.dev/gemini-api/docs/api-key)
- [Billing](https://ai.google.dev/gemini-api/docs/billing)
- [Libraries / SDKs](https://ai.google.dev/gemini-api/docs/libraries)
- [Coding agent setup (Docs MCP + Skills)](https://ai.google.dev/gemini-api/docs/coding-agents)
- [Google AI Studio](https://aistudio.google.com/)

**Runway API (Runway Dev)**
- [Developer portal](https://dev.runwayml.com/)
- [Setup](https://docs.dev.runwayml.com/guides/setup/)
- [Models](https://docs.dev.runwayml.com/guides/models/)
- [Pricing](https://docs.dev.runwayml.com/guides/pricing/)
- [SDKs](https://docs.dev.runwayml.com/api-details/sdks/)
- [Connect Dev MCP](https://docs.dev.runwayml.com/guides/mcp/)

**OpenAI API**
- [Pricing](https://developers.openai.com/api/docs/pricing)
- [Image generation guide](https://developers.openai.com/api/docs/guides/image-generation)
- [Text to speech guide](https://developers.openai.com/api/docs/guides/text-to-speech)
- [Video generation guide (Sora, shut down)](https://developers.openai.com/api/docs/guides/video-generation)
- [Deprecations](https://developers.openai.com/api/docs/deprecations)
- [Quickstart](https://developers.openai.com/api/docs/quickstart)
- [Rate limits & usage tiers](https://developers.openai.com/api/docs/guides/rate-limits)
- [Platform console](https://platform.openai.com/)

**ElevenLabs**
- [API pricing](https://elevenlabs.io/pricing/api)
- [Plans & licensing](https://elevenlabs.io/pricing)
- [API quickstart](https://elevenlabs.io/docs/eleven-api/quickstart)
- [Official MCP server (GitHub)](https://github.com/elevenlabs/elevenlabs-mcp)

**Agent clients**
- [Claude Code: MCP](https://code.claude.com/docs/en/mcp)
- [Claude Code: Skills](https://code.claude.com/docs/en/skills)
- [Codex: MCP](https://developers.openai.com/codex/mcp)
- [Codex: Skills](https://developers.openai.com/codex/skills)

**Exchange rate**
- [European Central Bank euro reference rates (1 Oct 2026)](https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml)
