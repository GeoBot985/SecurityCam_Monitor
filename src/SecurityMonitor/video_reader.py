import cv2
import time
from SecurityMonitor.utils import config, logger


class VideoReader:
    """Simple continuous RTSP reader with real-time freshness."""

    def __init__(self, rtsp_url=None, debug=config.DEBUG, name=None):
        # if no specific URL is passed, use the first camera from config.RTSP_URLS
        if rtsp_url is None:
            try:
                rtsp_url = config.RTSP_URLS[0]["url"]
            except Exception:
                raise ValueError("No RTSP URL provided and config.RTSP_URLS is empty.")

        self.rtsp_url = rtsp_url
        self.debug = debug
        self.name = name or rtsp_url
        self.cap = None
        self.frame_interval = 1.0 / max(1.0, config.FRAME_RATE)
        self.last_time = 0.0
        self.fail_count = 0
        self.max_failures = 5

    # -------------------------------------------------------------
    def open(self):
        logger.log(f"[{self.name}] Opening RTSP stream: {self.rtsp_url}")
        self.cap = cv2.VideoCapture(self.rtsp_url, cv2.CAP_FFMPEG)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        if not self.cap.isOpened():
            logger.log(f"[{self.name}] ❌ Failed to open RTSP stream.")
            return False
        # burn a few frames to clear the decoder
        for _ in range(10):
            self.cap.grab()
        logger.log(f"[{self.name}] Stream opened successfully.")
        return True

    # -------------------------------------------------------------
    def get_frame(self):
        """Continuously read frames; return latest only when interval passes."""
        if not self.cap or not self.cap.isOpened():
            return None

        success, frame = self.cap.read()
        if not success or frame is None:
            self.fail_count += 1
            if self.fail_count >= self.max_failures:
                logger.log(f"[{self.name}] ⚠️ Frame read failed repeatedly; attempting reopen.")
                self.reconnect()
            return None

        self.fail_count = 0
        now = time.time()
        # only yield frame once per configured interval
        if now - self.last_time < self.frame_interval:
            return None
        self.last_time = now

        if self.debug:
            cv2.imshow(f"{self.name} (Debug)", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                raise KeyboardInterrupt
        else:
            # pump decoder thread
            cv2.waitKey(1)

        return frame

    # -------------------------------------------------------------
    def reconnect(self):
        if self.cap:
            self.cap.release()
        time.sleep(3)
        self.open()

    # -------------------------------------------------------------
    def release(self):
        if self.cap:
            self.cap.release()
        if self.debug:
            cv2.destroyAllWindows()
        logger.log(f"[{self.name}] RTSP stream closed.")
