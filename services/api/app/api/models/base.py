from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class BaseResponse(BaseModel):
    success: bool = True
    message: Optional[str] = None