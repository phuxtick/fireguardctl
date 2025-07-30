from typing import Dict, Optional
from datetime import datetime
from pydantic import BaseModel

class StatusPayload(BaseModel):
    hostname: str
    location: str
    services: Dict[str, str]
    interfaces: Optional[Dict[str, str]] = None
    system_info: Optional[Dict[str, str]] = None
    endpoints: Dict[str, str] = {}
    timestamp: datetime


from sqlmodel import SQLModel, Field
from typing import Optional, Dict
from datetime import datetime

class HostStatus(SQLModel, table=True):
    hostname: str = Field(primary_key=True)
    location: str
    services: str
    interfaces: Optional[str] = None
    system_info: Optional[str] = None
    endpoints: Optional[str] = None
    timestamp: datetime
