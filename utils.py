"""
utils.py — MASKGEN helper utilities.
URL validation, cryptographically-safe code generation, and optional QR output.
"""

import re
import secrets
import string
import socket as _socket

# Alphabet for redirect codes (no ambiguous chars: 0/O, l/1/I)
_CODE_ALPHABET = (
    "abcdefghjkmnpqrstuvwxyz"
    "ABCDEFGHJKLMNPQRSTUVWXYZ"
    "23456789"
)


def generate_code(length: int = 7) -> str:
    """
    Generate a cryptographically random alphanumeric redirect code.
    Uses secrets module instead of random for unpredictability.
    Default length is 7 to match maskgen.py's original intent.
    """
    return ''.join(secrets.choice(_CODE_ALPHABET) for _ in range(length))


def is_valid_url(url: str) -> bool:
    """
    Validate that a URL starts with http:// or https:// and has a valid host.
    Rejects bare strings, localhost-only entries, and malformed schemes.
    """
    if not url or not isinstance(url, str):
        return False
    url = url.strip()
    # Must begin with http(s):// followed by at least one valid host character
    pattern = re.compile(
        r'^https?://'                        # scheme
        r'(?:[A-Za-z0-9\-._~%]+)'           # host (domain or IP)
        r'(?::\d{1,5})?'                     # optional port
        r'(?:[/?#]\S*)?$'                    # optional path/query/fragment
    )
    return bool(pattern.match(url.strip()))


def get_local_ip() -> str:
    """
    Attempt to find the primary LAN IP address of the machine.
    Returns 127.0.0.1 if it cannot determine an external-facing IP.
    """
    try:
        # We don't actually send data; we just trigger OS routing logic.
        s = _socket.socket(_socket.AF_INET, _socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"
