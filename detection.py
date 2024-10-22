import cv2
from ultralytics import YOLO
from time import sleep
import numpy as np

class Detector:
    def __init__(self, model_path):
        # Load the YOLO model
        self.model = YOLO(model_path)

    def capture_image(self):
        # Initialize the webcam
        cap = cv2.VideoCapture(0)  # 0 is usually the default camera
        
        if not cap.isOpened():
            print("Error: Could not open webcam.")
            return None
		
        for i in range(30):
			# Capture a single frame
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame.")
                cap.release()
                return None
            
        #frame = np.clip(frame - 20, 0, 255).astype(np.uint8)
        # Release the webcam after capturing the image
        cap.release()
        return frame

    def detect_objects(self, frame):
        # Perform inference
        results = self.model(frame)
        output = None
		
        # Draw bounding boxes and labels on the image
        for result in results:  # Iterate over each result
            boxes = result.boxes.xyxy  # Bounding boxes in (x1, y1, x2, y2)
            scores = result.boxes.conf  # Confidence scores
            labels = result.boxes.cls  # Class labels (indices)
            #print(labels, scores)
            for box, score, label in zip(boxes, scores, labels):
                if score >= 0.82:  # Confidence threshold
                    x1, y1, x2, y2 = map(int, box)  # Convert to integer
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Draw bounding box
                    label_text = f'{"Fresh Orange" if int(label) == 0 else "Rotten Orange"} {score:.2f}'
                    cv2.putText(frame, label_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                    output = ("Fresh Orange" if int(label) == 0 else "Rotten Orange")

        return frame, output

    def run(self):
        # Capture an image from the webcam
        frame = self.capture_image()
        if frame is None:
            return

        # Detect objects in the captured frame
        detected_frame, output = self.detect_objects(frame)

        # Show the image with detected objects
        cv2.imshow('Object Detection', detected_frame)
        
        cv2.waitKey(3000)
        cv2.destroyAllWindows()
        
        return output

# Example usage
if __name__ == "__main__":
    detector = Detector('./orange_ncnn_model')  # Replace with your model path
    detector.run()
