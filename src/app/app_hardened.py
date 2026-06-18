"""Hardened reference implementation for remediation proof.

This file intentionally exists beside app.py. app.py is the vulnerable lab target;
this file demonstrates how the same ideas should be implemented safely.
"""
from __future__ import annotations

import html
import ipaddress
import os
import re
import sqlite3
import subprocess
from pathlib import Path
from typing import Any

from flask import Flask, jsonify, request

app = Flask(__name__)
DB_PATH = Path(__file__).with_name("users.db")
HOSTNAME_PATTERN = re.compile(r"^[A-Za-z0-9.-]{1,253}$")


@app.after_request
def set_security_headers(response: Any) -> Any:
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "default-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    response.headers["Cache-Control"] = "no-store"
    return response


@app.route("/health")
def health() -> Any:
    return jsonify({"status": "ok", "service": "hardened-flask-app"})


@app.route("/")
def home() -> str:
    return """
    <h1>Enterprise DevSecOps Hardened Flask App</h1>
    <p>This reference app demonstrates secure remediations for the vulnerable lab.</p>
    <ul>
      <li>/user?id=1</li>
      <li>/ping?host=127.0.0.1</li>
      <li>/hello?name=Jagriti</li>
    </ul>
    """


@app.route("/user")
def get_user() -> Any:
    user_id_raw = request.args.get("id", "1")
    try:
        user_id = int(user_id_raw)
    except ValueError:
        return jsonify({"error": "id must be an integer"}), 400

    with sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True) as conn:
        cursor = conn.cursor()
        result = cursor.execute(
            "SELECT id, username, role FROM users WHERE id = ?",
            (user_id,),
        ).fetchall()

    return jsonify({"query_type": "parameterized", "result": result})


def validate_host(value: str) -> str | None:
    try:
        return str(ipaddress.ip_address(value))
    except ValueError:
        pass

    if not HOSTNAME_PATTERN.fullmatch(value):
        return None
    if ".." in value or value.startswith("-") or value.endswith("-"):
        return None
    return value


@app.route("/ping")
def ping() -> Any:
    host_raw = request.args.get("host", "127.0.0.1")
    host = validate_host(host_raw)
    if host is None:
        return jsonify({"error": "invalid host"}), 400

    try:
        result = subprocess.run(
            ["ping", "-c", "1", host],
            shell=False,
            capture_output=True,
            text=True,
            timeout=3,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return jsonify({"error": "ping timed out"}), 504

    return jsonify({"returncode": result.returncode, "stdout": result.stdout, "stderr": result.stderr})


@app.route("/hello")
def hello() -> str:
    name = request.args.get("name", "guest")[:80]
    return f"<h1>Hello {html.escape(name)}</h1>"


if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=5000, debug=debug_mode)
