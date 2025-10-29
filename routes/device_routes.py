# routes/device_routes.py
from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from services import auth_service, device_service
import logging
from models.device import Device

router = APIRouter()
logger = logging.getLogger(__name__)

# --- Require Admin ---
async def require_admin(current_user=Depends(auth_service.get_current_user)):
    if current_user["role"] != "company_admin":
        raise HTTPException(status_code=403, detail="Admins only")
    return current_user


# -------------------------------
# 🚀 Device Management
# -------------------------------

# --- Create Device ---
@router.post("/devices")
async def create_device(device: Device, current_user=Depends(require_admin)):
    device_data = device.dict()  # convert to dict for service
    device_id = await device_service.create_device(device_data)
    return {"message": "Device created successfully", "device_id": device_id}

# --- Get All Devices in a Department ---
@router.get("/devices/department/{dept_id}")
async def get_devices_by_department(dept_id: str, current_user=Depends(require_admin)):
    devices = await device_service.get_devices_by_department(dept_id)
    return {"devices": devices}

# --- Get All Devices ---
@router.get("/devices")
async def get_all_devices(current_user=Depends(require_admin)):
    devices = await device_service.get_all_devices()
    return {"devices": devices}



# --- Get Single Device ---
@router.get("/devices/{device_id}")
async def get_device(device_id: str, current_user=Depends(require_admin)):
    device = await device_service.get_device(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


# --- Update Device ---
@router.put("/devices/{device_id}")
async def update_device(device_id: str, update: dict, current_user=Depends(require_admin)):
    updated = await device_service.update_device(device_id, update)
    if not updated:
        raise HTTPException(status_code=404, detail="Device not found")
    return {"message": "Device updated successfully"}



# --- Simulate Device State & Metrics ---
from fastapi import Body


# --- Allow both company_admin and dept_admin ---
async def require_company_or_dept_admin(current_user=Depends(auth_service.get_current_user)):
    if current_user["role"] not in ("company_admin", "dept_admin"):
        raise HTTPException(status_code=403, detail="Admins only")
    return current_user

@router.patch("/devices/{device_id}/simulate")
async def simulate_device(
    device_id: str,
    status: str = Body(...),
    active_hours: float = Body(...),
    idle_hours: float = Body(...),
    overtime_hours: float = Body(...),
    current_user=Depends(require_company_or_dept_admin)
):
    updated = await device_service.simulate_device(
        device_id,
        status,
        active_hours,
        idle_hours,
        overtime_hours,
        user_id=current_user["_id"]
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Device not found")
    return {"message": "Device state and metrics updated"}



# --- Delete Device ---
@router.delete("/devices/{device_id}")
async def delete_device(device_id: str, current_user=Depends(require_admin)):
    deleted = await device_service.delete_device(device_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Device not found")
    return {"message": "Device deleted successfully"}
