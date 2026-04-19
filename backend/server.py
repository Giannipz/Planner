"""
Minimal FastAPI backend for Planner PWA.

The frontend is a static single-page app that stores everything in the user's
localStorage and syncs directly with Google Calendar. This backend only exists
to satisfy the deployment platform's requirements (health check + /api prefix).
"""
import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Planner API", version="3.0.0")

# CORS: allow the frontend origin (and any other configured origin)
_cors_origins_env = os.environ.get("CORS_ORIGINS", "*")
_cors_origins = [o.strip() for o in _cors_origins_env.split(",") if o.strip()] or ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


@app.get("/api/", response_model=HealthResponse)
async def root():
    return HealthResponse(status="ok", service="planner-api", version="3.0.0")


@app.get("/api/health", response_model=HealthResponse)
async def health():
    return HealthResponse(status="ok", service="planner-api", version="3.0.0")
