"""
Database client exception definitions.

These exceptions isolate infrastructure failures from domain logic.
The rest of the application must not depend on HTTP semantics.
"""


class DatabaseClientError(Exception):
    """Base exception for all database client failures."""


class DatabaseConnectionError(DatabaseClientError):
    """Raised when the database service is unreachable."""


class DatabaseTimeoutError(DatabaseClientError):
    """Raised when the database request times out."""


class DatabaseResponseError(DatabaseClientError):
    """Raised when the database returns a non-success response."""
