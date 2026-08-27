"""
Geography & Commodity Schemas.
SSOT Reference: 04_DATABASE_CONTRACT.md, 05_API_CONTRACT.md
"""
from typing import List, Optional
from pydantic import Field
from app.schemas.common import (
    BaseSchema,
    DataClassification,
    PerishabilityClass,
    CropGroup,
)


class State(BaseSchema):
    state_id: str
    state_name: str
    active: bool = True
    source_classification: DataClassification = DataClassification.REAL


class District(BaseSchema):
    district_id: str
    state_id: str
    district_name: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    active: bool = True
    source_classification: DataClassification = DataClassification.REAL


class ResolvedLocation(BaseSchema):
    state_id: Optional[str] = None
    state_name: Optional[str] = None
    district_id: Optional[str] = None
    district_name: Optional[str] = None
    latitude: float
    longitude: float
    distance_km: Optional[float] = None
    in_supported_region: bool = True
    display_name: str
    source: str = "GPS"
    resolution_status: str = "RESOLVED"  # "RESOLVED" | "OUT_OF_BOUNDS"


class Commodity(BaseSchema):
    commodity_id: str
    commodity_name: str
    commodity_category: str
    perishability_class: PerishabilityClass
    crop_group: CropGroup
    unit: str = "quintal"
    active: bool = True


class Mandi(BaseSchema):
    mandi_id: str
    mandi_name: str
    state_id: str
    district_id: str
    latitude: float
    longitude: float
    active: bool = True
    location_classification: DataClassification = DataClassification.REAL


class NearbyMandiQueryParams(BaseSchema):
    latitude: float
    longitude: float
    commodity_id: str
    radius_km: float = Field(default=100.0, ge=1.0, le=300.0)


class NearbyMandiCandidatePreview(BaseSchema):
    mandi: Mandi
    distance_km: float
    commodity_available: bool = True
    data_classification: DataClassification = DataClassification.REAL


class CropListResponse(BaseSchema):
    crops: List[Commodity]
