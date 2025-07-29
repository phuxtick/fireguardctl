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
    hostname: str = Field(primary_key=True)
    location: str
    services: str  # stored as JSON string
    interfaces: Optional[str] = None  # JSON string of dict
    system_info: Optional[str] = None  # JSON string of dict
    timestamp: datetime
