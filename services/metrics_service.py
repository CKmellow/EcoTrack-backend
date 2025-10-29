# services/metrics_service.py
from bson import ObjectId
from config.database import db
from utils.calculations import (
    calculate_expected_metrics,
    calculate_component_metrics,
    calculate_deviation
)

from services.ai_analytics_service import analyze_department

async def update_department_metrics(dept_id: str):
    department = await db.departments.find_one({"_id": ObjectId(dept_id)})
    devices = await db.devices.find({"deptId": dept_id}).to_list(None)

    if not department or not devices:
        return None

    employee_count = department.get("employee_count", 0)
    intensity = department.get("expected_power_intensity", 0)

    def get_float(device, key):
        val = device.get(key)
        if val is None:
            raise ValueError(f"Device {device.get('_id')} missing required field: {key}")
        return float(val)

    # Expected
    expected = calculate_expected_metrics(employee_count, intensity)
    expected_daily = expected["daily"]
    expected_monthly = expected["monthly"]

    # Calculate components using correct field names and type casting
    overtime_consumption = sum(get_float(d, "overtime_hours") * get_float(d, "powerRating") for d in devices)
    waste_consumption = sum(get_float(d, "idle_hours") * get_float(d, "powerRating") for d in devices)
    actual_consumption = expected_daily["consumption"] + overtime_consumption + waste_consumption

    overtime_metrics = calculate_component_metrics(overtime_consumption)
    waste_metrics = calculate_component_metrics(waste_consumption)
    total_metrics = calculate_component_metrics(actual_consumption)

    deviation = calculate_deviation(total_metrics, expected_daily)

    await db.departments.update_one(
        {"_id": ObjectId(dept_id)},
        {"$set": {
            "metrics.expected_daily": expected_daily,
            "metrics.expected_monthly": expected_monthly,
            "metrics.overtime_daily": overtime_metrics,
            "metrics.waste_daily": waste_metrics,
            "metrics.deviation": deviation,
            "metrics.totals.daily": total_metrics
        }}
    )

    # Fetch updated department for AI analysis
    updated_dept = await db.departments.find_one({"_id": ObjectId(dept_id)})
    ai_analysis = await analyze_department(updated_dept)

    return {
        "message": "Department metrics updated successfully",
        "ai_analysis": ai_analysis,
        "department": updated_dept
    }
