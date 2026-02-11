import os
import pytest
from app.config.settings import load_settings, ConfigurationError

def set_valid_env():
    os.environ["APP_ENV"] = "development"
    os.environ["APP_PORT"] = "8000"
    os.environ["DB_BASE_URL"] = "http://localhost:4000"
    os.environ["DB_TIMEOUT_SECONDS"] = "5"
    os.environ["JWT_SECRET"] = "supersecret"
    os.environ["JWT_ALGORITHM"] = "HS256"

def test_valid_configuration():
    set_valid_env()
    settings = load_settings()
    assert settings.app_env == "development"

def test_missing_variable():
    os.environ.clear()
    with pytest.raises(ConfigurationError):
        load_settings()

def test_invalid_environment():
    set_valid_env()
    os.environ["APP_ENV"] = "invalid"
    with pytest.raises(ConfigurationError):
        load_settings()


def test_insecure_production_secret():
    set_valid_env()
    os.environ["APP_ENV"] = "production"
    os.environ["JWT_SECRET"] = "change_me"
    with pytest.raises(ConfigurationError):
        load_settings()