from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from config.database import db
from services import auth_service
from services.ai_analytics_service import analyze_department, analyze_company

router = APIRouter()

# Only admins can access analytics
async def require_admin(current_user=Depends(auth_service.get_current_user)):
	if current_user["role"] not in ("company_admin", "dept_admin"):
		raise HTTPException(status_code=403, detail="Admins only")
	return current_user

# --- Analyze a specific department ---
@router.get("/analyze/department/{dept_id}")
async def ai_analyze_department(dept_id: str, current_user=Depends(require_admin)):
	dept = await db["departments"].find_one({"_id": ObjectId(dept_id)})
	if not dept:
		raise HTTPException(status_code=404, detail="Department not found")
	result = await analyze_department(dept)
	return {"analysis": result}

# --- Analyze the whole company ---
@router.get("/analyze/company")
async def ai_analyze_company(current_user=Depends(require_admin)):
	cursor = db["departments"].find()
	departments = []
	async for d in cursor:
		departments.append(d)
	if not departments:
		raise HTTPException(status_code=404, detail="No departments found")
	result = await analyze_company(departments)
	return {"analysis": result}
