# app/calculations/calc_deviation.py

def calculate_deviation_metrics(expected: dict, waste: dict, overtime: dict) -> dict:
    """
    Deviation = (waste + overtime) compared to expected.
    """

    daily_expected = expected["daily"]["consumption"]
    daily_actual = (
        expected["daily"]["consumption"]
        + waste["daily"]["consumption"]
        + overtime["daily"]["consumption"]
    )

    monthly_expected = expected["monthly"]["consumption"]
    monthly_actual = (
        expected["monthly"]["consumption"]
        + waste["monthly"]["consumption"]
        + overtime["monthly"]["consumption"]
    )

    return {
        "consumption": monthly_actual - monthly_expected,
        "cost": (monthly_actual - monthly_expected) * 0.15,
        "emissions": (monthly_actual - monthly_expected) * 0.5,
    }
