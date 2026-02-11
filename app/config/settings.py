"""
    Application configuration management.

    this module defines strict environment parsing and validation.
    Configuration is immutable after load.
"""


import os
from dataclasses import dataclass



if os.environ.get("APP_ENV", "development") != "production":
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        # dotenv is optional; fail only if variables are missing later
        pass

class ConfigurationError(Exception):
    """Raised when configuration is invalid."""


@dataclass(frozen=True)
class Settings:
    app_env: str
    app_port: int
    db_base_url: str
    db_timeout_seconds: int
    jwt_secret: str
    jwt_algorithm: str

ALLOWED_ENVS = {"development", "staging", "production"}
ALLOWED_JWT_ALGORITHMS = {"HS256", "HS384", "HS512"}

def load_settings() -> Settings:
    try: 
        app_env = os.environ["APP_ENV"]
        app_port = int(os.environ["APP_PORT"])
        db_base_url = os.environ["DB_BASE_URL"]
        db_timeout_seconds = int(os.environ["DB_TIMEOUT_SECONDS"])
        jwt_secret = os.environ["JWT_SECRET"]
        jwt_algorithm = os.environ["JWT_ALGORITHM"]
    except KeyError as exc:
        raise ConfigurationError(f"Missing environment variable: {exc}") from exc

    if app_env not in ALLOWED_ENVS:
        raise ConfigurationError("Invalid APP_ENV")
    
    if app_port <= 0:
        raise ConfigurationError("APP_PORT must be positive")

    if not  db_base_url.startswith("http"):
        raise ConfigurationError("DB_BASE_URL must be valid URL")
    
    if db_timeout_seconds <= 0:
        raise ConfigurationError("DB_TIMEOUT_SECONDS must be positive")

    if not jwt_secret:
        raise ConfigurationError("JWT_SECRET must not be empty")
    
    if jwt_algorithm not in ALLOWED_JWT_ALGORITHMS:
        raise ConfigurationError("Unsupported JWT algorithm")

    if app_env == "production" and jwt_secret == "change_me":
        raise ConfigurationError("Insecure JWT secret in production")

    return Settings(
        app_env=app_env,
        app_port=app_port,
        db_base_url=db_base_url,
        db_timeout_seconds=db_timeout_seconds,
        jwt_secret=jwt_secret,
        jwt_algorithm=jwt_algorithm,
    )