# Kekborn portraits v2 — owner review

**Hold approval of the twelve-portrait set.** In both versions of 01, 03, 09, 11 and 12, the frog has a closed mouth on its face and a separate pair of red lips below it. Open 09 at native preview size to see the gap. Sample 02 shows how a painted mouth can follow the muzzle while leaving the expression legible. On the sheet, each number identifies one input, with the plain composite on the left (P) and its harmonised version on the right (H). [Contact sheet][sheet] · [09 plain][09p] · [09 harmonised][09h] · [02 plain][02p]

The delivered repository is **identity-md-launches/goal-3429-kekborn-portraits-v2-repaint**, commit `faab8c3d27eab6675d7ceae7b55c44fd48b18b92`. It builds on the original portrait library at `9ab5835fd20d740eafc029416b163dce239d55f8`. All twelve plain masters reproduce from this commit. Exact recovery of the harmonised masters requires twelve missing model images. The goal records 39 landed build targets and 39 accepted checks. The proposed mouth repair exceeded the target-description limit (8,645 characters against 8,000) and never ran. Owner approval remains pending. The goal records no deployment, mint or additional spend. [Delivered commit][trunk] · [Original library][baseline]

## The twelve sittings

Each row links to the two 1024 × 1280 JPEGs from that input. Names in the expression column are the paintings the compositor selected, including those selected through legacy names.

| Input | Sitter | Expression | What to inspect in P and H | Previews |
|---|---|---|---|---|
| 01 | Scholar · moss · common | Smug | Both red lips sit below the jaw. Green forelimbs rise above the robe. The wall is plaster. | [P][01p] · [H][01h] |
| 02 | Antiquary · lichen · uncommon | Paranoid side-eye | The mouth follows the muzzle. The monocle, brocade and dark patterned arras give a comparison for the other sittings. The banner shield has a hard outline. | [P][02p] · [H][02h] |
| 03 | Knight · slate · rare | Serene | The red mouth hangs below the closed seam. Beads and brown paint from the cap extend onto the forehead. | [P][03p] · [H][03h] |
| 04 | Artisan · peat · epic | Scowl | The black cap sits high, the rusty collar breaks across the throat and the backdrop is masonry. | [P][04p] · [H][04h] |
| 05 | Seer · ivory · legendary | Dim grin | The open grin, gloved orb and jewelled frame read clearly. Oak panelling occupies the space reserved for damask. | [P][05p] · [H][05h] |
| 06 | Council · moss · common | Regal | Green shoulders rise behind a broad white ruff with a cut edge. The wall is plaster. | [P][06p] · [H][06h] |
| 07 | Scholar · peat · uncommon | Weeping | Darker skin makes the bent forelimbs easy to miss at sheet scale. Both remain visible above the fur robe. | [P][07p] · [H][07h] |
| 08 | Antiquary · oxblood · rare | Startled | The open mouth reads as startled. The pearl cap and thin silver-coloured chain have cutout edges. | [P][08p] · [H][08h] |
| 09 | Knight · lichen · epic | Melancholy | The complete red mouth is below and left of the muzzle. A pale strip follows the black brim, brown paint crosses the throat, and stone fills the backdrop. | [P][09p] · [H][09h] |
| 10 | Artisan · ivory · legendary | Sly | The grin and artisan tools are legible. The oak backdrop lacks damask. | [P][10p] · [H][10h] |
| 11 | Seer · slate · rare | Serene | The low red mouth crosses the chain below the muzzle. The backdrop is plaster. | [P][11p] · [H][11h] |
| 12 | Council · oxblood · epic | Smug | The red lips hang below the closed mouth. Rust-coloured regalia crosses the white ruff and the red skin blends into the clothing. | [P][12p] · [H][12h] |

## What the library delivers

The archive contains 90 layer PNGs, each 2048 × 2560 on the original 4:5 grid. There are six skins (ivory and oxblood are rare), eight eye sets, ten expressions with two layers each, fifteen garments and props across six categories, five headwear layers, five regalia layers, five backdrops, three banners, eighteen heraldry components and five frames. The frame progression is plain wood, carved oak, silver, gilded gold and jewelled gold with a plaque. The silver reads as flat grey at preview scale. The master has the surface and light of an oil study, but its narrow, naturalistic tree-frog head only partly achieves the requested heavy-lidded, full-lipped character. [Layer library][layers] · [Painted bust][bust]

