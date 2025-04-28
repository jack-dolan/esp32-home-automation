from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any, Union, List
from datetime import datetime
from enum import Enum

# Define state types for different devices
class TemperatureState(BaseModel):
    temperature: float
    humidity: Optional[float] = None
    battery_level: Optional[int] = None
    last_reading: datetime = Field(default_factory=datetime.now)

class ThermostatState(BaseModel):
    current_temperature: float
    target_temperature: float
    mode: str = "heat"  # heat, cool, off
    is_heating: bool = False
    is_cooling: bool = False
    humidity: Optional[float] = None
    
    @validator('mode')
    def validate_mode(cls, v):
        valid_modes = ["heat", "cool", "off", "auto"]
        if v not in valid_modes:
            raise ValueError(f"Mode must be one of: {', '.join(valid_modes)}")
        return v

class BlindState(BaseModel):
    position: int = 0  # 0-100%, 0 is closed, 100 is open. Will I ever use this? 
    is_moving: bool = False
    
    @validator('position')
    def validate_position(cls, v):
        if not 0 <= v <= 100:
            raise ValueError("Position must be between 0 and 100")
        return v

# Combined state model for all device types
class DeviceState(BaseModel):
    device_id: str
    last_updated: datetime = Field(default_factory=datetime.now)
    type: str
    state: Union[TemperatureState, ThermostatState, BlindState]
    
    class Config:
        orm_mode = True

# Response models
class StateResponse(BaseModel):
    success: bool = True
    message: Optional[str] = None
    state: Optional[DeviceState] = None

class StateUpdateRequest(BaseModel):
    state: Dict[str, Any]