import os
import pandas as pd
import numpy as np


INPUT_FILE = "data/synthetic_mandi_data.csv"
OUTPUT_FILE = "data/processed_mandi_data.csv"


def create_features(df):
    print("Creating ML features...")

    # Make sure date is datetime
    df["date"] = pd.to_datetime(df["date"])

    # Sort correctly for time-series calculations
    df = df.sort_values(
        by=["state", "district", "mandi", "commodity", "date"]
    ).reset_index(drop=True)

    # -------------------------
    # DATE FEATURES
    # -------------------------

    df["day_of_week"] = df["date"].dt.dayofweek
    df["month"] = df["date"].dt.month
    df["day_of_year"] = df["date"].dt.dayofyear

    # -------------------------
    # WEATHER / RAIN FLAG
    # -------------------------

    df["heavy_rain_flag"] = (df["rainfall"] > 10).astype(int)

    # Weather severity score
    df["weather_severity"] = (
        df["heavy_rain_flag"] * 2
        + (df["temperature"] > 38).astype(int)
        + (df["humidity"] > 85).astype(int)
    )

    # -------------------------
    # TIME-SERIES PRICE FEATURES
    # -------------------------

    group_cols = [
        "state",
        "district",
        "mandi",
        "commodity"
    ]

    # Previous days' prices
    df["price_lag_1"] = (
        df.groupby(group_cols)["modal_price"].shift(1)
    )

    df["price_lag_3"] = (
        df.groupby(group_cols)["modal_price"].shift(3)
    )

    df["price_lag_7"] = (
        df.groupby(group_cols)["modal_price"].shift(7)
    )

    # Rolling averages
    df["price_ma_7"] = (
        df.groupby(group_cols)["modal_price"]
        .transform(lambda x: x.shift(1).rolling(7).mean())
    )

    df["price_ma_14"] = (
        df.groupby(group_cols)["modal_price"]
        .transform(lambda x: x.shift(1).rolling(14).mean())
    )

    # Price volatility
    df["price_volatility_7"] = (
        df.groupby(group_cols)["modal_price"]
        .transform(lambda x: x.shift(1).rolling(7).std())
    )

    # -------------------------
    # PRICE TREND
    # -------------------------

    df["price_change_1d"] = (
        df["modal_price"] - df["price_lag_1"]
    )

    df["price_change_7d"] = (
        df["modal_price"] - df["price_lag_7"]
    )

    # -------------------------
    # DROP INITIAL ROWS
    # -------------------------

    df = df.dropna().reset_index(drop=True)

    return df


print("Loading synthetic dataset...")

df = pd.read_csv(INPUT_FILE)

print("Original shape:", df.shape)

processed_df = create_features(df)

os.makedirs("data", exist_ok=True)

processed_df.to_csv(OUTPUT_FILE, index=False)

print("\nSUCCESS!")
print("Processed shape:", processed_df.shape)
print("Saved to:", OUTPUT_FILE)

print("\nNew columns:")
print(processed_df.columns.tolist())

print("\nFirst 5 rows:")
print(processed_df.head())