The style guide includes the locked Tudor-oil prompt, the negative prompt, the palette, the bust grid and the upper-left light direction. The compositor tints expression underpainting to the selected skin, then places the separately painted lips, teeth or tears. All 26 catalogs use `kekborn-assets@1`. The assigned rarity values are `common` and `rare`. The legacy selections still resolve as wistful → melancholy, resolute → regal, amused → sly and dubious → weeping. All 76 surviving baseline layer PNGs changed. Four legacy expression PNGs were removed, and their input names remain valid through the aliases. [Style guide][guide] · [Bust grid][grid] · [Catalog][catalog] · [Compositor][compositor]

## Where the paintings depart from the brief

**Mouth registration.** In master pixels, the guide puts the far and near corners at (495, 1190) and (1060, 1220). On the painted bust they are (680, 1148) and (1200, 1104). From far to near, the guide descends 30 pixels while the painting rises 44. To meet the guide’s ±24-pixel tolerance on the painting, the vertical shift would have to fall in both [−66, −18] and [−140, −92]. Those intervals are disjoint. Decoding the three lip PNGs gives the same occupied bounds in each, x495–1059 and y1165–1324 inclusive. **Zero painted lip pixels intersect the master’s measured mouth box** (x680–1199, y1090–1161). That explains the second mouth in five pairs. With this bust, both corners and the slope of the seam need to follow the painted landmarks. [Guide §§2.2 and 4][guide] · [Measured landmarks][landmarks] · [Expression paintings][expressions]

**Fit of the clothing.** Compare the neck and collar of 01 and 07 in the native preview rectangle x240–770, y610–940. The bent limbs on the left and right match the bare peat bust. At master pixels (700, 1432) and (1364, 1378), both moss and peat are fully opaque and the front scholar robe has alpha zero. In 06 the wide white ruff likewise cuts across a second set of shoulders. Workers report using ImageGen reference edits for most fitted pieces. For the council coat and sash, rare cap and chain, and epic hat and collar, the three provenance files record text-only Sana generations at 686 × 858. The painters used the bust for placement after cutting out the clothing. The brown residue on 03’s forehead and 09’s throat survives harmonisation. These six wearables miss the requested on-bust inpainting step. Sana also supplied the soft master and the dim-grin and scowl sources. [Master provenance][master-prov] · [Expression provenance][expr-c] · [Scholar robe][robe] · [Peat bust][peat] · [Council provenance][council] · [Rare provenance][rare] · [Epic provenance][epic]

**Backdrop and heraldry.** Only green arras (02, 07, 12) and oxblood chamber (03, 08) supply patterned cloth. The recorded layer prompts specify uninterrupted plaster for umber hall (01, 06, 11), masonry for stone apse (04, 09) and solid wood for oak gallery (05, 10). Those materials are visible behind all seven sitters. The three banners are separate model-painted textiles. Their shields use an ImageGen atlas of six paint swatches inside the original heraldic outlines. A pixel-by-pixel comparison with the baseline found identical alpha planes in **18 of 18** heraldry PNGs, including all charge shapes. The painted substance changed, but the per-layer painting of heraldic forms remains outstanding. [Backdrop prompts][backdrops] · [Banner provenance][banners] · [Heraldry method][heraldry] · [Original heraldry][old-heraldry]

## Rendering, checks and recovery of the masters

The finishing pass applies a shadow glaze, seeded brush texture, warm varnish, fine craquelure and an inward frame shadow. Optional harmonisation requests strength 0.22 and seed 1536. The offline apply step blends up to 22% model colour inside the aperture with a 64-pixel feather. It preserves the rails and plaque. Both the real-catalog and sample-input suites passed within the **97/97** tests on this revision. The approval verifier also passed. [Finish][finish] · [Harmonisation][harm] · [Tests][tests]

The 24 quality-90 previews range from 246,107 to 547,940 bytes. The 4,288 × 2,048 contact sheet is 2,791,109 bytes, SHA-256 `80e1c59085c3ff251ebd3efa88a6fd08de57048ca9ccde617fbc1bd29699dc19`. All 225 manifest entries matched both byte counts and digests. Of the 226 archive files, the only file outside the manifest is the manifest itself, SHA-256 `a46373692834c23d3ee9d38dcc1328fef1a2a9869a77fdc9a14318cb439ba14f`. The largest file is the antiquary doublet at 3,342,318 bytes. [Manifest][manifest] · [Approval tooling][approval]

**Plain masters.** The compositor and assets reproduce the plain portraits offline. From the pinned repository root, the following renders sample 09 and writes its preview. Substitute any two-digit input number from 01 through 12. In this review, all twelve rebuilt PNGs matched their sidecar master hashes and all twelve rebuilt JPEGs matched their committed bytes. [Inputs][inputs] · [Sample 09 record][09json]

