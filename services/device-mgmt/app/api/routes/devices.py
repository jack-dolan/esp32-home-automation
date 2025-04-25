from fastapi import APIRouter, HTTPException, Query, Header, Depends
from typing import List, Optional
from uuid import uuid4

from app.models.device import (
    Device, DeviceRegistration, DeviceResponse, DeviceListResponse
)
from app.db.database import db_service

router = APIRouter()

async def verify_api_key(x_api_key: str = Header(...)):
    """
    Verify API key for protected endpoints.
    In the big boy final app, this would verify against a secure API key store.
    """
    # For development, using a hardcoded key
    # In prod, this would validate against secure storage
    VALID_API_KEYS = ["dev_api_key_12345"]
    if x_api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key

@router.get("/", response_model=DeviceListResponse)
async def get_devices(api_key: str = Depends(verify_api_key)):
    """Get all registered devices"""
    devices = await db_service.get_devices()
    return {"devices": devices, "success": True}

@router.get("/{device_id}", response_model=DeviceResponse)
async def get_device(device_id: str, api_key: str = Depends(verify_api_key)):
    """Get a specific device by ID"""
    device = await db_service.get_device(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return {"device": device, "success": True}

@router.post("/register", response_model=DeviceResponse)
async def register_device(device: DeviceRegistration, api_key: str = Depends(verify_api_key)):
    """Register a new device"""
    # Check if device with this MAC already exists
    existing_device = await db_service.get_device_by_mac(device.mac_address)
    if existing_device:
        return {
            "success": True,
            "message": "Device already registered",
            "device": existing_device
        }
    
    # Create new device
    device_data = device.dict()
    device_data["status"] = "provisioning"
    device_data["id"] = str(uuid4())
    device_data["api_key"] = str(uuid4())  # generate unique API key for device
    
    created_device = await db_service.create_device(device_data)
    return {
        "success": True,
        "message": "Device registered successfully",
        "device": created_device
    }

@router.put("/{device_id}/activate", response_model=DeviceResponse)
async def activate_device(device_id: str, api_key: str = Depends(verify_api_key)):
    """Activate a device after provisioning"""
    device = await db_service.get_device(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    if device.status != "provisioning":
        return {
            "success": True, 
            "message": f"Device already in {device.status} state",
            "device": device
        }
    
    updated_device = await db_service.update_device(device_id, {"status": "online"})
    return {
        "success": True,
        "message": "Device activated successfully",
        "device": updated_device
    }

@router.delete("/{device_id}", response_model=DeviceResponse)
async def deregister_device(device_id: str, api_key: str = Depends(verify_api_key)):
    """Remove a device from the registry"""
    device = await db_service.get_device(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    success = await db_service.delete_device(device_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete device")
    
    return {
        "success": True,
        "message": f"Device {device_id} deleted successfully"
    }