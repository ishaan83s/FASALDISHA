"""
Market Data Service: Manages historical prices, arrivals, and mandi price lookups.
SSOT Reference: 01_SYSTEM_ARCHITECTURE.md, 04_DATABASE_CONTRACT.md
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.db.models import MandiPriceModel


class MarketDataService:
    @staticmethod
    def get_latest_price(
        mandi_id: str,
        commodity_id: str,
        db: Session,
    ) -> Optional[MandiPriceModel]:
        """Returns the most recent price record for a given mandi and commodity."""
        return (
            db.query(MandiPriceModel)
            .filter(
                MandiPriceModel.mandi_id == mandi_id,
                MandiPriceModel.commodity_id == commodity_id.lower().strip(),
            )
            .order_by(MandiPriceModel.price_date.desc())
            .first()
        )

    @staticmethod
    def get_price_history(
        mandi_id: str,
        commodity_id: str,
        days: int = 30,
        db: Optional[Session] = None,
    ) -> List[Dict[str, Any]]:
        """Returns recent historical price records for explainability."""
        if not db:
            return []
        records = (
            db.query(MandiPriceModel)
            .filter(
                MandiPriceModel.mandi_id == mandi_id,
                MandiPriceModel.commodity_id == commodity_id.lower().strip(),
            )
            .order_by(MandiPriceModel.price_date.desc())
            .limit(days)
            .all()
        )
        return [
            {
                "priceDate": r.price_date,
                "minPrice": r.min_price,
                "modalPrice": r.modal_price,
                "maxPrice": r.max_price,
                "sourceClassification": r.source_classification,
            }
            for r in records
        ]
