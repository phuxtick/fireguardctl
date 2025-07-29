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
    services: str  # JSON string of metrics
    interfaces: Optional[str] = None  # <- ADD THIS
    system_info: Optional[str] = None  # <- AND THIS
    timestamp: datetime
