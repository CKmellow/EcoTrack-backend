# models/activity_log.py
from datetime import datetime

def build_log(user_id: str, dept_id: str, device_id: str, action: str, before: dict, after: dict):
    return {
        "user_id": user_id,
        "deptId": dept_id,
        "device_id": device_id,
        "action": action,  # "status_change", "update", "delete"
        "before": before,
        "after": after,
        "timestamp": datetime.utcnow(),
    }
