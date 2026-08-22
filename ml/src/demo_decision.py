from risk_engine import generate_decision


# ==========================================
# CURRENT MARKET DATA
# ==========================================

current_price = 2950

forecast_prices = [
    3002.19,
    3027.20,
    3060.29,
    3025.89,
    3062.92,
    3044.39,
    3061.46
]


# ==========================================
# NEARBY MANDI OPTIONS
# ==========================================

nearby_mandis = [

    {
        "mandi": "Current Mandi",
        "predicted_price": 3061.46,
        "distance_km": 0
    },

    {
        "mandi": "Nearby Mandi A",
        "predicted_price": 3180,
        "distance_km": 12
    },

    {
        "mandi": "Nearby Mandi B",
        "predicted_price": 3250,
        "distance_km": 28
    },

    {
        "mandi": "Nearby Mandi C",
        "predicted_price": 3100,
        "distance_km": 8
    }
]


# ==========================================
# RUN DECISION ENGINE
# ==========================================

result = generate_decision(

    current_price=current_price,

    forecast_prices=forecast_prices,

    current_mandi="Current Mandi",

    mandi_options=nearby_mandis,

    quantity_tonnes=1

)


# ==========================================
# DISPLAY RESULTS
# ==========================================

print("\n")
print("=" * 60)
print("        SMART AGRICULTURAL MANDI ADVISOR")
print("=" * 60)

print("\nCURRENT MARKET PRICE")
print(f"₹{result['current_price']:.2f}")

print("\n7-DAY PRICE FORECAST")

for i, price in enumerate(
    result["forecast_prices"],
    start=1
):
    print(f"Day {i}: ₹{price:.2f}")


print("\nFORECAST ANALYSIS")
print(
    f"Average Forecast: "
    f"₹{result['recommendation']['average_forecast']}"
)

print(
    f"Maximum Forecast: "
    f"₹{result['recommendation']['maximum_forecast']}"
)

print(
    f"Potential Best Gain: "
    f"{result['recommendation']['best_change']}%"
)


print("\nMARKET RISK ANALYSIS")
print(f"Risk Level: {result['risk_level']}")

print(
    f"Price Volatility: "
    f"{result['volatility']}%"
)


print("\nNEARBY MANDI COMPARISON")

print(
    f"{'Mandi':<20}"
    f"{'Price':>12}"
    f"{'Distance':>12}"
    f"{'Transport':>15}"
    f"{'Net Return':>15}"
)

print("-" * 75)

for mandi in result["mandi_comparison"]:

    print(
        f"{mandi['mandi']:<20}"
        f"₹{mandi['predicted_price']:>10.2f}"
        f"{mandi['distance_km']:>10.0f} km"
        f"₹{mandi['transport_cost']:>12.2f}"
        f"₹{mandi['net_price']:>12.2f}"
    )


print("\nBEST MANDI")

print(
    f"Mandi: "
    f"{result['best_mandi']['mandi']}"
)

print(
    f"Net Expected Return: "
    f"₹{result['best_mandi']['net_price']:.2f}"
)


print("\nFINAL RECOMMENDATION")

print(
    f"ACTION: "
    f"{result['recommendation']['recommendation']}"
)

print(
    f"REASON: "
    f"{result['recommendation']['reason']}"
)

print("\n" + "=" * 60)
print("ANALYSIS COMPLETE")
print("=" * 60)