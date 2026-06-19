import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
APP_DIR = PROJECT_ROOT / "src" / "app"

sys.path.insert(0, str(APP_DIR))

from app_hardened import app


def test_health_endpoint_returns_hardened_app():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"
    assert response.get_json()["service"] == "hardened-flask-app"


def test_sql_injection_payload_is_rejected():
    client = app.test_client()

    response = client.get("/user?id=1'%20OR%20'1'%3D'1")

    assert response.status_code == 400
    assert b"Invalid user id" in response.data


def test_command_injection_payload_is_rejected():
    client = app.test_client()

    response = client.get("/ping?host=127.0.0.1%3Bwhoami")

    assert response.status_code == 400
    assert b"Invalid host" in response.data


def test_unsafe_rendering_is_escaped():
    client = app.test_client()

    response = client.get("/hello?name=<script>alert(1)</script>")

    assert response.status_code == 200
    assert b"&lt;script&gt;alert(1)&lt;/script&gt;" in response.data
    assert b"<script>alert(1)</script>" not in response.data


def test_security_headers_are_present():
    client = app.test_client()

    response = client.get("/health")

    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["Referrer-Policy"] == "no-referrer"
    assert "default-src 'self'" in response.headers["Content-Security-Policy"]
