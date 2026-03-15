import os
import re
import sqlite3
import string
import random
import threading
import logging
import argparse
import sys
from datetime import datetime
from flask import Flask, redirect

# --- CONFIGURATION ---
DB_NAME = "maskgen.db"
HOST = "127.0.0.1"
PORT = 5000

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# --- DATABASE LAYER ---
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mask_text TEXT,
            target_url TEXT,
            redirect_code TEXT UNIQUE,
            created_at TEXT,
            clicks INTEGER DEFAULT 0
        )''')

def save_link(mask, target, code):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("INSERT INTO links (mask_text, target_url, redirect_code, created_at) VALUES (?, ?, ?, ?)",
                     (mask, target, code, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

def get_target_and_update(code):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.execute("SELECT target_url FROM links WHERE redirect_code = ?", (code,))
        row = cursor.fetchone()
        if row:
            conn.execute("UPDATE links SET clicks = clicks + 1 WHERE redirect_code = ?", (code,))
            return row[0]
    return None

def get_all_links():
    with sqlite3.connect(DB_NAME) as conn:
        return conn.execute("SELECT * FROM links").fetchall()

# --- REDIRECT SERVER ---
@app.route('/<code>')
def handle_redirect(code):
    target = get_target_and_update(code)
    if target:
        return redirect(target, code=302)
    return "Invalid or Expired Link", 404

def start_server():
    app.run(host=HOST, port=PORT, debug=False, use_reloader=False)

# --- CLI LOGIC ---
def display_help():
    print(f"""
\033[1;31mMASKGEN — USAGE GUIDE\033[0m
-----------------------------------------------------------
\033[1mDESCRIPTION:\033[0m
    Advanced URL Masking tool using RFC 3986 @-syntax.
    Prepend a trusted domain to hide the real redirect host.

\033[1mCOMMANDS:\033[0m
    \033[92mpython3 maskgen.py\033[0m          Launch interactive CLI mode
    \033[92mpython3 maskgen.py --help\033[0m   Display this manual

\033[1mSTAGES OF OPERATION:\033[0m
    1. \033[94mGeneration:\033[0m Input Target URL and Mask Text.
    2. \033[94mDeployment:\033[0m Threaded Flask server listens on {HOST}:{PORT}.
    3. \033[94mMasking:\033[0m URL format is [Mask]@[Host]/[Code].
    4. \033[94mTracking:\033[0m Real-time click analytics stored in SQLite.

\033[1mLEGAL:\033[0m
    For authorized security research and CTF purposes only.
-----------------------------------------------------------
    """)

def main_menu():
    print(f"""
    \033[91m███╗   ███╗ █████╗ ███████╗██╗  ██╗ ██████╗ ███████╗███╗   ██╗
    ████╗ ████║██╔══██╗██╔════╝██║ ██╔╝██╔════╝ ██╔════╝████╗  ██║
    ██╔████╔██║███████║███████╗█████╔╝ ██║  ███╗█████╗  ██╔██╗ ██║
    ██║╚██╔╝██║██╔══██║╚════██║██╔═██╗ ██║   ██║██╔══╝  ██║╚██╗██║
    ██║ ╚═╝ ██║██║  ██║███████║██║  ██╗╚██████╔╝███████╗██║ ╚████║
    ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝\033[0m
    [ Framework Active | Listener: {HOST}:{PORT} ]
    
    1. Create Masked URL
    2. View Analytics
    3. Exit
    """)
    return input("\033[92mraptor@maskgen\033[0m:~$ ")

if __name__ == "__main__":
    # Setup Argument Parser
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--help', '-h', action='store_true')
    args = parser.parse_args()

    # Check for --help flag
    if args.help:
        display_help()
        sys.exit()

    # Start Tool
    init_db()
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    while True:
        os.system('clear')
        choice = main_menu()
        if choice == '1':
            target = input("\nTarget URL: ")
            mask = input("Mask Text: ")
            code = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(7))
            save_link(mask, target, code)
            print(f"\n\033[94m[+] Link: {mask}@{HOST}:{PORT}/{code}\033[0m")
            input("\nEnter to continue...")
        elif choice == '2':
            links = get_all_links()
            print(f"\n{'ID':<3} | {'Mask':<25} | {'Clicks':<6}")
            for l in links: print(f"{l[0]:<3} | {l[1][:23]:<25} | {l[5]:<6}")
            input("\nEnter to continue...")
        elif choice == '3':
            break
