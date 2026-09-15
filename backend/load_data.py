import pandas as pd
from pathlib import Path
from optimizer import calculate_optimization

# Find the GreenOps project folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Location of workload dataset
DATA_FILE = BASE_DIR / "data" / "workloads.csv"

# Load workload data
data = pd.read_csv(DATA_FILE)

print("=================================")
print("        GREENOPS ANALYZER")
print("=================================")

print("\nTotal workloads:", len(data))

print("\nAverage CPU usage:",
      round(data["cpu_usage"].mean(), 2), "%")

print("Average RAM usage:",
      round(data["ram_usage"].mean(), 2), "%")

print("\nWorkload utilization:")
print(data[["workload", "cpu_usage", "ram_usage"]])

print("\nPotentially underutilized workloads:")

underutilized = data[
    (data["cpu_usage"] < 30) &
    (data["ram_usage"] < 30)
]

print(
    underutilized[
        ["workload", "cpu_usage", "ram_usage", "instance_type"]
    ]
)
print("\n========================================")
print("       OPTIMIZATION RECOMMENDATIONS")
print("========================================")

for _, row in data.iterrows():

    result = calculate_optimization(
        cpu_usage=row["cpu_usage"],
        ram_usage=row["ram_usage"],
        runtime_hours=row["runtime_hours"],
        current_instance=row["instance_type"]
    )

    print("\nWorkload:", row["workload"])

    print(
        "Current:",
        result["current_instance"]
    )

    print(
        "Recommended:",
        result["recommended_instance"]
    )

    print(
        "Cost Saving: ₹",
        round(result["cost_saving"], 2)
    )

    print(
        "Carbon Saving:",
        round(result["carbon_saving"], 2),
        "kg CO2"
    )