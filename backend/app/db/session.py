"""
SQLAlchemy Session and Database Engine Setup.
SSOT Reference: 04_DATABASE_CONTRACT.md
"""
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from app.config.settings import settings

connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    echo=False,
    future=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """Dependency for obtaining database sessions in API routes."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


import logging
from sqlalchemy import text

logger = logging.getLogger("fasaldisha.db")


def init_db() -> None:
    """Create all tables in the configured database and ensure columns exist."""
    Base.metadata.create_all(bind=engine)
    # Ensure latitude and longitude columns exist on districts table for SQLite
    try:
        with engine.connect() as conn:
            result = conn.execute(text("PRAGMA table_info(districts)")).fetchall()
            existing_cols = {row[1] for row in result}
            if "latitude" not in existing_cols:
                conn.execute(text("ALTER TABLE districts ADD COLUMN latitude FLOAT"))
            if "longitude" not in existing_cols:
                conn.execute(text("ALTER TABLE districts ADD COLUMN longitude FLOAT"))
            conn.commit()
    except Exception as exc:
        logger.error("Failed to execute database schema compatibility migration: %s", exc)
        raise RuntimeError(f"Database schema compatibility migration failed: {exc}") from exc
