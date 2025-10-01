# routes/energy_routes.py
# routers/energy_router.py

from fastapi import APIRouter, HTTPException
from services.energy_service import enrich_department_with_energy
from config.database import db
from bson import ObjectId

router = APIRouter(prefix="/energy", tags=["Energy"])

@router.get("/department/{department_id}")
async def get_department_energy(department_id: str):
    try:
        obj_id = ObjectId(department_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid department ID format")
    department = await db.departments.find_one({"_id": obj_id})
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    enriched = await enrich_department_with_energy(department)
    return enriched

