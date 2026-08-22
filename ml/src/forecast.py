import os
import joblib
import numpy as np
import pandas as pd

from weather_service import get_weather_forecast


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "mandi_price_model.pkl"
)

ENCODERS_PATH = os.path.join(
    BASE_DIR,
    "models",
    "label_encoders.pkl"
)

FEATURES_PATH = os.path.join(
    BASE_DIR,
    "models",
    "model_features.pkl"
)

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed_mandi_data.csv"
)

MANDI_MASTER_PATH = os.path.join(
    BASE_DIR,
    "data",
    "mandi_master.csv"
)


# ============================================================
# LOAD MODEL, ENCODERS AND DATA
# ============================================================

print("Loading trained model...")
model = joblib.load(MODEL_PATH)

print("Loading label encoders...")
label_encoders = joblib.load(ENCODERS_PATH)

print("Loading model features...")
model_features = joblib.load(FEATURES_PATH)

print("Loading processed dataset...")
df = pd.read_csv(DATA_PATH)

df["date"] = pd.to_datetime(df["date"])

print("Loading mandi location data...")
mandi_master = pd.read_csv(MANDI_MASTER_PATH)

print("Dataset loaded successfully!")
print("Dataset shape:", df.shape)


# ============================================================
# HELPER: ENCODE VALUE SAFELY
# ============================================================

def encode_value(column, value):

    encoder = label_encoders[column]

    value = str(value)

    if value not in encoder.classes_:

        raise ValueError(
            f"Unknown {column}: {value}\n"
            f"This value was not present in the training data."
        )

    return int(
        encoder.transform([value])[0]
    )


# ============================================================
# GET MANDI COORDINATES
# ============================================================

def get_mandi_coordinates(
    state,
    district,
    mandi
):

    matches = mandi_master[
        (
            mandi_master["state"]
            .astype(str)
            .str.lower()
            ==
            str(state).lower()
        )
        &
        (
            mandi_master["district"]
            .astype(str)
            .str.lower()
            ==
            str(district).lower()
        )
        &
        (
            mandi_master["mandi"]
            .astype(str)
            .str.lower()
            ==
            str(mandi).lower()
        )
    ]

    if matches.empty:

        raise ValueError(
            f"Coordinates not found for {mandi}."
        )

    selected = matches.iloc[0]

    return (
        float(selected["latitude"]),
        float(selected["longitude"])
    )


# ============================================================
# GET WEATHER FOR FORECAST DATES
# ============================================================

def get_forecast_weather(
    latitude,
    longitude,
    forecast_dates
):

    weather_df = get_weather_forecast(
        latitude=latitude,
        longitude=longitude,
        forecast_days=14
    )

    weather_df["date"] = pd.to_datetime(
        weather_df["date"]
    ).dt.normalize()

    required_dates = pd.to_datetime(
        forecast_dates
    ).normalize()

    weather_lookup = weather_df.set_index(
        "date"
    )

    weather_rows = []

    for forecast_date in required_dates:

        if forecast_date not in weather_lookup.index:

            raise ValueError(
                f"No weather forecast available for "
                f"{forecast_date.strftime('%Y-%m-%d')}."
            )

        row = weather_lookup.loc[forecast_date]

        weather_rows.append({

            "date": forecast_date,

            "temperature":
                float(row["temperature"]),

            "rainfall":
                float(row["rainfall"]),

            "humidity":
                float(row["humidity"]),

            "heavy_rain_flag":
                int(row["heavy_rain_flag"]),

            "weather_severity":
                int(row["weather_severity"])
        })

    return pd.DataFrame(
        weather_rows
    )


# ============================================================
# FORECAST FUNCTION
# ============================================================

