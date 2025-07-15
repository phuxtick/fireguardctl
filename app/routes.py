from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@router.get("/dashboard", response_class=HTMLResponse)
async def show_dashboard(request: Request):
    from app.routes import status_data
    print("STATUS DATA:", status_data)  # 👈 add this
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "status_data": status_data
        }
    )

from app.models import StatusPayload

# In-memory storage
status_data = {}

@router.post("/api/status")
async def update_status(payload: StatusPayload):
    status_data[payload.hostname] = {
        "location": payload.location,
        "services": payload.services,
        "timesampt": payload.timestamp
    }
    return {"message": "Status updated."}
