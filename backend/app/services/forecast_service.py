"""
Forecast Integration Service: Bridges Backend to ML Engine.
SSOT Reference: 02_DATA_AND_ML_SSOT.md, 05_API_CONTRACT.md
"""
from typing import Optional
from sqlalchemy.orm import Session
from app.db.models import MandiPriceModel
from app.schemas.forecast import ForecastOutput
from ml.forecast_engine import get_forecast


class ForecastService:
    @staticmethod
    def get_forecast_for_mandi(
        commodity_id: str,
        mandi_id: Optional[str] = None,
        db: Optional[Session] = None,
        as_of_date: Optional[str] = None,
    ) -> ForecastOutput:
        """
        Retrieves ML price forecast for a specific commodity and mandi.
        Pulls latest mandi baseline price if available, and invokes ML forecast engine.
        """
        current_price = None
        if db and mandi_id:
            latest_price_record = (
                db.query(MandiPriceModel)
                .filter(
                    MandiPriceModel.mandi_id == mandi_id,
                    MandiPriceModel.commodity_id == commodity_id.lower().strip(),
                )
                .order_by(MandiPriceModel.price_date.desc())
                .first()
            )
            if latest_price_record:
                current_price = latest_price_record.modal_price

        return get_forecast(
            commodity_id=commodity_id,
            mandi_id=mandi_id,
            as_of_date=as_of_date,
            current_price_override=current_price,
        )
