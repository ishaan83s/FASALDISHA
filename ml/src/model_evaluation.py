import pandas as pd
import numpy as np
import pickle
import os
import matplotlib.pyplot as plt

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
from sklearn.preprocessing import LabelEncoder


# ==========================================
# PATHS
# ==========================================

DATA_PATH = "data/processed_mandi_data.csv"
MODEL_PATH = "models/mandi_price_model.pkl"
FEATURES_PATH = "models/model_features.pkl"
OUTPUT_DIR = "outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ==========================================
# LOAD MODEL
# ==========================================

print("Loading trained XGBoost model...")

with open(MODEL_PATH, "rb") as file:
    model = pickle.load(file)


# ==========================================
# LOAD MODEL FEATURES
# ==========================================

print("Loading model features...")

with open(FEATURES_PATH, "rb") as file:
    model_features = pickle.load(file)

print("Model features:")
print(model_features)


# ==========================================
# LOAD DATA
# ==========================================

print("\nLoading processed dataset...")

df = pd.read_csv(DATA_PATH)

df["date"] = pd.to_datetime(df["date"])

print(f"Dataset shape: {df.shape}")
print(
    f"Date range: "
    f"{df['date'].min().date()} "
    f"to "
    f"{df['date'].max().date()}"
)


# ==========================================
# ENCODE CATEGORICAL COLUMNS
# ==========================================

categorical_columns = [
    "state",
    "district",
    "mandi",
    "commodity",
    "crop_category",
]

print("\nEncoding categorical columns...")

for column in categorical_columns:
    if column in df.columns:
        print(f"Encoding: {column}")

        encoder = LabelEncoder()

        df[column] = encoder.fit_transform(
            df[column].astype(str)
        )

print("Categorical encoding completed.")


# ==========================================
# SORT CHRONOLOGICALLY
# ==========================================

df = df.sort_values("date").reset_index(drop=True)


# ==========================================
# CREATE CHRONOLOGICAL SPLIT
# ==========================================

split_index = int(len(df) * 0.80)

train_data = df.iloc[:split_index].copy()
test_data = df.iloc[split_index:].copy()

print("\n========== CHRONOLOGICAL SPLIT ==========")

print(f"Training records: {len(train_data)}")
print(f"Training ends: {train_data['date'].max().date()}")

print(f"\nUnseen test records: {len(test_data)}")
print(f"Testing starts: {test_data['date'].min().date()}")

print("==========================================")


# ==========================================
# PREPARE TEST FEATURES
# ==========================================

missing_features = [
    feature
    for feature in model_features
    if feature not in test_data.columns
]

if missing_features:
    raise ValueError(
        f"Missing model features: {missing_features}"
    )

X_test = test_data[model_features].copy()


# ==========================================
# SAFETY: FORCE NUMERIC FEATURES
# ==========================================

for column in X_test.columns:
    X_test[column] = pd.to_numeric(
        X_test[column],
        errors="coerce"
    )

X_test = X_test.fillna(0)

print("\nTest feature dtypes:")
print(X_test.dtypes)

invalid_columns = [
    column
    for column in X_test.columns
    if not pd.api.types.is_numeric_dtype(
        X_test[column]
    )
]

if invalid_columns:
    raise ValueError(
        f"Non-numeric features still found: {invalid_columns}"
    )


# ==========================================
# PREDICT
# ==========================================

print("\nGenerating predictions on unseen data...")

predictions = model.predict(X_test)


# ==========================================
# EVALUATE
# ==========================================

y_test = test_data["modal_price"].astype(float)

mae = mean_absolute_error(
    y_test,
    predictions,
)

rmse = np.sqrt(
    mean_squared_error(
        y_test,
        predictions,
    )
)

r2 = r2_score(
    y_test,
    predictions,
)


# ==========================================
# RESULTS
# ==========================================

print("\n========== UNSEEN DATA PERFORMANCE ==========")

print(f"MAE  : ₹{mae:.2f}")
print(f"RMSE : ₹{rmse:.2f}")
print(f"R²   : {r2:.4f}")

print("==============================================")


# ==========================================
# SAVE RESULTS
# ==========================================

results_df = pd.DataFrame({
    "date": test_data["date"].values,
    "actual_price": y_test.values,
    "predicted_price": predictions,
})

results_path = os.path.join(
    OUTPUT_DIR,
    "unseen_test_predictions.csv",
)

results_df.to_csv(
    results_path,
    index=False,
)

print(f"\nPredictions saved to: {results_path}")


# ==========================================
# ACTUAL VS PREDICTED GRAPH
# ==========================================

plot_df = results_df.tail(100).copy()

plt.figure(figsize=(12, 6))

plt.plot(
    plot_df["date"],
    plot_df["actual_price"],
    label="Actual Price",
)

plt.plot(
    plot_df["date"],
    plot_df["predicted_price"],
    label="Predicted Price",
    linestyle="--",
)

plt.title("Actual vs Predicted Price")
plt.xlabel("Date")
plt.ylabel("Price (₹)")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

graph_path = os.path.join(
    OUTPUT_DIR,
    "actual_vs_predicted.png",
)

plt.savefig(graph_path, dpi=150)
plt.close()

print(f"Graph saved to: {graph_path}")

print("\n========== EVALUATION COMPLETE ==========")