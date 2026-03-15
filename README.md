<div align="center">

███╗   ███╗ █████╗ ███████╗██╗  ██╗ ██████╗ ███████╗███╗   ██╗
████╗ ████║██╔══██╗██╔════╝██║ ██╔╝██╔════╝ ██╔════╝████╗  ██║
██╔████╔██║███████║███████╗█████╔╝ ██║  ███╗█████╗  ██╔██╗ ██║
██║╚██╔╝██║██╔══██║╚════██║██╔═██╗ ██║   ██║██╔══╝  ██║╚██╗██║
██║ ╚═╝ ██║██║  ██║███████║██║  ██╗╚██████╔╝███████╗██║ ╚████║
╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝

# MASKGEN — Advanced URL Masking & Redirection Framework

**Social Engineering · URI Manipulation · Educational Research**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)
![Platform](https://img.shields.io/badge/Platform-Linux%20%2F%20Kali-557C94?style=flat-square&logo=linux)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Dependencies](https://img.shields.io/badge/Dependencies-Minimal-brightgreen?style=flat-square)
![Status](https://img.shields.io/badge/Research-Educational-red?style=flat-square)

*A specialized Linux-native framework for demonstrating URI @-syntax manipulation and redirect tracking.*

</div>

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage Guide](#usage-guide)
- [Functional Requirements](#functional-requirements)
- [Security Disclaimer](#security-disclaimer)

---

## Overview

**MASKGEN** is a specialized utility designed to demonstrate **URL Masking** techniques. It leverages the "User Information" subcomponent of the [RFC 3986](https://datatracker.ietf.org/doc/html/rfc3986#section-3.2) URI specification. 

By prepending a trusted domain followed by the `@` symbol, the browser treats the first half as login credentials and ignores it, navigating instead to the host specified after the symbol.

[Image of URI structure RFC 3986 userinfo host port path]

---

## Architecture

The tool is designed to be modular and stealthy, utilizing a single-process threaded model for both management and redirection.
maskgen/├── maskgen.py           # Core Framework (CLI + Threaded Server)├── database.py          # SQLite persistence layer├── utils.py             # Validation and logic├── requirements.txt     # Python dependencies└── maskgen.db           # Auto-generated database
---

## Installation

**Target OS:** Kali Linux, Parrot OS, or Ubuntu.

```bash
# 1. Clone the repository
git clone [https://github.com/yourusername/maskgen.git](https://github.com/yourusername/maskgen.git)
cd maskgen

# 2. Install dependencies
pip install flask qrcode

# 3. Initialize the tool
chmod +x maskgen.py
python3 maskgen.py
Usage GuideStage 1 — Generating the MaskLaunch the tool and select Option 1. You will be prompted for:Target URL: The real location (e.g., https://google.com).Mask Text: The decoy domain (e.g., https://verify-google.com).The output will be: https://verify-google.com@localhost:5000/XYZ123.Stage 2 — DeploymentThe redirect server starts automatically in a background thread upon running maskgen.py. As long as the script is running, any traffic hitting your localhost:5000 port with a valid code will be redirected.Stage 3 — AnalyticsSelect Option 2 in the CLI to see real-time click tracking:PlaintextID | Masked Domain                | Target                | Clicks
------------------------------------------------------------------
1  | [https://secure-login.com](https://secure-login.com)     | [https://victim.com](https://victim.com)    | 12
Functional RequirementsFeatureDetails@ MaskingImplements RFC-compliant URI userinfo manipulation.302 RedirectsUses Flask to issue temporary redirects for maximum stealth.SQLite DBStores all historical masks and click counts locally.Threaded ServerRuns the listener and CLI simultaneously in one terminal.Linux NativeOptimized for terminal-based workflows on Kali Linux.Security DisclaimerFOR AUTHORIZED SECURITY RESEARCH ONLY.MASKGEN is intended for use in controlled environments for educational purposes, CTF challenges, and authorized social engineering simulations. Using this tool to deceive individuals without prior written consent is illegal. The developers assume no liability for misuse or damage caused by this program.<div align="center">MASKGEN v2.5 — Built for Authorized Security ResearchReconnaissance · Attack · Redirection · Orchestration</div>
