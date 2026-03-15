"""
maskgen.py — MASKGEN core CLI.
Starts the threaded Flask redirect server, manages URL generation,
and renders the interactive analytics table.

Usage:
    python3 maskgen.py           Launch interactive mode
    python3 maskgen.py --help    Display usage manual
"""

import os
import sys
import argparse
import threading

import database
import redirect_server
from utils import generate_code, is_valid_url, make_qr, QR_AVAILABLE

# --- CONFIGURATION ---
HOST = "127.0.0.1"
PORT = 5000

# --- ANSI COLOR HELPERS ---
R  = "\033[1;31m"   # Bold Red
G  = "\033[1;32m"   # Bold Green
B  = "\033[1;34m"   # Bold Blue
Y  = "\033[1;33m"   # Bold Yellow
C  = "\033[1;36m"   # Bold Cyan
W  = "\033[0m"      # Reset


# ---------------------------------------------------------------------------
# DISPLAY HELPERS
# ---------------------------------------------------------------------------

def clear():
    os.system("clear")


def banner():
    print(f"""
{R}    ███╗   ███╗ █████╗ ███████╗██╗  ██╗ ██████╗ ███████╗███╗   ██╗
    ████╗ ████║██╔══██╗██╔════╝██║ ██╔╝██╔════╝ ██╔════╝████╗  ██║
    ██╔████╔██║███████║███████╗█████╔╝ ██║  ███╗█████╗  ██╔██╗ ██║
    ██║╚██╔╝██║██╔══██║╚════██║██╔═██╗ ██║   ██║██╔══╝  ██║╚██╗██║
    ██║ ╚═╝ ██║██║  ██║███████║██║  ██╗╚██████╔╝███████╗██║ ╚████║
    ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝{W}
    {G}[ Framework Active | Listener: {HOST}:{PORT} ]{W}
""")


def display_help():
    print(f"""
{R}MASKGEN — USAGE GUIDE{W}
{'-'*59}
{C}DESCRIPTION:{W}
    Advanced URL masking tool exploiting RFC 3986 @-syntax.
    Prepend a trusted domain to conceal the real redirect target.

{C}URI ANATOMY:{W}
    https://[MASK_DOMAIN]@{HOST}:{PORT}/[CODE]
              ───────────  ─────────────  ──────
              Userinfo     Real Host      Redirect Code
              (ignored)    (Flask server) (maps to target)

{C}COMMANDS:{W}
    {G}python3 maskgen.py{W}          Launch interactive CLI
    {G}python3 maskgen.py --help{W}   Display this manual

{C}INTERACTIVE MENU OPTIONS:{W}
    {Y}1. Create Masked URL{W}   →  Enter target + mask, get @-URL
    {Y}2. View Analytics{W}      →  Click counts and timestamps
    {Y}3. Delete a Link{W}       →  Remove a link by ID
    {Y}4. Exit{W}

{C}QR CODE SUPPORT:{W}
    {'Enabled  — qrcode package detected.' if QR_AVAILABLE else 'Disabled — install qrcode: pip install qrcode --break-system-packages'}

{C}LEGAL:{W}
    For authorized security research and CTF purposes only.
{'-'*59}
""")


def main_menu() -> str:
    banner()
    print(f"    {Y}1.{W} Create Masked URL")
    print(f"    {Y}2.{W} View Analytics")
    print(f"    {Y}3.{W} Delete a Link")
    print(f"    {Y}4.{W} Exit\n")
    return input(f"{G}raptor@maskgen{W}:~$ ").strip()


# ---------------------------------------------------------------------------
# FEATURE: CREATE MASKED URL
# ---------------------------------------------------------------------------

def create_masked_url():
    clear()
    banner()
    print(f"{C}[ Create Masked URL ]{W}\n")

    # --- Target URL ---
    while True:
        target = input(f"  {Y}Target URL{W} (e.g. https://real-site.com): ").strip()
        if not target:
            print(f"  {R}[!] Target URL cannot be empty.{W}")
            continue
        if not is_valid_url(target):
            print(f"  {R}[!] Invalid URL. Must start with http:// or https://{W}")
            continue
        break

    # --- Mask Text ---
    while True:
        mask = input(f"  {Y}Mask Domain{W} (e.g. legitimate-bank.com): ").strip()
        if not mask:
            print(f"  {R}[!] Mask text cannot be empty.{W}")
            continue
        # Strip any accidental scheme prefix from mask — it's userinfo, not a URL
        mask = mask.replace("https://", "").replace("http://", "").rstrip("/")
        break

    # --- Generate unique code (retry on collision) ---
    for _ in range(5):
        code = generate_code(length=7)
        if database.save_link(mask, target, code):
            break
    else:
        print(f"\n  {R}[!] Failed to generate a unique code. Please try again.{W}")
        input("\n  Press Enter to continue...")
        return

    masked_url = f"https://{mask}@{HOST}:{PORT}/{code}"

    print(f"\n  {G}[+] Masked URL Generated:{W}")
    print(f"\n      {B}{masked_url}{W}\n")
    print(f"  {C}Code:{W}    {code}")
    print(f"  {C}Target:{W}  {target}")
    print(f"  {C}Mask:{W}    {mask}")

    # --- Optional QR code ---
    if QR_AVAILABLE:
        save_qr = input(f"\n  {Y}Generate QR code?{W} [y/N]: ").strip().lower()
        if save_qr == "y":
            filename = f"maskgen_{code}.png"
            result = make_qr(masked_url, filename)
            if result:
                print(f"  {G}[+] QR saved → {filename}{W}")
            else:
                print(f"  {R}[!] QR generation failed.{W}")

    input(f"\n  Press Enter to continue...")


