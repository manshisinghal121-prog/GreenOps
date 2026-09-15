# GreenOps Carbon Calculator
#
# The values produced here are estimates for the MVP.
# They are based on estimated power consumption,
# CPU utilization, runtime and a configurable
# carbon-intensity value.


DEFAULT_CARBON_INTENSITY = 0.7


def calculate_energy(
    cpu_usage,
    runtime_hours,
    power_watts
):
    """
    Estimate energy consumption in kWh.

    Formula:

        Power (W)
        × CPU utilization
        × Runtime (hours)
        ÷ 1000

    The result is an estimated energy consumption.
    """

    utilization = cpu_usage / 100

    energy_kwh = (
        power_watts
        * utilization
        * runtime_hours
        / 1000
    )

    return energy_kwh


def calculate_carbon(
    energy_kwh,
    carbon_intensity=DEFAULT_CARBON_INTENSITY
):
    """
    Estimate carbon emissions in kg CO₂.

    Formula:

        Energy (kWh)
        × Carbon intensity (kg CO₂/kWh)
    """

    carbon_kg = (
        energy_kwh
        * carbon_intensity
    )

    return carbon_kg


def calculate_carbon_details(
    cpu_usage,
    runtime_hours,
    power_watts,
    carbon_intensity=DEFAULT_CARBON_INTENSITY
):
    """
    Return the complete calculation so the frontend
    can explain how the carbon estimate was obtained.
    """

    energy_kwh = calculate_energy(
        cpu_usage=cpu_usage,
        runtime_hours=runtime_hours,
        power_watts=power_watts
    )

    carbon_kg = calculate_carbon(
        energy_kwh=energy_kwh,
        carbon_intensity=carbon_intensity
    )

    return {
        "power_watts": power_watts,
        "cpu_usage": cpu_usage,
        "runtime_hours": runtime_hours,
        "energy_kwh": round(energy_kwh, 4),
        "carbon_intensity": carbon_intensity,
        "carbon_kg": round(carbon_kg, 4)
    }