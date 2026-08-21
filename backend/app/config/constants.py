"""
Canonical Constants Configuration for FasalDisha.
SSOT Reference: 03_DECISION_ENGINE_SSOT.md
"""

# Distance and Search Limits
RADIUS_KM_DEFAULT: float = 100.0
RADIUS_KM_MAX: float = 300.0
MAX_NEARBY_MANDIS_RETURNED: int = 20

# Default Transport Rate (INR per Quintal per Kilometer)
TRANSPORT_RATE_PER_QUINTAL_PER_KM: float = 2.5

# Risk Component Weights (Sum = 1.0)
RISK_WEIGHTS: dict[str, float] = {
    "weather": 0.30,
    "official_alert": 0.25,
    "transport": 0.20,
    "perishability": 0.15,
    "model_uncertainty": 0.10,
}

# Synthetic Buyer Signal Component Weights (Sum = 1.0)
BUYER_SIGNAL_WEIGHTS: dict[str, float] = {
    "demand": 0.40,
    "availability": 0.20,
    "offer_strength": 0.25,
    "reliability": 0.15,
}

# Ranking Score Weights (Sum = 1.0)
RANKING_WEIGHTS: dict[str, float] = {
    "risk_adjusted_return": 0.70,
    "buyer_signal": 0.20,
    "data_quality": 0.10,
}

# Decision & Risk Thresholds
TRAVEL_SIGNIFICANCE_THRESHOLD: float = 0.05
HOLD_SIGNIFICANCE_THRESHOLD: float = 0.05
HIGH_RISK_OVERRIDE_THRESHOLD: float = 51.0
CRITICAL_RISK_OVERRIDE_THRESHOLD: float = 76.0
PEAK_ALERT_THRESHOLD: float = 0.05
RISK_PENALTY_FACTOR: float = 0.20

# Seeded Demo Scenario Switch
SEEDED_RISK_OVERRIDE_SCENARIO_ENABLED: bool = True
