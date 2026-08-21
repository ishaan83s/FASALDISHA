"""
Geography Service: Manages States, Districts, and Commodity Catalogs.
SSOT Reference: 01_SYSTEM_ARCHITECTURE.md, 04_DATABASE_CONTRACT.md
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.models import StateModel, DistrictModel, CommodityModel
from app.schemas.geography import State, District, Commodity
from app.schemas.common import DataClassification, PerishabilityClass, CropGroup


class GeographyService:
    @staticmethod
    def get_states(db: Session) -> List[State]:
        states = db.query(StateModel).filter(StateModel.active == True).all()
        return [
            State(
                state_id=s.state_id,
                state_name=s.state_name,
                active=s.active,
                source_classification=DataClassification(s.source_classification),
            )
            for s in states
        ]

    @staticmethod
    def get_districts(state_id: str, db: Session) -> List[District]:
        districts = (
            db.query(DistrictModel)
            .filter(DistrictModel.state_id == state_id.lower().strip(), DistrictModel.active == True)
            .all()
        )
        return [
            District(
                district_id=d.district_id,
                state_id=d.state_id,
                district_name=d.district_name,
                active=d.active,
                source_classification=DataClassification(d.source_classification),
            )
            for d in districts
        ]

    @staticmethod
    def get_commodities(
        state_id: Optional[str] = None,
        district_id: Optional[str] = None,
        db: Optional[Session] = None,
    ) -> List[Commodity]:
        query = db.query(CommodityModel).filter(CommodityModel.active == True) if db else []
        commodities = query.all() if db else []
        return [
            Commodity(
                commodity_id=c.commodity_id,
                commodity_name=c.commodity_name,
                commodity_category=c.commodity_category,
                perishability_class=PerishabilityClass(c.perishability_class),
                crop_group=CropGroup(c.legacy_crop_group),
                unit=c.unit,
                active=c.active,
            )
            for c in commodities
        ]

    @staticmethod
    def get_commodity_by_id(commodity_id: str, db: Session) -> Optional[Commodity]:
        c = db.query(CommodityModel).filter(CommodityModel.commodity_id == commodity_id.lower().strip()).first()
        if not c:
            return None
        return Commodity(
            commodity_id=c.commodity_id,
            commodity_name=c.commodity_name,
            commodity_category=c.commodity_category,
            perishability_class=PerishabilityClass(c.perishability_class),
            crop_group=CropGroup(c.legacy_crop_group),
            unit=c.unit,
            active=c.active,
        )
