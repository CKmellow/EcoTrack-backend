# routes/CoAdmin_routes.py
from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from models.user import UserSignup
from models.department import Department
from services import auth_service
from config.database import db
import logging

router = APIRouter()
logger=logging.getLogger(__name__)

# --- Require Admin ---
async def require_admin(current_user=Depends(auth_service.get_current_user)):
    logger.info(f"🔑 Current user role: {current_user.get('role')}")
    if current_user["role"] != "company_admin":
        raise HTTPException(status_code=403, detail="Admins only")
    return current_user

# --- Add User ---
@router.post("/company/add-user")
async def add_user(new_user: UserSignup, current_user=Depends(require_admin)):
    user_dict = new_user.dict()

    # Check if email already exists
    existing = await db["users"].find_one({"email": user_dict["email"]})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user
    user_id = await auth_service.create_user(user_dict)

    return {"message": "User created successfully", "user_id": str(user_id)}
# --- Get single User ---
@router.get("/company/user/{user_id}")
async def get_user(user_id: str, current_user=Depends(require_admin)):
    user = await db["users"].find_one(
        {"_id": ObjectId(user_id)},
        {"password": 0}
    )
    if not user:
        raise HTTPException(status_code=404, detail="User not found or not in your company")
    user["_id"] = str(user["_id"])
    return user

# --- Edit User ---
@router.put("/company/edit-user/{user_id}")
async def edit_user(user_id: str, update: dict, current_user=Depends(require_admin)):
    result = await db["users"].update_one(
        {"_id": ObjectId(user_id)},
        {"$set": update}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found or not in your company")

    return {"message": "User updated successfully"}

# --- Delete User ---
@router.delete("/company/delete-user/{user_id}")
async def delete_user(user_id: str, current_user=Depends(require_admin)):
    result = await db["users"].delete_one(
        {"_id": ObjectId(user_id)}
    )
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found or not in your company")

    return {"message": "User deleted successfully"}

# --- View all Department Admins ---
@router.get("/company/department-admins")
async def get_department_admins(current_user=Depends(require_admin)):
    cursor = db["users"].find(
        {"role": "department_admin"},
        {"password": 0}
    )
    admins = []
    async for admin in cursor:
        admin["_id"] = str(admin["_id"])
        admins.append(admin)
    return admins


# -------------------------------
# 🚀 Department Management
# -------------------------------

# --- Create Department ---
@router.post("/company/departments")
async def create_department(dept: Department, current_user=Depends(require_admin)):
    dept_dict = dept.dict()



    result = await db["departments"].insert_one(dept_dict)
    return {
        "message": "Department created successfully",
        "department_id": str(result.inserted_id)
    }
# --- Get all Departments ---
# --- Get all Departments ---
@router.get("/company/departments")
async def list_departments(current_user=Depends(require_admin)):
    cursor = db["departments"].find({})
    departments = []
    async for dept in cursor:
        departments.append({
            "department_id": str(dept["_id"]),
            "name": dept.get("name"),            # Replace 'name' with your actual department fields
            "description": dept.get("description")  # Optional
            # Add any other fields from your Department model
        })
    return {
        "message": "Departments retrieved successfully",
        "departments": departments
    }


# --- Get single Department ---
@router.get("/company/departments/{dept_id}")
async def get_department(dept_id: str, current_user=Depends(require_admin)):
    dept = await db["departments"].find_one(
        {"_id": ObjectId(dept_id)}
    )
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found or not in your company")
    dept["_id"] = str(dept["_id"])
    return dept

# --- Update Department ---
@router.put("/company/departments/{dept_id}")
async def update_department(dept_id: str, update: dict, current_user=Depends(require_admin)):
    result = await db["departments"].update_one(
        {"_id": ObjectId(dept_id)},
        {"$set": update}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Department not found or not in your company")
    return {"message": "Department updated successfully"}

# --- Delete Department ---
@router.delete("/company/departments/{dept_id}")
async def delete_department(dept_id: str, current_user=Depends(require_admin)):
    result = await db["departments"].delete_one(
        {"_id": ObjectId(dept_id)}
    )
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Department not found or not in your company")
    return {"message": "Department deleted successfully"}
