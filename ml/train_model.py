import pandas as pd
import joblib

from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


# ==========================================
# 1. FIND DATASET
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = (
    BASE_DIR
    / "data"
    / "historical_workloads.csv"
)


# ==========================================
# 2. LOAD DATA
# ==========================================

data = pd.read_csv(DATA_FILE)

print("Dataset loaded successfully.")
print("Number of records:", len(data))


# ==========================================
# 3. DEFINE FEATURES
# ==========================================

X = data[
    [
        "cpu_usage",
        "ram_usage",
        "runtime_hours",
        "hour",
        "day_of_week",
        "workload_type"
    ]
]


# ==========================================
# 4. DEFINE TARGET
# ==========================================

y = data["future_cpu"]


# ==========================================
# 5. COLUMNS
# ==========================================

categorical_features = [
    "workload_type"
]

numerical_features = [
    "cpu_usage",
    "ram_usage",
    "runtime_hours",
    "hour",
    "day_of_week"
]


# ==========================================
# 6. PREPROCESSING
# ==========================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(
                handle_unknown="ignore"
            ),
            categorical_features
        ),
        (
            "numerical",
            "passthrough",
            numerical_features
        )
    ]
)


# ==========================================
# 7. RANDOM FOREST
# ==========================================

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)


# ==========================================
# 8. CREATE PIPELINE
# ==========================================

pipeline = Pipeline(
    steps=[
        (
            "preprocessor",
            preprocessor
        ),
        (
            "model",
            model
        )
    ]
)


# ==========================================
# 9. SPLIT DATA
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


print("\nTraining records:", len(X_train))
print("Testing records:", len(X_test))


# ==========================================
# 10. TRAIN MODEL
# ==========================================

print("\nTraining Random Forest...")

pipeline.fit(
    X_train,
    y_train
)

print("Training completed.")


# ==========================================
# 11. PREDICTION
# ==========================================

predictions = pipeline.predict(X_test)


# ==========================================
# 12. EVALUATION
# ==========================================

mae = mean_absolute_error(
    y_test,
    predictions
)

rmse = mean_squared_error(
    y_test,
    predictions
) ** 0.5

r2 = r2_score(
    y_test,
    predictions
)


print("\n======================================")
print("        GREENOPS ML RESULTS")
print("======================================")

print("\nModel: Random Forest Regressor")

print("\nMAE:")
print(round(mae, 2))

print("\nRMSE:")
print(round(rmse, 2))

print("\nR² Score:")
print(round(r2, 2))


# ==========================================
# 13. SAVE MODEL
# ==========================================

MODEL_FILE = (
    BASE_DIR
    / "ml"
    / "greenops_cpu_model.pkl"
)

joblib.dump(
    pipeline,
    MODEL_FILE
)

print("\n======================================")
print("Model saved successfully!")
print("======================================")

print("\nModel location:")
print(MODEL_FILE)