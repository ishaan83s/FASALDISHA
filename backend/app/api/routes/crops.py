"""
Crops Compatibility Route.
SSOT Reference: 05_API_CONTRACT.md Section 2
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.common import APIEnvelope
from app.schemas.geography import CropListResponse
from app.services.geography_service import GeographyService

router = APIRouter(tags=["Crops Compatibility"])


@router.get("/crops", response_model=APIEnvelope[CropListResponse])
def get_crops(db: Session = Depends(get_db)):
    """Compatibility endpoint returning all active commodities in CropListResponse format."""
    commodities = GeographyService.get_commodities(db=db)
    return APIEnvelope(
        success=True,
        data=CropListResponse(crops=commodities),
        error=None,
    )
