import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Home Automation API"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # AWS Configuration
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")
    DYNAMODB_TABLE_DEVICES: str = os.getenv("DYNAMODB_TABLE_DEVICES", "Devices")
    DYNAMODB_TABLE_TEMPERATURES: str = os.getenv("DYNAMODB_TABLE_TEMPERATURES", "Temperature")
    
    # Mock DB configuration
    USE_MOCK_DB: bool = os.getenv("USE_MOCK_DB", "true").lower() == "true"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()