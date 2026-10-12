{
  "direction": "short",
  "leverage": 500,
  "take_profit_pct": 0.08,
  "take_profit_price": 84130.14199999999,
  "liquidation_price_estimate": 84365.895,
  "max_hold_minutes": 15,
  "confidence": 0.54,
  "regime": "ranging",
  "key_levels": {
    "support": 84100,
    "resistance": 84294
  },
  "entry_mid": 84197.5,
  "data_time_utc": "2026-10-12T07:12:55.188445+00:00",
  "reasoning": "Hyperliquid live data (https://api.hyperliquid.xyz/info; archived in market-data.json) show a rejection of the 84294 high, followed by a 07:11 UTC closed one-minute candle at 84135; the live 84197.5 mid is a rebound within that consolidation. Displayed ask depth is 110.10 BTC versus 37.39 BTC of bids across the returned 20 levels, and the latest ten prints are sell-dominated by volume, supporting a low-confidence short inference despite the broader upward trend. I choose 500x for the widest permitted adverse-price buffer and a 0.08% target above 84100 support, with a 15-minute hard exit; the target distance is about 1.76 times the closed-candle one-minute ATR of 38.29.",
  "risks": "A renewed breakout through 84294 could squeeze the short toward the approximate 84365.895 liquidation level; displayed liquidity can cancel and the broader trend is upward. PaperTrade fees and maintenance-margin rules were not supplied, so actual liquidation may occur earlier and net profitability at the target is uncertain."
}
