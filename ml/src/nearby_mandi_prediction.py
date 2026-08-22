import os
import sys
import pandas as pd
import joblib


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

SRC_DIR = os.path.join(
    BASE_DIR,
    "src"
)

if SRC_DIR not in sys.path:
    sys.path.append(
        SRC_DIR
    )


from nearby_mandis import get_nearby_mandis


DATA_FILE = os.path.join(
    BASE_DIR,
    "data",
    "processed_mandi_data.csv"
)

MODEL_FILE = os.path.join(
    BASE_DIR,
    "models",
    "mandi_price_model.pkl"
)

ENCODERS_FILE = os.path.join(
    BASE_DIR,
    "models",
    "label_encoders.pkl"
)

FEATURES_FILE = os.path.join(
    BASE_DIR,
    "models",
    "model_features.pkl"
)


# ============================================================
# LOAD MODEL RESOURCES
# ============================================================

def load_prediction_resources():

    model = joblib.load(
        MODEL_FILE
    )

    label_encoders = joblib.load(
        ENCODERS_FILE
    )

    feature_columns = joblib.load(
        FEATURES_FILE
    )

    return (
        model,
        label_encoders,
        feature_columns
    )


# ============================================================
# LOAD MARKET DATA
# ============================================================

def load_market_data():

    df = pd.read_csv(
        DATA_FILE
    )

    df["date"] = pd.to_datetime(
        df["date"]
    )

    return df


# ============================================================
# PREDICT ONE MANDI
# ============================================================

def predict_mandi_price(
    mandi_name,
    commodity,
    state=None,
    district=None
):

    model, label_encoders, feature_columns = (
        load_prediction_resources()
    )

    df = load_market_data()

    mandi_df = df[
        (
            df["mandi"]
            .astype(str)
            .str.strip()
            .str.lower()
            ==
            str(mandi_name)
            .strip()
            .lower()
        )
        &
        (
            df["commodity"]
            .astype(str)
            .str.strip()
            .str.lower()
            ==
            str(commodity)
            .strip()
            .lower()
        )
    ].copy()

    if state is not None:

        mandi_df = mandi_df[
            mandi_df["state"]
            .astype(str)
            .str.strip()
            .str.lower()
            ==
            str(state)
            .strip()
            .lower()
        ]

    if district is not None:

        mandi_df = mandi_df[
            mandi_df["district"]
            .astype(str)
            .str.strip()
            .str.lower()
            ==
            str(district)
            .strip()
            .lower()
        ]

    if mandi_df.empty:
        return None

    mandi_df = mandi_df.sort_values(
        "date"
    )

    latest_record = (
        mandi_df
        .iloc[-1]
        .copy()
    )

    # --------------------------------------------------------
    # ENCODE CATEGORICAL FEATURES
    # --------------------------------------------------------

    categorical_columns = [
        "state",
        "district",
        "mandi",
        "commodity",
        "crop_category"
    ]

    for column in categorical_columns:

        if (
            column not in latest_record.index
            or
            column not in label_encoders
        ):
            continue

        encoder = label_encoders[column]

        value = str(
            latest_record[column]
        )

        if value not in encoder.classes_:
            return None

        latest_record[column] = (
            encoder.transform(
                [value]
            )[0]
        )

    # --------------------------------------------------------
    # CREATE MODEL INPUT
    # --------------------------------------------------------

    X = pd.DataFrame(
        [latest_record]
    )

    X = X[
        feature_columns
    ]

    X = X.apply(
        pd.to_numeric,
        errors="coerce"
    )

    X = X.fillna(
        0
    )

    prediction = model.predict(
        X
    )[0]

    return round(
        float(prediction),
        2
    )


# ============================================================
# PREDICT NEARBY MANDIS
# ============================================================

def predict_nearby_mandis(
    mandi_df,
    commodity
):
    """
    Add ML predicted prices to a DataFrame
    returned by get_nearby_mandis().
    """

    if mandi_df is None or mandi_df.empty:
        return pd.DataFrame()

    mandi_df = mandi_df.copy()

    predictions = []

    for _, row in mandi_df.iterrows():

        mandi_name = str(
            row["Mandi"]
        )

        state = row.get(
            "State",
            None
        )

        district = row.get(
            "District",
            None
        )

        if pd.isna(state):
            state = None

        if pd.isna(district):
            district = None

        try:

            prediction = predict_mandi_price(
                mandi_name=mandi_name,
                commodity=commodity,
                state=state,
                district=district
            )

            print(
                f"{mandi_name}: {prediction}"
            )

        except Exception as error:

            print(
                f"Prediction failed for "
                f"{mandi_name}: {error}"
            )

            prediction = None

        predictions.append(
            prediction
        )

    mandi_df[
        "Predicted Price"
    ] = predictions

    mandi_df = mandi_df.dropna(
        subset=["Predicted Price"]
    )

    return mandi_df.reset_index(
        drop=True
    )


# ============================================================
# COMPLETE NEARBY MANDI PIPELINE
# ============================================================

def get_nearby_mandi_predictions(
    selected_mandi,
    commodity,
    radius_km=100,
    max_results=4
):
    """
    Complete pipeline:

    Selected mandi
        ↓
    Find nearby ML-supported mandis
        ↓
    Calculate road distance using OSRM
        ↓
    Predict price for each nearby mandi
        ↓
    Return complete comparison data
    """

    # --------------------------------------------------------
    # GET NEARBY MANDIS + ROAD ROUTES
    # --------------------------------------------------------

    nearby_df = get_nearby_mandis(
        selected_mandi=selected_mandi,
        radius_km=radius_km,
        max_results=max_results,
        commodity=commodity
    )

    if nearby_df.empty:
        return nearby_df

    # --------------------------------------------------------
    # PREDICT NEARBY MANDI PRICES
    # --------------------------------------------------------

    predicted_df = predict_nearby_mandis(
        mandi_df=nearby_df,
        commodity=commodity
    )

    return predicted_df


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print(
        "\n========== REAL NEARBY MANDI PREDICTIONS ==========\n"
    )

    predictions = get_nearby_mandi_predictions(
        selected_mandi="Ahmedabad APMC",
        commodity="Banana",
        radius_km=120,
        max_results=4
    )

    if predictions.empty:

        print(
            "No nearby mandi predictions available."
        )

    else:

        print(
            predictions.to_string(
                index=False
            )
        )