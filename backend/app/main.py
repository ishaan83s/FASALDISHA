"""
FasalDisha Backend FastAPI Application Entrypoint.
SSOT Reference: 01_SYSTEM_ARCHITECTURE.md, 05_API_CONTRACT.md, 07_ENGINEERING_RULES.md
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.config.settings import settings
from app.db.session import init_db
from app.db.seed.seed_data import seed_database
from app.schemas.common import APIEnvelope, ErrorDetail
from app.api.routes import health, geography, crops, analysis

# Configure logging
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger("fasaldisha")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup & shutdown events."""
    logger.info("Initializing FasalDisha SQLite / Database...")
    init_db()
    seed_database()
    logger.info("Database initialized and seeded successfully.")
    yield
    logger.info("FasalDisha Backend shutting down.")


app = FastAPI(
    title="FasalDisha API",
    description="AI-Driven Crop Price Forecasting & Market Routing API (v2.0)",
    version="2.0.0",
    lifespan=lifespan,
)

# Configure CORS
origins = settings.CORS_ORIGINS if isinstance(settings.CORS_ORIGINS, list) else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
app.include_router(health.router)
app.include_router(geography.router)
app.include_router(crops.router)
app.include_router(analysis.router)


# Global Exception Handlers conforming to SSOT 05 & 07 (Global Envelope)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Wrap Pydantic validation errors in standard APIEnvelope."""
    errors = exc.errors()
    first_msg = errors[0]["msg"] if errors else "Invalid request input"
    first_loc = " -> ".join(str(loc) for loc in errors[0].get("loc", [])) if errors else ""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "data": None,
            "error": {
                "code": "INVALID_INPUT",
                "message": f"Validation failed at '{first_loc}': {first_msg}",
            },
        },
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Catch-all exception handler to guarantee APIEnvelope structure."""
    logger.error(f"Unhandled Exception on {request.url.path}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "data": None,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An internal server error occurred. Please check request parameters.",
            },
        },
    )
