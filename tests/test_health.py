"""
tests/test_health.py

Enterprise DevSecOps Security Lab - Health and Service Availability Tests
Author/Owner: Jagriti Banerjee

Purpose
-------
This test module validates the minimum operational health expectations for the
vulnerable Flask application used in the Enterprise DevSecOps project.

These tests are intentionally written like production CI/CD smoke tests:
- They verify that the Flask application can be imported safely.
- They verify that the /health endpoint exists and returns a successful status.
- They verify that the health response is machine-readable JSON.
- They verify that the endpoint remains lightweight and does not expose secrets.

Why this matters in DevSecOps
----------------------------
A reliable health endpoint is required before security gates, container checks,
Kubernetes readiness probes, liveness probes, and GitOps deployment validation can
be trusted. If /health is broken, the pipeline should fail early before deeper
security scans or deployment promotion.

Expected app structure
----------------------
Repository root:
  src/app/app.py

Flask application object:
  app = Flask(__name__)

Recommended run command
-----------------------
  python -m pytest tests/test_health.py -v
"""

from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path
from typing import Any, Dict

import pytest
from flask.testing import FlaskClient


REPO_ROOT = Path(__file__).resolve().parents[1]
APP_DIR = REPO_ROOT / "src" / "app"


@pytest.fixture(scope="session", autouse=True)
def add_app_to_python_path() -> None:
    """Ensure tests can import the Flask app from src/app/app.py.

    The project keeps application code under src/app instead of installing it as a
    package. Adding this directory to sys.path makes the tests work both locally
    and inside GitHub Actions without needing extra packaging steps.
    """

    app_path = str(APP_DIR)
    if app_path not in sys.path:
        sys.path.insert(0, app_path)


@pytest.fixture(scope="session")
def flask_app() -> Any:
    """Import and return the Flask application object.

    The test fails with a clear message if the module cannot be imported or if the
    expected Flask variable named `app` is missing.
    """

    try:
        module = importlib.import_module("app")
    except Exception as exc:  # pragma: no cover - pytest displays failure context
        pytest.fail(f"Unable to import src/app/app.py as module 'app': {exc}")

    if not hasattr(module, "app"):
        pytest.fail("src/app/app.py must expose a Flask application variable named 'app'.")

    application = module.app
    application.config.update(TESTING=True)
    return application


@pytest.fixture()
def client(flask_app: Any) -> FlaskClient:
    """Create a Flask test client for endpoint-level validation."""

    return flask_app.test_client()


def parse_json_response(response: Any) -> Dict[str, Any]:
    """Return parsed JSON with a helpful assertion message on failure."""

    try:
        return response.get_json(force=True)
    except Exception:
        pytest.fail(f"Expected JSON response, got body: {response.data!r}")


def test_health_endpoint_returns_http_200(client: FlaskClient) -> None:
    """The /health endpoint must be available and return HTTP 200.

    This validates the same endpoint used by Docker HEALTHCHECK and Kubernetes
    liveness/readiness probes.
    """

    response = client.get("/health")

    assert response.status_code == 200, (
        "The /health endpoint must return HTTP 200 so CI/CD, Docker, and "
        "Kubernetes probes can reliably confirm application readiness."
    )


def test_health_endpoint_returns_json_content_type(client: FlaskClient) -> None:
    """The /health endpoint should return JSON for automation compatibility."""

    response = client.get("/health")

    assert response.content_type.startswith("application/json"), (
        "The /health endpoint should return application/json so monitoring tools "
        "and automated deployment gates can parse it consistently."
    )


def test_health_endpoint_response_contract(client: FlaskClient) -> None:
    """Validate the expected /health response schema.

    Expected response example:
      {"status": "ok", "service": "vulnerable-flask-app"}
    """

    response = client.get("/health")
    payload = parse_json_response(response)

    assert "status" in payload, "Health response must include a 'status' field."
    assert payload["status"] == "ok", "Health status must be exactly 'ok'."

    assert "service" in payload, "Health response must include a 'service' field."
    assert isinstance(payload["service"], str), "Health service value must be a string."
    assert payload["service"].strip(), "Health service value must not be empty."


def test_health_endpoint_does_not_expose_sensitive_information(client: FlaskClient) -> None:
    """Health responses must not leak secrets or environment details.

    Health endpoints are often unauthenticated. They should provide only enough
    information for orchestration and monitoring systems, not sensitive runtime
    configuration.
    """

    response = client.get("/health")
    body = response.get_data(as_text=True).lower()

    forbidden_terms = [
        "secret",
        "password",
        "token",
        "private_key",
        "api_key",
        "connection_string",
        "sqlite://",
        "postgres://",
        "mysql://",
        "/etc/passwd",
        "/etc/shadow",
    ]

    leaked_terms = [term for term in forbidden_terms if term in body]
    assert not leaked_terms, f"Health endpoint appears to expose sensitive terms: {leaked_terms}"


def test_health_endpoint_uses_get_only_for_smoke_validation(client: FlaskClient) -> None:
    """GET /health should be the supported smoke-test method.

    POST is not required for health checks. The app may return 405 Method Not
    Allowed or another non-success status, but it should not perform state changes.
    """

    response = client.post("/health")

    assert response.status_code in {400, 404, 405}, (
        "POST /health should not be treated as a normal successful operation. "
        "A health endpoint should be read-only and should not accept state-changing methods."
    )


def test_homepage_is_available_for_lab_navigation(client: FlaskClient) -> None:
    """The root page should load so lab users can discover demo routes."""

    response = client.get("/")

    assert response.status_code == 200, "The root route should be available for lab navigation."
    body = response.get_data(as_text=True).lower()
    assert "devsecops" in body or "vulnerable" in body or "flask" in body, (
        "The root route should identify the lab application purpose."
    )


@pytest.mark.parametrize("path", ["/health", "/"])
def test_basic_routes_do_not_return_server_error(client: FlaskClient, path: str) -> None:
    """Basic operational routes must not return HTTP 5xx errors."""

    response = client.get(path)

    assert response.status_code < 500, f"{path} returned a server-side error: {response.status_code}"


def test_health_response_is_valid_json_serializable(client: FlaskClient) -> None:
    """The /health payload should be cleanly serializable by standard JSON tooling."""

    response = client.get("/health")
    payload = parse_json_response(response)

    try:
        json.dumps(payload)
    except TypeError as exc:
        pytest.fail(f"Health payload is not JSON serializable: {exc}")
