# ML Boundary & Integration Guide (FasalDisha)

## Role: AI / ML Engineer

### Frozen Handoff Contract
The backend calls `ml.forecast_engine.get_forecast(commodity_id, mandi_id, as_of_date, current_price_override)` and expects a `ForecastOutput` object matching `app.schemas.forecast.ForecastOutput`.

### Required Output Fields (P0)
1. `currentPrice`: float
2. `forecast1Day`: float
3. `forecast3Day`: float
4. `forecast7Day`: float
5. `expectedPeakPrice`: float
6. `peakDay`: int (day index 1-7)
7. `peakAlert`: boolean (`(expectedPeakPrice - currentPrice) / currentPrice >= 0.05`)
8. `dailyForecast`: array of `{ "day": int, "predictedPrice": float, "confidence": float }`
9. `forecastConfidence`: float (0.30 - 0.95)
10. `modelType`: `"LIVE"` | `"PRECOMPUTED"`
11. `historyWindowDays`: int
12. `historyClassification`: `"REAL"` | `"CACHED_REAL"` | `"SEEDED"` | `"DERIVED"`
13. `historySourceLabel`: string
14. `forecastScope`: `"DIRECT_MODEL"` | `"DERIVED_PROPAGATION"`

### Active Fallback
- `ml/precomputed_forecasts.json` contains pre-generated 7-day curves for Onion, Tomato, Potato, Wheat, Soybean, Mustard, and Cotton.
- When no live model is present or training is ongoing, the system seamlessly serves these contract-compliant forecasts.
