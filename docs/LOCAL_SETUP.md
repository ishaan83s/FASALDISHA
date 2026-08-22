# Local Setup & Verification Guide

## Prerequisites
- Python 3.11+
- Node.js 18+ / npm

---

## 1. Backend Setup

```bash
cd backend

# 1. Create and activate Python virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Optional) Run database seed script explicitly
python -m scripts.seed_db

# 4. Run automated test suite
PYTHONPATH=. pytest tests -v

# 5. Start Backend FastAPI Server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Backend will be accessible at: `http://localhost:8000`
API Docs (Swagger): `http://localhost:8000/docs`
Health check: `http://localhost:8000/health`

---

## 2. Frontend Setup

```bash
cd frontend

# 1. Install dependencies
npm install

# 2. Copy environment file
cp .env.example .env

# 3. Start development server
npm run dev
```

Frontend will be accessible at: `http://localhost:5173`
