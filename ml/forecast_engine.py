"""
ML Forecast Engine Integration Boundary.
Directly bridges trained XGBoost Model (mandi_price_model.pkl) with Backend Contracts.
SSOT Reference: 02_DATA_AND_ML_SSOT.md
"""
import json
import logging
import os
import sys
from typing import Optional, Tuple
from datetime import datetime, timedelta

# Initialize non-sensitive ML subsystem logger
logger = logging.getLogger("fasaldisha.ml")

# Ensure backend package is resolvable
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend"))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.schemas.forecast import ForecastOutput, DailyForecastPoint
from app.schemas.common import DataClassification, ModelType, ForecastScope

PRECOMPUTED_FILE = os.path.join(os.path.dirname(__file__), "precomputed_forecasts.json")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "mandi_price_model.pkl")
ENCODERS_PATH = os.path.join(os.path.dirname(__file__), "models", "label_encoders.pkl")
FEATURES_PATH = os.path.join(os.path.dirname(__file__), "models", "model_features.pkl")

# Cached ML resources
_model = None
_encoders = None
_features = None


def _load_ml_model():
    global _model, _encoders, _features
    if _model is not None:
        return _model, _encoders, _features

    if not (os.path.exists(MODEL_PATH) and os.path.exists(ENCODERS_PATH) and os.path.exists(FEATURES_PATH)):
        logger.warning(
            "Live ML model artifacts missing at %s. Activating precomputed fallback.",
            MODEL_PATH,
        )
        return None, None, None

    try:
        import joblib
        _model = joblib.load(MODEL_PATH)
        _encoders = joblib.load(ENCODERS_PATH)
        _features = joblib.load(FEATURES_PATH)
        logger.info(
            "Live XGBoost model successfully loaded from %s (%d features, %d encoders).",
            MODEL_PATH, len(_features), len(_encoders)
        )
    except Exception as e:
        logger.warning(
            "Failed to load live ML model (%s: %s). Activating precomputed fallback.",
            type(e).__name__, e
        )
        _model, _encoders, _features = None, None, None

    return _model, _encoders, _features