```sh
node bin/render.cjs sample-inputs/09.json out/09-plain.png
node tools/approval.cjs preview out/09-plain.png out/09-plain.jpg
```

**Harmonised masters.** The sidecars record AI Horde AlbedoBase XL at 832 × 1024 for 01–04 and 09–12, and FLUX.1-schnell at 1638 × 2048 for 05–08. Both groups resampled the model image to 2048 × 2560 before applying it. The FLUX jobs used four steps and guidance zero, without a negative prompt. Across the decoded JPEG pairs the full-preview RGB peak signal-to-noise ratio ranged from 33.28 to 42.87 dB, consistent with the slight visible change. [SDXL record][09json] · [FLUX record][05json]

Exact offline recovery fails for **12 of 12 harmonised masters**. The eight SDXL sidecars name the required input in `harmonise.modelOutputSha256`, and the four FLUX sidecars in `harmonise.resample.sha256`. All twelve digests are absent from the 225 manifest entries. For 05, `request` wrote the JSON with the expected seed and strength. `apply` then required `05-model.png`, whose recorded SHA-256 is `60615ae8ee88961a67dd1393f83e1f33c951113064965d3a0af585c4680ccb6c`, and stopped at the missing file. The supplied 1024 × 1280 JPEG cannot recover those full-resolution pixels. The remaining dependency is a lossless source for each model image, or a pinned generation path verified to recreate it. [05 reproduction record][05json] · [Request and apply implementation][harmcli]

**Delivery record.** The root-1-01 merge covers the empty first wave and the later guide, master, expression and renderer work. Root-1-02 covers the later integration (`b02-integrate`), the three preview groups (`b02-previews-a/b/c`) and final packaging (`b02-package`). The package and commit checks above use the final tree. The ten standalone media jobs remained unopened because their outputs could not enter the library or regenerate its sample pairs. This write-up records the artwork that landed. All seven reopened findings require changes in the artwork repository before the complete set can be approved and reproduced. [Integration record][integration] · [Pinned package][trunk]

