from pydantic import BaseModel, Field
from typing import Optional, Union, Dict, Any
from app.api.models.base import BaseResponse

# Constants for valid actions
THERMOSTAT_ACTIONS = ["set_temperature", "toggle_power"]
BLIND_ACTIONS = ["open", "close", "set_position"]

class ThermostatCommand(BaseModel):
    action: str
    temperature: Optional[float] = None
    
    def __init__(self, **data):
        super().__init__(**data)
        if self.action not in THERMOSTAT_ACTIONS:
            raise ValueError(f"Thermostat action must be one of: {', '.join(THERMOSTAT_ACTIONS)}")

class BlindCommand(BaseModel):
    action: str
    position: Optional[int] = None  # 0-100 percentage
    
    def __init__(self, **data):
        super().__init__(**data)
        if self.action not in BLIND_ACTIONS:
            raise ValueError(f"Blind action must be one of: {', '.join(BLIND_ACTIONS)}")

class DeviceCommand(BaseModel):
    action: str
    params: Optional[Dict[str, Any]] = None

class CommandResponse(BaseResponse):
    command_id: str
    status: str = "pending"