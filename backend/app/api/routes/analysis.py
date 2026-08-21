"""
Analysis Routes: Canonical Analysis Execution and Diagnostic Mandi Discovery.
SSOT Reference: 05_API_CONTRACT.md Section 3 & 4
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.analysis import AnalysisRequest, AnalysisResult
from app.schemas.geography import NearbyMandiCandidatePreview
from app.schemas.common import APIEnvelope, ErrorDetail, DataClassification
from app.services.analysis_service import AnalysisService
from app.services.mandi_service import MandiService
from app.services.geography_service import GeographyService

router = APIRouter(prefix="/analysis", tags=["Analysis Engine"])


@router.post("/run", response_model=APIEnvelope[AnalysisResult])
def run_analysis(request: AnalysisRequest, db: Session = Depends(get_db)):
    """
    Canonical End-to-End Analysis Endpoint (SSOT 05 Section 3).
    Executes full pipeline: geolocation search, forecasting, transport, synthetic buyer signals,
    weather/alerts risk, dynamic ranking, base decision, and risk override.
    """
    try:
        # Validate commodity existence
        commodity = GeographyService.get_commodity_by_id(request.commodity_id, db)
        if not commodity:
            return APIEnvelope(
                success=False,
                data=None,
                error=ErrorDetail(
                    code="COMMODITY_NOT_FOUND",
                    message=f"Commodity '{request.commodity_id}' is not in the active catalog",
                ),
            )

        result = AnalysisService.run_analysis(request, db)
        return APIEnvelope(success=True, data=result, error=None)
    except ValueError as ve:
        return APIEnvelope(
            success=False,
            data=None,
            error=ErrorDetail(code="INVALID_INPUT", message=str(ve)),
        )
    except Exception as e:
        return APIEnvelope(
            success=False,
            data=None,
            error=ErrorDetail(code="INTERNAL_ERROR", message=f"Analysis execution error: {str(e)}"),
        )


@router.get("/nearby-mandis", response_model=APIEnvelope[List[NearbyMandiCandidatePreview]])
def get_nearby_mandis_preview(
    latitude: float = Query(..., description="Authoritative farmer latitude"),
    longitude: float = Query(..., description="Authoritative farmer longitude"),
    commodity_id: str = Query(..., alias="commodityId", description="Commodity identifier"),
    radius_km: float = Query(100.0, alias="radiusKm", ge=1.0, le=300.0),
    db: Session = Depends(get_db),
):
    """
    Optional diagnostic/UI helper endpoint (SSOT 05 Section 4).
    Returns eligible mandis within radius without full ranking calculations.
    """
    # Validate commodity
    commodity = GeographyService.get_commodity_by_id(commodity_id, db)
    if not commodity:
        return APIEnvelope(
            success=False,
            data=None,
            error=ErrorDetail(code="COMMODITY_NOT_FOUND", message=f"Commodity '{commodity_id}' not found"),
        )

    raw_mandis = MandiService.find_nearby_mandis(
        latitude=latitude,
        longitude=longitude,
        commodity_id=commodity_id,
        radius_km=radius_km,
        db=db,
    )

    if not raw_mandis:
        return APIEnvelope(
            success=False,
            data=[],
            error=ErrorDetail(
                code="NO_ELIGIBLE_MANDI_IN_RADIUS",
                message=f"No active mandis trading '{commodity_id}' found within {radius_km} km",
            ),
        )

    previews = [
        NearbyMandiCandidatePreview(
            mandi=MandiService.to_schema(m),
            distance_km=dist,
            commodity_available=True,
            data_classification=DataClassification.REAL,
        )
        for m, dist in raw_mandis
    ]

    return APIEnvelope(success=True, data=previews, error=None)
