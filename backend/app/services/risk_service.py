"""
Risk Assessment and Risk-Adjusted Return Calculation Service.
SSOT Reference: 02_DATA_AND_ML_SSOT.md, 03_DECISION_ENGINE_SSOT.md
"""
from typing import List, Tuple, Optional
from sqlalchemy.orm import Session
from app.schemas.geography import Commodity
from app.schemas.weather import WeatherSignal
from app.schemas.forecast import ForecastOutput
from app.schemas.common import RiskLevel, PerishabilityClass
from app.config.constants import RISK_WEIGHTS, RISK_PENALTY_FACTOR


class RiskService:
    @staticmethod
    def calculate_mandi_risk(
        commodity: Commodity,
        weather: WeatherSignal,
        distance_km: float,
        forecast: ForecastOutput,
        db: Optional[Session] = None,
    ) -> Tuple[float, RiskLevel, List[str]]:
        """
        Calculates composite mandi risk score (0-100), risk level band, and risk factors.
        """
        risk_factors: List[str] = []

        # 1. Weather component (0-100)
        if weather.status == "UNAVAILABLE":
            w_score = 15.0
        elif weather.impact_level == RiskLevel.CRITICAL:
            w_score = 90.0
            risk_factors.append("Critical weather disruption active")
        elif weather.impact_level == RiskLevel.HIGH:
            w_score = 75.0
            risk_factors.append("Heavy rain / waterlogging alert active")
        elif weather.impact_level == RiskLevel.MODERATE:
            w_score = 45.0
            risk_factors.append("Moderate weather caution in region")
        else:
            w_score = 15.0

        # 2. Official alert component (0-100)
        # Default baseline unless an alert is present in weather events
        a_score = 15.0
        if any(e.severity in [RiskLevel.HIGH, RiskLevel.CRITICAL] for e in weather.events):
            a_score = 80.0
            risk_factors.append("Official meteorological advisory triggered")

        # 3. Transport distance risk (0-100)
        t_score = min(max((distance_km / 2.0), 10.0), 85.0)
        if distance_km > 75.0:
            risk_factors.append(f"Long transit distance ({distance_km:.1f} km)")

        # 4. Perishability holding / spoilage risk (0-100)
        if commodity.perishability_class == PerishabilityClass.HIGHLY_PERISHABLE:
            p_score = 80.0
            risk_factors.append("Highly perishable crop: High spoilage urgency")
        elif commodity.perishability_class == PerishabilityClass.MODERATELY_PERISHABLE:
            p_score = 45.0
            risk_factors.append("Moderately perishable crop: Monitor storage conditions")
        else:
            p_score = 15.0

        # 5. Model uncertainty risk (0-100)
        u_score = max((1.0 - forecast.forecast_confidence) * 100.0, 10.0)

        # Composite weighted risk score
        risk_score = (
            RISK_WEIGHTS["weather"] * w_score
            + RISK_WEIGHTS["official_alert"] * a_score
            + RISK_WEIGHTS["transport"] * t_score
            + RISK_WEIGHTS["perishability"] * p_score
            + RISK_WEIGHTS["model_uncertainty"] * u_score
        )
        risk_score = round(min(max(risk_score, 0.0), 100.0), 1)

        # Determine Risk Band
        if risk_score <= 25.0:
            level = RiskLevel.LOW
        elif risk_score <= 50.0:
            level = RiskLevel.MODERATE
        elif risk_score <= 75.0:
            level = RiskLevel.HIGH
        else:
            level = RiskLevel.CRITICAL

        return risk_score, level, risk_factors

    @staticmethod
    def calculate_risk_adjusted_return(
        net_return: float,
        risk_score: float,
    ) -> float:
        """
        Calculates risk-adjusted net return:
        riskPenalty = netReturn * (riskScore / 100) * RISK_PENALTY_FACTOR
        riskAdjustedReturn = netReturn - riskPenalty
        """
        risk_penalty = net_return * (risk_score / 100.0) * RISK_PENALTY_FACTOR
        risk_adjusted_return = net_return - risk_penalty
        return round(risk_adjusted_return, 2)
