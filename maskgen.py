"""
maskgen.py — MASKGEN core CLI.
Starts the threaded Flask redirect server, manages URL generation,
and renders the interactive analytics table.
"""

import os
import sys
import time
import socket
import argparse
import threading
import json
import webbrowser
import subprocess

import database
import redirect_server
from utils import generate_code, is_valid_url, get_local_ip

# --- PERSISTENT CONFIGURATION ---
CONFIG_FILE = "maskgen_config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_config(cfg):
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=4)

# --- CONFIGURATION DEFAULTS ---
_cfg = load_config()
HOST = _cfg.get("host", "0.0.0.0")
PORT = _cfg.get("port", 5000)
LAN_IP = get_local_ip()
PUBLIC_URL = _cfg.get("public_url", None)

# --- ANSI COLOR HELPERS ---
R  = "\033[1;31m"   # Bold Red
G  = "\033[1;32m"   # Bold Green
B  = "\033[1;34m"   # Bold Blue
Y  = "\033[1;33m"   # Bold Yellow
C  = "\033[1;36m"   # Bold Cyan
W  = "\033[0m"      # Reset

# --- UX HELPERS ---
def copy_to_clipboard(text: str):
    """Attempt to copy text to clipboard using platform tools."""
    try:
        if sys.platform == 'linux':
            # Try xclip first, then xsel
            for cmd in [['xclip', '-selection', 'clipboard'], ['xsel', '-ib']]:
                try:
                    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
                    proc.communicate(input=text.encode('utf-8'))
                    if proc.returncode == 0: return True
                except: continue
        
        # Fallback to pyperclip if installed
        import pyperclip
        pyperclip.copy(text)
        return True
    except:
        return False

def open_url(url: str):
    """Open a URL in the default browser."""
    try:
        webbrowser.open(url)
        return True
    except:
        return False

# ---------------------------------------------------------------------------
# DISPLAY HELPERS
# ---------------------------------------------------------------------------

def clear():
    os.system("clear")

def banner():
    listener = f"{HOST}:{PORT}" if not PUBLIC_URL else PUBLIC_URL
    print(f"""
{R}    ███╗   ███╗ █████╗ ███████╗██╗  ██╗ ██████╗ ███████╗███╗   ██╗
    ████╗ ████║██╔══██╗██╔════╝██║ ██╔╝██╔════╝ ██╔════╝████╗  ██║
    ██╔████╔██║███████║███████╗█████╔╝ ██║  ███╗█████╗  ██╔██╗ ██║
    ██║╚██╔╝██║██╔══██║╚════██║██╔═██╗ ██║   ██║██╔══╝  ██║╚██╗██║
    ██║ ╚═╝ ██║██║  ██║███████║██║  ██╗╚██████╔╝███████╗██║ ╚████║
    ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝{W}
    {G}[ Framework Active | Listener: {listener} ]{W}""")
    
    if not PUBLIC_URL:
        if ".23." in LAN_IP or ".17." in LAN_IP:
            print(f"    {R}[!] WSL2 IP detected ({LAN_IP}). Phone may not reach it.{W}")
    else:
        print(f"    {G}[+] Tunnel Active: {PUBLIC_URL}{W}")
    print()

def display_help():
    print(f"""
{R}MASKGEN — USAGE GUIDE{W}
{'-'*59}
{C}DESCRIPTION:{W}
    Advanced URL masking tool exploiting RFC 3986 @-syntax.

{C}COMMANDS:{W}
    {G}python3 maskgen.py{W}          Launch interactive CLI
    {G}python3 maskgen.py --help{W}   Display this manual
    {G}python3 maskgen.py --url URL{W} Use public tunnel URL (saves to config)

{C}INTERACTIVE MENU OPTIONS:{W}
    {Y}1. Create Masked URL{W}   →  Enter target + mask, get @-URL
    {Y}2. View Analytics{W}      →  List all links & pick one to Copy/Open
    {Y}3. Settings{W}            →  Change HOST/PORT or PUBLIC_URL
    {Y}4. Delete a Link{W}       →  Remove a link by ID
    {Y}5. Exit{W}
{'-'*59}
""")

