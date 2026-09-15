import joblib
import pandas as pd

from pathlib import Path

from .optimizer import calculate_optimization


BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_FILE = (
    BASE_DIR
    / "ml"
    / "greenops_cpu_model.pkl"
)

model = joblib.load(MODEL_FILE)


def analyze_workload(
    cpu_usage,
    ram_usage,
    runtime_hours,
    hour,
    day_of_week,
    workload_type,
    current_instance
):

    workload = pd.DataFrame([
        {
            "cpu_usage": cpu_usage,
            "ram_usage": ram_usage,
            "runtime_hours": runtime_hours,
            "hour": hour,
            "day_of_week": day_of_week,
            "workload_type": workload_type
        }
    ])

    prediction = model.predict(
        workload
    )

    predicted_cpu = float(
        prediction[0]
    )

    optimization = calculate_optimization(
        predicted_cpu=predicted_cpu,
        ram_usage=ram_usage,
        runtime_hours=runtime_hours,
        current_instance=current_instance
    )

    return {
        "current_cpu":
            cpu_usage,

        "predicted_cpu":
            predicted_cpu,

        "ram_usage":
            ram_usage,

        "current_instance":
            current_instance,

        "recommended_instance":
            optimization["recommended_instance"],

        "current_cost":
            optimization["current_cost"],

        "optimized_cost":
            optimization["optimized_cost"],

        "cost_saving":
            optimization["cost_saving"],

        "current_carbon":
            optimization["current_carbon"],

        "optimized_carbon":
            optimization["optimized_carbon"],

        "carbon_saving":
            optimization["carbon_saving"],

        "current_energy_kwh":
            optimization["current_energy_kwh"],

        "optimized_energy_kwh":
            optimization["optimized_energy_kwh"],

        "carbon_intensity":
            optimization["carbon_intensity"],

        "current_carbon_details":
            optimization["current_carbon_details"],

        "optimized_carbon_details":
            optimization["optimized_carbon_details"],

        "reason":
            optimization["reason"]
    }
