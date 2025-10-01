# services/energy_service.py
from config.database import db
from services.calculations.calc_expected import calculate_expected_metrics
from services.calculations.calc_waste import calculate_waste_metrics
from services.calculations.calc_overtime import calculate_overtime_metrics
from services.calculations.calc_deviation import calculate_deviation_metrics
from services.calculations.calc_total import calculate_total_metrics

async def enrich_department_with_energy(department: dict) -> dict:
    """Attach all energy metrics to a department."""
    
    dept_id = str(department["_id"])
    devices = await db.devices.find({"department_id": dept_id}).to_list(length=None)
    
    # Run all calculation modules
    expected = calculate_expected_metrics(department, devices)
    waste = calculate_waste_metrics(department, devices)
    overtime = calculate_overtime_metrics(department, devices)
    deviation = calculate_deviation_metrics(expected, waste, overtime)
    totals = calculate_total_metrics(expected, waste, overtime)

    # Build metrics structure
    department["metrics"] = {
        "expected_daily": expected["daily"],
        "expected_monthly": expected["monthly"],
        "overtime_daily": overtime["daily"],
        "overtime_monthly": overtime["monthly"],
        "waste_daily": waste["daily"],
        "waste_monthly": waste["monthly"],
        "deviation": deviation,
        "totals": totals,
    }

    def convert_obj_ids(obj):
        if isinstance(obj, dict):
            return {k: convert_obj_ids(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_obj_ids(i) for i in obj]
        elif hasattr(obj, "__str__") and type(obj).__name__ == "ObjectId":
            return str(obj)
        else:
            return obj

    return convert_obj_ids(department)