def main_menu() -> str:
    banner()
    print(f"    {Y}1.{W} Create Masked URL")
    print(f"    {Y}2.{W} View Analytics / Manage Links")
    print(f"    {Y}3.{W} Settings")
    print(f"    {Y}4.{W} Delete a Link")
    print(f"    {Y}5.{W} Exit\n")
    return input(f"{G}raptor @maskgen.db{W}:~$ ").strip()

# ---------------------------------------------------------------------------
# FEATURE: SETTINGS
# ---------------------------------------------------------------------------

def manage_settings():
    global HOST, PORT, PUBLIC_URL
    clear()
    banner()
    print(f"{C}[ Settings — Persistent ]{W}\n")
    print(f"  {Y}1.{W} Change Host (Current: {HOST})")
    print(f"  {Y}2.{W} Change Port (Current: {PORT})")
    print(f"  {Y}3.{W} Public Tunnel URL (Current: {PUBLIC_URL or 'None'})")
    print(f"  {Y}4.{W} Back to Menu\n")
    
    choice = input(f"{G}Settings{W}: ").strip()
    if choice == "1":
        HOST = input(f"  {Y}New Host{W}: ").strip() or HOST
    elif choice == "2":
        raw = input(f"  {Y}New Port{W}: ").strip()
        if raw.isdigit(): PORT = int(raw)
    elif choice == "3":
        PUBLIC_URL = input(f"  {Y}New Tunnel URL{W} (e.g. https://xyz.serveo.net): ").strip() or None
    else:
        return

    save_config({"host": HOST, "port": PORT, "public_url": PUBLIC_URL})
    print(f"\n  {G}[+] Settings saved to {CONFIG_FILE}.{W}")
    input("  Press Enter to continue...")

# ---------------------------------------------------------------------------
# FEATURE: CREATE MASKED URL
# ---------------------------------------------------------------------------

def create_masked_url():
    clear()
    banner()
    print(f"{C}[ Create Masked URL ]{W}\n")

    while True:
        target = input(f"  {Y}Target URL{W}: ").strip()
        if is_valid_url(target): break
        print(f"  {R}[!] Invalid URL (must start with http/https){W}")

    mask = input(f"  {Y}Mask Domain{W}: ").strip().replace("http://", "").replace("https://", "").rstrip("/") or "google.com"

    # Generate unique code
    for _ in range(5):
        code = generate_code(length=7)
        link_id = database.save_link(mask, target, code)
        if link_id: break
    else:
        print(f"\n  {R}[!] DB Error generating code.{W}")
        return

    # Generate URLs
    if PUBLIC_URL:
        scheme = "https://" if PUBLIC_URL.startswith("https") else "http://"
        base = PUBLIC_URL.replace("http://", "").replace("https://", "").rstrip("/")
        masked_url = f"{scheme}{mask}@{base}/{code}"
    else:
        masked_url = f"http://{mask}@{LAN_IP if LAN_IP != '127.0.0.1' else '127.0.0.1'}:{PORT}/{code}"

    print(f"\n  {G}[+] Masked URL Generated:{W}")
    print(f"      {B}{masked_url}{W}\n")
    
    # Auto-copy
    if copy_to_clipboard(masked_url):
        print(f"  {C}[i] Link copied to clipboard automatically.{W}")

    print(f"\n  {Y}[Actions]{W}")
    print(f"    [O] Open in Browser  |  [Enter] Back to Menu")
    
    action = input(f"\n  Choice: ").strip().lower()
    if action == 'o':
        open_url(masked_url)

# ---------------------------------------------------------------------------
# FEATURE: VIEW ANALYTICS
# ---------------------------------------------------------------------------

