"""
Dynamic Risk Assessment & Perishability Calculation Service.
SSOT Reference: 03_DECISION_ENGINE_SSOT.md, 13_JUDGE_PROOF_AND_P0_ACCEPTANCE.md
"""
from typing import Tuple, List
from app.schemas.weather import WeatherSignal
from app.schemas.common import PerishabilityClass, RiskLevel
from app.schemas.analysis import RiskSummary
from app.config.constants import RISK_WEIGHTS


class RiskService:
    @staticmethod
    def calculate_mandi_risk(
        weather_signal: WeatherSignal,
        distance_km: float,
        perishability_class: PerishabilityClass,
        forecast_confidence: float,
    ) -> Tuple[float, RiskLevel, List[str]]:
        """
        Calculates a composite risk score (0-100) for a candidate mandi.
        Considers weather, transport distance, perishability urgency, and forecast uncertainty.
        """
        factors: List[str] = []

        # 1. Weather component (0-100)
        if weather_signal.impact_level == RiskLevel.CRITICAL:
            weather_score = 95.0
            factors.append("Critical severe weather alert in area")
        elif weather_signal.impact_level == RiskLevel.HIGH:
            weather_score = 80.0
            factors.append("High weather risk / rainfall affecting transit")
        elif weather_signal.impact_level == RiskLevel.MODERATE:
            weather_score = 45.0
            factors.append("Moderate weather conditions")
        else:
            weather_score = 15.0

        # 2. Official alert component (0-100)
        has_active_events = len(weather_signal.events) > 0
        alert_score = 80.0 if has_active_events and weather_signal.impact_level in [RiskLevel.HIGH, RiskLevel.CRITICAL] else 10.0
        if has_active_events:
            factors.append(f"Active meteorological event: {weather_signal.events[0].event_type}")

        # 3. Transport distance risk (0-100)
        transport_score = min(distance_km / 150.0, 1.0) * 100.0
        if distance_km > 75.0:
            factors.append(f"Transit distance ({distance_km} km) adds logistics risk")

        # 4. Perishability urgency (0-100)
        if perishability_class == PerishabilityClass.HIGHLY_PERISHABLE:
            perishability_score = 85.0
            factors.append("Highly perishable commodity requires expedited market routing")
        elif perishability_class == PerishabilityClass.MODERATELY_PERISHABLE:
            perishability_score = 50.0
            factors.append("Moderately perishable crop with limited holding window")
        else:
            perishability_score = 15.0
            factors.append("Non-perishable commodity with flexible holding capability")

        # 5. Model uncertainty (0-100)
        model_uncertainty_score = max(0.0, min(100.0, (1.0 - forecast_confidence) * 100.0))

        # Weighted calculation from constants
        w = RISK_WEIGHTS
        risk_score = (
            w["weather"] * weather_score
            + w["official_alert"] * alert_score
            + w["transport"] * transport_score
            + w["perishability"] * perishability_score
            + w["model_uncertainty"] * model_uncertainty_score
        )
        risk_score = round(max(0.0, min(100.0, risk_score)), 1)

        # Risk band assignment
        if risk_score <= 25.0:
            risk_level = RiskLevel.LOW
        elif risk_score <= 50.0:
            risk_level = RiskLevel.MODERATE
        elif risk_score <= 75.0:
            risk_level = RiskLevel.HIGH
        else:
            risk_level = RiskLevel.CRITICAL

        return (risk_score, risk_level, factors)

    @staticmethod
    def build_risk_summary(
        weather_signal: WeatherSignal,
        perishability_class: PerishabilityClass,
        forecast_confidence: float,
    ) -> RiskSummary:
        """Build overall risk summary at the farmer origin context."""
        score, level, factors = RiskService.calculate_mandi_risk(
            weather_signal=weather_signal,
            distance_km=10.0,
            perishability_class=perishability_class,
            forecast_confidence=forecast_confidence,
        )
        return RiskSummary(
            overall_risk_score=score,
            risk_level=level,
            data_completeness=1.0,
            risk_factors=factors,
        )
