# Report: Interactive 5e character-sheet guide

**Question / task:** Build an interactive guide for making a new D&D 5e character sheet.
It needs a step panel on one half of the screen and the full sheet on the other; term
hotlinks to the most official source, opening in a mini-panel over the bottom quarter of
the sheet; choice-appropriate inputs; automatic math and point counters; a PDF save/print
at physical scale; a red-border "final check"; and accessibility features.

**Deliverable:** `index.html`, `css/style.css`, `js/data.js`, `js/app.js`, and
`README.md` (how to use it, scope, limits). It is a static page with no dependencies and
no build step; open `index.html` directly.

Labels used below: **[Fact]** = checked directly (command output or test result).
**[Inference]** = reasoned but not directly verified. **[Uncertain]** / **[Open]** = not
resolved.

---

## 1. What was built (requirement → implementation)

| Requirement | Implementation | Evidence |
|---|---|---|
| Section-by-section panel on half, full sheet on other half | CSS grid of two equal columns. The left side has 11 steps; the right side has a live two-page sheet. The panes stack below 900 px width. | [Fact] Screenshot at 1500×950 viewport shows both halves (test `done.png`). |
| Terms hotlink to official entry, opening a mini-panel over the bottom ¼ of the sheet | Each term is an `<a href>` to D&D Beyond. A click handler opens `#mini-panel` (absolute, `height:25%`, bottom of the sheet pane). Ctrl/⌘-click follows the link. Esc closes the panel and returns focus. | [Fact] Test: panel height 226 px vs. sheet pane 904 px (= 25%), bottom-aligned; Esc closes it. |
| Inputs suited to each section | Buttons for single choices, checkboxes for multi-selects, +/− steppers for point buy, number fields + 🎲 for rolls, text areas for prose. | [Fact] Exercised by the end-to-end test (below). |
| Automatic math | Modifiers, saves, skills/Expertise, passive Perception, AC (all armors, shield, unarmored variants, Defense), initiative, speed (incl. heavy-armor Strength penalty), HP, attacks, cantrip attacks/DCs, spell DC/attack, prepared counts. | [Fact] High Elf Wizard (standard array) gave HP 8, AC 12, passive Perception 13, spell DC 13 / +5, Fire Bolt +5 1d10: all match hand calculation from the 2014 rules. |
| Points counters | Point buy (27), standard-array assignment, class/racial/replacement skills, Expertise, languages, cantrips, spells, prepared spells, weapons. They show "n / max" with ok/over states and are announced via `aria-live`. | [Fact] Test read "Points spent: 0 / 27 — 27 left". |
| Save/print PDF at physical scale | Sheet pages are sized in `in` (8.5×11) or `mm` (A4). Print CSS hides the UI and removes the zoom transform. `@page {size: letter; margin:0}` is switchable to A4. | [Fact] Chromium `page.pdf(preferCSSPageSize)` produced 2 pages with `/MediaBox [0 0 612 792]`, i.e. exactly 8.5×11 in. |
| Final check with red borders | `validate()` returns issues mapped to sheet areas and steps. Final check adds a red outline to those areas and step tabs and lists the issues with "Go to" buttons. Covers incomplete *and* incorrect entries (over-budget point buy, duplicated array values, non-proficient armor/shield/weapons, metal armor on a Druid, wrong spell/skill counts). | [Fact] Empty sheet → 16 areas outlined. Completed wizard → 0 issues. Adding plate armor → AC box outlined. |
| Extra UX/accessibility | Autosave, JSON export/import, reset, "use class starting equipment", "suggest scores for my class", zoom, click-sheet-to-edit, skip links, labels, `aria-pressed`, live region, focus restoration, high contrast / larger text / sans font / reduced motion, responsive stacking, A4 option. | [Fact] Present in code. The test run had no JS errors. [Uncertain] No screen-reader or manual keyboard audit was done (see §4). |

## 2. Which source is "most official", and link verification

- **[Fact]** D&D Beyond is Wizards of the Coast's official digital rules site. It has a
  page for each class, species (race), background, spell and equipment entry. Slug URLs
  such as `https://www.dndbeyond.com/classes/wizard` redirect (301) to canonical
  `…/classes/8-wizard`, and `…/spells/fire-bolt` redirects to `…/spells/2103-fire-bolt`
  (curl, 2026-09-27).
- **[Fact]** Race links first used `/species/<name>`. That redirected to
  `/races/13-dwarf`, which returns **404**. I changed them to the ID form
  `/species/13-dwarf`, which returns 200, and did the same for all nine races.
- **[Fact]** `/backgrounds/criminal` and `/backgrounds/guild-artisan` return 404. The
  working slugs are `criminal-spy` and `guild-artisan-guild-merchant`, and both are now
  used.
