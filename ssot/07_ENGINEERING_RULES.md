# SSOT 07 — ENGINEERING RULES (v2.0)

## 1. Contract freeze

Docs 03–06 are frozen shared contracts. Any change requires Architect/Backend approval and immediate rebroadcast.

## 2. Modular, not distributed

Separate services/modules are required for:
- geography
- mandi search/data
- forecast
- weather
- risk
- transport
- ranking
- decision

They remain in one FastAPI deployment for P0.

## 3. Geographic rule

Never filter the nearby-mandi search by selected state/district after coordinates are available. Search by distance and commodity eligibility.

## 4. Quantity rule

Quantity is carried through return calculations. Unit is quintal in v2 P0.

## 5. Dynamic-list rule

No fixed array length in backend, schema, frontend, tests, or mock fixtures.

## 6. Data provenance rule

Response fields that surface non-real data must preserve classification metadata.

## 7. Error behavior

Expected validation/domain errors use the global envelope. No raw stack traces to frontend.

## 8. Git

Feature branches:
- `backend/`
- `frontend/`
- `ml/`
- `integration/`

Small merges after contract checks.

## 9. Round 2 freeze

Hard feature freeze at T+2:40. Revert broken late work instead of debugging on stage.

## 10. Judge-proof integration rule

Before freeze, Integration/QA must verify that every judge-feedback item has a visible UI proof, a backend value, an owner, and an honest data classification. A schema-only implementation does not pass this gate.

## 11. Required smoke tests

- state/district/commodity selectors
- geolocation/fallback path
- one highly/moderately perishable commodity
- one non-perishable commodity
- cross-district/state candidate within radius
- dynamic 1-candidate and multi-candidate rendering
- custom transport rate
- fallback forecast
- weather unavailable
- seeded weather risk override (deterministic, visible in demo)
- buyer active-count and synthetic-label visibility
- ranking breakdown consistency with score ordering
- peak alert threshold behavior
- historical forecast provenance visibility