# ---------------------------------------------------------------------------
# FEATURE: VIEW ANALYTICS
# ---------------------------------------------------------------------------

def view_analytics():
    clear()
    banner()
    print(f"{C}[ Analytics — All Links ]{W}\n")

    links = database.get_all_links()

    if not links:
        print(f"  {Y}[i] No links found. Create one first.{W}")
        input(f"\n  Press Enter to continue...")
        return

    # Column widths
    col = {"id": 4, "mask": 28, "code": 9, "clicks": 7, "created": 19, "last": 19}
    sep = (f"  {'─'*col['id']}─┼─{'─'*col['mask']}─┼─{'─'*col['code']}─┼─"
           f"{'─'*col['clicks']}─┼─{'─'*col['created']}─┼─{'─'*col['last']}─")

    header = (f"  {Y}{'ID':<{col['id']}} │ {'Mask':<{col['mask']}} │ "
              f"{'Code':<{col['code']}} │ {'Clicks':<{col['clicks']}} │ "
              f"{'Created':<{col['created']}} │ {'Last Hit':<{col['last']}}{W}")

    print(header)
    print(sep)

    for row in links:
        last = row["last_accessed"] if row["last_accessed"] else "—"
        mask_display = row["mask_text"][:col["mask"]]
        print(
            f"  {row['id']:<{col['id']}} │ "
            f"{mask_display:<{col['mask']}} │ "
            f"{row['redirect_code']:<{col['code']}} │ "
            f"{G}{row['clicks']:<{col['clicks']}}{W} │ "
            f"{row['created_at']:<{col['created']}} │ "
            f"{row['last_accessed'] or '—':<{col['last']}}"
        )

    total_clicks = sum(row["clicks"] for row in links)
    print(sep)
    print(f"\n  {C}Total links:{W} {len(links)}   {C}Total clicks:{W} {G}{total_clicks}{W}")
    input(f"\n  Press Enter to continue...")


# ---------------------------------------------------------------------------
# FEATURE: DELETE A LINK
# ---------------------------------------------------------------------------

def delete_link():
    clear()
    banner()
    print(f"{C}[ Delete a Link ]{W}\n")

    links = database.get_all_links()
    if not links:
        print(f"  {Y}[i] No links to delete.{W}")
        input(f"\n  Press Enter to continue...")
        return

    for row in links:
        print(f"  {Y}[{row['id']}]{W} {row['mask_text'][:30]}  →  code: {row['redirect_code']}")

    print()
    raw = input(f"  {Y}Enter link ID to delete{W} (or Enter to cancel): ").strip()
    if not raw:
        return

    if not raw.isdigit():
        print(f"\n  {R}[!] Invalid ID — must be a number.{W}")
        input(f"\n  Press Enter to continue...")
        return

    link_id = int(raw)
    confirm = input(f"  {R}Confirm delete ID {link_id}?{W} [y/N]: ").strip().lower()
    if confirm == "y":
        if database.delete_link(link_id):
            print(f"\n  {G}[+] Link ID {link_id} deleted.{W}")
        else:
            print(f"\n  {R}[!] No link found with that ID.{W}")
    else:
        print(f"\n  {Y}[i] Delete cancelled.{W}")

    input(f"\n  Press Enter to continue...")


# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--help", "-h", action="store_true",
                        help="Display the MASKGEN usage manual")
    args = parser.parse_args()

    if args.help:
        display_help()
        sys.exit(0)

    # Initialise DB before starting server thread
    database.init_db()

    # Start redirect server in background daemon thread
    server_thread = threading.Thread(
        target=redirect_server.run_server,
        kwargs={"host": HOST, "port": PORT},
        daemon=True,
        name="MaskgenRedirectServer"
    )
    server_thread.start()

    while True:
        clear()
        choice = main_menu()

        if choice == "1":
            create_masked_url()
        elif choice == "2":
            view_analytics()
        elif choice == "3":
            delete_link()
        elif choice == "4":
            print(f"\n{G}[+] Exiting MASKGEN. Stay authorized.{W}\n")
            sys.exit(0)
        else:
            # Silently ignore invalid menu input — loop back to menu
            pass


if __name__ == "__main__":
    main()

