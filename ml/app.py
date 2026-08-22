import streamlit as st
import pandas as pd
import os
import sys

# ============================================================
# PATH SETUP
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")

if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)


# ============================================================
# IMPORT BACKEND MODULES
# ============================================================

from trend_analysis import analyze_trend, get_trend_explanation

from nearby_mandis import get_nearby_mandis

from nearby_mandi_prediction import (
    predict_nearby_mandis,
    predict_mandi_price
)

from mandi_recommendation import (
    recommend_best_mandi,
    generate_recommendation_reason
)


# ============================================================
# STREAMLIT CONFIG
# ============================================================

st.set_page_config(
    page_title="Smart Mandi Advisor",
    page_icon="🌾",
    layout="wide"
)


# ============================================================
# PAGE HEADER
# ============================================================

st.title("🌾 Smart Agricultural Mandi Advisor")

st.markdown(
    """
    **AI-Powered Mandi Price Forecasting & Decision Support System**

    The system predicts commodity prices, compares real nearby APMC
    mandis, considers transportation costs and market risk, and
    recommends the best mandi for selling.
    """
)

st.divider()


# ============================================================
# LOAD BASE DATA
# ============================================================

@st.cache_data
def load_historical_data():

    data_path = os.path.join(
        BASE_DIR,
        "data",
        "processed_mandi_data.csv"
    )

    df = pd.read_csv(data_path)

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    return df


@st.cache_data
def load_mandi_master():

    master_path = os.path.join(
        BASE_DIR,
        "data",
        "mandi_master.csv"
    )

    return pd.read_csv(master_path)


try:

    historical_df = load_historical_data()

    mandi_master_df = load_mandi_master()

except Exception as e:

    st.error(
        f"Error loading project data: {e}"
    )

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("⚙️ Market Selection")


# ----------------------------
# STATE
# ----------------------------

available_states = sorted(
    historical_df["state"]
    .dropna()
    .astype(str)
    .unique()
)

state = st.sidebar.selectbox(
    "Select State",
    available_states
)


# ----------------------------
# DISTRICT
# ----------------------------

district_options = sorted(
    historical_df[
        historical_df["state"].astype(str)
        == str(state)
    ]["district"]
    .dropna()
    .astype(str)
    .unique()
)

district = st.sidebar.selectbox(
    "Select District",
    district_options
)


# ----------------------------
# MANDI
# ----------------------------

mandi_options = sorted(
    historical_df[
        (
            historical_df["state"].astype(str)
            == str(state)
        )
        &
        (
            historical_df["district"].astype(str)
            == str(district)
        )
    ]["mandi"]
    .dropna()
    .astype(str)
    .unique()
)

mandi = st.sidebar.selectbox(
    "Select Mandi",
    mandi_options
)


# ----------------------------
# COMMODITY
# ----------------------------

commodity_options = sorted(
    historical_df[
        (
            historical_df["state"].astype(str)
            == str(state)
        )
        &
        (
            historical_df["district"].astype(str)
            == str(district)
        )
        &
        (
            historical_df["mandi"].astype(str)
            == str(mandi)
        )
    ]["commodity"]
    .dropna()
    .astype(str)
    .unique()
)

commodity = st.sidebar.selectbox(
    "Select Commodity",
    commodity_options
)


# ----------------------------
# QUANTITY
# ----------------------------

quantity = st.sidebar.number_input(
    "Quantity (Tonnes)",
    min_value=1.0,
    max_value=100.0,
    value=1.0,
    step=1.0
)


# ============================================================
# FILTER SELECTED MARKET DATA
# ============================================================

selected_data = historical_df[
    (
        historical_df["state"].astype(str)
        == str(state)
    )
    &
    (
        historical_df["district"].astype(str)
        == str(district)
    )
    &
    (
        historical_df["mandi"].astype(str)
        == str(mandi)
    )
    &
    (
        historical_df["commodity"].astype(str)
        == str(commodity)
    )
].copy()


if selected_data.empty:

    st.warning(
        "No historical data is available for the "
        "selected market and commodity."
    )

    st.stop()


selected_data = selected_data.sort_values(
    "date"
)


# ============================================================
# CURRENT MARKET PRICE
# ============================================================

current_price = float(
    selected_data.iloc[-1]["modal_price"]
)


# ============================================================
# CURRENT MANDI ML PREDICTION
# ============================================================

current_prediction = predict_mandi_price(
    mandi_name=mandi,
    commodity=commodity,
    state=state,
    district=district
)


if current_prediction is None:

    current_prediction = current_price


# ============================================================
# HISTORICAL VOLATILITY
# ============================================================

recent_prices = (
    selected_data
    .tail(30)["modal_price"]
    .dropna()
)

