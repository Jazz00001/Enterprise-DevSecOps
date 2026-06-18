"""
tests/test_routes.py

Enterprise DevSecOps Security Lab - Application Route and Vulnerability Behavior Tests
Author/Owner: Jagriti Banerjee

Purpose
-------
This module validates the expected behavior of the deliberately vulnerable Flask
application routes used in the Enterprise DevSecOps project.

The test strategy is split into two categories:

1. Functional route checks
   These ensure the lab routes respond consistently and can be used in CI/CD
   smoke testing, Docker validation, and Kubernetes readiness validation.

2. Controlled vulnerability demonstration checks
   These confirm that the intentional lab vulnerabilities are present and
   reproducible in a safe private environment. These tests are useful for
   evidence generation before remediation and for proving that secure fixes later
   remove the vulnerable behavior.

Important safety note
---------------------
The payloads used here are safe local test payloads. They do not target external
systems. They are intended only for the private DevSecOps lab application.

Recommended run command
-----------------------
  python -m pytest tests/test_routes.py -v
"""

from __future__ import annotations

import importlib
import sqlite3
import sys
from pathlib import Path
from typing import Any

import pytest
from flask.testing import FlaskClient


REPO_ROOT = Path(__file__).resolve().parents[1]
APP_DIR = REPO_ROOT / "src" / "app"
DB_PATH = APP_DIR / "users.db"


@pytest.fixture(scope="session", autouse=True)
def add_app_to_python_path() -> None:
    """Allow direct import of the Flask app from src/app/app.py."""

    app_path = str(APP_DIR)
    if app_path not in sys.path:
        sys.path.insert(0, app_path)


@pytest.fixture(scope="session", autouse=True)
def ensure_test_database() -> None:
    """Create the SQLite database required by the /user route if missing.

    The application includes src/app/init_db.py, but CI systems may run tests
    before a developer manually initializes the DB. This fixture keeps the route
    tests deterministic.
    """

    APP_DIR.mkdir(parents=True, exist_ok=True)

    if DB_PATH.exists():
        return

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            role TEXT NOT NULL
        )
        """
    )
    cur.executemany(
        "INSERT INTO users (id, username, role) VALUES (?, ?, ?)",
        [
            (1, "alice", "admin"),
            (2, "bob", "developer"),
            (3, "charlie", "intern"),
        ],
    )
    conn.commit()
    conn.close()


@pytest.fixture(scope="session")
def flask_app() -> Any:
    """Import and configure the Flask app for route testing."""

    try:
        module = importlib.import_module("app")
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Unable to import src/app/app.py as module 'app': {exc}")

    if not hasattr(module, "app"):
        pytest.fail("src/app/app.py must expose a Flask application variable named 'app'.")

    application = module.app
    application.config.update(TESTING=True)
    return application


@pytest.fixture()
def client(flask_app: Any) -> FlaskClient:
    """Create a Flask test client."""

    return flask_app.test_client()


def test_root_route_returns_lab_overview(client: FlaskClient) -> None:
    """The root route should provide a simple lab overview page."""

    response = client.get("/")
    body = response.get_data(as_text=True).lower()

    assert response.status_code == 200
    assert "devsecops" in body or "vulnerable" in body
    assert "/user" in body
    assert "/ping" in body
    assert "/hello" in body


def test_user_route_returns_expected_user_for_valid_id(client: FlaskClient) -> None:
    """A normal /user lookup should return the requested user record."""

    response = client.get("/user?id=1")
    payload = response.get_json(force=True)

    assert response.status_code == 200
    assert "query_used" in payload
    assert "result" in payload
    assert any("alice" in str(row).lower() for row in payload["result"]), (
        "Expected /user?id=1 to return the seeded alice/admin record."
    )


def test_user_route_defaults_to_id_1_when_missing_parameter(client: FlaskClient) -> None:
    """The /user route currently defaults to id=1 when no id is provided."""

    response = client.get("/user")
    payload = response.get_json(force=True)

    assert response.status_code == 200
    assert "result" in payload
    assert any("alice" in str(row).lower() for row in payload["result"])


def test_sql_injection_lab_payload_returns_multiple_users(client: FlaskClient) -> None:
    """Controlled proof that the intentionally vulnerable SQL route is injectable.

    Payload logic:
      id=1' OR '1'='1

    Expected vulnerable behavior:
      More than one user row is returned.

    After remediation with parameterized queries, this test should be changed to
    assert that only zero or one row is returned and that the injection string is
    treated as data rather than SQL syntax.
    """

    payload = "1' OR '1'='1"
    response = client.get("/user", query_string={"id": payload})
    data = response.get_json(force=True)

    assert response.status_code == 200
    assert "result" in data
    assert len(data["result"]) >= 2, (
        "The lab app is expected to demonstrate SQL injection by returning multiple rows. "
        "If this fails after remediation, update this test into a negative security regression test."
    )
    assert "OR" in data.get("query_used", "") or "or" in data.get("query_used", "")


def test_ping_route_accepts_normal_localhost_input(client: FlaskClient) -> None:
    """A normal local ping request should complete without a server error."""

    response = client.get("/ping?host=127.0.0.1")

    assert response.status_code == 200
    assert response.status_code < 500


def test_command_injection_lab_payload_executes_safe_marker_command(client: FlaskClient) -> None:
    """Controlled proof that the intentionally vulnerable ping route is injectable.

    Payload logic:
      127.0.0.1; echo DEVSECOPS_CMD_INJECTION_TEST

    This avoids destructive commands and only checks for a safe marker string.

    After remediation with shell=False and strict host validation, this test
    should be changed to assert that the marker string is not returned.
    """

    marker = "DEVSECOPS_CMD_INJECTION_TEST"
    payload = f"127.0.0.1; echo {marker}"

    response = client.get("/ping", query_string={"host": payload})
    body = response.get_data(as_text=True)

    assert response.status_code == 200
    assert marker in body, (
        "The lab app is expected to demonstrate command injection using a safe marker. "
        "If this fails after remediation, update this test into a negative security regression test."
    )


def test_hello_route_renders_normal_name(client: FlaskClient) -> None:
    """The /hello route should render a normal supplied name."""

    response = client.get("/hello?name=Jagriti")
    body = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "Hello Jagriti" in body


def test_template_injection_lab_payload_is_evaluated(client: FlaskClient) -> None:
    """Controlled proof that unsafe template rendering is present.

    Payload logic:
      {{7*7}}

    Expected vulnerable behavior:
      Jinja evaluates the expression and returns 49.

    After remediation, this test should be changed to assert that the literal
    string '{{7*7}}' is displayed safely or encoded.
    """

    response = client.get("/hello", query_string={"name": "{{7*7}}"})
    body = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "49" in body, (
        "The lab app is expected to demonstrate unsafe template rendering. "
        "If this fails after remediation, update this into a negative security regression test."
    )


@pytest.mark.parametrize(
    "path",
    [
        "/",
        "/health",
        "/user?id=1",
        "/ping?host=127.0.0.1",
        "/hello?name=SecurityTester",
    ],
)
def test_lab_routes_do_not_return_http_500(client: FlaskClient, path: str) -> None:
    """Core lab routes should not return server-side exceptions."""

    response = client.get(path)

    assert response.status_code < 500, f"Route {path} returned HTTP {response.status_code}."


def test_unknown_route_returns_404_not_500(client: FlaskClient) -> None:
    """Unknown routes should return 404 instead of leaking server errors."""

    response = client.get("/this-route-does-not-exist")

    assert response.status_code == 404
