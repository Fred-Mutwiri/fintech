"""
Database request/response schemas.

These structures represent the HTTP contract between
FastAPI and the Elixir RDBMS.

They are intentionally minimal and do not model domain entities.
"""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class SQLQuery:
    """
    Represents a raw SQL string sent to the database.

    SQL construction must happen elsewhere.
    """
    statement: str


@dataclass(frozen=True)
class SQLResponse:
    """
    Represents a structured response from the database service.
    """
    success: bool
    data: Any | None
    error: str | None
