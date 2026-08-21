# SSOT 10 — ROUND 2 DEMO PLAN (v2.0)

## Demo narrative

1. Select a state and district for context.
2. Use actual/fallback farmer coordinates.
3. Select a commodity and quantity.
4. Explain that the 100 km search is coordinate-based and can cross administrative boundaries.
5. Run analysis.
6. Show multiple ranked mandis dynamically.
7. Compare distance, forecast, transport, estimated return, risk-adjusted return, active buyer count and risk.
8. Show the best mandi and alternative options.
9. Show the historical basis/provenance, forecast peak and whether the peak alert is active.
10. Show weather/risk flag and explain source classification.
11. Demonstrate the deterministic seeded risk override scenario and clearly label it SEEDED unless a REAL alert is actually active.
12. State that buyer data is synthetic and forecast/weather modes are labeled honestly.

## Judge Q&A anchors

**How do you choose the best mandi?**
Distance and transport affect net return; forecasted opportunity, buyer signal and risk-adjusted return feed a transparent ranking.

**Why not restrict to the selected district?**
District is input context; a farmer near a border can have a better mandi across the boundary. Coordinates and radius are the routing truth.

**How does weather change the recommendation?**
Weather/alerts feed a separate risk layer after forecasting. High risk can override HOLD or a risky travel recommendation. If weather data is unavailable, the system says so.

**Is the risk score ML?**
No. It is an explainable rule-based support layer separate from the forecast model.

**How are buyers found and how do they influence the result?**
For P0 they are not live-discovered. The backend looks up synthetic active buyer records for the candidate mandi and commodity, aggregates active-buyer count, demand, offer strength and reliability, and converts those into a transparent buyer signal used as one ranking input.

**Are buyers real?**
No. Current buyer records are synthetic and explicitly labeled.

## Scenario requirements

Prepare:
- one highly/moderately perishable scenario
- one non-perishable scenario
- one multi-mandi ranking
- one cross-boundary candidate if dataset supports it
- one weather unavailable or seeded event
- one deterministic seeded risk override (required demo fixture)
- one screen showing active buyer count + synthetic classification
- one screen showing ranking breakdown/top factors
- one screen showing historical forecast provenance + peak alert
