"""
Synthetic Buyer Intelligence Service.
SSOT Reference: 03_DECISION_ENGINE_SSOT.md, 13_JUDGE_PROOF_AND_P0_ACCEPTANCE.md
"""
from typing import Optional
from sqlalchemy.orm import Session
from app.db.models import BuyerModel
from app.schemas.analysis import BuyerSignal
from app.schemas.common import DataClassification, DemandLevel
from app.config.constants import BUYER_SIGNAL_WEIGHTS


class BuyerService:
    @staticmethod
    def get_buyer_signal(
        mandi_id: str,
        commodity_id: str,
        db: Optional[Session] = None,
    ) -> BuyerSignal:
        """
        Retrieves buyer signals for the candidate mandi from the synthetic dataset.
        Honesty Rule: Explicitly tagged as SYNTHETIC in classification and sourceLabel.
        """
        buyers = []
        if db:
            buyers = (
                db.query(BuyerModel)
                .filter(
                    BuyerModel.mandi_id == mandi_id,
                    BuyerModel.commodity_id == commodity_id.lower().strip(),
                    BuyerModel.active == True,
                )
                .all()
            )

        active_count = len(buyers)
        if active_count > 0:
            avg_offer = sum(b.offer_strength for b in buyers) / active_count
            avg_rel = sum(b.reliability_score for b in buyers) / active_count

            # Determine aggregate demand level
            demand_counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
            for b in buyers:
                demand_counts[b.demand_level] = demand_counts.get(b.demand_level, 0) + 1

            if demand_counts["HIGH"] >= demand_counts["MEDIUM"]:
                dominant_demand = DemandLevel.HIGH
            elif demand_counts["MEDIUM"] >= demand_counts["LOW"]:
                dominant_demand = DemandLevel.MEDIUM
            else:
                dominant_demand = DemandLevel.LOW
        else:
            # Deterministic heuristic fallback based on mandi/commodity hash
            h = hash(mandi_id + commodity_id)
            active_count = 2 + (h % 4)
            avg_offer = 60.0 + (h % 25)
            avg_rel = 70.0 + (h % 20)
            dominant_demand = DemandLevel.MEDIUM if (h % 2 == 0) else DemandLevel.HIGH

        # Map demand to numeric score (0-100)
        demand_num = 95.0 if dominant_demand == DemandLevel.HIGH else (65.0 if dominant_demand == DemandLevel.MEDIUM else 35.0)
        availability_score = min(active_count / 5.0, 1.0) * 100.0

        # Weighted calculation from constants
        w = BUYER_SIGNAL_WEIGHTS
        buyer_score = (
            w["demand"] * demand_num
            + w["availability"] * availability_score
            + w["offer_strength"] * avg_offer
            + w["reliability"] * avg_rel
        )

        return BuyerSignal(
            active_buyer_count=active_count,
            demand_level=dominant_demand,
            offer_strength=round(avg_offer, 1),
            reliability=round(avg_rel, 1),
            buyer_signal_score=round(buyer_score, 1),
            classification=DataClassification.SYNTHETIC,
            source_label="Synthetic demo dataset (Aggregated mandi buyer signals)",
        )