- **[Fact]** Final sweep of all **167** distinct URLs the app can generate, following
  redirects (`curl -L`; 166 in the batch loop, and the Basic Rules `equipment` page checked
  separately because the loop skipped the file's last line): **158 end at a 200 content page. 9 end at the D&D Beyond
  marketplace** (`marketplace.dndbeyond.com/category/players-handbook`). The 9 are
  Player's Handbook-only entries (for example Charlatan, Entertainer, Hermit, Outlander,
  Sailor, Urchin, Tasha's Hideous Laughter, Tenser's Floating Disk), and anonymous
  visitors are sent to the store for them.
  - **[Inference]** Logged-in users who own the PHB on D&D Beyond will probably see the
    entry. This was not tested because it needs an account.
  - To cover this, every mini-panel also links the free SRD 5.1 PDF from Wizards of the
    Coast (`https://media.wizards.com/2023/downloads/dnd/SRD_CC_v5.1.pdf`; [Fact] HTTP
    200, 3,158,713 bytes).
- **[Fact]** Rules terms (AC, proficiency bonus, point buy, death saves, etc.) link to
  section anchors in the free 2014 Basic Rules on D&D Beyond, e.g.
  `…/sources/dnd/basic-rules-2014/using-ability-scores#ArmorClass`. The anchor IDs were
  read from the live page HTML.
- **[Fact] Why a summary panel instead of the official page embedded in an iframe:**
  D&D Beyond sends `x-frame-options: SAMEORIGIN` and a CSP `frame-src` allowlist that
  excludes third parties. An iframe of the official page would be blank. The mini-panel
  therefore shows an original summary plus the official link, and it says so in the
  panel.

## 3. Rules accuracy (data)

- **[Fact]** The mechanics come from the 2014 PHB / SRD 5.1:
  - race ability increases, speeds and traits
  - class hit dice, saves, skill lists and counts, armor/weapon proficiencies
  - background skill pairs
  - armor AC formulas and Strength requirements
  - weapon damage and properties
  - point-buy costs (8=0 … 13=5, 14=7, 15=9; budget 27)
  - standard array
  - 1st-level spell counts (Bard 2/4 known, Cleric 3 + Wis+1 prepared, Druid 2 + Wis+1, Sorcerer 4/2, Warlock 2/2 + 1 pact slot, Wizard 3 + 6-spell book, Int+1 prepared)
  
  These were entered from my knowledge of those rules. **[Uncertain]** They were not
  checked line by line against the SRD PDF in this session, so an individual
  transcription error is possible. The end-to-end numbers I checked (§1) came out
  correct.
- **[Inference]** Summaries are my own paraphrases, and PHB-only content (e.g. extra
  subraces, 12 non-SRD backgrounds) is only mechanics and names, not reproduced text.
  **[Open]** Anyone planning to publish the tool should do a licensing review.

## 4. How it was checked

- `node --check` on both JS files: pass.
- Playwright + headless Chromium end-to-end script (in the discarded `test/scratch/`)
  with 14 checks, **all PASS** on the final run:
  - final check outlines areas on an empty sheet (16)
  - mini-panel opens, covers ¼ of the sheet pane and closes with Esc
  - racial bonus applied (INT 15+1 = 16)
  - a completed High Elf Wizard / Sage passes final check with 0 issues
  - HP 8, AC 12, passive Perception 13, spell DC 13 / +5, Fire Bolt +5
  - non-proficient plate armor flags AC
  - point-buy counter starts at 0/27
  - no JS errors
- PDF output: 2 pages at 612×792 pt.
- I looked at screenshots (full sheet, mini-panel, narrow viewport).

## 5. Limits and open questions

- **[Open]** Only 1st level is supported: the level is fixed at 1 and XP at 0. Higher
  levels would need per-level spell and feature tables.
- **[Open]** Only the 2014 ruleset is covered. D&D Beyond now also hosts the 2024
  revision, where backgrounds, not races, grant ability increases. Which edition the user
  wants is unconfirmed.
- **[Open]** For classes that pick a subclass at 1st level, only the SRD option is
  offered (Life, Draconic, Fiend).
- **[Open]** Tool choices phrased "one of your choice" are listed but not selectable.
- **[Open]** The Mountain Dwarf/Mountain armor and Tiefling/Drow innate spells are shown
  as traits but not added to the spell page.
- **[Uncertain]** The print scale was verified in Chromium's PDF engine only. Firefox and
  Safari print dialogs may default to "fit to page". The Review step tells users to pick
  100% / Actual size.
- **[Uncertain]** The layout is modelled on the official sheet's structure (header, three
  columns, spell page) but is not a pixel copy of it.
- **[Uncertain]** Accessibility: semantic structure and ARIA are in place, but there was
  no screen-reader testing (NVDA/VoiceOver) and no formal WCAG contrast audit.
- **[Uncertain]** D&D Beyond URLs and IDs are time-sensitive; they were verified on
  2026-09-27 and may change.
