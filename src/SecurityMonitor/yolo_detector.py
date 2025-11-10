# yolo_detector.py
from ultralytics import YOLO
import torch
from SecurityMonitor.utils import config, logger


class YoloDetector:
    def __init__(self, model_path="yolov8n.pt", conf_thresh=config.PERSON_CONFIDENCE):
        logger.log("Loading YOLO model...")
        self.model = YOLO(model_path)
        self.conf_thresh = conf_thresh
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.log(f"YOLO loaded on device: {self.device}")

    def detect_person(self, frame):
        """Detects persons in a frame, returns list of bounding boxes."""
        results = self.model.predict(frame, verbose=False, device=self.device)
        boxes = []
        for r in results:
            for box, cls, conf in zip(r.boxes.xyxy, r.boxes.cls, r.boxes.conf):
                if r.names[int(cls)] == "person" and conf >= self.conf_thresh:
                    boxes.append((box.tolist(), float(conf)))
        return boxes
