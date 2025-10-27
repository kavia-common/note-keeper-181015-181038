#!/usr/bin/env python3
"""
Run script for the Notes FastAPI backend.

PUBLIC_INTERFACE
This script launches the ASGI server using uvicorn and binds to the expected host/port
for the preview system. It defaults to 0.0.0.0:3001, but can be configured via env:

- HOST: Host interface to bind to. Default: 0.0.0.0
- PORT: Port to bind to. Default: 3001

Usage:
    python run.py
    HOST=127.0.0.1 PORT=3001 python run.py
"""
import os
import sys

def main() -> int:
    """Entrypoint that initializes uvicorn to serve src.api.main:app."""
    try:
        import uvicorn  # type: ignore
    except Exception as exc:
        # Provide a helpful error if uvicorn isn't installed
        sys.stderr.write(f"[run.py] Error: uvicorn is required to run the server. {exc}\n")
        return 1

    host = os.getenv("HOST", "0.0.0.0")
    port_str = os.getenv("PORT", "3001")
    try:
        port = int(port_str)
    except ValueError:
        port = 3001

    uvicorn.run("src.api.main:app", host=host, port=port, reload=False, factory=False)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
