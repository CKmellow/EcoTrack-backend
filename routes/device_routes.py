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


# --- Update Device Status Only ---
@router.patch("/devices/{device_id}/status")
async def update_device_status(device_id: str, status: str, current_user=Depends(require_admin)):
    updated = await device_service.update_device_status(device_id, status, user_id=current_user["_id"])
    if not updated:
        raise HTTPException(status_code=404, detail="Device not found")
    return {"message": f"Device status updated to {status}"}



# --- Delete Device ---
@router.delete("/devices/{device_id}")
async def delete_device(device_id: str, current_user=Depends(require_admin)):
    deleted = await device_service.delete_device(device_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Device not found")
    return {"message": "Device deleted successfully"}
