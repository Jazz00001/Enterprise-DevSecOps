"""
tests/test_security_headers.py

Enterprise DevSecOps Security Lab - HTTP Security Header Tests
Author/Owner: Jagriti Banerjee

Purpose
-------
This module validates whether the Flask application returns baseline HTTP
security headers expected in an enterprise web application.

These tests are intentionally strict because they are designed to operate as a
security regression suite and CI/CD quality gate. If the current vulnerable lab
application does not yet implement these headers, the failing tests represent a
clear remediation backlog item.

Security headers covered
------------------------
- X-Content-Type-Options
- X-Frame-Options
- Content-Security-Policy
- Referrer-Policy
- Permissions-Policy
- Cache-Control for sensitive/dynamic routes
- Server header minimization guidance

Recommended implementation pattern in Flask
-------------------------------------------
Add an after_request hook in src/app/app.py:

    @app.after_request
    def set_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Content-Security-Policy"] = "default-src 'self'; frame-ancestors 'none'; base-uri 'self'"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        response.headers["Cache-Control"] = "no-store"
        return response

Recommended run command
-----------------------
  python -m pytest tests/test_security_headers.py -v
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path
from typing import Any, Iterable

import pytest
from flask.testing import FlaskClient


REPO_ROOT = Path(__file__).resolve().parents[1]
APP_DIR = REPO_ROOT / "src" / "app"


@pytest.fixture(scope="session", autouse=True)
def add_app_to_python_path() -> None:
    """Allow direct import of the Flask app from src/app/app.py."""

    app_path = str(APP_DIR)
    if app_path not in sys.path:
        sys.path.insert(0, app_path)


@pytest.fixture(scope="session")
def flask_app() -> Any:
    """Import and configure the Flask application for security header tests."""

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
    """Create Flask test client."""

    return flask_app.test_client()


def get_header(response: Any, header_name: str) -> str:
    """Return a header value or an empty string for simpler assertions."""

    return response.headers.get(header_name, "")


def assert_header_present(response: Any, header_name: str) -> None:
    """Assert a security header exists with a helpful remediation message."""

    assert header_name in response.headers, (
        f"Missing security header: {header_name}. Add a Flask after_request hook "
        f"to set {header_name} consistently on dynamic responses."
    )


@pytest.mark.parametrize("path", ["/", "/health", "/hello?name=Jagriti"])
def test_x_content_type_options_nosniff(client: FlaskClient, path: str) -> None:
    """X-Content-Type-Options should be nosniff.

    Security value:
      Helps prevent browsers from MIME-sniffing a response into an unexpected
      executable content type.
    """

    response = client.get(path)
    assert_header_present(response, "X-Content-Type-Options")
    assert get_header(response, "X-Content-Type-Options").lower() == "nosniff"


@pytest.mark.parametrize("path", ["/", "/hello?name=Jagriti"])
def test_x_frame_options_blocks_clickjacking(client: FlaskClient, path: str) -> None:
    """X-Frame-Options should prevent clickjacking.

    Recommended enterprise values:
      DENY or SAMEORIGIN
    """

    response = client.get(path)
    assert_header_present(response, "X-Frame-Options")

    value = get_header(response, "X-Frame-Options").upper()
    assert value in {"DENY", "SAMEORIGIN"}, (
        "X-Frame-Options must be DENY or SAMEORIGIN to reduce clickjacking risk."
    )


def test_content_security_policy_is_present(client: FlaskClient) -> None:
    """Content-Security-Policy should be present on HTML responses.

    Security value:
      Reduces risk from XSS and unsafe content loading. For this lab, a strict
      baseline policy is acceptable because the app does not need external assets.
    """

    response = client.get("/")
    assert_header_present(response, "Content-Security-Policy")

    csp = get_header(response, "Content-Security-Policy").lower()
    assert "default-src" in csp, "CSP should include a default-src directive."
    assert "frame-ancestors" in csp or "x-frame-options" in [h.lower() for h in response.headers], (
        "CSP should include frame-ancestors or X-Frame-Options should be present."
    )


def test_content_security_policy_avoids_wildcard_defaults(client: FlaskClient) -> None:
    """CSP should not use overly permissive wildcard defaults."""

    response = client.get("/")
    assert_header_present(response, "Content-Security-Policy")

    csp = get_header(response, "Content-Security-Policy").lower().replace(" ", "")
    disallowed_fragments = [
        "default-src*",
        "script-src*",
        "object-src*",
    ]

    assert not any(fragment in csp for fragment in disallowed_fragments), (
        "Content-Security-Policy should not use wildcard directives for default-src, "
        "script-src, or object-src in this lab application."
    )


def test_referrer_policy_is_privacy_preserving(client: FlaskClient) -> None:
    """Referrer-Policy should limit unnecessary URL/referrer leakage."""

    response = client.get("/")
    assert_header_present(response, "Referrer-Policy")

    value = get_header(response, "Referrer-Policy").lower()
    allowed_values = {
        "no-referrer",
        "same-origin",
        "strict-origin",
        "strict-origin-when-cross-origin",
    }

    assert value in allowed_values, (
        f"Referrer-Policy should be one of {sorted(allowed_values)}, got: {value!r}."
    )


def test_permissions_policy_restricts_browser_features(client: FlaskClient) -> None:
    """Permissions-Policy should disable unused browser capabilities."""

    response = client.get("/")
    assert_header_present(response, "Permissions-Policy")

    value = get_header(response, "Permissions-Policy").lower()
    expected_restrictions = ["camera=()", "microphone=()", "geolocation=()"]

    missing = [restriction for restriction in expected_restrictions if restriction not in value]
    assert not missing, f"Permissions-Policy is missing expected restrictions: {missing}"


@pytest.mark.parametrize("path", ["/user?id=1", "/ping?host=127.0.0.1", "/hello?name=Jagriti"])
def test_dynamic_routes_have_no_store_cache_control(client: FlaskClient, path: str) -> None:
    """Dynamic routes should not be cached by default.

    Security value:
      Prevents sensitive or user-controlled responses from being stored in browser
      or proxy caches.
    """

    response = client.get(path)
    assert_header_present(response, "Cache-Control")

    cache_control = get_header(response, "Cache-Control").lower()
    assert "no-store" in cache_control or "no-cache" in cache_control, (
        "Dynamic routes should include Cache-Control: no-store or no-cache."
    )


def test_hsts_policy_when_https_is_used(client: FlaskClient) -> None:
    """HTTPS requests should include Strict-Transport-Security.

    In local HTTP-only development, HSTS may not appear. This test sends a request
    with HTTPS scheme to validate production behavior if ProxyFix/TLS termination
    support is implemented.
    """

    response = client.get("/", base_url="https://localhost")

    if "Strict-Transport-Security" not in response.headers:
        pytest.xfail(
            "HSTS is not configured yet. Add it when the app is served behind HTTPS/TLS termination."
        )

    hsts = get_header(response, "Strict-Transport-Security").lower()
    assert "max-age=" in hsts
    assert "includesubdomains" in hsts.replace("-", "") or "includeSubDomains" in get_header(response, "Strict-Transport-Security")


def test_server_header_should_not_disclose_detailed_framework_version(client: FlaskClient) -> None:
    """Server header should not disclose detailed framework versions.

    Flask's test client may not always expose a production Server header. If it is
    present, it should not contain detailed Werkzeug/Python versions.
    """

    response = client.get("/")
    server = get_header(response, "Server")

    if not server:
        return

    lower_server = server.lower()
    disallowed_terms = ["werkzeug/", "python/", "gunicorn/"]
    leaked = [term for term in disallowed_terms if term in lower_server]

    assert not leaked, f"Server header leaks implementation details: {leaked}"


def test_security_headers_are_consistent_across_core_routes(client: FlaskClient) -> None:
    """Core routes should receive the same baseline security headers."""

    required_headers: Iterable[str] = [
        "X-Content-Type-Options",
        "X-Frame-Options",
        "Content-Security-Policy",
        "Referrer-Policy",
        "Permissions-Policy",
    ]

    routes = ["/", "/health", "/hello?name=Jagriti", "/user?id=1", "/ping?host=127.0.0.1"]

    missing_by_route = {}
    for route in routes:
        response = client.get(route)
        missing = [header for header in required_headers if header not in response.headers]
        if missing:
            missing_by_route[route] = missing

    assert not missing_by_route, (
        "Security headers must be applied consistently across all core routes. "
        f"Missing headers by route: {missing_by_route}"
    )
