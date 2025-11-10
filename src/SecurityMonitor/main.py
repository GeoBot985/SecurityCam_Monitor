# main.py
import time
from SecurityMonitor.camera_worker import CameraWorker
from SecurityMonitor.yolo_detector import YoloDetector
from SecurityMonitor.utils import logger, config


def main():
    logger.log("🚀 Starting SecurityMonitor...")
    detector = YoloDetector()  # shared YOLO model for all cameras

    workers = []
    for cam in config.RTSP_URLS:
        worker = CameraWorker(cam["name"], cam["url"], detector)
        workers.append(worker)
        worker.start()

    logger.log("✅ All camera workers started. Press Ctrl+C to stop.")

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


if __name__ == "__main__":
    main()
