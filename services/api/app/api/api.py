from fastapi import APIRouter
from app.api.routes import devices, temperature

api_router = APIRouter()
api_router.include_router(devices.router, prefix="/devices", tags=["devices"])
api_router.include_router(temperature.router, prefix="/temperature", tags=["temperature"])