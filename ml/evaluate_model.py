import pandas as pd
import joblib
import matplotlib.pyplot as plt

from pathlib import Path
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = BASE_DIR / "data" / "historical_workloads.csv"
MODEL_FILE = BASE_DIR / "ml" / "greenops_cpu_model.pkl"

data = pd.read_csv(DATA_FILE)
pipeline = joblib.load(MODEL_FILE)

print("Dataset loaded successfully.")
print("Number of records:", len(data))
print("Model loaded successfully.")

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

y = data["future_cpu"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

predictions = pipeline.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
rmse = mean_squared_error(y_test, predictions) ** 0.5
r2 = r2_score(y_test, predictions)

print("\n======================================")
print("       GREENOPS MODEL EVALUATION")
print("======================================")
print("\nModel: Random Forest Regressor")
print("\nMAE:", round(mae, 2))
print("\nRMSE:", round(rmse, 2))
print("\nR² Score:", round(r2, 2))

plt.figure(figsize=(8, 6))

plt.scatter(
    y_test,
    predictions,
    alpha=0.7
)

minimum = min(y_test.min(), predictions.min())
maximum = max(y_test.max(), predictions.max())

plt.plot(
    [minimum, maximum],
    [minimum, maximum],
    linestyle="--"
)

plt.xlabel("Actual Future CPU (%)")
plt.ylabel("Predicted Future CPU (%)")
plt.title("GreenOps: Actual vs Predicted CPU")
plt.tight_layout()

actual_predicted_file = BASE_DIR / "ml" / "actual_vs_predicted.png"
plt.savefig(actual_predicted_file, dpi=150)
plt.close()

print("\nActual vs Predicted graph saved:")
print(actual_predicted_file)

forest_model = pipeline.named_steps["model"]
preprocessor = pipeline.named_steps["preprocessor"]

feature_names = preprocessor.get_feature_names_out()
importance_values = forest_model.feature_importances_

importance_df = pd.DataFrame({
    "feature": feature_names,
    "importance": importance_values
}).sort_values("importance", ascending=False)

print("\n======================================")
print("         FEATURE IMPORTANCE")
print("======================================")

for _, row in importance_df.iterrows():
    print(
        f"{row['feature']}: "
        f"{row['importance']:.4f}"
    )

plt.figure(figsize=(9, 6))

plot_data = importance_df.head(10).sort_values("importance")

plt.barh(
    plot_data["feature"],
    plot_data["importance"]
)

plt.xlabel("Importance")
plt.ylabel("Feature")
plt.title("GreenOps: Feature Importance")
plt.tight_layout()

feature_importance_file = BASE_DIR / "ml" / "feature_importance.png"
plt.savefig(feature_importance_file, dpi=150)
plt.close()

print("\nFeature importance graph saved:")
print(feature_importance_file)

print("\n======================================")
print("       EVALUATION COMPLETED")
print("======================================")
