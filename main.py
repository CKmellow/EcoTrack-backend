# main.py
import os
from datetime import datetime, timezone

from fastapi import FastAPI, Depends, Header, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from config.database import db



# Routers
from routes import auth_routes, CoAdmin_routes, department_routes, ai_routes, device_routes, activity_routes, energy_routes

# Middleware
from middleware.cors import setup_cors


app = FastAPI(title="EcoTrack Backend")

# Apply CORS
setup_cors(app)

security = HTTPBearer()

# Routers
app.include_router(auth_routes.router, prefix="/api/auth", tags=["Auth"])
app.include_router(CoAdmin_routes.router, prefix="/api/admin", tags=["Admin"])
app.include_router(department_routes.router, prefix="/api/departments", tags=["Departments"])
app.include_router(device_routes.router, prefix="/api/devices", tags=["Devices"])
app.include_router(activity_routes.router, prefix="/api/activity", tags=["Activity Logs"])
app.include_router(energy_routes.router, prefix="/api/energy", tags=["Energy"])



@app.get("/protected")
async def protected_route(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    return {"message": "Access granted", "token": token}

app.include_router(ai_routes.router, prefix="/api/ai", tags=["AI Analytics"])


@app.get("/")
def root():
    return {"message": "Welcome to EcoTrack API 🚀"}


@app.get("/api/internal/keepalive")
async def keepalive(authorization: str | None = Header(default=None)):
    cron_secret = os.getenv("CRON_SECRET")
    if cron_secret and authorization != f"Bearer {cron_secret}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        ping = await db.command("ping")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"DB ping failed: {exc}") from exc

    return {
        "status": "ok",
        "ping": ping,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
