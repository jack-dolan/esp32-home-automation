from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from uuid import uuid4

from app.api.models.device import (
    Device, DeviceCreate, DeviceList, DeviceResponse
)
from app.api.models.base import BaseResponse  # Add this import
from app.api.models.control import DeviceCommand, CommandResponse
from app.db.dynamodb import db_service


from app.api.models.device import (
    Device, DeviceCreate, DeviceList, DeviceResponse,
    DeviceCommandRequest, DeviceCommandResponse
)
from app.db.dynamodb import db_service

router = APIRouter()

@router.get("/", response_model=DeviceList)
async def get_devices():
    devices = await db_service.get_devices()
    return {"devices": devices, "success": True}

@router.get("/{device_id}", response_model=DeviceResponse)
async def get_device(device_id: str):
    device = await db_service.get_device(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return {"device": device, "success": True}

@router.post("/", response_model=DeviceResponse)
async def create_device(device: DeviceCreate):
    device_data = device.dict()
    device_data["id"] = str(uuid4())
    device_data["status"] = "offline"
    
    created_device = await db_service.create_device(device_data)
    return {"device": created_device, "success": True}

@router.post("/{device_id}/control", response_model=DeviceCommandResponse)
@router.post("/{device_id}/control", response_model=CommandResponse)
async def control_device(device_id: str, command: DeviceCommand):
    device = await db_service.get_device(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    # Validate command based on device type
    device_type = device.get("type")
    
    if device_type == "thermostat":
        if command.action not in ["set_temperature", "toggle_power"]:
            raise HTTPException(status_code=400, detail="Invalid action for thermostat")
        
        if command.action == "set_temperature" and ("temperature" not in command.params or not isinstance(command.params["temperature"], (int, float))):
            raise HTTPException(status_code=400, detail="Temperature parameter required")
    
    elif device_type == "blind":
        if command.action not in ["open", "close", "set_position"]:
            raise HTTPException(status_code=400, detail="Invalid action for blind")
        
        if command.action == "set_position" and ("position" not in command.params or not isinstance(command.params["position"], int)):
            raise HTTPException(status_code=400, detail="Position parameter required (0-100)")
    
    # In the real app, we'd send the command to the actual device
    # For now, we'll just generate a command ID
    command_id = str(uuid4())
    
    # Could store the command in dynamoDB if needed...
    # await db_service.create_command(device_id, command_id, command.dict())  # maybe?
    
    return {
        "success": True,
        "command_id": command_id,
        "status": "sent",
        "message": f"Command {command.action} sent to {device_type} {device_id}"
    }

@router.put("/{device_id}", response_model=DeviceResponse)
async def update_device(device_id: str, device_update: DeviceCreate):
    device = await db_service.get_device(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    device_data = device_update.dict()
    updated_device = await db_service.update_device(device_id, device_data)
    return {"device": updated_device, "success": True}

@router.delete("/{device_id}", response_model=BaseResponse)
async def delete_device(device_id: str):
    device = await db_service.get_device(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    result = await db_service.delete_device(device_id)
    return {"success": True, "message": f"Device {device_id} deleted successfully"}

@router.get("/{device_id}/status", response_model=DeviceResponse)
async def get_device_status(device_id: str):
    device = await db_service.get_device(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    # In the real app, I'd check the actual device status
    # For now, we'll just return what's in the db
    return {"device": device, "success": True}