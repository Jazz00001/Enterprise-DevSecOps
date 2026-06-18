"""Security regression tests for the hardened reference app."""
from __future__ import annotations

import importlib
import sys
from pathlib import Path
from typing import Any

import pytest
from flask.testing import FlaskClient

REPO_ROOT = Path(__file__).resolve().parents[1]
APP_DIR = REPO_ROOT / "src" / "app"


@pytest.fixture(scope="session", autouse=True)
def add_app_to_python_path() -> None:
    app_path = str(APP_DIR)
    if app_path not in sys.path:
        sys.path.insert(0, app_path)


@pytest.fixture(scope="session")
def flask_app() -> Any:
    module = importlib.import_module("app_hardened")
    application = module.app
    application.config.update(TESTING=True)
    return application


@pytest.fixture()
def client(flask_app: Any) -> FlaskClient:
    return flask_app.test_client()


def test_hardened_user_route_rejects_sql_injection_payload(client: FlaskClient) -> None:
    response = client.get("/user", query_string={"id": "1' OR '1'='1"})
    assert response.status_code == 400
    assert response.get_json()["error"] == "id must be an integer"


def test_hardened_user_route_uses_parameterized_query(client: FlaskClient) -> None:
    response = client.get("/user?id=1")
    data = response.get_json()
    assert response.status_code == 200
    assert data["query_type"] == "parameterized"
    assert len(data["result"]) == 1


def test_hardened_ping_rejects_command_injection_payload(client: FlaskClient) -> None:
    response = client.get("/ping", query_string={"host": "127.0.0.1; echo PWNED"})
    assert response.status_code == 400
    assert response.get_json()["error"] == "invalid host"


def test_hardened_hello_escapes_template_expression(client: FlaskClient) -> None:
    response = client.get("/hello", query_string={"name": "{{7*7}}"})
    body = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "49" not in body
    assert "{{7*7}}" in body


def test_hardened_security_headers_exist(client: FlaskClient) -> None:
    response = client.get("/")
    for header in [
        "X-Content-Type-Options",
        "X-Frame-Options",
        "Content-Security-Policy",
        "Referrer-Policy",
        "Permissions-Policy",
        "Cache-Control",
    ]:
        assert header in response.headers
