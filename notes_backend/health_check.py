#!/usr/bin/env python3
"""
Simple health check script for the Notes backend.

PUBLIC_INTERFACE
Starts the server externally (or assumes it's running) and verifies that /health returns 200.
Usage:
    python health_check.py
"""
import sys
import time
import json
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

def check(url: str, attempts: int = 20, delay: float = 0.5) -> int:
    """Try fetching the given URL until success or attempts exhausted."""
    for _ in range(attempts):
        try:
            req = Request(url, method="GET")
            with urlopen(req, timeout=2) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode("utf-8"))
                    print(f"OK {resp.status}: {data}")
                    return 0
        except (URLError, HTTPError):
            time.sleep(delay)
    print("Health check failed")
    return 1

if __name__ == "__main__":
    sys.exit(check("http://localhost:3001/health"))
