# FasalDisha — AI-Driven Crop Price Forecasting & Market Routing App

> **Problem Statement 9:** AI-Driven Crop Price Forecasting & Market Routing App  
> **Canonical Source of Truth:** `Crop_Market_Canonical_SSOT_v2.1_Judge_Ready`  
> **Branch:** `feature/architect-backend`  
> **Status:** P0 Working Foundation Complete & Verified

---

## 1. Executive Summary

**FasalDisha** is a forecasting, market-routing, and risk-aware agricultural decision engine designed for Indian farmers. It answers the fundamental economic dilemma:

> *"Given my commodity, quantity, location, forecast, transport cost, and current risks, where should I sell, and should I sell now or wait?"*

---

## 2. System Architecture & Topology

```text
React + Vite + TypeScript (Frontend)
              ↓ HTTP / JSON Envelope
           FastAPI (Backend)
              ↓
       analysis_service (Composer)
  ┌───────────┼────────────────────────────────────────┐
  ↓           ↓          ↓        ↓        ↓           ↓
geo/mandi   market_data  forecast weather  risk    decision/ranking
  │           │          │        │        │           │
  └───────────┴──────────┴────────┴────────┴───────────┘
                         ↓
               SQLite (Default Fallback) / PostgreSQL
```

- **Single Process In-Memory Orchestration**: Zero microservices complexity for hackathon resilience.
- **Authoritative Geolocation**: Coordinate-based Haversine radius search enables seamless cross-district and cross-state discovery.
- **Contract-Frozen ML Boundary**: Clean decoupling between ML forecasting algorithms and backend orchestration via `ForecastOutput`.
- **Transparent Multi-Criteria Ranking**: Normalized risk-adjusted return (70%), synthetic buyer signals (20%), data quality (10%).

---

## 3. Parallel Team Work Boundaries

| Role | Primary Directory | Key Responsibilities |
|---|---|---|
| **ARCHITECT / BACKEND** | `backend/` | API routing, schemas, database, orchestration, transport, risk, ranking & decision engine. |
| **FRONTEND** | `frontend/` | Dynamic form flow, results dashboard, charts, comparison cards, API client. |
| **AI / ML** | `ml/` | Commodity features, training pipeline, model store, `ForecastOutput` contract. |
| **INTEGRATION / QA** | `backend/tests/` | Smoke tests, cross-boundary verification, judge proof demonstration gates. |

---

## 4. Quickstart

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. pytest tests -v
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

- **Health Check:** `http://localhost:8000/health`
- **Swagger Docs:** `http://localhost:8000/docs`

---

## 5. Judge-Proof Acceptance Status (P0 Verified)

| Requirement | Implementation Proof | Status |
|---|---|---|
| **1. Weather Impact** | `weather_service` + `risk_service` supporting `REAL`, `SEEDED`, or `UNAVAILABLE`. Deterministic severe weather scenario in Pune triggers `SELL_EARLY_DUE_TO_RISK` override. | ✅ VERIFIED |
| **2. Crop Segregation** | 3-level perishability (`HIGHLY_PERISHABLE`, `MODERATELY_PERISHABLE`, `NON_PERISHABLE`) with legacy group mapping. Tomato vs Wheat tested. | ✅ VERIFIED |
| **3. Buyer Intelligence** | Synthetic buyer dataset queries active buyer count, demand level, offer strength, reliability. Visibly labeled as `SYNTHETIC`. | ✅ VERIFIED |
| **4. Best Location** | Distance, transport cost, forecast, and buyer signal dynamically rank mandis with complete ranking breakdown. | ✅ VERIFIED |
| **5. Transport Economics** | Quantity-aware expected revenue, transport cost per quintal, total logistics cost, and net return calculations. | ✅ VERIFIED |
| **6. Dynamic Mandis** | Coordinate-based radius search returns 1 to N candidates dynamically across district boundaries. | ✅ VERIFIED |
| **7. Confidence Transparency** | `forecastConfidence` (ML support metric) and `decisionConfidence` (evidence margin) remain strictly separated. | ✅ VERIFIED |

---

## 6. Environment Variables

### Backend (`backend/.env.example`)
```env
APP_NAME=FasalDisha-Backend
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000
DATABASE_URL=sqlite:///./fasal_disha.db
SEEDED_RISK_OVERRIDE_SCENARIO_ENABLED=true
PEAK_ALERT_THRESHOLD=0.05
RADIUS_KM_DEFAULT=100
RADIUS_KM_MAX=300
TRANSPORT_RATE_PER_QUINTAL_PER_KM=2.5
```
