import os
import random
import numpy as np
import pandas as pd

random.seed(42)
np.random.seed(42)


# Synthetic locations for Phase 1
locations = [
    # Maharashtra
    {"state": "Maharashtra", "district": "Mumbai", "mandi": "Mumbai APMC"},
    {"state": "Maharashtra", "district": "Pune", "mandi": "Pune Market Yard"},
    {"state": "Maharashtra", "district": "Nashik", "mandi": "Nashik APMC"},
    {"state": "Maharashtra", "district": "Nagpur", "mandi": "Nagpur APMC"},
    {"state": "Maharashtra", "district": "Kolhapur", "mandi": "Kolhapur APMC"},
    {"state": "Maharashtra", "district": "Aurangabad", "mandi": "Chhatrapati Sambhajinagar APMC"},

    # Gujarat
    {"state": "Gujarat", "district": "Ahmedabad", "mandi": "Ahmedabad APMC"},
    {"state": "Gujarat", "district": "Surat", "mandi": "Surat APMC"},
    {"state": "Gujarat", "district": "Rajkot", "mandi": "Rajkot APMC"},
    {"state": "Gujarat", "district": "Vadodara", "mandi": "Vadodara APMC"},
    {"state": "Gujarat", "district": "Anand", "mandi": "Anand APMC"},
    {"state": "Gujarat", "district": "Banaskantha", "mandi": "Palanpur APMC"},

    # Rajasthan
    {"state": "Rajasthan", "district": "Jaipur", "mandi": "Jaipur APMC"},
    {"state": "Rajasthan", "district": "Jodhpur", "mandi": "Jodhpur APMC"},
    {"state": "Rajasthan", "district": "Kota", "mandi": "Kota APMC"},
    {"state": "Rajasthan", "district": "Udaipur", "mandi": "Udaipur APMC"},
    {"state": "Rajasthan", "district": "Ajmer", "mandi": "Ajmer APMC"},
    {"state": "Rajasthan", "district": "Bikaner", "mandi": "Bikaner APMC"},
]


# Crop categories
crops = [
    {"crop": "Tomato", "category": "Vegetable", "perishable": 1, "base_price": 1800},
    {"crop": "Onion", "category": "Vegetable", "perishable": 0, "base_price": 2200},
    {"crop": "Potato", "category": "Vegetable", "perishable": 0, "base_price": 1500},
    {"crop": "Wheat", "category": "Cereal", "perishable": 0, "base_price": 2500},
    {"crop": "Maize", "category": "Cereal", "perishable": 0, "base_price": 2100},
    {"crop": "Soybean", "category": "Oilseed", "perishable": 0, "base_price": 4300},
    {"crop": "Cotton", "category": "Cash Crop", "perishable": 0, "base_price": 6500},
    {"crop": "Banana", "category": "Fruit", "perishable": 1, "base_price": 3000},
    {"crop": "Grapes", "category": "Fruit", "perishable": 1, "base_price": 5000},
]


def generate_data():

    records = []

    # Generate one year of daily data
    dates = pd.date_range(
        start="2025-01-01",
        end="2025-12-31",
        freq="D"
    )

    for location in locations:
        for crop in crops:

            base_price = crop["base_price"]

            for date in dates:

                # Seasonal pattern
                day_of_year = date.dayofyear

                seasonal_effect = 0.12 * np.sin(
                    2 * np.pi * day_of_year / 365
                )

                # Random market fluctuation
                noise = np.random.normal(0, 0.06)

                # Price
                modal_price = base_price * (
                    1 + seasonal_effect + noise
                )

                modal_price = max(500, modal_price)

                min_price = modal_price * random.uniform(0.80, 0.92)
                max_price = modal_price * random.uniform(1.08, 1.25)

                # Weather variables
                temperature = random.uniform(18, 42)
                rainfall = max(0, np.random.normal(2, 6))
                humidity = random.uniform(25, 90)

                records.append({
                    "date": date,
                    "state": location["state"],
                    "district": location["district"],
                    "mandi": location["mandi"],

                    "commodity": crop["crop"],
                    "crop_category": crop["category"],
                    "is_perishable": crop["perishable"],

                    "min_price": round(min_price, 2),
                    "max_price": round(max_price, 2),
                    "modal_price": round(modal_price, 2),

                    "temperature": round(temperature, 2),
                    "rainfall": round(rainfall, 2),
                    "humidity": round(humidity, 2)
                })

    return pd.DataFrame(records)


print("Generating synthetic mandi dataset...")

df = generate_data()

os.makedirs("data", exist_ok=True)

output_path = "data/synthetic_mandi_data.csv"

df.to_csv(output_path, index=False)

print("\nSUCCESS!")
print("Total records:", len(df))
print("Saved to:", output_path)

print("\nDataset shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())

print("\nRecords by state:")
print(df["state"].value_counts())