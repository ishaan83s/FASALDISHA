# 🌾 FasalDisha

**AI-driven crop price forecasting and market routing for Indian farmers.**

[Live App](https://fasaldisha.vercel.app) · [API Docs](http://localhost:8000/docs)

---

## Table of Contents

1. [Overview](#overview)
2. [Key Features](#key-features)
3. [Architecture](#architecture)
4. [Repository Structure](#repository-structure)
5. [Getting Started](#getting-started)
6. [Environment Variables](#environment-variables)
7. [Ranking & Decision Logic](#ranking--decision-logic)
8. [Tech Stack](#tech-stack)
9. [Testing](#testing)
10. [Roadmap](#roadmap)
11. [Contributing](#contributing)
12. [License](#license)

---

## Overview

Farmers routinely lose value at the point of sale because they lack visibility into where and when to sell their produce. Mandi (market) prices vary by location, transport costs eat into margins, weather introduces spoilage and delivery risk, and buyer demand shifts day to day — but none of this is presented in one place.

**FasalDisha** solves this by answering a single question directly:

> *Given my commodity, quantity, location, and current conditions — where should I sell, and should I sell now or wait?*

The platform ingests price history, weather data, and buyer demand signals, runs them through a forecasting and risk engine, and returns a clear **Sell / Wait / Travel** recommendation for each nearby market — along with a transparent breakdown of the reasoning behind it.

## Key Features

- **Price forecasting** — commodity-specific models predict near-term price movement to inform the sell/wait decision.
- **Market discovery** — coordinate-based radius search surfaces every viable mandi within range, across district and state boundaries.
- **Risk-aware recommendations** — weather and spoilage risk can override a "wait" recommendation when conditions turn unfavorable.
- **Transport-adjusted economics** — expected revenue is calculated net of quantity-aware transport cost, not just headline price.
- **Buyer demand signals** — active buyer count, demand level, and offer strength are factored into each market's ranking.
- **Explainable ranking** — every recommendation ships with a full breakdown of the criteria and weights that produced it, so results are never a black box.

## Architecture

```
React + Vite + TypeScript (Frontend)
              ↓ HTTP / JSON
           FastAPI (Backend)
              ↓
       Analysis Service (Composer)
  ┌───────────┼────────────────────────────────────────┐
  ↓           ↓          ↓        ↓        ↓           ↓
geo/mandi   market_data  forecast weather  risk    decision/ranking
  │           │          │        │        │           │
  └───────────┴──────────┴────────┴────────┴───────────┘
                         ↓
               SQLite (default) / PostgreSQL
```

**Design principles:**

- **Single-process orchestration** — the backend composes geolocation, market data, forecasting, weather, and risk services in-process, avoiding the operational overhead of a distributed system at this stage.
- **Coordinate-based geolocation** — Haversine radius search enables market discovery that isn't constrained by administrative boundaries.
- **Stable ML contract** — forecasting models communicate with the backend through a versioned `ForecastOutput` schema, so the ML pipeline and the API can evolve independently.
- **Weighted, transparent ranking** — final market ranking combines risk-adjusted return, buyer demand signals, and data quality into one normalized, auditable score.

## Repository Structure

```
FASALDISHA/
├── backend/       # FastAPI service: routing, schemas, orchestration, risk & decision engine
│   └── tests/     # API and integration tests
├── frontend/      # React + Vite + TypeScript client: input flow, results dashboard, charts
├── ml/            # Forecasting models, feature engineering, ForecastOutput contract
├── docs/          # Design docs and supporting documentation
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+ and npm
- (Optional) PostgreSQL — SQLite is used as the default fallback

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run tests
PYTHONPATH=. pytest tests -v

# Start the API server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

- **Health check:** `http://localhost:8000/health`
- **API docs (Swagger):** `http://localhost:8000/docs`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend expects the backend API at the URL configured in its environment file (defaults to `http://localhost:8000`).

### ML

```bash
cd ml
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

See `ml/` for training pipeline entry points and the `ForecastOutput` contract shared with the backend.

## Environment Variables

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

Copy this file to `backend/.env` and adjust values for your environment (e.g. swap `DATABASE_URL` for a PostgreSQL connection string in production).

## Ranking & Decision Logic

Each candidate market is scored on a normalized composite of:

| Factor | Weight |
|---|---|
| Risk-adjusted return | 70% |
| Buyer demand signal | 20% |
| Data quality | 10% |

Two distinct confidence metrics are surfaced alongside every result, and are never conflated:

- **`forecastConfidence`** — how well-supported the underlying price forecast is.
- **`decisionConfidence`** — the margin of evidence behind the final sell/wait/travel call.

Weather and spoilage risk can override a price-driven "wait" recommendation — for example, a severe-weather scenario will trigger a `SELL_EARLY_DUE_TO_RISK` verdict even when the price forecast alone would favor waiting.

## Tech Stack

- **Frontend:** React, Vite, TypeScript
- **Backend:** FastAPI (Python), Uvicorn
- **Database:** SQLite (default) / PostgreSQL (production-ready swap-in)
- **ML:** Python forecasting pipeline behind a versioned `ForecastOutput` contract
- **Testing:** Pytest
- **Deployment:** [fasaldisha.vercel.app](https://fasaldisha.vercel.app)

## Testing

```bash
cd backend
PYTHONPATH=. pytest tests -v
```

Test coverage includes API routing, cross-service integration (geo → forecast → risk → ranking), and scenario-based checks such as the severe-weather override path.

## Roadmap

- Expand commodity and mandi coverage
- Move from synthetic to live buyer/demand data sources
- Add historical backtesting view for past sell/wait decisions
- Production-grade PostgreSQL deployment with connection pooling

## Contributing

1. Fork the repository
2. Create a feature branch (`feature/your-feature-name`)
3. Make your changes within the relevant service directory (`backend/`, `frontend/`, or `ml/`)
4. Ensure `pytest tests -v` passes for any backend changes
5. Open a pull request with a clear description of the change

## License

License not yet specified. Contact the maintainer ([@ishaan83s](https://github.com/ishaan83s)) for usage terms.