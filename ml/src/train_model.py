import os
import pandas as pd
import joblib

from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from xgboost import XGBRegressor


# =================================================
# FILE PATHS
# =================================================

INPUT_FILE = "data/processed_mandi_data.csv"

MODEL_FILE = "models/mandi_price_model.pkl"
ENCODERS_FILE = "models/label_encoders.pkl"
FEATURES_FILE = "models/model_features.pkl"


# =================================================
# LOAD DATA
# =================================================

print("Loading processed dataset...")

df = pd.read_csv(INPUT_FILE)

df["date"] = pd.to_datetime(df["date"])

print("Dataset shape:", df.shape)
print(
    "Date range:",
    df["date"].min().date(),
    "to",
    df["date"].max().date()
)


# =================================================
# SORT DATA PROPERLY BEFORE FORECASTING
# =================================================

group_cols = [
    "state",
    "district",
    "mandi",
    "commodity"
]

df = df.sort_values(
    group_cols + ["date"]
).reset_index(drop=True)


# =================================================
# CREATE NEXT-DAY PRICE TARGET
# =================================================

df["target_next_day_price"] = (
    df.groupby(group_cols)["modal_price"]
    .shift(-1)
)


# IMPORTANT:
# Remove rows where a future price does not exist

df = df.dropna(
    subset=["target_next_day_price"]
).reset_index(drop=True)


print("\nDataset after creating target:", df.shape)


# =================================================
# CHRONOLOGICAL TRAIN / TEST SPLIT
# =================================================

# We must split based on TIME, not randomly.

df = df.sort_values("date").reset_index(drop=True)

split_index = int(len(df) * 0.80)

train_df = df.iloc[:split_index].copy()
test_df = df.iloc[split_index:].copy()


print("\n========== CHRONOLOGICAL SPLIT ==========")

print("Training records:", len(train_df))
print(
    "Training date range:",
    train_df["date"].min().date(),
    "to",
    train_df["date"].max().date()
)

print("\nTesting records:", len(test_df))
print(
    "Testing date range:",
    test_df["date"].min().date(),
    "to",
    test_df["date"].max().date()
)

print("==========================================")


# =================================================
# ENCODE CATEGORICAL DATA
# =================================================

categorical_columns = [
    "state",
    "district",
    "mandi",
    "commodity",
    "crop_category"
]

label_encoders = {}

print("\nEncoding categorical features...")

for column in categorical_columns:

    encoder = LabelEncoder()

    # Fit ONLY on training data
    train_df[column] = encoder.fit_transform(
        train_df[column].astype(str)
    )

    # Handle categories not seen during training
    mapping = {
        value: index
        for index, value in enumerate(
            encoder.classes_
        )
    }

    test_df[column] = (
        test_df[column]
        .astype(str)
        .map(mapping)
        .fillna(-1)
        .astype(int)
    )

    label_encoders[column] = encoder

    print(f"Encoded: {column}")


# =================================================
# FEATURE SELECTION
# =================================================

# IMPORTANT:
# We deliberately do NOT use:
#
# - target_next_day_price
# - modal_price
# - min_price
# - max_price
#
# This makes the forecast more honest.
# The model predicts the next-day price using
# historical trends and available information.

feature_columns = [

    # Location
    "state",
    "district",
    "mandi",

    # Crop information
    "commodity",
    "crop_category",
    "is_perishable",

    # Calendar
    "day_of_week",
    "month",
    "day_of_year",

    # Historical price features
    "price_lag_1",
    "price_lag_3",
    "price_lag_7",
    "price_ma_7",
    "price_ma_14",
    "price_volatility_7",

    # Price movement
    "price_change_1d",
    "price_change_7d",

    # Weather
    "temperature",
    "rainfall",
    "humidity",
    "heavy_rain_flag",
    "weather_severity"
]


target_column = "target_next_day_price"


# =================================================
# PREPARE TRAINING AND TEST DATA
# =================================================

X_train = train_df[feature_columns].copy()
X_test = test_df[feature_columns].copy()

y_train = train_df[target_column].copy()
y_test = test_df[target_column].copy()


# Safety check

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))

print("\nNumber of model features:", len(feature_columns))


# =================================================
# TRAIN XGBOOST MODEL
# =================================================

print("\nTraining XGBoost model...")

model = XGBRegressor(
    n_estimators=300,
    max_depth=8,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    objective="reg:squarederror",
    random_state=42,
    n_jobs=-1
)


model.fit(
    X_train,
    y_train
)


# =================================================
# PREDICTION ON UNSEEN DATA
# =================================================

print("\nGenerating predictions on unseen data...")

predictions = model.predict(X_test)


# =================================================
# MODEL EVALUATION
# =================================================

mae = mean_absolute_error(
    y_test,
    predictions
)

mse = mean_squared_error(
    y_test,
    predictions
)

rmse = mse ** 0.5

r2 = r2_score(
    y_test,
    predictions
)


print("\n========== TRUE UNSEEN DATA PERFORMANCE ==========")

print(f"MAE  : ₹{mae:.2f}")
print(f"RMSE : ₹{rmse:.2f}")
print(f"R²   : {r2:.4f}")

print("===================================================")


# =================================================
# SAVE MODEL FILES
# =================================================

os.makedirs(
    "models",
    exist_ok=True
)

joblib.dump(
    model,
    MODEL_FILE
)

joblib.dump(
    label_encoders,
    ENCODERS_FILE
)

joblib.dump(
    feature_columns,
    FEATURES_FILE
)


print("\nSUCCESS!")

print("Model saved to:", MODEL_FILE)
print("Encoders saved to:", ENCODERS_FILE)
print("Feature list saved to:", FEATURES_FILE)


# =================================================
# SAMPLE PREDICTIONS
# =================================================

results = pd.DataFrame({

    "Actual Next-Day Price":
        y_test.head(10).values,

    "Predicted Next-Day Price":
        predictions[:10]

})


print("\nSample predictions:")

print(
    results.round(2)
)


print("\n========== TRAINING COMPLETE ==========")