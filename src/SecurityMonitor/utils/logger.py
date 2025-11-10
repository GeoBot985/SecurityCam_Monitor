import os
import sys
import time
import logging
from logging.handlers import RotatingFileHandler

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "securitymonitor.log")

# Force stdout to UTF-8 (prevents Windows emoji crash)
if sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

_logger = logging.getLogger("SecurityMonitor")
_logger.setLevel(logging.INFO)

handler = RotatingFileHandler(LOG_FILE, maxBytes=1_000_000, backupCount=5, encoding="utf-8")
formatter = logging.Formatter("[%(asctime)s] %(message)s", "%Y-%m-%d %H:%M:%S")
handler.setFormatter(formatter)
_logger.addHandler(handler)

def log(msg: str):
    """Write to console and rotating file with UTF-8 safety."""
    try:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}")
    except UnicodeEncodeError:
        # fallback if console encoding fails
        safe_msg = msg.encode("ascii", "replace").decode()
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {safe_msg}")

    _logger.info(msg)
