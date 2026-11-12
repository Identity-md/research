# Hermes Agent Plugin Hackathon: plugins by kind

This covers the tag results for the Hermes Agent Plugin Hackathon (Nous Research, Nov 4 to 11, 2026). The plugins were tagged by kind so the public scoreboard of the IMD swarm's judging can be filtered by kind. **The tags change no score.**

## Sources and method

The sources are the fifteen slice results `.imd/reads/artifacts/item-tags-00` through `item-tags-14` (also at `artifacts/goal/items/tags-NN/result.json`). Each one is JSON of the form `{"slice": n, "tags": [{"pr", "name", "tags"}]}`. Every figure below comes from counting those files. Nothing else was used.

- **Plugins counted:** 1,464 entries across the 15 slices (slice sizes 97, 91, 81, 96, 99, 107, 102, 87, 98, 110, 101, 94, 103, 105, 93 for slices 00–14). No plugin name appears twice, and every entry has one or two tags. None is empty, so no slice result is missing or blank.
- **PR numbers vs plugins:** there are 1,442 distinct PR numbers. Eight PRs each hold several plugins, for example PR 153370 (7 plugins in slice 10), PR 149641 (6 in slice 01) and PR 153040 (5 `model-forge*` plugins in slice 10). The counts below are per plugin, not per PR.
- **Main tag:** the results do not label a main tag. I took the **first-listed tag** as the main one. Tag order is not alphabetical (307 of the 605 two-tag entries are in alphabetical order, 298 are not), so the order looks deliberate. Still, this is my reading, not something the files state.
- **Tags used:** 23 tags. 859 plugins have one tag and 605 have two.
- **Not checked:** the full public results file was not provided. So I could not confirm that the 15 slices together cover every entered plugin.

## How many plugins got each tag as their main tag

| Main tag | Plugins (main tag) | Share | Of these, tagged only this | Plugins carrying the tag at all |
|---|---:|---:|---:|---:|
| safety | 140 | 9.6% | 83 | 185 |
| dev | 134 | 9.2% | 79 | 205 |
| memory | 103 | 7.0% | 71 | 117 |
| media | 101 | 6.9% | 61 | 123 |
| automation | 91 | 6.2% | 56 | 118 |
| desktop | 85 | 5.8% | 52 | 169 |
| business | 84 | 5.7% | 45 | 101 |
| research | 81 | 5.5% | 55 | 119 |
| models | 66 | 4.5% | 48 | 90 |
| proof | 63 | 4.3% | 30 | 101 |
| marketing | 61 | 4.2% | 44 | 77 |
| monitoring | 59 | 4.0% | 31 | 94 |
| multi-agent | 54 | 3.7% | 19 | 83 |
| money | 46 | 3.1% | 29 | 68 |
| hardware | 45 | 3.1% | 19 | 52 |
| crypto | 41 | 2.8% | 16 | 55 |
| games | 41 | 2.8% | 20 | 53 |
| devices | 36 | 2.5% | 21 | 48 |
| messaging | 35 | 2.4% | 22 | 61 |
| sandboxes | 29 | 2.0% | 16 | 41 |
| voice | 29 | 2.0% | 19 | 45 |
| health | 22 | 1.5% | 17 | 26 |
| undo | 18 | 1.2% | 6 | 38 |
| **Total** | **1464** | 100% | 859 | 2069 tag uses |

"Plugins (main tag)" counts plugins whose first tag is this one. "Tagged only this" counts plugins whose single tag is this one. "Carrying the tag at all" counts plugins that have the tag in either position. The middle column sums to 1,464 plugins. The last column sums to 2,069 tag uses, which is 859 plus 2×605.

The slices disagree on nothing, because each plugin was tagged in exactly one slice. No plugin was tagged twice, so there was nothing to reconcile.

## The ten plugins hardest to place

The results hold only a name and tags for each plugin. There is no description, confidence or "hard to place" flag. So I picked these ten with a rule anyone can re-run on the files:

1. Take the two-tag plugins whose tag pair occurs **only once** among all 1,464 plugins. There are 47.
2. Rank them by how often their two tags would meet by chance: (uses of tag A × uses of tag B) ÷ 1,464.
3. Keep the top ten. These are plugins that sit across two common kinds which no other entrant combines, so either main tag is arguable.

Each "why" is reasoned from the tags and the name only, since the files hold nothing else.

1. **plagio** (PR 151422, slice 12; `media`, `dev`): it is the only plugin tagged both media and dev (123 and 205 uses). It reads as part creative tool and part developer tool.
2. **odoo-prod-guard** (PR 149142, slice 12; `business`, `safety`): it is the only business+safety pair (101 and 185 uses). It guards a business system (Odoo), so the scoreboard could list it under the domain or the guard. It also shares its PR with two other plugins.
3. **developh** (PR 151277, slice 02; `marketing`, `dev`): it is the only marketing+dev pair (77 and 205 uses). The name points to developers, while the main tag says marketing.
4. **playbox-witness** (PR 153141, slice 06; `safety`, `multi-agent`): it is the only safety+multi-agent pair (185 and 83 uses). It is a safeguard that is also about running several agents.
5. **imprint** (PR 153978, slice 03; `research`, `media`): it is the only research+media pair (119 and 123 uses). The name fits either kind, and the tagger chose research first.
6. **onbrief** (PR 153685, slice 10; `marketing`, `safety`): it is the only marketing+safety pair (77 and 185 uses). Two kinds that seldom overlap had to share one plugin.
7. **tupliq-launchpad** (PR 153731, slice 11; `money`, `dev`): it is the only money+dev pair (68 and 205 uses). A "launchpad" could be a builder's tool or a funding tool, and money was put first.
8. **stageglass** (PR 153194, slice 14; `desktop`, `marketing`): it is the only desktop+marketing pair (169 and 77 uses). It splits between the surface it runs on and what it is for.
9. **thumbs-fix** (PR 153796, slice 01; `dev`, `messaging`): it is the only dev+messaging pair (205 and 61 uses). The name suggests a fix to a chat or reaction feature, so it is either developer work or messaging.
10. **leitmotif** (PR 153412, slice 07; `monitoring`, `media`): it is the only monitoring+media pair (94 and 123 uses). The name is musical but the main tag is monitoring, and it is the least obvious name-to-tag match of the ten.

The next ones on the same ranking are contract-hunter (`crypto`, `dev`), minicpm-ocr (`research`, `models`) and reset-rescue (`models`, `automation`).

Two more kinds of plugin are hard to place but are not ranked above, because the rule does not measure them:

- **Bundled PRs:** for example, PR 153370 holds seven plugins in six different main-tag kinds (dev, media, business, games), so filtering by PR and filtering by kind give different results.
- **Single tags:** 859 plugins got only one tag, which may hide a second kind.

*Per-plugin tags are left out on purpose, as the brief asks. They are in the fifteen source files above.*
