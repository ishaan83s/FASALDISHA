import requests
import pandas as pd
from datetime import datetime


# ============================================================
# WEATHER SERVICE
# ============================================================

WEATHER_API_URL = (
    "https://api.open-meteo.com/v1/forecast"
)


def get_weather_forecast(
    latitude,
    longitude,
    forecast_days=14
):
    """
    Get daily weather forecast for a location.

    Returns:
    - Date
    - Temperature
    - Rainfall
    - Humidity
    """

    params = {

        "latitude": latitude,

        "longitude": longitude,

        "daily": (
            "temperature_2m_mean,"
            "precipitation_sum,"
            "relative_humidity_2m_mean"
        ),

        "forecast_days": forecast_days,

        "timezone": "auto"
    }

    try:

        response = requests.get(
            WEATHER_API_URL,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

    except requests.RequestException as e:

        raise RuntimeError(
            f"Weather API request failed: {e}"
        )


    # ========================================================
    # VALIDATE RESPONSE
    # ========================================================

    if "daily" not in data:

        raise ValueError(
            "Weather API returned no daily forecast data."
        )


    daily = data["daily"]


    # ========================================================
    # CREATE DATAFRAME
    # ========================================================

    weather_df = pd.DataFrame({

        "date": pd.to_datetime(
            daily["time"]
        ),

        "temperature": daily[
            "temperature_2m_mean"
        ],

        "rainfall": daily[
            "precipitation_sum"
        ],

        "humidity": daily[
            "relative_humidity_2m_mean"
        ]
    })


    # ========================================================
    # WEATHER FEATURES
    # ========================================================

    weather_df["heavy_rain_flag"] = (

        weather_df["rainfall"] > 10

    ).astype(int)


    weather_df["weather_severity"] = (

        weather_df["heavy_rain_flag"] * 2

        +

        (weather_df["temperature"] > 38)
        .astype(int)

        +

        (weather_df["humidity"] > 85)
        .astype(int)

    )


    # ========================================================
    # ROUND VALUES
    # ========================================================

    numeric_columns = [

        "temperature",

        "rainfall",

        "humidity"

    ]


    weather_df[numeric_columns] = (

        weather_df[numeric_columns]
        .round(2)

    )


    return weather_df


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    # Ahmedabad
    latitude = 23.0218
    longitude = 72.5922


    print(
        "\n========== 14-DAY WEATHER FORECAST ==========\n"
    )


    forecast = get_weather_forecast(

        latitude=latitude,

        longitude=longitude,

        forecast_days=14

    )


    print(
        forecast.to_string(
            index=False
        )
    )