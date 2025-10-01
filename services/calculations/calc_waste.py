# app/calculations/calc_waste.py

def calculate_waste_metrics(department: dict, devices: list) -> dict:
    """
    Waste is energy consumed by idle devices (standby mode).
    """

    # Assume each idle device still draws 10% of its rated power
    idle_factor = 0.1
    waste_load = sum([
        d.get("power_rating", 0) * idle_factor
        for d in devices if not d.get("is_active", True)
    ])

    # Daily waste (in kWh)
    daily_consumption = waste_load / 1000.0 * 24
    monthly_consumption = daily_consumption * 30

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
