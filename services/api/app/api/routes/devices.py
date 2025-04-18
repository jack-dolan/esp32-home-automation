from fastapi import APIRouter, HTTPException, Depends
from typing import List
from uuid import uuid4

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
async def control_device(device_id: str, command: DeviceCommandRequest):
    device = await db_service.get_device(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    # In the real app, I'd send the command to the device
    # For now, we'll just simulate it by recording the command
    command_id = str(uuid4())
    
    return {
        "success": True, 
        "command_id": command_id,
        "message": f"Command {command.action} sent to device {device_id}"
    }