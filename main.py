# main.py
from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials



# Routers
from routes import auth_routes, CoAdmin_routes, department_routes, ai_routes,device_routes, activity_routes, department_routes, auth_routes, energy_routes, stats_routes

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

@app.get("/")
def root():
    return {"message": "Welcome to EcoTrack API 🚀"}
