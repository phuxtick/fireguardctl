# --- Imports ---
import os
import json
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from sqlmodel import select
from app.models import HostStatus, StatusPayload
from app.database import get_session

# --- Constants ---
STALE_THRESHOLD_MINUTES = 5

# --- Router Setup ---
router = APIRouter()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# --- Routes ---

@router.get("/dashboard", response_class=HTMLResponse)
async def show_dashboard(request: Request):
    host_display_data = {}
    now = datetime.now(timezone.utc)

    with get_session() as session:
        hosts = session.exec(select(HostStatus)).all()

        for host in hosts:
            timestamp = host.timestamp
            if timestamp.tzinfo is None:
                timestamp = timestamp.replace(tzinfo=timezone.utc)

            delta = now - timestamp
            is_stale = delta > timedelta(minutes=STALE_THRESHOLD_MINUTES)

    host_display_data[host.hostname] = {
        "location": host.location,
        "services": json.loads(host.services),
        "interfaces": json.loads(host.interfaces) if host.interfaces else {},
        "system_info": json.loads(host.system_info) if host.system_info else {},
        "timestamp": timestamp,
        "is_stale": is_stale
    }



    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "status_data": host_display_data
    })


@router.post("/api/status")
async def update_status(payload: StatusPayload):
    timestamp = payload.timestamp
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)

    with get_session() as session:
        existing = session.exec(
            select(HostStatus).where(HostStatus.hostname == payload.hostname)
        ).first()

        if existing:
            session.delete(existing)

        host = HostStatus(
            hostname=payload.hostname,
            location=payload.location,
            services=json.dumps(payload.services),
            timestamp=timestamp
        )
        session.add(host)
        session.commit()

    return {"message": "Status updated."}
