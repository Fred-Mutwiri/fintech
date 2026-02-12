import pytest
from unittest.mock import patch
from app.infrastructure.db.client import DatabaseClient
from app.infrastructure.db.schemas import SQLQuery


def test_execute_success():
    client = DatabaseClient()

    with patch("httpx.post") as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "success": True,
            "data": [],
            "error": None,
        }

        response = client.execute(SQLQuery("SELECT * FROM test"))

        assert response.success is True
        assert response.data == []


def test_execute_non_200():
    client = DatabaseClient()

    with patch("httpx.post") as mock_post:
        mock_post.return_value.status_code = 500
        mock_post.return_value.json.return_value = {}

        with pytest.raises(Exception):
            client.execute(SQLQuery("SELECT * FROM test"))
