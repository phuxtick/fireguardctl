from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.routes import router as status_router
import os

app = FastAPI()

# Template engine
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Include routes from route.py
app.include_router(status_router)

# Optional: mount static files (CSS/images)
app.mount("/static", StaticFiles(directory="static"), name="static")

from app.database import init_db

init_db()