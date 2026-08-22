"""
Transport & Logistics Cost Calculation Service.
SSOT Reference: 03_DECISION_ENGINE_SSOT.md
"""
from typing import Tuple, Optional
from app.config.constants import TRANSPORT_RATE_PER_QUINTAL_PER_KM


class TransportService:
    @staticmethod
    def calculate_transport(
        distance_km: float,
        quantity_quintals: float,
        custom_rate: Optional[float] = None,
    ) -> Tuple[float, float]:
        """
        Calculate transport cost per quintal and total transport cost for the farmer's batch.
        Formula:
          transportCostPerQuintal = distanceKm * ratePerQuintalPerKm
          totalTransportCost = transportCostPerQuintal * quantityQuintals
        Returns: (transport_cost_per_quintal, total_transport_cost)
        """
        rate = custom_rate if (custom_rate is not None and custom_rate > 0) else TRANSPORT_RATE_PER_QUINTAL_PER_KM
        transport_cost_per_quintal = round(distance_km * rate, 2)
        total_transport_cost = round(transport_cost_per_quintal * quantity_quintals, 2)
        return (transport_cost_per_quintal, total_transport_cost)
