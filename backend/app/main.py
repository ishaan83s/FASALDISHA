"""
FasalDisha Backend FastAPI Application Entry Point.
SSOT Reference: 01_SYSTEM_ARCHITECTURE.md, 05_API_CONTRACT.md
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.config.settings import settings
from app.db.session import init_db
from app.db.seed.seed_data import seed_database
from app.api.routes import (
    health_router,
    geography_router,
    crops_router,
    analysis_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event: initialize database schema and seed data on startup."""
    init_db()
    seed_database()
    yield


app = FastAPI(
    title="FasalDisha API",
    description="AI-Driven Crop Price Forecasting & Market Routing App (PS9)",
    version="2.1.0",
    lifespan=lifespan,
)

# CORS Configuration
origins = settings.CORS_ORIGINS if isinstance(settings.CORS_ORIGINS, list) else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global Exception Handlers conforming to SSOT 05 API Envelope
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle 422 validation errors with global envelope."""
    error_msg = "; ".join(f"{'.'.join(str(loc) for loc in err['loc'])}: {err['msg']}" for err in exc.errors())
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "data": None,
            "error": {
                "code": "INVALID_INPUT",
                "message": error_msg,
            },
        },
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP errors with global envelope."""
    code_map = {
        404: "NOT_FOUND",
        422: "INVALID_INPUT",
        400: "BAD_REQUEST",
        500: "INTERNAL_ERROR",
    }
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "data": None,
            "error": {
                "code": code_map.get(exc.status_code, "ERROR"),
                "message": str(exc.detail),
            },
        },
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Handle unexpected internal errors without leaking stack traces."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "data": None,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred during analysis orchestration.",
            },
        },
    )


# Include API Routers
app.include_router(health_router)
app.include_router(geography_router)
app.include_router(crops_router)
app.include_router(analysis_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True,
    )
