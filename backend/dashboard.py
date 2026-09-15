import pandas as pd
from pathlib import Path

from .optimizer import calculate_optimization
from .carbon_calculator import calculate_energy, calculate_carbon
from .instance_specs import INSTANCE_SPECS


# ==========================================
# PROJECT PATH
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = BASE_DIR / "data" / "workloads.csv"


# ==========================================
# PROTOTYPE SETTINGS
# ==========================================

CARBON_INTENSITY = 0.7


# ==========================================
# CREATE DASHBOARD DATA
# ==========================================

def get_dashboard_data():

    data = pd.read_csv(DATA_FILE)

    total_cost = 0
    total_carbon = 0

    potential_savings = 0
    potential_carbon_reduction = 0

    optimization_opportunities = 0

    workload_results = []


    # ======================================
    # ANALYZE EACH WORKLOAD
    # ======================================

    for _, row in data.iterrows():

        instance = row["instance_type"]

        specs = INSTANCE_SPECS[instance]


        # ------------------------------
        # Current cost
        # ------------------------------

        current_cost = (
            specs["price_per_hour"]
            * row["runtime_hours"]
        )


        # ------------------------------
        # Current energy
        # ------------------------------

        energy = calculate_energy(
            row["cpu_usage"],
            row["runtime_hours"],
            specs["power_watts"]
        )


        # ------------------------------
        # Current carbon
        # ------------------------------

        carbon = calculate_carbon(
            energy,
            CARBON_INTENSITY
        )


        # ------------------------------
        # Optimization
        # ------------------------------

        optimization = calculate_optimization(

            cpu_usage=row["cpu_usage"],

            ram_usage=row["ram_usage"],

            runtime_hours=row["runtime_hours"],

            current_instance=instance
        )


        cost_saving = optimization["cost_saving"]

        carbon_saving = optimization["carbon_saving"]


        # ------------------------------
        # Add totals
        # ------------------------------

        total_cost += current_cost

        total_carbon += carbon

        potential_savings += cost_saving

        potential_carbon_reduction += carbon_saving


        # ------------------------------
        # Count opportunities
        # ------------------------------

        if (
            optimization["recommended_instance"]
            != instance
        ):
            optimization_opportunities += 1


        # ------------------------------
        # Store workload result
        # ------------------------------

        workload_results.append({

            "workload":
                row["workload"],

            "instance":
                instance,

            "cpu_usage":
                row["cpu_usage"],

            "ram_usage":
                row["ram_usage"],

            "runtime_hours":
                row["runtime_hours"],

            "current_cost":
                round(current_cost, 2),

            "current_carbon":
                round(carbon, 2),

            "recommended_instance":
                optimization[
                    "recommended_instance"
                ],

            "cost_saving":
                round(cost_saving, 2),

            "carbon_saving":
                round(carbon_saving, 2)
        })


    # ======================================
    # RETURN DASHBOARD
    # ======================================

    return {

        "total_workloads":
            len(data),

        "total_cost":
            round(total_cost, 2),

        "total_carbon":
            round(total_carbon, 2),

        "potential_cost_saving":
            round(potential_savings, 2),

        "potential_carbon_reduction":
            round(
                potential_carbon_reduction,
                2
            ),

        "optimization_opportunities":
            optimization_opportunities,

        "workloads":
            workload_results
    }