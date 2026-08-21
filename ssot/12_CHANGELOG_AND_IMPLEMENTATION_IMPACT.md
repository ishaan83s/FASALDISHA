# SSOT 12 — CHANGELOG & IMPLEMENTATION IMPACT (v2.0)

## Overall impact

Estimated change from v1.0:

- **System topology / stack:** ~10% change
- **Backend module boundaries:** ~25% change
- **Data model:** ~45% change
- **API contract:** ~55% change
- **Frontend input/results flow:** ~50% change
- **ML interface:** ~25% change
- **Decision/ranking semantics:** ~45% change
- **Overall implementation approach:** approximately **35–40% changed; 60–65% reusable**

This is not a restart. Keep FastAPI, React/Vite, SQLAlchemy, Supabase/local fallback, Haversine, in-process ML, forecast fallback, buyer intelligence, and vertical slices.

## What stays

- one FastAPI application
- React/Vite frontend
- in-process modular ML
- forecast fallback
- Haversine
- configurable transport rate
- synthetic buyer signal
- explainable rule-based decision layer
- forecast vs decision confidence distinction
- 3-hour vertical execution
- data classification discipline

## What changes materially

### Geography
Old: approximate location + small seeded mandi set.
New: state/district catalog + actual coordinates + all eligible mandis within radius, cross-boundary.

### Inputs
Old: crop + coordinates + radius.
New: state + district + coordinates + commodity + quantity + optional transport settings + radius.

### Commodity model
Old: two groups.
New: category + three perishability classes, with legacy group derivation.

### Economics
Old: ₹/quintal comparative opportunity.
New: quantity-aware expected revenue, total transport cost, net return and risk-adjusted return.

### Forecast
Old: mainly local 7-day curve propagated to nearby mandis.
New: explicit per-mandi forecast contract with 1/3/7 horizons and peak metadata; propagation remains an honest fallback.

### Weather/risk
Old: weather mostly schema-present/inert in P0.
New: active modular weather/risk contract with `REAL`, `SEEDED`, or `UNAVAILABLE` behavior and explicit risk override.

### Recommendation
Old: SELL_NOW/HOLD/TRAVEL only.
New: base decision plus final recommendation capable of sell-early and avoid-route overrides.

### Frontend
Old: fixed two-screen minimal form.
New: dynamic geography + quantity + risk-aware ranked results, still two main screens if desired.

## Migration order

1. Freeze v2 Pydantic schemas.
2. Add geography/commodity availability tables.
3. Rename `crop` contract to canonical `commodity`.
4. Add quantity-aware return fields.
5. Add forecast horizon fields.
6. Add risk/weather objects.
7. Replace old fixed result card assumptions.
8. Add risk override fields.
9. Update mocks and smoke fixtures.
10. Rebuild role packets from v2, not v1.1.

## v2.1 judge-proof completion patch

v2.1 does not change the core architecture. It closes judge-demonstrability gaps by freezing:

- active buyer count and buyer-component visibility
- explicit synthetic buyer discovery explanation
- deterministic seeded risk-override demo fixture
- historical forecast provenance
- configurable peak alert semantics
- per-mandi ranking breakdown and top factors
- a judge-proof integration gate

These are implementation/contract clarifications rather than a topology rewrite.

## Packet status

`Crop_Market_Round2_Execution_Packet_v1.1` is now **superseded for new implementation work** because its API/database/frontend assumptions are v1-based. Reuse only its process discipline and general role structure.
