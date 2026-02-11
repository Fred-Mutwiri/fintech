"""
    Application  entrypoint.

   Validates configuration at startup. no routes registered yet.

"""

from fastapi import FastAPI
from app.config.settings import load_settings, ConfigurationError

try: 
    settings = load_settings()

except ConfigurationError as exc: 
    raise SystemExit(f"Configuration error: {exc}")

app = FastAPI(title="Fintech Application")