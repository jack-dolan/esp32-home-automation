from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID, uuid4

from app.api.models.base import BaseResponse

class TemperatureReading(BaseModel):
    device_id: str
    timestamp: datetime = Field(default_factory=datetime.now)
    temperature: float
    humidity: Optional[float] = None

class TemperatureReadingCreate(TemperatureReading):
    pass

class TemperatureReadingList(BaseResponse):
    readings: List[TemperatureReading] = []