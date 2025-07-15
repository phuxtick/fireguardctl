from pydantic import BaseModel
from typing import Dict
from datetime import datetime

class StatusPayload(BaseModel):
    hostname: str
    location: str
    services: Dict[str, str]
    timestamp: datetime
