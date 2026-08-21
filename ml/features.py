"""
ML Feature Engineering Definitions.
SSOT Reference: 02_DATA_AND_ML_SSOT.md
"""
from typing import List, Dict, Any


def extract_time_series_features(price_series: List[float]) -> Dict[str, Any]:
    """
    Extract baseline time-series features for crop price forecasting:
    - Lag prices (t-1, t-3, t-7)
    - Rolling window statistics (mean, std)
    - Price momentum and volatility
    """
    if not price_series:
        return {}

    current_price = price_series[-1]
    lag_1 = price_series[-2] if len(price_series) > 1 else current_price
    lag_3 = price_series[-4] if len(price_series) > 3 else current_price
    lag_7 = price_series[-8] if len(price_series) > 7 else current_price

    rolling_mean_7 = sum(price_series[-7:]) / min(len(price_series), 7)

    return {
        "current_price": current_price,
        "lag_1": lag_1,
        "lag_3": lag_3,
        "lag_7": lag_7,
        "rolling_mean_7": rolling_mean_7,
        "momentum_7": (current_price - lag_7) / max(lag_7, 1.0),
    }
