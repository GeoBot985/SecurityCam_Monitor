"""
SecurityMonitor Configuration
This file is meant to stay editable even in production.
"""

# RTSP camera streams
RTSP_URLS = [
    {"name": "Front Cam", "url": "rtsp://geocon:geocon1@192.168.1.131/stream1"},
    {"name": "Side Cam",  "url": "rtsp://geocon:geocon11@192.168.1.132/stream1"},
]

# YOLO settings
MODEL_PATH = "yolov8s.pt"
PERSON_CONFIDENCE = 0.4

# Performance
FRAME_RATE = 1.0      # detection checks per second
COOLDOWN   = 120.0    # seconds between triggers per camera

# Recording
SAVE_PATH  = "recordings"

# General
DEBUG = False
