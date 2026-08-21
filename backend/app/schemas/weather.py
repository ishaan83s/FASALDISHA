"""
Weather & Meteorological Alert Schemas.
SSOT Reference: 02_DATA_AND_ML_SSOT.md, 05_API_CONTRACT.md
"""
from typing import List, Optional
from app.schemas.common import (
    BaseSchema,
    DataClassification,
    RiskLevel,
)


class WeatherEventDetail(BaseSchema):
    event_id: Optional[str] = None
    event_type: str
    severity: RiskLevel = RiskLevel.LOW
    event_date: Optional[str] = None
    description: Optional[str] = None
    classification: DataClassification = DataClassification.SEEDED
    source_label: str = "Deterministic seeded weather scenario"


class WeatherSignal(BaseSchema):
    status: str = "ACTIVE"  # "ACTIVE" | "UNAVAILABLE"
    impact_level: RiskLevel = RiskLevel.LOW
    events: List[WeatherEventDetail] = []
    classification: DataClassification = DataClassification.SEEDED
    source_label: str = "Weather Impact Service"
