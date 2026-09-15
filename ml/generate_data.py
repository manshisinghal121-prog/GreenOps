import pandas as pd
import numpy as np
from pathlib import Path

np.random.seed(42)

rows = []

workload_types = [
    "database",
    "machine_learning",
    "batch",
    "web",
    "analytics"
]

for i in range(1000):

    workload_type = np.random.choice(workload_types)

    cpu_usage = np.random.randint(10, 96)

    ram_usage = np.random.randint(10, 91)

    runtime_hours = np.random.randint(1, 25)

    hour = np.random.randint(0, 24)

    day_of_week = np.random.randint(0, 7)

    # Simulate future CPU usage
    future_cpu = cpu_usage + np.random.normal(0, 8)

    # Keep CPU between 5 and 100
    future_cpu = np.clip(future_cpu, 5, 100)

    rows.append({
        "cpu_usage": cpu_usage,
        "ram_usage": ram_usage,
        "runtime_hours": runtime_hours,
        "hour": hour,
        "day_of_week": day_of_week,
        "workload_type": workload_type,
        "future_cpu": future_cpu
    })


# Convert data into a DataFrame
data = pd.DataFrame(rows)


# Find the main GreenOps folder
BASE_DIR = Path(__file__).resolve().parent.parent


# Create the data folder if it doesn't exist
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)


# Create the output file path
DATA_FILE = DATA_DIR / "historical_workloads.csv"


# Save the dataset
data.to_csv(DATA_FILE, index=False)


print("======================================")
print("      GREENOPS DATA GENERATOR")
print("======================================")

print("\nHistorical dataset created successfully.")

print("Number of records:", len(data))

print("\nSaved to:")
print(DATA_FILE)

print("\nFirst 5 records:")
print(data.head())