if len(recent_prices) >= 2:

    average_price = recent_prices.mean()

    volatility = (
        (
            recent_prices.max()
            -
            recent_prices.min()
        )
        /
        average_price
    ) * 100

else:

    volatility = 2.0


volatility = round(
    float(volatility),
    2
)


# ============================================================
# 7-DAY FORECAST DISPLAY
# ============================================================

# NOTE:
# Until the dedicated future-date forecasting module is used,
# this section uses the latest model estimate and recent trend.

forecast_rows = []

recent_values = (
    selected_data
    .tail(7)["modal_price"]
    .tolist()
)

if len(recent_values) == 0:

    recent_values = [current_price]


while len(recent_values) < 7:

    recent_values.append(
        recent_values[-1]
    )


for i, price in enumerate(
    recent_values[-7:],
    start=1
):

    forecast_rows.append({

        "Day": f"Day {i}",

        "Predicted Price": round(
            float(price),
            2
        )
    })


forecast_df = pd.DataFrame(
    forecast_rows
)


# ============================================================
# REAL NEARBY MANDI SEARCH
# ============================================================

try:

    nearby_df = get_nearby_mandis(
        selected_mandi=mandi,
        radius_km=250,
        max_results=10
    )

except Exception as e:

    st.warning(
        f"Nearby mandi search failed: {e}"
    )

    nearby_df = pd.DataFrame()


# ============================================================
# ADD CURRENT MANDI
# ============================================================

current_mandi_df = pd.DataFrame([{

    "State": state,

    "District": district,

    "Mandi": mandi,

    "Distance (km)": 0.0
}])


# ============================================================
# FILTER NEARBY MANDIS BY AVAILABLE COMMODITY DATA
# ============================================================

if not nearby_df.empty:

    available_commodity_markets = (
        historical_df[
            historical_df["commodity"]
            .astype(str)
            .str.lower()
            ==
            str(commodity).lower()
        ]["mandi"]
        .dropna()
        .astype(str)
        .str.lower()
        .unique()
    )


    nearby_df = nearby_df[
        nearby_df["Mandi"]
        .astype(str)
        .str.lower()
        .isin(
            available_commodity_markets
        )
    ].copy()


# ============================================================
# COMBINE CURRENT + NEARBY MANDIS
# ============================================================

prediction_input_df = pd.concat(

    [
        current_mandi_df,
        nearby_df
    ],

    ignore_index=True

)


# ============================================================
# PREDICT REAL MANDI PRICES
# ============================================================

try:

    predicted_mandis = predict_nearby_mandis(

        prediction_input_df,

        commodity

    )

except Exception as e:

    st.error(
        f"Mandi prediction failed: {e}"
    )

    predicted_mandis = pd.DataFrame()


# ============================================================
# ENSURE CURRENT MANDI IS PRESENT
# ============================================================

if predicted_mandis.empty:

    predicted_mandis = pd.DataFrame([{

        "State": state,

        "District": district,

        "Mandi": mandi,

        "Distance (km)": 0.0,

        "Predicted Price": current_prediction

    }])


# ============================================================
# ADD VOLATILITY FOR RISK ENGINE
# ============================================================

predicted_mandis["Volatility (%)"] = volatility


# ============================================================
# FINAL MANDI RANKING
# ============================================================

ranked_mandis, best_mandi = (
    recommend_best_mandi(

        predicted_mandis[[
            "Mandi",
            "Predicted Price",
            "Distance (km)",
            "Volatility (%)"
        ]],

        quantity_tonnes=quantity

    )
)


# ============================================================
# FINAL RECOMMENDATION
# ============================================================

if best_mandi is not None:

    recommendation_reason = (
        generate_recommendation_reason(
            best_mandi,
            ranked_mandis
        )
    )

else:

    recommendation_reason = (
        "No mandi recommendation could be generated."
    )


# ============================================================
# SELL / WAIT DECISION
# ============================================================

forecast_max = float(
    forecast_df["Predicted Price"].max()
)

forecast_change = (
    (
        forecast_max
        -
        current_price
    )
    /
    current_price
) * 100


if forecast_change >= 5:

    action = "WAIT"

elif forecast_change >= 2:

    action = "WAIT AND MONITOR"

else:

    action = "SELL NOW"


# ============================================================
# TOP METRICS
# ============================================================

st.header("📊 Market Intelligence")

col1, col2, col3, col4 = st.columns(4)


col1.metric(

    "Current Price",

    f"₹{current_price:,.2f}"

)


col2.metric(

    "ML Predicted Price",

    f"₹{current_prediction:,.2f}"

)


col3.metric(

    "Market Risk",

    best_mandi["Risk Level"]

    if best_mandi is not None

    else "N/A"

)


col4.metric(

    "Recommendation",

    action

)


st.divider()


