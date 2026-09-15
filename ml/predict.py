import joblib
import pandas as pd
from pathlib import Path


# ==========================================
# 1. FIND GREENOPS FOLDER
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ==========================================
# 2. LOAD TRAINED MODEL
# ==========================================

MODEL_FILE = (
    BASE_DIR
    / "ml"
    / "greenops_cpu_model.pkl"
)

model = joblib.load(MODEL_FILE)


# ==========================================
# 3. CREATE A NEW WORKLOAD
# ==========================================

workload = pd.DataFrame([
    {
        "cpu_usage": 18,
        "ram_usage": 25,
        "runtime_hours": 24,
        "hour": 14,
        "day_of_week": 2,
        "workload_type": "database"
    }
])


# ==========================================
# 4. MAKE PREDICTION
# ==========================================

prediction = model.predict(workload)

predicted_cpu = prediction[0]


# ==========================================
# 5. DISPLAY RESULT
# ==========================================

print("======================================")
print("       GREENOPS ML PREDICTION")
print("======================================")

print("\nWorkload Type:")
print(workload["workload_type"].iloc[0])

print("\nCurrent CPU Usage:")
print(workload["cpu_usage"].iloc[0], "%")

print("\nCurrent RAM Usage:")
print(workload["ram_usage"].iloc[0], "%")

print("\nPredicted Future CPU:")
print(round(predicted_cpu, 2), "%")