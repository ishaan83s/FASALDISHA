"""
Analysis and Nearby Mandi Discovery Routes.
SSOT Reference: 05_API_CONTRACT.md
"""
from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.common import APIEnvelope, DataClassification
from app.schemas.analysis import AnalysisRequest, AnalysisResult
from app.schemas.geography import NearbyMandiCandidatePreview
from app.services.analysis_service import AnalysisService
from app.services.mandi_service import MandiService

router = APIRouter(prefix="/analysis", tags=["Analysis"])


@router.post("/run", response_model=APIEnvelope[AnalysisResult])
def run_analysis(
    request: AnalysisRequest,
    db: Session = Depends(get_db),
):
    """
    Canonical End-to-End Farmer Crop Decision & Market Routing Analysis.
    Orchestrates location, prices, forecasts, transport, risk, and transparent ranking.
    """
    result = AnalysisService.run_analysis(request, db)
    return APIEnvelope(success=True, data=result, error=None)


@router.get("/nearby-mandis", response_model=APIEnvelope[List[NearbyMandiCandidatePreview]])
def get_nearby_mandis(
    latitude: float = Query(..., description="Authoritative Farmer Latitude"),
    longitude: float = Query(..., description="Authoritative Farmer Longitude"),
    commodity_id: str = Query(..., alias="commodityId", description="Selected Commodity ID"),
    radius_km: float = Query(100.0, alias="radiusKm", ge=1.0, le=300.0, description="Search radius in KM"),
    db: Session = Depends(get_db),
):
    """
    Diagnostic / Map Preview Helper Endpoint.
    Discovers commodity-eligible mandis within radius without ranking.
    """
    matches = MandiService.find_nearby_mandis(
        latitude=latitude,
        longitude=longitude,
        commodity_id=commodity_id,
        radius_km=radius_km,
        db=db,
    )

    previews = [
        NearbyMandiCandidatePreview(
            mandi=MandiService.to_schema(m),
            distance_km=dist,
            commodity_available=True,
            data_classification=DataClassification.REAL,
        )
        for m, dist in matches
    ]

    return APIEnvelope(success=True, data=previews, error=None)
