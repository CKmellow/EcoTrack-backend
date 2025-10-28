# utils/calculations.py
COST_PER_KWH = 0.15
EMISSION_FACTOR = 0.5

def calculate_expected_metrics(employee_count, power_intensity, hours=10, days=30):
    daily = employee_count * power_intensity * hours
    monthly = daily * days
    return {
        "daily": {
            "consumption": daily,
            "cost": daily * COST_PER_KWH,
            "emissions": daily * EMISSION_FACTOR
        },
        "monthly": {
            "consumption": monthly,
            "cost": monthly * COST_PER_KWH,
            "emissions": monthly * EMISSION_FACTOR
        }
    }

def calculate_component_metrics(consumption):
    return {
        "consumption": consumption,
        "cost": consumption * COST_PER_KWH,
        "emissions": consumption * EMISSION_FACTOR
    }

def calculate_deviation(actual, expected):
    return {
        "consumption": actual["consumption"] - expected["consumption"],
        "cost": actual["cost"] - expected["cost"],
        "emissions": actual["emissions"] - expected["emissions"]
    }
