"""
Health Check Route.
SSOT Reference: 01_SYSTEM_ARCHITECTURE.md, 08_VERTICAL_SLICE_PLAN.md
"""
from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.session import get_db

router = APIRouter(tags=["Health"])


@router.api_route("/health", methods=["GET", "HEAD"])
def health_check(db: Session = Depends(get_db)):
    """Health check endpoint for readiness and liveness verification."""
    db_status = "healthy"
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "service": "FasalDisha-Backend",
        "version": "2.1.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "database": db_status,
    }
