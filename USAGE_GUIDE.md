# MASKGEN Technical Usage Guide

MASKGEN is a sophisticated URL masking framework designed for security researchers. Version 2.5 introduces significant stability and user experience enhancements.

## 🚀 Interactive Menu Structure

1.  **Create Masked URL:** The core engine. Generates your links.
2.  **View Analytics / Manage Links:** Interactive dashboard. Type an ID to Copy (`1c`) or Open (`1o`).
3.  **Settings / Maintenance:** Manage persistent config, switch tunnel providers, or view live logs.
4.  **Delete Links:** Clean up your database. Supports single ID, Bulk (`1, 2, 5`), or `all`.
5.  **Exit:** Gracefully closes the server and kills active tunnels.

---

## 🌐 Global Access & Tunneling

If you are not on a public VPS, your local machine is invisible to the internet. MASKGEN automates the use of **SSH Tunnels** to bridge this gap.

### Automated Providers:
*   **Serveo (serveo.net):** Standard reliable tunneling.
*   **Localhost.run (lhr.life):** Alternative provider with different domain names to bypass filters.

**Switching:** Go to **Option 3 -> 3** to toggle between providers. The tool will automatically restart your tunnel and update your public URL.

---

## 🛠 Features & Explanations

### RFC 3986 (The @ Mask)
The tool uses the "Userinfo" subcomponent of a URI. Browsers treat anything before the `@` as metadata (username) and connect to the host after the `@`.
*   **Example:** `https://bank.com@xyz.lhr.life/abc`
*   **Reality:** Connects to `xyz.lhr.life`.

### Actionable Analytics
The dashboard is no longer just for viewing.
*   **Copying:** Enter the ID (e.g., `5`) to immediately copy that link to your clipboard.
*   **Opening:** Enter ID + `o` (e.g., `5o`) to open it in your default browser.

### Bulk Deletion
Management is faster. You can enter `1 2 3` to delete those specific links or `all` to clear the entire database.

### Diagnostic Logging
All background activity (Server hits, SSH errors) is saved to `server.log`. You can view the last 30 lines directly in the app via **Option 3 -> 4**.

---

## 📘 Glossary

*   **Localhost (127.0.0.1):** This machine. Links using this address will NOT work on other devices.
*   **0.0.0.0:** A directive telling the server to "listen on every possible network interface."
*   **SSH Tunnel:** A secure pipe that forwards a public port to your local computer.
*   **Telnet:** A utility used to test if a port (like 5000) is actually open and accepting data.

---

## ⚖️ Legal Disclaimer
Unauthorized use of this tool for phishing or social engineering is illegal. This is for **authorized security testing only**.
