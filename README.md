<div align="center">

```
███╗   ███╗ █████╗ ███████╗██╗  ██╗ ██████╗ ███████╗███╗   ██╗
████╗ ████║██╔══██╗██╔════╝██║ ██╔╝██╔════╝ ██╔════╝████╗  ██║
██╔████╔██║███████║███████╗█████╔╝ ██║  ███╗█████╗  ██╔██╗ ██║
██║╚██╔╝██║██╔══██║╚════██║██╔═██╗ ██║   ██║██╔══╝  ██║╚██╗██║
██║ ╚═╝ ██║██║  ██║███████║██║  ██╗╚██████╔╝███████╗██║ ╚████║
╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝
```

### URI Masking Framework · RFC 3986 @-Syntax Exploitation

<br>

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Kali-557C94?style=for-the-badge&logo=linux&logoColor=white)](https://www.kali.org/)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](LICENSE)
[![Flask](https://img.shields.io/badge/Dependencies-Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Status](https://img.shields.io/badge/Status-Educational%20Research-F59E0B?style=for-the-badge&logo=bookstack&logoColor=white)]()

</div>

---

## 🚀 Overview

**MASKGEN** is a Linux-native URL masking framework built for security researchers, penetration testers, and CTF practitioners. It leverages a well-documented quirk in RFC 3986 — the **Userinfo subcomponent** of URIs — to construct URLs where the visible domain acts as cosmetic metadata while all traffic is silently routed to the real destination.

### 🔬 The URI Userinfo Exploit — How It Works

According to [RFC 3986 §3.2.1](https://datatracker.ietf.org/doc/html/rfc3986#section-3.2.1), a URI authority component can carry optional credential metadata in the following structure:

```
scheme://[userinfo@]host[:port]/path
```

The **`userinfo`** subcomponent is everything that appears **before** the `@` symbol. Browsers treat it as credential metadata (historically used for `user:password@host` FTP/HTTP authentication). Modern browsers **ignore this prefix entirely** and connect only to the **host specified after the `@`**.

#### 📐 Visual Breakdown

```
https://legitimate-bank.com@malicious-redirect.net/payload
         ─────────────────── ──────────────────────────────
               │                          │
         [ USERINFO ]              [ REAL HOST ]
     Treated as metadata         Browser connects HERE
     Displayed in URL bar        Hidden redirect target
         (ignored)
```

| URI Component   | Value                        | Browser Behavior             |
|-----------------|------------------------------|------------------------------|
| `scheme`        | `https://`                   | Protocol selection           |
| `userinfo`      | `legitimate-bank.com`        | **Ignored / Metadata only**  |
| `@` delimiter   | `@`                          | Userinfo/host separator      |
| `host`          | `malicious-redirect.net`     | **Actual connection target** |

> **In plain English:** The URL *looks* like it goes to `legitimate-bank.com`, but the browser connects to `malicious-redirect.net`. MASKGEN automates the construction, deployment, and tracking of such links via a local Flask redirection server.

---

## 🏗 Architecture

```
MASKGEN/
│
├── maskgen.py            # Core CLI — menu, URL generation, analytics, delete
├── redirect_server.py    # Threaded Flask redirect server (HTTP listener)
├── database.py           # SQLite interface — link persistence & click tracking
├── utils.py              # Helpers — code generation, URL validation, QR output
├── setup.sh              # Automated dependency bootstrap script
├── requirements.txt      # Python dependency manifest (flask, qrcode[pil])
├── maskgen.db            # SQLite database (auto-generated on first run)
└── README.md             # This file
```

### ⚙️ Component Interaction

```
  [ CLI / maskgen.py ]
         │
         ├──► [ utils.py ]         →  Input validation, URL construction
         ├──► [ database.py ]      →  SQLite R/W (maskgen.db)
         └──► [ redirect_server.py ] →  Threaded Flask listener on localhost
                      │
                      └──► Incoming requests → Log click + redirect to target
```

---

## 🛠 Installation

### Prerequisites

- OS: **Kali Linux**, Ubuntu 20.04+, or any Debian-based distro
- Python: **3.10 or higher**
- Permissions: Standard user (no root required for local server)

---

### Step 1 — Clone the Repository

```bash
git clone https://github.com/AbasSec/maskgen.git
cd maskgen
```

---

### Step 2 — Run the Setup Script

The included `setup.sh` handles the complete environment bootstrap automatically. It checks your Python version, installs all dependencies directly into your system Python, and sets the correct file permissions — no virtual environment required.

```bash
chmod +x setup.sh
./setup.sh
```

**What `setup.sh` does under the hood:**

```bash
# Checks for Python 3.10+ (exits if not met)
python3 --version

# Installs all required dependencies directly (no venv needed)
pip3 install -r requirements.txt --break-system-packages

# Sets execution permissions on the main script
chmod +x maskgen.py
```

---

### Step 3 — Manual Dependency Install (Alternative)

If you prefer to install dependencies manually without running the setup script:

```bash
pip3 install -r requirements.txt --break-system-packages
```

> **Why `--break-system-packages`?**
> Kali Linux (Debian 12+) enforces [PEP 668](https://peps.python.org/pep-0668/), which blocks `pip` from writing to the system Python environment by default. This flag explicitly permits it. On older Kali or Ubuntu systems it is harmless and simply ignored.

After installation, launch the tool directly:

```bash
python3 maskgen.py
```

---

## 🕹 Usage Guide — The Workflow

### Stage 1 · View the Manual

Before running the tool, inspect all available flags and options using the built-in styled help output:

```bash
python3 maskgen.py --help
```

**Expected output:**

```
MASKGEN — USAGE GUIDE
-----------------------------------------------------------
DESCRIPTION:
    Advanced URL masking tool exploiting RFC 3986 @-syntax.
    Prepend a trusted domain to conceal the real redirect target.

COMMANDS:
    python3 maskgen.py          Launch interactive CLI
    python3 maskgen.py --help   Display this manual

INTERACTIVE MENU OPTIONS:
    1. Create Masked URL   →  Enter target + mask, get @-URL
    2. View Analytics      →  Click counts and timestamps
    3. Delete a Link       →  Remove a link by ID
    4. Exit

LEGAL:
    For authorized security research and CTF purposes only.
-----------------------------------------------------------
```

---

### Stage 2 · Interactive Mode — Launch the Listener

Run MASKGEN without flags to enter **interactive mode**. This simultaneously starts the **threaded Flask redirection server** on port 5000 and presents the interactive menu:

```bash
python3 maskgen.py
```

```
    ███╗   ███╗ █████╗ ███████╗██╗  ██╗ ██████╗ ███████╗███╗   ██╗
    ...
    [ Framework Active | Listener: 127.0.0.1:5000 ]

    1. Create Masked URL
    2. View Analytics
    3. Delete a Link
    4. Exit

raptor@maskgen:~$
```

The Flask server runs in a **background daemon thread**, keeping the CLI fully interactive while handling all incoming HTTP redirect requests concurrently.

---

### Stage 3 · Generate a Masked URL

Select option `1` and provide two inputs when prompted:

```
raptor@maskgen:~$ 1

  Target URL (e.g. https://real-site.com): https://malicious-redirect.net
  Mask Domain (e.g. legitimate-bank.com):  legitimate-bank.com

  [+] Masked URL Generated:

      https://legitimate-bank.com@127.0.0.1:5000/aB3x9mK

  Code:    aB3x9mK
  Target:  https://malicious-redirect.net
  Mask:    legitimate-bank.com

  Generate QR code? [y/N]:
```

The tool validates both inputs before saving. The mask is automatically stripped of any accidental `https://` prefix. A QR code PNG can be optionally exported if `qrcode` is installed.

---

### Stage 4 · Analytics — Track Clicks

Select option `2` to view all generated links with click counts, creation timestamps, and last-accessed times:

```
  ID   │ Mask                         │ Code      │ Clicks  │ Created             │ Last Hit
  ─────┼──────────────────────────────┼───────────┼─────────┼─────────────────────┼───────────────────
  1    │ legitimate-bank.com          │ aB3x9mK   │ 14      │ 2025-01-15 03:40:01 │ 2025-01-15 03:42:07
  2    │ support-paypal.com           │ rT7yWqZ   │ 3       │ 2025-01-15 04:10:00 │ 2025-01-15 04:11:55
  3    │ verify-account.net           │ Kp2LmNv   │ 0       │ 2025-01-15 04:15:30 │ —

  Total links: 3   Total clicks: 17
```

---

## 🗃 Database Details

MASKGEN uses **SQLite** (`maskgen.db`) as its persistence layer — no external database server required.

| Feature                  | Details                                      |
|--------------------------|----------------------------------------------|
| **Engine**               | SQLite 3 (via Python `sqlite3` stdlib)       |
| **File location**        | `./maskgen.db` (project root)                |
| **Persistence**          | Survives server restarts — data is retained  |
| **Schema**               | `links` table: `id`, `mask`, `target`, `clicks`, `created_at`, `last_accessed` |
| **Managed by**           | `database.py` module                         |

The database is **auto-initialized** on first run. All generated links and their click-count metrics are permanently stored, enabling longitudinal analytics across multiple sessions.

```sql
-- Internal schema (reference only)
CREATE TABLE links (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    mask_text     TEXT    NOT NULL,
    target_url    TEXT    NOT NULL,
    redirect_code TEXT    UNIQUE NOT NULL,
    created_at    TEXT    NOT NULL,
    clicks        INTEGER DEFAULT 0,
    last_accessed TEXT    DEFAULT NULL
);
```

---

## ⚖️ Legal & Ethics

> **⚠️ IMPORTANT — READ BEFORE USE**

```
╔══════════════════════════════════════════════════════════════════╗
║                    AUTHORIZED USE ONLY                          ║
╠══════════════════════════════════════════════════════════════════╣
║  MASKGEN is developed exclusively for:                          ║
║                                                                  ║
║   ✔  Authorized penetration testing engagements                 ║
║   ✔  Security awareness training programs                       ║
║   ✔  CTF (Capture The Flag) competitions                        ║
║   ✔  Academic security research in controlled environments      ║
║   ✔  Red team simulations with written client authorization     ║
║                                                                  ║
║  The authors are NOT responsible for any misuse of this tool.   ║
║  Deploying masked URLs against individuals or organizations     ║
║  without explicit written consent is ILLEGAL in most            ║
║  jurisdictions and may violate:                                  ║
║                                                                  ║
║   ✘  Computer Fraud and Abuse Act (CFAA) — United States       ║
║   ✘  Computer Misuse Act — United Kingdom                       ║
║   ✘  Cybercrime laws in your respective jurisdiction            ║
╚══════════════════════════════════════════════════════════════════╝
```

**By using MASKGEN, you confirm that you have obtained all necessary authorizations and accept sole legal responsibility for your actions.**

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**MASKGEN** · Built for the security community · Use responsibly

*"Know the attack to build the defense."*

</div>
