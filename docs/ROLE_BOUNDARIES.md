# Role Boundaries & Handoff Agreement (Round 2)

## 1. ARCHITECT / BACKEND (Current Role)
- **Owns:**
  - FastAPI application structure & routes (`backend/app/api/`)
  - Shared Pydantic v2 schemas (`backend/app/schemas/`)
  - Database models, migrations, and seed scripts (`backend/app/db/`)
  - Location engine and Haversine distance search (`backend/app/services/mandi_service.py`)
  - Comparative economics & transport calculations (`backend/app/services/transport_service.py`)
  - Synthetic buyer signal aggregation (`backend/app/services/buyer_service.py`)
  - Risk engine & decision engine (`backend/app/services/risk_service.py`, `backend/app/services/decision_engine.py`)
  - Multi-criteria ranking service (`backend/app/services/ranking_service.py`)
  - Top-level composer (`backend/app/services/analysis_service.py`)
  - Backend automated test suite (`backend/tests/`)
- **Does NOT own:** React page layouts, ML model training algorithms.

---

## 2. FRONTEND ENGINEER
- **Owns:**
  - Dynamic Form (`AnalysisFormPage.tsx`, `GeographySelector.tsx`, `LocationPicker.tsx`, `CommoditySelector.tsx`)
  - Results Dashboard (`ResultsDashboardPage.tsx`, `RecommendationBanner.tsx`, `ForecastChart.tsx`, `MandiComparisonList.tsx`, `RiskPanel.tsx`, `WeatherAlert.tsx`, `ReasoningPanel.tsx`)
  - Typed API Client (`frontend/src/api/client.ts`)
- **Handoff Contract:**
  - Base URL: `http://localhost:8000`
  - Global Envelope: `{ success: boolean, data: T, error: ErrorDetail }`
  - Canonical Endpoint: `POST /analysis/run`
  - Never hard-code fixed mandi results; always render dynamic list from `data.nearbyMandis`.

---

## 3. AI / ML ENGINEER
- **Owns:**
  - Feature extraction (`ml/features.py`)
  - Training pipeline (`ml/train.py`)
  - Model weights store (`ml/model_store/`)
  - ML Forecast Output Contract (`ForecastOutput` in `ml/forecast_engine.py`)
- **Handoff Contract:**
  - Must return `ForecastOutput` with:
    - 1, 3, 7-day predicted prices
    - `expectedPeakPrice` and `peakDay`
    - `peakAlert` flag
    - `dailyForecast` array
    - `forecastConfidence` (0.30 - 0.95)
    - `modelType` (`LIVE` vs `PRECOMPUTED`)
    - `historyWindowDays` and `historyClassification` (`SEEDED` / `REAL`)
- Precomputed fallback in `ml/precomputed_forecasts.json` is active.

---

## 4. INTEGRATION / QA / DELIVERY
- **Owns:**
  - Git branch merges (`feature/architect-backend`, `feature/frontend`, `feature/ai-ml`)
  - End-to-end acceptance testing
  - Verifying judge-visible proofs (Weather override, perishability grouping, buyer signals, ranking breakdown, peak alert)
  - Smoke tests on live deployment.
