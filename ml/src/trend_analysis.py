import pandas as pd
import numpy as np


def analyze_trend(df, days=30):
    """
    Analyze recent mandi price movement.
    Uses the modal_price column from the processed dataset.
    """

    data = df.copy()

    # Ensure date is datetime
    data["date"] = pd.to_datetime(data["date"])

    # Sort chronologically
    data = data.sort_values("date")

    # Get latest records
    recent_data = data.tail(days).copy()

    if len(recent_data) < 2:
        return {
            "trend": "INSUFFICIENT DATA",
            "change_percent": 0,
            "slope": 0,
            "recent_data": recent_data
        }

    prices = recent_data["modal_price"].values

    # Calculate linear trend
    x = np.arange(len(prices))
    slope = np.polyfit(x, prices, 1)[0]

    first_price = prices[0]
    last_price = prices[-1]

    change_percent = (
        (last_price - first_price)
        / max(first_price, 1)
    ) * 100

    # Determine trend
    if change_percent > 2:
        trend = "UPWARD"
    elif change_percent < -2:
        trend = "DOWNWARD"
    else:
        trend = "STABLE"

    return {
        "trend": trend,
        "change_percent": round(change_percent, 2),
        "slope": round(float(slope), 2),
        "recent_data": recent_data
    }


def get_trend_explanation(trend_result):
    """
    Convert mathematical trend into a farmer-friendly explanation.
    """

    trend = trend_result["trend"]
    change = trend_result["change_percent"]

    if trend == "UPWARD":
        return (
            f"Prices have increased by approximately "
            f"{change}% during the recent period. "
            f"The market is showing an upward trend."
        )

    elif trend == "DOWNWARD":
        return (
            f"Prices have decreased by approximately "
            f"{abs(change)}% during the recent period. "
            f"The market is showing a downward trend."
        )

    elif trend == "STABLE":
        return (
            "Prices are relatively stable with no major "
            "upward or downward movement detected."
        )

    return "Not enough historical data to determine a reliable trend."


if __name__ == "__main__":

    print("Loading processed data...")

    df = pd.read_csv("data/processed_mandi_data.csv")

    # Use one specific mandi + commodity
    sample = df[
        (df["state"] == "Gujarat") &
        (df["district"] == "Ahmedabad") &
        (df["commodity"] == "Banana")
    ].copy()

    result = analyze_trend(sample, days=30)

    print("\n========== TREND ANALYSIS ==========")

    print("Trend:", result["trend"])
    print("Price Change:", result["change_percent"], "%")
    print("Price Slope:", result["slope"])

    print("\nExplanation:")
    print(get_trend_explanation(result))

    print("\nRecent Data:")
    print(
        result["recent_data"][
            ["date", "modal_price"]
        ].tail(10)
    )