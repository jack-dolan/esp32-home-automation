from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, Optional
from datetime import datetime

from app.models.device import Device
from app.models.state import StateResponse, StateUpdateRequest, DeviceState
from app.db.database import db_service
from app.api.routes.devices import verify_api_key

router = APIRouter()

@router.get("/{device_id}", response_model=StateResponse)
async def get_device_state(device_id: str, api_key: str = Depends(verify_api_key)):
    """Get the current state of a device"""
    # Check device exists
    device = await db_service.get_device(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    # Get state
    state = await db_service.get_device_state(device_id)
    if not state:
        raise HTTPException(status_code=404, detail="State not found for device")
    
    return {"state": state, "success": True}

@router.put("/{device_id}", response_model=StateResponse)
async def update_device_state(
    device_id: str, 
    state_update: StateUpdateRequest,
    api_key: str = Depends(verify_api_key)
):
    """Update the state of a device"""
    # Check device actually exists
    device = await db_service.get_device(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    # Validate state update for specific device type
    device_type = device.type
    state_data = state_update.state
    
    try:
        # Create state instance based on device type
        updated_state = await db_service.update_device_state(device_id, {
            "device_id": device_id,
            "type": device_type,
            "last_updated": datetime.now().isoformat(),
            "state": state_data
        })
        
        # Update device last_seen
        await db_service.update_device(device_id, {"last_seen": datetime.now().isoformat()})
        
        # also record in history
        await db_service.record_state_history(device_id, updated_state)
        
        return {"success": True, "state": updated_state}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))