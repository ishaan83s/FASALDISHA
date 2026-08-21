"""
Compatibility Crops Endpoint.
SSOT Reference: 05_API_CONTRACT.md Section 2
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.geography import CropListResponse
from app.schemas.common import APIEnvelope
from app.services.geography_service import GeographyService

router = APIRouter(tags=["Crops Compatibility"])


@router.get("/crops", response_model=APIEnvelope[CropListResponse])
def get_crops_compatibility(db: Session = Depends(get_db)):
    """Compatibility endpoint returning all active commodities with perishability and category metadata."""
    commodities = GeographyService.get_commodities(db=db)
    return APIEnvelope(
        success=True,
        data=CropListResponse(crops=commodities),
        error=None,
    )
