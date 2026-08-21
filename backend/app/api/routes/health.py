"""
Health Check Endpoint.
SSOT Reference: 05_API_CONTRACT.md
"""
from fastapi import APIRouter
from app.schemas.common import APIEnvelope

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=APIEnvelope[dict])
def health_check():
    """Returns application health status and version."""
    return APIEnvelope(
        success=True,
        data={
            "status": "healthy",
            "app": "FasalDisha-Backend",
            "version": "2.0.0",
            "round": 2,
            "architecture": "Modular Single-Process FastAPI",
        },
        error=None,
    )
