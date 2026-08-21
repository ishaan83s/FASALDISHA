"""
Common Schemas, Enums, and Envelope Models.
SSOT Reference: 02_DATA_AND_ML_SSOT.md, 03_DECISION_ENGINE_SSOT.md, 05_API_CONTRACT.md
"""
from enum import Enum
from typing import Generic, Optional, TypeVar
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class BaseSchema(BaseModel):
    """Base schema configured to auto-alias snake_case fields to camelCase."""
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class DataClassification(str, Enum):
    REAL = "REAL"
    CACHED_REAL = "CACHED_REAL"
    SEEDED = "SEEDED"
    SYNTHETIC = "SYNTHETIC"
    DERIVED = "DERIVED"
    UNAVAILABLE = "UNAVAILABLE"


class PerishabilityClass(str, Enum):
    HIGHLY_PERISHABLE = "HIGHLY_PERISHABLE"
    MODERATELY_PERISHABLE = "MODERATELY_PERISHABLE"
    NON_PERISHABLE = "NON_PERISHABLE"


class CropGroup(str, Enum):
    PERISHABLE = "PERISHABLE"
    NON_PERISHABLE = "NON_PERISHABLE"


class BaseDecision(str, Enum):
    SELL_NOW = "SELL_NOW"
    HOLD = "HOLD"
    TRAVEL = "TRAVEL"


class FinalRecommendation(str, Enum):
    SELL_NOW = "SELL_NOW"
    HOLD = "HOLD"
    SELL_AT_RECOMMENDED_MANDI = "SELL_AT_RECOMMENDED_MANDI"
    SELL_EARLY_DUE_TO_RISK = "SELL_EARLY_DUE_TO_RISK"
    AVOID_MANDI_OR_ROUTE = "AVOID_MANDI_OR_ROUTE"


class RiskLevel(str, Enum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class DemandLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class ModelType(str, Enum):
    LIVE = "LIVE"
    PRECOMPUTED = "PRECOMPUTED"


class ForecastScope(str, Enum):
    DIRECT_MODEL = "DIRECT_MODEL"
    DERIVED_PROPAGATION = "DERIVED_PROPAGATION"


class ErrorDetail(BaseSchema):
    code: str
    message: str


T = TypeVar("T")


class APIEnvelope(BaseModel, Generic[T]):
    """Standard global envelope as defined in SSOT 05."""
    success: bool
    data: Optional[T] = None
    error: Optional[ErrorDetail] = None

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )
