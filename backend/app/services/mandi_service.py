"""
Mandi Discovery & Haversine Distance Search Service.
SSOT Reference: 01_SYSTEM_ARCHITECTURE.md, 07_ENGINEERING_RULES.md
"""
import math
from typing import List, Tuple, Optional
from sqlalchemy.orm import Session
from app.db.models import MandiModel, MandiCommodityModel
from app.schemas.geography import Mandi
from app.schemas.common import DataClassification


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate the great-circle distance between two points in kilometers."""
    R = 6371.0  # Earth's radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2.0) ** 2
        + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2.0) ** 2
    )
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return round(R * c, 2)


class MandiService:
    @staticmethod
    def find_nearby_mandis(
        latitude: float,
        longitude: float,
        commodity_id: str,
        radius_km: float,
        db: Session,
    ) -> List[Tuple[MandiModel, float]]:
        """
        Dynamic nearby mandi discovery.
        - Filters active mandis carrying the selected commodity
        - Calculates Haversine distance
        - Includes all matches <= radiusKm (cross-district/cross-state)
        - Returns dynamic list sorted by distance
        """
        # Query active mandis that carry the commodity
        eligible_mandis = (
            db.query(MandiModel)
            .join(MandiCommodityModel, MandiCommodityModel.mandi_id == MandiModel.mandi_id)
            .filter(
                MandiModel.active == True,
                MandiCommodityModel.commodity_id == commodity_id.lower().strip(),
                MandiCommodityModel.active == True,
            )
            .all()
        )

        results: List[Tuple[MandiModel, float]] = []
        for m in eligible_mandis:
            dist = haversine_distance(latitude, longitude, m.latitude, m.longitude)
            if dist <= radius_km:
                results.append((m, dist))

        # Sort by distance
        results.sort(key=lambda x: x[1])
        return results

    @staticmethod
    def find_local_mandi(
        latitude: float,
        longitude: float,
        district_id: Optional[str],
        commodity_id: str,
        db: Session,
    ) -> Optional[Tuple[MandiModel, float]]:
        """Find the closest mandi (preferably within farmer's district or closest eligible)."""
        nearby = MandiService.find_nearby_mandis(latitude, longitude, commodity_id, 300.0, db)
        if not nearby:
            return None

        if district_id:
            for m, dist in nearby:
                if m.district_id == district_id.lower().strip():
                    return (m, dist)

        return nearby[0]

    @staticmethod
    def to_schema(model: MandiModel) -> Mandi:
        return Mandi(
            mandi_id=model.mandi_id,
            mandi_name=model.mandi_name,
            state_id=model.state_id,
            district_id=model.district_id,
            latitude=model.latitude,
            longitude=model.longitude,
            active=model.active,
            location_classification=DataClassification(model.location_classification),
        )
