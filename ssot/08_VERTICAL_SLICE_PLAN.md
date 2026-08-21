# SSOT 08 — VERTICAL SLICE PLAN (v2.0)

The canonical architecture is broader than the 3-hour implementation window. Build the vertical P0 in this order.

## 0:00–0:20 — Contract + deployment gate

Backend:
- freeze v2 API models
- health endpoint
- geography endpoint stubs

Frontend:
- deployed shell
- API base URL
- dynamic form skeleton

AI/ML:
- freeze `ForecastOutput` including history provenance + peak alert fields
- prepare precomputed fallback

Integration:
- prove deployed frontend → backend call

Exit: live deployment works.

## 0:20–1:05 — Geography + analysis spine

Backend:
- states/districts/commodities catalog
- coordinate validation
- nearby eligible mandi search
- Haversine + dynamic candidate list

Frontend:
- geography selectors
- location modes
- quantity/radius/transport input

AI/ML:
- data prep + forecast fallback/live model

Integration:
- verify cross-boundary candidate behavior

Exit: one real request reaches a candidate list and exposes buyer counts from the synthetic dataset.

## 1:05–1:50 — Forecast + return + ranking

Backend:
- market data lookup + history provenance
- transport calculations
- expected revenue/net return
- ranking service

AI/ML:
- forecast outputs 1/3/7 + peak/confidence

Frontend:
- results shell + dynamic cards + forecast panel

Integration:
- connect mock contract to live endpoint

Exit: ranked list works end-to-end with buyer count/synthetic label, ranking breakdown, and peak alert metadata.

## 1:50–2:25 — Risk + decision

Backend:
- weather adapter
- risk service
- base decision + override

Frontend:
- risk panel and alert flag
- recommendation banner

AI/ML:
- confidence metadata and weather input adapter where available

Integration:
- seeded/unavailable weather modes

Exit: one normal and one deterministic risk-override scenario work; source classification is visible.

## 2:25–2:40 — Verification and cut

- remove demo mocks
- force fallback forecast
- test 1 and many candidate lists
- test cross-boundary case
- choose deterministic demo scenarios
- run judge-proof checklist

## 2:40–3:00 — Freeze/demo

No feature merges.
