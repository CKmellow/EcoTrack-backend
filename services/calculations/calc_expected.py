# app/calculations/calc_expected.py

def calculate_expected_metrics(department: dict, devices: list) -> dict:
    """
    Expected metrics based on employee_count, expected_power_intensity,
    and device usage profiles.
    """

    employee_count = department.get("employee_count", 0)
    intensity = department.get("expected_power_intensity", 1.0)

    # Sum of base device wattage × usage_hours
    device_load = sum([
        d.get("power_rating", 0) * d.get("usage_hours", 0)
        for d in devices
    ])

    # Expected daily consumption (kWh)
    daily_consumption = (employee_count * intensity) + (device_load / 1000.0)
    monthly_consumption = daily_consumption * 30

    # Assume cost factor ($0.15/kWh) and emissions factor (0.5 kg CO2/kWh)
    cost_factor = 0.15
    emissions_factor = 0.5

    return {
        "daily": {
            "consumption": daily_consumption,
            "cost": daily_consumption * cost_factor,
            "emissions": daily_consumption * emissions_factor,
        },
        "monthly": {
            "consumption": monthly_consumption,
            "cost": monthly_consumption * cost_factor,
            "emissions": monthly_consumption * emissions_factor,
        },
    }
