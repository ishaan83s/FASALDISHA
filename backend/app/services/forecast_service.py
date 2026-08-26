"""
Forecast Service: Consumes ML Boundary via ForecastOutput Contract.
SSOT Reference: 02_DATA_AND_ML_SSOT.md, 05_API_CONTRACT.md
"""
import sys
import os
from typing import Optional
from app.schemas.forecast import ForecastOutput

# Ensure project root is in sys.path for direct ml package resolution
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from ml.forecast_engine import get_forecast as ml_get_forecast


class ForecastService:
    @staticmethod
    def get_forecast(
        commodity_id: str,
        mandi_id: Optional[str] = None,
        as_of_date: Optional[str] = None,
        current_price_override: Optional[float] = None,
    ) -> ForecastOutput:
        """
        Retrieves crop price forecast from ML module or contract-compliant precomputed fallback.
        The backend consumes ForecastOutput without depending on internal ML algorithms.
        """
        return ml_get_forecast(
            commodity_id=commodity_id,
            mandi_id=mandi_id,
            as_of_date=as_of_date,
            current_price_override=current_price_override,
        )
