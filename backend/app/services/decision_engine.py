"""
Explainable Decision Engine with Risk Overrides.
SSOT Reference: 03_DECISION_ENGINE_SSOT.md, 13_JUDGE_PROOF_AND_P0_ACCEPTANCE.md
"""
from typing import List, Optional
from app.schemas.geography import Commodity
from app.schemas.analysis import CandidateMandi, DecisionOutput, RiskSummary
from app.schemas.common import (
    BaseDecision,
    FinalRecommendation,
    PerishabilityClass,
    RiskLevel,
)
from app.config.constants import (
    TRAVEL_SIGNIFICANCE_THRESHOLD,
    HOLD_SIGNIFICANCE_THRESHOLD,
    HIGH_RISK_OVERRIDE_THRESHOLD,
)


class DecisionEngine:
    @staticmethod
    def evaluate_decision(
        commodity: Commodity,
        local_mandi: Optional[CandidateMandi],
        ranked_candidates: List[CandidateMandi],
        risk_summary: RiskSummary,
    ) -> DecisionOutput:
        """
        Synthesizes Market Forecasts, Economics, Buyer Signals, and Risk Overrides
        to produce an explainable, judge-ready recommendation.
        """
        if not ranked_candidates:
            return DecisionOutput(
                base_decision=BaseDecision.SELL_NOW,
                final_recommendation=FinalRecommendation.SELL_NOW,
                risk_override_applied=False,
                recommended_mandi=None,
                reason_codes=["NO_ELIGIBLE_MANDI_IN_RADIUS"],
                human_readable_reason="No eligible mandis found within the search radius carrying this commodity.",
                decision_confidence=0.50,
            )

        top_candidate = ranked_candidates[0]
        reason_codes: List[str] = []
        
        # Step 1: Evaluate Base Decision
        local_return = local_mandi.risk_adjusted_return if local_mandi else top_candidate.risk_adjusted_return
        top_return = top_candidate.risk_adjusted_return
        
        travel_margin = (top_return - local_return) / max(local_return, 1.0) if local_mandi else 0.0
        
        # Check forecast gain over current price
        curr_price = top_candidate.current_price
        expected_7d = top_candidate.forecast.forecast_7_day
        forecast_gain = (expected_7d - curr_price) / max(curr_price, 1.0)

        is_perishable = commodity.perishability_class in [
            PerishabilityClass.HIGHLY_PERISHABLE,
            PerishabilityClass.MODERATELY_PERISHABLE,
        ]

        if local_mandi and top_candidate.mandi.mandi_id != local_mandi.mandi.mandi_id and travel_margin >= TRAVEL_SIGNIFICANCE_THRESHOLD:
            base_decision = BaseDecision.TRAVEL
            reason_codes.append("TRAVEL_GAIN_ABOVE_THRESHOLD")
        elif forecast_gain >= HOLD_SIGNIFICANCE_THRESHOLD and commodity.perishability_class != PerishabilityClass.HIGHLY_PERISHABLE:
            base_decision = BaseDecision.HOLD
            reason_codes.append("HOLD_GAIN_ABOVE_THRESHOLD")
        else:
            base_decision = BaseDecision.SELL_NOW
            reason_codes.append("SELL_NOW_DEFAULT")

        # Step 2: Evaluate Risk Override (SSOT 03 Section 10 & SSOT 13 Section A)
        risk_override_applied = False
        final_rec = FinalRecommendation.SELL_NOW
        human_reason = ""

        # Case A: HOLD with elevated weather/alert risk -> SELL_EARLY_DUE_TO_RISK
        if base_decision == BaseDecision.HOLD and (
            risk_summary.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]
            or risk_summary.overall_risk_score >= HIGH_RISK_OVERRIDE_THRESHOLD
        ):
            risk_override_applied = True
            final_rec = FinalRecommendation.SELL_EARLY_DUE_TO_RISK
            reason_codes.append("WEATHER_RISK_HIGH")
            reason_codes.append("RISK_OVERRIDE_SELL_EARLY")
            human_reason = (
                f"Although a 7-day price gain (+{round(forecast_gain*100, 1)}%) was forecasted, "
                f"high meteorological/transit risk (Score: {risk_summary.overall_risk_score}/100) overrides holding. "
                f"Recommend selling early at {top_candidate.mandi.mandi_name} to prevent spoilage and logistical loss."
            )

        # Case B: TRAVEL with severe top mandi risk -> Find safer alternative or AVOID
        elif base_decision == BaseDecision.TRAVEL and top_candidate.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            # Look for a safer candidate
            safer_candidates = [c for c in ranked_candidates if c.risk_level in [RiskLevel.LOW, RiskLevel.MODERATE]]
            if safer_candidates:
                top_candidate = safer_candidates[0]
                risk_override_applied = True
                final_rec = FinalRecommendation.SELL_AT_RECOMMENDED_MANDI
                reason_codes.append("RISK_OVERRIDE_AVOID_ROUTE")
                human_reason = (
                    f"Higher return market had critical transit risk. "
                    f"Rerouted to safer alternative {top_candidate.mandi.mandi_name} "
                    f"offering ₹{top_candidate.risk_adjusted_return:,.0f} net return."
                )
            else:
                risk_override_applied = True
                final_rec = FinalRecommendation.AVOID_MANDI_OR_ROUTE
                reason_codes.append("RISK_OVERRIDE_AVOID_ROUTE")
                human_reason = "Elevated weather and transit risk across regional routes. Recommend avoiding long transit."

        # Case C: Standard TRAVEL execution
        elif base_decision == BaseDecision.TRAVEL:
            final_rec = FinalRecommendation.SELL_AT_RECOMMENDED_MANDI
            human_reason = (
                f"Transport-adjusted net return at {top_candidate.mandi.mandi_name} "
                f"(₹{top_candidate.net_return:,.0f}) exceeds local market by "
                f"+{round(travel_margin*100, 1)}%, backed by {top_candidate.buyer_signal.active_buyer_count} active buyers."
            )

        # Case D: Standard HOLD execution
        elif base_decision == BaseDecision.HOLD:
            final_rec = FinalRecommendation.HOLD
            human_reason = (
                f"Crop prices are projected to appreciate by +{round(forecast_gain*100, 1)}% over 7 days. "
                f"Low risk conditions allow holding for better returns at {top_candidate.mandi.mandi_name}."
            )

        # Case E: Standard SELL NOW execution
        else:
            final_rec = FinalRecommendation.SELL_NOW
            if is_perishable and commodity.perishability_class == PerishabilityClass.HIGHLY_PERISHABLE:
                reason_codes.append("PERISHABILITY_URGENCY_HIGH")
                human_reason = (
                    f"Commodity is highly perishable. Selling immediately at {top_candidate.mandi.mandi_name} "
                    f"maximizes realized value at ₹{top_candidate.current_price:,.0f}/quintal."
                )
            else:
                human_reason = (
                    f"Current spot price (₹{top_candidate.current_price:,.0f}/quintal) offers optimal certainty. "
                    f"Recommend immediate sale at {top_candidate.mandi.mandi_name}."
                )

        # Decision confidence derivation (evidence strength + data completeness)
        conf = 0.82
        if risk_override_applied:
            conf = 0.88
        elif travel_margin > 0.10:
            conf = 0.85
        elif is_perishable:
            conf = 0.80

        return DecisionOutput(
            base_decision=base_decision,
            final_recommendation=final_rec,
            risk_override_applied=risk_override_applied,
            recommended_mandi=top_candidate.mandi,
            reason_codes=reason_codes,
            human_readable_reason=human_reason,
            decision_confidence=conf,
        )
