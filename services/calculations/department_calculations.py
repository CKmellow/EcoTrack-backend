# services/calculations/department_calculations.py
from typing import List, Dict

def calculate_department_usage(devices: List[Dict], work_hours: int, working_days: int) -> Dict:
    """
    Calculate department totals:
    - expected (daily + monthly)
    - overtime (daily + monthly)
    - waste (daily + monthly)
    - deviation (monthly)
    Each device dict should include:
      expected_daily: {consumption, cost, emissions}
      overtime: {consumption, cost, emissions}
      waste: {consumption, cost, emissions}
    """

    def sum_metric(devices, key, metric):
        return sum(d.get(key, {}).get(metric, 0) for d in devices)

    # Expected
    expected_daily = {
        "consumption": sum_metric(devices, "expected_daily", "consumption"),
        "cost": sum_metric(devices, "expected_daily", "cost"),
        "emissions": sum_metric(devices, "expected_daily", "emissions"),
    }
    expected_monthly = {k: v * working_days for k, v in expected_daily.items()}

    # Overtime
    overtime_daily = {
        "consumption": sum_metric(devices, "overtime", "consumption"),
        "cost": sum_metric(devices, "overtime", "cost"),
        "emissions": sum_metric(devices, "overtime", "emissions"),
    }
    overtime_monthly = {k: v * working_days for k, v in overtime_daily.items()}

    # Waste
    waste_daily = {
        "consumption": sum_metric(devices, "waste", "consumption"),
        "cost": sum_metric(devices, "waste", "cost"),
        "emissions": sum_metric(devices, "waste", "emissions"),
    }
    waste_monthly = {k: v * working_days for k, v in waste_daily.items()}

    # Deviation (Actual - Expected)
    deviation = {
        k: (expected_monthly[k] + overtime_monthly[k] + waste_monthly[k]) - expected_monthly[k]
        for k in expected_monthly
    }

    return {
        "expected_daily": expected_daily,
        "expected_monthly": expected_monthly,
        "overtime_daily": overtime_daily,
        "overtime_monthly": overtime_monthly,
        "waste_daily": waste_daily,
        "waste_monthly": waste_monthly,
        "deviation": deviation,
    }
