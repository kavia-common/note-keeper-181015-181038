from __future__ import annotations

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .models import Note  # noqa: F401 - ensure model is imported so metadata includes it
from .routers_notes import router as notes_router

# Create tables automatically (simple auto-migrations for initial setup)
Base.metadata.create_all(bind=engine)

# PUBLIC_INTERFACE
app = FastAPI(
    """
    FastAPI application for the Notes service.

    Exposes CRUD endpoints under /api/notes and a health check at /health.
    This app is designed to be imported by ASGI servers like uvicorn: 'src.api.main:app'.
    """,
    title="Notes API",
    description="A simple Notes service exposing CRUD operations.",
    version="1.0.0",
    openapi_tags=[
        {"name": "Health", "description": "Service health checks"},
        {"name": "Notes", "description": "CRUD operations on notes"},
    ],
)

# Enable permissive CORS for preview/frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    "/health",
    tags=["Health"],
    summary="Health Check",
    description="Checks if the service is up and responding.",
)
# PUBLIC_INTERFACE
def health_check():
    """
    Health check endpoint.

    Returns:
        dict: A simple JSON object with service status.
    """
    return {"status": "ok"}


# Mount notes router under /api/notes
app.include_router(notes_router)


# Allow running via `python -m src.api.main` or `python src/api/main.py`
if __name__ == "__main__":
    # Avoid importing uvicorn during app import in some environments
    import uvicorn

    host = os.getenv("HOST", "0.0.0.0")
    port_str = os.getenv("PORT", "3001")
    try:
        port = int(port_str)
    except ValueError:
        port = 3001

    uvicorn.run("src.api.main:app", host=host, port=port, reload=False, factory=False)
