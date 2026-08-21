# SSOT 11 — CUT & FALLBACK RULES (v2.0)

## Never cut from the connected P0

- actual coordinate-based nearby search
- dynamic ranked results
- quantity-aware return calculations
- 7-day forecast or contract-compatible fallback
- transport calculation
- risk score/status
- deterministic seeded risk-override fixture
- buyer count/synthetic classification visibility
- ranking explanation fields
- final recommendation/reasoning
- honest data classification

## Ordered cuts if behind

1. Use precomputed forecasts for all commodities.
2. Use seeded representative geography catalog while preserving all-district-capable schema/API.
3. Use deterministic location fallback instead of map pin.
4. Use seeded weather event or `UNAVAILABLE` rather than live weather.
5. Reduce chart polish to textual forecast values.
6. Reduce commodity demo set, but keep at least one perishable and one non-perishable class.

Do not cut dynamic-list behavior or hard-code three mandis.

## Fallback matrix

| Problem | Fallback |
|---|---|
| Full 3-state registry unavailable | representative seeded catalog + accurate coverage disclosure |
| Live model fails | precomputed forecast |
| Weather source unavailable | `UNAVAILABLE` or clearly `SEEDED` event |
| No mandi within radius | graceful `searchStatus`, show no eligible route rather than hidden expansion |
| Geolocation blocked | deterministic fallback coordinates |
| Map incomplete | coordinate fallback; map omitted |
| Many results overwhelm UI | expandable dynamic list, not fixed truncation |
| Late broken merge | revert after T+2:40 |

## Coverage honesty

The architecture supports all districts in the three states. The demo claims actual complete coverage only when the loaded catalog contains it.
