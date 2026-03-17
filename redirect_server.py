"""
redirect_server.py — MASKGEN threaded Flask redirect server.
"""

import logging
import os
from flask import Flask, redirect
import database

# Configure logging to a file
logging.basicConfig(
    filename='server.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)

# Silence Werkzeug console output
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@app.route("/<code>")
def handle_redirect(code: str):
    """
    Look up redirect_code in the database.
    """
    logging.info(f"Incoming request for code: {code}")
    target = database.get_target(code)
    
    if target:
        # Security: Prevent malicious non-HTTP schemes (like javascript:)
        # We only allow http:// or https://
        clean_target = target.strip()
        if not clean_target.lower().startswith(("http://", "https://")):
            # If no scheme, default to http
            clean_target = "http://" + clean_target
        
        # Final safety check
        if not clean_target.lower().startswith(("http://", "https://")):
            logging.error(f"Dangerous target detected and blocked: {target}")
            return "Security violation: Invalid URL scheme.", 400

        logging.info(f"Redirecting to: {clean_target}")
        return redirect(clean_target, code=302)
    
    logging.warning(f"No match for code: {code}")
    return "Invalid or expired link.", 404

@app.route("/health")
def health_check():
    return "OK", 200

def run_server(host: str = "0.0.0.0", port: int = 5000):
    """Start the Flask server."""
    logging.info(f"Starting server on {host}:{port}")
    app.run(
        host=host,
        port=port,
        debug=False,
        use_reloader=False,
    )

if __name__ == "__main__":
    database.init_db()
    run_server()
