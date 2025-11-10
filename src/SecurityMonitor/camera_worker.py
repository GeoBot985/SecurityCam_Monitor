# SecurityMonitor/camera_worker.py
import time
import threading
from SecurityMonitor.video_reader import VideoReader
from SecurityMonitor.trigger_handler import TriggerHandler
from SecurityMonitor.utils import config, logger

class CameraWorker(threading.Thread):
    """Runs detection for one camera feed in its own thread."""

    def __init__(self, name, rtsp_url, detector):
        super().__init__(daemon=True)
        self.name = name
        self.rtsp_url = rtsp_url
        self.detector = detector
        self.trigger = TriggerHandler()
        self.reader = VideoReader(rtsp_url, debug=config.DEBUG)
        self.running = True

    def run(self):
        logger.log(f"[{self.name}] Starting camera worker.")
        self.reader.open()

        try:
            while self.running:
                frame = self.reader.get_frame()
                if frame is None:
                    continue

                self.trigger.update_buffer(frame)  # store recent frames
                boxes = self.detector.detect_person(frame)
                if boxes:
                    logger.log(f"[{self.name}] 👤 Person detected! ({len(boxes)} instances)")
                    self.trigger.handle_detection(cam_name=self.name)
                else:
                    logger.log(f"[{self.name}] No person detected.")


                #time.sleep(0.02)
        except KeyboardInterrupt:
            pass
        finally:
            self.reader.release()
            logger.log(f"[{self.name}] Camera worker stopped.")

    def stop(self):
        self.running = False