def _load_precomputed_forecasts() -> dict:
    if os.path.exists(PRECOMPUTED_FILE):
        try:
            with open(PRECOMPUTED_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.warning("Failed to parse precomputed forecasts file (%s: %s).", type(e).__name__, e)
            return {}
    return {}


COMMODITY_MAPPINGS = {
    "onion": ("Onion", "Vegetable", 1),
    "tomato": ("Tomato", "Vegetable", 1),
    "potato": ("Potato", "Vegetable", 1),
    "wheat": ("Wheat", "Cereal", 0),
    "cotton": ("Cotton", "Cash Crop", 0),
    "soybean": ("Soybean", "Oilseed", 0),
    "maize": ("Maize", "Cereal", 0),
    "banana": ("Banana", "Fruit", 1),
    "grapes": ("Grapes", "Fruit", 1),
}


def _try_live_xgboost_inference(
    commodity_id: str,
    mandi_id: Optional[str] = None,
    current_price_override: Optional[float] = None,
    state_id: Optional[str] = None,
    district_id: Optional[str] = None,
) -> Optional[ForecastOutput]:
    """
    Executes actual live inference on trained XGBoost model.
    Returns ForecastOutput with ModelType.LIVE only if .predict() executes successfully.
    """
    model, encoders, features = _load_ml_model()
    if model is None or encoders is None or features is None:
        return None

    cid = commodity_id.lower().strip()
    if cid not in COMMODITY_MAPPINGS:
        logger.info("Commodity '%s' has no trained XGBoost mapping. Using precomputed fallback.", commodity_id)
        return None

    comm_title, crop_cat, is_perishable = COMMODITY_MAPPINGS[cid]

    try:
        import pandas as pd
        import numpy as np

        # Resolve categorical values
        comm_classes = encoders["commodity"].classes_
        if comm_title not in comm_classes:
            logger.info("Commodity title '%s' not in trained encoder classes. Using precomputed fallback.", comm_title)
            return None
        enc_comm = int(encoders["commodity"].transform([comm_title])[0])

        cat_classes = encoders["crop_category"].classes_
        enc_cat = int(encoders["crop_category"].transform([crop_cat])[0]) if crop_cat in cat_classes else 0

        # 1. Dynamically resolve state
        state_classes = encoders["state"].classes_  # e.g., ['Gujarat', 'Maharashtra', 'Rajasthan']
        state_name = None

        if state_id:
            s_clean = state_id.strip().lower()
            for sc in state_classes:
                if sc.lower() == s_clean or s_clean in sc.lower():
                    state_name = sc
                    break

        if not state_name and mandi_id:
            m_clean = mandi_id.strip().lower()
            if any(k in m_clean for k in ["ahmedabad", "surat", "rajkot", "gondal", "unjha", "vadodara", "anand", "palanpur", "junagadh", "mehsana"]):
                state_name = "Gujarat"
            elif any(k in m_clean for k in ["jaipur", "jodhpur", "kota", "alwar", "sikar", "bikaner", "ajmer", "udaipur", "chomu", "muhana", "merta"]):
                state_name = "Rajasthan"
            elif any(k in m_clean for k in ["pune", "mumbai", "nashik", "ahmednagar", "solapur", "kolhapur", "nagpur", "chhatrapati", "csn", "shrigonda", "gultekdi", "chakan", "shirur", "junnar", "baramati", "lasalgaon", "pimpalgaon"]):
                state_name = "Maharashtra"

        if not state_name and district_id:
            d_clean = district_id.strip().lower()
            if any(k in d_clean for k in ["ahmedabad", "surat", "rajkot", "vadodara", "junagadh", "mehsana", "anand", "banaskantha"]):
                state_name = "Gujarat"
            elif any(k in d_clean for k in ["jaipur", "jodhpur", "kota", "alwar", "sikar", "bikaner", "ajmer", "udaipur"]):
                state_name = "Rajasthan"
            elif any(k in d_clean for k in ["pune", "nashik", "ahmednagar", "solapur", "kolhapur", "nagpur", "chhatrapati_sambhajinagar", "mumbai"]):
                state_name = "Maharashtra"

        if not state_name or state_name not in state_classes:
            logger.info(
                "State '%s' (state_id='%s', mandi_id='%s') is not recognized or not in trained XGBoost state classes (%s). Using fallback.",
                state_name, state_id, mandi_id, list(state_classes)
            )
            return None

        enc_state = int(encoders["state"].transform([state_name])[0])

        # 2. Dynamically resolve district
        dist_classes = encoders["district"].classes_
        enc_dist = None

        if district_id:
            d_clean = district_id.strip().lower().replace("_", " ")
            for dc in dist_classes:
                if dc.lower() == d_clean or d_clean in dc.lower():
                    enc_dist = int(encoders["district"].transform([dc])[0])
                    break

        if enc_dist is None and mandi_id:
            m_lower = mandi_id.lower()
            for d in dist_classes:
                if d.lower() in m_lower:
                    enc_dist = int(encoders["district"].transform([d])[0])
                    break

        if enc_dist is None:
            default_dist_by_state = {
                "Gujarat": "Ahmedabad",
                "Maharashtra": "Pune",
                "Rajasthan": "Kota",
            }
            fallback_dist = default_dist_by_state.get(state_name, dist_classes[0])
            enc_dist = int(encoders["district"].transform([fallback_dist])[0])

        # 3. Dynamically resolve mandi
        mandi_classes = encoders["mandi"].classes_
        enc_mandi = None
        if mandi_id:
            m_lower = mandi_id.lower()
            for m in mandi_classes:
                if any(part in m_lower for part in m.lower().split() if len(part) > 3):
                    enc_mandi = int(encoders["mandi"].transform([m])[0])
                    break

        if enc_mandi is None:
            default_mandi_by_state = {
                "Gujarat": "Ahmedabad APMC",
                "Maharashtra": "Pune Market Yard",
                "Rajasthan": "Kota APMC",
            }
            fallback_mandi = default_mandi_by_state.get(state_name, mandi_classes[0])
            enc_mandi = int(encoders["mandi"].transform([fallback_mandi])[0])

        base_p = current_price_override if (current_price_override and current_price_override > 0) else 2200.0

        # Construct 7-day future feature vectors
        now = datetime.now()
        rows = []
        for day in range(1, 8):
            future_dt = now + timedelta(days=day)
            row = {
                "state": enc_state,
                "district": enc_dist,
                "mandi": enc_mandi,
                "commodity": enc_comm,
                "crop_category": enc_cat,
                "is_perishable": is_perishable,
                "day_of_week": future_dt.weekday(),
                "month": future_dt.month,
                "day_of_year": future_dt.timetuple().tm_yday,
                "price_lag_1": base_p,
                "price_lag_3": base_p * 0.98,
                "price_lag_7": base_p * 0.95,
                "price_ma_7": base_p * 0.98,
                "price_ma_14": base_p * 0.96,
                "price_volatility_7": base_p * 0.025,
                "price_change_1d": base_p * 0.015,
                "price_change_7d": base_p * 0.04,
                "temperature": 27.5 + day * 0.4,
                "rainfall": 0.0,
                "humidity": 65.0,
                "heavy_rain_flag": 0,
                "weather_severity": 0,
            }
            rows.append(row)

        df_feat = pd.DataFrame(rows)[features]
        logger.info(
            "Executing live XGBoost model.predict(): commodity='%s', mandi='%s', state='%s' (encoded=%d), shape=%s",
            comm_title, mandi_id or "default", state_name, enc_state, df_feat.shape
        )
        raw_preds = model.predict(df_feat)
        logger.info(
            "Live XGBoost prediction successful: raw_preds=%s",
            [round(float(x), 2) for x in raw_preds]
        )

        # Scale predictions to reflect user's current price while preserving model trend
        base_pred = float(raw_preds[0])
        scale_factor = base_p / max(base_pred, 1.0) if abs(base_p - base_pred) > 5.0 else 1.0

        daily_points = []
        prices = []
        for idx, p in enumerate(raw_preds):
            scaled_price = round(float(p * scale_factor), 2)
            prices.append(scaled_price)
            daily_points.append(
                DailyForecastPoint(
                    day=idx + 1,
                    predicted_price=scaled_price,
                    confidence=round(0.78 - idx * 0.01, 2),
                )
            )

        f1 = prices[0]
        f3 = prices[2] if len(prices) > 2 else prices[-1]
        f7 = prices[6] if len(prices) > 6 else prices[-1]
        max_idx = int(np.argmax(prices))
        peak_price = prices[max_idx]
        peak_day = max_idx + 1
        peak_gain_ratio = (peak_price - base_p) / max(base_p, 1.0)
        peak_alert = peak_gain_ratio >= 0.05

        return ForecastOutput(
            current_price=base_p,
            forecast_1_day=f1,
            forecast_3_day=f3,
            forecast_7_day=f7,
            expected_peak_price=peak_price,
            peak_day=peak_day,
            peak_alert=peak_alert,
            daily_forecast=daily_points,
            forecast_confidence=0.78,
            model_type=ModelType.LIVE,
            history_window_days=45,
            history_classification=DataClassification.SYNTHETIC,
            history_source_label="Trained XGBoost Regressor (Synthetic training baseline)",
            forecast_scope=ForecastScope.DIRECT_MODEL,
        )
    except Exception as e:
        logger.warning(
            "Live XGBoost inference failed for commodity '%s' (%s: %s). Activating fallback.",
            commodity_id, type(e).__name__, e
        )
        return None


def get_forecast(
    commodity_id: str,
    mandi_id: Optional[str] = None,
    as_of_date: Optional[str] = None,
    current_price_override: Optional[float] = None,
    state_id: Optional[str] = None,
    district_id: Optional[str] = None,
) -> ForecastOutput:
    """
    Canonical ML boundary interface with strict provenance honesty.
    1. Attempts live XGBoost model inference -> ModelType.LIVE
    2. Falls back to precomputed forecast series -> ModelType.PRECOMPUTED
    3. Falls back to deterministic baseline heuristic -> ModelType.PRECOMPUTED (with fallback label)
    """
    # 1. Try Live Trained XGBoost Model First
    live_result = _try_live_xgboost_inference(
        commodity_id=commodity_id,
        mandi_id=mandi_id,
        current_price_override=current_price_override,
        state_id=state_id,
        district_id=district_id,
    )
    if live_result is not None:
        return live_result

    # 2. Fallback: Precomputed Forecasts
    logger.info("Serving precomputed forecast for commodity '%s', mandi '%s'.", commodity_id, mandi_id or "default")
    precomputed = _load_precomputed_forecasts()
    cid = commodity_id.lower().strip()

    if cid in precomputed:
        raw = precomputed[cid]
        base_current = raw["currentPrice"]

        # If a specific mandi current price is provided and differs, apply propagation rule (SSOT 02 Section 7)
        if current_price_override and current_price_override > 0 and abs(current_price_override - base_current) > 1.0:
            growth_ratio_1 = raw["forecast1Day"] / max(base_current, 1.0)
            growth_ratio_3 = raw["forecast3Day"] / max(base_current, 1.0)
            growth_ratio_7 = raw["forecast7Day"] / max(base_current, 1.0)
            growth_ratio_peak = raw["expectedPeakPrice"] / max(base_current, 1.0)

            f1 = round(current_price_override * growth_ratio_1, 2)
            f3 = round(current_price_override * growth_ratio_3, 2)
            f7 = round(current_price_override * growth_ratio_7, 2)
            peak_price = round(current_price_override * growth_ratio_peak, 2)

            daily = []
            for dp in raw.get("dailyForecast", []):
                ratio = dp["predictedPrice"] / max(base_current, 1.0)
                daily.append(
                    DailyForecastPoint(
                        day=dp["day"],
                        predicted_price=round(current_price_override * ratio, 2),
                        confidence=dp.get("confidence", 0.75),
                    )
                )

            peak_gain_ratio = (peak_price - current_price_override) / max(current_price_override, 1.0)
            peak_alert = peak_gain_ratio >= 0.05

            return ForecastOutput(
                current_price=current_price_override,
                forecast_1_day=f1,
                forecast_3_day=f3,
                forecast_7_day=f7,
                expected_peak_price=peak_price,
                peak_day=raw["peakDay"],
                peak_alert=peak_alert,
                daily_forecast=daily,
                forecast_confidence=raw.get("forecastConfidence", 0.75),
                model_type=ModelType.PRECOMPUTED,
                history_window_days=raw.get("historyWindowDays", 45),
                history_classification=DataClassification(raw.get("historyClassification", "SEEDED")),
                history_source_label=raw.get("historySourceLabel", "Seeded market baseline (Precomputed series)"),
                forecast_scope=ForecastScope.DERIVED_PROPAGATION,
            )

        daily = [
            DailyForecastPoint(
                day=dp["day"],
                predicted_price=dp["predictedPrice"],
                confidence=dp.get("confidence", 0.75),
            )
            for dp in raw.get("dailyForecast", [])
        ]

        return ForecastOutput(
            current_price=raw["currentPrice"],
            forecast_1_day=raw["forecast1Day"],
            forecast_3_day=raw["forecast3Day"],
            forecast_7_day=raw["forecast7Day"],
            expected_peak_price=raw["expectedPeakPrice"],
            peak_day=raw["peakDay"],
            peak_alert=raw.get("peakAlert", False),
            daily_forecast=daily,
            forecast_confidence=raw.get("forecastConfidence", 0.75),
            model_type=ModelType.PRECOMPUTED,
            history_window_days=raw.get("historyWindowDays", 45),
            history_classification=DataClassification(raw.get("historyClassification", "SEEDED")),
            history_source_label=raw.get("historySourceLabel", "Seeded market baseline (Precomputed series)"),
            forecast_scope=ForecastScope.DIRECT_MODEL,
        )

    # 3. Fallback: Deterministic Heuristic
    base_p = current_price_override if (current_price_override and current_price_override > 0) else 2000.0
    return ForecastOutput(
        current_price=base_p,
        forecast_1_day=round(base_p * 1.01, 2),
        forecast_3_day=round(base_p * 1.03, 2),
        forecast_7_day=round(base_p * 1.05, 2),
        expected_peak_price=round(base_p * 1.06, 2),
        peak_day=5,
        peak_alert=False,
        daily_forecast=[
            DailyForecastPoint(day=d, predicted_price=round(base_p * (1.0 + d * 0.01), 2), confidence=0.70)
            for d in range(1, 8)
        ],
        forecast_confidence=0.70,
        model_type=ModelType.PRECOMPUTED,
        history_window_days=30,
        history_classification=DataClassification.DERIVED,
        history_source_label="Deterministic baseline heuristic (Fallback)",
        forecast_scope=ForecastScope.DIRECT_MODEL,
    )
