import math


def calculate_transport_cost(distance_km, quantity_tonnes=1):
    """
    Estimated transport cost.
    ₹8 per km per tonne.
    """
    return distance_km * quantity_tonnes * 8


def calculate_risk(predictions):
    """
    Calculate market risk based on forecast volatility.
    """
    prices = list(predictions)

    if len(prices) < 2:
        return "LOW", 0.0

    avg_price = sum(prices) / len(prices)
    max_price = max(prices)
    min_price = min(prices)

    volatility = ((max_price - min_price) / avg_price) * 100

    if volatility < 3:
        risk = "LOW"
    elif volatility < 7:
        risk = "MEDIUM"
    else:
        risk = "HIGH"

    return risk, round(volatility, 2)


def recommend_action(current_price, forecast_prices):
    """
    Decide whether farmer should SELL NOW or WAIT.
    """
    avg_forecast = sum(forecast_prices) / len(forecast_prices)
    max_forecast = max(forecast_prices)

    average_change = (
        (avg_forecast - current_price) / current_price
    ) * 100

    best_change = (
        (max_forecast - current_price) / current_price
    ) * 100

    if best_change >= 5:
        recommendation = "WAIT"
        reason = "Price is expected to increase significantly."
    elif best_change >= 2:
        recommendation = "WAIT AND MONITOR"
        reason = "A moderate price increase is expected."
    elif average_change <= -3:
        recommendation = "SELL NOW"
        reason = "Prices are expected to decline."
    else:
        recommendation = "SELL NOW"
        reason = "No major price improvement is expected."

    return {
        "recommendation": recommendation,
        "reason": reason,
        "average_change": round(average_change, 2),
        "best_change": round(best_change, 2),
        "average_forecast": round(avg_forecast, 2),
        "maximum_forecast": round(max_forecast, 2)
    }


def compare_mandis(current_mandi, mandi_options, quantity_tonnes=1):
    """
    Compare nearby mandis after transport cost.

    mandi_options format:

    [
        {
            "mandi": "Mandi Name",
            "predicted_price": 3200,
            "distance_km": 25
        }
    ]
    """

    results = []

    for mandi in mandi_options:

        transport_cost = calculate_transport_cost(
            mandi["distance_km"],
            quantity_tonnes
        )

        net_price = mandi["predicted_price"] - transport_cost

        results.append({
            "mandi": mandi["mandi"],
            "predicted_price": round(mandi["predicted_price"], 2),
            "distance_km": mandi["distance_km"],
            "transport_cost": round(transport_cost, 2),
            "net_price": round(net_price, 2)
        })

    results = sorted(
        results,
        key=lambda x: x["net_price"],
        reverse=True
    )

    return results


def generate_decision(
    current_price,
    forecast_prices,
    current_mandi,
    mandi_options,
    quantity_tonnes=1
):

    risk_level, volatility = calculate_risk(forecast_prices)

    action = recommend_action(
        current_price,
        forecast_prices
    )

    mandi_comparison = compare_mandis(
        current_mandi,
        mandi_options,
        quantity_tonnes
    )

    best_mandi = mandi_comparison[0]

    return {
        "current_price": round(current_price, 2),
        "forecast_prices": forecast_prices,
        "risk_level": risk_level,
        "volatility": volatility,
        "recommendation": action,
        "best_mandi": best_mandi,
        "mandi_comparison": mandi_comparison
    }