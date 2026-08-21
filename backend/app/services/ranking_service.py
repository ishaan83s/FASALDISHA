"""
Mandi Ranking & Scoring Engine.
SSOT Reference: 03_DECISION_ENGINE_SSOT.md, 05_API_CONTRACT.md, 13_JUDGE_PROOF_AND_P0_ACCEPTANCE.md
"""
from typing import List
from app.schemas.analysis import CandidateMandi, RankingBreakdown
from app.config.constants import RANKING_WEIGHTS


class RankingService:
    @staticmethod
    def rank_candidates(candidates: List[CandidateMandi]) -> List[CandidateMandi]:
        """
        Ranks candidate mandis transparently:
        rankingScore = 0.70 * normRiskAdjReturn + 0.20 * buyerSignalScore + 0.10 * dataQualityScore
        Sorts descending and assigns sequential ranks.
        """
        if not candidates:
            return []

        returns = [c.risk_adjusted_return for c in candidates]
        min_ret = min(returns)
        max_ret = max(returns)

        scored_candidates: List[CandidateMandi] = []
        for c in candidates:
            # 1. Normalize Risk-Adjusted Return (0-100)
            if max_ret > min_ret:
                norm_return = ((c.risk_adjusted_return - min_ret) / (max_ret - min_ret)) * 100.0
            else:
                norm_return = 50.0

            # 2. Buyer signal score (0-100)
            buyer_score = c.buyer_signal.buyer_signal_score

            # 3. Data quality score (0-100)
            dq_score = 80.0 if c.forecast.history_classification.value == "SEEDED" else 95.0

            # 4. Composite ranking score
            ranking_score = (
                RANKING_WEIGHTS["risk_adjusted_return"] * norm_return
                + RANKING_WEIGHTS["buyer_signal"] * buyer_score
                + RANKING_WEIGHTS["data_quality"] * dq_score
            )
            ranking_score = round(ranking_score, 2)

            # 5. Top explainability factors
            top_factors = []
            if norm_return >= 70.0:
                top_factors.append(f"High risk-adjusted net return (₹{c.risk_adjusted_return:,.0f})")
            elif norm_return <= 30.0:
                top_factors.append(f"Lower net return after transit (₹{c.risk_adjusted_return:,.0f})")
            
            if buyer_score >= 65.0:
                top_factors.append(f"Strong buyer liquidity ({c.buyer_signal.active_buyer_count} active synthetic buyers)")
            
            if c.distance_km <= 35.0:
                top_factors.append(f"Short transit corridor ({c.distance_km:.1f} km)")
            elif c.distance_km > 75.0:
                top_factors.append(f"Longer haul distance ({c.distance_km:.1f} km)")

            if c.risk_level.value in ["HIGH", "CRITICAL"]:
                top_factors.append(f"Elevated route/weather risk ({c.risk_level.value})")

            breakdown = RankingBreakdown(
                normalized_risk_adjusted_return=round(norm_return, 1),
                buyer_signal_score=round(buyer_score, 1),
                data_quality_score=round(dq_score, 1),
                top_factors=top_factors,
                ranking_score=ranking_score,
            )

            # Update candidate with calculated fields
            c.ranking_breakdown = breakdown
            c.ranking_score = ranking_score
            scored_candidates.append(c)

        # Sort descending by ranking_score
        scored_candidates.sort(key=lambda x: x.ranking_score, reverse=True)

        # Re-assign 1-based ranks
        for idx, sc in enumerate(scored_candidates):
            sc.rank = idx + 1

        return scored_candidates
