import cv2
import logging
from ultralytics import YOLO

class AircraftDetector:
    def __init__(self, config):
        self.config = config['detection']
        self.model = None
        self.classes = self.config.get('classes', [4]) # Default 4 is airplane in COCO
        self.confidence = self.config.get('confidence_threshold', 0.5)

    def load_model(self):
        try:
            logging.info(f"Loading YOLO model: {self.config['model_path']}")
            self.model = YOLO(self.config['model_path'])
            return True
        except Exception as e:
            logging.error(f"Detection: Error loading model: {e}")
            return False

    def detect(self, frame):
        if self.model is None:
            return []

        results = self.model(frame, verbose=False)
        detections = []

        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                
                if cls in self.classes and conf >= self.confidence:
                    x1, y1, x2, y2 = box.xyxy[0]
                    detections.append({
                        'bbox': [int(x1), int(y1), int(x2), int(y2)],
                        'confidence': conf,
                        'class_id': cls,
                        'label': self.model.names[cls]
                    })
        
        return detections

    def draw_detections(self, frame, detections):
        for det in detections:
            x1, y1, x2, y2 = det['bbox']
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label = f"{det['label']} {det['confidence']:.2f}"
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        return frame
