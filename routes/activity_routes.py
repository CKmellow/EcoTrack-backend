# routes/activity_log_routes.py
from fastapi import APIRouter, Depends, HTTPException
from services import auth_service, activity_service

router = APIRouter()

# --- Require Admin ---
async def require_admin(current_user=Depends(auth_service.get_current_user)):
    if current_user["role"] != "company_admin":
        raise HTTPException(status_code=403, detail="Admins only")
    return current_user

async def require_admin(current_user=Depends(auth_service.get_current_user)):
    if current_user["role"] != "company_admin":
        raise HTTPException(status_code=403, detail="Admins only")
    return current_user

# --- Get All Logs ---
@router.get("/logs")
async def get_all_logs(current_user=Depends(require_admin)):
    logs = await activity_service.get_logs()
    return {"logs": logs}

# --- Get Logs by Device ---
@router.get("/logs/device/{device_id}")
async def get_device_logs(device_id: str, current_user=Depends(require_admin)):
    logs = await activity_service.get_logs(filter_query={"device_id": device_id})
    return {"logs": logs}

# --- Get Logs by User ---
@router.get("/logs/user/{user_id}")
async def get_user_logs(user_id: str, current_user=Depends(require_admin)):
    logs = await activity_service.get_logs(filter_query={"user_id": user_id})
    return {"logs": logs}
