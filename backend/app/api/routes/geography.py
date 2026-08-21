"""
Geography & Commodity Catalog Endpoints.
SSOT Reference: 05_API_CONTRACT.md
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.geography import State, District, Commodity
from app.schemas.common import APIEnvelope, ErrorDetail
from app.services.geography_service import GeographyService

router = APIRouter(prefix="/geography", tags=["Geography"])


@router.get("/states", response_model=APIEnvelope[List[State]])
def get_states(db: Session = Depends(get_db)):
    """Returns list of active states in catalog."""
    states = GeographyService.get_states(db)
    return APIEnvelope(success=True, data=states, error=None)


@router.get("/districts", response_model=APIEnvelope[List[District]])
def get_districts(
    state_id: Optional[str] = Query(None, alias="stateId", description="State ID to filter districts"),
    db: Session = Depends(get_db),
):
    """Returns districts for the given state context."""
    if not state_id:
        return APIEnvelope(
            success=False,
            data=None,
            error=ErrorDetail(code="INVALID_INPUT", message="Query parameter 'stateId' is required"),
        )
    
    districts = GeographyService.get_districts(state_id, db)
    if not districts:
        return APIEnvelope(
            success=False,
            data=None,
            error=ErrorDetail(
                code="GEOGRAPHY_CONTEXT_NOT_FOUND",
                message=f"No districts found for stateId '{state_id}'",
            ),
        )

    return APIEnvelope(success=True, data=districts, error=None)


@router.get("/commodities", response_model=APIEnvelope[List[Commodity]])
def get_commodities(
    state_id: Optional[str] = Query(None, alias="stateId"),
    district_id: Optional[str] = Query(None, alias="districtId"),
    db: Session = Depends(get_db),
):
    """Returns commodities available for the given context."""
    commodities = GeographyService.get_commodities(state_id=state_id, district_id=district_id, db=db)
    return APIEnvelope(success=True, data=commodities, error=None)
