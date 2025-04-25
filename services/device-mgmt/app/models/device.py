from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID, uuid4

# Consts for valid device types and statuses
DEVICE_TYPES = ["temperature", "thermostat", "blind"]
DEVICE_STATUSES = ["offline", "online", "provisioning"]

class DeviceRegistration(BaseModel):
    """Model for device registration request"""
    name: str
    type: str
    location: str
    mac_address: str
    hardware_version: str
    firmware_version: str
    
    def __init__(self, **data):
        super().__init__(**data)
        if self.type not in DEVICE_TYPES:
            raise ValueError(f"Device type must be one of: {', '.join(DEVICE_TYPES)}")

class Device(DeviceRegistration):
    """Model for device in the database"""
    id: str = Field(default_factory=lambda: str(uuid4()))
    status: str = "provisioning"
    last_seen: Optional[datetime] = None
    registration_date: datetime = Field(default_factory=datetime.now)
    api_key: str = Field(default_factory=lambda: str(uuid4()))
    
    def __init__(self, **data):
        super().__init__(**data)
        if self.status not in DEVICE_STATUSES:
            raise ValueError(f"Device status must be one of: {', '.join(DEVICE_STATUSES)}")
    
    class Config:
        orm_mode = True

class DeviceResponse(BaseModel):
    """Response model for device operations"""
    success: bool = True
    message: Optional[str] = None
    device: Optional[Device] = None

class DeviceListResponse(BaseModel):
    """Response model for listing devices"""
    success: bool = True
    message: Optional[str] = None
    devices: List[Device] = []