# SSOT 01 — SYSTEM ARCHITECTURE (v2.0)

## 1. Architecture

```text
React + Vite + TypeScript
        ↓
     FastAPI
        ↓
   analysis_service
 ┌──────┼──────────────────────────────────────┐
 ↓      ↓          ↓        ↓       ↓          ↓
geo  mandi_data  forecast weather  risk   decision/ranking
 │      │          │        │       │          │
 └──────┴──────────┴────────┴───────┴──────────┘
                    ↓
             PostgreSQL / fallback
```

One FastAPI application. No separate ML server is required.

## 2. Service boundaries

`analysis_service` is the only top-level composer:

1. validate input
2. resolve state/district context
3. find commodity-eligible nearby mandis
4. retrieve market prices
5. retrieve/derive forecasts
6. calculate distance and transport
7. resolve weather/alert signals
8. calculate mandi risk
9. calculate returns and ranking
10. compute base decision
11. apply risk override
12. return ranked results

No lateral service calls should bypass the orchestrator except pure utility functions.

## 3. Repository structure

```text
backend/
  app/
    api/routes/
      health.py
      crops.py
      geography.py
      analysis.py
    schemas/
      geography.py
      analysis.py
      common.py
    services/
      analysis_service.py
      geography_service.py
      mandi_service.py
      market_data_service.py
      forecast_service.py
      weather_service.py
      risk_service.py
      transport_service.py
      ranking_service.py
      decision_engine.py
      buyer_service.py
    config/constants.py
    db/
      models.py
      session.py
      seed/
  ml/
    features.py
    train.py
    model_store/
    precomputed_forecasts.json
  scripts/
    ingest_geography_catalog.py
    generate_seed_prices.py

frontend/src/
  pages/
    AnalysisFormPage.tsx
    ResultsDashboardPage.tsx
  components/
    GeographySelector.tsx
    LocationPicker.tsx
    CommoditySelector.tsx
    RecommendationBanner.tsx
    ForecastChart.tsx
    MandiComparisonList.tsx
    MandiComparisonCard.tsx
    RiskPanel.tsx
    WeatherAlert.tsx
    ReasoningPanel.tsx
  api/client.ts
  types/
```

Logical module names may vary only if the frozen API/schema contracts remain unchanged.

## 4. Technology lock

- React + Vite + TypeScript
- Tailwind CSS
- FastAPI + Python 3.11
- Pydantic v2
- SQLAlchemy 2
- PostgreSQL/Supabase primary
- SQLite/local seeded fallback
- scikit-learn default ML path
- Haversine distance calculation
- Recharts optional display; list fallback

## 5. Explicitly not required

No microservices, Redis, Celery, Kafka, Docker/Kubernetes, auth, GraphQL, separate model-serving process, or external routing API in the critical P0 path.

## 6. Geographic architecture

The database stores state/district/mandi coordinates and commodity availability. State and district selectors query the catalog. Actual coordinates are authoritative for nearby search.

`find_nearby()`:
- filters active mandis carrying the selected commodity
- calculates Haversine distance
- includes all matches `<= radiusKm`
- does not filter by selected district/state
- returns dynamic list length
- never assumes exactly N mandis

If no eligible mandi exists inside the requested radius, the service returns a graceful fallback result with explicit `searchStatus`, not a hidden cross-radius recommendation.
