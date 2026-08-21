"""
Forecast Schemas and ML Handoff Contract.
SSOT Reference: 02_DATA_AND_ML_SSOT.md, 05_API_CONTRACT.md
"""
from typing import List, Optional
from app.schemas.common import (
    BaseSchema,
    DataClassification,
    ModelType,
    ForecastScope,
)


class DailyForecastPoint(BaseSchema):
    day: int
    predicted_price: float
    confidence: Optional[float] = None


class ForecastOutput(BaseSchema):
    """
    Canonical ML Forecast Output Contract.
    Frozen interface for both ML module and backend consumption.
    """
    current_price: float
    forecast_1_day: float
    forecast_3_day: float
    forecast_7_day: float
    expected_peak_price: float
    peak_day: int
    peak_alert: bool = False
    daily_forecast: List[DailyForecastPoint] = []
    forecast_confidence: float = 0.70
    model_type: ModelType = ModelType.PRECOMPUTED
    history_window_days: int = 30
    history_classification: DataClassification = DataClassification.SEEDED
    history_source_label: str = "Agmarknet Historical / Seeded Series"
    forecast_scope: ForecastScope = ForecastScope.DIRECT_MODEL
