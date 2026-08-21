"""
SQLAlchemy ORM Models.
SSOT Reference: 04_DATABASE_CONTRACT.md
"""
import uuid
from sqlalchemy import (
    Column,
    String,
    Boolean,
    Float,
    ForeignKey,
    DateTime,
    JSON,
    UniqueConstraint,
    Index,
)
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.session import Base


class StateModel(Base):
    __tablename__ = "states"

    state_id = Column(String(50), primary_key=True)
    state_name = Column(String(100), unique=True, nullable=False)
    active = Column(Boolean, default=True, nullable=False)
    source_classification = Column(String(50), default="REAL", nullable=False)

    districts = relationship("DistrictModel", back_populates="state", cascade="all, delete-orphan")
    mandis = relationship("MandiModel", back_populates="state")


class DistrictModel(Base):
    __tablename__ = "districts"

    district_id = Column(String(50), primary_key=True)
    state_id = Column(String(50), ForeignKey("states.state_id"), nullable=False)
    district_name = Column(String(100), nullable=False)
    active = Column(Boolean, default=True, nullable=False)
    source_classification = Column(String(50), default="REAL", nullable=False)

    state = relationship("StateModel", back_populates="districts")
    mandis = relationship("MandiModel", back_populates="district")

    __table_args__ = (
        UniqueConstraint("state_id", "district_name", name="uq_state_district"),
    )


class CommodityModel(Base):
    __tablename__ = "commodities"

    commodity_id = Column(String(50), primary_key=True)
    commodity_name = Column(String(100), nullable=False)
    commodity_category = Column(String(50), nullable=False)
    perishability_class = Column(String(50), nullable=False)
    legacy_crop_group = Column(String(50), nullable=False)
    unit = Column(String(20), default="quintal", nullable=False)
    active = Column(Boolean, default=True, nullable=False)

    mandi_availabilities = relationship("MandiCommodityModel", back_populates="commodity")


class MandiModel(Base):
    __tablename__ = "mandis"

    mandi_id = Column(String(50), primary_key=True)
    mandi_name = Column(String(100), nullable=False)
    state_id = Column(String(50), ForeignKey("states.state_id"), nullable=False)
    district_id = Column(String(50), ForeignKey("districts.district_id"), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    active = Column(Boolean, default=True, nullable=False)
    location_classification = Column(String(50), default="REAL", nullable=False)

    state = relationship("StateModel", back_populates="mandis")
    district = relationship("DistrictModel", back_populates="mandis")
    commodity_availabilities = relationship("MandiCommodityModel", back_populates="mandi")
    prices = relationship("MandiPriceModel", back_populates="mandi")
    buyers = relationship("BuyerModel", back_populates="mandi")

    __table_args__ = (
        Index("idx_mandi_state_district", "state_id", "district_id", "active"),
    )


class MandiCommodityModel(Base):
    __tablename__ = "mandi_commodities"

    mandi_id = Column(String(50), ForeignKey("mandis.mandi_id"), primary_key=True)
    commodity_id = Column(String(50), ForeignKey("commodities.commodity_id"), primary_key=True)
    active = Column(Boolean, default=True, nullable=False)
    source_classification = Column(String(50), default="REAL", nullable=False)

    mandi = relationship("MandiModel", back_populates="commodity_availabilities")
    commodity = relationship("CommodityModel", back_populates="mandi_availabilities")


class MandiPriceModel(Base):
    __tablename__ = "mandi_prices"

    price_id = Column(String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    mandi_id = Column(String(50), ForeignKey("mandis.mandi_id"), nullable=False)
    commodity_id = Column(String(50), ForeignKey("commodities.commodity_id"), nullable=False)
    price_date = Column(String(20), nullable=False)
    min_price = Column(Float, nullable=False)
    modal_price = Column(Float, nullable=False)
    max_price = Column(Float, nullable=False)
    source_classification = Column(String(50), default="SEEDED", nullable=False)

    mandi = relationship("MandiModel", back_populates="prices")

    __table_args__ = (
        Index("idx_price_commodity_mandi_date", "commodity_id", "mandi_id", "price_date"),
    )


class BuyerModel(Base):
    __tablename__ = "buyers"

    buyer_id = Column(String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    buyer_type = Column(String(50), nullable=False)  # wholesaler, retailer, aggregator
    commodity_id = Column(String(50), ForeignKey("commodities.commodity_id"), nullable=False)
    mandi_id = Column(String(50), ForeignKey("mandis.mandi_id"), nullable=False)
    active = Column(Boolean, default=True, nullable=False)
    demand_level = Column(String(20), default="MEDIUM", nullable=False)  # LOW, MEDIUM, HIGH
    offer_strength = Column(Float, default=50.0, nullable=False)
    reliability_score = Column(Float, default=50.0, nullable=False)
    data_classification = Column(String(50), default="SYNTHETIC", nullable=False)

    mandi = relationship("MandiModel", back_populates="buyers")


class WeatherEventModel(Base):
    __tablename__ = "weather_events"

    event_id = Column(String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    state_id = Column(String(50), nullable=True)
    district_id = Column(String(50), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    event_type = Column(String(50), nullable=False)
    severity = Column(String(20), default="LOW", nullable=False)  # LOW, MODERATE, HIGH, CRITICAL
    event_date = Column(String(20), nullable=True)
    classification = Column(String(50), default="SEEDED", nullable=False)
    source_label = Column(String(100), default="Deterministic seeded weather scenario", nullable=False)
    active = Column(Boolean, default=True, nullable=False)


class OfficialAlertModel(Base):
    __tablename__ = "official_alerts"

    alert_id = Column(String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    source_name = Column(String(100), nullable=False)
    region = Column(String(100), nullable=False)
    alert_type = Column(String(50), nullable=False)
    severity = Column(String(20), default="LOW", nullable=False)
    starts_at = Column(String(30), nullable=True)
    ends_at = Column(String(30), nullable=True)
    classification = Column(String(50), default="SEEDED", nullable=False)
    source_label = Column(String(100), nullable=False)
    active = Column(Boolean, default=True, nullable=False)


class ForecastCacheModel(Base):
    __tablename__ = "forecast_cache"

    cache_id = Column(String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    commodity_id = Column(String(50), nullable=False)
    mandi_id = Column(String(50), nullable=True)
    generated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    forecast_payload = Column(JSON, nullable=False)
    forecast_confidence = Column(Float, default=0.7, nullable=False)
    model_type = Column(String(30), default="PRECOMPUTED", nullable=False)
    forecast_scope = Column(String(30), default="DIRECT_MODEL", nullable=False)
