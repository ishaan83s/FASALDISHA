# SSOT 00 — MASTER PRODUCT SSOT (v2.0)

**Status:** FINAL / SUPERSEDES v1.0**
**Project:** AI-Driven Crop Price Forecasting & Market Routing App

## 1. Product definition

The product answers:

> **Given my commodity, quantity, location, forecast, transport cost and current risks, where should I sell and should I sell now or wait?**

This is not a price dashboard. It is a **forecasting + market-routing + risk-aware decision system**.

### 1.1 Canonical flow

```text
Farmer
  ↓
State + District + Actual Coordinates
Commodity + Quantity + Radius
  ↓
LOCATION ENGINE
  ↓
All eligible mandis within radius
  ↓                 ↘
Market data          ML forecast
  ↓                   ↓
Weather + alerts + perishability + transport + confidence
  ↓
Risk engine
  ↓
Expected return / risk-adjusted return
  ↓
Ranked mandi list
  ↓
Final recommendation + reasoning + confidence
```

### 1.2 Geographic scope

Initial target coverage:
- Rajasthan
- Gujarat
- Maharashtra

Hierarchy:

```text
State → District → Mandi/APMC → Available Commodities
```

The hierarchy is used for browsing and input assistance. **Recommendation search is coordinate-based and may cross district/state boundaries.**

Default radius: `100 km`, configurable.

### 1.3 Decision model

Base market decision:
- `SELL_NOW`
- `HOLD`
- `TRAVEL`

Final user-facing recommendation may be:
- `SELL_NOW`
- `HOLD`
- `SELL_AT_RECOMMENDED_MANDI`
- `SELL_EARLY_DUE_TO_RISK`
- `AVOID_MANDI_OR_ROUTE`

The final decision may be a risk override of the base decision. The system always reports both `baseDecision` and `finalRecommendation`.

## 2. Problem Statement 9 alignment

The official problem asks for:
- 7–14 day mandi price forecasting
- historical APMC data
- weather forecasts and seasonal demand where available
- best-selling location within 100 km
- transport-adjusted optimization
- peak-price alerts

v2.1 explicitly supports all of these. Round 2 P0 guarantees a 7-day forecast with 1/3/7-day horizons, historical-price provenance, peak detection, and a deterministic `peakAlert` when the forecast peak is materially above the current price. The contract supports extension to day 14 without frontend redesign.

## 3. P0 / P1 / P2

### P0 — must be integrated

- State and district context
- Actual latitude/longitude from geolocation, pin, or deterministic fallback
- Commodity selection
- Quantity in quintals
- Default/configurable search radius
- Dynamic eligible-mandi search
- Cross-district/cross-state radius search
- Current price and forecast fields per ranked mandi
- 1/3/7-day forecast outputs
- Expected peak price/day
- Historical-price provenance/summary for forecast explainability
- Peak alert when configured threshold is met
- Transport cost and expected revenue
- Net return and risk-adjusted return
- Commodity category + 3-level perishability metadata
- Synthetic buyer intelligence, visibly labeled, with active-buyer count and ranking inputs exposed
- Weather/risk contract with honest REAL/SEEDED/UNAVAILABLE status
- At least one deterministic seeded risk-override demo scenario available in P0
- Rule-based risk score
- Ranked dynamic list, not fixed 1/3 cards
- Base decision + risk-aware final recommendation
- End-to-end frontend/backend integration

### P1

- Complete 14-day forecast where validated
- Live official weather/meteorological alerts
- Historical weather feature comparison
- Interactive map
- richer route disruption sources
- scheduled alerts

### P2

- authentication
- farmer history
- exact vehicle routing
- retraining infrastructure
- verified buyer marketplace
- multilingual expansion

## 4. Judge-feedback traceability

| Need | v2.0 implementation |
|---|---|
| Weather impact | `weather_service` + `risk_service`, explicit source classification, visible alert flag, and deterministic seeded override scenario when live weather is unavailable |
| Group-wise segregation | 3-level perishability metadata maps to the original PERISHABLE/NON_PERISHABLE group and visibly affects holding urgency/risk |
| Buyer intelligence | synthetic buyer signals influence mandi ranking transparently; active-buyer count, demand, offer strength, reliability, source and synthetic classification are visible |
| Best location | distance + transport + forecast + buyer signal + risk-adjusted return |
| Market routing | all eligible mandis within radius, including neighboring districts/states |
| Quantity economics | expected revenue and total transport cost are quantity-aware |

## 5. Judge-visible proof requirements

The following must be demonstrable in the integrated P0, not merely present in schema/code:

1. **Weather:** one `UNAVAILABLE` or `REAL` state plus one deterministic `SEEDED` severe-weather scenario that visibly changes or confirms the recommendation; source label must be shown.
2. **Group-wise segregation:** run at least one perishable and one non-perishable commodity and show the group/perishability explanation affecting urgency or holding logic.
3. **Buyer intelligence:** show active buyer count plus demand, offer strength and reliability; explicitly state that the records are synthetic and show how the buyer signal contributes to ranking.
4. **Best location:** show at least two eligible mandis and a per-mandi comparison of forecast opportunity, distance/transport, risk-adjusted return and buyer signal; the recommended mandi must be explainable from these fields.
5. **Historical/forecast credibility:** expose the history window or provenance used for the forecast and the forecast model/fallback classification.
6. **Peak-price value:** show current price, expected peak price, peak day and whether a peak alert is active.

A feature that exists only as an unused service or database column does not count as judge coverage.

## 6. Non-negotiable honesty rules

- Synthetic buyers are never called verified buyers.
- Seeded weather is never called live weather.
- A precomputed forecast is labeled `PRECOMPUTED`.
- Risk score is a support score, not a guaranteed probability.
- Net return is an estimate based on configured assumptions, not guaranteed profit.
- Full three-state coverage is claimed only if the loaded geography/mandi catalog actually contains that coverage.

## 7. Final architecture rule

Keep the system modular, but do not create microservices for the hackathon. `location`, `forecast`, `weather`, `risk`, `transport`, and `ranking` are **modules/services inside one FastAPI process**.
