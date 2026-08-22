"""API Routes Package."""
from app.api.routes.health import router as health_router
from app.api.routes.geography import router as geography_router
from app.api.routes.crops import router as crops_router
from app.api.routes.analysis import router as analysis_router

__all__ = [
    "health_router",
    "geography_router",
    "crops_router",
    "analysis_router",
]
