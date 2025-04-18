from fastapi import APIRouter, HTTPException
from datetime import datetime

from app.api.models.temperature import (
    TemperatureReading, TemperatureReadingCreate, TemperatureReadingList
)
from app.db.dynamodb import db_service

router = APIRouter()

@router.get("/{device_id}", response_model=TemperatureReadingList)
async def get_temperature_readings(device_id: str, hours: int = 24):
    device = await db_service.get_device(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    readings = await db_service.get_temperature_readings(device_id, hours)
    return {"readings": readings, "success": True}

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