# FasalDisha API Contract Reference (v2.1 Frozen)

## 1. Global Envelope Shape
All API responses strictly adhere to the unified envelope:

```json
{
  "success": true,
  "data": { ... },
  "error": null
}
```

Or on controlled failure:
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "INVALID_INPUT | NOT_FOUND | INTERNAL_ERROR",
    "message": "Human-readable description"
  }
}
```

---

## 2. Endpoints Summary

| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Liveness & database connection health check |
| `GET` | `/geography/states` | List active states (Rajasthan, Gujarat, Maharashtra) |
| `GET` | `/geography/districts?stateId=...` | List districts in selected state context |
| `GET` | `/geography/commodities?stateId=...&districtId=...` | List available commodities & perishability metadata |
| `GET` | `/crops` | Backward compatibility crop list endpoint |
| `POST` | `/analysis/run` | **Canonical Analysis Endpoint** (full routing, economics & decision) |
| `GET` | `/analysis/nearby-mandis` | Diagnostic / preview helper for nearby mandis |

---

## 3. Canonical Analysis Request (`POST /analysis/run`)

```json
{
  "stateId": "maharashtra",
  "districtId": "pune",
  "latitude": 18.5204,
  "longitude": 73.8567,
  "commodityId": "onion",
  "quantityQuintals": 20,
  "radiusKm": 100,
  "transportRatePerQuintalPerKm": 2.5
}
```

### Request Fields:
- `stateId` *(string, required)*: Geographic context state
- `districtId` *(string, required)*: Geographic context district
- `latitude` *(float, required)*: Authoritative farmer GPS coordinate
- `longitude` *(float, required)*: Authoritative farmer GPS coordinate
- `commodityId` *(string, required)*: e.g. `onion`, `tomato`, `wheat`, `potato`, `soybean`, `mustard`, `cotton`
- `quantityQuintals` *(float > 0, required)*: Batch volume in quintals
- `radiusKm` *(float 1-300, optional, default: 100)*: Search radius
- `transportRatePerQuintalPerKm` *(float > 0, optional, default: 2.5)*: Logistics rate override in INR/quintal/km

---

## 4. Canonical Response Structure (`AnalysisResult`)

```json
{
  "commodity": {
    "commodityId": "onion",
    "commodityName": "Onion",
    "commodityCategory": "Vegetable",
    "perishabilityClass": "MODERATELY_PERISHABLE",
    "cropGroup": "PERISHABLE",
    "unit": "quintal",
    "active": true
  },
  "farmerContext": {
    "stateId": "maharashtra",
    "districtId": "pune",
    "latitude": 18.5204,
    "longitude": 73.8567,
    "quantityQuintals": 20.0,
    "radiusKm": 100.0
  },
  "search": {
    "candidateCount": 6,
    "searchStatus": "OK",
    "crossBoundaryCandidatesIncluded": false
  },
  "localMandi": { ... },
  "forecast": {
    "currentPrice": 2350.0,
    "forecast1Day": 2390.0,
    "forecast3Day": 2480.0,
    "forecast7Day": 2620.0,
    "expectedPeakPrice": 2650.0,
    "peakDay": 6,
    "peakAlert": true,
    "dailyForecast": [ ... ],
    "forecastConfidence": 0.78,
    "modelType": "PRECOMPUTED",
    "historyWindowDays": 45,
    "historyClassification": "SEEDED",
    "historySourceLabel": "Agmarknet Historical / Seeded Seasonal Baseline",
    "forecastScope": "DIRECT_MODEL"
  },
  "weather": {
    "status": "ACTIVE",
    "impactLevel": "HIGH",
    "events": [ ... ],
    "classification": "SEEDED",
    "sourceLabel": "Deterministic seeded severe weather scenario for judge demo"
  },
  "riskSummary": {
    "overallRiskScore": 55.0,
    "riskLevel": "HIGH",
    "dataCompleteness": 1.0,
    "riskFactors": [ ... ]
  },
  "nearbyMandis": [
    {
      "rank": 1,
      "mandi": {
        "mandiId": "mandi_pune_chakan",
        "mandiName": "APMC Chakan (Khed)",
        "stateId": "maharashtra",
        "districtId": "pune",
        "latitude": 18.7562,
        "longitude": 73.8596,
        "active": true,
        "locationClassification": "REAL"
      },
      "distanceKm": 26.22,
      "commodityAvailable": true,
      "currentPrice": 2400.0,
      "forecast": { ... },
      "transportCostPerQuintal": 65.55,
      "totalTransportCost": 1311.0,
      "expectedRevenue": 53516.0,
      "netReturn": 52205.0,
      "riskScore": 55.0,
      "riskLevel": "HIGH",
      "riskAdjustedReturn": 46462.45,
      "buyerSignal": {
        "activeBuyerCount": 4,
        "demandLevel": "MEDIUM",
        "offerStrength": 77.0,
        "reliability": 82.5,
        "buyerSignalScore": 73.6,
        "classification": "SYNTHETIC",
        "sourceLabel": "Synthetic demo dataset (Aggregated mandi buyer signals)"
      },
      "weatherImpact": { ... },
      "rankingBreakdown": {
        "normalizedRiskAdjustedReturn": 100.0,
        "buyerSignalScore": 73.6,
        "dataQualityScore": 90.0,
        "topFactors": [
          "High risk-adjusted net return",
          "Strong buyer demand (4 active traders)",
          "Proximity minimizes logistics cost"
        ],
        "rankingScore": 93.7
      },
      "rankingScore": 93.7,
      "dataClassification": {
        "price": "SEEDED",
        "forecast": "PRECOMPUTED",
        "buyers": "SYNTHETIC",
        "weather": "SEEDED"
      }
    }
  ],
  "dataProvenance": {
    "coverage": {
      "supportedStates": ["Rajasthan", "Gujarat", "Maharashtra"],
      "activeCommodity": "Onion",
      "radiusKm": 100.0,
      "candidatesFound": 6
    },
    "buyerDataClassification": "SYNTHETIC"
  },
  "decision": {
    "baseDecision": "HOLD",
    "finalRecommendation": "SELL_EARLY_DUE_TO_RISK",
    "riskOverrideApplied": true,
    "recommendedMandi": { ... },
    "reasonCodes": [
      "HOLD_GAIN_ABOVE_THRESHOLD",
      "WEATHER_RISK_HIGH",
      "RISK_OVERRIDE_SELL_EARLY"
    ],
    "humanReadableReason": "Although a 7-day price gain (+11.5%) was forecasted, high meteorological/transit risk (Score: 55.0/100) overrides holding. Recommend selling early at APMC Chakan (Khed) to prevent spoilage and logistical loss.",
    "decisionConfidence": 0.88
  }
}
```
