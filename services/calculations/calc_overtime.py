# app/calculations/calc_overtime.py

def calculate_overtime_metrics(department: dict, devices: list) -> dict:
    """
    Overtime = consumption when usage_hours exceed normal working hours.
    """

    working_hours = department.get("working_hours", 8)
    overtime_load = sum([
        d.get("power_rating", 0) * max(0, d.get("usage_hours", 0) - working_hours)
        for d in devices
    ])

    daily_consumption = overtime_load / 1000.0
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