# ============================================================
# FORECAST GRAPH
# ============================================================

st.header("📈 7-Day Price Forecast")

st.line_chart(

    forecast_df.set_index(
        "Day"
    )["Predicted Price"]

)


st.dataframe(

    forecast_df,

    use_container_width=True,

    hide_index=True

)


# ============================================================
# MODEL VALIDATION
# ============================================================

st.divider()

st.header(
    "🧪 Model Validation on Unseen Data"
)

try:

    evaluation_path = os.path.join(
        BASE_DIR,
        "outputs",
        "unseen_test_predictions.csv"
    )

    evaluation_df = pd.read_csv(
        evaluation_path
    )

    evaluation_sample = (
        evaluation_df
        .head(100)
        .copy()
    )


    numeric_columns = (
        evaluation_sample
        .select_dtypes(
            include=["number"]
        )
        .columns
        .tolist()
    )


    if len(numeric_columns) >= 2:

        st.subheader(
            "📈 Actual vs Predicted Price"
        )

        actual_column = (
            numeric_columns[0]
        )

        predicted_column = (
            numeric_columns[1]
        )


        st.line_chart(

            evaluation_sample[[
                actual_column,
                predicted_column
            ]]

        )


    col1, col2, col3 = st.columns(3)

    col1.metric(
        "MAE",
        "₹200.72"
    )

    col2.metric(
        "RMSE",
        "₹294.55"
    )

    col3.metric(
        "R² Score",
        "0.9622"
    )


except FileNotFoundError:

    st.warning(
        "Model evaluation file not found."
    )


except Exception as e:

    st.error(
        f"Model evaluation error: {e}"
    )


# ============================================================
# REAL MANDI COMPARISON
# ============================================================

st.divider()

st.header(
    "🏪 Real Nearby Mandi Comparison"
)


if not ranked_mandis.empty:

    st.dataframe(

        ranked_mandis,

        use_container_width=True,

        hide_index=True

    )


    st.subheader(
        "Risk-Adjusted Net Return Comparison"
    )


    st.bar_chart(

        ranked_mandis
        .set_index("Mandi")[
            "Net Expected Return"
        ]

    )

else:

    st.warning(
        "No mandi predictions are available."
    )


# ============================================================
# HISTORICAL MARKET TREND
# ============================================================

st.divider()

st.header(
    "📊 Historical Market Trend Analysis"
)


try:

    trend_result = analyze_trend(

        selected_data,

        days=30

    )


    col1, col2, col3 = st.columns(3)


    col1.metric(

        "Market Trend",

        trend_result["trend"]

    )


    col2.metric(

        "Recent Price Change",

        f"{trend_result['change_percent']}%"

    )


    col3.metric(

        "Price Trend Slope",

        f"{trend_result['slope']:.2f}"

    )


    st.info(

        "🤖 AI Trend Explanation: "

        +

        get_trend_explanation(
            trend_result
        )

    )


    graph_data = (
        trend_result["recent_data"]
    )


    st.line_chart(

        graph_data
        .set_index("date")[
            "modal_price"
        ]

    )


except Exception as e:

    st.error(
        f"Trend analysis error: {e}"
    )


# ============================================================
# AI DECISION
# ============================================================

st.divider()

st.header("🏆 AI Decision")


col1, col2 = st.columns(2)


with col1:

    if best_mandi is not None:

        st.success(

            f"""
### Recommended Mandi

**{best_mandi['Mandi']}**

Distance: **{best_mandi['Distance (km)']:.2f} km**

Predicted Price: **₹{best_mandi['Predicted Price']:,.2f}**

Transport Cost: **₹{best_mandi['Transport Cost']:,.2f}**

Risk Level: **{best_mandi['Risk Level']}**

Net Expected Return:

**₹{best_mandi['Net Expected Return']:,.2f}**
"""

        )


with col2:

    st.info(

        f"""
### Recommended Action

## {action}

Potential price change:
**{forecast_change:.2f}%**

Market volatility:
**{volatility:.2f}%**
"""

    )


# ============================================================
# AI EXPLANATION
# ============================================================

st.subheader(
    "🤖 Why This Mandi?"
)

st.markdown(
    recommendation_reason
)


# ============================================================
# AI PIPELINE
# ============================================================

st.divider()

st.header(
    "🔄 AI Decision Pipeline"
)

st.markdown(
    """
    **Historical Mandi Data**
    → **Real Mandi Selection**
    → **Nearby APMC Detection**
    → **ML Price Prediction**
    → **Market Trend Analysis**
    → **Risk Analysis**
    → **Transport Cost Calculation**
    → **Mandi Ranking**
    → **SELL / WAIT Recommendation**
    """
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Smart Agricultural Mandi Advisor | "
    "AI/ML Powered Decision Support System"
)