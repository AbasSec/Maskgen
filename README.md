<div align="center">

```
███╗   ███╗ █████╗ ███████╗██╗  ██╗ ██████╗ ███████╗███╗   ██╗
████╗ ████║██╔══██╗██╔════╝██║ ██╔╝██╔════╝ ██╔════╝████╗  ██║
██╔████╔██║███████║███████╗█████╔╝ ██║  ███╗█████╗  ██╔██╗ ██║
██║╚██╔╝██║██╔══██║╚════██║██╔═██╗ ██║   ██║██╔══╝  ██║╚██╗██║
██║ ╚═╝ ██║██║  ██║███████║██║  ██╗╚██████╔╝███████╗██║ ╚████║
╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝
```

### URI Masking Framework · RFC 3986 Exploitation · Version 2.5 (Stable)

<br>

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Kali-557C94?style=for-the-badge&logo=linux&logoColor=white)](https://www.kali.org/)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](LICENSE)
[![Flask](https://img.shields.io/badge/Dependencies-Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)

</div>

---

## 🚀 Overview

**MASKGEN** is a high-performance URL masking framework. It leverages the URI Userinfo subcomponent (RFC 3986) to create links that appear to lead to a trusted domain while silently routing traffic to a hidden redirector.

### ✨ What's New in v2.5
- **Dual-Tunnel Engine:** Automated support for both **Serveo** and **Localhost.run**.
- **Actionable Dashboard:** Copy or Open links directly from the analytics table by ID.
- **Bulk Management:** Delete multiple links at once or wipe the database with the `all` command.
- **Improved Stability:** Non-blocking I/O and process group management prevents terminal hangs.
- **Security Hardening:** Strictly filtered URI schemes to prevent injection attacks.

---

## 🏗 Installation

```bash
git clone https://github.com/AbasSec/maskgen.git
cd maskgen
chmod +x setup.sh
./setup.sh
```

---

## 🕹 Quick Start

1.  **Launch:** `python3 maskgen.py`
2.  **Go Global:** Select **Option 3 -> 1** to initialize a public SSH tunnel instantly.
3.  **Create:** Select **Option 1**, enter your target and mask.
4.  **Manage:** Select **Option 2** to see hits. Type `1c` to copy link #1 or `1o` to test it in your browser.

---

## 📖 Documentation
See the [**Technical Usage Guide**](USAGE_GUIDE.md) for deep-dives into:
- Global vs. Local networking.
- How the URI Userinfo exploit works.
- Glossary of technical terms (Tunneling, Localhost, Telnet).
- Viewing live diagnostic logs.

---

## ⚖️ Legal & Ethics
**AUTHORIZED USE ONLY.** This tool is for educational research and authorized penetration testing. The authors are not responsible for misuse. Using this for unauthorized social engineering is illegal.

---

<div align="center">

**MASKGEN** · Built by **AbasSec**
*"Know the attack to build the defense."*
</div>
