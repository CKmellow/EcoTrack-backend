# services/activity_service.py
from config.database import db
from services.calculations.department_calculations import calculate_department_usage
from bson import ObjectId

activity_logs = db["activity_logs"]
devices = db["devices"]
departments = db["departments"]


async def log_and_recalc(user_id: str, dept_id: str, device_id: str, action: str, before: dict, after: dict):
    # 1. Save activity log
    log = {
        "user_id": user_id,
        "deptId": dept_id,
        "device_id": device_id,
        "action": action,
        "before": before,
        "after": after,
    }
    await activity_logs.insert_one(log)

    # 2. Recalculate department totals
    dept_devices = await devices.find({"deptId": dept_id}).to_list(None)
    dept_usage = calculate_department_usage(dept_devices, work_hours=8, working_days=22)

    await departments.update_one(
        {"_id": ObjectId(dept_id)} if ObjectId.is_valid(dept_id) else {"_id": dept_id},
        {"$set": {"metrics": dept_usage}}
    )


# -------------------------------
# 📜 Get all logs
# -------------------------------
async def get_logs(limit: int = 50, filter_query: dict = None):
    """Fetch latest activity logs for status changes only, with optional extra filter_query"""
    query = {"action": "status_change"}
    if filter_query:
        # Convert id fields to ObjectId if valid
        for key in ["user_id", "device_id", "deptId"]:
            if key in filter_query and ObjectId.is_valid(filter_query[key]):
                filter_query[key] = ObjectId(filter_query[key])
        query.update(filter_query)
    logs_cursor = activity_logs.find(query).sort("_id", -1).limit(limit)
    logs = await logs_cursor.to_list(length=limit)

    def convert_obj_ids(obj):
        if isinstance(obj, dict):
            return {k: convert_obj_ids(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_obj_ids(i) for i in obj]
        elif isinstance(obj, ObjectId):
            return str(obj)
        else:
            return obj

    return [convert_obj_ids(log) for log in logs]
