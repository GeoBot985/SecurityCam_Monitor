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

    # ----------------------------------------------------------
    def run(self):
        logger.log(f"[{self.name}] Starting camera worker.")
        self._open_stream_with_retry()

        while self.running:
            try:
                frame = self.reader.get_frame()
                if frame is None:
                    time.sleep(0.1)
                    continue

                # feed to trigger buffer
                self.trigger.update_buffer(frame)

                boxes = self.detector.detect_person(frame)
                if boxes:
                    logger.log(f"[{self.name}] 👤 Person detected! ({len(boxes)} instances)")
                    self.trigger.handle_detection(cam_name=self.name)
                else:
                    logger.log(f"[{self.name}] No person detected.")

                # short pause only to yield CPU
                time.sleep(0.01)

            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.log(f"[{self.name}] ❌ Worker crashed: {e}")
                self._reconnect_after_delay()

        self.reader.release()
        logger.log(f"[{self.name}] Camera worker stopped.")

    # ----------------------------------------------------------
    def _open_stream_with_retry(self):
        """Try opening the RTSP stream, retry until success."""
        while self.running:
            try:
                self.reader.open()
                logger.log(f"[{self.name}] Stream opened successfully.")
                return
            except Exception as e:
                logger.log(f"[{self.name}] ⚠️ Failed to open stream: {e}; retrying in 5s...")
                time.sleep(5)

    # ----------------------------------------------------------
    def _reconnect_after_delay(self):
        """Wait 5 s and reopen the RTSP stream."""
        self.reader.release()
        time.sleep(5)
        logger.log(f"[{self.name}] 🔄 Attempting reconnect...")
        self._open_stream_with_retry()

    # ----------------------------------------------------------
    def stop(self):
        self.running = False
        self.reader.release()
