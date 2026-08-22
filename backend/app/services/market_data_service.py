"""
Market Data Service: Historical & Current APMC Price Access.
SSOT Reference: 02_DATA_AND_ML_SSOT.md, 04_DATABASE_CONTRACT.md
"""
from typing import Optional, Tuple
from sqlalchemy.orm import Session
from app.db.models import MandiPriceModel
from app.schemas.common import DataClassification


# Fallback base prices in INR/quintal if no historical record exists
DEFAULT_MODAL_PRICES: dict[str, float] = {
    "onion": 2350.0,
    "tomato": 1950.0,
    "potato": 1600.0,
    "wheat": 2480.0,
    "soybean": 4650.0,
    "mustard": 5450.0,
    "cotton": 7100.0,
}


class MarketDataService:
    @staticmethod
    def get_latest_price(
        mandi_id: str,
        commodity_id: str,
        db: Session,
    ) -> Tuple[float, DataClassification]:
        """
        Retrieve latest modal price for a given mandi and commodity.
        Returns (modal_price, data_classification).
        """
        price_record = (
            db.query(MandiPriceModel)
            .filter(
                MandiPriceModel.mandi_id == mandi_id,
                MandiPriceModel.commodity_id == commodity_id.lower().strip(),
            )
            .order_by(MandiPriceModel.price_date.desc())
            .first()
        )

        if price_record:
            return (price_record.modal_price, DataClassification(price_record.source_classification))

        # Baseline fallback
        base_price = DEFAULT_MODAL_PRICES.get(commodity_id.lower().strip(), 2000.0)
        return (base_price, DataClassification.SEEDED)
