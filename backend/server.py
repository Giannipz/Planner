"""Minimal FastAPI backend for Planner PWA.

The frontend is a static single-page app that stores everything in the user's
localStorage and syncs directly with Google Calendar. This backend only exists
to satisfy the deployment platform's requirements (health check + /api prefix).
"""

import logging
import os
from typing import Final

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

APP_VERSION: Final[str] = os.environ.get("APP_VERSION", "3.0.0")
SERVICE_NAME: Final[str] = "planner-api"

app = FastAPI(title="Planner API", version=APP_VERSION)


def parse_cors_origins(origins_env: str | None) -> list[str]:
    """Parse and normalize configured CORS origins.

    Removes duplicates while preserving order and falls back to wildcard.
    """
    if not origins_env:
        return ["*"]

    origins: list[str] = []
    for origin in origins_env.split(","):
        value = origin.strip()
        if value and value not in origins:
            origins.append(value)

    return origins or ["*"]


cors_origins = parse_cors_origins(os.environ.get("CORS_ORIGINS"))
allow_credentials = "*" not in cors_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info(
    "CORS configured",
    extra={"allow_origins": cors_origins, "allow_credentials": allow_credentials},
)


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


def _health_payload() -> HealthResponse:
    return HealthResponse(status="ok", service=SERVICE_NAME, version=APP_VERSION)


@app.get("/api/", response_model=HealthResponse)
async def root() -> HealthResponse:
    return _health_payload()


@app.get("/api/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return _health_payload()
