from ultralytics import YOLO


class YOLOAgent:

    VEHICLE_CLASSES = {
        "car",
        "bus",
        "truck",
        "motorcycle"
    }

    def __init__(self, model_path="yolov8n.pt"):

        print(f"Loading model: {model_path}")

        self.model = YOLO(model_path)

    def detect(self, frame):

        results = self.model.predict(
            frame,
            verbose=False
        )

        detections = []

        result = results[0]

        for box in result.boxes:

            class_id = int(box.cls[0])
            class_name = self.model.names[class_id]

            # Keep only vehicle classes
            if class_name not in self.VEHICLE_CLASSES:
                continue

            x1, y1, x2, y2 = box.xyxy[0].tolist()

            detections.append({

                "class": class_name,
                "confidence": float(box.conf[0]),
                "bbox": [
                    int(x1),
                    int(y1),
                    int(x2),
                    int(y2)
                ]

            })

        return detections