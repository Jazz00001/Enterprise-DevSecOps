import pytest

from src.app.app_hardened import app


@pytest.fixture()
def client():
    app.config.update(TESTING=True)
    return app.test_client()


def test_hardened_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"
    assert data["runtime"] == "hardened"


def test_hardened_user_route_blocks_sql_injection(client):
    response = client.get("/user?id=1 OR 1=1")
    assert response.status_code == 400
    data = response.get_json()
    assert data["security_control"] == "input validation"


def test_hardened_user_route_uses_valid_id(client):
    response = client.get("/user?id=1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == 1
    assert data["security_control"] == "parameterized SQL query"


def test_hardened_ping_blocks_command_injection(client):
    response = client.get("/ping?host=localhost;cat /etc/passwd")
    assert response.status_code == 400
    data = response.get_json()
    assert data["security_control"] == "input validation and no shell execution"


def test_hardened_hello_does_not_execute_template_expression(client):
    response = client.get("/hello?name={{7*7}}")
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "49" not in body
    assert "{{7*7}}" in body or "&#123;&#123;7*7&#125;&#125;" in body


def test_hardened_security_headers_present(client):
    response = client.get("/health")
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["Referrer-Policy"] == "no-referrer"
    assert "default-src" in response.headers["Content-Security-Policy"]
