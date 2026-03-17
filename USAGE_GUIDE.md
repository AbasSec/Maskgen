# MASKGEN Usage Guide

MASKGEN is an advanced URL masking tool designed for security researchers and authorized testing. This guide explains how to use the tool and defines key networking concepts involved.

## 🚀 How to Use MASKGEN

### 1. Launching the Tool
Start the interactive CLI by running:
```bash
python3 maskgen.py
```

### 2. Global Access (Tunnels)
If you are on a private network (like Home Wi-Fi or WSL2), external devices cannot reach your machine directly. To use the tool globally, you must use a **Tunneling Service**.

**Using Serveo (Recommended):**
1. Open a new terminal and run:
   ```bash
   ssh -R 80:localhost:5000 serveo.net
   ```
2. Copy the URL provided (e.g., `https://xyz.serveo.net`).
3. Launch MASKGEN with that URL:
   ```bash
   python3 maskgen.py --url https://xyz.serveo.net
   ```

---

## 📘 Glossary of Terms

### Localhost (127.0.0.1)
**What it is:** A reserved IP address that refers to "this computer."
**What it does:** When you access `localhost`, your computer talks to itself without sending data over the network. MASKGEN uses this for its internal redirect server.
**Restriction:** A URL containing `localhost` will **not** work on your phone or any other device; it only works on the machine running the code.

### Tunneling (e.g., Serveo / ngrok)
**What it is:** A way to expose a local server (like MASKGEN) to the public internet.
**What it does:** It creates a "bridge" between a public URL and your local machine. This allows a person on the other side of the world to scan your QR or click your link and still reach your computer.

### Telnet (Network Testing)
**What it is:** An old but powerful network protocol used to communicate with a remote server.
**What it does:** In modern security testing, `telnet` is often used to check if a specific port (like 5000) is open and accepting connections.
**How to get it:**
*   **Linux/macOS:** `sudo apt install telnet` or `brew install telnet`.
*   **Windows:** Enable "Telnet Client" in "Windows Features."
**Example Test:** `telnet 127.0.0.1 5000` — if it connects, the MASKGEN server is healthy.

### RFC 3986 (The @ Mask)
**What it is:** The official technical standard for URIs (Uniform Resource Identifiers).
**What it does:** It allows the use of an `@` symbol to separate user credentials from the actual host. MASKGEN "exploits" this by putting a fake domain (the mask) in the credential section, which many users mistake for the real destination.
**Example:** `http://google.com@your-ip.com/abc`
*   `google.com` is treated as a username (the mask).
*   `your-ip.com` is the actual destination server.

---

## ⚖️ Legal Disclaimer
This tool is for **authorized security research and CTF purposes only**. Using MASKGEN to perform unauthorized phishing or social engineering attacks is illegal and unethical.
