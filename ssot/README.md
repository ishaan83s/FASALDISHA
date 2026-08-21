# Crop Market Canonical SSOT v2.1

**Status:** SUPERSEDING v1.0 for all implementation started after this package is issued.

## Why v2.0 exists

v2.0 incorporates:
- Hackathon Problem Statement 9: **AI-Driven Crop Price Forecasting & Market Routing App**
- the AI/ML developer's updated geographic, forecasting, risk, quantity, and routing plan
- the previously verified v1.1 execution fixes

The architecture remains intentionally hackathon-simple: one FastAPI application, one frontend, one database abstraction, and in-process ML. The major change is the **domain contract**, not a move to a larger distributed architecture.

## Canonical precedence

1. `00_MASTER_PRODUCT_SSOT.md`
2. Frozen contracts: `03`, `04`, `05`, `06`
3. Architecture and engineering rules: `01`, `07`
4. ML and risk rules: `02`, `03`
5. Execution and cut rules: `08`–`11`
6. Migration notes: `12`

## Critical v2.0 change

The system is now designed around:

```text
State + District + Actual Farmer Coordinates + Commodity + Quantity
                    ↓
           Find all eligible mandis
           within configurable radius
                    ↓
     Forecast + Weather + Risk + Transport
                    ↓
      Expected Return / Risk-Adjusted Return
                    ↓
          Ranked Mandi Comparison
                    ↓
        Final Decision + Risk Override
```

The selected state/district establish context. They **must never restrict** the radius search. Geographic eligibility is determined by actual coordinates and distance.

## v2.1 readiness status

**READY FOR CODING, subject to the execution packets being regenerated from v2.1 rather than v1.1.**

v2.1 closes the remaining judge-demonstrability gaps: buyer-count/source visibility, ranking explanation, deterministic seeded weather-risk override, historical forecast provenance, and peak-alert proof.

## Round 2 rule

The canonical architecture supports Rajasthan, Gujarat, and Maharashtra across all districts represented by the loaded geography catalog. The 3-hour demo may use a representative local dataset if a complete official registry cannot be ingested in time, but the UI/API architecture must remain data-driven and must not hard-code selected districts or a fixed number of mandis.
