# SSOT 04 — DATABASE CONTRACT (v2.0)

Primary: PostgreSQL/Supabase. Fallback: SQLite/local seeded store.

## 1. `states`

- `state_id` TEXT PK
- `state_name` TEXT UNIQUE
- `active` BOOLEAN
- `source_classification` TEXT

Canonical initial values: Rajasthan, Gujarat, Maharashtra.

## 2. `districts`

- `district_id` TEXT PK
- `state_id` FK
- `district_name` TEXT
- `active` BOOLEAN
- `source_classification` TEXT

Unique `(state_id, district_name)`.

## 3. `commodities`

- `commodity_id` TEXT PK
- `commodity_name` TEXT
- `commodity_category` TEXT
- `perishability_class` TEXT
- `legacy_crop_group` TEXT
- `unit` TEXT DEFAULT `quintal`
- `active` BOOLEAN

## 4. `mandis`

- `mandi_id` TEXT PK
- `mandi_name` TEXT
- `state_id` FK
- `district_id` FK
- `latitude` DOUBLE PRECISION
- `longitude` DOUBLE PRECISION
- `active` BOOLEAN
- `location_classification` TEXT

Index `(state_id, district_id, active)` and coordinate-friendly index where supported.

## 5. `mandi_commodities`

- `mandi_id` FK
- `commodity_id` FK
- `active` BOOLEAN
- `source_classification` TEXT

PK `(mandi_id, commodity_id)`.

This is the authoritative commodity-availability relation.

## 6. `mandi_prices`

- `price_id`
- `mandi_id`
- `commodity_id`
- `price_date`
- `min_price`
- `modal_price`
- `max_price`
- `source_classification`

Index `(commodity_id, mandi_id, price_date)`.

## 7. `buyers`

Synthetic only in current prototype:
- `buyer_id`
- `buyer_type`
- `commodity_id`
- `mandi_id`
- `active`
- `demand_level`
- `offer_strength`
- `reliability_score`
- `data_classification`

## 8. `weather_events`

- `event_id`
- `state_id` nullable
- `district_id` nullable
- `latitude` nullable
- `longitude` nullable
- `event_type`
- `severity`
- `event_date`
- `classification`
- `source_label`
- `active`

## 9. `official_alerts`

Schema-ready for future live alerts:
- `alert_id`
- `source_name`
- `region`
- `alert_type`
- `severity`
- `starts_at`
- `ends_at`
- `classification`
- `source_label`
- `active`

P0 may contain zero rows or clearly seeded rows.

## 10. `forecast_cache`

- `cache_id`
- `commodity_id`
- `mandi_id` nullable
- `generated_at`
- `forecast_payload` JSON
- `forecast_confidence`
- `model_type`
- `forecast_scope`

## 11. Coverage metadata

`data_coverage_metadata` may report:
- supported states
- district count loaded
- mandi count loaded
- last updated
- source classification

The UI/demo may display coverage metadata only if accurate.

## 12. Schema rule

No users/auth tables are part of v2.0 P0.
