from pydantic import BaseModel
from typing import Dict
from datetime import datetime

class StatusPayload(BaseModel):
    hostname: str
    location: str
    services: Dict[str, str]
    timestamp: datetime

from sqlmodel import SQLModel, Field
from typing import Optional, Dict
from datetime import datetime

class HostStatus(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hostname: str
    location: str
    services: str  # We'll store this as a JSON string for now
    timestamp: datetime
