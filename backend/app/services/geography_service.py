"""
Geography Service: Manages States, Districts, and Commodity Catalogs.
SSOT Reference: 01_SYSTEM_ARCHITECTURE.md, 04_DATABASE_CONTRACT.md
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.models import StateModel, DistrictModel, CommodityModel
from app.schemas.geography import State, District, Commodity, ResolvedLocation
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
                latitude=d.latitude,
                longitude=d.longitude,
                active=d.active,
                source_classification=DataClassification(d.source_classification),
            )
            for d in districts
        ]

    @staticmethod
    def get_district_by_id(district_id: str, db: Session) -> Optional[District]:
        d = (
            db.query(DistrictModel)
            .filter(DistrictModel.district_id == district_id.lower().strip(), DistrictModel.active == True)
            .first()
        )
        if not d:
            return None
        return District(
            district_id=d.district_id,
            state_id=d.state_id,
            district_name=d.district_name,
            latitude=d.latitude,
            longitude=d.longitude,
            active=d.active,
            source_classification=DataClassification(d.source_classification),
        )

    @staticmethod
    def resolve_location(
        latitude: float,
        longitude: float,
        db: Session,
        max_confidence_radius_km: float = 120.0,
    ) -> ResolvedLocation:
        """
        Resolves device GPS coordinates against the supported geography catalog.
        Finds the nearest supported district reference centroid using Haversine distance.
        If nearest district is within max_confidence_radius_km, returns RESOLVED administrative context.
        If coordinates are outside supported regions, returns OUT_OF_BOUNDS without guessing.
        """
        from app.services.mandi_service import haversine_distance

        all_districts = (
            db.query(DistrictModel, StateModel.state_name)
            .join(StateModel, StateModel.state_id == DistrictModel.state_id)
            .filter(DistrictModel.active == True, StateModel.active == True)
            .all()
        )

        if not all_districts:
            return ResolvedLocation(
                latitude=latitude,
                longitude=longitude,
                in_supported_region=False,
                display_name="Geography catalog unavailable",
                source="GPS",
                resolution_status="OUT_OF_BOUNDS",
            )

        best_dist = float("inf")
        best_match = None
        best_state_name = ""

        for d_model, state_name in all_districts:
            if d_model.latitude is not None and d_model.longitude is not None:
                dist = haversine_distance(latitude, longitude, d_model.latitude, d_model.longitude)
                if dist < best_dist:
                    best_dist = dist
                    best_match = d_model
                    best_state_name = state_name

        if best_match and best_dist <= max_confidence_radius_km:
            return ResolvedLocation(
                state_id=best_match.state_id,
                state_name=best_state_name,
                district_id=best_match.district_id,
                district_name=best_match.district_name,
                latitude=latitude,
                longitude=longitude,
                distance_km=best_dist,
                in_supported_region=True,
                display_name=f"{best_match.district_name}, {best_state_name} (GPS)",
                source="GPS",
                resolution_status="RESOLVED",
            )

        return ResolvedLocation(
            state_id=None,
            state_name=None,
            district_id=None,
            district_name=None,
            latitude=latitude,
            longitude=longitude,
            distance_km=best_dist if best_match else None,
            in_supported_region=False,
            display_name=f"Location ({latitude:.2f}°N, {longitude:.2f}°E) is outside supported coverage regions (Maharashtra, Gujarat, Rajasthan)",
            source="GPS",
            resolution_status="OUT_OF_BOUNDS",
        )

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
