#!/bin/bash

# --- MASKGEN Auto-Installer for Linux ---
echo -e "\e[1;31m[!] Initializing MASKGEN Setup...\e[0m"

# 1. Update and Check Python
if ! command -v python3 &> /dev/null; then
    echo "[!] Python3 not found. Installing..."
    sudo apt update && sudo apt install python3 python3-venv python3-pip -y
fi

# 2. Create Virtual Environment
echo "[*] Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# 3. Install Dependencies
echo "[*] Installing Flask..."
pip install flask

# 4. Set Permissions
echo "[*] Setting execution permissions..."
chmod +x maskgen.py

echo -e "\e[1;92m[+] Setup Complete!\e[0m"
echo -e "[*] Run the tool with: \e[1mpython3 maskgen.py\e[0m"
