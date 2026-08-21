"""
Transport Cost Calculation Service.
SSOT Reference: 03_DECISION_ENGINE_SSOT.md
"""
from typing import Optional, Tuple
from app.config.constants import TRANSPORT_RATE_PER_QUINTAL_PER_KM


class TransportService:
    @staticmethod
    def calculate_transport(
        distance_km: float,
        quantity_quintals: float,
        custom_rate_per_quintal_per_km: Optional[float] = None,
    ) -> Tuple[float, float]:
        """
        Calculates transport costs:
        - transportCostPerQuintal = distanceKm * rate
        - totalTransportCost = transportCostPerQuintal * quantityQuintals
        """
        rate = (
            custom_rate_per_quintal_per_km
            if (custom_rate_per_quintal_per_km is not None and custom_rate_per_quintal_per_km > 0)
            else TRANSPORT_RATE_PER_QUINTAL_PER_KM
        )

        cost_per_quintal = round(distance_km * rate, 2)
        total_cost = round(cost_per_quintal * quantity_quintals, 2)
        return cost_per_quintal, total_cost
