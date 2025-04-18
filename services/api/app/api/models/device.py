from pydantic import BaseModel, Field
from typing import Optional, List, Union
from datetime import datetime
from uuid import UUID, uuid4

from app.api.models.base import BaseResponse

# Replaced Literal with explicit string constants
DEVICE_TYPES = ["temperature", "thermostat", "blind"]
DEVICE_STATUSES = ["online", "offline"]

class DeviceBase(BaseModel):
    name: str
    type: str  # Will validate in the model
    location: str
    
    def __init__(self, **data):
        super().__init__(**data)
        if self.type not in DEVICE_TYPES:
            raise ValueError(f"Device type must be one of: {', '.join(DEVICE_TYPES)}")

class DeviceCreate(DeviceBase):
    pass

class Device(DeviceBase):
    id: str = Field(default_factory=lambda: str(uuid4()))
    status: str = "offline"  # Default value
    last_seen: Optional[datetime] = None
    
    def __init__(self, **data):
        super().__init__(**data)
        if self.status not in DEVICE_STATUSES:
            raise ValueError(f"Device status must be one of: {', '.join(DEVICE_STATUSES)}")
    
    class Config:
        orm_mode = True

class DeviceList(BaseResponse):
    devices: List[Device] = []

class DeviceResponse(BaseResponse):
    device: Optional[Device] = None

class DeviceCommandRequest(BaseModel):
    action: str
    value: Optional[str] = None

class DeviceCommandResponse(BaseResponse):
    command_id: Optional[str] = None