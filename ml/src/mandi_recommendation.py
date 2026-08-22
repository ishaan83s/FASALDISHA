import pandas as pd


# ============================================================
# TRANSPORT COST CONFIGURATION
# ============================================================

TRANSPORT_COST_PER_KM_PER_TONNE = 8.0


# ============================================================
# RISK CALCULATION
# ============================================================

def calculate_market_risk(volatility_percent):
    """
    Classifies market risk based on price volatility.
    """

    if volatility_percent < 3:
        return "LOW"

    elif volatility_percent < 7:
        return "MEDIUM"

    else:
        return "HIGH"


def calculate_risk_penalty(risk_level, gross_revenue):
    """
    Applies a risk penalty to expected revenue.
    """

    risk_penalties = {
        "LOW": 0.01,
        "MEDIUM": 0.03,
        "HIGH": 0.06
    }

    penalty_rate = risk_penalties.get(
        risk_level,
        0.03
    )

    return gross_revenue * penalty_rate


# ============================================================
# MAIN MANDI RECOMMENDATION ENGINE
# ============================================================

def recommend_best_mandi(
    mandi_data,
    quantity_tonnes=1.0
):
    """
    Ranks mandis based on:

    1. Predicted price
    2. Distance
    3. Transport cost
    4. Market volatility
    5. Risk penalty
    6. Risk-adjusted net expected return
    """

    if mandi_data is None or mandi_data.empty:
        return pd.DataFrame(), None

    results = []

    for _, row in mandi_data.iterrows():

        # ----------------------------------------------------
        # REQUIRED DATA
        # ----------------------------------------------------

        mandi_name = str(
            row["Mandi"]
        )

        predicted_price = float(
            row["Predicted Price"]
        )

        distance = float(
            row["Distance (km)"]
        )

        volatility = float(
            row.get(
                "Volatility (%)",
                2.0
            )
        )


        # ----------------------------------------------------
        # TRANSPORT COST
        # ----------------------------------------------------

        transport_cost = (
            distance
            * TRANSPORT_COST_PER_KM_PER_TONNE
            * quantity_tonnes
        )


        # ----------------------------------------------------
        # GROSS REVENUE
        # ----------------------------------------------------

        gross_revenue = (
            predicted_price
            * quantity_tonnes
        )


        # ----------------------------------------------------
        # MARKET RISK
        # ----------------------------------------------------

        risk_level = calculate_market_risk(
            volatility
        )


        # ----------------------------------------------------
        # RISK PENALTY
        # ----------------------------------------------------

        risk_penalty = calculate_risk_penalty(
            risk_level,
            gross_revenue
        )


        # ----------------------------------------------------
        # NET EXPECTED RETURN
        # ----------------------------------------------------

        net_return = (
            gross_revenue
            - transport_cost
            - risk_penalty
        )


        # ----------------------------------------------------
        # STORE RESULT
        # ----------------------------------------------------

        results.append({

            "Mandi": mandi_name,

            "Predicted Price": round(
                predicted_price,
                2
            ),

            "Distance (km)": round(
                distance,
                2
            ),

            "Transport Cost": round(
                transport_cost,
                2
            ),

            "Volatility (%)": round(
                volatility,
                2
            ),

            "Risk Level": risk_level,

            "Risk Penalty": round(
                risk_penalty,
                2
            ),

            "Gross Revenue": round(
                gross_revenue,
                2
            ),

            "Net Expected Return": round(
                net_return,
                2
            )
        })


    # ========================================================
    # CREATE RESULT DATAFRAME
    # ========================================================

    result_df = pd.DataFrame(
        results
    )


    if result_df.empty:
        return result_df, None


    # ========================================================
    # SORT BEST TO WORST
    # ========================================================

    result_df = result_df.sort_values(
        by="Net Expected Return",
        ascending=False
    ).reset_index(
        drop=True
    )


    # ========================================================
    # ADD RANKING
    # ========================================================

    result_df.insert(
        0,
        "Rank",
        range(
            1,
            len(result_df) + 1
        )
    )


    # ========================================================
    # BEST MANDI
    # ========================================================

    best_mandi = result_df.iloc[0]

    return (
        result_df,
        best_mandi
    )


# ============================================================
# EXPLAINABLE AI RECOMMENDATION
# ============================================================

def generate_recommendation_reason(
    best_mandi,
    ranked_mandis
):
    """
    Generates a human-readable explanation
    for the selected best mandi.
    """

    if best_mandi is None:
        return (
            "No mandi recommendation could be generated "
            "because prediction data is unavailable."
        )


    mandi_name = best_mandi[
        "Mandi"
    ]

    net_return = best_mandi[
        "Net Expected Return"
    ]

    predicted_price = best_mandi[
        "Predicted Price"
    ]

    distance = best_mandi[
        "Distance (km)"
    ]

    risk = best_mandi[
        "Risk Level"
    ]

    transport_cost = best_mandi[
        "Transport Cost"
    ]


    # ========================================================
    # COMPARE WITH SECOND-BEST MANDI
    # ========================================================

    if len(ranked_mandis) > 1:

        second_best = ranked_mandis.iloc[1]

        advantage = (
            net_return
            - second_best[
                "Net Expected Return"
            ]
        )

        comparison = (
            f"It provides approximately "
            f"₹{advantage:.2f} more expected net return "
            f"than the second-best option "
            f"({second_best['Mandi']})."
        )

    else:

        comparison = (
            "It is the only available mandi for comparison."
        )


    # ========================================================
    # FINAL EXPLANATION
    # ========================================================

    explanation = f"""
🤖 AI Mandi Selection Explanation

{mandi_name} was selected as the best mandi because
it provides the highest risk-adjusted net expected return.

• Predicted price: ₹{predicted_price:.2f}

• Distance: {distance:.1f} km

• Estimated transport cost: ₹{transport_cost:.2f}

• Market risk: {risk}

• Final risk-adjusted expected return:
₹{net_return:.2f}

{comparison}

The recommendation considers predicted market price,
transport distance, transportation cost, and market risk
instead of selecting only the mandi with the highest price.
"""

    return explanation


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    test_data = pd.DataFrame({

        "Mandi": [
            "Current Mandi",
            "Nearby Mandi A",
            "Nearby Mandi B",
            "Nearby Mandi C"
        ],

        "Predicted Price": [
            3061.46,
            3180.00,
            3250.00,
            3100.00
        ],

        "Distance (km)": [
            0,
            12,
            28,
            8
        ],

        "Volatility (%)": [
            2.0,
            3.5,
            8.0,
            2.5
        ]
    })


    ranked_mandis, best_mandi = (
        recommend_best_mandi(
            test_data,
            quantity_tonnes=1
        )
    )


    print(
        "\n========== MANDI RANKING ==========\n"
    )

    print(
        ranked_mandis.to_string(
            index=False
        )
    )


    print(
        "\n========== AI EXPLANATION ==========\n"
    )

    print(
        generate_recommendation_reason(
            best_mandi,
            ranked_mandis
        )
    )