def view_analytics():
    while True:
        clear()
        banner()
        print(f"{C}[ Analytics — All Links ]{W}\n")

        links = database.get_all_links()
        if not links:
            print(f"  {Y}[i] No links found.{W}")
            input(f"\n  Press Enter to continue...")
            return

        col = {"id": 3, "mask": 20, "code": 9, "clicks": 6, "last": 19}
        header = (f"  {Y}{'ID':<{col['id']}} │ {'Mask':<{col['mask']}} │ "
                  f"{'Code':<{col['code']}} │ {'Hits':<{col['clicks']}} │ {'Last Hit':<{col['last']}}{W}")
        print(header)
        print(f"  {'─'*col['id']}─┼─{'─'*col['mask']}─┼─{'─'*col['code']}─┼─{'─'*col['clicks']}─┼─{'─'*col['last']}─")

        for row in links:
            print(f"  {row['id']:<{col['id']}} │ {row['mask_text'][:col['mask']]:<{col['mask']}} │ "
                  f"{row['redirect_code']:<{col['code']}} │ {G}{row['clicks']:<{col['clicks']}}{W} │ "
                  f"{row['last_accessed'] or '—':<{col['last']}}")

        print(f"\n  {Y}[Manage ID]{W} Enter ID to [C]opy or [O]pen link | [Enter] Back")
        raw = input(f"\n  ID: ").strip().lower()
        if not raw: break
        
        # Parse choice like "7c" or "7o"
        target_id = "".join(filter(str.isdigit, raw))
        if not target_id: continue
        
        row = next((r for r in links if str(r["id"]) == target_id), None)
        if not row: continue

        # Reconstruct URL
        if PUBLIC_URL:
            scheme = "https://" if PUBLIC_URL.startswith("https") else "http://"
            base = PUBLIC_URL.replace("http://", "").replace("https://", "").rstrip("/")
            link = f"{scheme}{row['mask_text']}@{base}/{row['redirect_code']}"
        else:
            link = f"http://{row['mask_text']}@{LAN_IP}:{PORT}/{row['redirect_code']}"

        if 'o' in raw:
            open_url(link)
            print(f"  {G}[+] Opened ID {target_id}.{W}")
            time.sleep(1)
        elif 'c' in raw or True: # Default to copy
            if copy_to_clipboard(link):
                print(f"  {G}[+] Copied ID {target_id} to clipboard.{W}")
                time.sleep(1)

# ---------------------------------------------------------------------------
# FEATURE: DELETE A LINK
# ---------------------------------------------------------------------------

def delete_link():
    clear()
    banner()
    print(f"{C}[ Delete a Link ]{W}\n")
    links = database.get_all_links()
    if not links: return

    for row in links:
        print(f"  {Y}[{row['id']}]{W} {row['mask_text'][:30]}  →  {row['redirect_code']}")

    raw = input(f"\n  ID to delete (or Enter): ").strip()
    if raw.isdigit() and database.delete_link(int(raw)):
        print(f"\n  {G}[+] Deleted.{W}")
        time.sleep(1)

# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--help", "-h", action="store_true")
    parser.add_argument("--url", type=str)
    args = parser.parse_args()

    if args.help:
        display_help()
        sys.exit(0)

    global PUBLIC_URL
    if args.url:
        PUBLIC_URL = args.url
        save_config({"host": HOST, "port": PORT, "public_url": PUBLIC_URL})

    database.init_db()

    # Background Server
    server_thread = threading.Thread(
        target=redirect_server.run_server,
        kwargs={"host": HOST, "port": PORT},
        daemon=True
    )
    server_thread.start()

    # Wait for server
    for _ in range(50):
        try:
            with socket.create_connection((HOST if HOST != "0.0.0.0" else "127.0.0.1", PORT), timeout=0.1):
                break
        except: time.sleep(0.1)

    while True:
        clear()
        choice = main_menu()
        if choice == "1": create_masked_url()
        elif choice == "2": view_analytics()
        elif choice == "3": manage_settings()
        elif choice == "4": delete_link()
        elif choice == "5": break

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: sys.exit(0)
