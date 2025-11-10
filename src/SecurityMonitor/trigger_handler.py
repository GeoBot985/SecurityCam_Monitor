import time
import threading
from collections import deque
from SecurityMonitor.recorder import Recorder
from SecurityMonitor.utils import logger, config
from SecurityMonitor.utils.sound_alert import play_alert


class TriggerHandler:
    """Handles detection events, cooldowns, and recording triggers."""

    def __init__(self):
        self.last_trigger_time = 0.0
        self.cooldown = config.COOLDOWN
        self.recorder = Recorder()
        self.frame_buffer = deque(maxlen=int(config.FRAME_RATE * 30))  # ~30 s pre-event

    # --------------------------------------------------------------
    def update_buffer(self, frame):
        """Continuously push frames into buffer (called from camera worker)."""
        if frame is not None:
            self.frame_buffer.append(frame)

    # --------------------------------------------------------------
    def handle_detection(self, cam_name="Camera"):
        now = time.time()
        if now - self.last_trigger_time < self.cooldown:
            logger.log(f"[{cam_name}] ⏳ In cooldown; detection ignored.")
            return

        self.last_trigger_time = now
        logger.log(f"[{cam_name}] 🚨 Detection triggered!")
        play_alert()

        # snapshot of current buffer (pre-event)
        pre_frames = list(self.frame_buffer)

        # spawn a thread to collect post-event frames
        threading.Thread(
            target=self._collect_post_event,
            args=(cam_name, pre_frames),
            daemon=True,
        ).start()

    # --------------------------------------------------------------
    def _collect_post_event(self, cam_name, pre_frames):
        """Collects ~30 s of frames after event before writing clip."""
        post_frames = []
        deadline = time.time() + 30  # seconds after trigger

        logger.log(f"[{cam_name}] ⏳ Capturing 30 s post-event frames...")
        while time.time() < deadline:
            if self.frame_buffer:
                post_frames.append(self.frame_buffer[-1])
            time.sleep(1.0 / max(1.0, config.FRAME_RATE))

        all_frames = pre_frames + post_frames
        self.recorder.record_from_frames(all_frames, cam_name=cam_name)
        logger.log(f"[{cam_name}] ✅ Post-event capture complete ({len(all_frames)} frames).")
