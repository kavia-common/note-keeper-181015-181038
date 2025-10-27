from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .models import Note  # noqa: F401 - ensure model is imported so metadata includes it
from .routers_notes import router as notes_router

# Create tables automatically (simple auto-migrations for initial setup)
Base.metadata.create_all(bind=engine)

app = FastAPI(
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
def health_check():
    """Health check endpoint returning a simple JSON status."""
    return {"status": "ok"}


# Mount notes router under /api/notes
app.include_router(notes_router)
