from bson import ObjectId
from config.database import db
from services.activity_service import log_and_recalc

devices = db["devices"]

# -------------------------------
# CREATE
# -------------------------------
async def create_device(device_data: dict, user_id: str = "system"):
    """Create a new device and log"""
    result = await devices.insert_one(device_data)
    device_id = str(result.inserted_id)

    new_device = await devices.find_one({"_id": ObjectId(device_id)})

    await log_and_recalc(
        user_id=user_id,
        dept_id=new_device.get("deptId"),
        device_id=device_id,
        action="create",
        before=None,
        after=new_device,
    )
    return device_id


# -------------------------------
# READ
# -------------------------------
async def get_devices_by_department(dept_id: str):
    """Fetch all devices in a given department"""
    try:
        cursor = devices.find({"deptId": dept_id})
        result = []
        async for d in cursor:
            doc = dict(d)
            # Convert all ObjectId fields to str
            for key, value in doc.items():
                if isinstance(value, ObjectId):
                    doc[key] = str(value)
            result.append(doc)
        return result
    except Exception:
        return []

async def get_device(device_id: str):
    """Fetch a single device by ID"""
    device = await devices.find_one({"_id": ObjectId(device_id)})
    if device:
        for key, value in device.items():
            if isinstance(value, ObjectId):
                device[key] = str(value)
    return device

async def get_all_devices():
    """Fetch all devices across all departments"""
    cursor = devices.find({})
    result = []
    async for d in cursor:
        doc = dict(d)
        for key, value in doc.items():
            if isinstance(value, ObjectId):
                doc[key] = str(value)
        result.append(doc)
    return result


# -------------------------------
# UPDATE STATUS
# -------------------------------
async def update_device_status(device_id: str, status: str, user_id: str = "system"):
    """Update only the status field of a device and log"""
    device = await devices.find_one({"_id": ObjectId(device_id)})
    if not device:
        return False

    before = device.copy()

    await devices.update_one(
        {"_id": ObjectId(device_id)},
        {"$set": {"status": status}}
    )

    after = await devices.find_one({"_id": ObjectId(device_id)})

    await log_and_recalc(
        user_id=user_id,
        dept_id=after.get("deptId"),
        device_id=device_id,
        action="status_change",
        before=before,
        after=after,
    )
    return True


# -------------------------------
# UPDATE DEVICE
# -------------------------------
async def update_device(device_id: str, update: dict, user_id: str = "system"):
    """Update device details and log"""
    device = await devices.find_one({"_id": ObjectId(device_id)})
    if not device:
        return False

    before = device.copy()

    await devices.update_one(
        {"_id": ObjectId(device_id)},
        {"$set": update}
    )

    after = await devices.find_one({"_id": ObjectId(device_id)})

    await log_and_recalc(
        user_id=user_id,
        dept_id=after.get("deptId"),
        device_id=device_id,
        action="update",
        before=before,
        after=after,
    )
    return True


# -------------------------------
# DELETE DEVICE
# -------------------------------
async def delete_device(device_id: str, user_id: str = "system"):
    """Delete device and log"""
    device = await devices.find_one({"_id": ObjectId(device_id)})
    if not device:
        return False

    before = device.copy()

    result = await devices.delete_one({"_id": ObjectId(device_id)})

    if result.deleted_count:
        await log_and_recalc(
            user_id=user_id,
            dept_id=before.get("deptId"),
            device_id=device_id,
            action="delete",
            before=before,
            after=None,
        )

    return result.deleted_count > 0
