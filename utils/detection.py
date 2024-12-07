import cv2
from ultralytics import YOLO
from utils.bom_reader import BOMReader

class ObjectDetector:
    def __init__(self):
        self.model = YOLO("best.pt")
        self.names = self.model.model.names
        self.bom_reader = BOMReader()
        self.current_part_info = None

    def process_frame(self, frame):
        frame = cv2.resize(frame, (1020, 600))
        results = self.model.track(frame, persist=True)

        if results[0].boxes is not None and results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.int().cpu().tolist()
            class_ids = results[0].boxes.cls.int().cpu().tolist()
            track_ids = results[0].boxes.id.int().cpu().tolist()

            for box, class_id, track_id in zip(boxes, class_ids, track_ids):
                class_name = self.names[class_id]
                x1, y1, x2, y2 = box
                
                # Update part information when a new part is detected
                self.current_part_info = self.bom_reader.get_part_info(class_name)
                
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f'{track_id} - {class_name}', (x1, y1 - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1)

        return frame

    def get_current_part_info(self):
        return self.current_part_info or {
            'customer': 'Unknown',
            'program': 'Unknown',
            'part_number': 'Unknown',
            'description': 'Unknown'
        }