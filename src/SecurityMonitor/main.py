import time
import threading
from SecurityMonitor.camera_worker import CameraWorker
from SecurityMonitor.yolo_detector import YoloDetector
from SecurityMonitor.utils import logger, config


def validate_config():
    """Verify camera and core configuration before startup."""
    if not getattr(config, "RTSP_URLS", []):
        raise ValueError("No RTSP cameras defined in config.py.")
    for cam in config.RTSP_URLS:
        if "url" not in cam or "name" not in cam:
            raise ValueError(f"Invalid camera entry in config: {cam}")


def heartbeat(workers):
    """Logs camera thread health every 60 s."""
    while True:
        live = sum(1 for w in workers if w.is_alive())
        logger.log(f"💓 Heartbeat: {live}/{len(workers)} camera threads alive.")
        time.sleep(60)


def main():
    logger.log("🚀 Starting SecurityMonitor...")
    validate_config()

    # Load YOLO once and share across threads
    detector = YoloDetector()

    # Create and start all camera threads
    workers = []
    for cam in config.RTSP_URLS:
        worker = CameraWorker(cam["name"], cam["url"], detector)
        workers.append(worker)
        worker.start()

    logger.log("✅ All camera workers started. Press Ctrl+C to stop.")

    # Start heartbeat thread
    hb_thread = threading.Thread(target=heartbeat, args=(workers,), daemon=True)
    hb_thread.start()

    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.log("🛑 Shutting down SecurityMonitor...")
        for w in workers:
            w.stop()
        for w in workers:
            w.join()
        logger.log("✅ All camera threads stopped cleanly.")
        logger.log("👋 SecurityMonitor exited.")


if __name__ == "__main__":
    main()
