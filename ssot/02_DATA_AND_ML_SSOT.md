# SSOT 02 — DATA, ML & WEATHER SSOT (v2.0)

## 1. Data classifications

Every externally derived value has one classification:

- `REAL`
- `CACHED_REAL`
- `SEEDED`
- `SYNTHETIC`
- `DERIVED`
- `UNAVAILABLE`

No value may silently move between classes.

## 2. Data sources and fallback

| Data | Preferred | Fallback |
|---|---|---|
| Geography/APMC catalog | official/public registry | seeded representative catalog |
| Historical prices | Agmarknet/data.gov or cached public dataset | deterministic seeded history |
| eNAM/arrival/demand | public official data if available | omitted from P0 model or labeled derived proxy |
| Weather | official/API source | seeded event or `UNAVAILABLE` |
| Buyer intelligence | synthetic demo dataset | synthetic demo dataset |
| Forecast | live local model | precomputed contract-compatible output |

## 3. Geography coverage model

Canonical geography scope is Rajasthan, Gujarat, Maharashtra.

Tables/catalogs must support:
- state
- district
- mandi
- commodity availability

The architecture is complete-coverage capable. The actual loaded coverage is exposed as metadata and must not be overstated.

## 4. Commodity metadata

Each commodity has:
- `commodity_id`
- name
- category
- `perishability_class`

Allowed classes:
- `HIGHLY_PERISHABLE`
- `MODERATELY_PERISHABLE`
- `NON_PERISHABLE`

Examples:
- Tomato → Vegetable → HIGHLY_PERISHABLE
- Onion → Vegetable → MODERATELY_PERISHABLE
- Wheat → Cereal → NON_PERISHABLE

A legacy two-group field may be derived:
- HIGHLY/MODERATELY → `PERISHABLE`
- NON → `NON_PERISHABLE`

## 5. Forecast contract

Canonical service interface:

```text
get_forecast(commodity_id, mandi_id, as_of_date?) -> ForecastOutput
```

Minimum output:

```json
{
  "currentPrice": 2200,
  "forecast1Day": 2250,
  "forecast3Day": 2350,
  "forecast7Day": 2450,
  "expectedPeakPrice": 2500,
  "peakDay": 5,
  "dailyForecast": [],
  "forecastConfidence": 0.71,
  "modelType": "LIVE"
}
```

`dailyForecast` is required for charting and peak selection. P0 is 7 days. The model/output schema may additionally provide day 14 later.

Each forecast response must also carry enough provenance to explain the historical basis used, at minimum `historyWindowDays` and `historyClassification`. P0 does not require returning the full historical series from the ML service, but the analysis response may expose a short chartable history when available.

## 6. ML design

P0 model remains a pooled commodity model rather than one independent model per mandi if data is sparse.

Minimum features:
- lag prices
- rolling mean
- day/week seasonality features
- mandi identifier/category
- time index

Optional future features:
- weather history
- arrivals
- demand/transaction signals

Do not claim optional features are active unless they actually enter the model.

## 7. Per-mandi forecast behavior

Preferred: forecast each mandi through the same model interface.

P0 fallback when only one commodity-level/local curve is available:

```text
growth_ratio[h] = local_forecast[h] / local_current_price
mandi_forecast[h] = mandi_current_price × growth_ratio[h]
```

Mark propagated forecasts:
- `forecastScope: "DIRECT_MODEL"` or
- `forecastScope: "DERIVED_PROPAGATION"`

## 8. Historical-price provenance and peak alert

The system must preserve that forecasts are based on a historical price source or a deterministic seeded/precomputed substitute. Minimum metadata:

```text
historyWindowDays
historyClassification
historySourceLabel
```

Peak alert rule for P0:

```text
peakGainRatio = (expectedPeakPrice - currentPrice) / max(currentPrice, epsilon)
peakAlert = peakGainRatio >= PEAK_ALERT_THRESHOLD
```

`PEAK_ALERT_THRESHOLD` is configurable. The alert is advisory, not a guarantee that the peak will occur.

## 9. Weather and alerts

Weather service returns:

```json
{
  "status": "ACTIVE|UNAVAILABLE",
  "impactLevel": "LOW|MEDIUM|HIGH|CRITICAL",
  "events": [],
  "classification": "REAL|SEEDED|UNAVAILABLE"
}
```

Possible event inputs:
- heavy rain
- flood
- cyclone
- heatwave
- hail
- other severe meteorological event
- future transport disruption

A seeded event must say so in `sourceLabel`.

## 10. Forecast confidence

Confidence is a support metric derived from validation or fallback heuristics. It is not presented as a guaranteed probability.

Recommended live metric:

```text
MAPE = mean(abs(actual - predicted) / actual)
forecastConfidence = clip(1 - MAPE, 0.30, 0.95)
```

Fallback confidence must be labeled heuristic/conservative in internal metadata.
