from fastapi import APIRouter, HTTPException, Query
from datetime import datetime

from app.api.models.temperature import (
    TemperatureReading, TemperatureReadingCreate, TemperatureReadingList
)
from app.api.models.base import BaseResponse
from app.db.dynamodb import db_service

router = APIRouter()

@router.get("/{device_id}", response_model=TemperatureReadingList)
async def get_temperature_readings(
    device_id: str, 
    hours: int = Query(24, ge=1, le=168), 
    limit: int = Query(100, ge=1, le=1000)
):
    device = await db_service.get_device(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    readings = await db_service.get_temperature_readings(device_id, hours)
    
    # Sort by timestamp descending and apply limit
    readings = sorted(readings, key=lambda x: x.get("timestamp", 0), reverse=True)[:limit]
    
    return {"readings": readings, "success": True}

@router.get("/aggregate/{device_id}", response_model=BaseResponse)
async def get_temperature_aggregates(
    device_id: str, 
    hours: int = Query(24, ge=1, le=168)
):
    device = await db_service.get_device(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    readings = await db_service.get_temperature_readings(device_id, hours)
    
    # Calculate basic statistics
    if not readings:
        return {
            "success": True,
            "message": "No readings found for the specified period",
            "data": {}
        }
    
    temperatures = [r.get("temperature", 0) for r in readings]
    
    avg_temp = sum(temperatures) / len(temperatures)
    min_temp = min(temperatures)
    max_temp = max(temperatures)
    
    return {
        "success": True,
        "data": {
            "average_temperature": round(avg_temp, 1),
            "min_temperature": min_temp,
            "max_temperature": max_temp,
            "readings_count": len(readings)
        }
    }

@router.post("/", response_model=TemperatureReadingList)
async def create_temperature_reading(reading: TemperatureReadingCreate):
    device = await db_service.get_device(reading.device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    # Update device status to online and update last_seen
    device_update = {
        "status": "online",
        "last_seen": datetime.now().isoformat()
    }
    await db_service.update_device(reading.device_id, device_update)
    
    # Save the temperature reading
    reading_data = reading.dict()
    created_reading = await db_service.create_temperature_reading(reading_data)
    
    return {"readings": [created_reading], "success": True}