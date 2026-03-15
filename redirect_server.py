"""
redirect_server.py — MASKGEN threaded Flask redirect server.
Handles all incoming /<code> requests, logs clicks via database.py,
and issues HTTP 302 redirects to the stored target URL.
"""

import logging
import os
from flask import Flask, redirect
import database

# --- Silence ALL Flask / Werkzeug output so nothing bleeds into the CLI ---
# Level CRITICAL means only fatal internal errors surface (practically nothing)
logging.getLogger("werkzeug").setLevel(logging.CRITICAL)
logging.getLogger("werkzeug").propagate = False

_devnull = open(os.devnull, "w")

app = Flask(__name__)

# Silence Flask's own internal logger too
app.logger.setLevel(logging.CRITICAL)
app.logger.propagate = False


@app.route("/<code>")
def handle_redirect(code: str):
    """
    Look up redirect_code in the database.
    On hit  → increment click counter and 302 to target.
    On miss → return a plain 404 with a short message.
    """
    target = database.get_target(code)
    if target:
        return redirect(target, code=302)
    return "Invalid or expired link.", 404


def run_server(host: str = "127.0.0.1", port: int = 5000):
    """Start the Flask server. Called from maskgen.py in a daemon thread."""
    app.run(
        host=host,
        port=port,
        debug=False,
        use_reloader=False,
    )


if __name__ == "__main__":
    # Allow direct invocation for testing: python3 redirect_server.py
    database.init_db()
    print(f"[!] Starting standalone redirect server on http://127.0.0.1:5000")
    run_server()
