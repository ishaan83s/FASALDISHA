"""
Geography and Context Selection Routes.
SSOT Reference: 05_API_CONTRACT.md
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.common import APIEnvelope
from app.schemas.geography import State, District, Commodity, ResolvedLocation
from app.services.geography_service import GeographyService

router = APIRouter(prefix="/geography", tags=["Geography"])


@router.get("/states", response_model=APIEnvelope[List[State]])
def get_states(db: Session = Depends(get_db)):
    """Retrieve list of active states."""
    states = GeographyService.get_states(db)
    return APIEnvelope(success=True, data=states, error=None)


@router.get("/districts", response_model=APIEnvelope[List[District]])
def get_districts(
    state_id: str = Query(..., alias="stateId", description="State ID to filter districts"),
    db: Session = Depends(get_db),
):
    """Retrieve list of districts for the given state context."""
    districts = GeographyService.get_districts(state_id, db)
    return APIEnvelope(success=True, data=districts, error=None)


@router.get("/commodities", response_model=APIEnvelope[List[Commodity]])
def get_commodities(
    state_id: Optional[str] = Query(None, alias="stateId"),
    district_id: Optional[str] = Query(None, alias="districtId"),
    db: Session = Depends(get_db),
):
    """Retrieve list of commodities known in geographic context."""
    commodities = GeographyService.get_commodities(state_id, district_id, db)
    return APIEnvelope(success=True, data=commodities, error=None)


@router.get("/resolve-location", response_model=APIEnvelope[ResolvedLocation])
def resolve_location(
    latitude: float = Query(..., ge=-90.0, le=90.0, description="Farmer GPS Latitude"),
    longitude: float = Query(..., ge=-180.0, le=180.0, description="Farmer GPS Longitude"),
    db: Session = Depends(get_db),
):
    """
    Resolve device GPS coordinates to the nearest supported district reference location.
    Returns structured canonical location context or OUT_OF_BOUNDS without fake precision.
    """
    resolved = GeographyService.resolve_location(latitude, longitude, db)
    return APIEnvelope(success=True, data=resolved, error=None)
