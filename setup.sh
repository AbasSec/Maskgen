#!/bin/bash

# =============================================================
#  MASKGEN — Auto-Installer for Linux (Kali / Ubuntu / Debian)
#  Installs dependencies directly. No virtual environment.
# =============================================================

echo -e "\e[1;31m"
echo "  ███╗   ███╗ █████╗ ███████╗██╗  ██╗ ██████╗ ███████╗███╗   ██╗"
echo "  ████╗ ████║██╔══██╗██╔════╝██║ ██╔╝██╔════╝ ██╔════╝████╗  ██║"
echo "  ██╔████╔██║███████║███████╗█████╔╝ ██║  ███╗█████╗  ██╔██╗ ██║"
echo "  ██║╚██╔╝██║██╔══██║╚════██║██╔═██╗ ██║   ██║██╔══╝  ██║╚██╗██║"
echo "  ██║ ╚═╝ ██║██║  ██║███████║██║  ██╗╚██████╔╝███████╗██║ ╚████║"
echo "  ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝"
echo -e "\e[0m"
echo -e "\e[1;31m[!] Initializing MASKGEN Setup...\e[0m"
echo ""

# ------------------------------------------------------------------
# 1. Check Python 3.10+
# ------------------------------------------------------------------
if ! command -v python3 &>/dev/null; then
    echo -e "\e[1;33m[*] Python3 not found. Installing...\e[0m"
    sudo apt update -qq && sudo apt install -y python3 python3-pip
fi

PY_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
PY_MAJOR=$(python3 -c "import sys; print(sys.version_info.major)")
PY_MINOR=$(python3 -c "import sys; print(sys.version_info.minor)")

echo -e "\e[1;34m[*] Detected Python $PY_VERSION\e[0m"

if [ "$PY_MAJOR" -lt 3 ] || { [ "$PY_MAJOR" -eq 3 ] && [ "$PY_MINOR" -lt 10 ]; }; then
    echo -e "\e[1;31m[!] Python 3.10 or higher is required. Found $PY_VERSION\e[0m"
    exit 1
fi

# ------------------------------------------------------------------
# 2. Check pip
# ------------------------------------------------------------------
if ! command -v pip3 &>/dev/null; then
    echo -e "\e[1;33m[*] pip3 not found. Installing...\e[0m"
    sudo apt install -y python3-pip
fi

# ------------------------------------------------------------------
# 3. Install dependencies from requirements.txt
# ------------------------------------------------------------------
echo -e "\e[1;34m[*] Installing dependencies...\e[0m"

pip3 install -r requirements.txt --break-system-packages --quiet

if [ $? -ne 0 ]; then
    echo -e "\e[1;31m[!] Dependency installation failed.\e[0m"
    echo -e "\e[1;33m    Try manually: pip3 install -r requirements.txt --break-system-packages\e[0m"
    exit 1
fi

# ------------------------------------------------------------------
# 4. Set execution permissions
# ------------------------------------------------------------------
echo -e "\e[1;34m[*] Setting execution permissions...\e[0m"
chmod +x maskgen.py

# ------------------------------------------------------------------
# 5. Done
# ------------------------------------------------------------------
echo ""
echo -e "\e[1;92m[+] Setup complete! MASKGEN is ready.\e[0m"
echo -e "\e[1m[*] Run the tool with:\e[0m  python3 maskgen.py"
echo -e "\e[1m[*] View the manual with:\e[0m python3 maskgen.py --help"
echo ""

