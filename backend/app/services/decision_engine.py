"""
Decision Engine: Evaluates Base Market Decisions and Risk Overrides.
SSOT Reference: 03_DECISION_ENGINE_SSOT.md, 05_API_CONTRACT.md, 13_JUDGE_PROOF_AND_P0_ACCEPTANCE.md
"""
from typing import List, Optional
from app.schemas.geography import Commodity, Mandi
from app.schemas.analysis import (
    FarmerContext,
    CandidateMandi,
    DecisionOutput,
)
from app.schemas.forecast import ForecastOutput
from app.schemas.weather import WeatherSignal
from app.schemas.common import (
    BaseDecision,
    FinalRecommendation,
    RiskLevel,
    PerishabilityClass,
)
from app.config.constants import (
    TRAVEL_SIGNIFICANCE_THRESHOLD,
    HOLD_SIGNIFICANCE_THRESHOLD,
)


class DecisionEngine:
    @staticmethod
    def evaluate_decision(
        commodity: Commodity,
        farmer_context: FarmerContext,
        local_mandi: Optional[Mandi],
        ranked_mandis: List[CandidateMandi],
        general_forecast: ForecastOutput,
        general_weather: WeatherSignal,
    ) -> DecisionOutput:
        """
        Computes base decision (SELL_NOW | HOLD | TRAVEL) and applies risk overrides.
        Generates structured reason codes and transparent human-readable explanations.
        """
        if not ranked_mandis:
            return DecisionOutput(
                base_decision=BaseDecision.SELL_NOW,
                final_recommendation=FinalRecommendation.SELL_NOW,
                risk_override_applied=False,
                recommended_mandi=local_mandi,
                reason_codes=["NO_ELIGIBLE_MANDI_IN_RADIUS"],
                human_readable_reason="No eligible active mandis found within the search radius.",
                decision_confidence=0.50,
            )

        top = ranked_mandis[0]
        recommended_mandi = top.mandi

        # Locate local candidate in ranked list if available
        local_cand = None
        if local_mandi:
            for c in ranked_mandis:
                if c.mandi.mandi_id == local_mandi.mandi_id:
                    local_cand = c
                    break

        # -------------------------------------------------------------
        # 1. Base Decision Computation
        # -------------------------------------------------------------
        base_decision = BaseDecision.SELL_NOW
        base_reasons: List[str] = []

        # Check Travel Advantage
        if local_cand and top.mandi.mandi_id != local_cand.mandi.mandi_id:
            gain_ratio = (
                top.risk_adjusted_return - local_cand.risk_adjusted_return
            ) / max(local_cand.risk_adjusted_return, 1.0)

            if gain_ratio >= TRAVEL_SIGNIFICANCE_THRESHOLD:
                base_decision = BaseDecision.TRAVEL
                base_reasons.append("TRAVEL_GAIN_ABOVE_THRESHOLD")

        # Check Hold Opportunity if Travel is not indicated
        if base_decision != BaseDecision.TRAVEL:
            hold_gain_ratio = (
                general_forecast.forecast_7_day - general_forecast.current_price
            ) / max(general_forecast.current_price, 1.0)

            if commodity.perishability_class == PerishabilityClass.HIGHLY_PERISHABLE:
                # Perishable logic: holding is highly restricted unless short peak is detected
                if general_forecast.peak_day <= 2 and hold_gain_ratio >= HOLD_SIGNIFICANCE_THRESHOLD:
                    base_decision = BaseDecision.HOLD
                    base_reasons.append("HOLD_GAIN_ABOVE_THRESHOLD")
                else:
                    base_decision = BaseDecision.SELL_NOW
                    base_reasons.append("PERISHABILITY_URGENCY_HIGH")
            else:
                if hold_gain_ratio >= HOLD_SIGNIFICANCE_THRESHOLD:
                    base_decision = BaseDecision.HOLD
                    base_reasons.append("HOLD_GAIN_ABOVE_THRESHOLD")
                else:
                    base_decision = BaseDecision.SELL_NOW
                    base_reasons.append("SELL_NOW_DEFAULT")

        # -------------------------------------------------------------
        # 2. Risk Override Layer
        # -------------------------------------------------------------
        final_recommendation = FinalRecommendation.SELL_NOW
        risk_override_applied = False
        final_reasons = list(base_reasons)
        human_readable = ""
        decision_confidence = round(
            0.50 + 0.30 * general_forecast.forecast_confidence + 0.10 * (1.0 if top.risk_level == RiskLevel.LOW else 0.0),
            2,
        )

        has_severe_weather = (
            general_weather.impact_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]
            or top.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]
            or any(e.severity in [RiskLevel.HIGH, RiskLevel.CRITICAL] for e in general_weather.events)
        )

        if base_decision == BaseDecision.HOLD:
            if has_severe_weather:
                final_recommendation = FinalRecommendation.SELL_EARLY_DUE_TO_RISK
                risk_override_applied = True
                final_reasons.append("RISK_OVERRIDE_SELL_EARLY")
                final_reasons.append("WEATHER_RISK_HIGH")
                human_readable = (
                    f"Holding {commodity.commodity_name} is overridden due to active severe weather/waterlogging alerts. "
                    f"Recommended to SELL EARLY at {top.mandi.mandi_name} to prevent crop spoilage."
                )
            else:
                final_recommendation = FinalRecommendation.HOLD
                risk_override_applied = False
                human_readable = (
                    f"Forecast indicates prices rising to expected peak of ₹{general_forecast.expected_peak_price:,.0f} "
                    f"around Day {general_forecast.peak_day}. Low operational risk supports holding {commodity.commodity_name}."
                )

        elif base_decision == BaseDecision.TRAVEL:
            if top.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
                # Look for safer candidate
                safer_alt = next((c for c in ranked_mandis[1:] if c.risk_level not in [RiskLevel.HIGH, RiskLevel.CRITICAL]), None)
                if safer_alt:
                    recommended_mandi = safer_alt.mandi
                    final_recommendation = FinalRecommendation.SELL_AT_RECOMMENDED_MANDI
                    risk_override_applied = True
                    final_reasons.append("RISK_OVERRIDE_AVOID_ROUTE")
                    human_readable = (
                        f"Transit to primary market ({top.mandi.mandi_name}) carries high route/weather risk. "
                        f"Rerouting to safer alternative {safer_alt.mandi.mandi_name} (Risk: {safer_alt.risk_level.value})."
                    )
                else:
                    final_recommendation = FinalRecommendation.AVOID_MANDI_OR_ROUTE
                    risk_override_applied = True
                    final_reasons.append("RISK_OVERRIDE_AVOID_ROUTE")
                    final_reasons.append("TRANSPORT_RISK_HIGH")
                    human_readable = f"Severe transit disruptions active on routes to distant mandis. Avoid distant travel."
            else:
                final_recommendation = FinalRecommendation.SELL_AT_RECOMMENDED_MANDI
                risk_override_applied = False
                human_readable = (
                    f"Recommended to sell at {top.mandi.mandi_name}. Estimated net return of ₹{top.net_return:,.0f} "
                    f"(risk-adjusted: ₹{top.risk_adjusted_return:,.0f}) outweighs ₹{top.total_transport_cost:,.0f} transit cost "
                    f"over {top.distance_km:.1f} km."
                )

        else:  # BaseDecision.SELL_NOW
            final_recommendation = FinalRecommendation.SELL_NOW
            risk_override_applied = False
            human_readable = (
                f"Sell immediately at {top.mandi.mandi_name} to capture current modal price of ₹{top.current_price:,.0f}/quintal. "
                f"Holding offers negligible gain or elevated storage risk."
            )

        return DecisionOutput(
            base_decision=base_decision,
            final_recommendation=final_recommendation,
            risk_override_applied=risk_override_applied,
            recommended_mandi=recommended_mandi,
            reason_codes=final_reasons,
            human_readable_reason=human_readable,
            decision_confidence=decision_confidence,
        )
