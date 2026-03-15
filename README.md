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
├── maskgen.py            # Core CLI tool — URL generation, analytics, listener
├── redirect_server.py    # Threaded Flask redirection server (HTTP listener)
├── database.py           # SQLite interface — link persistence & click tracking
├── utils.py              # Helper functions — formatting, validation, output styling
├── setup.sh              # Automated environment bootstrap script
├── requirements.txt      # Python dependency manifest
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

The included `setup.sh` handles the entire environment bootstrap automatically:

```bash
chmod +x setup.sh
./setup.sh
```

**What `setup.sh` does under the hood:**

```bash
# Creates an isolated Python virtual environment
python3 -m venv .venv

# Activates the venv
source .venv/bin/activate

# Installs all required dependencies
pip install -r requirements.txt

# Initializes the SQLite database schema
python3 database.py --init

echo "[✔] MASKGEN environment ready."
```

---

### Step 3 — Virtual Environment (venv)

The setup script creates a `.venv/` directory in the project root. This **isolated environment** ensures:

- No conflicts with your system-wide Python packages
- Reproducible dependency versions across machines
- Clean uninstall — just delete the `.venv/` folder

**To manually activate the venv before running MASKGEN:**

```bash
source .venv/bin/activate
```

**To deactivate when done:**

```bash
deactivate
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
╔══════════════════════════════════════════════════╗
║              MASKGEN — URL Masking Tool          ║
║        RFC 3986 @-Syntax Exploitation Engine     ║
╠══════════════════════════════════════════════════╣
║  Usage:  python3 maskgen.py [OPTIONS]            ║
║                                                  ║
║  Options:                                        ║
║    --generate    Launch interactive mask creator ║
║    --analytics   Display click-tracking table    ║
║    --server      Start redirect listener only    ║
║    --port [N]    Set listener port (default 8080)║
║    --help        Show this manual                ║
╚══════════════════════════════════════════════════╝
```

---

### Stage 2 · Interactive Mode — Launch the Listener

Run MASKGEN without flags to enter **interactive mode**. This simultaneously starts the **threaded Flask redirection server** and launches the CLI prompt:

```bash
python3 maskgen.py
```

```
[*] Starting MASKGEN redirect listener on http://127.0.0.1:8080
[✔] Threaded Flask server active — awaiting connections
[✔] Database connection established → maskgen.db

MASKGEN > _
```

The Flask server runs in a **background thread**, keeping the CLI fully interactive while handling all incoming HTTP redirect requests concurrently.

---

### Stage 3 · Generate a Masked URL

At the interactive prompt, select the **Generate** option and provide two inputs:

```
MASKGEN > generate

[?] Enter TARGET domain (real redirect destination):
    > malicious-redirect.net

[?] Enter MASK domain (displayed/fake domain):
    > legitimate-bank.com

[✔] Masked URL generated:

    https://legitimate-bank.com@127.0.0.1:8080/redir?id=a3f9

[*] Link saved to database. ID: a3f9
[*] Share this URL — all clicks will be logged and redirected.
```

The generated URL routes through your local listener, which **logs the click** and then performs a `302 redirect` to the actual target.

---

### Stage 4 · Analytics — Track Clicks

View all generated links, click counts, and timestamps using the analytics view:

```
MASKGEN > analytics
```

```
╔═══════╦══════════════════════════════════════╦══════════╦══════════════════════╗
║  ID   ║  Masked URL (Truncated)              ║  Clicks  ║  Last Accessed       ║
╠═══════╬══════════════════════════════════════╬══════════╬══════════════════════╣
║ a3f9  ║  legitimate-bank.com@127.0.0.1:8080  ║    14    ║  2025-01-15 03:42:07 ║
║ b81c  ║  support-paypal.com@127.0.0.1:8080   ║     3    ║  2025-01-15 04:11:55 ║
║ c220  ║  verify-account.net@127.0.0.1:8080   ║     0    ║  —                   ║
╚═══════╩══════════════════════════════════════╩══════════╩══════════════════════╝

  Total Links: 3  |  Total Clicks: 17  |  Active Since: 2025-01-15
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
    id           TEXT PRIMARY KEY,
    mask_domain  TEXT NOT NULL,
    target_url   TEXT NOT NULL,
    clicks       INTEGER DEFAULT 0,
    created_at   DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_accessed DATETIME
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
