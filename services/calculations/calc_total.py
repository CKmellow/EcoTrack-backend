# app/calculations/calc_total.py

def calculate_total_metrics(expected: dict, waste: dict, overtime: dict) -> dict:
    """
    Totals = aggregate of expected + overtime + waste.
    """

    daily_consumption = (
        expected["daily"]["consumption"]
        + waste["daily"]["consumption"]
        + overtime["daily"]["consumption"]
    )

    monthly_consumption = (
        expected["monthly"]["consumption"]
        + waste["monthly"]["consumption"]
        + overtime["monthly"]["consumption"]
    )

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
