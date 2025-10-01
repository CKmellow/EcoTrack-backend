# models/device.py
from pydantic import BaseModel, Field
from typing import Optional

class Device(BaseModel):
    deviceName: str
    type: str
    powerRating: str
    status: str = Field(default="off")
    deptId: str   # Will be converted to ObjectId in service
    user_id: str  # Will be converted to ObjectId in service
