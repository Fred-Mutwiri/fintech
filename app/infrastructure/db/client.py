"""
Database client module.

This module is the exclusive integration point between
the FastAPI application and the Elixir RDBMS.

Responsibilities:
- Execute SQL statements over HTTP
- Enforce request timeouts
- Log interactions
- Translate HTTP errors into typed infrastructure exceptions

Non-responsibilities:
- SQL construction
- Business logic
- Retry semantics
- Transaction handling
"""

import httpx
import logging

from app.config.settings import load_settings
from .schemas import SQLQuery, SQLResponse
from .exceptions import (
    DatabaseClientError,
    DatabaseConnectionError,
    DatabaseTimeoutError,
    DatabaseResponseError,
)

settings = load_settings()
logger = logging.getLogger(__name__)


class DatabaseClient:
    """
    Thin HTTP client for interacting with the Elixir RDBMS.

    This client assumes:
    - Each SQL execution is atomic on the database side
    - No transaction semantics exist
    - Network failures may occur independently of DB success
    """

    def __init__(self) -> None:
        self._base_url = settings.db_base_url
        self._timeout = settings.db_timeout_seconds

    def execute(self, query: SQLQuery) -> SQLResponse:
        """
        Execute a SQL statement against the database service.
        """

        url = f"{self._base_url}/execute"

        try:
            response = httpx.post(
                url,
                json={"sql": query.statement},
                timeout=self._timeout,
            )

        except httpx.ConnectError as exc:
            logger.error("Database connection failed")
            raise DatabaseConnectionError() from exc

        except httpx.TimeoutException as exc:
            logger.error("Database request timed out")
            raise DatabaseTimeoutError() from exc

        if response.status_code != 200:
            logger.error(
                "Database returned non-200 response",
                extra={"status_code": response.status_code},
            )
            raise DatabaseResponseError(
                f"Database returned {response.status_code}"
            )

        try:
            payload = response.json()
        except ValueError as exc:
            logger.error("Invalid JSON response from database")
            raise DatabaseResponseError("Malformed JSON response") from exc

        return SQLResponse(
            success=payload.get("success", False),
            data=payload.get("data"),
            error=payload.get("error"),
        )
