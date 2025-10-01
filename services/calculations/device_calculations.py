# services/calculations/device_calculations.py
def calculate_device_consumption(power_rating_watts: float, hours_used: float) -> float:
    """Return kWh consumption for a device."""
    return (power_rating_watts / 1000) * hours_used


def calculate_device_cost(consumption_kwh: float, unit_cost: float) -> float:
    """Return energy cost for a device."""
    return consumption_kwh * unit_cost


def calculate_device_emissions(consumption_kwh: float, emission_factor: float = 0.233) -> float:
    """Return CO2 emissions in kg for a device."""
    return consumption_kwh * emission_factor


def calculate_expected_daily(device: dict, work_hours: int, unit_cost: float, emission_factor: float) -> dict:
    """Expected daily usage (normal work hours)."""
    consumption = calculate_device_consumption(device["power_rating_watts"], work_hours)
    return {
        "consumption": consumption,
        "cost": calculate_device_cost(consumption, unit_cost),
        "emissions": calculate_device_emissions(consumption, emission_factor),
    }


def calculate_off_hours(device: dict, start: float, stop: float, employee_present: bool,
                        unit_cost: float, emission_factor: float) -> dict:
    """
    Calculate off-hours usage (overtime or waste).
    Returns dict with type = 'overtime' or 'waste'.
    """
    hours_used = stop - start
    consumption = calculate_device_consumption(device["power_rating_watts"], hours_used)
    return {
        "consumption": consumption,
        "cost": calculate_device_cost(consumption, unit_cost),
        "emissions": calculate_device_emissions(consumption, emission_factor),
        "type": "overtime" if employee_present else "waste"
    }
