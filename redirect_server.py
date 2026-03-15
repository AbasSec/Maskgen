from flask import Flask, redirect, abort
import database

app = Flask(__name__)

@app.route('/<code>')
def handle_redirect(code):
    target = database.get_target(code)
    if target:
        print(f"[*] Redirecting code {code} to {target}")
        return redirect(target, code=302)
    return "Link not found", 404

def run_server():
    print("[!] Starting Redirect Server on http://localhost:5000")
    app.run(port=5000, debug=False)

if __name__ == "__main__":
    run_server()
