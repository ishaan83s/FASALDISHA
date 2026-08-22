"""
Hybrid Data-Science & Domain Risk Assessment Service.
Tutor & SSOT Reference: 70% Data-Science Model-Driven (Forecast Volatility, Uncertainty, Distance Decay) 
                     + 30% Domain Logic (Perishability Shelf-Life & Severe Weather Overrides).
"""
from typing import Tuple, List, Optional
from app.schemas.weather import WeatherSignal
from app.schemas.common import PerishabilityClass, RiskLevel
from app.schemas.analysis import RiskSummary
from app.schemas.forecast import ForecastOutput


class RiskService:
    @staticmethod
    def calculate_mandi_risk(
        weather_signal: WeatherSignal,
        distance_km: float,
        perishability_class: PerishabilityClass,
        forecast_confidence: float,
        forecast: Optional[ForecastOutput] = None,
    ) -> Tuple[float, RiskLevel, List[str]]:
        """
        Calculates a hybrid risk score (0-100) combining:
        - 70% Data-Science / Model-Driven Risk: Price Forecast Volatility, ML Residual Uncertainty, Spatial Decay
        - 30% Domain / Human Safety Rules: Crop Shelf-Life Urgency, Severe Meteorological Disaster Alert
        """
        factors: List[str] = []

        # =========================================================================
        # 1. DATA-SCIENCE / MODEL-DRIVEN PILLAR (70% WEIGHT)
        # =========================================================================
        
        # A. Forecast Price Volatility (ML output variance)
        if forecast and forecast.daily_forecast and len(forecast.daily_forecast) > 1:
            prices = [d.predicted_price for d in forecast.daily_forecast]
            avg_p = sum(prices) / max(len(prices), 1)
            volatility_pct = ((max(prices) - min(prices)) / max(avg_p, 1.0)) * 100.0
            volatility_score = min(volatility_pct * 8.0, 100.0)
            if volatility_pct >= 5.0:
                factors.append(f"ML forecast volatility ({volatility_pct:.1f}%) indicates market price dispersion")
        else:
            volatility_score = 25.0

        # B. ML Model Residual Uncertainty (1 - confidence)
        model_uncertainty_score = max(0.0, min(100.0, (1.0 - forecast_confidence) * 100.0))
        if forecast_confidence < 0.75:
            factors.append(f"Model uncertainty penalty (Confidence: {int(forecast_confidence*100)}%)")

        # C. Spatial Transport Decay Risk
        spatial_decay_score = min(distance_km / 150.0, 1.0) * 100.0
        if distance_km > 75.0:
            factors.append(f"Logistics transit distance ({distance_km:.1f} km) adds route friction")

        # Composite Data-Science Score (0-100)
        ds_score = (
            0.40 * volatility_score
            + 0.35 * model_uncertainty_score
            + 0.25 * spatial_decay_score
        )

        # =========================================================================
        # 2. DOMAIN / HUMAN-SAFETY POLICY PILLAR (30% WEIGHT)
        # =========================================================================

        # A. Crop Perishability Shelf-Life Urgency
        if perishability_class == PerishabilityClass.HIGHLY_PERISHABLE:
            perishability_score = 85.0
            factors.append("Highly perishable commodity requires expedited market routing")
        elif perishability_class == PerishabilityClass.MODERATELY_PERISHABLE:
            perishability_score = 50.0
            factors.append("Moderately perishable crop with limited holding window")
        else:
            perishability_score = 15.0
            factors.append("Non-perishable commodity with flexible holding capability")

        # B. Severe Meteorological Alert Severity
        if weather_signal.impact_level == RiskLevel.CRITICAL:
            weather_score = 95.0
            factors.append("Critical severe weather alert in area")
        elif weather_signal.impact_level == RiskLevel.HIGH:
            weather_score = 80.0
            factors.append("High weather risk / rainfall affecting transit")
        elif weather_signal.impact_level == RiskLevel.MODERATE:
            weather_score = 45.0
        else:
            weather_score = 15.0

        # Composite Domain Score (0-100)
        domain_score = 0.50 * perishability_score + 0.50 * weather_score

        # =========================================================================
        # 3. HYBRID SYNTHESIS (70% Data-Science + 30% Domain)
        # =========================================================================
        risk_score = round(0.70 * ds_score + 0.30 * domain_score, 1)

        # Environmental Disaster Floor: Active high/critical weather alerts enforce a safety floor
        if weather_signal.impact_level == RiskLevel.CRITICAL:
            risk_score = max(risk_score, 80.0)
        elif weather_signal.impact_level == RiskLevel.HIGH:
            risk_score = max(risk_score, 55.0)

        risk_score = max(0.0, min(100.0, risk_score))

        # Risk band categorization
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
        forecast: Optional[ForecastOutput] = None,
    ) -> RiskSummary:
        """Build overall risk summary at origin using the hybrid model."""
        score, level, factors = RiskService.calculate_mandi_risk(
            weather_signal=weather_signal,
            distance_km=10.0,
            perishability_class=perishability_class,
            forecast_confidence=forecast_confidence,
            forecast=forecast,
        )
        return RiskSummary(
            overall_risk_score=score,
            risk_level=level,
            data_completeness=1.0,
            risk_factors=factors,
        )
