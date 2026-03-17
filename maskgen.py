"""
maskgen.py — MASKGEN core CLI.
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
import re
import signal
import select
import logging

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
        except Exception:
            return {}
    return {}

def save_config(cfg):
    current = load_config()
    current.update(cfg)
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(current, f, indent=4)
    except Exception as e:
        logging.error(f"Failed to save config: {e}")

# --- CONFIGURATION DEFAULTS ---
_cfg = load_config()
HOST = "0.0.0.0"
PORT = _cfg.get("port", 5000)
LAN_IP = get_local_ip()
PUBLIC_URL = _cfg.get("public_url", None)
TUNNEL_PROVIDER = _cfg.get("tunnel_provider", "serveo")
TUNNEL_PROC = None

# --- ANSI COLOR HELPERS ---
R  = "\033[1;31m"   # Bold Red
G  = "\033[1;32m"   # Bold Green
B  = "\033[1;34m"   # Bold Blue
Y  = "\033[1;33m"   # Bold Yellow
C  = "\033[1;36m"   # Bold Cyan
W  = "\033[0m"      # Reset

def copy_to_clipboard(text: str):
    """Copies text to system clipboard."""
    try:
        if sys.platform == 'linux':
            for cmd in [['xclip', '-selection', 'clipboard'], ['xsel', '-ib']]:
                try:
                    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
                    proc.communicate(input=text.encode('utf-8'))
                    if proc.returncode == 0: return True
                except Exception: continue
        
        import pyperclip
        pyperclip.copy(text)
        return True
    except Exception:
        return False

def open_url(url: str):
    """Opens URL in default web browser."""
    try:
        webbrowser.open(url)
        return True
    except Exception:
        return False

def cleanup_tunnel():
    """Kills background tunnel process group."""
    global TUNNEL_PROC, PUBLIC_URL
    if TUNNEL_PROC:
        try:
            os.killpg(os.getpgid(TUNNEL_PROC.pid), signal.SIGTERM)
        except Exception:
            try: TUNNEL_PROC.terminate()
            except Exception: pass
        TUNNEL_PROC = None
    PUBLIC_URL = None
    save_config({"public_url": None})

def drain_tunnel_output(pipe):
    """Logs background tunnel output to file."""
    try:
        with pipe:
            for line in iter(pipe.readline, ''):
                if line:
                    logging.info(f"Tunnel: {line.strip()}")
    except Exception:
        pass

def start_auto_tunnel():
    """Initializes SSH tunnel based on provider choice."""
    global PUBLIC_URL, TUNNEL_PROC, TUNNEL_PROVIDER
    cleanup_tunnel()
    
    print(f"  {Y}[*]{W} Initializing Global Tunnel ({TUNNEL_PROVIDER})...")
    
    if TUNNEL_PROVIDER == "localhost.run":
        cmd = ["ssh", "-n", "-o", "StrictHostKeyChecking=no", "-R", f"80:127.0.0.1:{PORT}", "nokey@localhost.run"]
        regex = r"https://[a-zA-Z0-9.-]+lhr\.life"
    else: # serveo
        cmd = ["ssh", "-n", "-o", "StrictHostKeyChecking=no", "-R", f"80:127.0.0.1:{PORT}", "serveo.net"]
        regex = r"https://[a-zA-Z0-9.-]+(serveo\.net|serveousercontent\.com)"
    
    try:
        TUNNEL_PROC = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            text=True, 
            bufsize=1,
            preexec_fn=os.setsid
        )
        
        start_time = time.time()
        while time.time() - start_time < 15:
            if TUNNEL_PROC.poll() is not None: break
            
            r, _, _ = select.select([TUNNEL_PROC.stdout], [], [], 0.5)
            if r:
                line = TUNNEL_PROC.stdout.readline()
                if not line: break
                match = re.search(regex, line)
                if match:
                    PUBLIC_URL = match.group(0)
                    save_config({"public_url": PUBLIC_URL})
                    threading.Thread(target=drain_tunnel_output, args=(TUNNEL_PROC.stdout,), daemon=True).start()
                    return True
        cleanup_tunnel()
        return False
    except Exception as e:
        logging.error(f"SSH Tunnel Error: {e}")
        return False

# ---------------------------------------------------------------------------
# DISPLAY HELPERS
# ---------------------------------------------------------------------------

def clear():
    os.system("clear")

def banner():
    listener = f"{LAN_IP}:{PORT}" if not PUBLIC_URL else PUBLIC_URL
    print(f"""
{R}    ███╗   ███╗ █████╗ ███████╗██╗  ██╗ ██████╗ ███████╗███╗   ██╗
    ████╗ ████║██╔══██╗██╔════╝██║ ██╔╝██╔════╝ ██╔════╝████╗  ██║
    ██╔████╔██║███████║███████╗█████╔╝ ██║  ███╗█████╗  ██╔██╗ ██║
    ██║╚██╔╝██║██╔══██║╚════██║██╔═██╗ ██║   ██║██╔══╝  ██║╚██╗██║
    ██║ ╚═╝ ██║██║  ██║███████║██║  ██╗╚██████╔╝███████╗██║ ╚████║
    ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝{W}
    {G}[ Framework Active | Listener: {listener} ]{W}""")
    
    if PUBLIC_URL:
        print(f"    {G}[+] Global Mode Active ({TUNNEL_PROVIDER}): {PUBLIC_URL}{W}")
    else:
        print(f"    {Y}[i] Local Mode (LAN only). Use Settings to go Global.{W}")
    print()

# ---------------------------------------------------------------------------
# MENU FEATURES
# ---------------------------------------------------------------------------

def manage_settings():
    global PUBLIC_URL, TUNNEL_PROVIDER
    clear()
    banner()
    print(f"{C}[ Settings & Maintenance ]{W}\n")
    print(f"  {Y}1.{W} Reset/Start Global Tunnel")
    print(f"  {Y}2.{W} Stop Global Tunnel (Back to LAN)")
    print(f"  {Y}3.{W} Switch Provider (Current: {TUNNEL_PROVIDER})")
    print(f"  {Y}4.{W} View Server Logs (server.log)")
    print(f"  {Y}5.{W} Back to Menu\n")
    
    choice = input(f"{G}Settings{W}: ").strip()
    if choice == "1":
        if start_auto_tunnel():
            print(f"  {G}[+] Tunnel Active: {PUBLIC_URL}{W}")
        else:
            print(f"  {R}[!] Tunnel Failed. See server.log{W}")
    elif choice == "2":
        cleanup_tunnel()
        print(f"  {G}[+] Tunnel stopped.{W}")
    elif choice == "3":
        print(f"\n  {Y}[ Tunnel Providers ]{W}")
        print(f"    1. Serveo (serveo.net)")
        print(f"    2. Localhost.run (lhr.life)")
        p_choice = input(f"\n  Choice [1/2]: ").strip()
        TUNNEL_PROVIDER = "localhost.run" if p_choice == "2" else "serveo"
        save_config({"tunnel_provider": TUNNEL_PROVIDER})
        print(f"  {G}[+] Switched to {TUNNEL_PROVIDER}.{W}")
        if PUBLIC_URL: start_auto_tunnel()
    elif choice == "4":
        if os.path.exists("server.log"): os.system("tail -n 30 server.log")
        else: print("  [!] No logs found.")
    else: return
    input("\n  Press Enter to continue...")

def create_masked_url():
    clear()
    banner()
    print(f"{C}[ Create Masked URL ]{W}\n")

    target = ""
    while not is_valid_url(target):
        target = input(f"  {Y}Target URL{W}: ").strip()
        if not is_valid_url(target):
            print(f"  {R}[!] Invalid URL (must include http/https).{W}")

    mask = input(f"  {Y}Mask Domain{W} (e.g. google.com): ").strip()
    mask = mask.replace("http://", "").replace("https://", "").rstrip("/") or "google.com"

    use_global = False
    if PUBLIC_URL:
        print(f"\n  {Y}[ Connection Mode ]{W}")
        print(f"    {G}1.{W} Global Mode ({PUBLIC_URL})")
        print(f"    {G}2.{W} Local Mode  ({LAN_IP}:{PORT})")
        m_choice = input(f"\n  Choice [1/2]: ").strip()
        use_global = (m_choice != "2")
    else:
        go_global = input(f"\n  {Y}Make this link Global?{W} [y/N]: ").strip().lower()
        if go_global == 'y':
            if start_auto_tunnel():
                use_global = True
            else:
                print(f"  {R}[!] Tunnel failed. Using Local.{W}")

    code = generate_code(7)
    while database.save_link(mask, target, code) is None:
        code = generate_code(7)

    if use_global and PUBLIC_URL:
        base = PUBLIC_URL.replace("https://", "").replace("http://", "").rstrip("/")
        masked_url = f"https://{mask}@{base}/{code}"
        clean_url = f"https://{base}/{code}"
    else:
        host = LAN_IP if LAN_IP != "127.0.0.1" else "127.0.0.1"
        masked_url = f"http://{mask}@{host}:{PORT}/{code}"
        clean_url = f"http://{host}:{PORT}/{code}"

    print(f"\n  {G}[+] URLs Generated:{W}")
    print(f"      {C}Masked:{W} {B}{masked_url}{W}")
    print(f"      {C}Clean: {W} {clean_url}\n")
    
    to_copy = clean_url if use_global else masked_url
    if copy_to_clipboard(to_copy):
        print(f"  {C}[i] Link copied to clipboard.{W}")

    print(f"  {Y}[Actions]{W} [O] Open Clean | [M] Open Masked | [Enter] Menu")
    act = input(f"  Choice: ").strip().lower()
    if act == 'o': open_url(clean_url)
    elif act == 'm': open_url(masked_url)

def view_analytics():
    while True:
        clear()
        banner()
        print(f"{C}[ Analytics Dashboard ]{W}\n")
        links = database.get_all_links()
        if not links:
            print("  [i] No links found."); input("\n  Enter..."); return

        print(f"  {Y}{'ID':<3} │ {'Mask':<20} │ {'Hits':<6} │ {'Last Hit'}{W}")
        print(f"  {'─'*3}─┼─{'─'*20}─┼─{'─'*6}─┼─{'─'*19}")
        for r in links:
            print(f"  {r['id']:<3} │ {r['mask_text'][:20]:<20} │ {G}{r['clicks']:<6}{W} │ {r['last_accessed'] or '—'}")

        print(f"\n  {Y}[ID + Action]{W} e.g. '1c' to Copy, '1o' to Open | [Enter] Back")
        cmd = input(f"  Action: ").strip().lower()
        if not cmd: break
        
        target_id = "".join(filter(str.isdigit, cmd))
        row = next((r for r in links if str(r["id"]) == target_id), None)
        if not row: continue

        if PUBLIC_URL:
            base = PUBLIC_URL.replace("https://", "").replace("http://", "").rstrip("/")
            link = f"https://{row['mask_text']}@{base}/{row['redirect_code']}"
        else:
            link = f"http://{row['mask_text']}@{LAN_IP}:{PORT}/{row['redirect_code']}"

        if 'o' in cmd: open_url(link)
        else:
            if copy_to_clipboard(link): print(f"  {G}[+] Copied.{W}"); time.sleep(0.5)

def delete_links():
    clear()
    banner()
    print(f"{C}[ Delete Links ]{W}\n")
    links = database.get_all_links()
    if not links:
        print("  [i] No links found."); time.sleep(1); return

    for row in links:
        print(f"  {Y}[{row['id']}]{W} {row['mask_text'][:30]}  →  {row['redirect_code']}")

    print(f"\n  {Y}[Options]{W} IDs (e.g. '1,2'), 'all' to clear, or [Enter] to cancel")
    raw = input(f"  Choice: ").strip().lower()
    if not raw: return

    if raw == "all":
        confirm = input(f"  {R}[!] Delete ALL links? (y/N): {W}").strip().lower()
        if confirm == 'y':
            for r in links: database.delete_link(r['id'])
            print(f"  {G}[+] Database cleared.{W}")
            time.sleep(1)
        return

    ids = [i.strip() for i in raw.replace(",", " ").split() if i.strip().isdigit()]
    if not ids: return

    count = 0
    for tid in ids:
        if database.delete_link(int(tid)): count += 1
    
    print(f"  {G}[+] Deleted {count} link(s).{W}")
    time.sleep(1)

def main():
    database.init_db()

    # Server Thread
    server_thread = threading.Thread(target=redirect_server.run_server, kwargs={"host": "0.0.0.0", "port": 5000}, daemon=True)
    server_thread.start()

    # Availability Check
    for _ in range(30):
        try:
            with socket.create_connection(("127.0.0.1", 5000), timeout=0.1): break
        except Exception: time.sleep(0.1)

    try:
        while True:
            clear()
            banner()
            print(f"    {Y}1.{W} Create Masked URL")
            print(f"    {Y}2.{W} View Analytics / Manage Links")
            print(f"    {Y}3.{W} Settings / Maintenance")
            print(f"    {Y}4.{W} Delete Links")
            print(f"    {Y}5.{W} Exit\n")
            c = input(f"{G}raptor{W}:~$ ").strip()
            
            if c == "1": create_masked_url()
            elif c == "2": view_analytics()
            elif c == "3": manage_settings()
            elif c == "4": delete_links()
            elif c == "5": break
    finally:
        cleanup_tunnel()

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: cleanup_tunnel(); sys.exit(0)