[trunk]: https://github.com/identity-md-launches/goal-3429-kekborn-portraits-v2-repaint/tree/faab8c3d27eab6675d7ceae7b55c44fd48b18b92
[baseline]: https://github.com/identity-md-launches/goal-3401-create-kekborn-portrait-style/tree/9ab5835fd20d740eafc029416b163dce239d55f8
[old-heraldry]: https://github.com/identity-md-launches/goal-3401-create-kekborn-portrait-style/tree/9ab5835fd20d740eafc029416b163dce239d55f8/layers/heraldry
[sheet]: https://github.com/identity-md-launches/goal-3429-kekborn-portraits-v2-repaint/blob/faab8c3d27eab6675d7ceae7b55c44fd48b18b92/contact-sheet.jpg
[bust]: https://github.com/identity-md-launches/goal-3429-kekborn-portraits-v2-repaint/blob/faab8c3d27eab6675d7ceae7b55c44fd48b18b92/template/master-reference.png
[layers]: https://github.com/identity-md-launches/goal-3429-kekborn-portraits-v2-repaint/tree/faab8c3d27eab6675d7ceae7b55c44fd48b18b92/layers
[guide]: https://github.com/identity-md-launches/goal-3429-kekborn-portraits-v2-repaint/blob/faab8c3d27eab6675d7ceae7b55c44fd48b18b92/style-guide.md
[grid]: https://github.com/identity-md-launches/goal-3429-kekborn-portraits-v2-repaint/blob/faab8c3d27eab6675d7ceae7b55c44fd48b18b92/template/bust.svg
[master-prov]: https://github.com/identity-md-launches/goal-3429-kekborn-portraits-v2-repaint/blob/faab8c3d27eab6675d7ceae7b55c44fd48b18b92/provenance/master.json
[expr-c]: https://github.com/identity-md-launches/goal-3429-kekborn-portraits-v2-repaint/blob/faab8c3d27eab6675d7ceae7b55c44fd48b18b92/provenance/expr-c.json
[catalog]: https://github.com/identity-md-launches/goal-3429-kekborn-portraits-v2-repaint/tree/faab8c3d27eab6675d7ceae7b55c44fd48b18b92/catalog
[compositor]: https://github.com/identity-md-launches/goal-3429-kekborn-portraits-v2-repaint/tree/faab8c3d27eab6675d7ceae7b55c44fd48b18b92/src/compositor
[landmarks]: https://github.com/identity-md-launches/goal-3429-kekborn-portraits-v2-repaint/blob/faab8c3d27eab6675d7ceae7b55c44fd48b18b92/template/master-reference.json
[expressions]: https://github.com/identity-md-launches/goal-3429-kekborn-portraits-v2-repaint/tree/faab8c3d27eab6675d7ceae7b55c44fd48b18b92/layers/expressions
[robe]: https://github.com/identity-md-launches/goal-3429-kekborn-portraits-v2-repaint/blob/faab8c3d27eab6675d7ceae7b55c44fd48b18b92/layers/attire/scholar/attire-front.scholar-robe.png
[peat]: https://github.com/identity-md-launches/goal-3429-kekborn-portraits-v2-repaint/blob/faab8c3d27eab6675d7ceae7b55c44fd48b18b92/layers/skins/peat.png
[council]: https://github.com/identity-md-launches/goal-3429-kekborn-portraits-v2-repaint/blob/faab8c3d27eab6675d7ceae7b55c44fd48b18b92/provenance/attire-council.json
[rare]: https://github.com/identity-md-launches/goal-3429-kekborn-portraits-v2-repaint/blob/faab8c3d27eab6675d7ceae7b55c44fd48b18b92/provenance/tier-rare.json
[epic]: https://github.com/identity-md-launches/goal-3429-kekborn-portraits-v2-repaint/blob/faab8c3d27eab6675d7ceae7b55c44fd48b18b92/provenance/tier-epic.json
[backdrops]: https://github.com/identity-md-launches/goal-3429-kekborn-portraits-v2-repaint/blob/faab8c3d27eab6675d7ceae7b55c44fd48b18b92/provenance/backdrops.json
[banners]: https://github.com/identity-md-launches/goal-3429-kekborn-portraits-v2-repaint/blob/faab8c3d27eab6675d7ceae7b55c44fd48b18b92/provenance/banners.json
[heraldry]: https://github.com/identity-md-launches/goal-3429-kekborn-portraits-v2-repaint/blob/faab8c3d27eab6675d7ceae7b55c44fd48b18b92/provenance/heraldry.json
[finish]: https://github.com/identity-md-launches/goal-3429-kekborn-portraits-v2-repaint/blob/faab8c3d27eab6675d7ceae7b55c44fd48b18b92/docs/finish.md
[harm]: https://github.com/identity-md-launches/goal-3429-kekborn-portraits-v2-repaint/blob/faab8c3d27eab6675d7ceae7b55c44fd48b18b92/docs/harmonise.md
[tests]: https://github.com/identity-md-launches/goal-3429-kekborn-portraits-v2-repaint/tree/faab8c3d27eab6675d7ceae7b55c44fd48b18b92/test
[manifest]: https://github.com/identity-md-launches/goal-3429-kekborn-portraits-v2-repaint/blob/faab8c3d27eab6675d7ceae7b55c44fd48b18b92/manifest.json
[approval]: https://github.com/identity-md-launches/goal-3429-kekborn-portraits-v2-repaint/blob/faab8c3d27eab6675d7ceae7b55c44fd48b18b92/tools/approval.cjs
[inputs]: https://github.com/identity-md-launches/goal-3429-kekborn-portraits-v2-repaint/tree/faab8c3d27eab6675d7ceae7b55c44fd48b18b92/sample-inputs
[09json]: https://github.com/identity-md-launches/goal-3429-kekborn-portraits-v2-repaint/blob/faab8c3d27eab6675d7ceae7b55c44fd48b18b92/samples/09.json
[05json]: https://github.com/identity-md-launches/goal-3429-kekborn-portraits-v2-repaint/blob/faab8c3d27eab6675d7ceae7b55c44fd48b18b92/samples/05.json
[harmcli]: https://github.com/identity-md-launches/goal-3429-kekborn-portraits-v2-repaint/blob/faab8c3d27eab6675d7ceae7b55c44fd48b18b92/bin/harmonise.cjs
[integration]: https://github.com/identity-md-launches/goal-3429-kekborn-portraits-v2-repaint/blob/faab8c3d27eab6675d7ceae7b55c44fd48b18b92/provenance/integration.json
[01p]: https://github.com/identity-md-launches/goal-3429-kekborn-portraits-v2-repaint/blob/faab8c3d27eab6675d7ceae7b55c44fd48b18b92/samples/01-plain.jpg
[01h]: https://github.com/identity-md-launches/goal-3429-kekborn-portraits-v2-repaint/blob/faab8c3d27eab6675d7ceae7b55c44fd48b18b92/samples/01-harmonised.jpg
[02p]: https://github.com/identity-md-launches/goal-3429-kekborn-portraits-v2-repaint/blob/faab8c3d27eab6675d7ceae7b55c44fd48b18b92/samples/02-plain.jpg
[02h]: https://github.com/identity-md-launches/goal-3429-kekborn-portraits-v2-repaint/blob/faab8c3d27eab6675d7ceae7b55c44fd48b18b92/samples/02-harmonised.jpg
[03p]: https://github.com/identity-md-launches/goal-3429-kekborn-portraits-v2-repaint/blob/faab8c3d27eab6675d7ceae7b55c44fd48b18b92/samples/03-plain.jpg
[03h]: https://github.com/identity-md-launches/goal-3429-kekborn-portraits-v2-repaint/blob/faab8c3d27eab6675d7ceae7b55c44fd48b18b92/samples/03-harmonised.jpg
[04p]: https://github.com/identity-md-launches/goal-3429-kekborn-portraits-v2-repaint/blob/faab8c3d27eab6675d7ceae7b55c44fd48b18b92/samples/04-plain.jpg
[04h]: https://github.com/identity-md-launches/goal-3429-kekborn-portraits-v2-repaint/blob/faab8c3d27eab6675d7ceae7b55c44fd48b18b92/samples/04-harmonised.jpg
[05p]: https://github.com/identity-md-launches/goal-3429-kekborn-portraits-v2-repaint/blob/faab8c3d27eab6675d7ceae7b55c44fd48b18b92/samples/05-plain.jpg
[05h]: https://github.com/identity-md-launches/goal-3429-kekborn-portraits-v2-repaint/blob/faab8c3d27eab6675d7ceae7b55c44fd48b18b92/samples/05-harmonised.jpg
[06p]: https://github.com/identity-md-launches/goal-3429-kekborn-portraits-v2-repaint/blob/faab8c3d27eab6675d7ceae7b55c44fd48b18b92/samples/06-plain.jpg
[06h]: https://github.com/identity-md-launches/goal-3429-kekborn-portraits-v2-repaint/blob/faab8c3d27eab6675d7ceae7b55c44fd48b18b92/samples/06-harmonised.jpg
[07p]: https://github.com/identity-md-launches/goal-3429-kekborn-portraits-v2-repaint/blob/faab8c3d27eab6675d7ceae7b55c44fd48b18b92/samples/07-plain.jpg
[07h]: https://github.com/identity-md-launches/goal-3429-kekborn-portraits-v2-repaint/blob/faab8c3d27eab6675d7ceae7b55c44fd48b18b92/samples/07-harmonised.jpg
[08p]: https://github.com/identity-md-launches/goal-3429-kekborn-portraits-v2-repaint/blob/faab8c3d27eab6675d7ceae7b55c44fd48b18b92/samples/08-plain.jpg
[08h]: https://github.com/identity-md-launches/goal-3429-kekborn-portraits-v2-repaint/blob/faab8c3d27eab6675d7ceae7b55c44fd48b18b92/samples/08-harmonised.jpg
[09p]: https://github.com/identity-md-launches/goal-3429-kekborn-portraits-v2-repaint/blob/faab8c3d27eab6675d7ceae7b55c44fd48b18b92/samples/09-plain.jpg
[09h]: https://github.com/identity-md-launches/goal-3429-kekborn-portraits-v2-repaint/blob/faab8c3d27eab6675d7ceae7b55c44fd48b18b92/samples/09-harmonised.jpg
[10p]: https://github.com/identity-md-launches/goal-3429-kekborn-portraits-v2-repaint/blob/faab8c3d27eab6675d7ceae7b55c44fd48b18b92/samples/10-plain.jpg
[10h]: https://github.com/identity-md-launches/goal-3429-kekborn-portraits-v2-repaint/blob/faab8c3d27eab6675d7ceae7b55c44fd48b18b92/samples/10-harmonised.jpg
[11p]: https://github.com/identity-md-launches/goal-3429-kekborn-portraits-v2-repaint/blob/faab8c3d27eab6675d7ceae7b55c44fd48b18b92/samples/11-plain.jpg
[11h]: https://github.com/identity-md-launches/goal-3429-kekborn-portraits-v2-repaint/blob/faab8c3d27eab6675d7ceae7b55c44fd48b18b92/samples/11-harmonised.jpg
[12p]: https://github.com/identity-md-launches/goal-3429-kekborn-portraits-v2-repaint/blob/faab8c3d27eab6675d7ceae7b55c44fd48b18b92/samples/12-plain.jpg
[12h]: https://github.com/identity-md-launches/goal-3429-kekborn-portraits-v2-repaint/blob/faab8c3d27eab6675d7ceae7b55c44fd48b18b92/samples/12-harmonised.jpg
