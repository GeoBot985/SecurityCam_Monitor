# SecurityMonitor/recorder.py
"""
Recorder module – saves short video clips using frames already read
by the active VideoReader, avoiding a second RTSP connection.
"""

import cv2
import time
import threading
import os
from SecurityMonitor.utils import config, logger


class Recorder:
    """Writes buffered frames to disk as video clips."""

    def __init__(self, save_path=config.SAVE_PATH):
        self.save_path = save_path
        os.makedirs(save_path, exist_ok=True)
        self.recording = False

    # --------------------------------------------------------------
    def record_from_frames(self, frames, cam_name="Camera"):
        """Start a background write using frames provided by VideoReader."""
        if not frames or self.recording:
            return
        self.recording = True
        t = threading.Thread(
            target=self._write_clip, args=(frames, cam_name), daemon=True
        )
        t.start()

    # --------------------------------------------------------------
    def _write_clip(self, frames, cam_name):
        """Actually write frames to file (runs in background thread)."""
        try:
            # Video parameters
            h, w, _ = frames[0].shape
            fourcc = cv2.VideoWriter_fourcc(*"XVID")
            fps = max(1.0, config.FRAME_RATE)  # use detection FPS as nominal rate

            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"{cam_name}_{timestamp}.avi"
            filepath = os.path.join(self.save_path, filename)

            out = cv2.VideoWriter(filepath, fourcc, fps, (w, h))
            logger.log(f"[{cam_name}] 🎥 Writing {len(frames)} frames to {filepath}")

            for f in frames:
                out.write(f)

            out.release()
            logger.log(f"[{cam_name}] 💾 Saved recording: {filepath}")
        except Exception as e:
            logger.log(f"[{cam_name}] ❌ Recording failed: {e}")
        finally:
            self.recording = False
