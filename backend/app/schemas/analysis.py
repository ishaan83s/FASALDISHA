"""
Analysis Request and Response Schemas.
SSOT Reference: 03_DECISION_ENGINE_SSOT.md, 05_API_CONTRACT.md, 13_JUDGE_PROOF_AND_P0_ACCEPTANCE.md
"""
from typing import Any, Dict, List, Optional
from pydantic import Field
from app.schemas.common import (
    BaseSchema,
    DataClassification,
    BaseDecision,
    FinalRecommendation,
    RiskLevel,
    DemandLevel,
)
from app.schemas.geography import Commodity, Mandi
from app.schemas.forecast import ForecastOutput
from app.schemas.weather import WeatherSignal


class AnalysisRequest(BaseSchema):
    """Canonical Request for POST /analysis/run."""
    state_id: str
    district_id: str
    latitude: float = Field(ge=-90.0, le=90.0, description="Farmer Latitude (-90 to 90)")
    longitude: float = Field(ge=-180.0, le=180.0, description="Farmer Longitude (-180 to 180)")
    commodity_id: str
    quantity_quintals: float = Field(gt=0, description="Quantity in quintals")
    radius_km: float = Field(default=100.0, ge=1.0, le=300.0)
    transport_rate_per_quintal_per_km: Optional[float] = Field(
        default=None,
        description="Optional custom transport rate override in INR/quintal/km",
    )


class FarmerContext(BaseSchema):
    state_id: str
    district_id: str
    latitude: float
    longitude: float
    quantity_quintals: float
    radius_km: float


class SearchMetadata(BaseSchema):
    candidate_count: int
    search_status: str = "OK"  # "OK" | "NO_ELIGIBLE_MANDI_IN_RADIUS"
    cross_boundary_candidates_included: bool = False


class BuyerSignal(BaseSchema):
    active_buyer_count: int = 0
    demand_level: DemandLevel = DemandLevel.MEDIUM
    offer_strength: float = 50.0
    reliability: float = 50.0
    buyer_signal_score: float = 50.0
    classification: DataClassification = DataClassification.SYNTHETIC
    source_label: str = "Synthetic demo dataset"


class RankingBreakdown(BaseSchema):
    normalized_risk_adjusted_return: float
    buyer_signal_score: float
    data_quality_score: float
    top_factors: List[str] = []
    ranking_score: float


class CandidateMandi(BaseSchema):
    rank: int
    mandi: Mandi
    distance_km: float
    commodity_available: bool = True
    current_price: float
    forecast: ForecastOutput
    transport_cost_per_quintal: float
    total_transport_cost: float
    expected_revenue: float
    net_return: float
    risk_score: float
    risk_level: RiskLevel
    risk_adjusted_return: float
    buyer_signal: BuyerSignal
    weather_impact: WeatherSignal
    ranking_breakdown: RankingBreakdown
    ranking_score: float
    data_classification: Dict[str, Any] = {}


class RiskSummary(BaseSchema):
    overall_risk_score: float = 0.0
    risk_level: RiskLevel = RiskLevel.LOW
    data_completeness: float = 1.0
    risk_factors: List[str] = []


class DataProvenance(BaseSchema):
    coverage: Dict[str, Any] = {}
    buyer_data_classification: DataClassification = DataClassification.SYNTHETIC


class DecisionOutput(BaseSchema):
    base_decision: BaseDecision = BaseDecision.SELL_NOW
    final_recommendation: FinalRecommendation = FinalRecommendation.SELL_NOW
    risk_override_applied: bool = False
    recommended_mandi: Optional[Mandi] = None
    reason_codes: List[str] = []
    human_readable_reason: str = ""
    decision_confidence: float = 0.0


class AnalysisResult(BaseSchema):
    """
    Canonical Top-level Response for POST /analysis/run.
    Frozen response schema for backend and frontend integration.
    """
    commodity: Commodity
    farmer_context: FarmerContext
    search: SearchMetadata
    local_mandi: Optional[Mandi] = None
    forecast: ForecastOutput
    weather: WeatherSignal
    risk_summary: RiskSummary
    nearby_mandis: List[CandidateMandi] = []
    data_provenance: DataProvenance
    decision: DecisionOutput
