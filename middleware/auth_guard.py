# middleware/auth_guard.py
from fastapi import Depends, HTTPException
from services import auth_service
import logging

logger = logging.getLogger(__name__)

async def require_company_admin(current_user=Depends(auth_service.get_current_user)):
    if current_user["role"] != "company_admin":
        raise HTTPException(status_code=403, detail="Company Admins only")
    return current_user

async def require_department_admin(current_user=Depends(auth_service.get_current_user)):
    if current_user["role"] not in ["department_admin", "company_admin"]:
        raise HTTPException(status_code=403, detail="Department Admins or Company Admins only")
    return current_user
