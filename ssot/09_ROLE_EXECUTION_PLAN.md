# SSOT 09 — ROLE EXECUTION PLAN (v2.0)

## ARCHITECT + BACKEND

Owns:
- frozen contracts
- geography/mandi search
- analysis orchestration
- transport/ranking/decision
- risk service integration
- peak alert + ranking breakdown fields
- API verification

Does not own ML internals or frontend rendering.

## FRONTEND

Owns:
- dynamic geography selectors
- location acquisition/fallback
- quantity and transport inputs
- all dynamic results rendering
- risk/weather presentation
- buyer-count/synthetic-label and ranking-explanation presentation
- API integration

Does not hard-code fixed mandis or result count.

## AI / ML

Owns:
- commodity-level data preparation
- forecasting features/models
- forecast output contract
- model artifacts/precomputed fallback
- forecast confidence
- history provenance + peak metadata
- optional weather features/model comparison

Does not own final risk policy or business decision rules.

## INTEGRATION / QA / DELIVERY

Owns:
- branch/merge coordination
- deployed connectivity
- contract smoke fixtures
- cross-boundary test
- fallback tests
- demo scenario selection
- judge-proof gate verification

Does not invent business logic.

## Cross-role handoff

AI/ML freezes `ForecastOutput` early.
Backend freezes `AnalysisResult` early.
Frontend builds against exact typed mock only until live endpoint exists.
Integration rejects drift immediately.
