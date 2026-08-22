"""
Mandi Economics, Risk Penalty, and Multi-Criteria Ranking Service.
SSOT Reference: 03_DECISION_ENGINE_SSOT.md, 13_JUDGE_PROOF_AND_P0_ACCEPTANCE.md
"""
from typing import List, Dict, Any
from app.schemas.analysis import (
    CandidateMandi,
    RankingBreakdown,
    BuyerSignal,
)
from app.schemas.geography import Mandi
from app.schemas.forecast import ForecastOutput
from app.schemas.weather import WeatherSignal
from app.schemas.common import RiskLevel
from app.config.constants import (
    RANKING_WEIGHTS,
    RISK_PENALTY_FACTOR,
)


class RankingService:
    @staticmethod
    def process_and_rank_candidates(
        raw_candidates: List[Dict[str, Any]],
        quantity_quintals: float,
    ) -> List[CandidateMandi]:
        """
        Calculates quantity-aware economics, risk-adjusted returns, and normalizes ranking inputs.
        Returns a dynamic list of CandidateMandi ranked descending by rankingScore.
        """
        if not raw_candidates:
            return []

        # Step 1: Calculate comparative economics for each candidate
        processed = []
        for item in raw_candidates:
            mandi: Mandi = item["mandi"]
            dist_km: float = item["distance_km"]
            curr_price: float = item["current_price"]
            forecast: ForecastOutput = item["forecast"]
            transport_per_q: float = item["transport_cost_per_quintal"]
            total_transport: float = item["total_transport_cost"]
            buyer_sig: BuyerSignal = item["buyer_signal"]
            weather_sig: WeatherSignal = item["weather_impact"]
            risk_score: float = item["risk_score"]
            risk_level: RiskLevel = item["risk_level"]

            forecasted_price = forecast.forecast_7_day
            expected_revenue = round(forecasted_price * quantity_quintals, 2)
            net_return = round(expected_revenue - total_transport, 2)

            # Risk penalty formula: netReturn * (riskScore / 100) * RISK_PENALTY_FACTOR
            risk_penalty = net_return * (risk_score / 100.0) * RISK_PENALTY_FACTOR
            risk_adjusted_return = round(net_return - risk_penalty, 2)

            processed.append({
                "mandi": mandi,
                "distance_km": dist_km,
                "current_price": curr_price,
                "forecast": forecast,
                "transport_cost_per_quintal": transport_per_q,
                "total_transport_cost": total_transport,
                "expected_revenue": expected_revenue,
                "net_return": net_return,
                "risk_score": risk_score,
                "risk_level": risk_level,
                "risk_adjusted_return": risk_adjusted_return,
                "buyer_signal": buyer_sig,
                "weather_impact": weather_sig,
                "data_quality_score": 90.0,
            })

        # Step 2: Normalize risk-adjusted returns across the candidate set
        returns = [p["risk_adjusted_return"] for p in processed]
        min_ret = min(returns)
        max_ret = max(returns)

        for p in processed:
            if max_ret > min_ret:
                norm_ret = ((p["risk_adjusted_return"] - min_ret) / (max_ret - min_ret)) * 100.0
            else:
                norm_ret = 50.0  # Default midpoint if equal

            norm_ret = round(norm_ret, 1)
            b_score = p["buyer_signal"].buyer_signal_score
            dq_score = p["data_quality_score"]

            w = RANKING_WEIGHTS
            ranking_score = round(
                w["risk_adjusted_return"] * norm_ret
                + w["buyer_signal"] * b_score
                + w["data_quality"] * dq_score,
                1,
            )

            # Generate top explainability factors for judge proof
            top_factors = []
            if norm_ret >= 75.0:
                top_factors.append("High risk-adjusted net return")
            if b_score >= 70.0:
                top_factors.append(f"Strong buyer demand ({p['buyer_signal'].active_buyer_count} active traders)")
            if p["distance_km"] <= 30.0:
                top_factors.append("Proximity minimizes logistics cost")
            if p["risk_score"] <= 30.0:
                top_factors.append("Favorable weather & low route risk")
            if not top_factors:
                top_factors.append("Balanced price and transport feasibility")

            p["norm_return"] = norm_ret
            p["ranking_score"] = ranking_score
            p["top_factors"] = top_factors

        # Step 3: Sort descending by ranking_score
        processed.sort(key=lambda x: x["ranking_score"], reverse=True)

        # Step 4: Assemble CandidateMandi schemas with ranks
        results: List[CandidateMandi] = []
        for idx, p in enumerate(processed, start=1):
            results.append(
                CandidateMandi(
                    rank=idx,
                    mandi=p["mandi"],
                    distance_km=p["distance_km"],
                    commodity_available=True,
                    current_price=p["current_price"],
                    forecast=p["forecast"],
                    transport_cost_per_quintal=p["transport_cost_per_quintal"],
                    total_transport_cost=p["total_transport_cost"],
                    expected_revenue=p["expected_revenue"],
                    net_return=p["net_return"],
                    risk_score=p["risk_score"],
                    risk_level=p["risk_level"],
                    risk_adjusted_return=p["risk_adjusted_return"],
                    buyer_signal=p["buyer_signal"],
                    weather_impact=p["weather_impact"],
                    ranking_breakdown=RankingBreakdown(
                        normalized_risk_adjusted_return=p["norm_return"],
                        buyer_signal_score=p["buyer_signal"].buyer_signal_score,
                        data_quality_score=p["data_quality_score"],
                        top_factors=p["top_factors"],
                        ranking_score=p["ranking_score"],
                    ),
                    ranking_score=p["ranking_score"],
                    data_classification={
                        "price": "SEEDED",
                        "forecast": p["forecast"].model_type.value,
                        "buyers": "SYNTHETIC",
                        "weather": p["weather_impact"].classification.value,
                    },
                )
            )

        return results
