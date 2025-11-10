import os
import time
import sys
from logging.handlers import RotatingFileHandler
import logging

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "securitymonitor.log")

_logger = logging.getLogger("SecurityMonitor")
_logger.setLevel(logging.INFO)
handler = RotatingFileHandler(LOG_FILE, maxBytes=1_000_000, backupCount=5)
formatter = logging.Formatter("[%(asctime)s] %(message)s", "%Y-%m-%d %H:%M:%S")
handler.setFormatter(formatter)
_logger.addHandler(handler)

def log(msg: str):
    """Simple console logger, UTF-8 safe on Windows."""
    timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]")
    try:
        print(f"{timestamp} {msg}", flush=True)
    except UnicodeEncodeError:
        safe_msg = msg.encode("utf-8", errors="replace").decode("utf-8", errors="ignore")
        print(f"{timestamp} {safe_msg}", flush=True)
