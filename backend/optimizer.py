from .instance_specs import INSTANCE_SPECS
from .carbon_calculator import (
    calculate_energy,
    calculate_carbon,
    calculate_carbon_details
)


def calculate_optimization(
    current_instance,
    ram_usage,
    runtime_hours,
    predicted_cpu=None,
    cpu_usage=None
):
    """
    Find the smallest suitable instance using predicted CPU
    and RAM utilization.

    The instance capacities are simplified MVP values.
    """

    if predicted_cpu is None:
        predicted_cpu = cpu_usage

    if predicted_cpu is None:
        predicted_cpu = 0

    current = INSTANCE_SPECS[current_instance]

    # Estimate the actual resource requirement from
    # the current instance and its utilization.
    required_vcpu = (
        current["vcpus"] *
        (predicted_cpu / 100)
    )

    required_ram = (
        current["ram_gb"] *
        (ram_usage / 100)
    )

    suitable_instances = []

    for instance_name, specs in INSTANCE_SPECS.items():

        if (
            specs["vcpus"] >= required_vcpu
            and
            specs["ram_gb"] >= required_ram
        ):
            suitable_instances.append(
                (instance_name, specs)
            )

    suitable_instances.sort(
        key=lambda item: item[1]["price_per_hour"]
    )

    if suitable_instances:
        recommended_instance = suitable_instances[0][0]
    else:
        recommended_instance = current_instance

    recommended = INSTANCE_SPECS[
        recommended_instance
    ]

    # -----------------------------
    # Cost
    # -----------------------------

    current_cost = (
        current["price_per_hour"]
        * runtime_hours
    )

    optimized_cost = (
        recommended["price_per_hour"]
        * runtime_hours
    )

    cost_saving = max(
        current_cost - optimized_cost,
        0
    )

    # -----------------------------
    # Energy and carbon
    # -----------------------------

    current_energy = calculate_energy(
        cpu_usage=predicted_cpu,
        runtime_hours=runtime_hours,
        power_watts=current["power_watts"]
    )

    optimized_energy = calculate_energy(
        cpu_usage=predicted_cpu,
        runtime_hours=runtime_hours,
        power_watts=recommended["power_watts"]
    )

    current_carbon = calculate_carbon(
        current_energy
    )

    optimized_carbon = calculate_carbon(
        optimized_energy
    )

    carbon_saving = max(
        current_carbon - optimized_carbon,
        0
    )

    # Detailed calculations for the frontend.
    current_carbon_details = calculate_carbon_details(
        cpu_usage=predicted_cpu,
        runtime_hours=runtime_hours,
        power_watts=current["power_watts"]
    )

    optimized_carbon_details = calculate_carbon_details(
        cpu_usage=predicted_cpu,
        runtime_hours=runtime_hours,
        power_watts=recommended["power_watts"]
    )

    # -----------------------------
    # Explanation
    # -----------------------------

    if recommended_instance != current_instance:

        reason = (
            f"Predicted CPU usage is "
            f"{predicted_cpu:.1f}% and RAM usage is "
            f"{ram_usage:.1f}%. "
            f"The workload can be handled by "
            f"{recommended_instance}, which has sufficient "
            f"vCPU and RAM capacity while costing less "
            f"than the current instance."
        )

    else:

        reason = (
            "The current instance is already the smallest "
            "suitable option based on the predicted CPU "
            "and RAM requirements."
        )

    return {
        "current_instance": current_instance,
        "recommended_instance": recommended_instance,

        "current_cost": round(current_cost, 2),
        "optimized_cost": round(optimized_cost, 2),
        "cost_saving": round(cost_saving, 2),

        "current_carbon": round(current_carbon, 2),
        "optimized_carbon": round(optimized_carbon, 2),
        "carbon_saving": round(carbon_saving, 2),

        "current_energy_kwh": round(
            current_energy,
            4
        ),

        "optimized_energy_kwh": round(
            optimized_energy,
            4
        ),

        "carbon_intensity": (
            current_carbon_details["carbon_intensity"]
        ),

        "current_carbon_details":
            current_carbon_details,

        "optimized_carbon_details":
            optimized_carbon_details,

        "reason": reason
    }
