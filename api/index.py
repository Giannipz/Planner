"""
Vercel Python serverless entrypoint.

Vercel's Python builder auto-detects an ASGI `app` object in files under
/api. The actual FastAPI app lives in backend/server.py (also used for local
`uvicorn` runs) so this file just re-exports it, adding backend/ to the path
since Vercel bundles each function in isolation.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from server import app  # noqa: E402