def forecast_prices(
    state,
    district,
    mandi,
    commodity,
    days=14
):

    if days < 1:

        raise ValueError(
            "Forecast days must be at least 1."
        )

    if days > 14:

        raise ValueError(
            "This forecast service currently "
            "supports a maximum of 14 days."
        )


    print("\nSearching mandi data...")


    # --------------------------------------------------------
    # FILTER EXACT COMBINATION
    # --------------------------------------------------------

    filtered = df[
        (
            df["state"]
            .astype(str)
            .str.lower()
            ==
            str(state).lower()
        )
        &
        (
            df["district"]
            .astype(str)
            .str.lower()
            ==
            str(district).lower()
        )
        &
        (
            df["mandi"]
            .astype(str)
            .str.lower()
            ==
            str(mandi).lower()
        )
        &
        (
            df["commodity"]
            .astype(str)
            .str.lower()
            ==
            str(commodity).lower()
        )
    ].copy()


    if filtered.empty:

        raise ValueError(
            "\nNo data found for:\n"
            f"State: {state}\n"
            f"District: {district}\n"
            f"Mandi: {mandi}\n"
            f"Commodity: {commodity}"
        )


    # --------------------------------------------------------
    # SORT BY DATE
    # --------------------------------------------------------

    filtered = filtered.sort_values(
        "date"
    ).reset_index(
        drop=True
    )


    print(
        "Records found:",
        len(filtered)
    )


    # --------------------------------------------------------
    # LATEST RECORD
    # --------------------------------------------------------

    latest_row = filtered.iloc[-1].copy()

    latest_date = pd.to_datetime(
        latest_row["date"]
    ).normalize()

    current_price = float(
        latest_row["modal_price"]
    )


    print(
        "Latest historical date:",
        latest_date.strftime("%Y-%m-%d")
    )

    print(
        "Latest price:",
        current_price
    )


    # --------------------------------------------------------
    # CREATE FORECAST DATES
    # --------------------------------------------------------

    forecast_dates = [

        latest_date
        +
        pd.Timedelta(days=day)

        for day in range(
            1,
            days + 1
        )
    ]


    # --------------------------------------------------------
    # GET MANDI COORDINATES
    # --------------------------------------------------------

    latitude, longitude = (
        get_mandi_coordinates(
            state=state,
            district=district,
            mandi=mandi
        )
    )


    print(
        f"Using coordinates: "
        f"{latitude}, {longitude}"
    )


        # --------------------------------------------------------
    # GET WEATHER FOR FORECAST DATES
    # --------------------------------------------------------

    print(
        f"Fetching {days}-day weather forecast..."
    )

    try:

        weather_forecast = get_forecast_weather(
            latitude=latitude,
            longitude=longitude,
            forecast_dates=forecast_dates
        )

        weather_source = "LIVE WEATHER FORECAST"

        print(
            "Weather source: Live forecast"
        )

    except ValueError:

        print(
            "Live weather dates do not match "
            "the historical forecast period."
        )

        print(
            "Using latest available historical "
            "weather features for recursive forecasting."
        )

        # ----------------------------------------------------
        # HISTORICAL WEATHER FALLBACK
        # ----------------------------------------------------

        latest_weather = {
            "temperature": float(
                latest_row["temperature"]
            ),

            "rainfall": float(
                latest_row["rainfall"]
            ),

            "humidity": float(
                latest_row["humidity"]
            ),

            "heavy_rain_flag": int(
                latest_row["heavy_rain_flag"]
            ),

            "weather_severity": int(
                latest_row["weather_severity"]
            )
        }

        weather_rows = []

        for forecast_date in forecast_dates:

            weather_rows.append({
                "date": forecast_date,

                "temperature":
                    latest_weather["temperature"],

                "rainfall":
                    latest_weather["rainfall"],

                "humidity":
                    latest_weather["humidity"],

                "heavy_rain_flag":
                    latest_weather["heavy_rain_flag"],

                "weather_severity":
                    latest_weather["weather_severity"]
            })

        weather_forecast = pd.DataFrame(
            weather_rows
        )

        weather_source = (
            "LATEST AVAILABLE HISTORICAL WEATHER"
        )

        print(
            "Weather source: Historical fallback"
        )
        
    # ----------------------------------------------------
    # HISTORICAL WEATHER FALLBACK
    # ----------------------------------------------------

    latest_weather = {

        "temperature":
            float(latest_row["temperature"]),

        "rainfall":
            float(latest_row["rainfall"]),

        "humidity":
            float(latest_row["humidity"]),

        "heavy_rain_flag":
            int(latest_row["heavy_rain_flag"]),

        "weather_severity":
            int(latest_row["weather_severity"])
    }


    weather_rows = []


    for forecast_date in forecast_dates:

        weather_rows.append({

            "date":
                forecast_date,

            "temperature":
                latest_weather["temperature"],

            "rainfall":
                latest_weather["rainfall"],

            "humidity":
                latest_weather["humidity"],

            "heavy_rain_flag":
                latest_weather["heavy_rain_flag"],

            "weather_severity":
                latest_weather["weather_severity"]
        })


    weather_forecast = pd.DataFrame(
        weather_rows
    )


    weather_source = (
        "LATEST AVAILABLE HISTORICAL WEATHER"
    )

    print(
        "Weather source: Historical fallback"
    )


    # --------------------------------------------------------
    # ENCODE CATEGORICAL VALUES
    # --------------------------------------------------------

    encoded_state = encode_value(
        "state",
        latest_row["state"]
    )

    encoded_district = encode_value(
        "district",
        latest_row["district"]
    )

    encoded_mandi = encode_value(
        "mandi",
        latest_row["mandi"]
    )

    encoded_commodity = encode_value(
        "commodity",
        latest_row["commodity"]
    )

    encoded_crop_category = encode_value(
        "crop_category",
        latest_row["crop_category"]
    )


    # --------------------------------------------------------
    # PRICE HISTORY
    # --------------------------------------------------------

    price_history = filtered[
        "modal_price"
    ].tail(14).astype(
        float
    ).tolist()


    if len(price_history) < 14:

        price_history = (

            [current_price]
            *
            (
                14
                -
                len(price_history)
            )

            +

            price_history
        )


    # --------------------------------------------------------
    # CONSTANT FEATURES
    # --------------------------------------------------------

    is_perishable = int(
        latest_row["is_perishable"]
    )


    # --------------------------------------------------------
    # FORECAST STORAGE
    # --------------------------------------------------------

    results = []


    # ========================================================
    # RECURSIVE 14-DAY FORECAST
    # ========================================================

    for day in range(1, days + 1):


        # ----------------------------------------------------
        # FORECAST DATE
        # ----------------------------------------------------

        forecast_date = forecast_dates[
            day - 1
        ]


        # ----------------------------------------------------
        # GET WEATHER FOR THIS EXACT DAY
        # ----------------------------------------------------

        weather_row = weather_forecast.iloc[
            day - 1
        ]

        temperature = float(
            weather_row["temperature"]
        )

        rainfall = float(
            weather_row["rainfall"]
        )

        humidity = float(
            weather_row["humidity"]
        )

        heavy_rain_flag = int(
            weather_row["heavy_rain_flag"]
        )

        weather_severity = int(
            weather_row["weather_severity"]
        )


        # ----------------------------------------------------
        # LAG FEATURES
        # ----------------------------------------------------

        price_lag_1 = (
            price_history[-1]
        )

        price_lag_3 = (
            price_history[-3]
        )

        price_lag_7 = (
            price_history[-7]
        )


        # ----------------------------------------------------
        # ROLLING AVERAGES
        # ----------------------------------------------------

        price_ma_7 = float(
            np.mean(
                price_history[-7:]
            )
        )

        price_ma_14 = float(
            np.mean(
                price_history[-14:]
            )
        )


        # ----------------------------------------------------
        # PRICE VOLATILITY
        # ----------------------------------------------------

        price_volatility_7 = float(
            np.std(
                price_history[-7:]
            )
        )


        # ----------------------------------------------------
        # PRICE MOVEMENT
        # ----------------------------------------------------

        price_change_1d = float(
            price_history[-1]
            -
            price_history[-2]
        )

        price_change_7d = float(
            price_history[-1]
            -
            price_history[-8]
        )


        # ----------------------------------------------------
        # BUILD MODEL INPUT
        # ----------------------------------------------------

        input_data = pd.DataFrame([{

            # Location
            "state": encoded_state,
            "district": encoded_district,
            "mandi": encoded_mandi,

            # Commodity
            "commodity": encoded_commodity,
            "crop_category": encoded_crop_category,
            "is_perishable": is_perishable,

            # Calendar
            "day_of_week":
                forecast_date.dayofweek,

            "month":
                forecast_date.month,

            "day_of_year":
                forecast_date.dayofyear,

            # Historical price features
            "price_lag_1":
                price_lag_1,

            "price_lag_3":
                price_lag_3,

            "price_lag_7":
                price_lag_7,

            "price_ma_7":
                price_ma_7,

            "price_ma_14":
                price_ma_14,

            "price_volatility_7":
                price_volatility_7,

            # Price movement
            "price_change_1d":
                price_change_1d,

            "price_change_7d":
                price_change_7d,

            # Weather for this forecast date
            "temperature":
                temperature,

            "rainfall":
                rainfall,

            "humidity":
                humidity,

            "heavy_rain_flag":
                heavy_rain_flag,

            "weather_severity":
                weather_severity

        }])


        # ----------------------------------------------------
        # EXACT MODEL FEATURE ORDER
        # ----------------------------------------------------

        X_input = input_data[
            model_features
        ]


        # ----------------------------------------------------
        # PREDICT
        # ----------------------------------------------------

        prediction = float(
            model.predict(
                X_input
            )[0]
        )


        # ----------------------------------------------------
        # SAVE RESULT
        # ----------------------------------------------------

        results.append({

            "Day":
                day,

            "Date":
                forecast_date.strftime(
                    "%Y-%m-%d"
                ),

            "Predicted Price":
                round(
                    prediction,
                    2
                ),

            "Temperature":
                round(
                    temperature,
                    2
                ),

            "Rainfall":
                round(
                    rainfall,
                    2
                ),

            "Humidity":
                round(
                    humidity,
                    2
                ),

            "Weather Severity":
                weather_severity

        })


        # ----------------------------------------------------
        # UPDATE HISTORY
        #
        # Prediction from this day becomes input
        # for the next forecast day.
        # ----------------------------------------------------

        price_history.append(
            prediction
        )

        price_history = (
            price_history[-14:]
        )


    # ========================================================
    # RETURN RESULTS
    # ========================================================

    return pd.DataFrame(
        results
    )


# ============================================================
# RUN TEST
# ============================================================

if __name__ == "__main__":

    result = forecast_prices(

        state="Gujarat",

        district="Ahmedabad",

        mandi="Ahmedabad APMC",

        commodity="Banana",

        days=14
    )


    print(
        "\n========== 14-DAY PRICE FORECAST ==========\n"
    )


    print(
        result.to_string(
            index=False
        )
    )


    print(
        "\n=========================================="
    )