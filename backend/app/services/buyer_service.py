"""
Synthetic Buyer Intelligence Service.
SSOT Reference: 02_DATA_AND_ML_SSOT.md, 03_DECISION_ENGINE_SSOT.md, 05_API_CONTRACT.md, 13_JUDGE_PROOF_AND_P0_ACCEPTANCE.md
"""
from typing import List, Optional
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
        Aggregates synthetic buyer signals for candidate mandi + commodity.
        All data is explicitly labeled SYNTHETIC per SSOT Honesty Rules.
        """
        if db:
            buyers: List[BuyerModel] = (
                db.query(BuyerModel)
                .filter(
                    BuyerModel.mandi_id == mandi_id,
                    BuyerModel.commodity_id == commodity_id.lower().strip(),
                    BuyerModel.active == True,
                )
                .all()
            )
        else:
            buyers = []

        if buyers:
            active_count = len(buyers)
            avg_offer_strength = sum(b.offer_strength for b in buyers) / float(active_count)
            avg_reliability = sum(b.reliability_score for b in buyers) / float(active_count)

            # Demand score mapping
            demand_counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
            for b in buyers:
                dl = b.demand_level.upper()
                if dl in demand_counts:
                    demand_counts[dl] += 1
                else:
                    demand_counts["MEDIUM"] += 1

            if demand_counts["HIGH"] >= demand_counts["MEDIUM"] and demand_counts["HIGH"] > demand_counts["LOW"]:
                overall_demand = DemandLevel.HIGH
                demand_score = 90.0
            elif demand_counts["LOW"] > demand_counts["MEDIUM"] and demand_counts["LOW"] > demand_counts["HIGH"]:
                overall_demand = DemandLevel.LOW
                demand_score = 35.0
            else:
                overall_demand = DemandLevel.MEDIUM
                demand_score = 65.0

            # Availability score (up to 5 active buyers maxes out at 100)
            availability_score = min(active_count * 20.0, 100.0)

            # Composite buyer signal score (0-100)
            buyer_signal_score = (
                BUYER_SIGNAL_WEIGHTS["demand"] * demand_score
                + BUYER_SIGNAL_WEIGHTS["availability"] * availability_score
                + BUYER_SIGNAL_WEIGHTS["offer_strength"] * avg_offer_strength
                + BUYER_SIGNAL_WEIGHTS["reliability"] * avg_reliability
            )

            return BuyerSignal(
                active_buyer_count=active_count,
                demand_level=overall_demand,
                offer_strength=round(avg_offer_strength, 1),
                reliability=round(avg_reliability, 1),
                buyer_signal_score=round(buyer_signal_score, 1),
                classification=DataClassification.SYNTHETIC,
                source_label="Synthetic demo dataset",
            )

        # Deterministic synthetic fallback when db query is empty
        # Generates deterministic values based on mandi_id hash
        seed_val = abs(hash(mandi_id + commodity_id))
        count = 2 + (seed_val % 4)
        offer = 60.0 + (seed_val % 30)
        rel = 70.0 + (seed_val % 25)
        demand = DemandLevel.HIGH if (seed_val % 2 == 0) else DemandLevel.MEDIUM
        d_score = 85.0 if demand == DemandLevel.HIGH else 60.0
        b_score = (
            BUYER_SIGNAL_WEIGHTS["demand"] * d_score
            + BUYER_SIGNAL_WEIGHTS["availability"] * (count * 20.0)
            + BUYER_SIGNAL_WEIGHTS["offer_strength"] * offer
            + BUYER_SIGNAL_WEIGHTS["reliability"] * rel
        )

        return BuyerSignal(
            active_buyer_count=count,
            demand_level=demand,
            offer_strength=round(float(offer), 1),
            reliability=round(float(rel), 1),
            buyer_signal_score=round(float(b_score), 1),
            classification=DataClassification.SYNTHETIC,
            source_label="Synthetic demo dataset",
        )
