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

**MASKGEN** is a Linux-native URL masking framework built for security researchers and penetration testers. It leverages a well-documented quirk in RFC 3986 — the **Userinfo subcomponent** of URIs — to construct URLs where a visible domain acts as cosmetic metadata while traffic is routed to a hidden destination.

### ✨ New in Version 2.0 (UX Enhanced)
- **Persistent Settings:** Save your tunnel URLs and server config in `maskgen_config.json`.
- **Auto-Clipboard:** Generated links are automatically copied to your clipboard.
- **Interactive Analytics:** Open or Copy any previous link directly from the analytics table.
- **Global Support:** Built-in support for public tunnels (Serveo/ngrok).

---

## 🏗 Architecture

```
MASKGEN/
│
├── maskgen.py            # Enhanced CLI — menu, settings, analytics
├── redirect_server.py    # Threaded Flask redirect server
├── database.py           # SQLite interface — link persistence
├── utils.py              # Helpers — code generation, IP detection
├── USAGE_GUIDE.md        # Detailed technical guide & glossary
├── setup.sh              # Automated dependency bootstrap
└── requirements.txt      # Python dependencies (flask, pyperclip)
```

---

## 🛠 Installation & Setup

### Step 1 — Clone & Bootstrap
```bash
git clone https://github.com/AbasSec/maskgen.git
cd maskgen
chmod +x setup.sh
./setup.sh
```

### Step 2 — Global Access (Tunneling)
If you are behind a NAT or using WSL2, you must use a tunnel to make your links work globally:
1. Start a tunnel: `ssh -R 80:localhost:5000 serveo.net`
2. Run MASKGEN with your tunnel URL:
   ```bash
   python3 maskgen.py --url https://your-subdomain.serveo.net
   ```

---

## 🕹 Features

### 1. Create Masked URL
Generate a link like `http://google.com@your-tunnel.com/abc`. The tool validates the target and automatically copies the result to your clipboard.

### 2. Interactive Analytics
View hits and timestamps. Type an ID (e.g., `5`) to copy that link, or `5o` to open it in your browser immediately.

### 3. Persistent Settings
Configure your server once. The tool remembers your `PUBLIC_URL` and listener settings across sessions.

---

## 📘 Detailed Documentation
For a deep dive into how the exploit works, definitions of terms like **Localhost**, **Tunneling**, and **Telnet**, see the full [**Usage Guide**](USAGE_GUIDE.md).

---

## ⚖️ Legal & Ethics
**AUTHORIZED USE ONLY.** MASKGEN is for educational research and authorized penetration testing. The authors are not responsible for misuse. Using this for unauthorized phishing is illegal.

---

<div align="center">

**MASKGEN** · Built by **AbasSec** · Use responsibly
*"Know the attack to build the defense."*
</div>
