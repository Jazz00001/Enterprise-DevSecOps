from flask import Flask, request, jsonify, Response
from markupsafe import escape
import ipaddress
import os
import re
import sqlite3
import subprocess

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")


@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Cache-Control"] = "no-store"
    response.headers["Content-Security-Policy"] = "default-src 'self'; frame-ancestors 'none'; base-uri 'self'"
    return response


@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "hardened-flask-app"
    })


@app.route("/")
def home():
    return Response(
        """
        <h1>Enterprise DevSecOps Hardened Flask App</h1>
        <p>This is the remediated application used by Dockerfile.hardened.</p>
        """,
        mimetype="text/html"
    )


def is_valid_user_id(value: str) -> bool:
    return value.isdigit() and 1 <= int(value) <= 999999


@app.route("/user")
def get_user():
    user_id = request.args.get("id", "1")

    if not is_valid_user_id(user_id):
        return jsonify({
            "error": "Invalid user id. Only numeric IDs are allowed."
        }), 400

    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, username, role FROM users WHERE id = ?",
        (user_id,)
    )

    result = cursor.fetchall()
    conn.close()

    return jsonify({
        "query_type": "parameterized",
        "result": result
    })


def is_valid_host(host: str) -> bool:
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        pass

    hostname_pattern = re.compile(
        r"^(?=.{1,253}$)(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.(?!-)[A-Za-z0-9-]{1,63}(?<!-))*$"
    )

    return bool(hostname_pattern.fullmatch(host))


@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")

    if not is_valid_host(host):
        return jsonify({
            "error": "Invalid host. Only valid IP addresses or hostnames are allowed."
        }), 400

    result = subprocess.run(
        ["ping", "-c", "1", host],
        shell=False,
        capture_output=True,
        text=True,
        timeout=5
    )

    safe_output = escape(result.stdout + "\n" + result.stderr)

    return Response(f"<pre>{safe_output}</pre>", mimetype="text/html")


@app.route("/hello")
def hello():
    name = request.args.get("name", "guest")
    safe_name = escape(name)

    return Response(f"<h1>Hello {safe_name}</h1>", mimetype="text/html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
