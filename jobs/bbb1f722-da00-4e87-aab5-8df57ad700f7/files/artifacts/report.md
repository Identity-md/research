# Swarm Pepe #1043 rarity

**As of 2026-09-30.** The explorer currently serves #1043 with `Status: Unrevealed`; its metadata contains no Skin, Eyes, Mouth, Hat, or Accessory traits. This matches `SwarmPepe.tokenURI(uint256)`: while `seedOf[tokenId] == 0`, it returns the placeholder image and an Unrevealed attribute. `SwarmPepe.reveal(uint256[])` later stores a seed and emits `Revealed`; the renderer then supplies the five attributes. [#1043 metadata](https://eth.blockscout.com/api/v2/tokens/0x999ce0ce8c5f7661e0c74a568ffe27ceb9177bdb/instances/1043) · [SwarmPepe verified source](https://etherscan.io/address/0x999ce0ce8c5f7661e0c74a568ffe27ceb9177bdb#code) · [PixelArt verified source](https://etherscan.io/address/0x07Fd9841eEB6a359EfB30f861D59bFa1f6B03FcA#code)

## Results

| Measure | Probability | Expected / rank |
|---|---:|---:|
| #1043 exact five-trait combo | N/A | N/A |
| Gold + Crown, other traits ignored | 0.03000003% | 1.5000 / 1 of 10 floor pairs |

The first row is unavailable because #1043 is unrevealed, not because its traits were inferred from an external rarity rank. The pair row is a model-based probability from the on-chain selection mechanism and assumes hash seeds are uniform; expected counts use a full `MAX_SUPPLY = 5000` mint.

### Floor-pair ranking

Each row pairs the lowest-weight value in two different renderer categories. Values in the last column are expected counts in 5,000 seeds. Gold + Crown ranks rarest.

| Rank | Floor pair | Probability | Expected / 5,000 |
|---:|---|---:|---:|
| 1 | Gold + Crown | 0.03000003% | 1.5000 |
| 2 | Gold + Vape | 0.05000305% | 2.5002 |
| 3 | Gold + VR | 0.07031250% | 3.5156 |
| 4 | Gold + Mole | 0.08000000% | 4.0000 |
| 5 | Vape + Crown | 0.15625000% | 7.8125 |
| 6 | VR + Crown | 0.20999146% | 10.4996 |
| 7 | Crown + Mole | 0.24609375% | 12.3047 |
| 8 | VR + Vape | 0.35546875% | 17.7734 |
| 9 | Vape + Mole | 0.40000916% | 20.0005 |
| 10 | VR + Mole | 0.56000030% | 28.0000 |

## On-chain calculation

`PixelArt` defines `W_SKIN = 3c 12 0c 06 03 01`, `W_EYES = 26 10 0d 09 07 09 08`, `W_MOUTH = 28 14 0f 0c 08 05`, `W_HAT = 1e 0d 0b 0b 0b 08 0d 03`, and `W_ACC = 3a 15 0d 08` (hex bytes, each vector totals 100). Its `attributes(uint256)` calls `_pick` on `seed >> 8`, `>> 16`, `>> 24`, `>> 32`, and `>> 40`; `_pick` takes the residue modulo 100 and selects the interval given by cumulative weights. `_skinName` maps the final Skin slot to Gold (weight 1); `_hatName` maps the final Hat slot to Crown (weight 3). Thus their marginal product would be `1% × 3% = 0.03%`, or 1.5 expected in 5,000.

The report accounts for the fact that these selectors are byte-shifted views of one seed rather than independent draws. For each adjacent selector, if its higher-shift residue is `u`, the next lower-shift residue is `(56u + b) mod 100`, where `b` is the intervening 0–255 seed byte. The ranking probabilities use this transition under a uniform 256-bit seed assumption; the slight differences from multiplying marginal weights are due to that correlation. The 10 rows cover every unordered pair among the five category floors: Gold (Skin, 1), VR (Eyes, 7), Vape (Mouth, 5), Crown (Hat, 3), and Mole (Accessory, 8). `MAX_SUPPLY` is the contract constant 5000.

## Evidence limits

- **Observed:** the explorer’s #1043 metadata response says `Unrevealed` and includes only the Status attribute.
- **Source facts:** the verified contract and renderer expose the functions and constants named above; `tokenURI` branches on whether the stored seed is zero.
- **Inference:** probability and expected-count figures assume Keccak-derived seeds behave uniformly. They are not empirical frequencies and do not assert a finalized trait for #1043.
- **Unanswered:** #1043’s eventual exact five-trait combo and its combo-specific probability/expected count cannot be stated until its on-chain reveal supplies a nonzero seed.
