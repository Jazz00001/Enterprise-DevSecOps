from flask import Flask, request, render_template_string
import sqlite3
import subprocess
import os

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")


@app.after_request
def set_security_headers(response):
    """Apply baseline defensive headers across lab routes.

    The app remains intentionally vulnerable for SQLi/command injection/SSTI demonstrations,
    but these headers make the HTTP layer closer to an enterprise baseline and keep
    regression tests meaningful.
    """
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'"
    )
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    response.headers["Cache-Control"] = "no-store"
    return response


@app.route("/health")
def health():
    return {"status": "ok", "service": "vulnerable-flask-app"}


@app.route("/")
def home():
    return """
    <h1>Enterprise DevSecOps Vulnerable Flask App</h1>
    <p>This app is intentionally vulnerable for private lab testing.</p>

    <h3>Test Routes</h3>
    <ul>
      <li>/user?id=1</li>
      <li>/ping?host=127.0.0.1</li>
      <li>/hello?name=Jagriti</li>
    </ul>
    """


@app.route("/user")
def get_user():
    user_id = request.args.get("id", "1")

    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    cursor = conn.cursor()

    query = f"SELECT id, username, role FROM users WHERE id = '{user_id}'"

    result = cursor.execute(query).fetchall()
    conn.close()

    return {
        "query_used": query,
        "result": result
    }


@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")

    result = subprocess.run(
        f"ping -c 1 {host}",
        shell=True,
        capture_output=True,
        text=True
    )

    return f"<pre>{result.stdout}\n{result.stderr}</pre>"


@app.route("/hello")
def hello():
    name = request.args.get("name", "guest")

    template = f"<h1>Hello {name}</h1>"
    return render_template_string(template)


if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=5000, debug=debug_mode)
