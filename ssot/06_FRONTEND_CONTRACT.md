# SSOT 06 — FRONTEND CONTRACT (v2.0)

## 1. Analysis form

Required input flow:

1. State
2. District
3. Farmer location
   - browser/device geolocation preferred
   - map pin if implemented
   - deterministic seeded/demo fallback
4. Commodity
5. Quantity
6. Search radius (default 100 km)
7. Optional transport rate

State/district are context selectors. The actual coordinate is what powers nearby search.

No frontend hard-codes:
- states
- districts
- commodities
- mandis
- number of ranked results

## 2. Location behavior

All entry modes write the same `{latitude, longitude}` state.

If geolocation fails, the UI must:
- explain permission/availability issue
- retain state/district
- offer pin/fallback selection

## 3. Results dashboard

### `RecommendationBanner`

Shows:
- final recommendation
- base decision
- recommended mandi
- decision confidence
- risk override if applied

### `ForecastPanel`

Shows:
- current price
- 1-day
- 3-day
- 7-day forecast
- peak price/day
- forecast confidence
- model type
- history window/provenance label
- peak alert state

### `MandiComparisonList`

Renders one card per returned candidate, sorted as received.

Each card shows:
- rank
- mandi/state/district
- distance
- current price
- forecasted price
- total transport cost
- expected revenue
- net return
- risk score/level
- risk-adjusted return
- active buyer count
- buyer demand/offer strength/reliability summary
- buyer signal score with synthetic label
- weather flag
- recommended badge

No fixed count. If 1 candidate exists, render 1. If 10 exist, render 10 or an expandable list without truncating the data contract.

### `RiskPanel`

Shows:
- risk score
- band
- active weather/official alert factors
- data classification
- whether a risk override changed the base decision
- source label/classification for active weather or alert evidence

### `WeatherAlert`

Near the recommendation:
- green LOW
- yellow MEDIUM
- red HIGH/CRITICAL

If unavailable, explicitly say weather signal unavailable/not active rather than pretending no risk exists.

## 4. Copy rules

Use:
- "Estimated revenue"
- "Estimated net return"
- "Risk-adjusted comparison"

Do not use guaranteed "profit" unless the system actually models all farmer-specific costs.

Synthetic buyer data must be visibly labeled.

## 5. Judge proof UI

The results page must include a compact, always-visible evidence area or expandable panel that answers:

- Why is this mandi ranked first?
- How many active buyer records contributed and what signals were used?
- Is buyer data synthetic?
- What weather/alert data is active and what is its source classification?
- Did risk override the base decision?
- What historical basis/model type supports the forecast?
- Is a peak-price alert active?

This may reuse existing `ReasoningPanel`, `RiskPanel`, and candidate-card components; no extra page is required.

## 6. API client

Centralized typed client only. Components do not call `fetch()` directly.
