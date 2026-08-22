import os
import sys
import pandas as pd


# ==========================================
# PROJECT PATH
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.append(
    os.path.join(BASE_DIR, "src")
)


# ==========================================
# IMPORT PROJECT MODULES
# ==========================================

from forecast import forecast_prices

from nearby_mandi_prediction import (
    get_nearby_mandi_predictions
)

from mandi_recommendation import (
    recommend_best_mandi,
    generate_recommendation_reason
)


# ==========================================
# CONFIGURATION
# ==========================================

SELECTED_MANDI = "Ahmedabad APMC"

COMMODITY = "Banana"

QUANTITY_TONNES = 1.0

FORECAST_DAYS = 14


# ==========================================
# RUN FULL PIPELINE
# ==========================================

def run_full_pipeline():

    print("\n")
    print("=" * 70)
    print("        SMART AGRICULTURAL MANDI ADVISOR")
    print("=" * 70)


    # ======================================
    # STEP 1: 14-DAY PRICE FORECAST
    # ======================================

    print(
        "\n[1/5] GENERATING 14-DAY PRICE FORECAST..."
    )

    forecast_df = forecast_prices(

    state="Gujarat",

    district="Ahmedabad",

    mandi=SELECTED_MANDI,

    commodity=COMMODITY,

    days=FORECAST_DAYS
)

    if forecast_df is None or forecast_df.empty:

        raise ValueError(
            "Price forecast could not be generated."
        )

    print(
        "\n========== PRICE FORECAST ==========\n"
    )

    print(
        forecast_df.to_string(
            index=False
        )
    )


    # ======================================
    # GET CURRENT MANDI FORECAST PRICE
    # ======================================

    latest_forecast_price = float(

        forecast_df[
            "Predicted Price"
        ].iloc[-1]

    )


    # ======================================
    # STEP 2: FIND + ROUTE NEARBY MANDIS
    # ======================================

    print(
        "\n[2/5] FINDING NEARBY MANDIS..."
    )

    nearby_predictions = get_nearby_mandi_predictions(
    selected_mandi=SELECTED_MANDI,
    commodity=COMMODITY,
    radius_km=120,
    max_results=4
)

    if nearby_predictions.empty:

        print(
            "\nWARNING: No nearby mandi predictions available."
        )

        return


    print(
        "\n========== NEARBY MANDI PREDICTIONS ==========\n"
    )

    print(
        nearby_predictions.to_string(
            index=False
        )
    )


    # ======================================
    # STEP 3: PREPARE DATA
    # ======================================

    print(
        "\n[3/5] PREPARING MANDI COMPARISON..."
    )


    mandi_comparison_df = (
        nearby_predictions.copy()
    )


    # --------------------------------------
    # USE ROAD DISTANCE
    # --------------------------------------

    if "Road Distance (km)" in (
        mandi_comparison_df.columns
    ):

        mandi_comparison_df[
            "Distance (km)"
        ] = mandi_comparison_df[
            "Road Distance (km)"
        ]


    # --------------------------------------
    # ADD VOLATILITY
    # --------------------------------------

    forecast_prices_list = (
        forecast_df[
            "Predicted Price"
        ].tolist()
    )

    average_forecast = (
        sum(forecast_prices_list)
        /
        len(forecast_prices_list)
    )

    volatility = (

        (
            max(forecast_prices_list)
            -
            min(forecast_prices_list)
        )

        /
        average_forecast

    ) * 100


    mandi_comparison_df[
        "Volatility (%)"
    ] = volatility


    # --------------------------------------
    # ADD CURRENT MANDI
    # --------------------------------------

    current_mandi_row = pd.DataFrame({

        "State": ["Current"],

        "District": ["Current"],

        "Mandi": [SELECTED_MANDI],

        "Distance (km)": [0.0],

        "Predicted Price": [
            latest_forecast_price
        ],

        "Volatility (%)": [
            volatility
        ]

    })


    # Keep only required columns

    required_columns = [

        "Mandi",

        "Predicted Price",

        "Distance (km)",

        "Volatility (%)"

    ]


    current_mandi_row = (
        current_mandi_row[
            required_columns
        ]
    )


    nearby_for_comparison = (
        mandi_comparison_df[
            required_columns
        ]
    )


    final_mandi_data = pd.concat(

        [
            current_mandi_row,

            nearby_for_comparison
        ],

        ignore_index=True

    )


    # ======================================
    # STEP 4: RANK MANDIS
    # ======================================

    print(
        "\n[4/5] CALCULATING TRANSPORT AND RISK..."
    )


    ranked_mandis, best_mandi = (

        recommend_best_mandi(

            final_mandi_data,

            quantity_tonnes=QUANTITY_TONNES

        )

    )


    if ranked_mandis.empty:

        print(
            "\nNo recommendation could be generated."
        )

        return


    print(
        "\n========== MANDI RANKING ==========\n"
    )

    print(

        ranked_mandis.to_string(

            index=False

        )

    )


    # ======================================
    # STEP 5: AI EXPLANATION
    # ======================================

    print(
        "\n[5/5] GENERATING FINAL RECOMMENDATION..."
    )


    explanation = (

        generate_recommendation_reason(

            best_mandi,

            ranked_mandis

        )

    )


    print(
        "\n"
        +
        "=" * 70
    )

    print(
        "FINAL MANDI RECOMMENDATION"
    )

    print(
        "=" * 70
    )


    print(

        explanation

    )


    print(
        "\n"
        +
        "=" * 70
    )

    print(
        "ANALYSIS COMPLETE"
    )

    print(
        "=" * 70
    )


    return {

        "forecast": forecast_df,

        "nearby_mandis": nearby_predictions,

        "ranking": ranked_mandis,

        "best_mandi": best_mandi

    }


# ==========================================
# RUN
# ==========================================

if __name__ == "__main__":

    run_full_pipeline()