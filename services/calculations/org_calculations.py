# services/calculations/org_calculations.py
from typing import List, Dict

def calculate_org_usage(departments: List[Dict]) -> Dict:
    """
    Aggregate department metrics at org level.
    Each department dict should include the same keys as calculate_department_usage.
    """

    def sum_metric(departments, key, metric):
        return sum(d.get(key, {}).get(metric, 0) for d in departments)

    keys = [
        "expected_daily", "expected_monthly",
        "overtime_daily", "overtime_monthly",
        "waste_daily", "waste_monthly", "deviation"
    ]

    return {
        f"org_{key}": {
            "consumption": sum_metric(departments, key, "consumption"),
            "cost": sum_metric(departments, key, "cost"),
            "emissions": sum_metric(departments, key, "emissions"),
        }
        for key in keys
    }
