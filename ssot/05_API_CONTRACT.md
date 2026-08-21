# SSOT 05 — API CONTRACT (v2.0)

JSON boundary uses `camelCase`; Python internals use `snake_case`.

Global envelope:

```json
{"success": true, "data": {}, "error": null}
```

or

```json
{"success": false, "data": null, "error": {"code": "STRING", "message": "string"}}
```

## 1. Geography endpoints

### `GET /geography/states`

Returns dynamic state list.

### `GET /geography/districts?stateId=...`

Returns districts for the selected state.

### `GET /geography/commodities?stateId=...&districtId=...`

Returns commodities known in that context. Frontend may still allow a broader commodity query if catalog policy permits; selected context is not a routing boundary.

## 2. `GET /crops`

Compatibility endpoint. Returns all active commodities and metadata:

```json
{
  "crops": [
    {
      "commodityId": "onion",
      "commodityName": "Onion",
      "commodityCategory": "Vegetable",
      "perishabilityClass": "MODERATELY_PERISHABLE",
      "cropGroup": "PERISHABLE"
    }
  ]
}
```

## 3. `POST /analysis/run`

### Request

```json
{
  "stateId": "maharashtra",
  "districtId": "pune",
  "latitude": 18.52,
  "longitude": 73.85,
  "commodityId": "onion",
  "quantityQuintals": 10,
  "radiusKm": 100,
  "transportRatePerQuintalPerKm": 2.5
}
```

Rules:
- state/district are required frontend context unless an explicit `coordinateOnly` mode is enabled later
- latitude/longitude are authoritative for radius search
- `quantityQuintals > 0`
- `radiusKm` default 100, bounded by config
- custom transport rate optional

### Response `AnalysisResult`

```json
{
  "commodity": {},
  "farmerContext": {
    "stateId": "maharashtra",
    "districtId": "pune",
    "latitude": 18.52,
    "longitude": 73.85,
    "quantityQuintals": 10,
    "radiusKm": 100
  },
  "search": {
    "candidateCount": 7,
    "searchStatus": "OK",
    "crossBoundaryCandidatesIncluded": true
  },
  "localMandi": {},
  "forecast": {
    "currentPrice": 0,
    "forecast1Day": 0,
    "forecast3Day": 0,
    "forecast7Day": 0,
    "expectedPeakPrice": 0,
    "peakDay": 0,
    "peakAlert": false,
    "historyWindowDays": 0,
    "historyClassification": "REAL|CACHED_REAL|SEEDED|DERIVED",
    "modelType": "LIVE|PRECOMPUTED"
  },
  "weather": {},
  "riskSummary": {},
  "nearbyMandis": [
    {
      "rank": 1,
      "mandi": {},
      "distanceKm": 0,
      "commodityAvailable": true,
      "currentPrice": 0,
      "forecast": {},
      "transportCostPerQuintal": 0,
      "totalTransportCost": 0,
      "expectedRevenue": 0,
      "netReturn": 0,
      "riskScore": 0,
      "riskLevel": "LOW",
      "riskAdjustedReturn": 0,
      "buyerSignal": {
        "activeBuyerCount": 0,
        "demandLevel": "LOW|MEDIUM|HIGH",
        "offerStrength": 0,
        "reliability": 0,
        "buyerSignalScore": 0,
        "classification": "SYNTHETIC",
        "sourceLabel": "Synthetic demo dataset"
      },
      "weatherImpact": {},
      "rankingBreakdown": {
        "normalizedRiskAdjustedReturn": 0,
        "buyerSignalScore": 0,
        "dataQualityScore": 0,
        "topFactors": []
      },
      "rankingScore": 0,
      "dataClassification": {}
    }
  ],
  "dataProvenance": {
    "coverage": {},
    "buyerDataClassification": "SYNTHETIC"
  },
  "decision": {
    "baseDecision": "SELL_NOW",
    "finalRecommendation": "SELL_NOW",
    "riskOverrideApplied": false,
    "recommendedMandi": {},
    "reasonCodes": [],
    "humanReadableReason": "",
    "decisionConfidence": 0.0
  }
}
```

`nearbyMandis` is dynamic length.

## 4. `GET /analysis/nearby-mandis`

Optional diagnostic/UI helper. Query:
- latitude
- longitude
- commodityId
- radiusKm

Returns eligible mandis with name, state, district, coordinates, distance, commodity availability and current data classification. It does not perform ranking.

This endpoint is useful for map/list previews but `POST /analysis/run` remains the canonical end-to-end analysis endpoint.

## 5. Judge-support fields

The canonical analysis response must make the following directly available to the frontend:
- `forecast.peakAlert`, `expectedPeakPrice`, `peakDay`
- historical basis/provenance metadata
- weather classification and source label
- per-mandi active buyer count and buyer component metrics
- per-mandi ranking breakdown
- base decision, final recommendation and override reason

These fields are not optional presentation extras; they are required for the judge-visible proof defined in SSOT 00.

## 6. Errors

- `422 INVALID_INPUT`
- `404 COMMODITY_NOT_FOUND`
- `404 GEOGRAPHY_CONTEXT_NOT_FOUND`
- `404 NO_ELIGIBLE_MANDI_IN_RADIUS` only for the helper endpoint; the main analysis endpoint returns graceful `searchStatus`
- `500 INTERNAL_ERROR`

## 7. Backward compatibility

The old v1 `cropId` is replaced by `commodityId` at the canonical v2 boundary. Compatibility adapters may accept `cropId` internally during migration, but new frontend code must use `commodityId`.
