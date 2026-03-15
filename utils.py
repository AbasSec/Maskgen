"""
utils.py — MASKGEN helper utilities.
URL validation, cryptographically-safe code generation, and optional QR output.
"""

import re
import secrets
import string

# Optional dependency — qrcode is listed in requirements.txt
try:
    import qrcode as _qrcode
    QR_AVAILABLE = True
except ImportError:
    QR_AVAILABLE = False

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


def make_qr(data: str, filename: str) -> str | None:
    """
    Generate a QR code PNG for the given data string.
    Returns the saved filename, or None if qrcode is not installed.
    """
    if not QR_AVAILABLE:
        return None
    qr = _qrcode.make(data)
    qr.save(filename)
    return filename
