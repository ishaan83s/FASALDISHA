# SSOT 03 — RETURN, RISK, RANKING & DECISION ENGINE (v2.0)

## 1. Configurable constants

Single source: `backend/app/config/constants.py`

```python
RADIUS_KM_DEFAULT = 100
RADIUS_KM_MAX = 300
MAX_NEARBY_MANDIS_RETURNED = 20

TRANSPORT_RATE_PER_QUINTAL_PER_KM = 2.5

RISK_WEIGHTS = {
    "weather": 0.30,
    "official_alert": 0.25,
    "transport": 0.20,
    "perishability": 0.15,
    "model_uncertainty": 0.10,
}

BUYER_SIGNAL_WEIGHTS = {
    "demand": 0.40,
    "availability": 0.20,
    "offer_strength": 0.25,
    "reliability": 0.15,
}

RANKING_WEIGHTS = {
    "risk_adjusted_return": 0.70,
    "buyer_signal": 0.20,
    "data_quality": 0.10,
}

TRAVEL_SIGNIFICANCE_THRESHOLD = 0.05
HOLD_SIGNIFICANCE_THRESHOLD = 0.05
HIGH_RISK_OVERRIDE_THRESHOLD = 51
CRITICAL_RISK_OVERRIDE_THRESHOLD = 76
PEAK_ALERT_THRESHOLD = 0.05

# P0 demo fixture: must produce a deterministic visible override without requiring a live API.
SEEDED_RISK_OVERRIDE_SCENARIO_ENABLED = True
```

These values are hackathon defaults, not agricultural truths.

## 2. Perishability behavior

| Class | Hold horizon | Urgency/risk |
|---|---|---|
| HIGHLY_PERISHABLE | shortest | highest |
| MODERATELY_PERISHABLE | medium | medium |
| NON_PERISHABLE | longest | lowest |

Constants must be configurable.

## 3. Distance and transport

```text
distanceKm = Haversine(farmerCoordinates, mandiCoordinates)

transportCostPerQuintal =
    distanceKm × configuredTransportRatePerQuintalPerKm

totalTransportCost =
    transportCostPerQuintal × quantityQuintals
```

If the user provides a custom rate, it overrides the default only for that analysis.

## 4. Return model

For each mandi:

```text
forecastedPrice = forecast7Day or selected recommendation horizon
expectedRevenue = forecastedPrice × quantityQuintals
netReturn = expectedRevenue − totalTransportCost
```

This is an estimated comparative return, not guaranteed profit.

## 5. Risk score

Each mandi receives a `riskScore` from 0–100.

Signal components:
- weather risk
- official alert risk
- transport risk
- perishability/holding risk
- model uncertainty

When a signal is unavailable, its weight is redistributed across available signals and `riskDataCompleteness` is reported.

Bands:
- 0–25 `LOW`
- 26–50 `MODERATE`
- 51–75 `HIGH`
- 76–100 `CRITICAL`

## 6. Risk-adjusted return

For v2.0 P0:

```text
riskPenalty = netReturn × (riskScore / 100) × RISK_PENALTY_FACTOR
riskAdjustedReturn = netReturn − riskPenalty
```

`RISK_PENALTY_FACTOR` is configurable and defaults to `0.20`.

This is a transparent heuristic ranking mechanism, not a financial risk model.

## 7. Buyer signal

For the current prototype, buyers are **not discovered from a live marketplace**. They are read from the synthetic buyer dataset filtered by `(mandi_id, commodity_id, active=true)`. This must be stated in the product/demo.

Synthetic buyer data contributes:

```text
activeBuyerCount
demandLevel
offerStrength
reliability
→ buyerSignalScore (0–100)
```

The classification `SYNTHETIC`, source label, active-buyer count and component metrics are carried to the response. Buyer records are an input to mandi ranking; they are not presented as verified buyer offers.

## 8. Ranking

Normalize ranking inputs over the current eligible candidate set:

```text
rankingScore =
  0.70 × normalizedRiskAdjustedReturn
+ 0.20 × buyerSignalScore
+ 0.10 × dataQualityScore
```

If all risk-adjusted returns are equal, their normalized value is `50`.

Results are sorted descending. The frontend must render all returned candidates or paginate/expand without assuming a fixed count.

For judge explainability, each candidate must expose a ranking breakdown containing at least `normalizedRiskAdjustedReturn`, `buyerSignalScore`, `dataQualityScore`, `rankingScore`, and human-readable top factors. This makes it possible to answer why mandi A ranked above mandi B.

## 9. Base decision

```text
If best non-local risk-adjusted return beats local by threshold:
    baseDecision = TRAVEL
Else if hold return beats sell-now by threshold
    and confidence/horizon/perishability permit:
    baseDecision = HOLD
Else:
    baseDecision = SELL_NOW
```

## 10. Risk override

Risk is evaluated after the base decision.

Examples:

```text
HOLD + HIGH/CRITICAL weather/alert risk
    → SELL_EARLY_DUE_TO_RISK

TRAVEL + severe route/weather risk
    → SELL_AT_RECOMMENDED_MANDI (closer safe candidate)
      OR AVOID_MANDI_OR_ROUTE

SELL_NOW + no override
    → SELL_NOW
```

The response must contain:
- `baseDecision`
- `finalRecommendation`
- `riskOverrideApplied`
- reason codes

## 11. Reason codes

Core codes:
- `TRAVEL_GAIN_ABOVE_THRESHOLD`
- `HOLD_GAIN_ABOVE_THRESHOLD`
- `FORECAST_CONFIDENCE_LOW`
- `PERISHABILITY_URGENCY_HIGH`
- `WEATHER_RISK_HIGH`
- `OFFICIAL_ALERT_ACTIVE`
- `TRANSPORT_RISK_HIGH`
- `RISK_OVERRIDE_SELL_EARLY`
- `RISK_OVERRIDE_AVOID_ROUTE`
- `NO_ELIGIBLE_MANDI_IN_RADIUS`
- `SELL_NOW_DEFAULT`

## 12. Peak alert

The decision layer receives peak metadata and preserves it in the response. `peakAlert` is advisory and is triggered by the configured threshold defined in the ML SSOT. A peak alert alone must not override a high perishability or high-risk decision.

## 13. Confidence

Keep separate:
- `forecastConfidence`
- `decisionConfidence`

Decision confidence is a support score based on evidence strength, margin, data completeness, and risk consistency. It is not a probability guarantee.
