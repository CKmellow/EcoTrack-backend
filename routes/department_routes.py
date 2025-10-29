# routes/department_routes.py

from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from models.department import Department
from config.database import db
from services import auth_service

def default_metrics():
    return {
        "expected_daily": {"consumption": 0, "cost": 0, "emissions": 0},
        "expected_monthly": {"consumption": 0, "cost": 0, "emissions": 0},
        "overtime_daily": {"consumption": 0, "cost": 0, "emissions": 0},
        "overtime_monthly": {"consumption": 0, "cost": 0, "emissions": 0},
        "waste_daily": {"consumption": 0, "cost": 0, "emissions": 0},
        "waste_monthly": {"consumption": 0, "cost": 0, "emissions": 0},
        "deviation": {"consumption": 0, "cost": 0, "emissions": 0},
    }

router = APIRouter()

# Only Company Admins can manage departments
async def require_admin(current_user=Depends(auth_service.get_current_user)):
    if current_user["role"] != "company_admin":
        raise HTTPException(status_code=403, detail="Admins only")
    return current_user


# --- Recalculate Department Metrics ---
from services.metrics_service import update_department_metrics

@router.post("/departments/{dept_id}/recalculate")
async def recalculate_department_metrics(dept_id: str, current_user=Depends(require_admin)):
    result = await update_department_metrics(dept_id)
    if not result:
        raise HTTPException(status_code=404, detail="Department or devices not found")
    return result


# --- Create Department ---
@router.post("/departments")
async def create_department(dept: Department, current_user=Depends(require_admin)):
    dept_dict = dept.dict()
    if "metrics" not in dept_dict:
        dept_dict["metrics"] = default_metrics()
    result = await db["departments"].insert_one(dept_dict)
    return {"message": "Department created", "id": str(result.inserted_id)}


# --- List Departments (Company Only) ---
@router.get("/departments")
async def list_departments(current_user=Depends(require_admin)):
    cursor = db["departments"].find()
    depts = []
    async for d in cursor:
        d["_id"] = str(d["_id"])
        if "metrics" not in d:
            d["metrics"] = default_metrics()
        depts.append(d)
    return {"departments": depts}


# --- View Specific Department ---
@router.get("/departments/{dept_id}")
async def get_department(dept_id: str, current_user=Depends(require_admin)):
    if not ObjectId.is_valid(dept_id):
        raise HTTPException(status_code=400, detail="Invalid department ID format")

    dept = await db["departments"].find_one({
        "_id": ObjectId(dept_id)
    })
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    dept["_id"] = str(dept["_id"])
    if "metrics" not in dept:
        dept["metrics"] = default_metrics()
    return dept


# --- Edit Department ---
@router.put("/departments/{dept_id}")
async def edit_department(dept_id: str, update: dict, current_user=Depends(require_admin)):
    if not ObjectId.is_valid(dept_id):
        raise HTTPException(status_code=400, detail="Invalid department ID format")

    
    result = await db["departments"].update_one(
        {"_id": ObjectId(dept_id)},
        {"$set": update}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Department not found or not yours")
    return {"message": "Department updated successfully"}


# --- Delete Department ---
@router.delete("/departments/{dept_id}")
async def delete_department(dept_id: str, current_user=Depends(require_admin)):
    if not ObjectId.is_valid(dept_id):
        raise HTTPException(status_code=400, detail="Invalid department ID format")

    result = await db["departments"].delete_one(
        {"_id": ObjectId(dept_id)}
    )
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Department not found or not yours")
    return {"message": "Department deleted successfully"}
