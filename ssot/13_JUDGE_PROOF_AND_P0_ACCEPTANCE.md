# SSOT 13 — JUDGE PROOF & P0 ACCEPTANCE GATE (v2.1)

This document is a release gate for the integrated Round 2 build. It does not add a new architecture. It defines what must be visibly demonstrable.

## A. Weather impact

**Backend:** `weather_service` returns status, impact, events, classification and source label. `risk_service` consumes the signal.

**Owner:** Architect/Backend; Frontend presents; Integration/QA verifies.

**Data classification:** REAL, SEEDED or UNAVAILABLE.

**Visible proof:** weather flag near recommendation + risk panel. At least one deterministic SEEDED severe-weather scenario must demonstrate a risk override.

**Pass condition:** a judge can see both the source classification and the recommendation effect.

## B. Group-wise crop segregation

**Backend/data:** commodity category + three-level perishability, with legacy PERISHABLE/NON_PERISHABLE group derivation.

**Owner:** AI/ML owns metadata/data preparation; Backend consumes it; Frontend explains it.

**Visible proof:** one perishable and one non-perishable scenario with different urgency/holding explanation.

**Pass condition:** grouping changes an explainable decision/risk input, not merely a database label.

## C. Buyer intelligence

**How buyers are found:** P0 performs lookup in a synthetic demo buyer dataset by candidate mandi + commodity + active status. No live buyer marketplace claim is allowed.

**Metrics:** active buyer count, demand level, offer strength, reliability, derived buyer signal score.

**Owner:** Backend/buyer service; Frontend presents; Integration verifies classification.

**Visible proof:** recommended mandi and alternatives show buyer count/signal, with `SYNTHETIC` label and a compact explanation of the contribution to ranking.

**Pass condition:** the team can answer all three judge questions: how found, how many, how used.

## D. Best location selection

**Method:** dynamic radius search over all eligible mandis, including cross-district/state candidates; return calculations use forecast, quantity and transport; risk-adjusted return and buyer signal contribute to ranking.

**Owner:** Architect/Backend.

**Visible proof:** at least two candidate mandis with distance, transport cost, forecast, net return, risk, buyer signal and ranking explanation.

**Pass condition:** the top mandi can be justified from returned fields without saying 'the AI chose it'.

## E. Historical forecast + peak price

**Method:** forecast output carries history window/provenance, 1/3/7-day forecast, peak price/day and peak alert.

**Owner:** AI/ML for output; Backend for propagation; Frontend for display.

**Visible proof:** current price, forecast horizons, peak day/price, model type and history provenance.

**Pass condition:** peak alert is advisory and source/model classification is honest.

## F. Final recommendation

The response must visibly distinguish:
- `baseDecision`
- `finalRecommendation`
- `riskOverrideApplied`
- reason codes / human-readable reason

**Pass condition:** if risk changes the result, the user can see what changed and why.

## Release gate checklist

Do not declare Round 2 ready until all are true:

- [ ] One normal scenario passes end-to-end.
- [ ] One perishable and one non-perishable scenario pass.
- [ ] One multi-mandi ranking passes.
- [ ] One cross-boundary candidate passes when loaded data supports it.
- [ ] One deterministic SEEDED risk override passes.
- [ ] Buyer count + SYNTHETIC label are visible.
- [ ] Ranking breakdown is visible/expandable.
- [ ] Historical forecast provenance + peak alert are visible.
- [ ] No hard-coded result count exists.
- [ ] API response matches frozen schema.
- [ ] Frontend receives no raw backend error shape.
- [ ] Demo wording does not overclaim geographic, buyer, forecast or weather data.
