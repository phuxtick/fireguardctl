from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime, timedelta, timezone

import os

from app.models import StatusPayload

# In-memory storage
status_data = {}

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

STALE_THRESHOLD_MINUTES = 5

@router.get("/dashboard", response_class=HTMLResponse)
async def show_dashboard(request: Request):
    host_display_data = {}
    now = datetime.now(timezone.utc)

    for hostname, data in status_data.items():
        timestamp = data.get("timestamp")
        if not timestamp:
            print(f"Skipping {hostname} — no timestamp found.")
            continue

        if isinstance(timestamp, str):
            try:
                timestamp = datetime.fromisoformat(timestamp)
            except Exception as e:
                print(f"Error parsing timestamp for {hostname}: {e}")
                continue

        delta = now - timestamp
        is_stale = delta > timedelta(minutes=STALE_THRESHOLD_MINUTES)

        host_display_data[hostname] = {
            "location": data["location"],
            "services": data["services"],
            "timestamp": timestamp,
            "is_stale": is_stale
        }

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "status_data": host_display_data
    })



@router.post("/api/status")
async def update_status(payload: StatusPayload):
    status_data[payload.hostname] = {
        "location": payload.location,
        "services": payload.services,
        "timesampt": payload.timestamp
    }
    return {"message": "Status updated."}
